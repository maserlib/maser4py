# -*- coding: utf-8 -*-
import numpy as np

from astropy.time import Time
from astropy.units import Unit

from typing import Union, List
from pathlib import Path
from maser.data.base import CdfData
from maser.data.base.sweeps import Sweeps

TNR_SWEEP_DTYPE = [
    ("Epoch", ("datetime64[ns]", 4)),
    ("VOLTAGE_SPECTRAL_POWER1", ("float32", 128)),
    ("VOLTAGE_SPECTRAL_POWER2", ("float32", 128)),
    ("FLUX_DENSITY1", ("float32", 128)),
    ("FLUX_DENSITY2", ("float32", 128)),
    ("MAGNETIC_SPECTRAL_POWER1", ("float32", 128)),
    ("MAGNETIC_SPECTRAL_POWER2", ("float32", 128)),
]


class RpwTnrSurvSweeps(Sweeps):
    @property
    def generator(self):
        """
        For each time, yield a frequency range and a dictionary with the following keys:
        - VOLTAGE_SPECTRAL_POWER1 : Power spectral density at receiver + PA for channel 1 before applying antenna gain (V²/Hz)
        - VOLTAGE_SPECTRAL_POWER2 : Power spectral density at receiver + PA for channel 2 before applying antenna gain (V²/Hz)
        - FLUX_DENSITY1 : Flux of the power spectral density for channel 1 with antenna gain (W/m²/Hz)
        - FLUX_DENSITY2 : Flux of the power spectral density for channel 2 with antenna gain (W/m²/Hz)
        - MAGNETIC_SPECTRAL_POWER1 : Magnetic power spectral density from 1 search coil axis in channel 1
        - MAGNETIC_SPECTRAL_POWER1 : Magnetic power spectral density from 1 search coil axis in channel 2
        """

        def add_rec(in_data, out_data, rec_index):

            # Get frequency band range
            i_band = self.file["TNR_BAND"][rec_index]
            i0, i1 = self.data_reference.frequency_band_indices[i_band]

            # Fill values
            out_data["Epoch"][0, i_band] = in_data["Epoch"][rec_index]
            out_data["VOLTAGE_SPECTRAL_POWER1"][0, i0 : i1 + 1] = in_data["AUTO1"][
                rec_index, :
            ]
            out_data["VOLTAGE_SPECTRAL_POWER2"][0, i0 : i1 + 1] = in_data["AUTO2"][
                rec_index, :
            ]
            out_data["FLUX_DENSITY1"][0, i0 : i1 + 1] = in_data["FLUX_DENSITY1"][
                rec_index, :
            ]
            out_data["FLUX_DENSITY2"][0, i0 : i1 + 1] = in_data["FLUX_DENSITY2"][
                rec_index, :
            ]
            out_data["MAGNETIC_SPECTRAL_POWER1"][0, i0 : i1 + 1] = in_data[
                "MAGNETIC_SPECTRAL_POWER1"
            ][rec_index, :]
            out_data["MAGNETIC_SPECTRAL_POWER2"][0, i0 : i1 + 1] = in_data[
                "MAGNETIC_SPECTRAL_POWER2"
            ][rec_index, :]

            return out_data

        # First build list of frequency values for TNR (A+B+C+D bands)
        freq = self.data_reference.frequencies

        # Initialize output data vector for the first sweep
        sweep_data = np.zeros(1, dtype=TNR_SWEEP_DTYPE)

        # Loop over each record in the CDF
        sweep_completed = False
        for i in range(self.file["SWEEP_NUM"].shape[0]):
            try:
                if self.file["SWEEP_NUM"][i] != self.file["SWEEP_NUM"][i + 1]:
                    sweep_data = add_rec(self.file, sweep_data, i)
                    sweep_completed = True
                    yield (
                        {key: sweep_data[key][...] for key in sweep_data.dtype.names},
                        Time(sweep_data["Epoch"][0, 0]),
                        freq,
                        self.file["SENSOR_CONFIG"][i],
                        self.file["SURVEY_MODE"][i],
                    )
                else:
                    if sweep_completed:
                        sweep_completed = False
                        sweep_data = np.empty(1, dtype=TNR_SWEEP_DTYPE)

                    sweep_data = add_rec(self.file, sweep_data, i)
            except IndexError:
                # End of CDF file is reached, force yield for last record
                yield (
                    {key: sweep_data[key][...] for key in sweep_data.dtype.names},
                    Time(sweep_data["Epoch"][0, 0]),
                    freq,
                    self.file["SENSOR_CONFIG"][i],
                    self.file["SURVEY_MODE"][i],
                )


