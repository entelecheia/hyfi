# HyFI Example

This Jupyter Notebook demonstrates the usage of the `hyfi` package, including initializing a workspace, mounting Google Drive on Colab, and using HyFI to manage configurations.

First, let's import the necessary functions and classes from the `hyfi` package.

```python
from hyfi import HyFI
```

## About the `hyfi` package

Now, let's check the version of the `hyfi` package we are using.

```python
HyFI.print_about()
```

## Initialize Project

We'll initialize the project using the `HyFI.initialize` function. The function takes the following parameters:

- `project_name`: Name of the project to use.
- `project_description`: Description of the project that will be used.
- `project_root`: Root directory of the project.
- `project_workspace_name`: Name of the project's workspace directory.
- `global_hyfi_root`: Root directory of the global hyfi.
- `global_workspace_name`: Name of the global hierachical workspace directory.
- `num_workers`: Number of workers to run.
- `logging_level`: Log level for the log.
- `autotime`: Whether to automatically set time and / or keep track of run times.
- `retina`: Whether to use retina or not.
- `verbose`: Enables or disables logging

We'll check if we're running in Google Colab, and if so, we'll mount Google Drive.

```python
if HyFI.is_colab():
    HyFI.mount_google_drive()

h = HyFI.initialize(
    project_name="hyfi",
    logging_level="DEBUG",
    verbose=True,
)

print("project_dir:", h.project.root_dir)
print("project_workspace_dir:", h.project.workspace_dir)
```

## Compose Configuration

We can use the `HyFI.compose` function to load a configuration file. In this example, we'll use the default workflow configuration file.

```python
cfg = HyFI.compose("workflow=__init__")
```

## Display Configuration

Now, let's print the loaded configuration using the `HyFI.print` function.

```python
HyFI.print(cfg)
```

That's it! This example demonstrated the basic usage of the `hyfi` package. You can now use this package to manage your own projects and tasks in a structured manner.
