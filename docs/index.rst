.. maser4py documentation master file, created by
   sphinx-quickstart on Mon Dec  7 12:42:37 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

maser4py |release|
##################

maser4py is a Python 3 package to deal with the MASER portal.
The MASER portal provides a centralized access to services, data and tools relative to the low frequency radio astronomy.

For more information about MASER, please visit: http://maser.lesia.obspm.fr/

Overview
========

maser4py modules are divided into three categories:

- **services**, Web service access clients and tools (i.e., Virtual Observatories, Data providers, etc.)
- **data**, radio astronomy data programs
- **utils**, generic utilities relative to the data formats and common tools

Content
=======

The maser4py package is organized as follows:

   maser/
      services/
         helio/
            Module to use data from the HELIO Virtual Observatory
      data/
         wind/
            Module related to the Wind NASA mission data
         solo/
            Module related to the Solar Orbiter mission data
      utils/
         cdf/
            Module to handle the NASA Common Data Format (CDF)
         toolbox/
            Module containing common tools for maser4py

maser4py support data files are stored in:

   maser/
      maser/support
         Directory containing support data

Details
=======

.. Contents:

.. toctree::
   :maxdepth: 2

   install
   data
   services
   utils
   appendices

Support
=======

The maser4py is developed at the LESIA (http://www.lesia.obspm.fr/) by:

* Xavier Bonnin - xavier dot bonnin at obspm dot fr
* Quynh Nhu Nguyen - quynh-nhu dot nguyen at obspm dot fr
* Baptiste Cecconi - baptiste dot cecconi at obspm dot fr

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
