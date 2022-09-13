# -*- coding: utf-8 -*-

import numpy
from typing import Union


class RecordsOnly:
    _access_modes = ["records", "file"]

    @property
    def sweeps(self):
        raise ValueError("Illegal access mode.")


class FixedFrequencies:
    pass


class VariableFrequencies:
    def __init__(self):
        self.fixed_frequencies = False
        self._sweep_masks = None
        self._sweep_mode_masks = None
        self.__frequencies = None
        self.__max_sweep_length = None

    @property
    def sweep_masks(self) -> Union[list, None]:
        return None

    @property
    def sweep_mode_masks(self) -> Union[list, None]:
        return None

    @property
    def _max_sweep_length(self):
        if self.__max_sweep_length is None:
            self.__max_sweep_length = numpy.max([len(f) for f in self.frequencies])
        return self.__max_sweep_length

    def as_xarray(self):
        import xarray

        fields = self.fields
        units = self.units

        freq_arr = numpy.full((self._nsweep, self._max_sweep_length), numpy.nan)
        for i in range(self._nsweep):
            f = self.frequencies[i].value
            freq_arr[i, : len(f)] = f
            freq_arr[i, len(f) :] = f[-1]

        freq_index = range(self._max_sweep_length)

        datasets = {}
        for dataset_key, dataset_unit in zip(fields, units):
            data_arr = numpy.full((self._nsweep, self._max_sweep_length), numpy.nan)
            for i, sweep in enumerate(self.sweeps):
                d = sweep.data[dataset_key]
                data_arr[i, : len(d)] = d

            datasets[dataset_key] = xarray.DataArray(
                data=data_arr,
                name=dataset_key,
                coords={
                    "freq_index": freq_index,
                    "time": self.times.to_datetime(),
                    "frequency": (["time", "freq_index"], freq_arr, {"units": "kHz"}),
                },
                attrs={"units": dataset_unit},
                dims=("time", "freq_index"),
            )

        return datasets
