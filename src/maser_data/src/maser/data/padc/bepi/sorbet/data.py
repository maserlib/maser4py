# -*- coding: utf-8 -*-

"""Classes for Sorbet datasets"""

from maser.data.base import CdfData

from typing import Union, List
from pathlib import Path
from astropy.time import Time
from astropy.units import Unit


class SorbetL1CdfData(CdfData, dataset="mmo_pwi_sorbet_l1_"):  # type: ignore
    """Class for `sorbet` L1 CDF files."""

    def __init_subclass__(cls, *args, dataset: str, **kwargs) -> None:
        return super().__init_subclass__(*args, dataset=dataset, **kwargs)

    # _dataset_keys = ["sorbet_WPT_spectra"]

    @property
    def times(self):
        if self._times is None:
            self._times = Time([], format="jd")
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

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def as_xarray(self):
        import xarray

        dataset_keys = self.dataset_keys
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


class SorbetL1CdfTnr(SorbetL1CdfData, dataset="mmo_pwi_sorbet_l1_ex_specdB-tnr-qtn_"):
    """Class for `sorbet` L1 CDF TNR files."""

    _dataset_keys = ["sorbet_WPT_spectra"]

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        yscale: str = "log",
        keys: List[str] = ["sorbet_WPT_spectra"],
        **kwargs,
    ):
        self._quicklook(
            keys=keys,
            file_png=file_png,
            # landscape=landscape,
            # db=[True,True],
            yscale=yscale,
            **kwargs,
        )


class SorbetL1CdfDbsc(
    SorbetL1CdfData, dataset="mmo_pwi_sorbet_l1_bz-ex_complex-specdB-tnr"
):
    """Class for `sorbet` L1 CDF TNR-DBSC files."""

    _dataset_keys = [
        "sorbet_dbsc_spectra",
        "Bz_Ex_cross_amplitude",
        "Bz_Ex_cross_phase",
    ]

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        yscale: str = "log",
        keys: List[str] = [
            "sorbet_dbsc_spectra",
            "Bz_Ex_cross_amplitude",
            "Bz_Ex_cross_phase",
        ],
        **kwargs,
    ):
        self._quicklook(
            keys=keys,
            file_png=file_png,
            # landscape=landscape,
            # db=[True,True],
            yscale=yscale,
            **kwargs,
        )
