#!/usr/bin/env python3
"""Validate the completeness and vocabulary of the continuity registry."""
import json
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / "docs/continuity/RECOVERY-REGISTRY.json"
ALLOWED = {"present", "unverified", "external_action_required", "proposed"}
REQUIRED = {
    "id", "name", "criticality", "status", "last_verified", "primary",
    "fallback", "fallback_status", "rto_minutes", "rpo_hours", "verification",
}


def main():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    errors = []
    seen = set()
    for index, item in enumerate(data.get("dependencies", [])):
        prefix = f"dependencies[{index}]"
        missing = REQUIRED - item.keys()
        if missing:
            errors.append(f"{prefix}: missing {', '.join(sorted(missing))}")
        if item.get("id") in seen:
            errors.append(f"{prefix}: duplicate id {item.get('id')}")
        seen.add(item.get("id"))
        for field in ("status", "fallback_status"):
            if item.get(field) not in ALLOWED:
                errors.append(f"{prefix}: invalid {field}={item.get(field)!r}")
        for field in ("rto_minutes", "rpo_hours"):
            if not isinstance(item.get(field), (int, float)) or item[field] <= 0:
                errors.append(f"{prefix}: {field} must be a positive number")
    if not data.get("dependencies"):
        errors.append("registry has no dependencies")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(seen)} dependency records are complete and valid")


if __name__ == "__main__":
    main()
