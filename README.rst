MASER4PY: The Python 3 package for MASER
=====================================
X.Bonnin (LESIA, Obs. Paris, CNRS), 20-OCT-2016

About MASER4PY
--------------

MASER4PY python package contains modules to
deal with services, data and tools provided in the framework
on the MASER portal.


Installation
---------------

In order to install the maser4py python module:

1. Make sure that Python 3.4 or higher is already installed on your system.

2. Install and configure the NASA CDF software (visit http://cdf.gsfc.nasa.gov/ for more details).

3. Install numpy 1.11.0 or higher by entering:

    pip install numpy>=1.11.0

4. From the maser4py directory, install the module by entering:

    python setup.py install

Usage
-------

From Python, enter "import maser".
The module also offers specific command line interfaces.

For more details, see the user manual in pdf format (doc/build/latex/maser4py.pdf) or html format (doc/build/index.html).

MASER4PY content
----------------

The maser4py directory contains the following items:

- doc/  stores the maser4py documentation (source and build)
- maser/ stores the maser4py source files
- scripts/ store scripts to run/test/manage maser4py
- __main__.py python script to run maser.main program
- CHANGELOG.rst software change history log
- MANIFEST.in files to be included to the package installation (used by setup.py)
- README.rst current file
- requirements.txt list of python package dependencies and versions
- setup.cfg file used by sphinx to build the maser4py doc.
- setup.py maser4py package setup file

About MASER
-----------

The MASER portal (Mesures, Analyses et Simulations d’Emissions Radio) gives an access to tools and database related to low frequency radioastronomy (from few kilohertz up to several tens of megahertz). The radio measurements in the spectral range are realized with ground observatories (for the frequencies above the 10 MHz Earth ionospheric cut-off) or from spacecraft (at lower frequencies).

In this frequency range, the main radio sources are the Sun and the magnetized planets. The low frequency fluctuations measurement of the electric and magnetic fields can also provide a diagnosis on the local plasma conditions, and in-situ observations of plasma waves phenomena in the Solar Wind and the planetary environements.

* For more information about the MASER project: http://maser.lesia.obspm.fr/ (in french)
* For more information about MASER4PY: https://github.com/maserlib/maser4py



