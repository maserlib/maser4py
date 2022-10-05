# About maser-data

maser-data is a submodule of [maser4py](https://pypi.org/project/maser4py/).

It offers programs to handle radio data from the following missions:

- Cassini
- Ecallisto
- Interball
- Juno
- Mars Express
- nancay decametric array (Jupiter only)
- Nancay NenuFAR/BST
- Solar orbiter
- Viking
- Wind

Read maser4py [main documentation](https://maser.pages.obspm.fr/maser4py/) for details.

# Installation

To install the package, run the following command:

```
pip install maser-data
```

or use one of the extra options:

- `jupyter` for Jupyter notebook support
- `spacepy` for CDF data format support (note that this requires the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html))
- `nenupy` for NenuFAR data products support
- `all` to install all the above

For example use `maser-data[jupyter,spacepy]` if you want to use `maser-data` with spacepy and jupyter notebooks:

```bash
pip install maser-data[jupyter,spacepy]
```

# Usage

The `Data` class is a wrapper around several classes that allow you to read data from many different formats, including CDF, Fits, and some custom binary formats. By default, the class will try to automagically detect the format of the file and use the appropriate class to read the data.

```python
from maser.data import Data

filepath = "path/to/my/data/file.ext"
data = Data(filepath=filepath)
```

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.obspm.fr%2Fmaser%2Fmaser4py.git/master) You can also launch a Binder environment and browse through the notebook [examples](https://gitlab.obspm.fr/maser/maser4py/-/tree/namespace/examples).

# Development

To contribute to the development of the package, you will need to install a local copy of maser.data

```
git clone https://gitlab.obspm.fr/maser/maser4py.git
```

Then, you can install the package locally

## Requirements

`maser-data` requirements are detailed in the `src/maser_data/pyproject.toml` file

### poetry

To install the package, it is recommended to use [poetry](https://python-poetry.org/docs/#installing-with-pip):

```
pip install poetry
```

### CDF file format

To use `maser-data` to read CDF files you have to install the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html) and the [spacepy.pycdf](https://spacepy.github.io/install.html) package.

## Installing a local copy of maser-data

Use the following command from `src/maser_data` folder to install the package:

```bash
poetry install
```

or this one if you want to use `maser-data` with spacepy to handle CDF files:

```bash
poetry install --extras "spacepy"
```

## Tests

Use `pytest -m "not test_data_required"` to skip tests that require test data (and to skip auto download).

## Manually publish `maser-data` on pypi

To publish `maser-data` with `poetry` you will have to build a `dist` package:

```
poetry build
```

And then publish the package on pypi (and/or on Gitlab, see https://python-poetry.org/docs/cli/#publish):

```
poetry publish
```

Commands above must be run from `src/maser_data` directory.
