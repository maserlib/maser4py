# -*- coding: utf-8 -*-
from typing import Union

from maser.data.base import BinData, Sweeps, Records
from maser.data.base.sweeps import Sweep
from .kronos import fi_freq, ti_datetime, t97_datetime

from astropy.units import Unit
from astropy.time import Time
import numpy
import json
from pathlib import Path


KRONOS_LEVEL_FORMAT_JSON_FILE = Path(__file__).parent / "kronos_level_format.json"

with open(KRONOS_LEVEL_FORMAT_JSON_FILE, "r") as f:
    kronos_level_format = json.load(f)


class CoRpwsHfrKronosDataSweep(Sweep):
    def __init__(self, header, data):
        super().__init__(header, data)
        self._frequencies = header["frequencies"]
        self._time = header["time"]


class CoRpwsHfrKronosDataSweeps(Sweeps):
    @property
    def generator(self):
        for f, t, sweep_mask in zip(
            self.data_reference.frequencies,
            self.data_reference.times,
            self.data_reference._sweep_masks,
        ):
            yield CoRpwsHfrKronosDataSweep(
                {
                    "frequencies": f,
                    "time": t,
                    "level": self.data_reference.level,
                    "file": self.data_reference.filepath.name,
                },
                self.data_reference._data[sweep_mask],
            )


class CoRpwsHfrKronosDataRecords(Records):
    @property
    def generator(self):
        for i in range(self.data_reference._nrecord):
            yield self.data_reference._data[i]


class CoRpwsHfrKronosData(BinData, dataset="co_rpws_hfr_kronos"):

    _iter_sweep_class = CoRpwsHfrKronosDataSweeps
    _iter_record_class = CoRpwsHfrKronosDataRecords

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        super().__init__(
            filepath,
            dataset,
            access_mode,
            fixed_frequencies=False,
        )
        self.level = self.dataset[19:]
        self._data = self.read_data_binary()
        self._sweep_masks = None
        self.__max_frequencies_len = None
        self._nrecord = len(self._data)
        self._nsweep = len(self.sweep_masks)

    @property
    def _format(self):
        return kronos_level_format[self.level]

    def read_data_binary(self):
        file_size = self.file_size
        rec_size = self._format["record_def"]["length"]
        dtype = list(
            zip(
                self._format["record_def"]["fields"],
                self._format["record_def"]["np_dtype"],
            )
        )
        if file_size % rec_size != 0:
            raise IOError("Corrupted file...")

        data = numpy.fromfile(
            self.filepath,
            dtype=dtype,
        )
        return data

    @property
    def sweep_masks(self):
        if self._sweep_masks is None:
            if self.level == "n1":
                tvar = "ti"
            else:
                tvar = "t97"
            sweep_masks = []
            t_values = numpy.unique(self._data[tvar])
            for t in t_values:
                sweep_masks.append(self._data[tvar] == t)
            self._sweep_masks = sweep_masks
        return self._sweep_masks

    def __len__(self):
        if self.access_mode == "sweeps":
            return self._nsweep
        elif self.access_mode == "records":
            return self._nrecord
        else:
            return self.file_size

    @property
    def _decode_times(self):
        return []

    @property
    def times(self):
        if self._times is None:
            times = self._decode_times
            if self.access_mode == "records":
                self._times = times
            elif self.access_mode == "sweeps":
                self._times = Time([times[mask][0] for mask in self.sweep_masks])
        return self._times

    @property
    def _decode_frequencies(self):
        return []

    @property
    def frequencies(self):
        if self._frequencies is None:
            f = self._decode_frequencies
            if self.access_mode == "records":
                self._frequencies = f
            if self.access_mode == "sweeps":
                self._frequencies = [f[mask] for mask in self.sweep_masks]
        return self._frequencies

    @property
    def _max_frequencies_len(self):
        if self.__max_frequencies_len is None:
            self.__max_frequencies_len = numpy.max(
                [numpy.count_nonzero(mask) for mask in self.sweep_masks]
            )
        return self.__max_frequencies_len

    def as_xarray(self):
        import xarray

        freq_arr = numpy.full((self._nsweep, self._max_frequencies_len), numpy.nan)
        for i in range(self._nsweep):
            f = self.frequencies[i].value
            freq_arr[i, : len(f)] = f

        freq_index = range(self._max_frequencies_len)

        datasets = {}
        for dataset_key in self._format["record_def"]["fields"]:
            data_arr = numpy.full((self._nsweep, self._max_frequencies_len), numpy.nan)
            for i, sweep in enumerate(self.sweeps):
                d = sweep.data[dataset_key]
                data_arr[i, : len(d)] = d
            datasets[dataset_key] = xarray.DataArray(
                data=data_arr,
                name=dataset_key,
                coords={
                    "freq_index": freq_index,
                    "time": self.times.to_datetime(),
                    "frequency": (["time", "freq_index"], freq_arr),
                },
                dims=("time", "freq_index"),
            )

        return datasets


class CoRpwsHfrKronosN1Data(CoRpwsHfrKronosData, dataset="co_rpws_hfr_kronos_n1"):
    @property
    def _decode_times(self):
        return Time(
            list(
                map(
                    ti_datetime,
                    self._data["ti"],  # time index (YYDDDSSSSS) with YY = YYYY - 1996
                    self._data["c"],  # centiseconds
                )
            )
        )

    @property
    def _decode_frequencies(self):
        return numpy.array(list(map(fi_freq, self._data["fi"]))) * Unit("kHz")


class CoRpwsHfrKronosN2Data(CoRpwsHfrKronosData, dataset="co_rpws_hfr_kronos_n2"):
    @property
    def _decode_times(self):
        return Time(list(map(t97_datetime, self._data["t97"])))

    @property
    def _decode_frequencies(self):
        return self._data["f"] * Unit("kHz")
