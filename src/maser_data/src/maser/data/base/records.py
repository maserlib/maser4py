# -*- coding: utf-8 -*-
class Record:
    def __init__(self, header, data):
        self.header = header
        self.data = data
        self._time = None

    @property
    def time(self):
        return self._time


class Records:
    def __init__(self, *, data_instance):
        """_summary_

        Args:
            data_instance (maser.data.Data): a reference to the parent data object
        """
        self.data_reference = data_instance

    def __iter__(self):
        for d in self.generator:
            yield d

    def __call__(self, load_data: bool = None, *args, **kwargs):
        return self.generator

    @property
    def load_data(self):
        return self.data_reference.load_data

    @property
    def file(self):
        return self.data_reference.file

    @property
    def generator(self):
        for d in self.file:
            yield d

    def __next__(self):
        next(self.generator)
