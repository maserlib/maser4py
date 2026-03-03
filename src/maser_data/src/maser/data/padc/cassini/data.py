# -*- coding: utf-8 -*-

"""
Classes for Cassini datasets.
"""
from typing import Iterable, Union, List, Any

from maser.data.base import Data, BinData, Sweeps, Records, VariableFrequencies
from maser.data.base.sweeps import Sweep
from .kronos import fi_freq, ti_datetime, t97_datetime

from astropy.units import Unit
from astropy.time import Time
import numpy
import numpy.typing
import json
import math
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


class CoRpwsHfrKronosFixedFrequencyDataSweeps(Sweeps):
    @property
    def generator(self):
        for t in self.data_reference.times:
            yield CoRpwsHfrKronosDataSweep(
                {
                    "frequencies": self.data_reference.frequencies,
                    "time": t,
                    "level": self.data_reference.level,
                    "file": self.data_reference.filepath.name,
                },
                self.data_reference._data,
            )


class CoRpwsHfrKronosDataRecords(Records):
    @property
    def generator(self):
        for i in range(self.data_reference._nrecord):
            yield self.data_reference._data[i]


class CoRpwsHfrKronosData(BinData, dataset="co_rpws_hfr_kronos"):
    _static_period_times = {
        "Turn_on": ("1997298", "1997299"),
        "Venus1": ("1998116", "1998116"),
        "Ico_m14": ("1998364", "1999005"),
        "Venus2": ("1999175", "1999175"),
        "Earth": ("1999227", "1999257"),
    }

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        BinData.__init__(self, filepath, dataset, access_mode)
        self.__format = None
        self.level = self.dataset[19:]
        self._data = self.read_data_binary()
        self._depend_datasets: Iterable[str] = []
        self._dataset_keys = self._format["vars"].keys()
        self.units = [self._format["vars"][field][1] for field in self._dataset_keys]

    @property
    def period_name(self):
        return self.filepath.parents[1].name

    @property
    def _period_times(self) -> tuple:
        if self.period_name in self._static_period_times:
            return self._static_period_times[self.period_name]
        else:
            from calendar import isleap

            yyyy, ddb, dde = self.period_name.split("_")
            if dde == "366":
                if not isleap(int(yyyy)):
                    dde = "365"
            return f"{yyyy}{ddb}", f"{yyyy}{dde}"

    @property
    def _format(self):
        if self.__format is None:
            format_data = kronos_level_format[self.level]
            self.__format = {"length": format_data["record_def"]["length"], "vars": {}}
            for key, dtype, unit in zip(
                format_data["record_def"]["fields"],
                format_data["record_def"]["np_dtype"],
                format_data["record_def"]["units"],
            ):
                if isinstance(dtype, list):
                    self.__format["vars"][key] = (tuple(dtype), unit)
                else:
                    self.__format["vars"][key] = (dtype, unit)
        return self.__format

    def read_data_binary(self):
        file_size = self.file_size.value

        # size of 1 record of the structure:
        dtype = [
            (key, self._format["vars"][key][0]) for key in self._format["vars"].keys()
        ]
        rec_size = numpy.dtype(dtype).itemsize

        # assert rec_size == self._format["length"]

        if file_size % rec_size != 0:
            raise IOError("Corrupted file...")

        # opening binary data file:
        # (swapping byte order if CPU is big endian)
        data = numpy.memmap(
            self.filepath,
            dtype=dtype,
            mode="r",
        )
        return data

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def as_xarray(self):
        import xarray

        units = self.units

        dataset_keys = self._dataset_keys
        data_vars = {}
        for key, unit in zip(dataset_keys, units):
            data_vars[key] = (
                ["frequency"],
                self._data[key][...].T,
                {
                    "units": unit,
                },
            )

        datasets = xarray.Dataset(
            data_vars=data_vars,
            coords={
                "frequency": (
                    ["frequency"],
                    self.frequencies.value,
                    {"units": self.frequencies.unit},
                ),
            },
        ).sortby("frequency")
        # for key in dataset_keys:
        #    datasets[key] = datasets[key].where(datasets[key] != self.file[key].attrs["FILLVAL"])
        return datasets


