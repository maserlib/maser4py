#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to create a generic Class for Data and data files handling
"""

import os

__author__ = "Baptiste Cecconi"
__institute__ = "LESIA, Observatoire de Paris, PSL Research University, CNRS."
__date__ = "26-JUL-2017"
__version__ = "0.10"
__project__ = "MASER"

__all__ = ["MaserData"]


class MaserData:

    def __init__(self, file):
        self.file = os.path.abspath(file)

    def file_name(self):
        return os.path.basename(self.file)

    def file_path(self):
        return os.path.dirname(self.file)

    def file_size(self):
        return os.path.getsize(self.file)

