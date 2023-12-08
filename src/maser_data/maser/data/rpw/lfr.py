# -*- coding: utf-8 -*-
from maser.data.base import CdfData

from astropy.time import Time, TimeDelta
from astropy.units import Unit
from maser.data.base.sweeps import Sweeps
import numpy

from typing import Union, List
from pathlib import Path


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
                self.data_reference.times,  # [frequency_band],
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

    """
    keys used to loop over F0, F1, F2 frequency ranges and Burst/Normal modes
    Freq are sorted in "theoretical" sweep start time order,
    but the method can handle any order.
    """
    # frequency_band_labels = ["N_F2", "B_F1", "N_F1", "B_F0", "N_F0"]
    frequency_band_labels = ["N_F0", "B_F0", "N_F1", "B_F1", "N_F2"]
    _multiple_mode = None

    _dataset_keys = [
        "PE",
        "PB",
        "DOP",
        "ELLIP",
        "SX_REA",
        "DELTA_TIMES",
        "MODE_NB",
    ]

    @property
    def multiple_mode(self):
        if self._multiple_mode is None:
            NBmode = ""
            with self.open(self.filepath) as cdf_file:
                for frequency_band in self.frequency_band_labels:
                    frequencies = cdf_file[frequency_band][...]
                    if len(frequencies) == 0:
                        continue
                    else:
                        if "N" in frequency_band:
                            if "N" not in NBmode:
                                NBmode += "N"
                        elif "B" in frequency_band:
                            if "B" not in NBmode:
                                NBmode += "B"
            if "N" in NBmode and "B" in NBmode:
                self._multiple_mode = 1
            else:
                self._multiple_mode = 0
        return self._multiple_mode

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
            self._times = Time([], format="jd")
            self._delta_times = {}
            timesbymode = {}
            truetimesbyfreq = {}
            timesbyfreq = {}
            NBtable = {"B": [], "N": []}
            NBdone = ""
            with self.open(self.filepath) as cdf_file:
                for frequency_band in self.frequency_band_labels:
                    if len(cdf_file[f"Epoch_{frequency_band}"][...]) == 0:
                        tmp = cdf_file[f"Epoch_{frequency_band}"][...]
                        # Sometimes some bands are not recorded and not present in a file
                        # continue
                    else:
                        # Dealing with different times between Burst and Normal modes to combine them
                        if "B" in frequency_band:
                            NBmode = "B"
                        else:
                            NBmode = "N"
                        # Filling arrays for delta_times
                        truetimesbyfreq[frequency_band] = Time(
                            cdf_file[f"Epoch_{frequency_band}"][...]
                        )
                        # Filling temporary array with time values from B and N modes
                        if NBmode not in NBdone:
                            NBdone += NBmode
                            timesbymode[NBmode] = Time(
                                cdf_file[f"Epoch_{frequency_band}"][...]
                            )
                            # Filling temporary array with time values for as_xarray times
                            timesbyfreq[frequency_band] = Time(
                                cdf_file[f"Epoch_{frequency_band}"][...]
                            )
                        else:
                            # Checking the dimensions are the same

                            # The same tests as the proper ones (next section) are applied reversed to as_xarray times
                            # In case new time series starts after - take only the later part
                            if timesbymode[NBmode][0] - Time(
                                cdf_file[f"Epoch_{frequency_band}"][...]
                            )[0] < TimeDelta(-0.1 * Unit("s")):
                                nstart = 1
                                truetimesbyfreq[frequency_band] = Time(
                                    numpy.append(
                                        timesbymode[NBmode][0],
                                        truetimesbyfreq[frequency_band],
                                    )
                                )  # .sort()
                            else:
                                nstart = 0
                            # In case new time series ends earlier
                            if timesbymode[NBmode][-1] - Time(
                                cdf_file[f"Epoch_{frequency_band}"][...]
                            )[-1] > TimeDelta(0.1 * Unit("s")):
                                timesbyfreq[frequency_band] = timesbymode[NBmode][
                                    nstart:-1
                                ]
                                truetimesbyfreq[frequency_band] = Time(
                                    numpy.append(
                                        truetimesbyfreq[frequency_band],
                                        timesbymode[NBmode][-1],
                                    )
                                )  # .sort()
                            else:
                                timesbyfreq[frequency_band] = timesbymode[NBmode][
                                    nstart:
                                ]

                            # In case new time series starts before ### Should only happen if the cutting time between two files is in the middle of a sweep ###
                            if timesbymode[NBmode][0] - Time(
                                cdf_file[f"Epoch_{frequency_band}"][...]
                            )[0] > TimeDelta(0.1 * Unit("s")):
                                timesbymode[NBmode] = Time(
                                    numpy.append(
                                        Time(
                                            cdf_file[f"Epoch_{frequency_band}"][...][0]
                                        ),
                                        timesbymode[NBmode],
                                    )
                                )  # .sort()
                                timesbyfreq[frequency_band] = Time(
                                    numpy.append(
                                        Time(
                                            cdf_file[f"Epoch_{frequency_band}"][...][0]
                                        ),
                                        timesbyfreq[frequency_band],
                                    )
                                )  # .sort()
                                for freq in NBtable[NBmode]:
                                    truetimesbyfreq[freq] = Time(
                                        numpy.append(
                                            Time(
                                                cdf_file[f"Epoch_{frequency_band}"][
                                                    ...
                                                ][0]
                                            ),
                                            truetimesbyfreq[freq],
                                        )
                                    )  # .sort()
                                # print('Adding earlier time')
                            # In case new time series ends later
                            if timesbymode[NBmode][-1] - Time(
                                cdf_file[f"Epoch_{frequency_band}"][...]
                            )[-1] < TimeDelta(-0.1 * Unit("s")):
                                timesbymode[NBmode] = Time(
                                    numpy.append(
                                        timesbymode[NBmode],
                                        Time(
                                            cdf_file[f"Epoch_{frequency_band}"][...][-1]
                                        ),
                                    )
                                )  # .sort()
                                timesbyfreq[frequency_band] = Time(
                                    numpy.append(
                                        timesbyfreq[frequency_band],
                                        Time(
                                            cdf_file[f"Epoch_{frequency_band}"][...][-1]
                                        ),
                                    )
                                )  # .sort()
                                for freq in NBtable[NBmode]:
                                    truetimesbyfreq[freq] = Time(
                                        numpy.append(
                                            truetimesbyfreq[freq],
                                            Time(
                                                cdf_file[f"Epoch_{frequency_band}"][
                                                    ...
                                                ][-1]
                                            ),
                                        )
                                    )  # .sort()
                                # print('Adding later time')
                        NBtable[NBmode].append(frequency_band)
            if "N" in NBdone and "B" in NBdone:
                # If the file has both Normal and Burst mode, combine the times
                self._times = Time(
                    numpy.append(timesbymode["N"], timesbymode["B"])
                ).sort()
                for freq in NBtable["B"]:
                    truetimesbyfreq[freq] = Time(
                        numpy.append(truetimesbyfreq[freq], timesbymode["N"])
                    ).sort()
                    self._delta_times[freq] = truetimesbyfreq[freq] - self._times
                for freq in NBtable["N"]:
                    truetimesbyfreq[freq] = Time(
                        numpy.append(truetimesbyfreq[freq], timesbymode["B"])
                    ).sort()
                    self._delta_times[freq] = truetimesbyfreq[freq] - self._times
            elif NBdone == "":
                self._times = tmp
                truetimesbyfreq = tmp
            else:
                self._times = timesbymode[NBdone]
                for freq in NBtable[NBdone]:
                    self._delta_times[freq] = truetimesbyfreq[freq] - self._times
            self.times_per_frequency = timesbyfreq
        return self._times.sort()

    @property
    def delta_times(self):
        if self._delta_times is None:
            times = self.times
            for band in self._delta_times.keys():
                if len(self._delta_times[band]) != len(times):
                    raise ValueError("Conflict in Time object dimensions.")
                """
                self._delta_times = {}
                deltatmp = {}
                for frequency_band in self.frequency_band_labels:
                    deltatmp[frequency_band] = self.times
                with self.open(self.filepath) as cdf_file:
                    for frequency_band in self.frequency_band_labels:
                        dttemp = cdf_file[f"Epoch_{frequency_band}"][...]
                        if len(dttemp) == 0:
                            self._delta_times[frequency_band] = Time(dttemp)
                        else:
                            self._delta_times[frequency_band] = Time(dttemp) - self.times
                """
        return self._delta_times

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def as_xarray(self):
        import xarray

        dataset = {
            "PE": {},
            "PB": {},
            "DOP": {},
            "ELLIP": {},
            "SX_REA": {},
            "DELTA_TIMES": {},
            "MODE_NB": {},
        }

        datasets = {}
        firstdataset = 1
        firstbandN = 1
        firstbandB = 1

        default_units = {"PB": "nT^2/Hz"}

        deltatimes = self.delta_times

        for dataset_key in dataset:
            if firstbandN == 0 or firstbandB == 0:
                firstdataset = 0
            firstbandN = 1
            firstbandB = 1
            for frequency_band in self.frequency_band_labels:
                frequencies = self.file[frequency_band][...]
                if len(frequencies) == 0:
                    continue

                if firstbandN == 1 and firstbandB == 1 and firstdataset == 1:
                    # force lower keys for frequency and time attributes
                    time_attrs = {
                        k.lower(): v
                        for k, v in self.file[f"Epoch_{frequency_band}"].attrs.items()
                    }

                    frequency_attrs = {
                        k.lower(): v for k, v in self.file[frequency_band].attrs.items()
                    }

                    # modification of the attrs to make them frequency_band independant
                    # frequency_attrs['fieldnam'] = frequency_attrs['fieldnam'][:20] for old version of the data
                    frequency_attrs["fieldnam"] = "Frequency"
                    frequency_attrs["catdesc"] = frequency_attrs["catdesc"][:-20]
                    # frequency_attrs['lablaxis'] = 'S'+frequency_attrs['lablaxis'][5:]
                    time_attrs["fieldnam"] = time_attrs["fieldnam"][:5]
                    time_attrs["catdesc"] = time_attrs["catdesc"][:4]
                    time_attrs["lablaxis"] = time_attrs["lablaxis"][:5]

                    if not frequency_attrs["units"].strip():
                        frequency_attrs["units"] = "Hz"

                if dataset_key == "DELTA_TIMES":
                    times = self.times.to_datetime()  # value
                    values = numpy.tile(
                        deltatimes[frequency_band].value, (len(frequencies), 1)
                    ).transpose()
                    attrs = {}
                    attrs["units"] = "jd"
                    attrs["fieldnam"] = "Time shifts between frequency measurements"
                    attrs[
                        "catdesc"
                    ] = "Time difference to reference time for each frequency"
                    attrs["validmin"] = -1e30
                    attrs["validmax"] = 1e30
                    attrs["scalemin"] = -1e30
                    attrs["scalemax"] = 1e30
                    attrs["lablaxis"] = "DELTA_TIMES"
                    attrs["var_types"] = "support_data"
                    attrs["var_notes"] = "Extracted from Epochs"
                    attrs["format"] = "Astropy.TimeDelta"
                    attrs["scaletype"] = "linear"
                    attrs["display_type"] = "time_series"
                    attrs["fillval"] = -1e31
                    attrs["depend_0"] = "Epoch"

                elif dataset_key == "MODE_NB":
                    times = self.times_per_frequency[
                        frequency_band
                    ].to_datetime()  # value
                    # values = numpy.chararray([len(times),len(frequencies)])
                    values = numpy.zeros([len(times), len(frequencies)])
                    if "N" in frequency_band:
                        mode_nb = 1
                    else:
                        mode_nb = 2
                    values[:] = mode_nb
                    attrs = {}
                    attrs["units"] = "N=1 ; B=2"
                    attrs["fieldnam"] = "Instrument mode: Normal/Burst"
                    attrs["catdesc"] = "Instrument mode between Normal and Burst"
                    attrs["validmin"] = 0
                    attrs["validmax"] = 3
                    attrs["scalemin"] = 0
                    attrs["scalemax"] = 3
                    attrs["lablaxis"] = "Instrument mode"
                    attrs["var_types"] = "support_data"
                    attrs["var_notes"] = "Extracted from data/header"
                    attrs["format"] = "int"
                    attrs["scaletype"] = "linear"
                    attrs["display_type"] = "time_series"
                    attrs["fillval"] = -1
                    attrs["depend_0"] = "Epoch"

                else:
                    times = self.times_per_frequency[
                        frequency_band
                    ].to_datetime()  # value
                    values = self.file[f"{dataset_key}_{frequency_band}"][...]

                    attrs = {
                        k.lower(): v
                        for k, v in self.file[
                            f"{dataset_key}_{frequency_band}"
                        ].attrs.items()
                    }
                    # modification of the attrs to make them frequency_band independant
                    attrs["fieldnam"] = attrs["fieldnam"][
                        :2
                    ]  # [:25] for old version of the data
                    attrs["catdesc"] = attrs["catdesc"][:25]
                    attrs["lablaxis"] = dataset_key
                    attrs["depend_0"] = attrs["depend_0"][:-5]

                    # if units are not defined, use the default ones
                    if not attrs["units"].strip():
                        attrs["units"] = default_units.get(dataset_key, "")

                data_array = xarray.DataArray(
                    values,
                    coords=[
                        ("time", times, time_attrs),
                        ("frequency", frequencies, frequency_attrs),
                    ],
                    attrs=attrs,
                    name=f"{dataset_key}",
                )
                if "N" in frequency_band:  # Filling the Normal DataArray
                    if firstbandN == 1:
                        data_array_concatN = data_array
                        firstbandN = 0
                    else:
                        data_array_concatN = xarray.concat(
                            [data_array_concatN, data_array], "frequency"
                        )
                else:  # Filling the Burst DataArray
                    if firstbandB == 1:
                        data_array_concatB = data_array
                        firstbandB = 0
                    else:
                        data_array_concatB = xarray.concat(
                            [data_array_concatB, data_array], "frequency"
                        )

            # Combining the different DataArrays from the same dataset into the same DataArray
            if firstbandB == 1:
                data_array_concat = data_array_concatN
            elif firstbandN == 1:
                data_array_concat = data_array_concatB
            else:
                if dataset_key == "DELTA_TIMES":
                    data_array_concat = xarray.concat(
                        [data_array_concatN, data_array_concatB], "frequency"
                    )
                else:
                    data_array_concat = xarray.concat(
                        [data_array_concatN, data_array_concatB], "time"
                    )
            datasets[dataset_key] = (
                (data_array_concat.sortby("frequency")).sortby("time")
            ).transpose(
                "frequency", "time"
            )  # .sortby('frequency').sortby('time')

        return xarray.Dataset(data_vars=datasets)

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = [
            "PB",
            "PE",
            "DOP",
            "ELLIP",
            "SX_REA",
            "DELTA_TIMES",
            "MODE_NB",
        ],
        # db=[True, True, False, False, True, False, False],
        # vmax=[-50, -60, 1, 1, 50, 0.2 * 10 ** (-8), 3],
        # vmin=[-100, -130, 0, 0, -50, 0 * 10 ** (-8), 0],
        **kwargs,
    ):
        if self.multiple_mode == 1:
            selection = {
                "select_key": ["MODE_NB", "MODE_NB"],
                "select_value": [1, 2],
                "select_dim": ["frequency", "frequency"],
                "select_how": ["all", "all"],
            }
        else:
            selection = None
        default_keys = [
            "PB",
            "PE",
            "DOP",
            "ELLIP",
            "SX_REA",
            "DELTA_TIMES",
            "MODE_NB",
        ]
        forbidden_keys: List[str] = []
        db_tab = numpy.array([True, True, False, False, True, False, False])
        vmin_tab = numpy.array([-100, -130, 0, 0, -50, 0 * 10 ** (-8), 0])
        vmax_tab = numpy.array([-50, -60, 1, 1, 50, 0.2 * 10 ** (-8), 3])
        for qkey, tab in zip(["db", "vmin", "vmax"], [db_tab, vmin_tab, vmax_tab]):
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
        self._quicklook(
            keys=keys,
            file_png=file_png,
            # db=db,
            # vmin=[0.008,0.006],
            # vmax=vmax,
            # vmin=vmin,
            # vmax=[0.009,0.007],
            iter_on_selection=selection,
            **kwargs,
        )
