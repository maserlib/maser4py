# About maser-plot

maser-plot is a submodule of [maser4py](https://pypi.org/project/maser4py/).

It can be used with [maser.data](https://pypi.org/project/maser.data/) to plot radio data from the following missions:

- RPW/Solar Orbiter

# Installation

To install the package, run the following command:

```
pip install maser-plot
```

or use one of the extra options:

- `jupyter` for Jupyter notebook support
- `spacepy` for CDF data format support (note that this requires the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html))
- `nenupy` for NenuFAR data products support
- `all` to install all the above

For example use `maser-plot[jupyter,spacepy]` if you want to use `maser-plot` with spacepy and jupyter notebooks:

```bash
pip install maser-plot[jupyter,spacepy]
```

# Usage

See in `examples` folder about illustrations on how to use `maser-plot`.

Examples can also be run on Binder [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.obspm.fr%2Fmaser%2Fmaser4py.git/master) You can also launch a Binder environment and browse through the notebook [examples](https://gitlab.obspm.fr/maser/maser4py/-/tree/namespace/examples).

# Development

To contribute to the development of the package, you will need to install a local copy of maser-plot

```
git clone https://gitlab.obspm.fr/maser/maser4py.git
```

Then, you can install the package locally

## Requirements

`maser-plot` requirements are detailed in the `src/maser_plot/pyproject.toml` file

### poetry

To install the package, it is recommended to use [poetry](https://python-poetry.org/docs/#installing-with-pip):

```
pip install poetry
```

### CDF file format

To use `maser-plot` to read CDF files you have to install the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html) and the [spacepy.pycdf](https://spacepy.github.io/install.html) package.

## Installing a local copy of maser-plot

Use the following command from `src/maser_plot` folder to install the package:

```bash
poetry install
```

or this one if you want to use `maser-plot` with spacepy to handle CDF files:

```bash
poetry install --extras "spacepy"
```

## Tests

Use `pytest -m "not test_data_required"` to skip tests that require test data (and to skip auto download).

## Manually publish `maser-plot` on pypi

To publish `maser-plot` with `poetry` you will have to build a `dist` package:

```
poetry build
```

And then publish the package on pypi (and/or on Gitlab, see https://python-poetry.org/docs/cli/#publish):

```
poetry publish
```

Commands above must be run from `src/maser_plot` directory.
