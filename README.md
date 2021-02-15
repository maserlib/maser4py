[![PyPI version](https://badge.fury.io/py/maser4py.svg)](https://img.shields.io/pypi/pyversions/maser4py)
[![license](https://img.shields.io/pypi/l/maser4py)](https://pypi.python.org/pypi/maser4py)
[![Documentation Status](https://readthedocs.org/projects/maser/badge/?version=latest)](https://maser.readthedocs.io)

About maser4py
==============

**maser4py** python package offers tools for radioastronomy at low frequency.

It contains modules to deal with services, data and tools provided in the framework
of the MASER portal (http://maser.lesia.obspm.fr).

Read maser4py [documentation][maser4py readthedocs] for more information.

[maser4py readthedocs]: https://maser.readthedocs.io/en/latest

Installation
==============

Prerequisites
--------------


Python 3 must be available (tested with 3.6 and 3.8).

The maser4py also requires the NASA CDF software to be run (visit http://cdf.gsfc.nasa.gov/ for more details). Especially the CDFLeapSeconds.txt file
should be on the local disk and reachable from the $CDF_LEAPSECONDSTABLE env. variable. If it is not the case, maser4py offers tools to read and/or download
this file from the NASA Web site (see user manual for more details).

Using pip
----------

From a terminal, enter:

   pip install maser4py

Using source
-------------

From a terminal, enter:

    git clone https://github.com/maserlib/maser4py

Then, from the maser4py directory, enter:

    pip install -r requirements.txt

Then,

    python3 setup.py install


Usage
======

From Python, enter "import maser".
The module also offers specific command line interfaces.

For more details, see the maser4py user manual.

Content
=========

The maser4py directory contains the following items:

::

    doc/  stores the maser4py documentation (source and build)

    maser/ stores the maser4py source files

    scripts/ store scripts to run/test/manage maser4py

    __main__.py python script to run maser.main program

    CHANGELOG.rst software change history log

    MANIFEST.in files to be included to the package installation (used by   tup.py)

    pyproject.tom Python package pyproject file

    README.md current file

    requirements.txt list of python package dependencies and versions

    setup.cfg file used by sphinx to build the maser4py doc.

    setup.py maser4py package setup file

About MASER project
====================

The MASER (Measuring, Analyzing & Simulating Emissions in the Radio range) portal is offering access to a series of tools and databases linked to low frequency radioastronomy (a few kilohertz to a few tens of megahertz). Radio measurements in this spectral range are done with ground based observatories (for frequencies above the terrestrial ionosphere cutoff at 10 MHz) or from space based platforms (at low frequencies).

In this frequency range, the main radio sources are the Sun and the magnetized planets. Measurements of the low frequency electric and magnetic field fluctuations can also provide local plasma diagnostics and in-situ observations of plasma waves phenomena in the Solar Wind or in planetary environments.

* For more information about the MASER project: http://maser.lesia.obspm.fr/
* For more information about MASER4PY: https://github.com/maserlib/maser4py

Acknowledgements
==================

The development of the MASER library is supported by Observatoire de Paris, CNRS (Centre National de la Recherche Scientique) and CNES (Centre National d'Etudes Spatiales). The technical support from PADC (Paris Astronomical Data Centre) and CDPP (Centre de Données de la Physique des Plasmas) is also acknowledged.

The project has also received support from the European Union through:
* HELIO (Heliophysics Integrated Observatory), which received funding from Capacities Specific Programme of the European Commission's Seventh Framework Programme (FP7) under grant agreement No 238969;
* EPN2020RI (Europlanet 2020 Research Infrastructure project), which received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 654208.
