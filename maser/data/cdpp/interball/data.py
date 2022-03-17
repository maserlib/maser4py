# -*- coding: utf-8 -*-
from maser.data.base import BinData
from .sweeps import InterballAuroralPolradRspSweeps
from ..ccsds import decode_ccsds_date

from astropy.time import Time
from astropy.units import Unit
import numpy


class InterballAuroralPolradRspBinData(BinData, dataset="cdpp_int_aur_polrad_rspn2"):
    _iter_sweep_class = InterballAuroralPolradRspSweeps

    @property
    def times(self):
        if self._times is None:
            times = []
            _load_data, self._load_data = self._load_data, False
            for header, _ in self.sweeps:
                times.append(
                    Time(
                        decode_ccsds_date(
                            header["P_Field"],
                            header["T_Field"],
                            header["CCSDS_CDS_LEVEL2_EPOCH"],
                        ).datetime
                    )
                )
            self._load_data = _load_data
            self._times = Time(times)
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            _load_data, self._load_data = self._load_data, False
            header, _ = next(self.sweeps)
            self._frequencies = numpy.flipud(
                numpy.arange(header["STEPS"]) * 4.096 + 4.096
            ) * Unit("kHz")
            self._load_data = _load_data
        return self._frequencies

    @staticmethod
    def decode_session_name(session_name):
        tmp = dict()

        tmp["YEAR"] = int(session_name[0]) + 1990
        tmp["DOY"] = int(session_name[1:4])
        tmp["SUB_SESSION_NB"] = int(session_name[4])

        if session_name[5] == "S":
            tmp["TELEMETRY_TYPE"] = "SSNI"
        elif session_name[5] == "C":
            tmp["TELEMETRY_TYPE"] = "STO"
        else:
            tmp["TELEMETRY_TYPE"] = "unk"

        if session_name[6] == "1":
            tmp["TELEMETRY_MODE"] = "DIRECT"
        elif session_name[6] == "2":
            tmp["TELEMETRY_MODE"] = "MEMORY"
        else:
            tmp["TELEMETRY_TYPE"] = "unk"

        if session_name[7] == "1":
            tmp["STATION_CODE"] = "EVPATORIA"
        elif session_name[7] == "8":
            tmp["STATION_CODE"] = "PANSKA_VES"
        else:
            tmp["STATION_CODE"] = "unk"

        return tmp
