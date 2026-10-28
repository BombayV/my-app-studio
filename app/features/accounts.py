"""APP-002 account pages and APIs share the prepared guarded security services."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from app import security
from app.schemas import LoginInput, PublicUser, SignupInput

router = APIRouter()
CurrentUser = Annotated[dict, Depends(security.require_user)]


def api_csrf(request: Request) -> None:
    """Require a same-origin synchronizer token for every state-changing API."""
    security.require_csrf(request, request.headers.get("X-CSRF-Token"))


@router.get("/api/csrf")
def csrf(request: Request, response: Response):
    """Return a CSRF token without exposing the HttpOnly session cookie."""
    return {"csrf_token": security.csrf_token(request, response)}


@router.post(
    "/api/signup",
    status_code=201,
    response_model=PublicUser,
    dependencies=[Depends(api_csrf)],
)
def signup_api(request: Request, credentials: SignupInput):
    """Validate public inputs and create only a member account."""
    security.limit_signup(request)
    return security.signup(
        request.app.state.settings, credentials.username, credentials.password
    )


@router.post("/api/login", response_model=PublicUser, dependencies=[Depends(api_csrf)])
def login_api(request: Request, response: Response, credentials: LoginInput):
    """Issue a signed session cookie; JSON contains only public user fields."""
    return security.login(request, response, credentials.username, credentials.password)


@router.get("/api/me", response_model=PublicUser)
def current_user_api(user: CurrentUser):
    """Protect private API content with 401 rather than a browser redirect."""
    return user


@router.post("/api/logout", dependencies=[Depends(api_csrf)])
def logout_api(request: Request, response: Response, _user: CurrentUser):
    """Revoke the session on the server before clearing the browser cookie."""
    security.logout(request, response)
    return {"status": "logged_out"}


def account_page(request, mode, *, status=200, error=None, username=""):
    """Render an accessible form with CSRF state and never refill a password."""
    cookie_response = Response()
    token = security.csrf_token(request, cookie_response)
    response = request.app.state.templates.TemplateResponse(
        request=request,
        name="account.html",
        context={
            "mode": mode,
            "csrf_token": token,
            "error": error,
            "username": username,
        },
        status_code=status,
    )
    if "set-cookie" in cookie_response.headers:
        response.headers.append("set-cookie", cookie_response.headers["set-cookie"])
    return response


@router.get("/signup", include_in_schema=False)
def signup_page(request: Request):
    """Let anonymous visitors create an account, or reuse their active session."""
    if security.authenticate(request):
        return RedirectResponse("/dashboard", status_code=303)
    return account_page(request, "signup")


@router.get("/login", include_in_schema=False)
def login_page(request: Request):
    """Show login only when there is no valid active session."""
    if security.authenticate(request):
        return RedirectResponse("/dashboard", status_code=303)
    return account_page(request, "login")


async def form_credentials(request, model):
    """Bound form fields and reject extra properties, including public role input."""
    async with request.form(max_files=0, max_fields=3, max_part_size=4096) as form:
        security.require_csrf(request, form.get("csrf_token"))
        if any(len(form.getlist(key)) != 1 for key in form):
            raise HTTPException(422, "Submit each field once.")
        return model.model_validate(
            {key: value for key, value in form.items() if key != "csrf_token"}
        )


@router.post("/signup", include_in_schema=False)
async def signup_form(request: Request):
    """Use the same member creation and limits as JSON signup."""
    credentials = None
    try:
        credentials = await form_credentials(request, SignupInput)
        security.limit_signup(request)
        security.signup(
            request.app.state.settings, credentials.username, credentials.password
        )
    except ValidationError:
        return account_page(
            request,
            "signup",
            status=422,
            error="Use 3–32 letters, numbers or underscores for your username "
            "and a password of 15–128 characters. Extra fields are not allowed.",
        )
    except HTTPException as error:
        response = account_page(
            request,
            "signup",
            status=error.status_code,
            error=error.detail,
            username=credentials.username if credentials else "",
        )
        response.headers.update(error.headers or {})
        return response
    return RedirectResponse("/login", status_code=303)


@router.post("/login", include_in_schema=False)
async def login_form(request: Request):
    """Recover from wrong credentials without reflecting the supplied password."""
    credentials = None
    response = RedirectResponse("/dashboard", status_code=303)
    try:
        credentials = await form_credentials(request, LoginInput)
        security.login(request, response, credentials.username, credentials.password)
    except ValidationError:
        return account_page(
            request, "login", status=422, error="Enter a valid username and password."
        )
    except HTTPException as error:
        response = account_page(
            request,
            "login",
            status=error.status_code,
            error=error.detail,
            username=credentials.username if credentials else "",
        )
        response.headers.update(error.headers or {})
    return response


@router.get("/dashboard", include_in_schema=False)
def dashboard(request: Request):
    """Revalidate the session before rendering any private browser content."""
    user = security.authenticate(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)
    response = Response()
    token = security.csrf_token(request, response)
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"user": user, "csrf_token": token},
    )


@router.post("/logout", include_in_schema=False)
async def logout_form(request: Request):
    """Revoke authenticated browser sessions through a CSRF-protected POST."""
    if security.authenticate(request) is None:
        return RedirectResponse("/login", status_code=303)
    async with request.form(max_files=0, max_fields=1, max_part_size=4096) as form:
        security.require_csrf(request, form.get("csrf_token"))
    response = RedirectResponse("/login", status_code=303)
    security.logout(request, response)
    return response
