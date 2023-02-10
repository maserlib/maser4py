# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from maser.data.base import FitsData
from .sweeps import SrnNdaRoutineEdrSweeps

from astropy.time import Time
from astropy.units import Unit


class SrnNdaRoutineEdrCdfData(CdfData, dataset="srn_nda_routine_edr"):
    """ORN NDA Routine Jupiter dataset"""

    _iter_sweep_class = SrnNdaRoutineEdrSweeps

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


class SrnNdaRoutineJupEdrCdfData(
    SrnNdaRoutineEdrCdfData, dataset="srn_nda_routine_jup_edr"
):
    """ORN NDA Routine Jupiter dataset"""

    pass


class SrnNdaRoutineSunEdrCdfData(
    SrnNdaRoutineEdrCdfData, dataset="srn_nda_routine_sun_edr"
):
    """ORN NDA Routine Sun dataset"""

    pass


class SrnNdaNewRoutineEdrCdfData(FitsData, dataset="orn_nda_newroutine_edr"):
    """ORN NDA NewRoutine dataset"""

    pass


class SrnNdaNewRoutineSunEdrCdfData(
    SrnNdaNewRoutineEdrCdfData, dataset="orn_nda_newroutine_sun_edr"
):
    """ORN NDA NewRoutine Sun dataset"""

    pass


class SrnNdaNewRoutineJupEdrCdfData(
    SrnNdaNewRoutineEdrCdfData, dataset="orn_nda_newroutine_jup_edr"
):
    """ORN NDA NewRoutine Jupiter dataset"""

    pass


class SrnNdaNewRoutineTransitEdrCdfData(
    SrnNdaNewRoutineEdrCdfData, dataset="orn_nda_newroutine_transit_edr"
):
    """ORN NDA NewRoutine Radio Source Transit dataset"""

    pass
