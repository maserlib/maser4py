# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from astropy.time import Time
from astropy.units import Unit
import numpy as np
from typing import Union, List
from pathlib import Path

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
        # band = self.file["HFR_BAND"][...] # not reliable
        units = Unit(self.file["FREQUENCY"].attrs["UNITS"].strip() or "kHz")

        # Loop over each sweep in the CDF
        for i in range(n_sweeps):
            # Get start/end indices of the current sweep
            i0 = sweep_start_index[i]
            i1 = sweep_start_index[i + 1]

            # Define indices of the frequencies for current sweep
            # freq_indices = get_freq_indices(freq[i0:i1], band[i0:i1]) # deprecated

            yield (
                {
                    "VOLTAGE_SPECTRAL_POWER1": self.file["AGC1"][i0:i1],
                    "VOLTAGE_SPECTRAL_POWER2": self.file["AGC2"][i0:i1],
                },
                # Return the time of the first sample of the current sweep
                Time(self.file["Epoch"][i0]),
                # Return the list of frequencies
                # self.data_reference.frequencies[freq_indices],
                freq[i0:i1] * units,
                (
                    SENSOR_MAPPING[self.file["SENSOR_CONFIG"][i][0]],
                    SENSOR_MAPPING[self.file["SENSOR_CONFIG"][i][1]],
                ),
                SURVEY_MODE_LABELS[self.file["SURVEY_MODE"][i]],
            )


