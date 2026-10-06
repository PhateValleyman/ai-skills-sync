#!/usr/bin/env python3
"""Portable ai-skills-sync/v1 consumer.

Dependency-free GitHub-native synchronizer. It reads the profile repository,
validates protocol/repository identity, verifies optional SHA-256 checksums,
and mirrors registered components below ~/.agents.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path, PurePosixPath

PROTOCOL = "ai-skills-sync/v1"
DEFAULT_REPOSITORY = "PhateValleyman/ai-skills-sync"
DEFAULT_ROOT = Path("~/.agents").expanduser()
STATE_NAME = ".ai-skills-sync-state.json"
REF_RE = re.compile(r"^[A-Za-z0-9._/-]+$")
REPOSITORY_RE = re.compile(r"^[^/]+/[^/]+$")


def die(message: str) -> "None":
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def fetch(base: str, path: str, ref: str) -> bytes:
    url = f"{base.rstrip('/')}/{path}?ref={ref}"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ai-skills-sync/1.1"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        die(f"HTTP {exc.code} while fetching {path}")
    except urllib.error.URLError as exc:
        die(f"Unable to fetch {path}: {exc.reason}")


def parse_json(data: bytes, name: str) -> dict:
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        die(f"Invalid JSON in {name}: {exc}")
    if not isinstance(value, dict):
        die(f"{name} must contain a JSON object")
    return value


def validate(registry: dict, profile: dict, repository: str) -> None:
    if registry.get("protocol") != PROTOCOL:
        die("unsupported registry protocol")
    if profile.get("protocol") != PROTOCOL:
        die("unsupported profile protocol")
    if registry.get("repository") != repository:
        die("registry repository does not match requested repository")
    if profile.get("repository") != repository:
        die("profile repository does not match requested repository")
    if registry.get("version") != profile.get("version"):
        die("registry/profile version mismatch")
    if registry.get("canonical_root") != "~/.agents":
        die("unsupported canonical root")
    if profile.get("canonical_local_root") != "~/.agents":
        die("unsupported profile root")


def component_list(
    registry: dict,
    categories: list[str],
    selected: set[str] | None,
) -> list[tuple[str, dict]]:
    components = registry.get("components")
    if not isinstance(components, dict):
        die("registry.components must be an object")

    result: list[tuple[str, dict]] = []
    for category in categories:
        entries = components.get(category, [])
        if not isinstance(entries, list):
            die(f"registry.components.{category} must be an array")
        for entry in entries:
            if not isinstance(entry, dict):
                die(f"invalid component entry in {category}")
            item_id = entry.get("id")
            path = entry.get("path")
            fmt = entry.get("format")
            scope = entry.get("scope")
            if not all(isinstance(value, str) and value for value in (item_id, path, fmt, scope)):
                die(f"component in {category} requires non-empty id/path/format/scope")
            if selected is None or f"{category}:{item_id}" in selected or item_id in selected:
                result.append((category, entry))
    if selected is not None and not result:
        die("no selected components matched the registry")
    return result


def safe_relative_path(path: str) -> Path:
    p = PurePosixPath(path)
    if p.is_absolute() or ".." in p.parts:
        die(f"unsafe component path: {path}")
    allowed = {"skills", "agents", "plugins", "knowledge", "manifests"}
    if not p.parts or p.parts[0] not in allowed:
        die(f"component path outside managed profile areas: {path}")
    return Path(*p.parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize an ai-skills-sync/v1 profile.")
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--ref", default="master")
    parser.add_argument("--destination", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "--category",
        action="append",
        choices=["skills", "agents", "plugins", "knowledge", "manifests"],
    )
    parser.add_argument("--component", action="append", dest="components")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument(
        "--require-checksums",
        action="store_true",
        help="Reject registry entries that do not declare sha256.",
    )
    parser.add_argument(
        "--print-checksums",
        action="store_true",
        help="Print calculated SHA-256 values without modifying the destination.",
    )
    args = parser.parse_args()

    if not REPOSITORY_RE.fullmatch(args.repository):
        die("repository must be owner/name")
    if not REF_RE.fullmatch(args.ref) or args.ref.startswith(("/", ".", "-")):
        die("unsafe ref")
    if args.check_only and args.print_checksums:
        die("--check-only and --print-checksums are mutually exclusive")

    categories = args.category or ["skills", "agents", "plugins", "knowledge", "manifests"]
    selected = set(args.components) if args.components else None
    base = f"https://raw.githubusercontent.com/{args.repository}"

    registry = parse_json(fetch(base, "registry.json", args.ref), "registry.json")
    profile = parse_json(fetch(base, "profile.json", args.ref), "profile.json")
    validate(registry, profile, args.repository)

    entries = component_list(registry, categories, selected)
    state = {
        "protocol": PROTOCOL,
        "repository": args.repository,
        "ref": args.ref,
        "registry_version": registry.get("version"),
        "components": {},
    }

    for category, entry in entries:
        repo_path = entry["path"]
        target = args.destination / safe_relative_path(repo_path)
        data = fetch(base, repo_path, args.ref)

        expected = entry.get("sha256")
        actual = hashlib.sha256(data).hexdigest()
        if args.require_checksums and not expected:
            die(f"missing sha256 for {repo_path}")
        if expected is not None and (
            not isinstance(expected, str) or
            not re.fullmatch(r"[0-9a-fA-F]{64}", expected) or
            expected.lower() != actual
        ):
            die(f"sha256 mismatch for {repo_path}")

        state["components"][f"{category}:{entry['id']}"] = {
            "path": repo_path,
            "sha256": actual,
            "version": entry.get("version"),
        }

        if args.print_checksums:
            print(f"{actual}  {repo_path}")
            continue

        if args.check_only:
            print(f"OK: {repo_path}")
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        print(f"OK: {target}")

    if not args.check_only and not args.print_checksums:
        args.destination.mkdir(parents=True, exist_ok=True)
        state_path = args.destination / "manifests" / STATE_NAME
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            json.dumps(state, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"OK: state {state_path}")

    print(f"OK: processed {len(entries)} component(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
