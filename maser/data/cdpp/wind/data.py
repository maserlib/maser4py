# -*- coding: utf-8 -*-
from typing import Union
from pathlib import Path
from maser.data.base import BinData
from .sweeps import (
    WindWavesL260sSweeps,
    WindWavesL2HighResSweeps,
    WindWaves60sSweeps,
)
from .records import WindWavesTnrL3Bqt1mnRecords
from astropy.time import Time
from astropy.units import Unit


class WindWavesRad1L260sV2BinData(BinData, dataset="cdpp_wi_wa_rad1_l2_60s_v2"):
    """CDPP Wind Waves RAD1 Level 2 60s-Average (version 2) dataset

    - Observatory/Facility: WIND
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_wi_wa_rad1_l2_60s_v2`
    - Data format: Binary"""

    _iter_sweep_class = WindWavesL260sSweeps


class WindWavesRad1L2BinData(BinData, dataset="cdpp_wi_wa_rad1_l2"):
    """Class for `cdpp_wi_wa_rad1_l2` binary data."""

    _iter_sweep_class = WindWavesL2HighResSweeps

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


class WindWavesRad2L260sV2BinData(BinData, dataset="cdpp_wi_wa_rad2_l2_60s_v2"):
    """Class for `cdpp_wi_wa_rad2_l2_60s_v2` binary data."""

    pass


class WindWavesTnrL260sV2BinData(BinData, dataset="cdpp_wi_wa_tnr_l2_60s_v2"):
    """Class for `cdpp_wi_wa_tnr_l2_60s_v2` binary data."""

    pass


class WindWavesTnrL3Bqt1mnBinData(BinData, dataset="cdpp_wi_wa_tnr_l3_bqt_1mn"):
    """Class for `cdpp_wi_wa_tnr_l3_bqt_1mn` data."""

    _access_modes = ["records", "file"]
    _iter_record_class = WindWavesTnrL3Bqt1mnRecords

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "records",
        load_data: bool = True,
    ) -> None:
        super().__init__(filepath, dataset, access_mode, load_data)

    @property
    def sweeps(self):
        raise ValueError("Illegal access mode.")


class WindWavesTnrL3NnBinData(BinData, dataset="cdpp_wi_wa_tnr_l3_nn"):
    """Class for `cdpp_wi_wa_tnr_l3_nn` data."""

    pass


class WindWavesRad1L260sV1BinData(BinData, dataset="cdpp_wi_wa_rad1_l2_60s_v1"):
    """Class for `cdpp_wi_wa_rad1_l2_60s_v1` binary data"""

    _iter_sweep_class = WindWaves60sSweeps


class WindWavesRad2L260sV1BinData(BinData, dataset="cdpp_wi_wa_rad2_l2_60s_v1"):
    """Class for `cdpp_wi_wa_rad2_l2_60s_v1` binary data"""

    _iter_sweep_class = WindWaves60sSweeps


class WindWavesTnrL260sV1BinData(BinData, dataset="cdpp_wi_wa_tnr_l2_60s_v1"):
    """Class for `cdpp_wi_wa_tnr_l2_60s_v1` binary data"""

    _iter_sweep_class = WindWaves60sSweeps
