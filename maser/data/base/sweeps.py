# -*- coding: utf-8 -*-
from .records import Records, Record


class Sweep(Record):
    @property
    def frequencies(self):
        pass


class Sweeps(Records):
    pass
