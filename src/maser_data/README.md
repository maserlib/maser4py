# About maser-data

This is maser-data, a submodule of [maser4py](https://pypi.org/project/maser4py/). maser4py offers modules to handle data from several space and ground radio observatory and maser-data is the submodule dedicated to handling radio data parsing.

maser4py is developed in the framework of the [MASER project](https://maser-lira.obspm.fr/?lang=en).

maser-data offers programs to handle radio data from the following instruments:

- BepiColombo/MMO/PWI/SORBET
- Cassini/RPWS/HFR
- E-Callisto
- Interball-Auroral/POLRAD
- Juno/Waves
- Mars Express/MARSIS
- Nançay Decameter Array (Jupiter only)
- Nançay NenuFAR/BST
- Solar Orbiter/RPW
- STEREO/Waves
- Viking
- Voyager/PRA
- Wind/Waves

Detailed information can be found in [maser-data user guide](https://maser.pages.obspm.fr/maser4py/sections/user_guide.html#read-radio-data-with-maser-data).

You can also have a look to [maser-data examples and notebooks](https://maser.pages.obspm.fr/maser4py/sections/tutorial.html#maser-data).

For a broader documentation, please check maser4py [main documentation](https://maser.pages.obspm.fr/maser4py/) for details.

# Installation

## As a standalone submodule (recommanded)

To install the package, run the following command:

```
pip install maser-data
```

maser-data (through [spacepy](https://pypi.org/project/spacepy/) ), requires the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html) that needs to be installed on its own (see below).

It is also possible to use the extra option `jupyter` when installing maser-data:

- `jupyter` for Jupyter notebook support

- (`all` is equivalent to the line above)

For example use `maser-data[jupyter,spacepy]` if you want to use `maser-data` with spacepy and jupyter notebooks:

```bash
pip install maser-data[jupyter,spacepy]
```

## With maser4py

An alternative way of installing the package is to run the following command:

```
pip install maser4py[data]
```

and use the extra options:

- `jupyter` for Jupyter notebook support

For example use `maser4py[data,jupyter]` if you want to use `maser-data` with jupyter notebooks:

```bash
pip install maser4py[data,jupyter]
```

You can also use other options from [maser4py](https://pypi.org/project/maser4py/) such as:

- `tools` for [maser-tools](https://pypi.org/project/maser-tools/) submodule
- `all` to install all the above

```bash
pip install maser4py[all]
```

## CDF file format

To use `maser-data` to read CDF files you have to install the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html) and the [spacepy.pycdf](https://spacepy.github.io/install.html) package.

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

Then, you can install the package locally, by using `pip install -e .[all]` or by using `poetry` (see below).

## Requirements

`maser-data` requirements are detailed in the `src/maser_data/pyproject.toml` file

## poetry

To install the package as a developer, it is recommended to use [poetry](https://python-poetry.org/docs/#installing-with-pip):

```
pip install poetry
```

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
