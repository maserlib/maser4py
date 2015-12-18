Introduction
====================================

The MASER python package (MASER-PY) contains modules to
deal with services and data provided in the framework
of the MASER portal.

For more information about MASER, please visit: http://maser.lesia.obspm.fr/

Installation
====================================

System Requirements
--------------------------------

In order to install MASER, make sure to have Python 3.4 or higher
available on your system.

The package installation requires the following Python modules:
- setuptools (12.0.5 or higher)

If they are not found, the following Python packages will
be downloaded automatically during the installation:
- openpyxl
- spacepy
- simplejson

MASER-PY has been tested on the following Operating Systems:
- Mac OS X 10.10, 10.11
- Debian Jessie 8.2

In order to use the "cdf" submodule, the NASA CDF software
distribution shall be installed and configured on your system.
Especially, make sure that the directory containing the CDF binary
executables is on your $PATH, and the $CDF_LIB env. var. is set.

How to get MASER-PY
---------------------------------

To download MASER-PY, enter the following command from a terminal:

    git clone git://git.renater.fr/maser/maser-py.git

Make sure to have Git (https://git-scm.com/) installed on your system.

If everything goes right, you should have a new local "maser-py" directory created on your disk.

How to set up MASER-PY
-------------------------------------

To set up the package on your system, enter the following
command from the "maser-py" directory:

    python3 setup.py install

This should install the maser-py package on your
system.

To check that the installation ends correctly, you can enter:

    maser-py

, which should return something like:

    "This is maser-py package VX.Y.Z"

If you have an issue durint installation, please read the "Troubleshooting" section for help.

How to run MASER-PY
-------------------------------------

If the installation has ended correctly, you can run MASER-PY:

  - From a Python interpreter session, by entering "import maser".
  - Using the command line interface available for some MASER-PY modules.

For more details about the MASER-PY modules, please read the user manual.

Overview
====================================

The MASER-PY package is organized as follows:

    maser/
        services/
            helio/
                Module to get and plot the HELIO Virtual Observatory data.
        data/
            wind/
                Module to handle the Wind NASA mission data.
        utils/
            cdf/
                Module to handle the NASA Common Data Format (CDF).
            toolbox/
                Module containing common tool methods for MASER-PY

In order to work, the MASER-PY package modules rely on additional files and directories:

maser/support
    Directory containing support data
