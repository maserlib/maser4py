# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from astropy.time import Time
from astropy.units import Unit
from maser.data.base.sweeps import Sweeps
import numpy as np


class RpwHfrSurvSweeps(Sweeps):
    @property
    def generator(self):
        """
        For each time, yield a frequency range and a dictionary with the following keys:
        - AGC1 : Power spectral density at receiver + PA for channel 1 before applying antenna gain (V²/Hz)
        - AGC2 : Power spectral density at receiver + PA for channel 2 before applying antenna gain (V²/Hz)
        - SENSOR_CONFIG : Indicates the THR sensor configuration
        - SURVEY_MODE : normal (=0) or burst (=1) acquisition mode

        """

        def increment_sweep(sweep_mask, i):
            if self.file["SWEEP_NUM"][i] != self.file["SWEEP_NUM"][i - 1]:
                sweep_mask[-1].sort()
                sweep_mask.append([i])
            else:
                sweep_mask[-1].append(i)

        # First generate a mask for each sweep
        sweep_mask = [[0]]
        _ = [
            increment_sweep(sweep_mask, i)
            for i in range(1, self.file["SWEEP_NUM"].shape[0])
        ]

        for indices in sweep_mask:
            yield (
                {
                    "VOLTAGE_SPECTRAL_POWER1": np.take(
                        self.file["AGC1"], indices, axis=0
                    ).flatten(),
                    "VOLTAGE_SPECTRAL_POWER2": np.take(
                        self.file["AGC2"], indices, axis=0
                    ).flatten(),
                    "SENSOR_CONFIG": np.take(self.file["SENSOR_CONFIG"], indices),
                    "SURVEY_MODE": np.take(self.file["SURVEY_MODE"], indices),
                },
                Time(self.file["Epoch"][indices[0]]),
                np.take(self.file["FREQUENCY"], indices, axis=0).flatten(),
            )


class RpwHfrSurv(CdfData, dataset="solo_L2_rpw-hfr-surv"):
    _iter_sweep_class = RpwHfrSurvSweeps

    frequency_band_labels = ["HF1", "HF2"]

    survey_mode_labels = ["SURVEY_NORMAL", "SURVEY_BURST"]

    channel_labels = ["1", "2"]

    sensor_mapping = {
        1: "V1",
        2: "V2",
        3: "V3",
        4: "V1-V2",
        5: "V2-V3",
        6: "V3-V1",
        7: "B_MF",
        9: "HF_V1-V2",
        10: "HF_V2-V3",
        11: "HF_V3-V1",
    }

    @property
    def frequencies(self):
        if self._frequencies is None:

            with self.open(self.filepath) as cdf_file:
                for band_index, band_label in enumerate(self.frequency_band_labels):
                    # if units are not specified, assume Hz
                    units = cdf_file["FREQUENCY"].attrs["UNITS"].strip() or "kHz"
                    freq = np.unique(cdf_file["FREQUENCY"][...]) * Unit(units)
                    self._frequencies = freq

        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            for band_index, frequency_band in enumerate(self.frequency_band_labels):
                mask = (self.file["TNR_BAND"][...] == band_index)[0]
                self._times[frequency_band] = Time(self.file["Epoch"][mask])
        return self._times

    def as_xarray(self):
        """
        Return the data as a xarray
        """
        import xarray

        band = xarray.DataArray(
            [self.frequency_band_labels[idx] for idx in self.file["TNR_BAND"][...]]
        )
        time = self.file["Epoch"][...]

        sensor_config = list(
            map(
                lambda configs: (
                    self.sensor_mapping[configs[0]],
                    self.sensor_mapping[configs[1]],
                ),
                self.file["SENSOR_CONFIG"][...],
            )
        )

        tnr_frequency_bands = self.file["TNR_BAND_FREQ"][...]
        freq_index = range(tnr_frequency_bands.shape[1])

        frequency = self.file["FREQUENCY"][...]  # (n_time, n_freq)

        agc = xarray.DataArray(
            [self.file["AGC1"][...], self.file["AGC2"][...]],
            coords={
                "channel": self.channel_labels,
                "time": time,
                "freq_index": freq_index,
                "band": ("time", band.data),
                "frequency": (["time", "freq_index"], frequency.data),
                "sensor": (["time", "channel"], sensor_config),
            },
            dims=["channel", "time", "freq_index"],
        )

        return xarray.Dataset({"agc": agc})
