# Review instructions

Read by the required OCR delegation reviewer (Claude Code, Codex, or Kimi Code), additional `/codex:review` or `/code-review` passes, and human reviewers alike.

## Passes

Run these passes and tag every finding with its pass:

- Bugs: logic errors, broken edge cases, regressions.
- Security: configs choose which Python callables run, so look for paths where a `_target_` escapes the allowlist, for shell or `eval` use, and for secrets reaching manifests or logs.
- Compliance: the change matches issue #466 (spec and dated decision lines). Workflow changes (`.github/workflows/`) are checked against the workspace CI standard: every job has `timeout-minutes`, PR runs cancel in progress, docs-only changes skip builds, actions are pinned by SHA.
- Instruction prose (AGENTS.md, REVIEW.md): does each directive name the failure it prevents, and did rationale or history land here instead of README.md? Nits unless runtime behavior changes.

## Repo focus

- Importing `hyfi` has no side effects: no OmegaConf resolver, no `GlobalHydra` initialization, no `os.environ` change. Enforced by `tests/test_config.py:16`. Environment changes happen only inside `compose()` (`src/hyfi/config.py:104`), and Hydra global state is cleared only there (`src/hyfi/config.py:110`).
- With an allowlist, every nested `_target_` is checked before Hydra runs anything (`src/hyfi/config.py:159`, `check_allowed` at `src/hyfi/config.py:57`), on every Hydra version. Workflow steps go through that path (`src/hyfi/workflow.py:114`). `plan()` imports targets but never calls them (`src/hyfi/workflow.py:86`).
- Search-path precedence is user directory, then plugins, then `hyfi.conf`, whether or not the user directory has a primary config (`tests/test_config.py:60`).
- A run writes its manifest before the first step and after the last (`src/hyfi/runner.py:54`, `src/hyfi/runner.py:62`); writes are atomic via a temp file (`src/hyfi/manifest.py:80`).
- CLI exit codes: 1 for a failed run or dry-run (`src/hyfi/cli.py:103`, `src/hyfi/cli.py:116`), 2 for any raised error (`src/hyfi/cli.py:208`).

## Findings

Each finding carries its pass, severity, evidence (`file:line` or a reproduction), and provenance: introduced by this change, pre-existing, or indeterminate. Pre-existing findings go to a follow-up issue instead of widening the change. Report what was reviewed and what was not reached.

## Re-review

Hand the reviewer the diff, the spec, and this file, and let it read the rest of the repo (AGENTS.md included). Do not hand it fix-status claims, earlier dispositions, or do-not-reflag notes. Judge recurrence by the violated invariant, not by wording.

## What Important means here

Reserve Important for findings that let a config run a callable outside the allowlist, break an invariant above, change CLI exit codes or `--json` shapes without a spec line, add a core dependency, or lose run records. Style and naming are nits.

## Cap the nits

Report at most 5 nits per review; summarize the rest as a count.

## Do not report

- Generated paths: `uv.lock` (style only; a lock change without a matching `pyproject.toml` change stays in the Security pass), `CHANGELOG.md`, `src/hyfi/_version.py`.
- Anything CI already enforces: `uv lock --locked`, ruff check and format, mypy strict on `src/hyfi`, pytest with the 85% coverage floor, strict mkdocs build.

## Feedback into AGENTS.md

When the same finding appears twice, add the rule to AGENTS.md in the same PR.
