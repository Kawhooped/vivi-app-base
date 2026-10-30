#!/usr/bin/env python3
"""Reality Loom's lightweight, scheduled system monitor.

Checks repository invariants, HTML integrity, public Pages endpoints, and the
latest Pages workflow. Writes a machine-readable status for the Control Center.
"""
from __future__ import annotations
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "control-center" / "status.json"
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
    req = urllib.request.Request(url, headers={"User-Agent": "RealityLoom-Monitor/1.0", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        body = response.read(1_000_000)
        return response.status, body.decode("utf-8", "replace")

def check(name: str, fn):
    try:
        detail = fn()
        return {"name": name, "status": "pass", "detail": str(detail)[:500]}
    except Exception as exc:
        return {"name": name, "status": "fail", "detail": str(exc)[:500]}

def main():
    results = []
    results.append(check("Required project files", lambda: (
        [p for p in REQUIRED if not (ROOT / p).is_file()] or f"{len(REQUIRED)} required files present"
    ) if not [p for p in REQUIRED if not (ROOT / p).is_file()] else (_ for _ in ()).throw(
        RuntimeError("Missing: " + ", ".join(p for p in REQUIRED if not (ROOT / p).is_file()))
    )))

    def html_check():
        target = ROOT / "docs/control-center/index.html"
        parser = HTMLAudit()
        parser.feed(target.read_text(encoding="utf-8"))
        if parser.errors:
            raise RuntimeError("; ".join(parser.errors))
        return f"HTML parsed; {len(parser.ids)} unique element IDs"
    results.append(check("Control Center HTML", html_check))

    def links_check():
        for path in ("/", "/reality-loom/", "/control-center/"):
            status, body = fetch(BASE + path)
            if status != 200:
                raise RuntimeError(f"{path}: HTTP {status}")
            if not body.strip():
                raise RuntimeError(f"{path}: empty response")
        return "3 published routes returned HTTP 200"
    results.append(check("Published website routes", links_check))

    def pages_run():
        token = os.getenv("GITHUB_TOKEN", "")
        headers = {"Accept": "application/vnd.github+json"}
        if token:
            headers["Authorization"] = "Bearer " + token
        status, raw = fetch(f"https://api.github.com/repos/{REPO}/actions/workflows/pages.yml/runs?per_page=1", headers)
        data = json.loads(raw)
        runs = data.get("workflow_runs", [])
        if not runs:
            raise RuntimeError("No Pages workflow runs found")
        run = runs[0]
        conclusion = run.get("conclusion") or run.get("status") or "unknown"
        if run.get("status") == "completed" and run.get("conclusion") != "success":
            raise RuntimeError(f"Latest Pages run: {conclusion} ({run.get('html_url','')})")
        return f"Latest Pages run: {conclusion}; {run.get('html_url','')}"
    results.append(check("GitHub Pages deployment", pages_run))

    failed = sum(item["status"] == "fail" for item in results)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    payload = {
        "service": "Reality Loom Autopilot",
        "checked_at": now,
        "overall": "attention" if failed else "healthy",
        "passed": len(results) - failed,
        "failed": failed,
        "checks": results,
        "note": "Scheduled monitor. A healthy result means these checks passed, not that every application feature is defect-free."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    # Monitoring failures are reported, not treated as a monitor crash.
    # The independent test job remains responsible for failing the workflow.
if __name__ == "__main__":
    main()
