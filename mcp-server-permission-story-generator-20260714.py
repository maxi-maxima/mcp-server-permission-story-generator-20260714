#!/usr/bin/env python
"""Turn MCP tool manifests into human-readable permission stories."""

import argparse
import json
import sys

RISK = {
    "filesystem": "Can read or write local files",
    "network": "Can contact external services",
    "shell": "Can execute local commands",
    "browser": "Can operate a browser session",
    "database": "Can query or mutate data stores",
}

RISK_WEIGHT = {"shell": 3, "filesystem": 3, "database": 3, "network": 2, "browser": 2}


def normalize_caps(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return [str(item) for item in value]


def tool_caps(tool):
    return normalize_caps(tool.get("permissions") or tool.get("capabilities"))


def risk_level(caps):
    score = max((RISK_WEIGHT.get(cap, 1) for cap in caps), default=0)
    if score >= 3:
        return "high"
    if score == 2:
        return "medium"
    return "low"


def story(manifest, min_level="low"):
    tools = manifest.get("tools", [])
    min_weight = {"low": 0, "medium": 2, "high": 3}[min_level]
    lines = ["# MCP Permission Story", ""]
    shown = 0
    for tool in tools:
        caps = tool_caps(tool)
        risks = [RISK.get(cap, cap) for cap in caps]
        level = risk_level(caps)
        if {"low": 0, "medium": 2, "high": 3}[level] < min_weight:
            continue
        shown += 1
        lines.append(f"- **{tool.get('name', 'unnamed')}** ({level}): {tool.get('description', 'No description')}")
        if risks:
            lines.append("  - Permissions: " + "; ".join(risks))
        else:
            lines.append("  - Permissions: none declared")
    if shown == 0:
        lines.append("No tools matched the selected risk threshold.")
    return "\n".join(lines)


def summarize(manifest):
    counts = {"high": 0, "medium": 0, "low": 0}
    permissions = {}
    for tool in manifest.get("tools", []):
        caps = tool_caps(tool)
        counts[risk_level(caps)] += 1
        for cap in caps:
            permissions[cap] = permissions.get(cap, 0) + 1
    return {"tools": len(manifest.get("tools", [])), "levels": counts, "permissions": dict(sorted(permissions.items()))}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Turn an MCP tool manifest into a human-readable permission story for reviewers.")
    ap.add_argument("manifest_json")
    ap.add_argument("--format", choices=["markdown", "json-summary"], default="markdown")
    ap.add_argument("--min-level", choices=["low", "medium", "high"], default="low", help="Only show tools at or above this risk level in markdown output.")
    args = ap.parse_args(argv)

    with open(args.manifest_json, encoding="utf-8") as handle:
        manifest = json.load(handle)
    if args.format == "json-summary":
        print(json.dumps(summarize(manifest), indent=2, sort_keys=True))
    else:
        print(story(manifest, min_level=args.min_level))
    return 0


if __name__ == "__main__":
    sys.exit(main())
