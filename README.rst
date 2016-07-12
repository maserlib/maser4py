--------------------------------------------------------
 MASER-PY:
 The MASER project package for Python
 --------------------------------------------------------
 X.Bonnin (LESIA, CNRS), 10-NOV-2015

 MASER-PY python package contains modules to
 deal with services and data provided in the framework
 on the MASER project (Mesures, Analyses et Simulations d’Emissions Radio).

 For more information about MASER, please visit:
 http://maser.lesia.obspm.fr/


 INSTALLATION
 -----------------------

 In order to install MASER-PY, make sure to have Python 3.4 or higher
 available on your system.

 The package installation requires the following Python modules:
    - setuptools (12.0.5 or higher)

  If they are not found, the following Python modules will
  be downloaded automatically during the installation:
    - openpyxl
    - simplejson

    In order to use the "cdf" submodule, the NASA CDF software
    distribution shall be installed and configured on your system.
    Especially, make sure that the directory containing the CDF binary
    executables is on your $PATH, and the $CDF_LIB env. var. is set.
