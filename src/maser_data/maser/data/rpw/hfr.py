# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from astropy.time import Time
from astropy.units import Unit
import numpy as np

from maser.data.base.sweeps import Sweeps
from maser.data.base.cdf_fill import fill_records

HFR_SWEEP_DTYPE = [
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

        def get_sweep_data(i_sweep_start, i_sweep_end):

            # Initialize output data vector for the current sweep
            sweep_data = np.zeros(1, dtype=HFR_SWEEP_DTYPE)
            fill_records(sweep_data)

            # Extract HFR band and frequency values from sweep subset
            band = self.file["HFR_BAND"][i_sweep_start:i_sweep_end]
            freq = self.file["FREQUENCY"][i_sweep_start:i_sweep_end]

            # Identify HF1 and HF2 band cases
            where_hf1 = np.where(band == 1)[0]
            where_hf2 = np.where(band == 2)[0]

            # If there are HF1 band samples
            if where_hf1.shape[0] > 0:
                i_freq = ((freq[where_hf1] - 375.0) / 50.0).astype(int)
                sweep_data["VOLTAGE_SPECTRAL_POWER1"][0, i_freq] = self.file["AGC1"][
                    i_sweep_start:i_sweep_end
                ][where_hf1]
                sweep_data["VOLTAGE_SPECTRAL_POWER2"][0, i_freq] = self.file["AGC2"][
                    i_sweep_start:i_sweep_end
                ][where_hf1]

            # If there are HF2 band samples
            if where_hf2.shape[0] > 0:
                i_freq = (((freq[where_hf2] - 3625.0) / 100.0) + 64).astype(int)
                sweep_data["VOLTAGE_SPECTRAL_POWER1"][0, i_freq] = self.file["AGC1"][
                    i_sweep_start:i_sweep_end
                ][where_hf2]
                sweep_data["VOLTAGE_SPECTRAL_POWER2"][0, i_freq] = self.file["AGC2"][
                    i_sweep_start:i_sweep_end
                ][where_hf2]

            return sweep_data

        # Get total number of records in the CDF file
        n_rec = self.file["Epoch"].shape

        # Get list of indices of each sweep start
        sweep_start_index = get_sweep_start_index(self.file["SWEEP_NUM"][...])
        n_sweeps = len(sweep_start_index)
        # Add last CDF record index at the end of sweep_start_index
        # (needed to avoid loop failure below)
        sweep_start_index = np.insert(sweep_start_index, n_sweeps, n_rec)

        # Loop over each sweep in the CDF
        for i in range(n_sweeps):
            # Get start/end indices of the current sweep
            i_sweep_start = sweep_start_index[i]
            i_sweep_end = sweep_start_index[i + 1]

            sweep_data = get_sweep_data(i_sweep_start, i_sweep_end)

            yield (
                {
                    "VOLTAGE_SPECTRAL_POWER1": sweep_data["VOLTAGE_SPECTRAL_POWER1"][
                        0, :
                    ],
                    "VOLTAGE_SPECTRAL_POWER2": sweep_data["VOLTAGE_SPECTRAL_POWER2"][
                        0, :
                    ],
                },
                # Return the time of the first sample of the current sweep
                Time(self.file["Epoch"][i_sweep_start]),
                # Return the full list of available frequencies for HFR (192)
                self.data_reference.frequencies,
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
            # Get Epoch time of each first sample in the sweep
            mask = self.sweep_start_index
            self._times = Time(np.take(self.file["Epoch"][...], mask, axis=0))
        return self._times

    @property
    def sweep_start_index(self):
        # Define the list of indices of the first element of each sweep in the file
        if not hasattr(self, "_sweep_start_index") or self._sweep_start_index is None:
            self._sweep_start_index = get_sweep_start_index(self.file["SWEEP_NUM"][...])

        # Return resulting index array as a list
        return list(self._sweep_start_index)

    def as_xarray(self):
        """
        Return the data as a xarray
        """
        import xarray

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

        frequency = self.file["FREQUENCY"][...]

        try:
            units = self.file["AGC1"].attrs["UNITS"]
        except KeyError:
            # If UNITS not found in variable attribute
            # assume V^2/Hz
            units = "V^2/Hz"

        agc = xarray.DataArray(
            [self.file["AGC1"][...], self.file["AGC2"][...]],
            coords={
                "channel": self.channel_labels,
                "time": time,
                "frequency": (["time"], frequency),
                "sensor": (["time", "channel"], sensor_config),
            },
            dims=["channel", "time"],
            attrs={"units": units},
            name="VOLTAGE_SPECTRAL_POWER",
        )

        return xarray.Dataset({"VOLTAGE_SPECTRAL_POWER": agc})


def get_sweep_start_index(sweep_num):
    # Look for sweep start indices in SWEEP_NUM input array
    # (np.diff() is used to find where SWEEP_NUM value changes, i.e. != 0)
    sweep_start_index = np.asarray(np.diff(sweep_num) != 0).nonzero()
    sweep_start_index = np.insert((sweep_start_index[0] + 1), 0, 0)

    return list(sweep_start_index)
