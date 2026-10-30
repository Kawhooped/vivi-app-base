#!/usr/bin/env python3
"""Reality Loom system monitor.

Writes reports outside docs/ so monitoring cannot trigger a Pages deployment.
A failed check produces a non-zero exit code; CI still uploads the report.
"""
from __future__ import annotations

from datetime import datetime, timezone
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "system-monitor" / "status.json"
REPO = os.getenv("GITHUB_REPOSITORY", "Kawhooped/vivi-app-base")
BASE = "https://kawhooped.github.io/vivi-app-base"
REQUIRED = [
    "docs/index.html",
    "docs/reality-loom/index.html",
    "docs/control-center/index.html",
    ".github/workflows/pages.yml",
    ".github/workflows/agent-cycle.yml",
    "tools/agent_cycle.py",
    "tools/research_agent.py",
    "tools/test_agent.py",
]


class HTMLAudit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids: set[str] = set()
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key == "id" and value:
                if value in self.ids:
                    self.errors.append(f"duplicate id: {value}")
                self.ids.add(value)


def fetch(url: str, headers: dict | None = None, timeout: int = 15):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "RealityLoom-Monitor/1.1", **(headers or {})},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read(1_000_000)
        return response.status, body.decode("utf-8", "replace")


def check(name: str, fn):
    try:
        return {"name": name, "status": "pass", "detail": str(fn())[:500]}
    except Exception as exc:
        return {"name": name, "status": "fail", "detail": str(exc)[:500]}


def check_required_files():
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        raise RuntimeError("Missing: " + ", ".join(missing))
    return f"{len(REQUIRED)} required files present"


def check_control_center_html():
    parser = HTMLAudit()
    parser.feed((ROOT / "docs/control-center/index.html").read_text(encoding="utf-8"))
    if parser.errors:
        raise RuntimeError("; ".join(parser.errors))
    return f"HTML parsed; {len(parser.ids)} unique element IDs"


def check_published_routes():
    for path in ("/", "/reality-loom/", "/control-center/"):
        status, body = fetch(BASE + path)
        if status != 200:
            raise RuntimeError(f"{path}: HTTP {status}")
        if not body.strip():
            raise RuntimeError(f"{path}: empty response")
    return "3 published routes returned HTTP 200"


def check_pages_workflow():
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN", "")
    if token:
        headers["Authorization"] = "Bearer " + token
    _, raw = fetch(
        f"https://api.github.com/repos/{REPO}/actions/workflows/pages.yml/runs?per_page=1",
        headers,
    )
    runs = json.loads(raw).get("workflow_runs", [])
    if not runs:
        raise RuntimeError("No Pages workflow runs found")
    run = runs[0]
    conclusion = run.get("conclusion") or run.get("status") or "unknown"
    if run.get("status") != "completed" or run.get("conclusion") != "success":
        raise RuntimeError(
            f"Latest Pages run is not successful: {conclusion} "
            f"({run.get('html_url', '')})"
        )
    return f"Latest Pages run succeeded: {run.get('html_url', '')}"


def main():
    results = [
        check("Required project files", check_required_files),
        check("Control Center HTML", check_control_center_html),
        check("Published website routes", check_published_routes),
        check("GitHub Pages deployment", check_pages_workflow),
    ]
    failed = sum(result["status"] == "fail" for result in results)
    payload = {
        "service": "Reality Loom system monitor",
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "overall": "attention" if failed else "healthy",
        "passed": len(results) - failed,
        "failed": failed,
        "checks": results,
        "scope": "These checks do not prove that every simulation feature works.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
