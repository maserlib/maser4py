#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to create a generic Class for Data and data files handling
"""

import os
import math
import datetime
import dateutil.parser

__author__ = "Baptiste Cecconi"
__institute__ = "LESIA, Observatoire de Paris, PSL Research University, CNRS."
__date__ = "26-JUL-2017"
__version__ = "0.10"
__project__ = "MASER"

__all__ = ["MaserError", "MaserData", "MaserDataFromFile", "MaserDataFromInterval", "MaserDataRecord", "MaserDataSweep"]

pds_bin = '/Users/baptiste/Projets/VOParis/igpp-git/VG1_JUPITER-cdf-1.0.11/bin/'
cdf_bin = '/Applications/cdf/cdf/bin/'


class MaserError(Exception):
    """
    Placeholder class for handling errors
    """
    pass


class MaserData:
    """
    Basic MaserData class with minimal methods
    """

    def __init__(self, verbose=True, debug=False):
        """
        Method to instantiate generic MaserData object.
        :param verbose: (bool) set to False to remove verbose output (default to True)
        :param debug: (bool) set to True to have debug output (default to False)
        """
        self.verbose = verbose
        self.debug = debug
        self.start_time = None
        self.end_time = None
        self.dataset_name = None


class MaserDataFromInterval(MaserData):
    """
    MaserDataFromInterval class for MaserData objects built from an interval and a dataset
    """

    def __init__(self, start_time, end_time, dataset='', verbose=True, debug=False):
        """
        Method to instantiate a MaserDataFromInterval object.
        :param start_time: start date-time (either ISO formatted or datetime.datetime object)
        :param end_time: end date-time (either ISO formatted or datetime.datetime object)
        :param dataset: (string) dataset name
        :param verbose: (bool) set to False to remove verbose output (default to True)
        :param debug: (bool) set to True to have debug output (default to False)
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
        :returns: datetime.datetime object
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
    MaserDataFromFile class for MaserData objects built from a file
    """

    def __init__(self, file, verbose=True, debug=False):
        """
        Method instantiate a MaserData object from a file
        :param file: input file (including path to file)
        :param verbose: (bool) set to False to remove verbose output (default to True)
        :param debug: (bool) set to True to have debug output (default to False)
        """

        MaserData.__init__(self, verbose, debug)
        self.file = os.path.abspath(file)
        self.format = ''

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


class MaserDataFromFileCDF(MaserDataFromFile):

    def __init__(self, file, verbose=True, debug=False):

        MaserDataFromFile.__init__(file, verbose, debug)
        self.format = 'CDF'

    def validate_pds(self):

        if self.verbose:
            print("### [Check PDS-CDF compliance]")
            verb_arg = '-v'
        else:
            verb_arg = ''

        shell_command = "{}cdfcheck {} {}".format(pds_bin, verb_arg, self.file)

        if self.verbose:
            print(shell_command)

        os.system(shell_command)

    def fix_cdf(self):

        if self.verbose:
            print("### [Fix CDF --- cdfconvert to self]")

        shell_command = "{0}cdfconvert {1} /tmp/cdfconvert_tmp.cdf; " \
                        "mv /tmp/cdfconvert_tmp.cdf {1}".format(cdf_bin, self.file)

        if self.verbose:
            print(shell_command)

        os.system(shell_command)

    def get_mime_type(self):
        return 'application/x-cdf'


class MaserDataRecord(object):

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
        pass


class MaserDataSweep(MaserData):

    def __init__(self, parent, index):
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
        return None
