# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from astropy.units import Unit
from astropy.time import Time
import numpy
import xarray


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
            data = numpy.where(data == data_attr["FILLVAL"], numpy.nan, data)

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


class WindWavesRad1L3DfData(CdfData, dataset="wi_wav_rad1_l3_df"):

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
