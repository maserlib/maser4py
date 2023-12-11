# -*- coding: utf-8 -*-
from maser.data.base import CdfData  # BinData, Sweeps
from astropy.units import Unit
from astropy.time import Time
from typing import List

from .hfr import RpwHfrSurv  # noqa: F401
from .tnr import RpwTnrSurv  # noqa: F401
from .lfr import RpwLfrSurvBp1  # noqa: F401


class RpwHfrL3Cdf(CdfData, dataset="solo_L3_rpw-hfr-flux_"):
    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as cdf_file:
                units = cdf_file["FREQUENCY"].attrs["UNITS"]
                freq = cdf_file["FREQUENCY"][...] * Unit(units)
                self._frequencies = freq
        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            self._times = Time([], format="jd")
            with self.open(self.filepath) as cdf_file:
                self._times = Time(cdf_file["Epoch"][...])
        return self._times

    def as_xarray(self):
        import xarray

        dataset_keys = {"PSD_V2", "PSD_FLUX", "PSD_SFU", "SC_POS_HCI"}

        data_vars = {}
        for key in dataset_keys:
            data_vars[key] = (
                ["frequency", "time"],
                self.file[key][...].T,
                {
                    "units": self.file[key].attrs["UNITS"],
                },
            )

        datasets = xarray.Dataset(
            data_vars=data_vars,
            coords={
                "frequency": (
                    ["frequency"],
                    self.frequencies.value,
                    {"units": self.frequencies.unit},
                ),
                "time": self.times.to_datetime(),
            },
        ).sortby("frequency")

        return datasets

    def quicklook(self, file_png=None, keys: List[str] = ["PSD_FLUX"], **kwargs):
        self._quicklook(
            keys=keys,
            file_png=file_png,
            # vmin=[68, 68],
            # vmax=[94, 94],
            db=[True, True],
            **kwargs,
        )


class RpwTnrL3Cdf(CdfData, dataset="solo_L3_rpw-tnr-flux_"):
    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as cdf_file:
                units = cdf_file["FREQUENCY"].attrs["UNITS"]
                freq = cdf_file["FREQUENCY"][...] * Unit(units)
                self._frequencies = freq
        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            self._times = Time([], format="jd")
            with self.open(self.filepath) as cdf_file:
                self._times = Time(cdf_file["Epoch"][...])
        return self._times

    def as_xarray(self):
        import xarray

        dataset_keys = {"PSD_V2", "PSD_FLUX", "PSD_SFU", "SC_POS_HCI"}

        data_vars = {}
        for key in dataset_keys:
            data_vars[key] = (
                ["frequency", "time"],
                self.file[key][...].T,
                {
                    "units": self.file[key].attrs["UNITS"],
                },
            )

        datasets = xarray.Dataset(
            data_vars=data_vars,
            coords={
                "frequency": (
                    ["frequency"],
                    self.frequencies.value,
                    {"units": self.frequencies.unit},
                ),
                "time": self.times.to_datetime(),
            },
        ).sortby("frequency")

        return datasets

    def quicklook(self, file_png=None, keys: List[str] = ["PSD_FLUX"], **kwargs):
        self._quicklook(
            keys=keys,
            file_png=file_png,
            # vmin=[68, 68],
            # vmax=[94, 94],
            db=[True, True],
            **kwargs,
        )
