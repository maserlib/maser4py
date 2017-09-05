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

__all__ = ["MaserData"]

pds_bin = '/Users/baptiste/Projets/VOParis/igpp-git/pds-cdf-1.0.11/bin/'
cdf_bin = '/Applications/cdf/cdf/bin/'


class MaserData:

    def __init__(self, file, verbose=True, debug=False):
        self.file = os.path.abspath(file)
        self.verbose = verbose
        self.debug = debug
        self.format = ''
        self.dataset = ''

    def get_file_name(self):
        return os.path.basename(self.file)

    def get_file_path(self):
        return os.path.dirname(self.file)

    def get_file_size(self):
        return os.path.getsize(self.file)

    def get_mime_type(self):
        return 'application/binary'

    def get_str_file_size(self):
        """
        Returns the file size in a nice human format.
        :return:
        """
        size = os.path.getsize(self.file)

        if size == 0:
            return '0B'
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size, 1024)))
        p = math.pow(1024, i)
        s = round(size/p, 2)
        return '{} {}'.format(s, size_name[i])


class MaserCDFData(MaserData):

    def __init__(self, file, verbose=True, debug=False):

        MaserData.__init__(file, verbose, debug)
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