# hyfi

HyFI 2.0: compose Hydra configs, validate them with Pydantic, run step workflows, and record run manifests. Package `hyfi` under `src/hyfi/`. It is not a data-processing library: no pandas, datasets, or plotting code belongs in core.

Design and decisions: issue #466 (the spec). Change the spec before the code when they disagree.

## Commands

- Install: `make install` (uv sync with all dependency groups)
- Lint: `make lint` (`uv lock --locked`, ruff check, ruff format --check, mypy strict on `src/hyfi`)
- Test: `make test` (pytest with coverage, fails under 85%)
- Docs: `make docs-test` (strict mkdocs build)

## Verifying your work

```bash
make verify
```

Healthy output ends with `Required test coverage of 85.0% reached` and `N passed`. Run it before reporting any change complete and paste the tail. Fix the code when a test fails, never the test or the threshold.

For changes touching Hydra calls, also run the pre-release job locally:

```bash
UV_PYTHON=3.14 uv run --isolated --prerelease allow --with 'hydra-core>=1.4.0rc1' --no-default-groups --group test pytest -q
```

## Conventions

- Python `>=3.11`; ruff targets py311, line length 100. Development pins 3.13 (`.python-version`).
- Core runtime dependencies are exactly hydra-core, omegaconf, pydantic, python-dotenv. Adding one needs a spec decision in #466.
- Conventional commits; python-semantic-release versions from tags on the `release` branch. Never hand-edit `src/hyfi/_version.py` or the version in `pyproject.toml`.
- `uv.lock` is committed; re-run `uv lock` after editing dependencies or `make lint` fails.
- CLI output for agents: every command keeps `--json`, and exit codes stay 0 ok, 1 run or check failed, 2 usage or config error.

## Architecture

- `config.py`: search path, `compose`, `compose_group`, `instantiate`, allowlist, `BaseConfig`.
- `plugins.py`: `hyfi.plugins` entry point discovery.
- `project.py`, `workflow.py`, `runner.py`, `manifest.py`: paths, steps, execution, run records.
- `cli.py`: argparse subcommands only; logic stays in the modules above.
- `conf/`: HyFI's own config groups, always last on the search path. `_primary/`: only `config.yaml`; never add group options there, or they would shadow user and plugin options.

## Things the agent gets wrong

- 2026-10-19, Hydra version drift: Hydra 1.4 deprecates `version_base` and warns on `instantiate` without an execution whitelist. Call Hydra through `hyfi.config` helpers, which branch on the installed version; do not call `hydra.utils.instantiate` directly elsewhere. Revisit when Hydra 1.5 ships.
- 2026-10-19, env values leaking (three review rounds): anything printed or written from a resolved config (manifest fields, plan entries, names, errors) must pass through `runner.redact` with the secrets from `runner.record_config`. Do not add per-field redaction. Revisit if a new output path is added.
- 2026-10-19, tests leaking state: tests that compose must use the `project` fixture (`tests/conftest.py`), which isolates cwd, `HYFI_*` env, and the fake plugin. Revisit if the fixture changes.

---

Contract and update rule for this file: `_meta/rules/development-lifecycle.md` §6 in the workspace repo. When the same mistake appears twice, add the correction here in the same PR.
