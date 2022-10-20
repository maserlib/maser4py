# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from astropy.time import Time
from astropy.units import Unit
import numpy as np

from maser.data.base.sweeps import Sweeps

# ________________ Global Variables _____________
# (define here the global variables)

FREQUENCY_BAND_LABELS = ["HF1", "HF2"]
SURVEY_MODE_LABELS = ["SURVEY_NORMAL", "SURVEY_BURST"]
CHANNEL_LABELS = ["1", "2"]
SENSOR_MAPPING = {
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

# Total number of frequencies for HFR
N_FREQ = 192

# Initialize data type for output ndarray
HFR_SWEEP_DTYPE = [
    ("VOLTAGE_SPECTRAL_POWER1", ("float32", N_FREQ)),
    ("VOLTAGE_SPECTRAL_POWER2", ("float32", N_FREQ)),
]

# Lambda functions to return
GET_FREQ_INDEX = {
    1: lambda f: int((f - 375.0) / 50.0),
    "HF1": lambda f: int((f - 375.0) / 50.0),
    2: lambda f: int(((f - 3625.0) / 100.0) + 64),
    "HF2": lambda f: int(((f - 3625.0) / 100.0) + 64),
}

# ________________ Global Functions __________
# (If required, define here global functions)


def get_freq_indices(freq, band):
    return list(map(lambda freq, band: (GET_FREQ_INDEX[band](freq)), freq, band))


def get_sweep_start_index(sweep_num):
    # Look for sweep start indices in SWEEP_NUM input array
    # (np.diff() is used to find where SWEEP_NUM value changes, i.e. != 0)
    sweep_start_index = np.asarray(np.diff(sweep_num) != 0).nonzero()
    sweep_start_index = np.insert((sweep_start_index[0] + 1), 0, 0)

    return list(sweep_start_index)


# ________________ Class Definition __________
# (If required, define here classes)
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

        # Get total number of records in the CDF file
        n_rec = self.file["Epoch"].shape

        # Get list of indices of each sweep start
        sweep_start_index = get_sweep_start_index(self.file["SWEEP_NUM"][...])
        n_sweeps = len(sweep_start_index)
        # Add last CDF record index at the end of sweep_start_index
        # (needed to avoid loop failure below)
        sweep_start_index = np.insert(sweep_start_index, n_sweeps, n_rec)

        # Get frequency and corresponding HFR band values
        freq = self.file["FREQUENCY"][...]
        band = self.file["HFR_BAND"][...]

        # Loop over each sweep in the CDF
        for i in range(n_sweeps):
            # Get start/end indices of the current sweep
            i0 = sweep_start_index[i]
            i1 = sweep_start_index[i + 1]

            # Define indices of the frequencies for current sweep
            freq_indices = get_freq_indices(freq[i0:i1], band[i0:i1])

            yield (
                {
                    "VOLTAGE_SPECTRAL_POWER1": self.file["AGC1"][i0:i1],
                    "VOLTAGE_SPECTRAL_POWER2": self.file["AGC2"][i0:i1],
                },
                # Return the time of the first sample of the current sweep
                Time(self.file["Epoch"][i0]),
                # Return the list of frequencies
                self.data_reference.frequencies[freq_indices],
                (
                    SENSOR_MAPPING[self.file["SENSOR_CONFIG"][i][0]],
                    SENSOR_MAPPING[self.file["SENSOR_CONFIG"][i][1]],
                ),
                SURVEY_MODE_LABELS[self.file["SURVEY_MODE"][i]],
            )


class RpwHfrSurv(CdfData, dataset="solo_L2_rpw-hfr-surv"):
    _iter_sweep_class = RpwHfrSurvSweeps

    frequency_band_labels = FREQUENCY_BAND_LABELS
    survey_mode_labels = SURVEY_MODE_LABELS
    channel_labels = CHANNEL_LABELS
    sensor_mapping = SENSOR_MAPPING

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

    def as_xarray(self, as_is=True):
        """
        Return the HFR data as a xarray

        :param as_is: If True, returns HFR data is stored in the CDF. Otherwise build and return power as a 3D array
                      as a function of channel[2], time and frequency[192].
        :return: xarray containing HFR data
        """
        import xarray

        try:
            units = self.file["AGC1"].attrs["UNITS"]
        except KeyError:
            # If UNITS not found in variable attribute
            # assume V^2/Hz
            units = "V^2/Hz"

        if as_is:
            time = self.file["Epoch"][...]
            # Return HFR data as is
            sensor_config = list(
                map(
                    lambda configs: (
                        self.sensor_mapping[configs[0]],
                        self.sensor_mapping[configs[1]],
                    ),
                    self.file["SENSOR_CONFIG"][...],
                )
            )

            # Get vector of frequencies in the file
            frequency = self.file["FREQUENCY"][...]

            # Build xarray
            V_da = xarray.DataArray(
                [self.file["AGC1"][...], self.file["AGC2"][...]],
                coords={
                    "channel": self.channel_labels,
                    "time": time,
                    "frequency": (["time"], frequency),
                    "sensor": (["time", "channel"], sensor_config),
                },
                dims=["channel", "time"],
            )
        else:

            # Extract frequency and corresponding band values from file
            freq = self.file["FREQUENCY"][...]
            band = self.file["HFR_BAND"][...]

            # Define number of records
            n_rec = band.shape[0]
            # Get Epoch times of first sample of each sweep in the file
            sweep_times = self.times
            nt = len(sweep_times)
            # Get complete list of HFR frequency values
            hfr_frequency = self.frequencies
            nf = len(hfr_frequency)

            # Initialize output 2D array containing voltage spectral power values in V^2/Hz
            # Dims = (channels[2], time of the first sweep sample[len(time)], frequency[192])
            V_2d = np.empty((2, nt, nf))
            # Fill 2D array with NaN for HRF frequencies not actually measured in the file
            V_2d[:] = np.nan

            # Get list of first index of sweeps
            isweep = self.sweep_start_index
            # Get number of sweeps
            n_sweeps = len(isweep)
            # Insert an element in the end of the isweep list
            # containing the end of the latest sweep
            # (required for the loop below, in order to have
            # a start/end index range for each sweep)
            isweep = np.insert(isweep, n_sweeps, n_rec)

            # Initialize sensor_config
            sensor_config = np.zeros((2, nt), dtype=object)

            # Perform a loop on each sweep
            for i in range(n_sweeps):
                # Get first and last index of the sweep
                i0 = isweep[i]
                i1 = isweep[i + 1]

                # Get indices of the actual frequency values in the 192 frequency vector
                freq_indices = get_freq_indices(freq[i0:i1], band[i0:i1])

                # fill output 2D array
                V_2d[0, i, freq_indices] = self.file["AGC1"][i0:i1]
                V_2d[1, i, freq_indices] = self.file["AGC2"][i0:i1]

                # Fill sensor config
                sensor_config[0, i] = self.sensor_mapping[
                    self.file["SENSOR_CONFIG"][i0, 0]
                ]
                sensor_config[1, i] = self.sensor_mapping[
                    self.file["SENSOR_CONFIG"][i0, 1]
                ]

            # Define hfr bands
            hfr_band = (["HF1"] * 64) + (["HF2"] * 128)

            V_da = xarray.DataArray(
                V_2d,
                coords={
                    "channel": self.channel_labels,
                    "time": sweep_times.value,
                    "frequency": hfr_frequency,
                    "band": (["frequency"], hfr_band),
                    "sensor": (["channel", "time"], sensor_config),
                },
                dims=["channel", "time", "frequency"],
                attrs={"units": units},
                name="VOLTAGE_SPECTRAL_POWER",
            )

        return xarray.Dataset({"VOLTAGE_SPECTRAL_POWER": V_da})
