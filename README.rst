-------------------------------------
 Maser python module
 -------------------------------------

 The maser Python module

 TBW







 X.Bonnin (LESIA, CNRS), 10-NOV-2015

 Introduction
  ----------------

    The xlsx2skt program allows users to generate a CDF skeleton table in ASCII format
    from a Excel 2007 format file.
    For more information about the CDF format, please visit http://cdf.gsfc.nasa.gov/.


 System requirements
 ------------------------------

    xlsx2skt requires Python 3.2 or higher with the following modules:
        - openpyxl 2.2.0 or higher

    The program has been tested on the following Operating Systems:
        - Mac OS X 10.10, 10.11
        - Debian Jessie 8.2

 Excel file format definition
 ------------------------------------

    xlsx2skt supports the Excel 2007 format only (i.e., .xlsx).

    Note: the xlsx2skt parser is case sensitive!

    The Excel file shall contain the following sheets:

        - header
        - GLOBALattributes
        - zVariables
        - VARIABLEattributes
        - Options
        - NRV

    The first row of each sheet shall be used to provide the name of the columns.

    * header

        The "header" sheet shall contain the following columns:

            - CDF_NAME
            - DATA ENCODING
            - MAJORITY
            - FORMAT

    * GLOBALattributes

        The "GLOBALattributes" sheet shall contain the following columns:

            - Attribute Name
            - Entry Number
            - Data Type
            - Value

    * zVariables

        The "zVariables" sheet shall contain the following columns:

            - Variable Name
            - Data Type
            - Number Elements
            - Dims
            - Sizes
            - Record Variance
            - Dimension Variances

    * VARIABLEattributes

        The "VARIABLEattributes" sheet shall contain the following columns:

            - Variable Name
            - Attribute Name
            - Data Type
            - Value

    * Options

        The "Options" sheet shall contain the following columns:

            - CDF_COMPRESSION
            - CDF_CHECKSUM
            - VAR_COMPRESSION
            - VAR_SPARSERECORDS
            - VAR_PADVALUE

    * NRV

        The "NRV" sheet shall contain the following columns:

            - Variable Name
            - Index
            - Value

    An example of xlsx2skt use case is presend in the "Use case" section.

 Calling sequence
 -------------------------

    * To display the help of the module, enter:
        >python3 xlsx2skt.py --help

        (We assume here that python 3.x can be called using the "python3" alias.)

    * The full calling sequence is:
        >python3 xlsx2skt.py [--version] [--change] [--help] [--0verwrite] [--Verbose] [--Auto_pad] [--Ignore_none] [-c [skeletoncdf]] xlsx_file skt_file

    * Input keyword list:
        -h, -help               : Display the module help
        -O, --Overwrite    : Overwrite existing output ASCII skeleton table.
        -V, --Verbose      : Talkative mode
        -A, --Auto_pad    : If provided, the module will automatically set the pad values (i.e, !VAR_PADVALUE) for each CDF variable
        -I, --Ignore_none : If provided, the module will skip rows for which the Attribute/Variable name columns are empty.
                                    By default, the module returns an error if a empty Attribute/Variable name value is encountered.
        -c [skeletoncdf]   : Path of the NASA GSFC CDF "skeletoncdf" executable.
                                        If provided, the module will also build the CDF binary file
                                        from the skeleton table calling "skeletoncdf".
                                        (Visit http://cdf.gsfc.nasa.gov/. for more details about the
                                        skeletoncdf program).
        --version               : Show version
        --change               : Show change

 Example
 -------------

    To test the xlsx2skt program, enter:
        >python3 xlsx2skt.py --Verbose --Overwrite --Auto_pad --Ignore_none xlsx2skt_example.xlsx xlsx2skt_example.skt

    Be sure that the xlsx2skt_example.xlsx file is present in the current directory.

    It should generate the output skeleton table "xlsx2skt_example.skt" in the current directory.


 Limitations & Known Issues
 ---------------------------------------

 Here are some identified limitations to the module uses:
    - Values provided in the "Options" sheet is valid for all of CDF
    file and variables. The module does not allow to set (yet) the values
    for each variable individually.
    THUS, WE STRONGLY RECOMMEND TO USE THE AUTO_PAD KEYWORD
    (then edit the resulting skeleton table to modify the !VAR_PADVALUE if required).



