# -*- coding: utf-8 -*-

"""Classes for Sorbet datasets"""

from maser.data.base import CdfData

from typing import Union
from pathlib import Path
from astropy.time import Time
from astropy.units import Unit


class SorbetCdfData(CdfData, dataset="sorbet"):
    """Class for `sorbet` CDF files."""

    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as f:
                self._times = Time(f["Epoch"][...])
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as f:
                self._frequencies = f["Frequency"][...] * Unit(
                    f["Frequency"].attrs["UNITS"]
                )
        return self._frequencies

    def as_xarray(self):
        import xarray

        dataset_keys = ["DBSC", " "]
        datasets = {}

        for dataset_key in dataset_keys:
            datasets[dataset_key] = xarray.DataArray(
                data=self.file[dataset_key][...].T,
                name=self.file[dataset_key].attrs["LABLAXIS"],
                coords=[
                    (
                        "frequency",
                        self.frequencies.value,
                        {"units": self.frequencies.unit},
                    ),
                    ("time", self.times.to_datetime()),
                ],
                dims=("frequency", "time"),
                attrs={
                    "units": self.file[dataset_key].attrs["UNITS"],
                    "title": self.file[dataset_key].attrs["CATDESC"],
                },
            )
        return xarray.Dataset(data_vars=datasets)

    def quicklook(self, file_png: Union[str, Path, None] = None):
        self._quicklook(
            keys=["DBSC", " "],
            file_png=file_png,
        )
