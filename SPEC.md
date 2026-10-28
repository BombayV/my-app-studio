# App Studio decisions

The durable agreement between learner and AI. Update only agreed decisions and
actual evidence; pending is a valid state. Keep explanations/help in
[LEARNING.md](LEARNING.md), not a second copy here.

## Current stage

- **Current feature:** APP-002.
- **Status:** APP-001 merged as PR #2, issue #1 closed, both PR and post-merge CI jobs passed; approved learner-evidence gaps remain. APP-002 account flow implemented; full local cumulative checks and AI review passed. Learner reported redirect to login after logout, chose to keep the flow and approved the summary; AI-assisted interpretation is disclosed. GitHub completion pending.
- **Next step:** Publish the reviewed APP-002 PR and verify both CI jobs before the learner decides to merge.
- **Implementation marker:** `studio.json` is `implemented_through: 2`, advanced after explicit APP-002 checks passed; normal full checks including the added route/narrow-form regressions then passed.

This repository owns application code. Server/proxy changes and production
deployment are outside these three local-development lessons. Prepared helpers
are reusable foundations, not evidence that unfinished routes are implemented.

## APP-001 · Branded homepage

**Scope:** make the neutral FastAPI homepage express one chosen identity with
a simple original SVG mark, coherent copy, navigation and shared style tokens.
Keep account actions honest about their unfinished state.

