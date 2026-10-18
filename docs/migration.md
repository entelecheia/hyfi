# Migrating from 1.x

HyFI 2.0 is a rewrite with a much smaller core. There is no compatibility layer.

**Staying on 1.x**: pin `hyfi<2` (projects generated from hyfi-template already pin `^1.36`). The 1.x source lives on the `v1` branch. HyFI 1.x does not install on Python 3.13 or newer.

| 1.x | 2.0 |
|---|---|
| `from hyfi import HyFI`, `HyFI.compose(...)` | `hyfi.compose([...overrides])` |
| `HyFI.instantiate(cfg)`, `instantiate_config` | `hyfi.instantiate(cfg)` |
| `hyfi.composer.BaseConfig` with implicit composition on construction | `hyfi.BaseConfig` subclass, explicit `Model.compose()` |
| `hyfi.composer.BaseModel`, `Field`, validators | `pydantic` directly |
| `HyFI.initialize_global_hyfi(plugins=[...])` | `[project.entry-points."hyfi.plugins"]` in `pyproject.toml` |
| `hyfi_main()` CLI wrapper | the `hyfi` CLI (`config`, `plugins`, `run`, `rerun`) |
| workflow → task → pipeline → pipe, `uses:` | `workflow` with a flat `steps:` list, `run:` + `with:` |
| `Runner`, `BatchTask`, `/batch`, `/path:__batch__` | `Project` paths plus run manifests |
| built-in `/pipe` dataframe and dataset helpers, jsonl/dataframe I/O, graphics | removed: call pandas, datasets, or your own functions as steps |
| about 30 custom resolvers (`__get_path__`, `today`, `iif`, ...) | interpolation of composed values (`${project.root}`) and Hydra's built-ins (`${now:...}`, `${oc.env:...}`) |
| `hyfi-run` click CLI, copier commands | removed |

A 1.x pipeline such as

```yaml
steps:
  - uses: load_dataframes
    with: {data_files: in.parquet}
  - uses: save_dataframes
    with: {data_file: out.parquet}
```

becomes

```yaml
steps:
  - run: pandas.read_parquet
    with: {path: in.parquet}
  - run: pandas.DataFrame.to_parquet
    with: {path: out.parquet}
```
