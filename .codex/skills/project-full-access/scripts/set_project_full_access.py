#!/usr/bin/env python3
"""Upsert Codex full-access defaults into the current project's .codex/config.toml."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


SANDBOX_LINE = 'sandbox_mode = "danger-full-access"\n'
APPROVAL_LINE = 'approval_policy = "never"\n'
TABLE_HEADER_RE = re.compile(r"^\s*(?:\[\[.*\]\]|\[.*\])\s*(?:#.*)?$")
KEY_RE = {
    "sandbox_mode": re.compile(r"^\s*sandbox_mode\s*="),
    "approval_policy": re.compile(r"^\s*approval_policy\s*="),
}
INLINE_COMMENT_RE = re.compile(r"^(?P<body>.*?)(?P<comment>\s+#.*)?(?P<newline>\n?)$")


def resolve_project_root(cwd: Path, project_root: str | None) -> Path:
    if project_root:
        return Path(project_root).expanduser().resolve()

    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return Path(result.stdout.strip()).resolve()
    return cwd.resolve()


def split_top_level_prefix(text: str) -> tuple[list[str], list[str]]:
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if TABLE_HEADER_RE.match(line):
            return lines[:index], lines[index:]
    return lines, []


def ensure_trailing_newline(lines: list[str]) -> list[str]:
    if lines and not lines[-1].endswith("\n"):
        lines[-1] = lines[-1] + "\n"
    return lines


def render_replacement_line(line: str, replacement: str) -> str:
    match = INLINE_COMMENT_RE.match(line)
    if not match:
        return replacement

    comment = match.group("comment") or ""
    newline = match.group("newline") or "\n"
    return replacement.rstrip("\n") + comment + newline


def upsert_top_level_keys(prefix_lines: list[str]) -> list[str]:
    prefix_lines = ensure_trailing_newline(prefix_lines[:])
    updated: list[str] = []
    seen: set[str] = set()

    for line in prefix_lines:
        if KEY_RE["sandbox_mode"].match(line):
            updated.append(render_replacement_line(line, SANDBOX_LINE))
            seen.add("sandbox_mode")
            continue
        if KEY_RE["approval_policy"].match(line):
            updated.append(render_replacement_line(line, APPROVAL_LINE))
            seen.add("approval_policy")
            continue
        updated.append(line)

    missing: list[str] = []
    if "sandbox_mode" not in seen:
        missing.append(SANDBOX_LINE)
    if "approval_policy" not in seen:
        missing.append(APPROVAL_LINE)

    if missing:
        if updated and updated[-1].strip():
            updated.append("\n")
        updated.extend(missing)

    if updated and updated[-1].strip():
        updated.append("\n")

    return updated


def render_updated_config(original_text: str) -> str:
    prefix, suffix = split_top_level_prefix(original_text)
    updated_prefix = upsert_top_level_keys(prefix)
    updated = "".join(updated_prefix + ensure_trailing_newline(suffix))
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply Codex full-access defaults to a project-scoped .codex/config.toml.",
    )
    parser.add_argument(
        "--project-root",
        help="Explicit project root. Defaults to the current Git root or cwd.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the resulting config without writing it.",
    )
    args = parser.parse_args()

    cwd = Path.cwd().resolve()
    project_root = resolve_project_root(cwd, args.project_root)
    home_dir = Path.home().resolve()

    if project_root == home_dir:
        print(
            "Refusing to treat the home directory as a project root. "
            "Run this inside the target project or pass --project-root.",
            file=sys.stderr,
        )
        return 2

    config_path = project_root / ".codex" / "config.toml"
    original_text = config_path.read_text() if config_path.exists() else ""
    updated_text = render_updated_config(original_text)
    changed = updated_text != original_text

    print(f"project_root={project_root}")
    print(f"config_path={config_path}")
    print(f"changed={str(changed).lower()}")

    if args.dry_run:
        print("----- BEGIN CONFIG -----")
        sys.stdout.write(updated_text)
        if updated_text and not updated_text.endswith("\n"):
            print()
        print("----- END CONFIG -----")
        return 0

    if changed:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(updated_text)

    print("Project-scoped config loads only for trusted projects.")
    print("Open a new Codex session in this project to use the updated defaults.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
