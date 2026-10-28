"""APP-003 checks current server-side permissions on every admin request."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse

from app import security

router = APIRouter()
AdminUser = Annotated[dict, Depends(security.require_admin)]


@router.get("/api/admin")
def admin_api(user: AdminUser):
    """Require the current database role, not navigation visibility or JWT claims."""
    return {
        "message": "Administration access confirmed.",
        "username": user["username"],
        "role": user["role"],
    }


@router.get("/admin", include_in_schema=False)
def admin_page(request: Request):
    """Redirect missing sessions and show a genuine 403 page to members."""
    user = security.authenticate(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)
    allowed = user["role"] == "admin"
    token = security.csrf_token(request, Response())
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={"allowed": allowed, "user": user, "csrf_token": token},
        status_code=200 if allowed else 403,
    )
