# App Studio decisions

The durable agreement between learner and AI. Update only agreed decisions and
actual evidence; pending is a valid state. Keep explanations/help in
[LEARNING.md](LEARNING.md), not a second copy here.

## Current stage

- **Current feature:** APP-001.
- **Status:** APP-001 homepage implemented; full local checks and AI layout/keyboard review passed. Learner requested keeping the result and moving on; approved summary records the remaining interpretation/observation gaps. GitHub completion pending.
- **Next step:** Publish the reviewed APP-001 PR, verify both CI jobs and review for merge.
- **Implementation marker:** `studio.json` is `implemented_through: 1`, set only after explicit APP-001 checks passed; normal full checks then passed again.

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
| Expected public/private behavior and account flow | Pending |
| Valid and rejected cases to demonstrate | Pending |
| Own issue / branch / PR | Pending |

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
| APP-001 | [Issue #1](https://github.com/BombayV/my-app-studio/issues/1); [brand brief](app/brand.json), [homepage](app/templates/home.html), [shared navigation](app/templates/base.html), [styles](app/static/site.css), [SVG mark](app/static/logo.svg). [PR #2](https://github.com/BombayV/my-app-studio/pull/2); [initial CI run](https://github.com/BombayV/my-app-studio/actions/runs/40558665254). | Full `check --lesson APP-001`, then normal `check` after marker update: Black/Pylint, 98 foundation tests, 2 homepage contracts, 2 Chromium journeys passed. AI reviewed 1280px desktop and 390px narrow rendering/keyboard/anchor behavior. Learner saw the neutral navbar, hero, footer and CTA, and predicted separate work/contact sections would help students. Learner reported “Everything looks good” and requested moving on. Specific branded-page observation and independent check interpretation remain unrecorded in the approved summary. | Learner authorized keep/publication; PR opened; both CI jobs and merge pending. Latest checks are linked from PR #2. |
| APP-002 | Pending | Unfinished; explicit contracts not yet passed | Pending |
| APP-003 | Pending | Unfinished; explicit contracts not yet passed | Pending |

The instructor's reference branches show possible implementations. They do not
establish this repository's completion or the learner's own reasoning.