| Decision | Agreement |
|---|---|
| Visitor and concrete use situation | Students finding important assignment links; when an issue arises, finding how to contact a professor. |
| Reused IS117 brand, or name / promise / primary archetype | MSR26 CMS; “Your coursework and professor contacts, in one place.” Clear, helpful Sage/guide identity (AI suggestion adopted by learner). |
| One visible choice and visitor benefit | Separate Assignments and Professor contacts sections so students can handle work and find help. Learner clarified the intended contact is a professor. AI-proposed navy/cream/teal field-guide styling and original book/bookmark SVG. Informational homepage only: no actual email sending or stored assignment links. Learner expected the original CTA to open `/register`; approved renaming it “Explore the planned tools” to clarify the current in-page destination. |
| Own issue / branch / PR | [APP-001 issue #1](https://github.com/BombayV/my-app-studio/issues/1); `codex/app-001-msr26-homepage`; [PR #2](https://github.com/BombayV/my-app-studio/pull/2). |

**Keep when:** the agreed identity is visible and usable at desktop/narrow widths;
full foundation + APP-001 checks pass; AI review and the learner's actual check
interpretation/browser observation/keep reason are recorded; reviewed evidence
and verified GitHub state are linked below.

## APP-002 · Signup, login and logout

**Scope:** add browser forms and REST behavior for member signup, login, a private
dashboard and logout backed by SQLite. Reuse the prepared password/JWT/CSRF/session
helpers; keep data local. New accounts cannot choose their role.

| Decision | Agreement |
|---|---|
| Expected public/private behavior and account flow | Username/password signup creates members; login opens a private dashboard; logout revokes the session. Without a valid session, private HTML redirects to `/login`; private API returns 401. Valid sessions reach private content. Prepared hashing, HttpOnly cookie, CSRF and SQLite helpers are reused. No admin routes, assignment management or emailing. |
| Valid and rejected cases to demonstrate | Valid signup/login; invalid/duplicate signup, role injection and wrong credentials rejected; missing/invalid CSRF rejected; no-session requests and revoked-token replay rejected. |
| Own issue / branch / PR | [APP-002 issue #3](https://github.com/BombayV/my-app-studio/issues/3); `codex/app-002-accounts`; [PR #4](https://github.com/BombayV/my-app-studio/pull/4). |

**Keep when:** the agreed forms/API work; duplicate/invalid signup and wrong
credentials are rejected; passwords are hashed; authentication uses validated,
expiring JWTs with protected cookies and CSRF; private requests require a live
session and logout revokes it. Full cumulative checks, AI review, actual learner
contributions and GitHub state are recorded. This is not a production-security certification.

## APP-003 · Server-enforced roles

**Scope:** enforce a small member/admin boundary in the API and browser. Assign
roles only through the trusted local terminal command; use current server-side
permissions, including for an existing session after a role change.

| Visitor | Homepage | Member area | Admin area/API |
|---|---|---|---|
| Anonymous | Allowed | Login required | Login required |
| Member | Allowed | Allowed | Forbidden |
| Admin | Allowed | Allowed | Allowed |

| Decision | Agreement |
|---|---|
| Intended admin-only result | Pending |
| Actual allowed/denied request evidence | Pending |
| Own issue / branch / PR | Pending |

**Keep when:** a direct request cannot bypass the role boundary, role changes
take effect as specified, new signup remains member-only, and full cumulative
checks plus AI review pass. Link the learner's actual interpretation/observation,
reviewed record and verified GitHub result. Hidden navigation alone is insufficient.

## Evidence

Link actual files/checks and the student's own issues/PRs. No fabricated URLs,
customer research or claims that a timestamp proves learning.

| Feature | Files / own issue / PR | Actual checks and learner observations | Kept / GitHub state |
|---|---|---|---|
| APP-001 | [Issue #1](https://github.com/BombayV/my-app-studio/issues/1); [brand brief](app/brand.json), [homepage](app/templates/home.html), [shared navigation](app/templates/base.html), [styles](app/static/site.css), [SVG mark](app/static/logo.svg). [PR #2](https://github.com/BombayV/my-app-studio/pull/2); [initial CI run](https://github.com/BombayV/my-app-studio/actions/runs/40558665254). | Full `check --lesson APP-001`, then normal `check` after marker update: Black/Pylint, 98 foundation tests, 2 homepage contracts, 2 Chromium journeys passed. AI reviewed 1280px desktop and 390px narrow rendering/keyboard/anchor behavior. Learner saw the neutral navbar, hero, footer and CTA, and predicted separate work/contact sections would help students. Learner reported “Everything looks good” and requested moving on. Specific branded-page observation and independent check interpretation remain unrecorded in the approved summary. | Learner authorized keep/publication; [PR #2](https://github.com/BombayV/my-app-studio/pull/2) merged; issue #1 closed. [PR CI](https://github.com/BombayV/my-app-studio/actions/runs/40558731479) and [post-merge CI](https://github.com/BombayV/my-app-studio/actions/runs/40559385606) passed both check/windows. Learner gaps preserved. |
| APP-002 | [Issue #3](https://github.com/BombayV/my-app-studio/issues/3); [routes](app/features/accounts.py), [account forms](app/templates/account.html), [dashboard](app/templates/dashboard.html), [route regressions](tests/test_account_routes.py), [browser journeys](tests/browser/test_browser.py); [PR #4](https://github.com/BombayV/my-app-studio/pull/4); [initial CI run](https://github.com/BombayV/my-app-studio/actions/runs/40694920697). | Full cumulative and normal checks passed: Black/Pylint, 102 foundation/regression tests, 14 contracts, 4 Chromium cases. Actual checks cover member-only signup, password hashing, valid/wrong login, CSRF and rotation, missing/malformed/expired sessions, HTML redirect vs API 401, logout and copied-cookie replay, database persistence, mobile form layout and keyboard access. AI reviewed rendered desktop login and narrow signup pages. The extra HTML role field is rejected with 400 by the three-field form parser; API role input returns 422. | Learner approved keeping/publication; observed return to login after logout and explained that returning users can log in again. AI-assisted check interpretation is disclosed in LEARNING.md. PR opened; latest Linux/Windows checks and merge pending. |
| APP-003 | Pending | Unfinished; explicit contracts not yet passed | Pending |

The instructor's reference branches show possible implementations. They do not
establish this repository's completion or the learner's own reasoning.