class CoRpwsHfrKronosNxData(VariableFrequencies, CoRpwsHfrKronosData, dataset="co_rpws_hfr_kronos_nx"):  # type: ignore
    _iter_sweep_class = CoRpwsHfrKronosDataSweeps
    _iter_record_class = CoRpwsHfrKronosDataRecords

    _dataset_keys = None

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        VariableFrequencies.__init__(self)
        CoRpwsHfrKronosData.__init__(self, filepath, dataset, access_mode)
        self._levels = None
        self._nrecord = len(self._data)
        self._nsweep = len(self.sweep_masks)

    @property
    def _ydh(self):
        return self.filepath.name[-10:]

    def _filepath_to_level(self, level):
        switcher = {
            "n1": self.filepath.parents[1] / "n1" / f"R{self._ydh}",
            "n2": self.filepath.parents[1] / "n2" / f"P{self._ydh}",
        }
        if level not in switcher.keys():
            raise ValueError()
        return switcher[level]

    def levels(self, level):
        if self._levels is None:
            self._levels = {level: Data(self._filepath_to_level(level))}
        elif level not in self._levels.keys():
            self._levels[level] = Data(self._filepath_to_level(level))

        return self._levels[level]

    @property
    def sweep_masks(self):
        if self._sweep_masks is None:
            if self.level == "n1":
                # If level=n1: time is encoded in 'ti' (time index)
                tvar = self._data["ti"]
            elif self.level == "n2":
                # If level=n1: time is provided in 't97' (days of 1997; t97=1 <=> 1997-01-01)
                tvar = self._data["t97"]
            else:
                # for upper data levels, use n2['t97'] and filter with data['num'] indices
                tvar = (self.levels("n2")._data["t97"])[self._data["num"]]
            sweep_masks = []
            t_values = numpy.unique(tvar)
            for t in t_values:
                sweep_masks.append(tvar == t)
            self._sweep_masks = sweep_masks
        return self._sweep_masks

    @property
    def sweep_mode_masks(self):
        if self._sweep_mode_masks is None:
            sweep_mode_masks = []
            mode_hashes = numpy.array(
                [hash(item.to_string()) for item in self.frequencies]
            )
            for mode_hash in numpy.unique(mode_hashes):
                sweep_mode_masks.append(mode_hashes == mode_hash)
            self._sweep_mode_masks = sweep_mode_masks
        return self._sweep_mode_masks

    @property
    def max_sweep_length(self):
        if self._max_sweep_length is None:
            self._max_sweep_length = numpy.max(
                [numpy.count_nonzero(mask) for mask in self.sweep_masks]
            )
        return self._max_sweep_length

    def __len__(self):
        if self.access_mode == "sweeps":
            return self._nsweep
        elif self.access_mode == "records":
            return self._nrecord
        else:
            return int(self.file_size.value)

    def _decode_times(self) -> Time:  # pragma: no cover
        pass

    @property
    def times(self):
        if self._times is None:
            self._times = Time([], format="jd")
            times = self._decode_times()
            if self.access_mode == "records":
                self._times = times
            elif self.access_mode == "sweeps":
                self._times = Time([times[mask][0] for mask in self.sweep_masks])
        return self._times

    def _decode_frequencies(self) -> numpy.typing.NDArray[Any]:  # pragma: no cover
        return numpy.array([])  # pass

    @property
    def frequencies(self):
        if self._frequencies is None:
            self._frequencies_ = self._decode_frequencies()
            if self.access_mode == "records":
                self._frequencies = self._frequencies_
            if self.access_mode == "sweeps":
                self._frequencies = [
                    self._frequencies_[mask] for mask in self.sweep_masks
                ]
        return self._frequencies

    def epncore(self):
        md = BinData.epncore(self)
        md["obs_id"] = f"K{self._ydh}"
        md["instrument_host_name"] = "cassini-orbiter"
        md["instrument_name"] = "rpws"
        md["target_name"] = "Saturn"
        md["target_class"] = "planet"
        md["target_region"] = "magnetosphere"
        md["feature_name"] = "SKR#Saturn Auroral Kilometric Radiation"

        md["dataproduct_type"] = "ds"

        md["spectral_range_min"] = min(
            [min(freqs.to("Hz").value) for freqs in self.frequencies]
        )
        md["spectral_range_max"] = max(
            [max(freqs.to("Hz").value) for freqs in self.frequencies]
        )

        md["publisher"] = "PADC"
        return md