class RpwTnrSurv(CdfData, dataset="solo_L2_rpw-tnr-surv"):
    _iter_sweep_class = RpwTnrSurvSweeps

    _dataset_keys = [
        "VOLTAGE_SPECTRAL_POWER_CH1",
        "VOLTAGE_SPECTRAL_POWER_CH2",
        "SENSOR_CH1",
        "SENSOR_CH2",
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
    ]

    # Define TNR frequency band names
    frequency_band_labels = ["A", "B", "C", "D"]

    # Define range of indices for each TNR frequency band
    frequency_band_indices = [[0, 31], [32, 63], [64, 95], [96, 127]]

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
                # if units are not specified, assume Hz
                units = Unit(cdf_file["TNR_BAND_FREQ"].attrs["UNITS"].strip() or "Hz")
                self._frequencies = (
                    np.sort(self.file["TNR_BAND_FREQ"][...].flatten()) * units
                )

        return self._frequencies

    @property
    def times(self):
        import xarray

        if self._times is None:
            self._times = Time([], format="jd")
            band = xarray.DataArray(
                [self.frequency_band_labels[idx] for idx in self.file["TNR_BAND"][...]]
            )
            timeref = self.file["Epoch"][...]
            # Get Epoch time values for Band A
            self._times = Time(timeref[np.where(band == self.frequency_band_labels[0])])
            self._delta_times = {}
            for freqband in self.frequency_band_labels:
                self._delta_times[freqband] = (
                    Time(timeref[np.where(band == freqband)]) - self._times
                )
            # mask = self.file["TNR_BAND"][...] == 0
            # self._times = Time(np.take(self.file["Epoch"][...], mask, axis=0))
        return self._times

    @property
    def delta_times(self):
        if self._delta_times is None:
            times = self.times
            for band in self._delta_times.keys():
                if len(self._delta_times[band]) != len(times):
                    raise ValueError("Conflict in Time object dimensions.")
        return self._delta_times

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def as_xarray(self):
        """
        Return the data as a xarray
        """
        import xarray

        dataset_keys = [
            "VOLTAGE_SPECTRAL_POWER_CH1",
            "VOLTAGE_SPECTRAL_POWER_CH2",
            "SENSOR_CH1",
            "SENSOR_CH2",
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

        bandtab = xarray.DataArray(
            [self.frequency_band_labels[idx] for idx in self.file["TNR_BAND"][...]]
        )
        # timeref = self.file["Epoch"][...]

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
        # freq_index = range(tnr_frequency_bands.shape[1])
        freq_index = tnr_frequency_bands.shape[1]

        # band_array_tmp = {}
        # np.zeros([len(self.times), len(self.frequencies)])
        # band_array_2 = np.zeros([len(self.times), len(self.frequencies)])
        # for i in range(2):  # loop on channels

        sensor_config = np.array(sensor_config)
        for i, freqband in enumerate(self.frequency_band_labels):
            # band_array_tmp[freqband+"_"+str(i)] = sensor_config[i][np.where(bandtab==freqband)]
            if i == 0:
                band_array_1 = np.tile(
                    sensor_config[:, 0][np.where(bandtab == freqband)], (freq_index, 1)
                ).transpose()
                band_array_2 = np.tile(
                    sensor_config[:, 1][np.where(bandtab == freqband)], (freq_index, 1)
                ).transpose()
            else:
                band_array_1 = np.append(
                    band_array_1,
                    np.tile(
                        sensor_config[:, 0][np.where(bandtab == freqband)],
                        (freq_index, 1),
                    ).transpose(),
                    axis=1,
                )
                band_array_2 = np.append(
                    band_array_2,
                    np.tile(
                        sensor_config[:, 1][np.where(bandtab == freqband)],
                        (freq_index, 1),
                    ).transpose(),
                    axis=1,
                )

            # istart = 0 + freq_index*i
            # iend = freq_index * (i + 1)
            # band_array_1[:,istart:iend] = sensor_config[0][np.where(bandtab==freqband)]  # chan 1
            # band_array_2[:,istart:iend] = sensor_config[1][np.where(bandtab==freqband)]  # chan 2

        data_1 = self.file["AUTO1"][...]
        data_2 = self.file["AUTO2"][...]
        try:
            fillval = self.file["AUTO1"].attrs["FILLVAL"]
        except KeyError:
            # If FILLVAL not found in variable attribute
            fillval = -1e31
        data_array_1 = (
            np.ones(
                [
                    len(bandtab[np.where(bandtab == "A")]),
                    freq_index * len(self.frequency_band_labels),
                ]
            )
            * fillval
        )
        data_array_2 = (
            np.ones(
                [
                    len(bandtab[np.where(bandtab == "A")]),
                    freq_index * len(self.frequency_band_labels),
                ]
            )
            * fillval
        )
        for i, freqband in enumerate(self.frequency_band_labels):
            for j in range(freq_index):
                # cond = bandtab==freqband
                data_array_1[:, j + i * freq_index] = data_1[:, j][
                    np.where(bandtab == freqband)
                ]
                data_array_2[:, j + i * freq_index] = data_2[:, j][
                    np.where(bandtab == freqband)
                ]

        # frequency = self.file["FREQUENCY"][...]  # (n_time, n_freq)

        for i, freqband in enumerate(self.frequency_band_labels):
            if i == 0:
                deltatimes = np.tile(
                    self.delta_times[freqband].value, (freq_index, 1)
                ).transpose()
            else:
                deltatimes = np.append(
                    deltatimes,
                    np.tile(
                        self.delta_times[freqband].value, (freq_index, 1)
                    ).transpose(),
                    axis=1,
                )

        try:
            unit_data = self.file["AUTO1"].attrs["UNITS"]
        except KeyError:
            # If UNITS not found in variable attribute
            # assume V^2/Hz
            unit_data = "V^2/Hz"

        """
        dataset_keys = [
            "VOLTAGE_SPECTRAL_POWER_CH1",
            "VOLTAGE_SPECTRAL_POWER_CH2",
            "SENSOR_CH1",
            "SENSOR_CH2",
            "DELTA_TIMES",
        ]
        """
        dataset = {}
        firstloop = 1
        for key in dataset_keys:
            if key == "VOLTAGE_SPECTRAL_POWER_CH1":
                values = data_array_1.T
                units = unit_data
            elif key == "VOLTAGE_SPECTRAL_POWER_CH2":
                values = data_array_2.T
                units = unit_data
            elif key == "SENSOR_CH1":
                values = band_array_1.T
                units = ""
            elif key == "SENSOR_CH2":
                values = band_array_2.T
                units = ""
            elif key == "DELTA_TIMES":
                values = deltatimes.T
                units = "jd"
            elif key in sensor_keys:
                valuetmp = np.empty(data_array_1.T.shape)
                valuetmp[:] = np.nan
                # faster than np.where
                loc1 = np.asarray(band_array_1.T == key).nonzero()
                loc2 = np.asarray(band_array_2.T == key).nonzero()
                valuetmp[loc1] = data_array_1.T[loc1]
                valuetmp[loc2] = data_array_2.T[loc2]
                values = valuetmp
                units = unit_data
            else:
                raise KeyError("Unknown key.")

            dataset[key] = xarray.DataArray(
                values,  # [self.file["AUTO1"][...], self.file["AUTO2"][...]],
                coords=[
                    # "channel": self.channel_labels,
                    (
                        "frequency",
                        self.frequencies.value,
                        {"units": self.frequencies.unit},
                    ),  # (["time", "freq_index"], frequency.data),
                    ("time", self.times.to_datetime()),  # timeref,
                    # "freq_index": freq_index,
                    # "band": ("time", bandtab.data),
                    # "sensor": (["time", "channel"], sensor_config),
                ],
                dims=["frequency", "time"],  # ["channel", "time", "freq_index"],
                attrs={"units": units},
                name=key,  # "VOLTAGE_SPECTRAL_POWER",
            )
            if firstloop == 1:
                ds = xarray.Dataset(data_vars=dataset)
                firstloop = 0
            else:
                ds[key] = dataset[key]

        return ds  # xarray.Dataset({"VOLTAGE_SPECTRAL_POWER": auto})

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = [
            "VOLTAGE_SPECTRAL_POWER_CH1",
            "VOLTAGE_SPECTRAL_POWER_CH2",
            "DELTA_TIMES",
        ],
        # db: List[bool] = [True, True, False],
        # vmin: List[Union[float, None]] = [None, None, -2e-5],
        # vmax: List[Union[float, None]] = [None, None, 2e-5],
        yscale: str = "log",
        **kwargs
    ):
        default_keys = [
            "VOLTAGE_SPECTRAL_POWER_CH1",
            "VOLTAGE_SPECTRAL_POWER_CH2",
            "DELTA_TIMES",
        ]
        forbidden_keys = ["SENSOR_CH1", "SENSOR_CH2"]
        db_tab = np.array([True, True, False])
        vmin_tab = np.array([None, None, -2e-5])
        vmax_tab = np.array([None, None, 2e-5])
        for qkey, tab in zip(["db", "vmin", "vmax"], [db_tab, vmin_tab, vmax_tab]):
            if qkey not in kwargs:
                qkey_tab = []
                for key in keys:
                    if key in forbidden_keys:
                        raise KeyError("Key: " + str(key) + " is not supported.")
                    if key in default_keys:
                        qkey_tab.append(tab[np.where(key == np.array(default_keys))][0])
                    else:
                        qkey_tab.append(None)
                kwargs[qkey] = list(qkey_tab)
        self._quicklook(
            keys=keys,
            file_png=file_png,
            # db=db,
            # vmin=vmin,
            # vmax=vmax,
            yscale=yscale,
            **kwargs
        )
