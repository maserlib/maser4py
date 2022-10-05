Installation
=============

Pre-requisites
----------------

The following software will be required to install and run maser4py:

    - `Python 3 <https://www.python.org/>`_ and `pip <https://pypi.org/project/pip/>`_ tool (tested on Python 3.8, 3.9 and 3.10)
    - `git <https://git-scm.com/>`_ tool is needed to get source files
    - `poetry <https://python-poetry.org/>`_ package is recommended to install the package from source files

Using pip
---------------

To install the full package, run the following command:

.. code:: bash

    pip install maser4py[all]


If the installation has ended correctly, the following command should return the maser4py version:

.. code:: bash

    maser --version


It is also possible to choose the submodules to install.

For instance, to install only ``maser-data`` and ``maser-plot`` submodules:

.. code:: bash

    pip install maser4py[data, plot]


Following options are currently available:

- ``data`` to get `maser-data <https://pypi.org/project/maser-data/>`_ submodule features
- ``plot`` to get `maser-plot <https://pypi.org/project/maser-plot/>`_ submodule features
- ``tools`` to get `maser-tools <https://pypi.org/project/maser-tools/>`_ submodule features
- ``jupyter`` to install Jupyter for notebook support
- ``jupytext`` to install Jupyter for notebook text support
- ``all`` to install all the submodules above

From
---------------

To retrieve maser4py source files:

.. code:: bash

    git clone https://gitlab.obspm.fr/maser/maser4py.git

.. note::

    The ``master`` branch will be retrieved by default. Use ``--branch develop`` option to get the development version.

Then install `poetry <https://python-poetry.org/>`_ package:

.. code:: bash

    pip install poetry

Finally install maser4py package, executing the following command from the maser4py main directory:

.. code:: bash

    poetry install

.. note::

    By default poetry will install package in the editable mode. See poetry manual for more details.
