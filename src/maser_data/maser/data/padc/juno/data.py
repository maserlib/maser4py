# -*- coding: utf-8 -*-
from maser.data.base import CdfData, Sweeps
from astropy.units import Unit
from astropy.time import Time
from typing import Union, List
from pathlib import Path


class JnoWavLesiaL3aV02Sweeps(Sweeps):
    @property
    def generator(self):
        attrs = self.file["Data"].attrs
        for t, d in zip(self.data_reference.times, self.file["Data"][...]):
            yield (
                t,
                self.data_reference.frequencies,
                d[...] * Unit(attrs["UNITS"]),
            )


class JnoWavLesiaL3aV02Data(CdfData, dataset="jno_wav_cdr_lesia"):
    _iter_sweep_class = JnoWavLesiaL3aV02Sweeps

    _dataset_keys = [
        "DEFAULT",
    ]

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as cdf_file:
                units = cdf_file["Frequency"].attrs["UNITS"]
                freq = cdf_file["Frequency"][...] * Unit(units)
                self._frequencies = freq
        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as cdf_file:
                self._times = Time(cdf_file["Epoch"][...])
        return self._times

    def as_xarray(self):
        import xarray

        datasets = {}

        for dataset_key in self._dataset_keys:
            dataset = xarray.DataArray(
                data=self.file["Data"][...].T,
                name=self.dataset,
                coords=[
                    (
                        "frequency",
                        self.frequencies.value,
                        {"units": self.frequencies.unit},
                    ),
                    ("time", self.times.to_datetime()),
                ],
                dims=("frequency", "time"),
                attrs={"units": self.file["Data"].attrs["UNITS"]},
            )
            datasets[dataset_key] = dataset.sortby("frequency")
        return xarray.Dataset(data_vars=datasets)

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["DEFAULT", "DEFAULT"],
        **kwargs,
    ):
        self._quicklook(keys=keys, file_png=file_png, db=[True, True], **kwargs)
