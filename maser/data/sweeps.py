# -*- coding: utf-8 -*-
from maser.data.sweep import Sweep


class Sweeps:
    def __iter__(self):
        self.__call__(load_data=True)

    def __call__(self, *args, **kwargs):
        yield Sweep(*args, **kwargs)
