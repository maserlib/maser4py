# -*- coding: utf-8 -*-
from maser.data.base import CdfData

from astropy.time import Time
from astropy.units import Unit
from maser.data.base.sweeps import Sweeps


class RpwLfrSurvBp1Sweeps(Sweeps):
    @property
    def generator(self):
        """
        For each time, yield a frequency range and a dictionary with the following keys:
        - PB: power spectrum of the magnetic field (nT^2/Hz),
        - PE: the power spectrum of the electric field (V^2/Hz),
        - DOP: the degree of polarization of the waves (unitless),
        - ELLIP: the wave ellipticity (unitless),
        - SX_REA: the real part of the radial component of the Poynting flux (V nT/Hn, QF=1),

        """
        for frequency_band in self.data_reference.frequency_band_labels:
            for time, pb, pe, dop, ellip, sx_rea in zip(
                self.data_reference.times[frequency_band],
                self.file[f"PB_{frequency_band}"][...],
                self.file[f"PE_{frequency_band}"][...],
                self.file[f"DOP_{frequency_band}"][...],
                self.file[f"ELLIP_{frequency_band}"][...],
                self.file[f"SX_REA_{frequency_band}"][...],
            ):
                yield (
                    {"PB": pb, "PE": pe, "DOP": dop, "ELLIP": ellip, "SX_REA": sx_rea},
                    Time(time),
                    self.data_reference.frequencies[frequency_band],
                )


class RpwLfrSurvBp1(CdfData, dataset="solo_L2_rpw-lfr-surv-bp1"):
    _iter_sweep_class = RpwLfrSurvBp1Sweeps

    # keys used to loop over F0, F1, F2 frequency ranges and Burst/Normal modes
    frequency_band_labels = ["N_F2", "B_F1", "N_F1", "B_F0", "N_F0"]

    @property
    def frequencies(self):
        if self._frequencies is None:

            self._frequencies = {}

            with self.open(self.filepath) as cdf_file:
                for frequency_band in self.frequency_band_labels:
                    # if units are not specified, assume Hz
                    units = cdf_file[frequency_band].attrs["UNITS"].strip() or "Hz"
                    freq = cdf_file[frequency_band][...] * Unit(units)
                    self._frequencies[frequency_band] = freq

        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as cdf_file:
                self._times = {}
                for frequency_band in self.frequency_band_labels:
                    self._times[frequency_band] = Time(
                        cdf_file[f"Epoch_{frequency_band}"][...]
                    )

        return self._times

    def as_xarray(self):
        import xarray

        dataset = {
            "PE": {},
            "PB": {},
            "DOP": {},
            "ELLIP": {},
            "SX_REA": {},
        }

        default_units = {"PB": "nT^2/Hz"}

        for frequency_band in self.frequency_band_labels:
            frequencies = self.file[frequency_band][...]
            if len(frequencies) == 0:
                continue
            times = self.file[f"Epoch_{frequency_band}"][...]

            # force lower keys for frequency and time attributes
            time_attrs = {
                k.lower(): v
                for k, v in self.file[f"Epoch_{frequency_band}"].attrs.items()
            }

            frequency_attrs = {
                k.lower(): v for k, v in self.file[frequency_band].attrs.items()
            }
            if not frequency_attrs["units"].strip():
                frequency_attrs["units"] = "Hz"

            for dataset_key in dataset:
                values = self.file[f"{dataset_key}_{frequency_band}"][...]

                attrs = {
                    k.lower(): v
                    for k, v in self.file[
                        f"{dataset_key}_{frequency_band}"
                    ].attrs.items()
                }

                # if units are not defined, use the default ones
                if not attrs["units"].strip():
                    attrs["units"] = default_units.get(dataset_key, "")

                dataset[dataset_key][frequency_band] = xarray.DataArray(
                    values,
                    coords=[
                        ("time", times, time_attrs),
                        ("frequency", frequencies, frequency_attrs),
                    ],
                    attrs=attrs,
                    name=f"{dataset_key}_{frequency_band}",
                )

        return dataset
