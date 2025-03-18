# -*- coding: utf-8 -*-

"""
Module to define generic iterator class for sweep-based access.
"""

from .records import Records, Record
import warnings


class Sweep(Record):
    def __init__(self, header, data):
        super().__init__(header, data)
        self._frequencies = None

    @property
    def frequencies(self):
        return self._frequencies


class Sweeps(Records):
    warnings.warn("Sweep format will be changed.", FutureWarning)

    @property
    def generator(self):
        for sweep in self.data_reference._data:
            yield sweep
