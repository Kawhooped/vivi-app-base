# Reality Loom Agent Operations

## Workers

- **Repository Scout** (`tools/agent_cycle.py`): inventories tracked assets and existing capability signals.
- **Research Agent** (`tools/research_agent.py`): searches public GitHub repositories for reusable simulation software, records metadata and flags candidates as unverified. If an LLM provider is configured, it also requests a reuse-first assessment.
- **Independent Test Agent** (`tools/test_agent.py`): runs Python syntax checks and the test suite, then writes a separate verification report.

## Schedule

The GitHub Actions workflow runs every six hours and can also be started manually. GitHub scheduled execution is periodic, not continuous, and GitHub may delay scheduled jobs. This is not a 24/7 resident process.

## Optional AI provider configuration

To enable model-based analysis, add this repository Actions secret and these Actions variables:

- `LLM_API_KEY`
- Actions variable `LLM_API_BASE_URL` (OpenAI-compatible API base URL, without `/chat/completions`)
- Actions variable `LLM_MODEL`

Without all three, the research worker still performs real GitHub repository discovery and records that model-based analysis was skipped. No provider is hard-coded.

## Permissions and safety

The workflow can commit generated reports only. Workers do not receive permission to rewrite application source code, deploy releases, or change repository settings. Candidate repositories are unverified until source, compatibility, security and license checks are completed.

## Reports

- `reports/agent-cycle/latest.md`
- `reports/agent-cycle/research.md`
- `reports/agent-cycle/testing.md`
