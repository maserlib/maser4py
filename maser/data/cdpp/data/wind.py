# -*- coding: utf-8 -*-
from typing import Union
from pathlib import Path
from maser.data.base import BinData
from maser.data.cdpp.sweeps import (
    WindWavesL260sSweeps,
    WindWavesL2HighResSweeps,
    WindWaves60sSweeps,
    WindWavesTnrL3Bqt1mnSweeps,
)
from astropy.time import Time
from astropy.units import Unit


class WindWavesRad1L260sV2BinData(BinData, dataset="wi_wa_rad1_l2_60s_v2"):
    @property
    def sweeps(self):
        # sweeps =
        return WindWavesL260sSweeps(file=self.file, load_data=self._load_data)
        # for sweep in sweeps:
        #    yield sweep


class WindWavesRad1L2BinData(BinData, dataset="wi_wa_rad1_l2"):
    @property
    def sweeps(self):
        sweeps = WindWavesL2HighResSweeps(file=self.file, load_data=self._load_data)
        # return WindWavesL2HighResSweeps(file=self.file, load_data=self._load_data)
        for sweep in sweeps:
            yield sweep

    @property
    def times(self):
        if self._times is None:
            times = []
            _load_data, self._load_data = self._load_data, False
            for header, _ in self.sweeps:
                times.append(
                    Time(
                        f"{header['CALEND_DATE_YEAR']}-{header['CALEND_DATE_MONTH']}-"
                        f"{header['CALEND_DATE_DAY']} {header['CALEND_DATE_HOUR']}:"
                        f"{header['CALEND_DATE_MINUTE']}:{header['CALEND_DATE_SECOND']}"
                    )
                )
            self._load_data = _load_data
            self._times = Time(times)
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            _load_data, self._load_data = self._load_data, True
            _, data = next(self.sweeps)
            self._frequencies = data["FREQ"] * Unit("kHz")
            self._load_data = _load_data
        return self._frequencies


class WindWavesRad2L260sV2BinData(BinData, dataset="wi_wa_rad2_l2_60s_v2"):
    pass


class WindWavesTnrL260sV2BinData(BinData, dataset="wi_wa_tnr_l2_60s_v2"):
    pass


class WindWavesTnrL3Bqt1mnBinData(BinData, dataset="wi_wa_tnr_l3_bqt_1mn"):
    _access_modes = ["records", "file"]

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "records",
        load_data: bool = True,
    ) -> None:
        super().__init__(filepath, dataset, access_mode, load_data)

    @property
    def records(self):
        records = WindWavesTnrL3Bqt1mnSweeps(file=self.file, load_data=self._load_data)
        for record in records:
            yield record

    @property
    def sweeps(self):
        raise ValueError("Illegal access mode.")


class WindWavesTnrL3NnBinData(BinData, dataset="wi_wa_tnr_l3_nn"):
    pass


class WindWavesRad1L260sV1BinData(BinData, dataset="wi_wa_rad1_l2_60s_v1"):
    @property
    def sweeps(self):
        sweeps = WindWaves60sSweeps(file=self.file, load_data=self._load_data)
        for sweep in sweeps:
            yield sweep


class WindWavesRad2L260sV1BinData(BinData, dataset="wi_wa_rad2_l2_60s_v1"):
    @property
    def sweeps(self):
        sweeps = WindWaves60sSweeps(file=self.file, load_data=self._load_data)
        for sweep in sweeps:
            yield sweep


class WindWavesTnrL260sV1BinData(BinData, dataset="wi_wa_tnr_l2_60s_v1"):
    @property
    def sweeps(self):
        sweeps = WindWaves60sSweeps(file=self.file, load_data=self._load_data)
        for sweep in sweeps:
            yield sweep
