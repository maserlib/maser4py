#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to create generic Classes for Data and data files handling
"""

import os
import math
import datetime
import dateutil.parser
from astropy.io import fits
import subprocess

__author__ = "Baptiste Cecconi"
__institute__ = "LESIA, Observatoire de Paris, PSL Research University, CNRS."
__date__ = "26-JUL-2017"
__version__ = "0.10"
__project__ = "MASER"

__all__ = ["MaserError", "MaserData", "MaserDataFromFile", "MaserDataFromInterval", "MaserDataRecord",
           "MaserDataSweep", "MaserDataFromFileCDF"]

# defining local library paths

# Path to bin directory of IGPP/PDS/CDF library: http://release.igpp.ucla.edu/pds/cdf/
_pdscdf_bin = '/Users/baptiste/Projets/VOParis/igpp-git/pds-cdf-1.0.11/bin/'

# Path to bin directory of CDF C library: https://spdf.sci.gsfc.nasa.gov/pub/software/cdf/dist/cdf36_4/
_libcdf_bin = '/Applications/cdf/cdf/bin/'

# Path to bin directory of IGPP/Docgen library: http://release.igpp.ucla.edu/igpp/docgen/index.html
_docgen_bin = '/Users/baptiste/Projets/VOParis/igpp/docgen/bin/'

# local directory path
_local_path = os.path.dirname(__file__)


class MaserError(Exception):
    """
    Placeholder class for handling exceptions in the maser.data packages and modules.
    """
    pass


class MaserData(object):
    """
    Basic MaserData class with minimal methods.

    :ivar start_time: a datetime.datetime object (or None is not applicable) providing the start time of the data.
    :ivar end_time: a datetime.datetime object (or None is not applicable) providing the end time of the data.
    :ivar dataset_name: a string (or None is not applicable) providing the dataset name.

    :param verbose: (bool) set to False to remove verbose output (default to True)
    :param debug: (bool) set to True to have debug output (default to False)
    """

    def __init__(self, verbose=True, debug=False):
        self.verbose = verbose
        self.debug = debug
        self.start_time = None
        self.end_time = None
        self.dataset_name = None

    @staticmethod
    def _lib_path() -> dict:
        """
        Loads the paths of the useful local libraries. First tries to load from environment variable, then uses the paths
        defined in this module
        :return: lib_path
        """

        lib_path = dict()
        lib_path['pdscdf_bin'] = os.environ.get('PDSCDF_BIN', _pdscdf_bin)
        lib_path['libcdf_bin'] = os.environ.get('CDF_BIN', _libcdf_bin)
        lib_path['docgen_bin'] = os.environ.get('DOCGEN_BIN', _docgen_bin)

        return lib_path

    def get_epncore_meta(self):
        """
        Method to get EPNcore metadata from the MaserData object instance. This method is extended in classes inheriting
        from MaserData.
        :return md: a dict with time_min, time_max and granule_gid (from dataset_name attribute) keys.
        """
        md = dict()
        md['time_min'] = self.start_time
        md['time_max'] = self.end_time
        md['granule_gid'] = self.dataset_name
        return md

    def get_istp_meta(self):
        """
        Method to get ISTP metadata from the MaserData object instance. This method is extended in classes inheriting
        from MaserData.
        :return: a dict with a projet key set to "MASER"
        """
        md = dict()
        md['project'] = ['MASER']
        return md

    def get_pds4_meta(self):
        """
        Placeholder class to get PDS4 metadata from the MaserData object instance. This method is extended in classes
        inheriting from MaserData.
        :return:
        """
        pass

    def build_edr_data(self, start_time=None, end_time=None):
        """
        TBD
        :param start_time:
        :param end_time:
        :return:
        """
        if start_time is None:
            start_time = self.start_time
        if end_time is None:
            end_time = self.end_time

        var = {'header': {}, 'time': [], 'data': {}}
        return var, start_time, end_time


class MaserDataFromInterval(MaserData):
    """
    MaserDataFromInterval class for MaserData objects built from an interval and a dataset

    :ivar start_time: a datetime.datetime object (or None is not applicable) providing the start time of the data.
    :ivar end_time: a datetime.datetime object (or None is not applicable) providing the end time of the data.
    :ivar dataset_name: a string (or None is not applicable) providing the dataset name.

    :param start_time: start date-time (either ISO formatted or datetime.datetime object)
    :param end_time: end date-time (either ISO formatted or datetime.datetime object)
    :param dataset: (string) dataset name
    :param verbose: (bool) set to False to remove verbose output (default to True)
    :param debug: (bool) set to True to have debug output (default to False)
    """

    def __init__(self, start_time, end_time, dataset='', verbose=True, debug=False):
        """
        Method to instantiate a MaserDataFromInterval object.
        """
        MaserData.__init__(self, verbose, debug)
        self.start_time = self.parse_time(start_time)
        self.end_time = self.parse_time(end_time)
        self.dataset_name = dataset

    @staticmethod
    def parse_time(input_time):
        """
        Method to parse an input time
        :param input_time: date-time (either ISO formatted or datetime.datetime object)
        :returns dt: datetime.datetime object
        """

        if isinstance(input_time, datetime.datetime):
            dt = input_time
        elif isinstance(input_time, str):
            dt = dateutil.parser.parse(input_time)
        elif input_time is None:
            dt = None
        else:
            raise MaserError("Unable to parse input time ({})".format(input_time))

        return dt


class MaserDataFromFile(MaserData):
    """
    MaserDataFromFile class for MaserData objects built from a file.

    :ivar file: Absolute path of current file
    :ivar format: File format (default in 'bin')

    :param file: input file (including path to file)
    :param verbose: (bool) set to False to remove verbose output (default to True)
    :param debug: (bool) set to True to have debug output (default to False)
    """

    def __init__(self, file, verbose=False, debug=False):
        MaserData.__init__(self, verbose, debug)
        self.file = os.path.abspath(file)
        self.format = 'bin'

    def get_file_name(self):
        """
        Method to get the base name of the current file
        :returns: (string) file name.
        """
        return os.path.basename(self.file)

    def get_file_path(self):
        """
        Method to get the path to the directory containing the current file
        :returns: (string) path to directory
        """
        return os.path.dirname(self.file)

    def get_file_size(self):
        """
        Method to get the current file size in bytes
        :returns: (int) file size.
        """
        return os.path.getsize(self.file)

    def get_mime_type(self):
        """
        Method to get the MIME type of the current file
        :returns: (string) MIME type.
        """
        return 'application/binary'

    def get_str_file_size(self):
        """
        Returns the file size in a nice human format.
        :returns: (string) nicely formatted file size
        """
        size = os.path.getsize(self.file)

        if size == 0:
            return '0B'
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size, 1024)))
        p = math.pow(1024, i)
        s = round(size/p, 2)
        return '{} {}'.format(s, size_name[i])

    def __lt__(self, other):
        return self.get_file_name() < other.get_file_name()

    def __gt__(self, other):
        return self.get_file_name() > other.get_file_name()

    def __eq__(self, other):
        return self.get_file_name() == other.get_file_name()

    def __le__(self, other):
        return self.get_file_name() <= other.get_file_name()

    def __ge__(self, other):
        return self.get_file_name() >= other.get_file_name()

    def __ne__(self, other):
        return self.get_file_name() != other.get_file_name()

    def __len__(self):
        pass

    def get_epncore_meta(self):
        """
        Method to get EPNcore metadata dictionary
        Adds file_name, access_format and access_estsize to the MaserData.get_epn_core method
        :return:
        """
        md = MaserData.get_epncore_meta(self)
        md['file_name'] = self.get_file_name()
        md['access_format'] = self.get_mime_type()
        md['access_estsize'] = self.get_file_size()/1024
        return md

    def get_single_sweep(self, index=0, **kwargs):
        """
        Placeholder method to retrieve a single data sweep.
        :param index: index number of the sweep to be retreived. Default=0
        :param kwargs: Any arguments that shall be passed to the method.
        :return:
        """
        pass

    def sweeps(self, **kwargs):
        """
        Placeholder method to retrieve a list of all sweeps for the data object.
        :param kwargs:  Any arguments that shall be passed to the method.
        :returns: a list of all sweep objects in the data object.
        """
        return (self.get_single_sweep(cur_sweep_id, **kwargs) for cur_sweep_id in range(len(self)))


class MaserDataFromFileCDF(MaserDataFromFile):
    """
    This class inherits from the MaserDataFromFile class, and is used for CDF file types.

    :ivar format: this attribute is set to 'cdf'
    """
    def __init__(self, file, verbose=True, debug=False):

        MaserDataFromFile.__init__(self, file, verbose, debug)
        self.format = 'CDF'

    def validate_pds(self):
        """
        This method calls the PDS-CDF validator provided by NASA/PDS/PPI (UCLA/IGPP group).
        The validate script is available at: http://release.igpp.ucla.edu/pds/cdf/
        :return:
        """
        if self.verbose:
            print("### [Check PDS-CDF compliance]")
            verb_arg = '-v'
        else:
            verb_arg = ''

        shell_command = "{}cdfcheck {} {}".format(_pdscdf_bin, verb_arg, self.file)

        if self.verbose:
            print(shell_command)

        os.system(shell_command)

    def fix_cdf(self):
        """
        This method is used to fix CDF internal structure if needed. It is running the cdfconvert command of the CDF-C
        library from NASA/GSFC.
        """
        if self.verbose:
            print("### [Fix CDF --- cdfconvert to self]")

        shell_command = "{0}cdfconvert {1} /tmp/cdfconvert_tmp.cdf; " \
                        "mv /tmp/cdfconvert_tmp.cdf {1}".format(_libcdf_bin, self.file)

        if self.verbose:
            print(shell_command)

        os.system(shell_command)

    def get_mime_type(self):
        """
        The method returns the MIME type of the data object (here: 'application/x-cdf').
        """
        return 'application/x-cdf'

    def build_pds4_label(self):
        """
        This method builds a CDF PDS4 label for the current CDF file.
        """
        java_process_list = ['java', '-jar', "{}jar/igpp.docgen.jar".format(_docgen_bin),
                             '-t {}'.format(os.path.join(_local_path, 'templates')),
                             'cdf:{}'.format(self.file), 'maser_cdf_pds4_label_template.vm']
        subprocess.call(java_process_list)


class MaserDataFromFileFITS(MaserDataFromFile):
    """
    This class inherits from the MaserDataFromFile class, and is used for CDF file types.

    :ivar format: this attribute is set to 'fits'
    """

    def __init__(self, file, verbose=True, debug=False):
        MaserDataFromFile.__init__(file, verbose, debug)
        self.format = 'FITS'

    def get_mime_type(self):
        """
        The method returns the MIME type of the data object (here: 'application/fits').
        """
        return 'application/fits'


class MaserDataFromFileText(MaserDataFromFile):
    """
    This class inherits from the MaserDataFromFile class, and is used for CDF file types.

    :ivar format: this attribute is set to 'TXT'
    """

    def __init__(self, file, verbose=True, debug=False):

        MaserDataFromFile.__init__(file, verbose, debug)
        self.format = 'TXT'

    def get_mime_type(self):
        """
        The method returns the MIME type of the data object (here: 'text/plain').
        """
        return 'text/plain'


class MaserDataFromFileCSV(MaserDataFromFile):
    """
    This class inherits from the MaserDataFromFile class, and is used for CDF file types.

    :ivar format: this attribute is set to 'CSV'
    """

    def __init__(self, file, verbose=True, debug=False):

        MaserDataFromFile.__init__(file, verbose, debug)
        self.format = 'CSV'

    def get_mime_type(self):
        """
        The method returns the MIME type of the data object (here: 'text/csv').
        """
        return 'text/csv'


class MaserDataRecord(object):
    """
    Placeholder class for MaserData records.

    :ivar parent: parent MaserData object
    :ivar data: dict with data record content.
    """

    def __init__(self, parent, raw_data):
        self.parent = parent
        self.data = self.load_data(raw_data)

    def load_data(self, raw_data):
        """
        Placeholder method to be overridden by subclass methods
        :returns: empty header and data dict()
        """
        return dict()

    def __getitem__(self, key):
        """
        Overrides generic __getitem__ and looks into self.data content
        :param key: key
        :return: value
        """
        if key in self.data.keys():
            return self.data[key]
        else:
            raise MaserError("Key {} doesn't exist".format(key))

    def get_datetime(self) -> datetime.datetime:
        """
        Method to retrieve the epoch of the record
        :return: datetime.datetime object
        """
        pass


class MaserDataSweep(MaserData):
    """
    Placeholder class for MaserData sweeps.

    :ivar parent: parent MaserData object
    :ivar data: dict with sweep data content.
    :ivar header: dict with sweep header content
    """

    def __init__(self, parent, index, verbose=False, debug=False):
        MaserData.__init__(self)
        self.parent = parent
        self.data = None
        self.header = None

        if isinstance(index, int):
            self.index = index
        else:
            raise MaserError("Unable to process provided index value... Aborting")

    def get_datetime(self):
        """
        Method to get the datetime of the current sweep (or start of sweep).
        :return: datetime.datetime object
        """
        pass