class CoRpwsHfrKronosN1Data(CoRpwsHfrKronosNxData, dataset="co_rpws_hfr_kronos_n1"):  # type: ignore
    def _decode_times(self) -> Time:
        return Time(
            list(
                map(
                    ti_datetime,
                    self._data["ti"],  # time index (YYDDDSSSSS) with YY = YYYY - 1996
                    self._data["c"],  # centiseconds
                )
            )
        )

    def _decode_frequencies(self):
        return numpy.array(list(map(fi_freq, self._data["fi"]))) * Unit("kHz")

    def quicklook(
        self,
        file_png=None,
        keys: List[str] = ["agc1", "auto1", "agc2", "auto2", "cross1", "cross2"],
        **kwargs,
    ):
        default_keys = ["agc1", "auto1", "agc2", "auto2", "cross1", "cross2"]
        vmin_tab = numpy.array([0, 128, 0, 128, -255, -255])
        vmax_tab = numpy.array([127, 191, 127, 191, 255, 255])
        for qkey, tab in zip(["vmin", "vmax"], [vmin_tab, vmax_tab]):
            if qkey not in kwargs:
                qkey_tab = []
                for key in keys:
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
            # vmax=[127, 191, 127, 191, 255, 255],
            # vmin=[0, 128, 0, 128, -255, -255],
            **kwargs,
        )


class CoRpwsHfrKronosN2Data(CoRpwsHfrKronosNxData, dataset="co_rpws_hfr_kronos_n2"):  # type: ignore
    def _decode_times(self) -> Time:
        return Time(list(map(t97_datetime, self._data["t97"])))

    def _decode_frequencies(self):
        return self._data["f"] * Unit("kHz")

    def quicklook(
        self,
        file_png=None,
        keys: List[str] = ["autoX", "autoZ", "crossR", "crossI"],
        yscale: str = "log",
        **kwargs,
    ):
        default_keys = ["autoX", "autoZ", "crossR", "crossI"]
        db_tab = numpy.array([True, True, False, False])
        for qkey, tab in zip(["db"], [db_tab]):
            if qkey not in kwargs:
                qkey_tab = []
                for key in keys:
                    if key in default_keys:
                        qkey_tab.append(
                            tab[numpy.where(key == numpy.array(default_keys))][0]
                        )
                    else:
                        qkey_tab.append(None)
                kwargs[qkey] = list(qkey_tab)
        self._quicklook(
            keys=keys,
            # db=[True, True, False, False],
            file_png=file_png,
            y="frequency",
            yscale=yscale,
            **kwargs,
        )


class CoRpwsHfrKronosN3Data(CoRpwsHfrKronosNxData, dataset="co_rpws_hfr_kronos_n3"):  # type: ignore
    def _decode_times(self) -> Time:
        return Time(
            list(map(t97_datetime, (self.levels("n2")._data["t97"])[self._data["num"]]))
        )

    def _decode_frequencies(self):
        return (self.levels("n2")._data["f"])[self._data["num"]] * Unit("kHz")


