Introduction
====================================

About
--------------------

MASER4PY is a Python 3 package to deal with data from the MASER portal.
The MASER portal provides access to services, data and tools in the framework of the radio astronomy.

For more information about MASER, please visit: http://maser.lesia.obspm.fr/

Overview
--------------------

MASER4PY modules are divided in three categories:

- **services**, Web service access
- **data**, radio astronomy data handling
- **utils**, generic utilities

Content
~~~~~~~~~~~~~~~~~~~~

The MASER4PY package is organized as follows:

    maser/
        services/
            helio/
                Module to use data from the HELIO Virtual Observatory.
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


Installation
--------------------------------

System Requirements
~~~~~~~~~~~~~~~~~~~~

In order to install MASER4PY, make sure to have Python 3.4 or higher
available on your system.

The package installation requires the following Python modules:

- setuptools
- openpyxl
- numpy
- matplolib
- sphinx

MASER4PY has been tested on the following Operating Systems:

- Mac OS X 10.10 or higher
- Debian Jessie 8.2 or higher

In order to use the "cdf" submodule, the NASA CDF software
distribution (https://cdf.gsfc.nasa.gov/) shall be installed and configured on your system.
Especially, make sure that the directory containing the CDF binary
executables is on your $PATH, and the $CDF_LIB env. var. is set.

How to get MASER4PY?
~~~~~~~~~~~~~~~~~~~~

From pip
..........

If the pip tool is installed on your system, just enter:

.. code-block:: bash

    pip install maser4py

From Github
............

To get MASER4PY from Github, enter:

.. code-block:: bash

    git clone https://github.com/maserlib/maser4py.git

Make sure to have Git (https://git-scm.com/) installed on your system.

If everything goes right, you should have a new local "maser4py" directory created on your disk.

How to install MASER4PY?
~~~~~~~~~~~~~~~~~~~~

From the "maser4py" main directory, install program dependencies:

.. code-block:: bash

    pip3 install -r requirements.txt

To install the package on your system, enter the following
command :

.. code-block:: bash

    python3 setup.py install

This should install the maser4py package on your
system.

To check that the installation ends correctly, you can enter:

.. code-block:: bash

    maser4py

, which should return something like:

.. code-block:: bash

    "This is maser4py package VX.Y.Z"

If you have an issue during installation, please read the "Troubleshooting" section for help.

How to run MASER4PY?
~~~~~~~~~~~~~~~~~~~~

If the installation has ended correctly, you can run MASER4PY:

  - From a Python interpreter session, by entering "import maser".
  - Using the command line interface available for some MASER4PY modules.

For more details about the MASER4PY modules, please read the user manual.

Contacts
--------------

* Xavier Bonnin - xavier.bonnin@obspm.fr
* Quynh Nhu Nguyen - quynh-nhu.nguyen@obspm.fr
* Baptiste Cecconi - baptiste.cecconi@obspm.fr
