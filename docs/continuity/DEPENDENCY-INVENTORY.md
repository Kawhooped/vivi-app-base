# Continuity Architecture: Dependency Inventory

Last reviewed: 2026-10-30
Repository: `Kawhooped/vivi-app-base`
Purpose: identify what Reality Loom needs to operate, how each dependency is checked, and what happens when it fails.

## Status meanings

- **Present**: configuration or implementation exists in the repository.
- **Unverified**: configured or planned, but no successful live test has been recorded.
- **External action required**: requires account access, credentials, or setup outside this repository.
- **Fallback**: a recovery path exists but must be tested before it is trusted.

## Dependency register

| Dependency | Required for | Current evidence | Failure mode | Recovery / fallback | Verification |
|---|---|---|---|---|---|
| GitHub repository | Source of truth, version history, code delivery | Repository and `master` branch are present | GitHub/API unavailable, permissions denied, branch conflict | Keep local/exported source snapshot; retry API operations; use another authorized Git client | Read repository metadata and fetch known files; verify latest commit |
| GitHub Pages | Public browser access to the static site | Pages workflow exists; earlier deployments failed | Build/deploy failure, 404/403, stale publication | Keep source in Git; deploy the same `docs/` artifact to an alternate static host | HTTP check plus browser-level smoke test for all required routes |
| GitHub Actions | Pages deployment and Android build automation | Workflows exist; runner allocation has previously failed | Runner unavailable, workflow failure, permissions issue | Use CircleCI for read-only checks; keep deploy workflow separate | A run must acquire a runner, execute steps, and produce artifacts |
| CircleCI | Alternate automation runner | `.circleci/config.yml` and setup instructions exist | Project not connected, schedule absent, job failure | GitHub Actions remains a secondary runner when healthy | Connect project, run manually, inspect all three reports, then schedule |
| Cloudflare Worker | Private Control Center gateway | Worker source and Wrangler config exist | Not deployed, missing secrets, CORS/auth errors, provider outage | Control Center remains static/read-only; retain source and redeploy from repository; later add a second gateway only if justified | `/health`, authenticated `/api/actions`, then a read-only agent request |
| OpenAI API | Model reasoning inside the Worker | Worker expects `OPENAI_API_KEY` | Missing/invalid key, quota, rate limit, API outage | Disable AI-dependent actions; keep deterministic checks and manual operation available | Authenticated test request with safe read-only task |
| GitHub API token | Worker repository access and optional automation writes | Worker expects `GITHUB_TOKEN`; agent workflow uses built-in token | Missing scope, expiry/revocation, rate limit | Read public repository data where possible; keep writes disabled | Read a known file; verify denied writes remain denied |
| Browser storage | Local simulation state and session gateway settings | Reality Loom uses browser-side state; Worker README says token is session-stored | Cleared storage, private browsing, browser/device loss | Export/import simulation state; never treat browser storage as the only durable copy | Save, reload, restore, and export/import test |
| Android build environment | Installable Android application | Kotlin/Compose project and Android workflow exist | Runner failure, dependency resolution, signing/configuration missing | Browser version remains usable; build from another runner or local Android toolchain | Build APK, verify artifact, install and launch |
| Third-party libraries/CDNs | Browser simulation rendering and physics | Browser prototype imports external libraries | CDN outage, version change, network blocked | Pin versions and add locally hosted copies of critical libraries | Load with CDN blocked; confirm local fallback |
| Persistent task/report storage | Resume work and retain evidence between runs | CircleCI artifacts and repository reports are configured in parts | Artifact expiry, failed commit, lost browser state | Durable versioned reports in Git or independent object storage | Restart a run and recover its last verified checkpoint |
| DNS/TLS/network | Reach public site and APIs | Public GitHub Pages URL is configured in project | DNS/TLS/network/provider outage | Alternate host and locally usable project copy | Resolve hostname, validate TLS, request health endpoint |

## Operating rules

1. Never mark a dependency operational because its configuration file exists.
2. Every critical dependency needs a live health check and a last-verified timestamp.
3. Keep source, deployment, monitoring, and task reports separate. Monitoring output must not trigger a deployment loop.
4. Use bounded retries with backoff. After repeated failure, switch to a tested fallback or stop safely.
5. Preserve the last known-good version before changing configuration or deploying.
6. Keep secrets outside the repository. Test permissions with the least privilege required.
7. A fallback is not trusted until a deliberate failure test proves it works.
8. Do not allow an unavailable external service to erase local work or block unrelated local tasks.

## Initial priority

**P0 — Restore a verified operating path**
- Verify GitHub source access.
- Get one automation runner to complete a full read-only cycle.
- Verify public hosting independently from automation.
- Remove monitoring writes from the published `docs/` tree.
- Verify the Worker only after its deployment and secrets are configured.

**P1 — Add continuity**
- Add a durable task queue and checkpoints.
- Add local copies of critical browser dependencies.
- Add export/import for simulation state and configuration.
- Test alternate hosting and recovery from a failed runner.

## Acceptance test

The foundation is considered operational only when:
- The site loads and its core simulation works.
- A scheduled runner completes seven consecutive cycles.
- Each cycle produces independently verifiable reports.
- A deliberately disabled primary dependency triggers the documented fallback.
- No monitoring run causes an unintended deployment.
- A restart resumes from the last verified checkpoint.
