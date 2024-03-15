# -*- coding: utf-8 -*-

"""Classes for e-Callisto datasets"""

from maser.data.base import FitsData

from typing import Union, List
from pathlib import Path
from astropy.time import Time
from astropy.units import Unit


class ECallistoFitsData(FitsData, dataset="ecallisto"):
    """Class for `ecallisto` FITS files."""

    _dataset_keys = ["Flux Density"]

    @property
    def times(self):
        if self._times is None:
            self._times = Time([], format="jd")
            with self.open(self.filepath) as f:
                self._times = f[1].data["TIME"][0] * Unit("s") + Time(
                    f"{f[0].header['DATE-OBS'].replace('/', '-')} {f[0].header['TIME-OBS']}"
                )
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as f:
                self._frequencies = f[1].data["FREQUENCY"][0] * Unit("MHz")
        return self._frequencies

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def as_xarray(self):
        import xarray

        dataset = {}
        dataset["Flux Density"] = xarray.DataArray(
            data=self.file[0].data,
            name="Flux Density",
            coords=[
                ("frequency", self.frequencies.value, {"units": self.frequencies.unit}),
                ("time", self.times.to_datetime()),
            ],
            dims=("frequency", "time"),
            attrs={
                "units": "digits",
                "title": self.file[0].header["CONTENT"],
                "instrument": self.file[0].header["INSTRUME"].strip(),
                "target": self.file[0].header["OBJECT"].strip(),
            },
        )
        return xarray.Dataset(data_vars=dataset)

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["Flux Density"],
        **kwargs,
    ):
        self._quicklook(
            keys=keys,
            file_png=file_png,
            **kwargs,
        )
