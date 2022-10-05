# About maser-tools

maser-tools is a submodule of [maser4py](https://pypi.org/project/maser4py/).
It offers programs to support radio data format (e.g., CDF) and time (e.g. leap seconds and time conversion handling)

Read [main documentation](https://maser.pages.obspm.fr/maser4py/) for details.

# Installation

To install the package, run the following command:

```
pip install maser-tools
```

# Usage

See in `examples` folder about illustrations on how to use `maser-tools`.

Examples can also be run on Binder [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.obspm.fr%2Fmaser%2Fmaser4py.git/master) You can also launch a Binder environment and browse through the notebook [examples](https://gitlab.obspm.fr/maser/maser4py/-/tree/namespace/examples).

# Development

To contribute to the development of the package, you will need to install a local copy of maser-tools:

```
git clone https://gitlab.obspm.fr/maser/maser4py.git
```

Then, you can install the package locally.

## Requirements

`maser-tools` requirements are detailed in the `src/maser_tools/pyproject.toml` file

### poetry

To install the package, it is recommended to use [poetry](https://python-poetry.org/docs/#installing-with-pip):

```
pip install poetry
```

### CDF file format

To use `maser-tools` to read CDF files you have to install the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html) and the [spacepy.pycdf](https://spacepy.github.io/install.html) package.

## Installing a local copy of maser-tools

Use the following command from `src/maser_tools` folder to install the package:

```bash
poetry install
```

or this one if you want to use `maser-tools` with spacepy to handle CDF files:

```bash
poetry install --extras "spacepy"
```

## Tests

Use `pytest -m "not test_data_required"` to skip tests that require test data (and to skip auto download).

## Build the documentation

Use `sphinx-build docs/source docs/public` to build the documentation.

## Manually publish `maser-tools` on pypi

To publish `maser` with `poetry` you will have to build a `dist` package:

```
poetry build
```

And then publish the package on pypi (and/or on Gitlab, see https://python-poetry.org/docs/cli/#publish):

```
poetry publish
```

Commands above must be run from `src/maser_tools` directory.
