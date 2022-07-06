# Installation

## Requirements

### poetry

To install the package, it is recommended to use [poetry](https://python-poetry.org/docs/#installing-with-pip):

```
pip install poetry
```

### CDF file format

To use `maser.data` to read CDF files you have to install the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html) and the [spacepy.pycdf](https://spacepy.github.io/install.html) package.

## Installing maser.data

Use the following command to install the package:

```bash
poetry install
```

or this one if you want to use `maser.data` with jupyter notebooks:

```bash
poetry install --extras "jupyter"
```

Extra installation options are:

- `jupyter` for Jupyter notebook support
- `spacepy` for CDF data format support
- `nenupy` for NenuFAR data products support

# Usage

The `Data` class is a wrapper around several classes that allow you to read data from many different formats, including CDF, Fits, and some custom binary formats. By default, the class will try to automagically detect the format of the file and use the appropriate class to read the data.

```python
from maser.data import Data

filepath = "path/to/my/data/file.ext"
data = Data(filepath=filepath)
```

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.obspm.fr%2Fcecconi%2Fmaser-data.git/dataset/rpw) You can also launch a Binder environment and browse through the notebook [examples](https://gitlab.obspm.fr/cecconi/maser-data/-/tree/master/examples).

# Tests

Use `pytest -m "not test_data_required"` to skip tests that require test data (and to skip auto download).

# Generate setup.py for editable local installation

In top level of the project folder, run:

```
python generate_setup.py
```

To install the package locally in editable mode, run:

```
pip install -e path/to/project/folder
```
