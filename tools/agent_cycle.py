#!/usr/bin/env python3
"""Reality Loom's first scheduled worker: a deterministic repository scout.

This worker inventories existing assets before proposing new implementation.
It deliberately does not modify application source code.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "agent-cycle" / "latest.md"

def git_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return sorted(line for line in result.stdout.splitlines() if line)

def read_text(path: str, limit: int = 12000) -> str:
    target = ROOT / path
    if not target.is_file():
        return ""
    try:
        return target.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""

def main() -> None:
    files = git_files()
    groups = {
        "Reality Loom browser prototype": [p for p in files if "reality-loom" in p.lower() and p.endswith((".html", ".js", ".ts"))],
        "Android integration": [p for p in files if p.endswith((".kt", ".java")) and any(k in p.lower() for k in ("realityloom", "navgraph", "mainscreen"))],
        "GitHub workflows": [p for p in files if p.startswith(".github/workflows/")],
        "Documentation": [p for p in files if p.lower().endswith((".md", ".mdx"))],
        "Dependency manifests": [p for p in files if Path(p).name.lower() in {
            "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
            "gradle/libs.versions.toml", "build.gradle", "build.gradle.kts",
            "settings.gradle", "settings.gradle.kts", "requirements.txt", "pyproject.toml"
        }],
        "Tests": [p for p in files if any(token in p.lower() for token in ("/test", "/tests", "test_", ".test.", ".spec."))],
    }

    html_paths = groups["Reality Loom browser prototype"]
    html_text = "\n".join(read_text(p) for p in html_paths)
    checks = [
        ("Three.js reference", "three" in html_text.lower()),
        ("Rapier physics reference", "rapier" in html_text.lower()),
        ("Module registry reference", "moduleregistry" in html_text.lower()),
        ("Local persistence reference", "localstorage" in html_text.lower()),
        ("Fixed-step accumulator reference", "accumulator" in html_text.lower() or "fixedtimestep" in html_text.lower()),
    ]

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Reality Loom Agent Cycle: Repository Scout",
        "",
        f"**Generated:** {now}",
        "**Worker:** deterministic repository inventory",
        "**Policy:** inspect and reuse before proposing or writing code",
        "",
        "## Repository snapshot",
        f"- Tracked files: {len(files)}",
        f"- Browser prototype files detected: {len(html_paths)}",
        f"- Workflow files detected: {len(groups['GitHub workflows'])}",
        f"- Test-related paths detected: {len(groups['Tests'])}",
        "",
        "## Existing capability signals",
        "| Signal | Detected |",
        "|---|---|",
    ]
    lines.extend(f"| {label} | {'Yes' if found else 'Not detected'} |" for label, found in checks)

    for title, paths in groups.items():
        lines.extend(["", f"## {title}", ""])
        if paths:
            lines.extend(f"- `{p}`" for p in paths[:100])
            if len(paths) > 100:
                lines.append(f"- … and {len(paths) - 100} more")
        else:
            lines.append("- None detected")

    lines.extend([
        "",
        "## Scout assessment",
        "",
        "- This report is an inventory, not proof that a feature works.",
        "- A detected file or dependency must be inspected and tested before it is marked verified.",
        "- No application source files were changed by this worker.",
        "- New implementation is blocked until an audit identifies a genuine missing capability.",
        "",
        "## Next audit targets",
        "",
        "1. Inspect the browser prototype and verify module lifecycle wiring.",
        "2. Inspect Android navigation and WebView configuration.",
        "3. Identify dependency versions and license obligations.",
        "4. Locate existing automated tests and establish actual build status.",
        "5. Compare candidate external modules against the existing inventory.",
        "",
    ])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(files)} tracked files.")

if __name__ == "__main__":
    main()
