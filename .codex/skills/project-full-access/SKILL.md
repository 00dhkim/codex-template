---
name: project-full-access
description: Apply Codex full-access defaults to the current project's `.codex/config.toml` without editing user-global config. Use when the user wants to stop running `/permissions`, wants project-scoped `danger-full-access` plus `approval_policy = "never"`, or asks to enable full access by default for the current repository/worktree.
---

# Project Full Access

## Overview

Apply project-scoped full-access defaults by updating the current project's `.codex/config.toml` instead of changing `~/.codex/config.toml`.

## Workflow
1. Resolve the target project root.
   Prefer the current Git root.
   If the current directory is not inside a Git repository, use the current working directory only if it is clearly the intended project root.
2. Avoid writing to the home directory's global config by mistake.
   If the resolved project root is the home directory, stop and ask the user to move into the project directory or provide the intended project root.
3. Explain the edit before making it.
   Say that you will update the current project's `.codex/config.toml` to set:
   `sandbox_mode = "danger-full-access"`
   `approval_policy = "never"`
4. Run the bundled updater:
   `python3 scripts/set_project_full_access.py`
   Use `--project-root <abs-path>` only when you need to target a project other than the current working directory.
5. Verify the result by printing the target file contents after the update.
6. Remind the user that project-scoped config loads only for trusted projects.
   If trust is missing, explain that the project may also need a matching trusted-project entry in `~/.codex/config.toml`, and ask before changing user-global config.

## Rules
- Modify only the current project's `.codex/config.toml` unless the user explicitly asks to touch global config too.
- Preserve unrelated settings and comments already present in the project config.
- Keep `sandbox_mode` and `approval_policy` as top-level keys.
- Do not silently change trust settings in `~/.codex/config.toml`.

## Script
- Updater: `scripts/set_project_full_access.py`
- Dry run:
  `python3 scripts/set_project_full_access.py --dry-run`
