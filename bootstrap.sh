#!/usr/bin/env bash
set -euo pipefail

# AI Skills Sync v1 bootstrap/sync helper.
# Usage:
#   ./bootstrap.sh [REPOSITORY] [DESTINATION]
#
# Defaults:
#   REPOSITORY=PhateValleyman/ai-skills-sync
#   DESTINATION=$HOME/.agents
#
# Requirements: git, curl, python3

REPOSITORY="${1:-PhateValleyman/ai-skills-sync}"
DESTINATION="${2:-$HOME/.agents}"
BRANCH="${AI_SKILLS_SYNC_BRANCH:-master}"
RAW_BASE="https://raw.githubusercontent.com/$REPOSITORY/$BRANCH"

command -v curl >/dev/null || { echo "ERROR: curl is required" >&2; exit 1; }
command -v python3 >/dev/null || { echo "ERROR: python3 is required" >&2; exit 1; }

mkdir -p "$DESTINATION"

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

curl -fsSL "$RAW_BASE/registry.json" -o "$tmpdir/registry.json"
curl -fsSL "$RAW_BASE/profile.json" -o "$tmpdir/profile.json"

python3 - "$tmpdir/registry.json" "$tmpdir/profile.json" "$REPOSITORY" <<'PY'
import json
import sys

registry_path, profile_path, repository = sys.argv[1:4]

with open(registry_path, encoding="utf-8") as f:
    registry = json.load(f)
with open(profile_path, encoding="utf-8") as f:
    profile = json.load(f)

if registry.get("protocol") != "ai-skills-sync/v1":
    raise SystemExit("ERROR: unsupported registry protocol")
if profile.get("protocol") != "ai-skills-sync/v1":
    raise SystemExit("ERROR: unsupported profile protocol")
if registry.get("repository") != repository:
    raise SystemExit("ERROR: registry repository mismatch")
if profile.get("repository") != repository:
    raise SystemExit("ERROR: profile repository mismatch")

for category, entries in registry.get("components", {}).items():
    if not isinstance(entries, list):
        raise SystemExit(f"ERROR: invalid component category: {category}")
    for entry in entries:
        if not entry.get("id") or not entry.get("path"):
            raise SystemExit(f"ERROR: invalid registry entry in {category}")

print("OK: registry/profile validated")
print(f"INFO: profile={registry.get('profile')}")
print(f"INFO: version={registry.get('version')}")
PY

python3 - "$tmpdir/registry.json" "$DESTINATION" "$RAW_BASE" <<'PY'
import json
import os
import pathlib
import subprocess
import sys
import urllib.request

registry_path, destination, raw_base = sys.argv[1:4]

with open(registry_path, encoding="utf-8") as f:
    registry = json.load(f)

root = pathlib.Path(destination).expanduser().resolve()

for category, entries in registry.get("components", {}).items():
    for entry in entries:
        path = entry["path"]
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        url = f"{raw_base}/{path}"
        with urllib.request.urlopen(url) as response:
            data = response.read()
        target.write_bytes(data)
        print(f"OK: {path}")

state = root / "manifests" / ".ai-skills-sync-state.json"
state.parent.mkdir(parents=True, exist_ok=True)
state.write_text(
    json.dumps(
        {
            "protocol": registry["protocol"],
            "profile": registry["profile"],
            "repository": registry["repository"],
            "version": registry["version"],
            "branch": os.environ.get("AI_SKILLS_SYNC_BRANCH", "master"),
        },
        indent=2,
    ) + "\n",
    encoding="utf-8",
)
print(f"OK: state -> {state}")
PY

echo "OK: AI Skills Sync profile installed at $DESTINATION"
