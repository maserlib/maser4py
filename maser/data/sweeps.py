# -*- coding: utf-8 -*-
from maser.data.sweep import Sweep


class Sweeps:
    def __iter__(self):
        self.__call__(load_data=True)

    def __call__(self, load_data: bool = False, *args, **kwargs):
        yield Sweep()
