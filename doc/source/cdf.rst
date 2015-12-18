The *cdf* module
====================================

The *cdf* module is divided in two submodules:

- *cdfconverter*, which allows users to convert CDF skeleton files into master CDF binary files
- *cdfvalidator*, which allows users to perform some validations on CDF files.

For more information about the CDF format, please visit http://cdf.gsfc.nasa.gov/.

The *cdfconverter* submodule
-------------------------------------------

*cdfconverter* contains the following classes:

- *Xlsx2skt*, convert an Excel 2007 format file into a CDF skeleton table in the ASCII format. The organization of the Excel file shall follow some rules defined in the present document (see the section "Excel file format definition" below)
- *Skt2cdf*, convert a CDF skeleton table in ASCII format into a CDF master binary file. This module calls the "skeletoncdf" program from the NASA CDF software distribution.

Both classes can be imported from Python or called directly from a terminal using the dedicated command line interface.

The Xlsx2skt class
````````````````````````````

To import the Xlsx2skt class from Python, enter:

.. code-block:: python

  from maser.cdf.cdfconverter import Xlsx2skt

Excel file format definition
''''''''''''''''''''''''''''''''''''''''''''''''''''

This section describes the organization of the input skeleton file in Excel format.

Note that:

* xlsx2skt supports the Excel 2007 format only (i.e., .xlsx).
* Only zVariables are supported

**Make sure to respect the letter case, since the xlsx2skt parser is case sensitive!**

The input Excel file shall contain the following sheets:

- header
- GLOBALattributes
- zVariables
- VARIABLEattributes
- Options
- NRV

The first row of each sheet shall be used to provide the name of the columns.

*header* sheet
............................

The "header" sheet shall contain the following columns:

CDF_NAME
  Name of the CDF master file (without the extension)
DATA ENCODING
  Type of data encoding
MAJORITY
  Majority of the CDF data parsing ("COLUMN" or "ROW")
FORMAT
  Indicates if the data are saved in a single ("SINGLE") or
  on multiple ("MULTIPLE") CDF files

*GLOBALattributes* sheet
.................................................

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
.................................................

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

*VARIABLEattributes* sheet
.....................................................

The "VARIABLEattributes" sheet shall contain the following columns:

Variable Name
  Name of the zVariable
Attribute Name
  Name of the variable attribute
Data Type
  CDF data type of the variable attribute
Value
  Value of the variable attribute

*Options* sheet
..............................................

The "Options" sheet shall contain the following columns:

CDF_COMPRESSION
  Type of compression of the CDF file ("None" or empty field indicates no compression)
CDF_CHECKSUM
  Checksum algorithm of the CDF file ("None" or empty field indicates no checksumming)
VAR_COMPRESSION
  Type of compression of each CDF variable ("None" or empty field indicates no compression)
VAR_SPARSERECORDS
  value of sparese records ("None" or empty field indicates no sparese value)
VAR_PADVALUE
  padvalue to provide to each variable. This option only works in the
  case where all of the CDF variables has the same data type.
  In the other cases, users should use the --Auto_pad input keyword.

*NRV* sheet
.................................................

The "NRV" sheet shall contain the following columns:

Variable Name
  Name of the zVariable
Index
  Index of the current NR row
Value
  Value of the current NR row

Command line interface
''''''''''''''''''''''''''''''''''''''''''''''''''''

To display the help of the module, enter:

::

  xlsx2skt --help

The full calling sequence is:

::

  xlsx2skt [-h] [-O] [-V] [-Q] [-A] [-I] [-s [skeleton]] xlsx_file

Input keyword list:

-h, -help                 Display the module help
-s, --skeleton  skeleton
          Name of the output skeleton table in ASCII format.
          If not provided, use the name of the input file replacing the extension by '.skt'.
-o, --output_dir  Path of the output directory. If not provided, use the directory of the input file.
-A, --Auto_pad        If provided, the module will automatically set the pad values
          (i.e, \!VAR_PADVALUE) for each CDF variable
-I, --Ignore_none   If provided, the module will skip rows
          for which the Attribute/Variable name columns are empty.
          By default, the module returns an error if a empty Attribute/Variable name value is encountered.
-O, --Overwrite       Overwrite existing output ASCII skeleton table
-V, --Verbose         Talkative mode

Example
''''''''''''''''''''''''''''''''''''''''''''''''''''

To test the cdfconverter program, use the dedicated scripts/test_cdfconverter.sh bash script.

Limitations & Known Issues
''''''''''''''''''''''''''''''''''''''''''''''''''''

Here are some identified limitations to the module uses:

  - Values provided in the "Options" sheet is valid for all of CDF file and variables. The module does not allow to set (yet) the values for each variable individually. **THUS, WE STRONGLY RECOMMEND TO USE THE --Auto_pad INPUT KEYWORD (then edit the resulting skeleton table to modify the !VAR_PADVALUE if required).**


The *Skt2cdf* class
````````````````````````````

To import the Skt2cdf class from Python, enter:

.. code-block:: python

  from maser.cdf.cdfconverter import Skt2cdf

Command line interface
''''''''''''''''''''''''''''''''''''''''''''''''''''

To display the help of the module, enter:

::

  skt2cdf --help

The full calling sequence is:

::

  skt2cdf [-h] [-O] [-V] [-Q] [-s [executable]] [-c [output_cdf]] skeleton

Input keyword list:

  -h, -help             Display the module help
  -c, --cdf  output_cdf Name of the output CDF master binary file.
              If not provided, use the name of the input file replacing the extension by '.cdf'.
  -o, --output_dir          Path of the output directory. If not provided, use the directory of the input file.
  -s, --skeletoncdf executable
              Path of the NASA GSFC CDF "skeletoncdf" executable.
              If not provided, the program will search for the
              executable in the $PATH env. variable.
  -O, --Overwrite         Overwrite existing output ASCII skeleton table
  -V, --Verbose           Talkative mode
  -Q, --Quiet                 Quiet mode


Example
'''''''''''''''''''''''''''''''''''''''''''''''''

To test the cdfconverter program, use the dedicated scripts/test_cdfconverter.sh bash script.


The *cdfvalidator* submodule
-------------------------------------------

The *cdfvalidator* submodule provides tools to validate a CDF format file.

It contains only one *Validate* class that regroups all of the validation methods.


The *Validate* class
```````````````````````````````

To import the *Validate* class from Python, enter:

.. code-block:: python

  from maser.cdf.cdfvalidator import Validate

The Model validation test
''''''''''''''''''''''''''''''''''''''''''''''''''''

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
''''''''''''''''''''''''''''''''''''''''''''''''''''

To display the help of the module, enter:

::

  cdfvalidator --help

The full calling sequence is:

::

  cdfvalidator [--help] [--Verbose] [--Quiet] [--log_file [log_file]] \
  [--ISTP] [--CDFValidate [executable]] [--model_file [model_file]] skeleton

Input keyword list:

-h, -help       Display the module help
-l, --log_file      Path of the output log file.
-I, --ISTP          Perform the ISTP compliance validation test
-m, --model_file        Path to the input model file in JSON format
                  (see "Model validation test" section for more information).
-C, --CDFValidate executable       Path of the NASA GSFC CDF "CDFValidate" executable.
                               If it is not provided, the module will
                               search in the directories defined in %%$PATH%%.
-Q, --Quiet         Quiet mode
-V, --Verbose     Talkative mode

Example
'''''''''''''''''''''''''''''''''''''''''''''''''

To test the cdfvalidator program, use the dedicated scripts/test_cdfvalidator.sh bash script.

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

