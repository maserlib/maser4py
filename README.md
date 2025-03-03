# About maser4py

maser4py offers modules to handle data from several space and ground radio observatory.

It comes with the following submodules:

- [maser-data](https://pypi.org/project/maser-data/) for radio data parsing features
- [maser-plot](https://pypi.org/project/maser-plot/) for radio data plotting features
- [maser-tools](https://pypi.org/project/maser-tools/) for additional support programs

Read maser4py [main documentation](https://maser.pages.obspm.fr/maser4py/) for details.

maser4py is developed in the framework of the [MASER project](https://maser.lesia.obspm.fr).

# Installation

To install the full package, run the following command:

```
pip install maser4py[all]
```

or use one of the extra options:

- `data` to get [maser-data](https://pypi.org/project/maser-data/) submodule features
- `plot` to get [maser-plot](https://pypi.org/project/maser-plot/) submodule features
- `tools` to get [maser-tools](https://pypi.org/project/maser-tools/) submodule features
- `jupyter` for Jupyter notebook support
- `jupytext` for Jupyter notebook text support
- `all` to install all the submodules above

For example if you want to use `maser4py` with maser-data and maser-plot submodules:

```bash
pip install maser4py[data,plot]
```

# Usage

Examples of usage can be found in the `examples` folder.

Examples can also be run as Jupyter notebooks on Binder [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.obspm.fr%2Fmaser%2Fmaser4py.git/master) You can also launch a Binder environment and browse through the notebook [examples](https://gitlab.obspm.fr/maser/maser4py/-/tree/namespace/examples).

# Development

To contribute to the development of the package, you will need to install a local copy of maser4py:

```
git clone https://gitlab.obspm.fr/maser/maser4py.git
```

Then, you can install the package locally, by using `pip install -e .[all]` or by using `poetry` (see below).

## Requirements

`maser4py` requirements are detailed in the `pyproject.toml` file

### poetry

To install the package, it is recommended to use [poetry](https://python-poetry.org/docs/#installing-with-pip):

```
pip install poetry
```

### CDF file format

To use `maser4py` to read CDF files you have to install the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html) and the [spacepy.pycdf](https://spacepy.github.io/install.html) package.

## Installing a local copy of maser4py

Use the following command to install the package from a local copy:

```bash
poetry install
```

## Tests

Use `pytest -m "not test_data_required"` to skip tests that require test data (and to skip auto download).

```
pip install -e path/to/project/folder
```

## Build the documentation

Use `sphinx-build docs/source docs/public` to build the documentation.

## Manually publish `maser` and generate a new DOI

To publish `maser` with `poetry` you will have to build a `dist` package:

```
poetry build
```

And then publish the package on pypi (and/or on Gitlab, see https://python-poetry.org/docs/cli/#publish):

```
poetry publish
```

`maser` comes with a Python client (see `.ci/zenodo.py`) to interact with the Zenodo API and generate automatically a DOI for each new version of `maser`.

To archive `maser` on Zenodo:

1. [Create an access token](https://zenodo.org/account/settings/applications/tokens/new/)
2. Is this the first maser deposit on Zenodo ?

- Yes it's the first deposit, so you don't need any ID
- No, it's a new version of `maser`. Then browse to the first record of maser on Zenodo and check the URL : `https://zenodo.org/record/<DEPOSITION_ID>` to get the `maser` deposition ID.

3. Use the following command to deposit the package on Zenodo:

```bash
 python .ci/zenodo.py -p ./ -t <ACCESS_TOKEN> -a ./dist/maser4py-X.Y.Z.tar.gz  -id <DEPOSITION_ID>
```

4. Browse to the `maser` record on Zenodo, check the metadata/files and publish the package to finally generate the DOI.

Notes :

- the `--sandbox` keyword can be used to deposit files on the Zenodo test server
- the `--publish` keyword can be used to automatically publish the new record and generate the DOI. But **be careful**, once published, there is no way to modify a record on Zenodo without publishing a new version.
