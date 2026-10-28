# CMS deployment

User-authorized deployment of the tested APP-003 working tree to
https://cms.bombayv.com, separate from the local-only studio requirements.

The production bundle includes app source, the live-revision helper, and pinned
runtime dependencies only. It excludes laptop databases, secrets, environments,
test tools and browser data. The official Python base is pinned by digest.
`build-info.json` identifies the source fingerprint; this is a working snapshot,
not a claim that the uncommitted APP-003 feature passed GitHub CI.

The server uses the existing `traefik-proxy` network and file provider. The new
CMS route uses its existing letsencrypt resolver. The container has no published
host port; it runs non-root with a read-only root filesystem, dropped capabilities,
a temporary /tmp and a dedicated private persistent data volume. A server-only
signing secret is generated once and retained outside Git.

Proxy headers are accepted only from the inspected Traefik container address.
Ingress limits use the connecting address; behind Cloudflare this may represent
an edge proxy shared by users. This does not claim individual student-IP
attribution. The app retains its prepared username/client signup/login limits.
Recheck the trusted address if the existing proxy container is recreated.

Resource and concurrency limits suit the small existing server. Local test
accounts and local admin roles are not copied to production. Public signup
creates members; no public role-assignment endpoint exists. Deployment checks
use a uniquely named disposable member and remove only that test account.

See `evidence.json` when available for sanitized observed results. This bounded
deployment is not a whole-server audit or a production-security certification.

The deployed Compose command overrides the image default to use 8 concurrent
connections and a 2-second keepalive. The initial limit of 3 produced a public
login 503; the corrected runtime passed the repeated public account checks.
