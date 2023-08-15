# HyFI: Hydra Fast Interface

[![pypi-image]][pypi-url]
[![version-image]][release-url]
[![release-date-image]][release-url]
[![license-image]][license-url]
[![DOI][zenodo-image]][zenodo-url]
[![codecov][codecov-image]][codecov-url]
[![codefactor][codefactor-image]][codefactor-url]
[![codacy][codacy-image]][codacy-url]

HyFI, short for Hydra Fast Interface, is a powerful Python framework built atop the foundations of [Hydra](https://hydra.cc) and [Pydantic](https://docs.pydantic.dev/latest/). Its main objective is to provide a streamlined interface for configuring, structuring, executing, and scaling Python applications and workflows.

- [Documentation][docs-url]
- [GitHub Repository][repo-url]
- [PyPI Package][pypi-url]

## Overview

In the modern world of software and data science, creating scalable, reproducible, and modular Python workflows is vital. HyFI is here to make that process not just feasible but also efficient and straightforward. It has been meticulously crafted to help developers and researchers build pipeline-oriented projects and promote shareable and reproducible workflows.

## Core Features

### **1. Dynamic Configuration Management**

- **Modular Configuration**: Harness the power of [Hydra](https://hydra.cc) and [Pydantic](https://docs.pydantic.dev/latest/) to manage your application configurations dynamically and modularity.
- **Seamless Command Line Overrides**: Experiment swiftly without the clutter of multiple similar configuration files.
- **Jupyter Notebook Integration**: The **HyFI** class allows for easy composition of configurations even in a jupyter notebook setting.

### **2. Zero Boilerplate**

Stay focused on your core problems. HyFI takes care of the usual overheads such as command line flags, loading configuration files, and logging.

### **3. Structured Workflows**

- **Configurable Automated Processes**: Divide your research into unit jobs or tasks, and then bundle them into workflows.

- **Versatility**: Have the liberty to create multiple workflows, with each performing varied sets of tasks.

### **4. Reproducibility and Sharing**

- **Sharing Capability**: Share your datasets, models, and configurations effortlessly.

- **Reproducibility**: Sharing configurations alongside datasets and models ensures that every piece of research can be replicated.

- **Granular or Holistic**: Choose to share individual unit jobs or an entire workflow, as per your need.

### **5. Support for Plugins**

- **Integration of HyFI-based Applications**: Enhance your project by plugging in several HyFI-based applications. This allows you to leverage the functionalities of plugins along with their specific configuration files.
- **Modular Design Enablement**: The plugin support fosters a truly modular design approach, enabling seamless integration of various components and features, thereby promoting greater flexibility and extensibility in your projects.

## Other Noteworthy Features:

- **Workspace Management**: Automatic workspace creation and environment variable management.
- **Task Pipelining**: Chain and parallelize jobs and steps seamlessly.
- **Optimized Parallelism**: Efficient job batching with the help of Joblib.
- **Dotenv Integration**: Manage configurations via .env files with ease.
- **Built-in Commands**: Simplify processes like initializing projects, running pipelines, and copying files.
- **Extensibility**: Easily extend HyFI's capabilities by crafting new Config classes and utilizing the building blocks it offers.
- **Command Line Interface (CLI)**: Access a suite of commands and workflows directly from the command line.
- **Advanced Logging**: Make use of the integrated logging configurations, complemented by Hydra logging.
- **Robust Caching**: Cache both files and data efficiently.

## Citation

```tex
@software{lee_2023_8247719,
  author       = {Young Joon Lee},
  title        = {HyFI: Hydra Fast Interface},
  month        = aug,
  year         = 2023,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.8247719},
  url          = {https://doi.org/10.5281/zenodo.8247719}
}
```

```tex
@software{lee_2023_hyfi,
  author       = {Young Joon Lee},
  title        = {HyFI: Hydra Fast Interface},
  year         = 2023,
  publisher    = {GitHub},
  url          = {https://github.com/entelecheia/hyfi}
}
```

## Changelog

See the [CHANGELOG] for more information.

## Contributing

Contributions are welcome! Please see the [contributing guidelines] for more information.

## License

This project is released under the [MIT License][license-url].

<!-- Links: -->

[zenodo-image]: https://zenodo.org/badge/DOI/10.5281/zenodo.8247719.svg
[zenodo-url]: https://doi.org/10.5281/zenodo.8247719
[codecov-image]: https://codecov.io/gh/entelecheia/hyfi/branch/main/graph/badge.svg?token=HCYTYW1WVF
[codecov-url]: https://codecov.io/gh/entelecheia/hyfi
[pypi-image]: https://img.shields.io/pypi/v/hyfi
[license-image]: https://img.shields.io/github/license/entelecheia/hyfi
[license-url]: https://github.com/entelecheia/hyfi/blob/main/LICENSE
[version-image]: https://img.shields.io/github/v/release/entelecheia/hyfi?sort=semver
[release-date-image]: https://img.shields.io/github/release-date/entelecheia/hyfi
[release-url]: https://github.com/entelecheia/hyfi/releases
[codefactor-image]: https://www.codefactor.io/repository/github/entelecheia/hyfi/badge
[codefactor-url]: https://www.codefactor.io/repository/github/entelecheia/hyfi
[codacy-image]: https://app.codacy.com/project/badge/Grade/6be6d2ecfbfe40b9ab8490ca25327a96
[codacy-url]: https://app.codacy.com/gh/entelecheia/hyfi/dashboard?utm_source=github.com&utm_medium=referral&utm_content=entelecheia/hyfi&utm_campaign=Badge_grade
[repo-url]: https://github.com/entelecheia/hyfi
[pypi-url]: https://pypi.org/project/hyfi
[docs-url]: https://hyfi.entelecheia.ai
[changelog]: https://github.com/entelecheia/hyfi/blob/main/CHANGELOG.md
[contributing guidelines]: https://github.com/entelecheia/hyfi/blob/main/CONTRIBUTING.md

<!-- Links: -->
