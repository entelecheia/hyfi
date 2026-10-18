# Using HyFI from coding agents

Every command takes `--json` and exits non-zero on failure (1: the run or check failed, 2: usage or config error, with `{"error": ...}` on stdout).

A safe loop for an agent:

1. **Inspect**: `hyfi plugins --json`, `hyfi config show workflow=<name> --json`.
2. **Learn the shape**: `hyfi config schema workflow` (or `project`, or any dotted Pydantic model) prints JSON Schema.
3. **Dry-run with an allowlist**: `hyfi run workflow=<name> --dry-run --json --allow '<pkg>.*'`. Every step must report `"ok": true`.
4. **Run**: same command without `--dry-run`. Read `status` and `steps[*].status` from the JSON output.
5. **Reproduce**: `hyfi rerun <run_id> --json`; the manifest is at `<project.root>/.hyfi/runs/<run_id>/manifest.json`.

Always pass `--allow` when the config was written or changed by someone other than the person who asked for the run.
