maser4py: The Python 3 package for the MASER portal
###################################################
X.Bonnin (LESIA, Obs. Paris, CNRS), 20-MAR-2017

About maser4py
==============

maser4py python package contains modules to
deal with services, data and tools provided in the framework
of the MASER portal.


Installation
============

Make sure that Python 3.4 (or higher) as well as pip and setuptools are already installed on your system.

The maser4py also requires the NASA CDF software to be run (visit http://cdf.gsfc.nasa.gov/ for more details). Especially the CDFLeapSeconds.txt file
should be on the local disk and reachable from the $CDF_LEAPSECONDSTABLE env. variable. If it is not the case, maser4py offers tools to read and/or download
this file from the NASA Web site (see user manual for more details).

Using pip
---------

From a terminal, enter:

   pip install maser4py

Using Source
------------

From a terminal, enter:

    git clone https://github.com/maserlib/maser4py

Then, from the maser4py directory, enter:

    pip install -r requirements.txt

Then,

    python3 setup.py install


Usage
=====

From Python, enter "import maser".
The module also offers specific command line interfaces.

For more details, see the maser4py user manual available in the pdf format (in doc/build/latex/maser4py.pdf) or from https://pypi.python.org/pypi/maser4py (see in "Package Documentation").

Tree
====

The maser4py directory contains the following items:

::

    doc/  stores the maser4py documentation (source and build)

    maser/ stores the maser4py source files

    scripts/ store scripts to run/test/manage maser4py

    __main__.py python script to run maser.main program

    CHANGELOG.rst software change history log

    MANIFEST.in files to be included to the package installation (used by   tup.py)

    README.rst current file

    requirements.txt list of python package dependencies and versions

    setup.cfg file used by sphinx to build the maser4py doc.

    setup.py maser4py package setup file

About MASER
===========

The MASER portal (Mesures, Analyses et Simulations d’Emissions Radio) gives an access to tools and database related to low frequency radioastronomy (from few kilohertz up to several tens of megahertz). The radio measurements in the spectral range are realized with ground observatories (for the frequencies above the 10 MHz Earth ionospheric cut-off) or from spacecraft (at lower frequencies).

In this frequency range, the main radio sources are the Sun and the magnetized planets. The low frequency fluctuations measurement of the electric and magnetic fields can also provide a diagnosis on the local plasma conditions, and in-situ observations of plasma waves phenomena in the Solar Wind and the planetary environements.

* For more information about the MASER project: http://maser.lesia.obspm.fr/ (in french)
* For more information about MASER4PY: https://github.com/maserlib/maser4py