class RpwHfrSurv(CdfData, dataset="solo_L2_rpw-hfr-surv"):
    _iter_sweep_class = RpwHfrSurvSweeps

    _dataset_keys = [
        "VOLTAGE_SPECTRAL_POWER",
        "SENSOR",
        "CHANNEL",
        "V1",
        "V2",
        "V3",
        "V1-V2",
        "V2-V3",
        "V3-V1",
        "B_MF",
        "HF_V1-V2",
        "HF_V2-V3",
        "HF_V3-V1",
        "DELTA_TIMES",
        "FREQ_INDICES",
        "VOLTAGE_SPECTRAL_POWER_CH1",
        "VOLTAGE_SPECTRAL_POWER_CH2",
    ]

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
                # Removed # Compute frequency values for HF1 and HF2 bands
                # f1 = 375 + 50 * np.arange(64)
                # f2 = 3625 + 100 * np.arange(128)

                def sort_uniq(sequence):  # a fast way to sort(unique(sequence))
                    import itertools
                    import operator

                    return map(
                        operator.itemgetter(0), itertools.groupby(sorted(sequence))
                    )

                freq = cdf_file["FREQUENCY"][...]
                freq = list(sort_uniq(freq))
                self._frequencies = freq * units  # np.concatenate((f1, f2)) * units

        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            self._times = Time([], format="jd")
            # Get Epoch time of each first sample in the sweep
            mask = self.sweep_start_index
            self._times = Time(np.take(self.file["Epoch"][...], mask, axis=0))
        return self._times

    @property
    def delta_times(self):
        if self._delta_times is None:
            xr = self.as_xarray()
            if len(self._delta_times[0, :]) != len(xr.time):
                raise ValueError("Conflict in Time object dimensions.")
        return self._delta_times

    @property
    def sweep_start_index(self):
        # Define the list of indices of the first element of each sweep in the file
        if not hasattr(self, "_sweep_start_index") or self._sweep_start_index is None:
            self._sweep_start_index = get_sweep_start_index(self.file["SWEEP_NUM"][...])

        # Return resulting index array as a list
        return list(self._sweep_start_index)

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def as_xarray(self, as_is=False):
        """
        Return the HFR data as a xarray

        :param as_is: If True, returns HFR data is stored in the CDF. Otherwise build and return power as a 3D array
                      as a function of channel[2], time and frequency[192].
        :return: xarray containing HFR data
        """
        import xarray

        dataset_keys = [
            "VOLTAGE_SPECTRAL_POWER",
            "SENSOR",
            "CHANNEL",
            "V1",
            "V2",
            "V3",
            "V1-V2",
            "V2-V3",
            "V3-V1",
            "B_MF",
            "HF_V1-V2",
            "HF_V2-V3",
            "HF_V3-V1",
            "DELTA_TIMES",
            "FREQ_INDICES",
            "VOLTAGE_SPECTRAL_POWER_CH1",
            "VOLTAGE_SPECTRAL_POWER_CH2",
        ]

        sensor_keys = [
            "V1",
            "V2",
            "V3",
            "V1-V2",
            "V2-V3",
            "V3-V1",
            "B_MF",
            "HF_V1-V2",
            "HF_V2-V3",
            "HF_V3-V1",
        ]

        try:
            units = self.file["AGC1"].attrs["UNITS"]
        except KeyError:
            # If UNITS not found in variable attribute
            # assume V^2/Hz
            units = "V^2/Hz"

        if as_is:  # old way
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
                attrs={"units": units},
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

            # Same for a verification table
            freq_ind_table = np.empty((nt, nf))
            freq_ind_table[:] = np.nan

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

                # Get indices of the actual frequency values since they are not always sorted
                # freq_indices = get_freq_indices(freq[i0:i1], band[i0:i1]) # old way if 192 freqs
                freq_indices = hfr_frequency.value.searchsorted(freq[i0:i1])
                # freq_ind_table[i, :] = freq_indices
                freq_ind_table[i, freq_indices] = np.arange(len(freq_indices))

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

            # Filtering the All-NaN slice warning for the following section
            # nanmax is used here to detect the All-NaN lines and thus we do not want the warning
            # There is always MAX 1 channel used so at least 1 Nan per (freq,time) in 1 channel
            import warnings

            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="All-NaN slice encountered")
                # Computing delta_times
                nanline = np.empty((nt - 2))
                nanline[:] = np.nan
                # delta_times = Time([], format="jd")
                timeref = Time(self.file["Epoch"][...])
                delta_times = []
                delta_times_first = np.empty((nf))
                delta_times_last = np.empty((nf))
                delta_times_first[:] = np.nan
                delta_times_last[:] = np.nan
                isweep_r = isweep[1:-2]
                j = 0
                jfirst = 0
                jlast = 0
                for i in range(nf):
                    # First sweep - may be incomplete
                    # Check whether the measurement exists and fills delta_times if so
                    if np.nanmax(V_2d[:, 0, i], axis=0) > -np.inf:
                        delta_times_first[i] = (timeref[jfirst] - self.times[0]).value
                        jfirst += 1

                    # regular sweep
                    if np.nanmax(V_2d[:, :, i]) > -np.inf:  # Main case
                        delta_times = np.append(
                            delta_times,
                            (timeref[isweep_r + j] - self.times[1:-1]).value,
                        )
                        j += 1
                    else:
                        delta_times = np.append(
                            delta_times, nanline
                        )  # if a frequency is ONLY here in first or last sweep

                    # Last sweep - maybe be incomplete
                    # Check whether the measurement exists and fills delta_times if so
                    if np.nanmax(V_2d[:, -1, i], axis=0) > -np.inf:
                        delta_times_last[i] = (
                            timeref[isweep[-2] + jlast] - self.times[-1]
                        ).value
                        jlast += 1
                delta_times = np.append(delta_times_first, delta_times)
                delta_times = np.append(delta_times, delta_times_last)
                delta_times = np.reshape(delta_times, (nf, nt))
                self._delta_times = delta_times  # stores delta_times

            # Define hfr bands
            # hfr_band = (["HF1"] * 64) + (["HF2"] * 128) # not accurrate

            dataset = {}
            firstloop = 1
            for key in dataset_keys:
                if key == "VOLTAGE_SPECTRAL_POWER":
                    main_data = (np.nanmax(V_2d, axis=0)).T
                    values = main_data
                    # sensor_conf = np.max(sensor_config, axis = 0)
                    coords = [
                        # "channel": self.channel_labels,
                        ("frequency", hfr_frequency, {"units": self.frequencies.unit}),
                        ("time", sweep_times.value),
                        # ("band", (["frequency"], hfr_band)),
                        # "sensor": (["channel", "time"], sensor_config),
                        # ("sensor", (["time"], sensor_conf)),
                    ]
                    dims = ["frequency", "time"]
                    units_da = units
                elif "VOLTAGE_SPECTRAL_POWER_CH" in key:
                    if key == "VOLTAGE_SPECTRAL_POWER_CH1":
                        i = 1
                    else:
                        i = 2
                    values = (V_2d[i - 1, :, :]).T
                    # sensor_conf = sensor_config[i-1, :]
                    coords = [
                        ("frequency", hfr_frequency, {"units": self.frequencies.unit}),
                        ("time", sweep_times.value),
                    ]
                    dims = ["frequency", "time"]
                    units_da = units
                elif key == "SENSOR":

                    # Computing which sensor of the 2 channels is used
                    tabref = np.array(
                        np.nanmax(
                            V_2d[
                                1,
                                :,
                                :,
                            ],
                            axis=1,
                        )
                    )
                    sens_conf = sensor_config[0, :]
                    sens_conf[np.where(tabref - np.inf)] = sensor_config[1, :][
                        np.where(tabref > -np.inf)
                    ]
                    values = sens_conf
                    # Saving channel info as well
                    channel = np.ones([len(sens_conf)])
                    channel[np.where(tabref > -np.inf)] = 2
                    coords = [
                        ("time", sweep_times.value),
                    ]
                    dims = ["time"]
                    units_da = ""
                elif key == "CHANNEL":
                    if "SENSOR" not in dataset.keys():
                        raise ValueError("Trying to add CHANNEL before computing it.")
                    values = channel  # Computed in key i = 3
                    coords = [
                        ("time", sweep_times.value),
                    ]
                    dims = ["time"]
                    units_da = ""
                elif key == "DELTA_TIMES":
                    values = delta_times
                    coords = [
                        ("frequency", hfr_frequency, {"units": self.frequencies.unit}),
                        ("time", sweep_times.value),
                    ]
                    dims = ["frequency", "time"]
                    units_da = "jd"
                elif key == "FREQ_INDICES":  # Previously hfr_band but dropped
                    # for check purpose mainly
                    values = freq_ind_table.T
                    coords = [
                        ("frequency", hfr_frequency, {"units": self.frequencies.unit}),
                        ("time", sweep_times.value),
                    ]
                    dims = ["frequency", "time"]
                    units_da = ""
                elif key in sensor_keys:
                    if "VOLTAGE_SPECTRAL_POWER" not in dataset.keys():
                        raise ValueError(
                            "Trying to add a sensor key before computing the main data."
                        )
                    if "SENSOR" not in dataset.keys():
                        raise ValueError(
                            "Trying to add a sensor key before the sensor mapping."
                        )
                    valuetmp = np.empty((nf, nt))
                    valuetmp[:] = np.nan
                    loc = np.asarray(sens_conf == key).nonzero()  # faster than np.where
                    for fr in range(nf):
                        valuetmp[fr, loc] = main_data[fr, loc]
                    values = valuetmp
                    coords = [
                        ("frequency", hfr_frequency, {"units": self.frequencies.unit}),
                        ("time", sweep_times.value),
                    ]
                    dims = ["frequency", "time"]
                    units_da = units
                else:
                    raise KeyError("Unknown key.")

                V_da = xarray.DataArray(
                    values,
                    coords=coords,
                    # dims=["channel", "time", "frequency"],
                    dims=dims,
                    attrs={"units": units_da},
                    name=key,
                )
                dataset[key] = V_da
                if firstloop == 1:
                    V_ds = xarray.Dataset(data_vars=dataset)
                    firstloop = 0
                else:
                    V_ds[key] = dataset[key]

        return V_ds  # xarray.Dataset({"VOLTAGE_SPECTRAL_POWER": V_da})

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = [
            "VOLTAGE_SPECTRAL_POWER",
            "VOLTAGE_SPECTRAL_POWER_CH1",
            "VOLTAGE_SPECTRAL_POWER_CH2",
            "DELTA_TIMES",
            "FREQ_INDICES",
        ],
        # db: List[bool] = [True, True, True, False, False],
        **kwargs
    ):
        import numpy

        default_keys = [
            "VOLTAGE_SPECTRAL_POWER",
            "VOLTAGE_SPECTRAL_POWER_CH1",
            "VOLTAGE_SPECTRAL_POWER_CH2",
            "DELTA_TIMES",
            "FREQ_INDICES",
        ]
        forbidden_keys = ["SENSOR", "CHANNEL"]
        db_tab = numpy.array([True, True, True, False, False])
        for qkey, tab in zip(["db"], [db_tab]):
            if qkey not in kwargs:
                qkey_tab = []
                for key in keys:
                    if key in forbidden_keys:
                        raise KeyError("Key: " + str(key) + " is not supported.")
                    if key in default_keys:
                        qkey_tab.append(
                            tab[numpy.where(key == numpy.array(default_keys))][0]
                        )
                    else:
                        qkey_tab.append(None)
                kwargs[qkey] = list(qkey_tab)
        self._quicklook(keys=keys, file_png=file_png, **kwargs)
