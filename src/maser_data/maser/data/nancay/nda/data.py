# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from maser.data.base import FitsData
from .sweeps import SrnNdaRoutineEdrSweeps, SrnNdaNewRoutineEdrSweeps

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


class SrnNdaNewRoutineEdrFitsData(FitsData, dataset="orn_nda_newroutine_edr"):
    """ORN NDA NewRoutine dataset"""

    _iter_sweep_class = SrnNdaNewRoutineEdrSweeps

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as f:
                self._frequencies = f[1].data[0][0] * Unit(f[1].header["TUNIT1"])
        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as f:
                self._times = Time(f[2].data["jd"], format="jd")
        return self._times

    def as_xarray(self):
        import xarray

        dataset_keys = [self.file[0].header[f"CHANNEL{i+1}"] for i in range(4)]
        datasets = {}

        for i, dataset_key in enumerate(dataset_keys):
            datasets[dataset_key] = xarray.DataArray(
                data=self.file[2].data["DATA"][:, :, i].T,
                name=dataset_key,
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
                    "unit": Unit("V**2/Hz"),
                    "title": f"{self.file[0].header['TITLE']} {dataset_key}",
                },
            )
        return datasets


class SrnNdaNewRoutineSunEdrFitsData(
    SrnNdaNewRoutineEdrFitsData, dataset="orn_nda_newroutine_sun_edr"
):
    """ORN NDA NewRoutine Sun dataset"""

    pass


class SrnNdaNewRoutineJupEdrFitsData(
    SrnNdaNewRoutineEdrFitsData, dataset="orn_nda_newroutine_jup_edr"
):
    """ORN NDA NewRoutine Jupiter dataset"""

    pass


class SrnNdaNewRoutineTransitEdrFitsData(
    SrnNdaNewRoutineEdrFitsData, dataset="orn_nda_newroutine_transit_edr"
):
    """ORN NDA NewRoutine Radio Source Transit dataset"""

    pass
