# -*- coding: utf-8 -*-
from .records import Records, Record


class Sweep(Record):
    def __init__(self, header, data):
        super().__init__(header, data)
        self._frequencies = None

    @property
    def frequencies(self):
        return self._frequencies


class Sweeps(Records):
    pass
