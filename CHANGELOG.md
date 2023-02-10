# CHANGELOG

## 0.15.3

- Release maser-data 0.3.5
- Release maser-plot 0.2.6

## 0.15.2

- Update solo/rpw tnr and hfr reader in maser-data
- Update maser-plots to be compatible with new RpwTnrSurv.as_xarray()
- Update docs

## 0.15.1

- Add as_xarray() for ecallisto in maser-data
- Update data.py for wind, cassini and nda
- Update mixin classes
- Add spacepy as an extra in maser4py pyproject.toml

## 0.15.0

- Add as_xarray() for NDA/Routine (CDF) in maser-data
- Reduce processing time for in RpwHfrSurvSweeps class in maser-data
- Fix bug in RpwHfrSurv.as_xarray() in maser-data
- Make maser command line works with new architecture
- Update documentation

## 0.14.0

- Add maser-tools as a new maser4py submodule
- Replace "." by "-" in maser4py submodule package names
- Update README for each maser4py, maser-data, maser-plot and maser-tools
- Update documentation

## 0.13.0

- Add SOLO/RPW/HFR Data class in maser.data
- Update SOLO/RPW/TNR Data.sweep method in maser.data
- Update README
- Update pyproject.toml (tool.poetry.source gitlab_obspm not required anymore)

## 0.12.0

- Internal updates

## 0.11.2

- Update pypi publish process
- Update documentation

## 0.11.1

- Add mixins
- Upgrade sweep method and plot_auto for tnr data

## 0.11.0

- Split maser into several submodules by namespace

## 0.10.0

- Update package dependencies in pyproject.toml
- Remove CDF class backup instance
- Add read_l2_hres() and read_l2_60s() methods in maser.data.stereo.swaves
- Minor bug fixes

  0.9.3

---

- added Saturn data support and new data organisation
- Update dependencies

  0.9.2

---

- Minor hotfixes

  0.9.1

---

- Add read_l2_60s() method in maser.data.wind.waves.read_wind_waves_file.py
- Update read_l2_hres() output (now is dictionary instead of Waves_data object previously)

  0.9.0

---

- Add the numerical precision option for cdf_compare
- Correctly handle NRV scalar value in cdf_compare
- Update setup environment (add pyproject.toml)
- Update dev. environment (pre-commit)
- Remove services/helio and data/solo modules
- Minor improvement in codes

  0.8.3

---

- Hotfix in utils/cdf serializer

  0.8.2

---

- cdf_compare is now correctly called from the maser command line.
- Rework of logger usage in cdf_compare.
- zVar NRV values are now correctly written in output skeleton table file.
- Size of zvars with more than 1 digit are now correctly written into the output skeleton table file.

  0.8.1

---

- Fix bug when releasing 0.8.0

  0.8.0

---

- Update the cdf_validator tool
- Update the skeletoncdf tool
- Add skeletontable command
- Update CDPP data object
- Update unit tests for data modules

  0.7.1

---

- Fix dependencies installation bug (in requirements.txt)
- Change README.rst to README.md
- Change CHANGELOG.rst to CHANGELOG.md
- Change cdf import handling
- Update read_wind_waves_file.py for python3 syntax

  0.7.0

---

- Add cdf_compare function
- Update maser command line interface call
- Update obsolete openpyxl functions from the xlsx cdf converter
- Use CHANGELOG.rst to get MASER version (in setup.py and program)

  0.6.1

---

- Fix a bug in toolbox.py

  0.6.0

---

- Simplify the CDFLeapSeconds.txt file handling.
- Add the utils/time/time.py submodule to deal with time conversion

  0.5.0

---

- Update leapsec.py to allow usage of the $CDF_LEAPSECONDSTABLE env. variable as a default path for the CDFLeapSeconds.txt file
- Update leapsec section in the doc.

  0.4.4

---

- Update doc
- Update setup.py
- Add leapsec.py

  0.4.3

---

- Update setup.py and requirements.txt

  0.4.2

---

- Fix a bug in utils.cdf

  0.4.1

---

- Update doc
- Remove INSTALL.rst
- Update README.rst

  0.4.0

---

- Add solo/rpw modules
- Update cdf/converter/tools/xlsx methods
- Update README.rst

  0.3.0

---

- Add utils.cdf.converter.tools

  0.2.6

---

- Rename maser-py to maser4py
- Update doc. and src files.

  0.2.5

---

- Add requirements.txt and INSTALL.rst
- Update xlsx2skt.py to avoid zvar name cuts

  0.2.4

---

- Fix error in maser.utils.cdf.tools.py

  0.2.3

---

- Remove use of spacepy.pycdf module
- Add CHANGELOG.rst file

  0.2.2

---

- Add Empty attribute value checking in xlsx2skt

  0.2.1

---

- Add DOUBLE in cdfconverter PADVALUE

  0.2.0

---

- Modify the source code tree

  0.1.0

---

- First beta release
-
