============
Installation
============

System Requirements
===================

In order to install maser4py, make sure to have Python 3.4 (or higher) as well as the pip and setuptools programs available on your system.

If there are not found, the following Python modules will be also installed:

- openpyxl
- numpy
- matplolib
- sphinx

maser4py has been tested on the following Operating Systems:

- Mac OS X 10.10 or higher
- Debian Jessie 8.2 or higher

.. warning::

    Make sure that the NASA CDF software
    distribution is installed and configured on your system.
    Visit https://cdf.gsfc.nasa.gov/ for more details.

How to install maser4py?
========================

From pip
--------

If the pip tool is installed on your system, just enter:

.. code-block:: bash

    pip install maser

From Github
-----------

1. To get MASER4PY source files from Github, enter:

.. code-block:: bash

    git clone https://github.com/maserlib/maser4py.git

Make sure to have Git (https://git-scm.com/) installed on your system.

If everything goes right, you should have a new local "maser4py" directory created on your disk.

2. From the "maser4py" main directory, install program dependencies:

.. code-block:: bash

    pip3 install -r requirements.txt

3. To install the package on your system, enter the following
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


How to run maser4py?
====================

If the installation has ended correctly, you can run maser4py:

  - From a Python interpreter session, by entering "import maser".
  - Using the command line interface available for some maser4py modules.

For more details about the MASER4PY modules, please read the user manual.
