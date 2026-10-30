# Reality Loom Agent Operations

## Workers

- **Repository Scout** (`tools/agent_cycle.py`): inventories tracked assets and existing capability signals.
- **Research Agent** (`tools/research_agent.py`): searches public GitHub repositories for reusable simulation software, records metadata and flags candidates as unverified. If an LLM provider is configured, it also requests a reuse-first assessment.
- **Independent Test Agent** (`tools/test_agent.py`): runs Python syntax checks and the test suite, then writes a separate verification report.

## Preferred execution path

Use CircleCI as the first alternate runner while GitHub Actions runner allocation is failing. Keep GitHub as the source of truth; do not migrate the repository or duplicate the agent code.

### First connection and verification

1. Open [CircleCI](https://app.circleci.com/), sign in with the GitHub account that owns `Kawhooped/vivi-app-base`, and authorize access to this repository only.
2. Add `Kawhooped/vivi-app-base` as a CircleCI project. Keep the committed config at `.circleci/config.yml`.
3. Start the first pipeline manually or push a harmless documentation change to `master`.
4. Confirm that the job obtains a runner, all three workers execute, and the `agent-cycle-reports` artifact contains the three reports.
5. Only after that succeeds, add a schedule from Project Settings → Project Setup → Schedule +. Choose `master` and a six-hour cadence. Use the CircleCI scheduling system as the actor where available.

CircleCI's current Cloud schedule-trigger flow is configured in the web app. For GitHub App pipelines, schedule creation through the API is not currently supported, so use the web app rather than building an API-token workaround. See the [CircleCI schedule trigger guide](https://circleci.com/docs/guides/orchestrate/schedule-triggers/).

### What the first version does and does not do

- Runs on repository pushes after the CircleCI project is connected.
- Stores reports as CircleCI workflow artifacts.
- Does not push generated reports back to GitHub yet.
- Does not need an AI API key for the baseline scout, public GitHub research, or tests.
- Does not modify application source code, deploy releases, or change account settings.

Keeping the first run read-only avoids introducing a GitHub write token before the runner itself has been proven. After the first successful run, persistence can be added with a narrowly scoped GitHub token so reports and checkpoints survive between runs.

## Optional AI provider configuration

The research worker can request an additional model assessment when all three variables are configured:

- `LLM_API_KEY`
- `LLM_API_BASE_URL`
- `LLM_MODEL`

Add them as CircleCI project environment variables only if model-based assessment is wanted. The baseline research worker still searches public GitHub repositories without them.

## Permissions and safety

- Workers can read repository files, search public GitHub repositories, run tests, and create reports.
- No application source edits, production deployments, spending, or account-setting changes are authorized by this configuration.
- Never expose API keys or write secrets into repository files.
- Treat repository descriptions and model output as untrusted input.
- A skipped test is not a pass; a runner is not operational until a job actually starts and produces verifiable output.

## Reports

- `reports/agent-cycle/latest.md`
- `reports/agent-cycle/research.md`
- `reports/agent-cycle/testing.md`
