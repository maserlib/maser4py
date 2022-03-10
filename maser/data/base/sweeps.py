# -*- coding: utf-8 -*-


class Sweeps:
    def __init__(self, file, load_data: bool = True):
        self.file = file
        self.load_data = load_data

    def __iter__(self):
        for d in self.generator:
            yield d

    def __call__(self, load_data: bool = None, *args, **kwargs):
        if load_data is not None:
            self.load_data = load_data
        return self.generator

    @property
    def generator(self):
        for d in self.file:
            yield d

    def __next__(self):
        next(self.generator)
