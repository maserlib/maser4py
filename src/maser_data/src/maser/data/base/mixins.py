# -*- coding: utf-8 -*-

import numpy
from typing import Union


class RecordsOnly:
    _access_modes = ["records", "file"]

    @property
    def sweeps(self):
        raise ValueError("Illegal access mode.")


class FixedFrequencies:
    """This mixin class defines the attributes, properties and methods for datasets
    with fixed spectral sampling.
    """

    def __init__(self):
        self.fixed_frequencies = True


class VariableFrequencies:
    """This mixin class defines the attributes, properties and methods for datasets
    with variable spectral sampling.
    """

    def __init__(self):
        self.fixed_frequencies = False
        self._sweep_masks = None
        self._sweep_mode_masks = None
        self._frequencies_ = None
        self._max_sweep_length = None

    @property
    def sweep_masks(self) -> Union[list, None]:
        """This property contains a list numpy.ma (masked arrays). Each item of
        the list corresponds to a sweep. Each mask has to be applied onto
        the self._data attribute.

        :return: list of sweep masks
        """
        return None

    @property
    def sweep_mode_masks(self) -> Union[list, None]:
        """This property contains a list of numpy.ma (masked arrays). Each item of
        the list corresponds to a sweeping mode. Each mask has to be applied onto
        the self.sweep_masks property.

        :return: list of sweep mode masks
        """
        return None

    @property
    def max_sweep_length(self):
        if self._max_sweep_length is None:
            self._max_sweep_length = numpy.max([len(f) for f in self.frequencies])
        return self._max_sweep_length

    def as_xarray(self):
        import xarray

        fields = self.fields
        units = self.units

        freq_arr = numpy.full((self._nsweep, self.max_sweep_length), numpy.nan)
        for i in range(self._nsweep):
            f = self.frequencies[i].value
            freq_arr[i, : len(f)] = f
            freq_arr[i, len(f) :] = f[-1]

        freq_index = range(self.max_sweep_length)

        datasets = {}
        for dataset_key, dataset_unit in zip(fields, units):
            data_arr = numpy.full((self._nsweep, self.max_sweep_length), numpy.nan)
            for i, sweep in enumerate(self.sweeps):
                d = sweep.data[dataset_key]
                data_arr[i, : len(d)] = d

            datasets[dataset_key] = xarray.DataArray(
                data=data_arr.T,
                name=dataset_key,
                coords={
                    "freq_index": freq_index,
                    "time": self.times.to_datetime(),
                    "frequency": (["time", "freq_index"], freq_arr, {"units": "kHz"}),
                },
                attrs={"units": dataset_unit},
                dims=("freq_index", "time"),
            )

        return xarray.Dataset(data_vars=datasets)
