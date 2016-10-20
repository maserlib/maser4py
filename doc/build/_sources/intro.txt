Introduction
====================================

The MASER4PY python package contains modules to
deal with services, data and tools provided in the framework
of the MASER portal.

For more information about MASER, please visit: http://maser.lesia.obspm.fr/

Installation
====================================

System Requirements
--------------------------------

In order to install MASER4PY, make sure to have Python 3.4 or higher
available on your system.

The package installation requires the following Python modules:
- setuptools (12.0.5 or higher)
- openpyxl
- numpy (1.11.0 or higher)
- simplejson

MASER4PY has been tested on the following Operating Systems:
- Mac OS X 10.10
- Debian Jessie 8.2

In order to use the "cdf" submodule, the NASA CDF software
distribution shall be installed and configured on your system.
Especially, make sure that the directory containing the CDF binary
executables is on your $PATH, and the $CDF_LIB env. var. is set.

How to get MASER4PY?
---------------------------------

The MASER4PY package is available on Github:

    https://github.com/maserlib/maser4py

To download MASER4PY, enter the following command from a terminal:

    git clone https://github.com/maserlib/maser4py.git

Make sure to have Git (https://git-scm.com/) installed on your system.

If everything goes right, you should have a new local "maser4py" directory created on your disk.

How to install MASER4PY?
-------------------------------------

To set up the package on your system, enter the following
command from the "maser4py" directory:

    python3 setup.py install

This should install the maser4py package on your
system.

To check that the installation ends correctly, you can enter:

    maser4py

, which should return something like:

    "This is maser4py package VX.Y.Z"

If you have an issue during installation, please read the "Troubleshooting" section for help.

How to run MASER4PY?
-------------------------------------

If the installation has ended correctly, you can run MASER4PY:

  - From a Python interpreter session, by entering "import maser".
  - Using the command line interface available for some MASER4PY modules.

For more details about the MASER4PY modules, please read the user manual.

Overview
====================================

The MASER4PY package is organized as follows:

    maser/
        services/
            helio/
                Module to get and plot the HELIO Virtual Observatory data.
        data/
            wind/
                Module related to the Wind NASA mission data.
            solo/
                Module related to the Solar Orbiter mission data.
        utils/
            cdf/
                Module to handle the NASA Common Data Format (CDF).
            toolbox/
                Module containing common tool methods for MASER-PY

In order to work, the MASER4PY package modules also rely on additional files and directories:

maser/support
    Directory containing support data
