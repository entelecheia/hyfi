"""
Interate folders unlder src/hyfi/conf and generate config markdown docs named as the folder name.

Contents of the markdown file are yaml files in the folder.

Example of the generated markdown file:

```markdown
# Config group name (folder name)

Config location: `conf/<config_group_name>`

## `file_name.yaml`

```yaml
{% include "../../src/hyfi/conf/<config_group_name>/file_name.yaml" %}
```

```

Variables:

config_folder = "src/hyfi/conf"
output_docs_folder = "docs/configs"

"""

import os

config_folder = "src/hyfi/conf"
output_docs_folder = "docs/configs"

if not os.path.exists(output_docs_folder):
    os.makedirs(output_docs_folder)

for folder in os.listdir(config_folder):
    folder_path = os.path.join(config_folder, folder)
    if os.path.isdir(folder_path):
        output_file = os.path.join(output_docs_folder, f"{folder}.md")
        with open(output_file, "w") as f:
            f.write(f"# {folder}\n\n")
            f.write(f"Config location: `conf/{folder}`\n\n")
            files = sorted(os.listdir(folder_path))
            for file in files:
                if file.endswith(".yaml"):
                    file_path = os.path.join(folder_path, file)
                    with open(file_path) as yaml_file:
                        f.write(f"## `{file}`\n\n")
                        f.write("```yaml\n")
                        f.write(
                            "{% include '../../src/hyfi/conf/"
                            + f"{folder}/{file}'"
                            + " %}"
                        )
                        f.write("\n```\n\n")
