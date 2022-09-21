# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from astropy.time import Time
from astropy.units import Unit
from maser.data.base.sweeps import Sweeps
import numpy as np

HFR_SWEEP_DTYPE = [
    ("Epoch", ("datetime64[ns]", 192)),
    ("VOLTAGE_SPECTRAL_POWER1", ("float32", 192)),
    ("VOLTAGE_SPECTRAL_POWER2", ("float32", 192)),
]


class RpwHfrSurvSweeps(Sweeps):
    @property
    def generator(self):
        """
        For each time, yield a frequency range and a dictionary with the following keys:
        - VOLTAGE_SPECTRAL_POWER1 : Power spectral density at receiver + PA for channel 1 before applying antenna gain (V²/Hz)
        - VOLTAGE_SPECTRAL_POWER2 : Power spectral density at receiver + PA for channel 2 before applying antenna gain (V²/Hz)
        - SENSOR_CONFIG : Indicates the THR sensor configuration
        - SURVEY_MODE : normal (=0) or burst (=1) acquisition mode

        """

        def add_rec(in_data, out_data, rec_index):

            # Get frequency band index
            if in_data["HFR_BAND"][rec_index] == 1:
                i_band = int((in_data["FREQUENCY"][rec_index] - 375.0) / 50.0)
            elif in_data["HFR_BAND"][rec_index] == 2:
                i_band = int((in_data["FREQUENCY"][rec_index] - 3625.0) / 100.0) + 64
            else:
                return out_data

            # Fill values
            out_data["Epoch"][0, i_band] = in_data["Epoch"][rec_index]
            out_data["VOLTAGE_SPECTRAL_POWER1"][0, i_band] = in_data["AGC1"][rec_index]
            out_data["VOLTAGE_SPECTRAL_POWER2"][0, i_band] = in_data["AGC2"][rec_index]

            return out_data

        # First build list of frequency values for HFR (HF1+HF2 bands)
        freq = self.data_reference.frequencies

        # Initialize output data vector for the first sweep
        sweep_data = np.zeros(1, dtype=HFR_SWEEP_DTYPE)

        # Loop over each record in the CDF
        sweep_completed = False
        for i in range(self.file["SWEEP_NUM"].shape[0]):
            try:
                if self.file["SWEEP_NUM"][i] != self.file["SWEEP_NUM"][i + 1]:
                    sweep_data = add_rec(self.file, sweep_data, i)
                    sweep_completed = True
                    yield (
                        sweep_data,
                        Time(sweep_data["Epoch"][0, 0]),
                        freq,
                        self.file["SENSOR_CONFIG"][i],
                        self.file["SURVEY_MODE"][i],
                    )
                else:
                    if sweep_completed:
                        sweep_completed = False
                        sweep_data = np.empty(1, dtype=HFR_SWEEP_DTYPE)

                    sweep_data = add_rec(self.file, sweep_data, i)
            except IndexError:
                # End of CDF file is reached, force yield for last record
                yield (
                    sweep_data,
                    Time(sweep_data["Epoch"][0, 0]),
                    freq,
                    self.file["SENSOR_CONFIG"][i],
                    self.file["SURVEY_MODE"][i],
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
                # if units are not specified, assume kHz
                units = Unit(cdf_file["FREQUENCY"].attrs["UNITS"].strip() or "kHz")
                # Compute frequency values for HF1 and HF2 bands
                f1 = 375 + 50 * np.arange(64)
                f2 = 3625 + 100 * np.arange(128)
                self._frequencies = np.concatenate((f1, f2)) * units

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
