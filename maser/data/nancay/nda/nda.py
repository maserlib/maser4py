#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to define classes for the Nancay Decameter Array (NDA) datasets at Obs-Nancay.
@author: B.Cecconi(LESIA)
"""

import datetime

__author__ = "Baptiste Cecconi"
__institute__ = "LESIA, Observatoire de Paris, PSL Research University, CNRS."
__date__ = "25-JUL-2017"
__version__ = "0.10"
__project__ = "MASER/SRN/NDA"

__all__ = ["NDAData"]

class NDAData:

    def __init__(self, file, header, data, name):
        self.header = header
        self.data = data
        self.file = file
        self.name = name

    def __len__(self):
        return len(self.data)
