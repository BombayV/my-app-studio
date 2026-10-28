# Conversation evidence

AI-drafted task summary, not a transcript or grade. It may be public. Use actual
short words or labeled paraphrases; disclose help and leave missing responses
pending. The learner reviews, corrects or removes new excerpts before commit/push.
Accuracy approval is not proof of understanding. Label simulated trials explicitly.

**Available conversation context:** This coaching chat, 2026-10-27.

## APP-001

- Prediction: Learner chose MSR26 CMS for students finding assignments and contacting professors. Learner predicted that separate sections would help students handle assignments and find help; clarified “professor” after initially saying “student.”
- Check interpretation: Pending. Learner expected the CTA to redirect to `/register`, rather than describing a bug caught by the in-page navigation test.
- Browser observation: Pending. Learner initially noticed the neutral navbar, hero, footer and CTA. After the branded-page inspection request, reported “Everything looks good. Lets move on to the next task”; a specific branded-page detail was not supplied.
- Keep decision: Learner requested moving on after “Everything looks good”; a more specific reason was not supplied.
- Review: Learner approved this summary and publication: “Yes, commit it and lets move on to the next task.”
- Help/gaps: AI suggested the promise “Your coursework and professor contacts, in one place” and Sage/guide voice; learner adopted them. AI built the homepage, SVG and responsive styles, ran full checks and reviewed desktop/narrow/keyboard behavior. AI explained the in-page CTA check and suggested “Explore the planned tools” after the learner expected registration; learner approved the wording. Independent check interpretation and a specific branded-page observation remain unrecorded. No answer is invented from approval.
- Evidence links / next step: [Issue #1](https://github.com/BombayV/my-app-studio/issues/1); [SPEC.md](SPEC.md). Full local APP-001 checks passed. Publish the PR, verify both CI jobs and review for merge before APP-002.

## APP-002

- Prediction: Learner expected protected pages without a valid session to redirect to login. Initially proposed JWT storage in localStorage or cookies; AI clarified that the signing key stays server-side and this app uses the prepared HttpOnly cookie. Learner agreed that valid sessions reach private pages, while unauthenticated APIs return 401.
- Check interpretation: Learner suggested a cache/expiration issue when asked about a copied pre-logout cookie still receiving 200. AI clarified that the check tests server-side session rejection after logout, even when the token is retained.
- Browser observation: After the requested signup/login/dashboard/logout/revisit exercise, learner reported: “You get redirected to login.”
- Keep decision: Learner chose to keep the flow because someone returning to a protected page may already have an account and can log in again (labeled paraphrase).
- Review: Learner approved this APP-002 summary before publication on 2026-10-28: “Yes.”
- Help/gaps: AI connected the prepared security helpers to forms and APIs, ran full checks and reviewed account layouts. AI supplied the server-revocation explanation; independent articulation of that explanation was not recorded. No password, cookie value or signing key is recorded.
- Evidence links / next step: [Issue #3](https://github.com/BombayV/my-app-studio/issues/3), [SPEC.md](SPEC.md). Full local APP-002 checks passed; publish the reviewed PR, verify both CI jobs, then obtain the learner's merge decision.

## APP-003

- Prediction: Learner predicted 403 for a member requesting the admin API directly; clarified that the earlier 401 was an unrelated typing mistake.
- Check interpretation: “It checks for permissions and returns different html depending on the role.”
- Browser observation: On the public CMS, learner saw “Admin access required” as a member, then their username and current role “admin” after trusted promotion, then “admin access required” again after restoration to member without logging out. Learner also observed planned dashboard features linking to the homepage.
- Keep decision: “Yes because it allows the user to know what role it has.” Learner also chose to retain the planned-feature dashboard.
- Review: Learner approved the APP-003 summary before publication on 2026-10-28: “Yes.”
- Help/gaps: AI implemented and checked the role boundary, explained the HTTP statuses, and temporarily changed the named test account through the trusted server-side helper for the requested public comparison, then restored member access. This comparison happened on the separately agreed public deployment. AI drafted this reviewed summary; no password or session value is recorded.
- Evidence links / next step: [Issue #5](https://github.com/BombayV/my-app-studio/issues/5), [SPEC.md](SPEC.md), [public deployment checks](deploy/cms/evidence.json). Full local APP-003 checks passed. Review the diff, publish the PR and verify both CI jobs before a merge decision.
