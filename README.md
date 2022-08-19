# Installation

To install the package, run the following command:

```
pip install maser.data --extra-index-url https://gitlab.obspm.fr/api/v4/projects/2440/packages/pypi/simple
```

or use one of the extra options:

- `jupyter` for Jupyter notebook support
- `spacepy` for CDF data format support (note that this requires the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html))
- `nenupy` for NenuFAR data products support
- `all` to install all the above

For example use `maser.data[jupyter,spacepy]` if you want to use `maser.data` with spacepy and jupyter notebooks:

```bash
pip install maser.data[jupyter,spacepy] --extra-index-url https://gitlab.obspm.fr/api/v4/projects/2440/packages/pypi/simple
```

# Usage

The `Data` class is a wrapper around several classes that allow you to read data from many different formats, including CDF, Fits, and some custom binary formats. By default, the class will try to automagically detect the format of the file and use the appropriate class to read the data.

```python
from maser.data import Data

filepath = "path/to/my/data/file.ext"
data = Data(filepath=filepath)
```

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.obspm.fr%2Fcecconi%2Fmaser-data.git/dataset/rpw) You can also launch a Binder environment and browse through the notebook [examples](https://gitlab.obspm.fr/cecconi/maser-data/-/tree/master/examples).

# Development

To contribute to the development of the package, you will need to install a local copy of maser.data

```
git clone https://gitlab.obspm.fr/cecconi/maser-data.git
```

Then, you can install the package locally

## Requirements

`maser.data` requirements are detailed in the `pyproject.toml` file

### poetry

To install the package, it is recommended to use [poetry](https://python-poetry.org/docs/#installing-with-pip):

```
pip install poetry
```

### CDF file format

To use `maser.data` to read CDF files you have to install the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html) and the [spacepy.pycdf](https://spacepy.github.io/install.html) package.

## Installing a local copy of maser.data

Use the following command to install the package:

```bash
poetry install
```

or this one if you want to use `maser.data` with spacepy to handle CDF files:

```bash
poetry install --extras "spacepy"
```

## Tests

Use `pytest -m "not test_data_required"` to skip tests that require test data (and to skip auto download).

## Generate setup.py for editable local installation

The `setup.py` file have to be updated after any changes to the `pyproject.toml` file.

To generate a new `setup.py` file, go to the top level of the `maser.data` project folder and run:

```
python generate_setup.py
```

Now you can use the `setup.py` file to install the package locally in editable mode:

```
pip install -e path/to/project/folder
```

## Build the documentation

Use `sphinx-build docs/source docs/public` to build the documentation.
