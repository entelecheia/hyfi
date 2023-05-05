# HyFI Example

This Jupyter Notebook demonstrates the usage of the `hyfi` package, including initializing a workspace, mounting Google Drive on Colab, and using HyFI to manage configurations.

First, let's import the necessary functions and classes from the `hyfi` package.

```python
from hyfi import HyFI
```

## About the `hyfi` package

Now, let's check the version of the `hyfi` package we are using.

```python
HyFI.about()
```

## Initialize Workspace

We'll initialize the workspace using the `HyFI.init_workspace` function. The function takes the following parameters:

- `workspace`: The root workspace directory.
- `project`: The project subdirectory.
- `task`: The specific task within the project.
- `log_level`: Logging level for the workspace.
- `verbose`: Whether to print verbose messages.

We'll check if we're running in Google Colab, and if so, we'll mount Google Drive.

```python
if HyFI.is_colab():
    HyFI.mount_google_drive()

ws = HyFI.init_workspace(
    workspace="/workspace",
    project="hyfi/examples",
    task="test",
    log_level="INFO",
    verbose=True,
)

print("version:", ws.version)
print("project_dir:", ws.project_dir)
```

## Compose Configuration

We can use the `HyFI.compose` function to load a configuration file. In this example, we'll use the default configuration by specifying `path=__default__`.

```python
cfg = HyFI.compose("path=__default__")
```

## Display Configuration

Now, let's print the loaded configuration using the `HyFI.print` function.

```python
HyFI.print(cfg)
```

That's it! This example demonstrated the basic usage of the `hyfi` package. You can now use this package to manage your own projects and tasks in a structured manner.
