Utilities
#########

The utils/ module of MASER4PY provides utilities to deal with data in MASER.


The *cdf* module
*****************

The *cdf* module contains the following tools:

- *cdf*, a backup of the spacepy.pycdf module (https://pythonhosted.org/SpacePy/pycdf.html), only used in the case where spacepy package is not installed in the system.
- *cdfcompare*, a tool to compare two CDFs
- *serializer*, to convert skeleton CDF files (in Excel or ASCII format) into master CDF binary files
- *validator*, to validate the content of a CDF file from a given data model.

For more information about the CDF format, please visit http://cdf.gsfc.nasa.gov/.

cdf.cdfcompare
==========================

The *cdf.cdfcompare* module can be used to compare the content of two CDFs.



cdf.serializer
==========================

The *cdf.serializer* module allows users to convert CDF between the following formats:

- Skeleton table (ASCII)
- Binary CDF ("Master")
- Excel 2007 format (.xlsx)

Module can be imported in Python programs or called directly from a terminal using the dedicated command line interface.

Excel format description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section describes the structure of the Excel format file that can be used by the cdf.serializer module.

Note that:

* Only the Excel 2007 format is supported (i.e., .xlsx).
* Only zVariables are supported

.. warning::

  Make sure to respect the letter case!

The Excel file shall contain the following sheets:

- header
- GLOBALattributes
- zVariables
- VARIABLEattributes
- NRV

The first row of each sheet must be used to provide the name of the columns.

*header* sheet
""""""""""""""

The "header" sheet must contain the following columns:

CDF_NAME
  Name of the CDF master file (without the extension)
DATA ENCODING
  Type of data encoding
MAJORITY
  Majority of the CDF data parsing ("COLUMN" or "ROW")
FORMAT
  Indicates if the data are saved in a single ("SINGLE") or
  on multiple ("MULTIPLE") CDF files
CDF_COMPRESSION
  Type of compression applied to the CDF
CDF_CHECKSUM
  Checksum applied to the CDF

*GLOBALattributes* sheet
""""""""""""""""""""""""

The "GLOBALattributes" sheet shall contain the following columns:

Attribute Name
  Name of the global attribute
Entry Number
  Index of the current entry starting at 1
Data Type
  CDF data type of the global attribute (only the "CDF_CHAR" type is supported)
Value
  Value of the current entry

*zVariables* sheet
""""""""""""""""""

The "zVariables" sheet shall contain the following columns:

Variable Name
  Name of the zVariable
Data Type
  CDF data type of the zVariable
Number Elements
  Number of elements of the zVariable (shall be always 1, except for CDF_[U]CHAR" type)
Dims
  Number of dimension of the zVariable (shall be 0 if the variable is a scalar)
Sizes
  If the variable is not a scalar, provides its dimension sizes.
Record Variance
  Indicates if the variable values can change ("T") or not ("F") from a record to another.
Dimension Variances
  Indicates how the variable values vary over each dimension.
VAR_COMPRESSION
  Compression algorithm applied to the variable.
VAR_SPARESERECORDS
  Spare record of the variable.
VAR_PADVALUE
  Pad value of the variable.

*VARIABLEattributes* sheet
""""""""""""""""""""""""""

The "VARIABLEattributes" sheet shall contain the following columns:

Variable Name
  Name of the zVariable
Attribute Name
  Name of the variable attribute
Data Type
  CDF data type of the variable attribute
Value
  Value of the variable attribute


*NRV* sheet
"""""""""""

The "NRV" sheet shall contain the following columns:

Variable Name
  Name of the zVariable
Index
  Index of the current NR row
Value
  Value of the current NR row

Command line interface
^^^^^^^^^^^^^^^^^^^^^^

*skeletontable* sub-command
"""""""""""""""""""""""""""

The *skeletontable* sub-command allows to convert CDF from binary CDF to skeleton table by calling the skeletontable NASA CDF software program.

An option also permits to export skeleton table into Excel 2007 format file (.xlsx).

To display the help, enter:

::

  maser skeletontable --help

Examples
^^^^^^^^

Convert all input CDFs named "input_*.cdf" into skeleton tables. Output files will be saved into the /tmp/cdf/build folder. Output files will have the same names than input CDFs but with the extension ".skt".

::

   maser skeletontable "input_*.cdf" --output_dir /tmp/cdf/build


Convert the input binary CDF named "input1.cdf" into skeleton table. Output files will be saved into the /tmp/cdf/build folder. Output file will have the same name than input CDF but with the extension ".skt". An export file in Excel 2007 format (input1.xlsx) will also be saved.

::

   maser skeletontable "input1.cdf" --output_dir /tmp/cdf/build --to-xlsx

*skeletoncdf* sub-command
"""""""""""""""""""""""""""

The *skeletoncdf* sub-command allows to convert CDF from skeleton table to binary CDF by calling the skeletoncdf NASA CDF software program.

An option also permits to use Excel 2007 format file (.xlsx) as an input to the *skeletoncdf* sub-command.

To display the help, enter:

::

  maser skeletoncdf --help



Examples
^^^^^^^^

Convert all input skeleton tables named "input_*.skt" into binary CDFs. Output files will be saved into the /tmp/cdf/build folder. Output files will have the same names than input files but with the extension ".cdf".

::

   maser skeletoncdf "input_*.skt" --output_dir /tmp/cdf/build


Convert the input Excel format file named "input1.xlsx" into skeleton table and binary CDF. Output files will be saved into the /tmp/cdf/build folder. Output files will have the same name than input CDF but with the extension ".skt". An export file in Excel 2007 format (.xlsx) will also be saved.

::

   maser skeletoncdf "input1.xlsx" --output_dir /tmp/cdf/build

If the conversion from Excel to ASCII skeleton table is required only, then add the --no-cdf input keyword to the command line to not create the binary CDF.

Limitations & Known Issues
^^^^^^^^^^^^^^^^^^^^^^^^^^

TBW


The *cdf.validator* tool
========================

*validator* provides methods to validate a CDF format file from a given model.

It contains only one *Validate* class that regroups all of the validation methods.


The *Validate* class
--------------------

To import the *Validate* class from Python, enter:

.. code-block:: python

  from maser.utils.cdf.cdfvalidator import Validate

The Model validation test
^^^^^^^^^^^^^^^^^^^^^^^^^

The *Validate* class allows user to check if a given CDF format file contains specific attributes or variables, by providing a
so-called "cdfvalidator model file".

This model file shall be in the JSON format. All items and values are case sensitive.
It can include the following JSON objects:

.. csv-table::  CDFValidator JSON objects
   :header: "JSON object", "Description"
   :widths: 35, 65

   "GLOBALattributes", "Contains the list of global attributes to check"
   "VARIABLEattributes", "Contains the list of variable attributes to check"
   "zVariables", "Contains the list of zvariables to check"

Note that any additional JSON object will be ignored.

The table below lists the JSON items that are allowed to be found in the *GLOBALattributes*, *VARIABLEattributes* and *zVariables* JSON objects.

.. csv-table::  CDFValidator JSON object items
   :header: "JSON item", "JSON type", "Priority", "Description"
   :widths: 45, 15, 15, 35

    "attributes", "vector", "optional", "List of variable attributes. An element of the vector shall be a JSON object that can contain one or more of the other  JSON items listed in this table"
    "dims", "integer", "optional", "Number of dimensions of the CDF item"
    "entries", "vector", "optional", "Entry value(s) of the CDF item to be found"
    "hasvalue", "boolean", "optional", "If it is set to true, then the current CDF item must have at least one nonzero entry value"
    "name", "string", "mandatory", "Name of the CDF item (attribute or variable) to check"
    "sizes", "vector", "optional", "Dimension sizes of the CDF item"
    "type", "attribute", "optional", "CDF data type of the CDF item "


Command line interface
----------------------

To display the help of the module, enter:

::

  cdf_validator --help

The full calling sequence is:

::

    maser cdf_validator [-h] [-m MODEL_FILE] [-c CDFVALIDATE_BIN] [-I] [-C] cdf_file

positional arguments:
  cdf_file              Path of the CDF format file to validate

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL_FILE, --model-file MODEL_FILE
                        Path to the model file in JSON format
  -c CDFVALIDATE_BIN, --cdfvalidate-bin CDFVALIDATE_BIN
                        Path of the cdfvalidate NASA CDF tool executable
  -I, --istp            Check the ISTP guidelines compliance
  -C, --run-cdfvalidate
                        Run the cdfvalidate NASA CDF tool

Example
^^^^^^^

To test the cdf.validator program, use the dedicated scripts/test_cdfvalidator.sh bash script.

It should return something like:

.. code-block:: python

  INFO    : Opening /tmp/cdfconverter_example.cdf
  INFO    : Loading /Users/xbonnin/Work/projects/MASER/Software/Tools/Git/maser-py/scripts/../maser/support/cdf/cdfvalidator_model_example.json
  INFO    : Checking GLOBALattributes:
  INFO    : --> Project
  WARNING : "Project"  has a wrong entry value: "Python>Python 2" ("Python>Python 3" expected)!
  INFO    : --> PI_name
  INFO    : --> TEXT
  INFO    : Checking VARIABLEattributes:
  INFO    : --> FIELDNAM
  INFO    : --> CATDESC
  INFO    : --> VAR_TYPE
  INFO    : Checking zVariables:
  INFO    : --> Epoch
  INFO    : --> Variable2
  INFO    : Checking variable attributes of "Variable2":
  INFO    : --> DEPEND_0
  WARNING : DEPEND_0 required!
  INFO    : Closing /tmp/cdfconverter_example.cdf


The *time* module
*****************

The *leapsec* tool
==================

The *leapsec* tool allows users to handle the leap seconds.

Using the leapsec tool requires to read the CDFLeapSeconds.txt file. This file is available on the NASA CDF Web site (https://cdf.gsfc.nasa.gov).

.. warning::
  Before using the leapsec tool, it is highly recommended to have the CDFLeapSeconds.txt file saved on the localdisk, and reachable from the $CDF_LEAPSECONDSTABLE env. variable. If the file is not on the disk, the tool will attempt to read the file directly from the NASA CDF Web site.

The *Lstable* class
-------------------
The Lstable class provides the methods to deal with the
CDFLeapSeconds.txt table file.

To import the *Lstable* class from Python, enter:

.. code-block:: python

  from maser.utils.time import Lstable

Then, to load the CDFLeapSeconds.txt table, first enter:

.. code-block:: python

  lstable = Lstable(file=path_to_the_file)

.. note::
  Note that if the optional input keyword *file=* is not set, the tool will
  first check if the path is given in the $CDF_LEAPSECONDSTABLE environment variable. If not, then the program will look into the maser/support/data sub-folder of the package directory. Finally, if it is still not found, it will attempt to retrieve the table data from the file on the
  NASA CDF Web site (https://cdf.gsfc.nasa.gov/html/CDFLeapSeconds.txt)

Once the table is loaded, then to print the leap seconds table, enter:

.. code-block:: python

  print(lstable)


To get the total elapsed leap seconds for a given date, enter:

.. code-block:: python

  lstable.get_leapsec(date=date_time)

Where date_time is a datetime object of the datetime module.


Downloading the CDFLeapSeconds.txt file from the NASA Web site can be done
by entering:

.. code-block:: python

  Lstable.get_lstable_file(target_dir=target_dir, overwrite=overwrite)

Where *target_dir* is the local directory where the CDFLeapSeconds.txt file will be saved. *overwrite* keyword can be used to replace existing file (default is *overwrite=False*)

.. note::
  get_lstable_file is a staticmethod, which does not require to instanciate the
  Lstable class.

.. note::
  If the method is called without the *target_dir=* input keyword (i.e., *get_lstable()*), then it will first check if the $CDF_LEAPSECONDSTABLE env. variable is defined, if yes the *target_dir* will be set with the $CDF_LEAPSECONDSTABLE value, otherwise the file is saved in the
  maser/support/data folder of the module.


Command line interface
-----------------------

To display the help of the module, enter:

::

  maser leapsec --help

The full calling sequence is:

::

  maser leapsec [-h] [-D] [-O] [-S] [-f FILEPATH] [-d DATE]

Input keywords:

-h, --help            show this help message and exit
-f FILEPATH, --filepath FILEPATH
                      CDFLeapSeconds.txt filepath. Default is
                      [maser4py_rootdir]/support/data/CDFLeapSeconds.txt,
                      where [maser4py_rootdir] is the maser4py root directory.
-d DATE, --date DATE  Return the leap seconds for a given date and
                      time. (Expected format is "YYYY-MM-DDThh:mm:ss")
-S, --SHOW-TABLE      Show the leap sec. table
-O, --OVERWRITE       Overwrite existing file
-D, --DOWNLOAD-FILE
                      Download the CDFLeapSeconds.txt from
                      the NASA CDF site. The file will be saved in the path
                      defined in the --filepath argument..

The *time* tool
==================

The *time* tool offers time conversion methods between the following time systems:

- UTC: Coordinated Universal Time
- JD: Julian Days
- MJD: Modified Julian Days
- TT: Terrestrial Time
- TAI: International Atomic Time
- TT2000: Terrestrial Time since J2000 (2000-01-01T12:00:00)

.. note::
  The time conversion inside the methods is performed using numpy.timedelta64 and numpy.datetime64 objects for better time resolution.

.. warning::
  The highest time resolution of JD and MJD systems are fixed to microsecond. The TT2000 system can reach the nanosecond resolution.
