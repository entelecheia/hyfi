# HyFI: Hydra Fast Interface

[![pypi-image]][pypi-url]
[![license-image]][license-url]

HyFI composes [Hydra](https://hydra.cc) configs, validates them with [Pydantic](https://docs.pydantic.dev/), and runs reproducible workflows. Every run writes a manifest with the resolved config, the code version, and per-step results, so the same run can be repeated later, by a person or by a coding agent.

- [Documentation][docs-url]
- [Migrating from 1.x](https://hyfi.entelecheia.ai/migration/)

HyFI 2.0 is a rewrite. The 1.x line stays on the `v1` branch; pin `hyfi<2` to keep it.

## Install

```bash
uv add hyfi          # or: pip install hyfi
uvx hyfi --version   # run without installing
```

Python 3.11 or newer. Core dependencies: hydra-core, omegaconf, pydantic, python-dotenv.

## Quick start

Put configs in `./conf`:

```yaml
# conf/workflow/charcount.yaml
name: charcount
steps:
  - run: pathlib.Path
    with: {_args_: [README.md]}
  - run: pathlib.Path.read_text   # receives the previous result as its first argument
  - run: builtins.len
```

```bash
hyfi run workflow=charcount --dry-run   # resolve every step without running it
hyfi run workflow=charcount             # run it and write .hyfi/runs/<run_id>/manifest.json
hyfi rerun <run_id>                     # run the recorded config again
```

From Python or a notebook:

```python
import hyfi

cfg = hyfi.compose(["workflow=charcount"])
manifest = hyfi.run_workflow(cfg)
print(manifest.status, [s.status for s in manifest.steps])
```

## What is in the box

- `compose()` / `instantiate()` / `BaseConfig`: Hydra composition with Pydantic validation, from the CLI, code, or notebooks. Nothing happens at import time.
- Plugins: any package can ship config groups through the `hyfi.plugins` entry point.
- Workflows: ordered steps, each a Python callable built with Hydra `instantiate`; results pipe into the next step.
- Run manifests: resolved config, git SHA, `uv.lock` hash, Python and platform, timings, errors.
- Execution allowlist: `--allow 'mypkg.*'` limits which callables a config may run (forwarded to Hydra 1.4's execution whitelist).
- Agent-friendly CLI: `--json` on every command, `hyfi config schema` for JSON Schema, non-zero exit codes on failure.

## Citation

```tex
@software{lee_hyfi,
  author = {Young Joon Lee},
  title  = {HyFI: Hydra Fast Interface},
  year   = 2023,
  url    = {https://github.com/entelecheia/hyfi}
}
```

## License

[MIT][license-url]

[pypi-image]: https://img.shields.io/pypi/v/hyfi
[pypi-url]: https://pypi.org/project/hyfi
[license-image]: https://img.shields.io/github/license/entelecheia/hyfi
[license-url]: https://github.com/entelecheia/hyfi/blob/main/LICENSE
[docs-url]: https://hyfi.entelecheia.ai
