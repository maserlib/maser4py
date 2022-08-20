# -*- coding: utf-8 -*-
from maser.data.base import BinData
from .sweeps import InterballAuroralPolradRspSweeps
from .records import InterballAuroralPolradRspRecords
from pathlib import Path
import numpy

from typing import Union
from astropy.time import Time
from ..const import CCSDS_CDS_FIELDS
from ..utils import _read_sweep_length, _read_block


class InterballAuroralPolradRspBinData(BinData, dataset="cdpp_int_aur_polrad_rspn2"):
    """Class for `cdpp_int_aur_polrad_rspn2` binary data"""

    _iter_sweep_class = InterballAuroralPolradRspSweeps
    _iter_record_class = InterballAuroralPolradRspRecords

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
        )
        self._data = None
        self._nsweep = None
        self._data = self._loader()

    def _loader(self, count_only=False):
        data = []
        nsweep = 0

        ccsds_fields, ccsds_dtype = CCSDS_CDS_FIELDS
        sfa_conf_fields, sfa_conf_dtype = (
            ["STEPS", "FIRST_FREQ", "CHANNELS", "SWEEP_DURATION", "ATTENUATION"],
            ">ififi",
        )

        while True:
            try:
                # Reading number of octets in the current sweep
                loctets1 = _read_sweep_length(self.file)
                if loctets1 is None:
                    break

                header_i = _read_block(self.file, ccsds_dtype, ccsds_fields)

                # => Here we fix the `P_Field` which is corrupted
                # First we reverse the order of the bits in the byte
                P_Field_tmp = int("{:08b}".format(header_i["CCSDS_PREAMBLE"])[::-1], 2)
                # Then we put back the initial 4-6 bits into bits 1-3 (defining the CSSDS code)
                # as those bits are not in reverse order in the file...
                P_Field_tmp = (P_Field_tmp & 241) + (
                    header_i["CCSDS_PREAMBLE"] & 112
                ) // 8

                header_i["P_Field"] = P_Field_tmp
                header_i["T_Field"] = bytearray(
                    [
                        header_i["CCSDS_JULIAN_DAY_B1"],
                        header_i["CCSDS_JULIAN_DAY_B2"],
                        header_i["CCSDS_JULIAN_DAY_B3"],
                        header_i["CCSDS_MILLISECONDS_OF_DAY_B0"],
                        header_i["CCSDS_MILLISECONDS_OF_DAY_B1"],
                        header_i["CCSDS_MILLISECONDS_OF_DAY_B2"],
                        header_i["CCSDS_MILLISECONDS_OF_DAY_B3"],
                    ]
                )

                header_i["CCSDS_CDS_LEVEL2_EPOCH"] = Time("1950-01-01 00:00:00")
                header_i["SESSION_NAME"] = "".join(
                    [x.decode() for x in _read_block(self.file, ">cccccccc")]
                )
                header_i.update(_read_block(self.file, sfa_conf_dtype, sfa_conf_fields))
                header_i["SWEEP_ID"] = nsweep

                data_dtype = ">" + "f" * header_i["STEPS"]

                data_i = dict((("EX", None), ("EY", None), ("EZ", None)))
                data_i["EY"] = _read_block(self.file, data_dtype)
                if header_i["CHANNELS"] == 3:
                    data_i["EZ"] = _read_block(self.file, data_dtype)
                    data_i["EX"] = _read_block(self.file, data_dtype)

                # Reading number of octets in the current sweep
                loctets2 = _read_sweep_length(self.file)
                if loctets2 != loctets1:
                    print("Error reading file!")
                    return None

            except EOFError:
                print("End of file reached")
                break

            else:
                data.append((header_i, data_i))
                nsweep += 1

        self._nsweep = nsweep
        return data

    def __len__(self):
        if self._nsweep is None:
            self._loader(count_only=True)
        return self._nsweep

    @property
    def times(self):
        if self._times is None:
            times = []
            for sweep in self.sweeps:
                times.append(sweep.time)
            self._times = Time(times)
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            sweep = next(self.sweeps)
            self._frequencies = sweep.frequencies
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

    def as_xarray(self):
        import xarray

        datasets = {}
        for dataset_key in ["EX", "EY", "EZ"]:
            datasets[dataset_key] = xarray.DataArray(
                data=numpy.array([item.data[dataset_key] for item in self.sweeps]).T,
                name=dataset_key,
                coords=[
                    ("frequency", self.frequencies, {"units": "kHz"}),
                    ("time", self.times.to_datetime()),
                ],
                dims=("frequency", "time"),
                attrs={"units": "W m^-2 Hz^-1"},
            )

        return datasets
