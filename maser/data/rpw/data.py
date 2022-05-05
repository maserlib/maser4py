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
        for frequency_key in self.data_reference.frequency_keys:
            for time, pb, pe, dop, ellip, sx_rea in zip(
                self.data_reference.times[frequency_key],
                self.file[f"PB_{frequency_key}"],
                self.file[f"PE_{frequency_key}"],
                self.file[f"DOP_{frequency_key}"],
                self.file[f"ELLIP_{frequency_key}"],
                self.file[f"SX_REA_{frequency_key}"],
            ):
                yield (
                    {"PB": pb, "PE": pe, "DOP": dop, "ELLIP": ellip, "SX_REA": sx_rea},
                    Time(time),
                    self.data_reference.frequencies[frequency_key],
                )


class RpwLfrSurvBp1(CdfData, dataset="solo_L2_rpw-lfr-surv-bp1"):
    _iter_sweep_class = RpwLfrSurvBp1Sweeps

    # keys used to loop over F0, F1, F2 frequency ranges and Burst/Normal modes
    frequency_keys = ["N_F2", "B_F1", "N_F1", "B_F0", "N_F0"]

    @property
    def frequencies(self):
        if self._frequencies is None:

            self._frequencies = {}

            with self.open(self.filepath) as cdf_file:
                for frequency_key in self.frequency_keys:
                    # if units are not specified, assume Hz
                    units = cdf_file[frequency_key].attrs["UNITS"].strip() or "Hz"
                    freq = cdf_file[frequency_key][...] * Unit(units)
                    self._frequencies[frequency_key] = freq

        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as cdf_file:
                self._times = {}
                for frequency_key in self.frequency_keys:
                    self._times[frequency_key] = Time(
                        cdf_file[f"Epoch_{frequency_key}"][...]
                    )
        return self._times
