# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from astropy.units import Unit
from astropy.time import Time
import numpy as np
import xarray
from .sweeps import WindWavesRad1Sweeps


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
            with self.open(self.filepath) as cdf_file:
                self._times = Time(cdf_file["Epoch"][...])
        return self._times

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
            with self.open(self.filepath) as cdf_file:
                self._times = Time(cdf_file["Epoch"][...])
        return self._times

    def as_xarray(self):
        pass


class WindWavesRad1L3DfV02Data(CdfData, dataset="wi_wav_rad1_l3_df_v02"):
    from functools import lru_cache

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
    @lru_cache(maxsize=32)
    def dirty_sorting(self):
        return np.argsort(self.file["Epoch"][...])

    @property
    def frequencies(self):
        if self._frequencies is None:
            units = self.file["FREQUENCY"].attrs["UNITS"]
            freq = self.file["FREQUENCY"][...][self.dirty_sorting]
            if self.access_mode == "sweeps":
                freq = np.unique(np.sort(freq[:64]))
            self._frequencies = freq * Unit(units)
        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as cdf_file:
                times = Time(cdf_file["Epoch"][...])[self.dirty_sorting]
                if self.access_mode == "sweeps":
                    times = times[::16]
                self._times = times
        return self._times

    @staticmethod
    def get_indices(isweep):
        """Get the list of data indices in raw data for a given sweep.

        Internal data format is a 1D data vector: a series of 64-steps raw sweeps, with repeating some frequencies.
        - 16 frequency steps repeated once (band-a)
            f(kHz) | 20, 24, 28, 32, 36, 40, 44, 48, 52, 60, 72, 80, 92, 104, 116, 136
            -------+--------------------------------------------------------------------
            index  | 63, 31, 47, 15, 55, 23, 39,  7, 62, 30, 46, 14, 54,  22,  38,   6

        - 8 frequency steps repeated twice (band-b)
            f(kHz) | 152, 176, 196, 224, 256, 292, 332, 376
            -------+-----------------------------------------
            index  |  29,  13,  21,   5,  28,  12,  20,   4
            index  |  61,  45,  53,  37,  60,  44,  52,  36

        - 8 frequency steps repeated four times (band-c)
            f(kHz) | 428, 484, 548, 624, 708, 804, 916, 1040
            -------+------------------------------------------
            index  |  11,   3,  10,   2,   9,   1,   8,   0
            index  |  27,  19,  26,  18,  25,  17,  24,  16
            index  |  43,  35,  42,  34,  41,  33,  40,  32
            index  |  59,  51,  58,  50,  57,  49,  56,  48

        Public data format is composed of 32-steps sweeps, with distinct frequencies.
        - band-a is repeated in each consecutive 4 sweeps
            [63, 31, 47, 15, 55, 23, 39,  7, 62, 30, 46, 14, 54, 22, 38,  6]
            [63, 31, 47, 15, 55, 23, 39,  7, 62, 30, 46, 14, 54, 22, 38,  6]
            [63, 31, 47, 15, 55, 23, 39,  7, 62, 30, 46, 14, 54, 22, 38,  6]
            [63, 31, 47, 15, 55, 23, 39,  7, 62, 30, 46, 14, 54, 22, 38,  6]
        - band-b is repeated in each consecutive 2 sweeps
            [29, 13, 21,  5, 28, 12, 20,  4]
            [29, 13, 21,  5, 28, 12, 20,  4]
            [61, 45, 53, 37, 60, 44, 52, 36]
            [61, 45, 53, 37, 60, 44, 52, 36]
        - band-c is not repeated
            [11,  3, 10,  2,  9,  1,  8,  0]
            [27, 19, 26, 18, 25, 17, 24, 16]
            [43, 35, 42, 34, 41, 33, 40, 32]
            [59, 51, 58, 50, 57, 49, 56, 48]

        :param isweep: sweep id in public data format
        :return: list of indices in raw data
        """
        isweep_raw = isweep // 4
        # band-a
        steps_band_a = [63, 31, 47, 15, 55, 23, 39, 7, 62, 30, 46, 14, 54, 22, 38, 6]
        # band-b (second set is +32 for each value)
        steps_band_b = [29, 13, 21, 5, 28, 12, 20, 4]
        steps_band_b = [k + 32 * ((isweep // 2) % 2) for k in steps_band_b]
        # band-c (other sets are +16,+32,+48 for each value)
        steps_band_c = [11, 3, 10, 2, 9, 1, 8, 0]
        steps_band_c = [k + 16 * (isweep % 4) for k in steps_band_c]
        return isweep_raw, steps_band_a + steps_band_b + steps_band_c

    def as_xarray(self):

        datasets = {}
        nsweep_raw = int(len(self.times) / 4)
        nstep_raw = 64
        nsweep = len(self.times)
        nstep = len(self.frequencies)

        for dataset_key in self._dataset_keys:
            data_ext = self.file[dataset_key]
            data_attr = data_ext.attrs
            data_raw = data_ext[...][self.dirty_sorting].reshape(nsweep_raw, nstep_raw)
            data_raw = np.where(data_raw == data_attr["FILLVAL"], np.nan, data_raw)

            data = np.zeros((nstep, nsweep))

            for i in range(len(self.times)):
                raw_sweep, raw_indices = self.get_indices(i)
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

        return datasets
