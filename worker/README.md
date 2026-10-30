# Reality Loom Control Center Worker

Private backend for the static Control Center at `https://kawhooped.github.io/vivi-app-base/control-center/` (adjust if your Pages project uses a different base path).

## Deploy
1. Create a Cloudflare Worker named `reality-loom-control-center`.
2. Upload `src/index.js` as the Worker entry point, or deploy this folder with Wrangler.
3. Set Worker secrets: `OPENAI_API_KEY`, `GATEWAY_TOKEN`, and optionally `GITHUB_TOKEN`.
4. Set variables: `GITHUB_REPO=Kawhooped/vivi-app-base`, `GITHUB_BRANCH=master`, `OPENAI_MODEL=gpt-4.1-mini`, `ALLOW_REPO_WRITES=false`, and `ALLOWED_ORIGIN=https://kawhooped.github.io`.
5. Paste the Worker URL and the same private gateway token into the website's Connections page.

## Capabilities
- `GET /health`: health check.
- `GET /api/actions`: list registered tools.
- `POST /api/agent`: OpenAI Responses API agent with GitHub repository tools.
- Read-only tools: list repository files and read text files.
- Guarded write tool: create/update files only under `docs/control-center/`. It requires both `ALLOW_REPO_WRITES=true` on the Worker and `allow_writes=true` in the request.

## Security
- Never put OpenAI or GitHub credentials in the static website.
- Use a dedicated GitHub token scoped to this repository and only the required contents permissions.
- Keep repository writes disabled until tested.
- Rotate the gateway token if it is exposed. The browser stores it in session storage for the current tab session.
- This first version does not execute arbitrary shell commands, install packages, deploy code, or run arbitrary internet requests.
