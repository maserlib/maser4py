# About maser.plot

maser.plot is a submodule of [maser4py](https://pypi.org/project/maser4py/).

It can be used with [maser.data](https://pypi.org/project/maser.data/) to plot radio data from the following missions:

- RPW/Solar Orbiter

# Installation

To install the package, run the following command:

```
pip install maser.plot
```

or use one of the extra options:

- `jupyter` for Jupyter notebook support
- `spacepy` for CDF data format support (note that this requires the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html))
- `nenupy` for NenuFAR data products support
- `all` to install all the above

For example use `maser.plot[jupyter,spacepy]` if you want to use `maser.plot` with spacepy and jupyter notebooks:

```bash
pip install maser.plot[jupyter,spacepy]
```

# Usage

See in `examples` folder about illustrations on how to use `maser.plot`.

Examples can also be run on Binder [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.obspm.fr%2Fmaser%2Fmaser4py.git/namespace) You can also launch a Binder environment and browse through the notebook [examples](https://gitlab.obspm.fr/maser/maser4py/-/tree/namespace/examples).

# Development

To contribute to the development of the package, you will need to install a local copy of maser.plot

```
git clone https://gitlab.obspm.fr/maser/maser4py.git
```

Then, you can install the package locally

## Requirements

`maser.plot` requirements are detailed in the `pyproject.toml` file

### poetry

To install the package, it is recommended to use [poetry](https://python-poetry.org/docs/#installing-with-pip):

```
pip install poetry
```

### CDF file format

To use `maser.plot` to read CDF files you have to install the [CDF library](https://cdf.gsfc.nasa.gov/html/sw_and_docs.html) and the [spacepy.pycdf](https://spacepy.github.io/install.html) package.

## Installing a local copy of maser.plot

Use the following command to install the package:

```bash
poetry install
```

or this one if you want to use `maser.plot` with spacepy to handle CDF files:

```bash
poetry install --extras "spacepy"
```

## Tests

Use `pytest -m "not test_data_required"` to skip tests that require test data (and to skip auto download).

## Generate setup.py for editable local installation

The `setup.py` file have to be updated after any changes to the `pyproject.toml` file.

To generate a new `setup.py` file, go to the top level of the `maser.plot` project folder and run:

```
python generate_setup.py
```

Now you can use the `setup.py` file to install the package locally in editable mode:

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
