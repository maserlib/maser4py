#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to create a generic Class for Data and data files handling
"""

import os
import math

__author__ = "Baptiste Cecconi"
__institute__ = "LESIA, Observatoire de Paris, PSL Research University, CNRS."
__date__ = "26-JUL-2017"
__version__ = "0.10"
__project__ = "MASER"

__all__ = ["MaserError", "MaserDataFromFile"]

pds_bin = '/Users/baptiste/Projets/VOParis/igpp-git/pds-cdf-1.0.11/bin/'
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

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.dataset_name = ''


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
        :returns: (MaserData) object built from the input file.
        """

        MaserData.__init__(self)
        self.file = os.path.abspath(file)
        self.verbose = verbose
        self.debug = debug
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