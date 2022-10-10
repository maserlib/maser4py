# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from .sweeps import SrnNdaRoutineJupEdrSweeps

from astropy.time import Time
from astropy.units import Unit


class SrnNdaRoutineJupEdrCdfData(CdfData, dataset="srn_nda_routine_jup_edr"):
    """ORN NDA Routine Jupiter dataset"""

    _iter_sweep_class = SrnNdaRoutineJupEdrSweeps

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as f:
                self._frequencies = f["Frequency"][...] * Unit(
                    f["Frequency"].attrs["UNITS"]
                )
        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as f:
                self._times = Time(f["Epoch"][...])
        return self._times

    def as_xarray(self):
        import xarray

        dataset_keys = ["LL", "RR"]
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
                    "unit": self.file[dataset_key].attrs["UNITS"],
                    "title": self.file[dataset_key].attrs["CATDESC"],
                },
            )
        return datasets
