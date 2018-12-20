CHANGELOG
====================

0.7.1
-----
* Fix dependencies installation bug (in requirements.txt)
* Change README.rst to README.md
* Change CHANGELOG.rst to CHANGELOG.md
* Change cdf import handling
* Update read_wind_waves_file.py for python3 syntax

0.7.0
-----
* Add cdf_compare function
* Update maser command line interface call
* Update obsolete openpyxl functions from the xlsx cdf converter
* Use CHANGELOG.rst to get MASER version (in setup.py and program)

0.6.1
-----
* Fix a bug in toolbox.py

0.6.0
-----
* Simplify the CDFLeapSeconds.txt file handling.
* Add the utils/time/time.py submodule to deal with time conversion


0.5.0
-----
* Update leapsec.py to allow usage of the $CDF_LEAPSECONDSTABLE env. variable as a default path for the CDFLeapSeconds.txt file
* Update leapsec section in the doc.

0.4.4
-----
* Update doc
* Update setup.py
* Add leapsec.py

0.4.3
-----
* Update setup.py and requirements.txt

0.4.2
-----
* Fix a bug in utils.cdf

0.4.1
-----
* Update doc
* Remove INSTALL.rst
* Update README.rst

0.4.0
-----
* Add solo/rpw modules
* Update cdf/converter/tools/xlsx methods
* Update README.rst

0.3.0
-----
* Add utils.cdf.converter.tools

0.2.6
-----
* Rename maser-py to maser4py
* Update doc. and src files.

0.2.5
-----
* Add requirements.txt and INSTALL.rst
* Update xlsx2skt.py to avoid zvar name cuts

0.2.4
-----
* Fix error in maser.utils.cdf.tools.py

0.2.3
-----
* Remove use of spacepy.pycdf module
* Add CHANGELOG.rst file

0.2.2
-----
* Add Empty attribute value checking in xlsx2skt

0.2.1
-----
* Add DOUBLE in cdfconverter PADVALUE

0.2.0
-----
* Modify the source code tree

0.1.0
-----
* First beta release
*