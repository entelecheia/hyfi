# Writing a plugin

A plugin is an ordinary Python package that ships Hydra config groups. Declare the config package in `pyproject.toml`:

```toml
[project]
name = "mypkg"
dependencies = ["hyfi>=2"]

[project.entry-points."hyfi.plugins"]
mypkg = "mypkg.conf"
```

```text
src/mypkg/
  __init__.py
  steps.py
  conf/
    __init__.py
    workflow/
      tokenize.yaml
    tokenizer/
      simple.yaml
```

After `uv add mypkg`, its groups are available everywhere HyFI composes:

```bash
hyfi plugins               # name, module, distribution, importable?
hyfi run workflow=tokenize
```

Guidelines:

- Keep the library usable without HyFI; put HyFI-specific wiring in `conf/` and small step functions.
- Name group options so they do not collide with other plugins. When two sources define the same option, the user directory wins, then plugins in name order, then HyFI.
- Use `hyfi.BaseConfig` for typed defaults that live in your config groups.
