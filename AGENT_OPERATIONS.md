# Reality Loom Agent Operations

## Workers

- **Repository Scout** (`tools/agent_cycle.py`): inventories tracked assets and existing capability signals.
- **Research Agent** (`tools/research_agent.py`): searches public GitHub repositories for reusable simulation software, records metadata and flags candidates as unverified. If an LLM provider is configured, it also requests a reuse-first assessment.
- **Independent Test Agent** (`tools/test_agent.py`): runs Python syntax checks and the test suite, then writes a separate verification report.

## Execution options

### GitHub Actions

The GitHub Actions workflow is intended to run every six hours and can also be started manually. It can commit generated reports only. It does not rewrite application source code or change repository settings.

### CircleCI fallback

A second runner configuration is available at `.circleci/config.yml`. To use it if GitHub-hosted runners remain unavailable:

1. Sign in to CircleCI and connect the GitHub account that owns `Kawhooped/vivi-app-base`.
2. Add the repository as a CircleCI project and use `.circleci/config.yml` as its config.
3. In CircleCI Project Settings, add `LLM_API_KEY`, `LLM_API_BASE_URL`, and `LLM_MODEL` as environment variables if model-based research is wanted.
4. In Project Settings → Triggers, create a schedule for the `master` branch (for example, every six hours).

CircleCI stores each run's reports as workflow artifacts. This fallback does not push reports back into GitHub. It runs on pushes and on the schedule configured in CircleCI. Schedule triggers are configured in CircleCI's web app.

## Optional AI provider configuration

For GitHub Actions, add `LLM_API_KEY` as a repository secret and `LLM_API_BASE_URL` and `LLM_MODEL` as repository variables.

For CircleCI, add the same three names as project environment variables.

Without all three, the research worker still performs real GitHub repository discovery and records that model-based analysis was skipped. No provider is hard-coded.

## Permissions and safety

Workers do not receive permission to rewrite application source code, deploy releases, or change repository settings. The GitHub Actions workflow can commit generated reports only. CircleCI stores reports as artifacts. Candidate repositories are unverified until source, compatibility, security and license checks are completed.

## Reports

- `reports/agent-cycle/latest.md`
- `reports/agent-cycle/research.md`
- `reports/agent-cycle/testing.md`
