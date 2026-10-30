#!/usr/bin/env python3
"""Independent verifier for the Reality Loom scheduled agent workers."""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import py_compile
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "agent-cycle" / "testing.md"

def run(command: list[str], timeout: int = 900) -> tuple[int, str]:
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        output = (result.stdout + "\n" + result.stderr).strip()
        return result.returncode, output[-12000:]
    except subprocess.TimeoutExpired as exc:
        return 124, "Timed out: " + str(exc)[-12000:]

def main() -> int:
    checks: list[tuple[str, int, str]] = []
    python_files = sorted((ROOT / "tools").glob("*.py")) + sorted((ROOT / "tests").glob("*.py"))
    compile_errors = []
    for path in python_files:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            compile_errors.append(str(exc))
    checks.append(("Python syntax", 1 if compile_errors else 0, "\n".join(compile_errors) or f"Compiled {len(python_files)} Python files."))

    test_code, test_output = run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], timeout=180)
    checks.append(("Unit tests", test_code, test_output or "No test output."))

    wrapper = ROOT / "gradlew"
    if wrapper.is_file():
        wrapper.chmod(wrapper.stat().st_mode | 0o111)
        gradle_code, gradle_output = run(["./gradlew", ":app:assembleDebug", "--no-daemon"], timeout=900)
        checks.append(("Android debug build", gradle_code, gradle_output or "No Gradle output."))
    else:
        checks.append(("Android debug build", 0, "SKIPPED: Gradle wrapper not found at repository root."))

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Reality Loom Independent Test Agent", "",
        f"**Generated:** {now}",
        f"**Python files inspected:** {len(python_files)}", "",
        "| Check | Result |", "|---|---|",
    ]
    for name, code, _ in checks:
        lines.append(f"| {name} | {'PASS' if code == 0 else 'FAIL'} |")
    for name, code, output in checks:
        lines.extend(["", f"## {name}", "", f"Exit code: {code}", "", "Output:", output])
    lines.extend([
        "", "## Verification limits", "",
        "- Passing static and unit tests does not prove the simulation is scientifically valid.",
        "- A skipped Android build is not a successful Android build.",
        "- Research candidates remain unverified until their source, license and compatibility are inspected.", "",
    ])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT.relative_to(ROOT)}.")
    return 1 if any(code != 0 for _, code, _ in checks) else 0

if __name__ == "__main__":
    sys.exit(main())
