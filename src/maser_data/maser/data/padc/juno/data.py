# -*- coding: utf-8 -*-
from maser.data.base import CdfData, Sweeps
from astropy.units import Unit
from astropy.time import Time
from datetime import datetime
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

    @property
    def epncore(self):
        import os
        import numpy

        md = CdfData.epncore(self)
        md["obs_id"] = md["granule_uid"]
        # md["instrument_host_name"] = "juno"
        # md["instrument_name"] = "waves"
        md["target_name"] = "Jupiter"
        # md["target_class"] = "planet"
        # md["target_region"] = "TBD"
        # md["feature_name"] = "Radio Emission#Type II#Type III"

        md["dataproduct_type"] = "ds"

        md["spectral_range_min"] = min(self.frequencies.to("Hz").value)
        md["spectral_range_max"] = max(self.frequencies.to("Hz").value)

        md["publisher"] = "PADC"
        md["filepath"] = str(self.filepath)  # cdf_file

        datetmp = str(self.file.attrs["Generation_date"])
        md["creation_date"] = Time(
            datetime(int(datetmp[0:4]), int(datetmp[5:6]), int(datetmp[7:8]))
        ).iso
        # md["creation_date"] = Time(self.file.attrs["Generation_date"][0], format="datetime").iso
        md["release_date"] = Time(os.path.getmtime(self.filepath), format="unix").iso
        md["modification_date"] = Time.now().iso

        md["processing_level"] = 5  # simulation / derived data

        md["spectral_resolution_min"] = float(md["spectral_range_min"]) / 50e3
        md["spectral_resolution_max"] = float(md["spectral_range_max"]) / 50e3

        freq = numpy.sort(self.frequencies.to("Hz").value)  # .sort()
        sampling_step = freq[1:] - freq[:-1]
        md["spectral_sampling_step_min"] = min(sampling_step)

        md["spectral_sampling_step_max"] = max(sampling_step)

        md["time_scale"] = "UTC"

        return md

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["DEFAULT", "DEFAULT"],
        **kwargs,
    ):
        self._quicklook(keys=keys, file_png=file_png, db=[True, True], **kwargs)
