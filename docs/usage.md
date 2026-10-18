# Usage

## Configs

HyFI looks for configs in three places, highest priority first:

1. Your config directory: `--config-dir`, or `./conf` when it exists.
2. Installed plugins (the `hyfi.plugins` entry point group), in name order.
3. HyFI's own defaults (`hyfi.conf`): a `project` group and an empty `workflow` slot.

If your directory holds `config.yaml` it becomes the primary config. Start it from HyFI's defaults:

```yaml
# conf/config.yaml
defaults:
  - project: default
  - workflow: null
  - _self_
```

Select group options and change values with ordinary Hydra overrides:

```bash
hyfi config show workflow=charcount project.name=demo
hyfi config show --json --no-resolve
```

`.env` in the current directory (or a parent) is loaded before composing, without overriding variables that are already set, so `${oc.env:NAME,default}` can read it.

## Project

The `project` node becomes a `hyfi.Project`:

| key | default | env |
|---|---|---|
| `name` | `hyfi-project` | `HYFI_PROJECT_NAME` |
| `root` | `.` | `HYFI_PROJECT_ROOT` |
| `workspace` | `<root>/workspace` | `HYFI_PROJECT_WORKSPACE` |

Run manifests go to `<root>/.hyfi/runs/`.

## Workflows

A workflow is a list of steps. Each step names a callable in `run` and its keyword arguments in `with`. Hydra builds it with `instantiate`, so nested `_target_` values inside `with` are built too, and `_args_` gives positional arguments.

```yaml
name: clean
steps:
  - run: mypkg.io.load_csv
    with: {path: data/in.csv}
  - run: mypkg.text.normalize     # gets the loaded table as its first argument
    with: {lowercase: true}
  - run: mypkg.io.save_csv
    with: {path: "${project.workspace}/out.csv"}
```

- `pipe: true` (default) passes the previous step's result as the first positional argument when it is not `None`. Set `pipe: false` to start fresh.
- A step's `name` defaults to the last part of `run`.
- A failing step stops the run; later steps are recorded as `skipped`.

Your own modules must be importable: run HyFI inside your project's environment (`uv run hyfi ...` after declaring your package), or use `python -m hyfi`, which puts the current directory on `sys.path`.

## Runs and reruns

```bash
hyfi run workflow=clean                 # exit 0 on success, 1 if a step failed
hyfi run workflow=clean --dry-run       # resolve targets only; exit 1 if any cannot be imported
hyfi rerun 20261019T010203Z-a1b2c3      # run the recorded resolved config again
```

The manifest records the run id, status, start and end time, HyFI and Python versions, platform, argv, config name and directory, overrides, the allowlist, the fully resolved config, git SHA and dirty flag, the SHA-256 of `uv.lock`, and per-step status, seconds, and error.

`hyfi rerun` does not recompose: it executes the recorded config, so interpolations such as `${now:...}` keep their recorded values.

## Execution allowlist

A config decides which Python callables run. When configs come from somewhere you do not fully trust, limit them:

```bash
hyfi run workflow=clean --allow 'mypkg.*' --allow builtins.len
HYFI_ALLOW='mypkg.*,builtins.len' hyfi run workflow=clean
```

A pattern is an exact target or `pkg.*` for everything under a package. Every `_target_` in a step, including nested ones, must match. On Hydra 1.4+ the list is also passed to Hydra's execution whitelist. `hyfi rerun` reuses the recorded list unless you pass `--allow`. Without a list, Hydra's default applies (Hydra 1.4 warns; 1.5 plans to refuse).

## Typed config groups

```python
from hyfi import BaseConfig


class Tokenizer(BaseConfig):
    _config_group_ = "tokenizer"
    _config_name_ = "simple"
    lowercase: bool = True


tok = Tokenizer.compose(overrides=["tokenizer.lowercase=false"])
```

`compose()` composes `tokenizer=simple` with the usual search path and validates the node.
