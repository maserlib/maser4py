# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from astropy.units import Unit
from astropy.time import Time
import numpy as np
import xarray
from .sweeps import WindWavesRad1Sweeps
from typing import List

# from functools import lru_cache
from .utils import get_indices


class WindWavesRad1L3AkrData(CdfData, dataset="wi_wa_rad1_l3-akr"):

    _dataset_keys = [
        "FLUX_DENSITY",
        "SNR",
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
            self._times = Time([], format="jd")
            with self.open(self.filepath) as cdf_file:
                self._times = Time(cdf_file["Epoch"][...])
        return self._times

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def as_xarray(self):

        datasets = {}

        for dataset_key in self._dataset_keys:

            # Sort out data and attributes
            data_ext = self.file[dataset_key]
            data_attr = self.file[dataset_key].attrs

            # extract the data and replace the values at FILLVAL by NaN
            data = data_ext[...]
            data = np.where(data == data_attr["FILLVAL"], np.nan, data)

            datasets[dataset_key] = xarray.DataArray(
                data=data,
                name=data_attr.get("LABLAXIS", dataset_key),
                coords=[
                    ("time", self.times.to_datetime()),
                    (
                        "frequency",
                        self.frequencies.value,
                        {"units": self.frequencies.unit},
                    ),
                ],
                dims=("time", "frequency"),
                attrs={
                    "units": data_attr.get("UNITS", None),
                    "title": data_attr["CATDESC"],
                },
            ).transpose("frequency", "time")
        return xarray.Dataset(data_vars=datasets)

    def quicklook(
        self, file_png=None, keys: List[str] = ["FLUX_DENSITY", "SNR"], **kwargs
    ):
        import numpy

        default_keys = ["FLUX_DENSITY", "SNR"]
        db_tab = numpy.array([True, True])
        for qkey, tab in zip(["db"], [db_tab]):
            if qkey not in kwargs:
                qkey_tab = []
                for key in keys:
                    if key in default_keys:
                        qkey_tab.append(
                            tab[numpy.where(key == numpy.array(default_keys))][0]
                        )
                    else:
                        qkey_tab.append(None)
                kwargs[qkey] = list(qkey_tab)
        self._quicklook(
            keys=keys,
            file_png=file_png,
            # vmin=[68, 68],
            # vmax=[94, 94],
            # db=[True, True],
            **kwargs,
        )

    def epncore(self):
        if self._epncore is None:
            self._epncore = CdfData.epncore(self)
        self._epncore["obs_id"] = f"wi_wa_rad1_{self.filepath.stem.split('_')[-2]}"
        self._epncore["publisher"] = "PADC"
        return self._epncore


class WindWavesRad1L3DfV01Data(CdfData, dataset="wi_wav_rad1_l3_df_v01"):

    _iter_sweep_class = WindWavesRad1Sweeps
    _dataset_keys = [
        "FLUX",
        "ELEVATION",
        "AZIMUTH",
        "ANGULAR_RADIUS",
        "MODULATION",
    ]

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as cdf_file:
                units = cdf_file["FREQ"].attrs["UNITS"]
                freq = cdf_file["FREQ"][...] * Unit(units)
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
        pass


class WindWavesRad1L3DfV02Data(CdfData, dataset="wi_wav_rad1_l3_df_v02"):

    _iter_sweep_class = WindWavesRad1Sweeps
    _dataset_keys = [
        "STOKES_I",
        "SWEEP",
        # "NUM",
        "WAVE_AZIMUTH_SRF",
        "WAVE_COLATITUDE_SRF",
        "SOURCE_SIZE",
        "QUALITY_FLAG",
        "MODULATION_RATE",
    ]

    @property
    def frequencies(self):
        if self._frequencies is None:
            units = self.file["FREQUENCY"].attrs["UNITS"]
            freq = self.file["FREQUENCY"][...]
            if self.access_mode == "sweeps":
                freq = np.unique(np.sort(freq[:64]))
            self._frequencies = freq * Unit(units)
        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            self._times = Time([], format="jd")
            with self.open(self.filepath) as cdf_file:
                times = Time(cdf_file["Epoch"][...])
                if self.access_mode == "sweeps":
                    times = times[::16]
                self._times = times
        return self._times

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def as_xarray(self):

        datasets = {}
        nsweep_raw = int(len(self.times) / 4)
        nstep_raw = 64
        nsweep = len(self.times)
        nstep = len(self.frequencies)

        for dataset_key in self._dataset_keys:
            data_ext = self.file[dataset_key]
            data_attr = data_ext.attrs
            data_raw = data_ext[...].reshape(nsweep_raw, nstep_raw)
            data_raw = np.where(data_raw == data_attr["FILLVAL"], np.nan, data_raw)

            data = np.zeros((nstep, nsweep))

            for i in range(len(self.times)):
                raw_sweep, raw_indices = get_indices(i)
                data[:, i] = data_raw[raw_sweep, raw_indices]

            datasets[dataset_key] = xarray.DataArray(
                data=data,
                name=data_attr.get("LABLAXIS", dataset_key),
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
                    "units": data_attr.get("UNITS", None),
                    "title": data_attr["CATDESC"],
                },
            )

        return xarray.Dataset(data_vars=datasets)

    def quicklook(
        self, file_png=None, keys: List[str] = ["SWEEP", "STOKES_I"], **kwargs
    ):
        import numpy

        default_keys = ["SWEEP", "STOKES_I"]
        db_tab = numpy.array([True, True])
        for qkey, tab in zip(["db"], [db_tab]):
            if qkey not in kwargs:
                qkey_tab = []
                for key in keys:
                    if key in default_keys:
                        qkey_tab.append(
                            tab[numpy.where(key == numpy.array(default_keys))][0]
                        )
                    else:
                        qkey_tab.append(None)
                kwargs[qkey] = list(qkey_tab)
        self._quicklook(
            keys=keys,
            file_png=file_png,
            # vmin=[68, 68],
            # vmax=[94, 94],
            # db=[True, True],
            **kwargs,
        )