class CoRpwsHfrKronosN3eData(CoRpwsHfrKronosN3Data, dataset="co_rpws_hfr_kronos_n3e"):  # type: ignore
    def quicklook(
        self,
        file_png=None,
        keys: List[str] = ["s", "v", "th", "ph", "snx", "snz"],
        yscale: str = "log",
        **kwargs,
    ):
        default_keys = ["s", "v", "th", "ph", "snx", "snz"]
        db_tab = numpy.array([True, False, False, False, True, True])
        vmin_tab = numpy.array([-160, -1, 0, -math.pi, 10, 10])
        vmax_tab = numpy.array([-120, 1, math.pi, math.pi, 40, 40])
        for qkey, tab in zip(["db", "vmin", "vmax"], [db_tab, vmin_tab, vmax_tab]):
            if qkey not in kwargs:
                qkey_tab = []
                for key in keys:
                    if key in default_keys:
                        qkey_tab.append(
                            tab[numpy.where(key == numpy.array(default_keys))][0]
                        )
                    else:
                        qkey_tab.append(None)
                kwargs[qkey] = list(qkey_tab)
        self._quicklook(
            keys=keys,
            # db=[True, False, False, False, True, True],
            file_png=file_png,
            y="frequency",
            yscale=yscale,
            # vmin=[-160, -1, 0, -math.pi, 10, 10],
            # vmax=[-120, 1, math.pi, math.pi, 40, 40],
            **kwargs,
        )


class CoRpwsHfrKronosN3dData(CoRpwsHfrKronosN3Data, dataset="co_rpws_hfr_kronos_n3d"):  # type: ignore
    def quicklook(
        self,
        file_png=None,
        keys: List[str] = ["s", "q", "u", "v", "snx", "snz"],
        yscale: str = "log",
        **kwargs,
    ):
        default_keys = ["s", "q", "u", "v", "snx", "snz"]
        db_tab = numpy.array([True, False, False, False, True, True])
        vmin_tab = numpy.array([-160, -1, -1, -1, 10, 10])
        vmax_tab = numpy.array([-120, 1, 1, 1, 40, 40])
        for qkey, tab in zip(["db", "vmin", "vmax"], [db_tab, vmin_tab, vmax_tab]):
            if qkey not in kwargs:
                qkey_tab = []
                for key in keys:
                    if key in default_keys:
                        qkey_tab.append(
                            tab[numpy.where(key == numpy.array(default_keys))][0]
                        )
                    else:
                        qkey_tab.append(None)
                kwargs[qkey] = list(qkey_tab)
        self._quicklook(
            keys=keys,
            # db=[True, False, False, False, True, True],
            file_png=file_png,
            y="frequency",
            yscale=yscale,
            # vmin=[-160, -1, -1, -1, 10, 10],
            # vmax=[-120, 1, 1, 1, 40, 40],
            **kwargs,
        )


class CoRpwsHfrKronosBgData(CoRpwsHfrKronosData, dataset="co_rpws_hfr_kronos_bg"):
    _iter_sweep_class = CoRpwsHfrKronosFixedFrequencyDataSweeps
    _iter_record_class = CoRpwsHfrKronosDataRecords

    _dataset_keys = None

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        CoRpwsHfrKronosData.__init__(self, filepath, dataset, access_mode)
        self._nrecord = len(self._data)
        self._nsweep = 1

    @property
    def _ydh(self):
        return None
        # return f"{self._period_times[0]}.00"

    @property
    def times(self):
        from datetime import datetime

        return Time([datetime.strptime(self._period_times[0], "%Y%j")])

    @property
    def frequencies(self):
        return self._data["xf"] * Unit("kHz")

    def as_xarray(self):
        import xarray

        dataset_keys = self.dataset_keys
        units = self.units
        antennas = ["Z", "-X", "+X", "D"]
        bins = numpy.linspace(-170, -90, 1601)
        dependencies = [
            ["frequency", "antenna", "bin"],
            ["frequency", "antenna"],
            ["frequency", "antenna"],
            ["frequency"],
            ["frequency"],
            ["frequency", "antenna"],
            ["frequency", "antenna"],
            ["frequency", "antenna"],
            ["frequency", "antenna"],
        ]

        data_vars = {}
        for key, units, deps in zip(dataset_keys, units, dependencies):
            data_vars[key] = (
                deps,
                self._data[key],
                {"units": units},
            )

        datasets = xarray.Dataset(
            data_vars=data_vars,
            coords={
                "frequency": (["frequency"], self.frequencies, {"units": "kHz"}),
                "antenna": (["antenna"], antennas),
                "bin": (["bin"], bins, {"units": "dB"}),
            },
        )
        return datasets.sortby("frequency")
