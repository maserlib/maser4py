.. maser4py documentation master file, created by
   sphinx-quickstart on Mon Dec  7 12:42:37 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MASER4PY |release|
##################

MASER4PY is a Python 3 package to deal with the MASER portal services and data.
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
            Module to use some of the HELIO Virtual Observatory services (http://www.helio-vo.eu/)
      data/
         cassini/
            Module to handle the CASSINI mission data
         cdpp/
            Module to handle the data archived at CDPP (http://www.cdpp.eu/)
         nancay/
            Module to handle the Nancay Observatory data
         padc/
            Module to handle the PADC data (https://padc.obspm.fr/)
         pds/
            Module to handle the NASA PDS data (https://pds.nasa.gov/)
         psa/
            Module to handle the ESA PSA data (https://archives.esac.esa.int/psa/)
         radiojove/
            Module to handle the Radiojove project data (http://www.radiojove.org/)
         solo/
            Module related to the Solar Orbiter mission data (in progress)
         wind/
            Module related to the Wind mission data
      utils/
         cdf/
            Module to handle the NASA Common Data Format (CDF)
         das2stream/
            Module related to DAS2 server (https://das2.org/)
         time/
            Module to handle time.
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
* Alan Loh - alan dot loh at obspm dot fr
* Sonny Lion - sonny dot lion at obspm dot fr

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
