# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from maser.data.base import FitsData
from .sweeps import OrnNdaRoutineEdrSweeps, OrnNdaNewRoutineEdrSweeps

from typing import Union
from pathlib import Path
from astropy.time import Time
from astropy.units import Unit


class OrnNdaRoutineEdrCdfData(CdfData, dataset="orn_nda_routine_edr"):
    """ORN NDA Routine Jupiter dataset"""

    _iter_sweep_class = OrnNdaRoutineEdrSweeps

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
                    "units": self.file[dataset_key].attrs["UNITS"],
                    "title": self.file[dataset_key].attrs["CATDESC"],
                },
            )
        return xarray.Dataset(data_vars=datasets)

    def quicklook(
        self, file_png: Union[str, Path, None] = None, keys: [str] = ["LL", "RR"]
    ):
        self._quicklook(
            keys=keys,
            file_png=file_png,
        )


class OrnNdaRoutineJupEdrCdfData(
    OrnNdaRoutineEdrCdfData, dataset="orn_nda_routine_jup_edr"
):
    """ORN NDA Routine Jupiter dataset"""

    pass


class OrnNdaRoutineSunEdrCdfData(
    OrnNdaRoutineEdrCdfData, dataset="orn_nda_routine_sun_edr"
):
    """ORN NDA Routine Sun dataset"""

    pass


class OrnNdaNewRoutineEdrFitsData(FitsData, dataset="orn_nda_newroutine_edr"):
    """ORN NDA NewRoutine dataset"""

    _iter_sweep_class = OrnNdaNewRoutineEdrSweeps

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        FitsData.__init__(self, filepath, dataset, access_mode)
        self._fields = None

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

    def epncore(self):
        md = FitsData.epncore(self)
        md["granule_uid"] = f"{self.dataset}:{self.filepath.stem}"
        return md

    def as_xarray(self):
        import xarray

        dataset_keys = self.fields
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
                    "units": Unit("V**2/Hz"),
                    "title": f"{self.file[0].header['TITLE']} ({dataset_key} component)",
                },
            )
        return xarray.Dataset(data_vars=datasets)


class OrnNdaNewRoutineSunEdrFitsData(
    OrnNdaNewRoutineEdrFitsData, dataset="orn_nda_newroutine_sun_edr"
):
    """ORN NDA NewRoutine Sun dataset"""

    @property
    def fields(self):
        if self._fields is None:
            self._fields = [self.file[0].header[f"CHANNEL{i+1}"] for i in range(2)]
        return self._fields

    def quicklook(self, file_png=None, keys: [str] = ["LL", "RR"]):
        self._quicklook(
            keys=keys,
            file_png=file_png,
            vmin=[68, 68],
            vmax=[94, 94],
            db=[True, True],
        )


class OrnNdaNewRoutineJupEdrFitsData(
    OrnNdaNewRoutineEdrFitsData, dataset="orn_nda_newroutine_jup_edr"
):
    """ORN NDA NewRoutine Jupiter dataset"""

    @property
    def fields(self):
        if self._fields is None:
            self._fields = [self.file[0].header[f"CHANNEL{i+1}"] for i in range(4)]
        return self._fields

    def quicklook(
        self, file_png: Union[str, Path, None] = None, keys: [str] = ["LL", "RR"]
    ):
        self._quicklook(keys=keys, file_png=file_png, db=[True, True])


class OrnNdaNewRoutineTransitEdrFitsData(
    OrnNdaNewRoutineEdrFitsData, dataset="orn_nda_newroutine_transit_edr"
):
    """ORN NDA NewRoutine Radio Source Transit dataset"""

    @property
    def fields(self):
        if self._fields is None:
            self._fields = [self.file[0].header[f"CHANNEL{i+1}"] for i in range(2)]
        return self._fields

    def quicklook(
        self, file_png: Union[str, Path, None] = None, keys: [str] = ["LL", "RR"]
    ):
        self._quicklook(keys=keys, file_png=file_png, db=[True, True])


class OrnNdaMefistoSunEdrFitsData(
    OrnNdaNewRoutineEdrFitsData, dataset="orn_nda_mefisto_sun_edr"
):
    """ORN NDA Mefisto Sun dataset"""

    @property
    def fields(self):
        if self._fields is None:
            self._fields = [self.file[0].header[f"CHANNEL{i+1}"] for i in range(2)]
        return self._fields

    def quicklook(self, file_png=None, keys: [str] = ["LL", "RR"]):
        self._quicklook(keys=keys, file_png=file_png, db=[True, True])
