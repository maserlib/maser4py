# -*- coding: utf-8 -*-
from maser.data.base.sweeps import Sweeps, Sweep
from ..const import CCSDS_CDS_FIELDS
from ..ccsds import decode_ccsds_date
from ..utils import _read_sweep_length, _read_block

import struct
import numpy
from astropy.time import Time
from astropy.units import Unit


class InterballAuroralPolradRspSweep(Sweep):
    @property
    def time(self):
        return Time(
            decode_ccsds_date(
                self.header["P_Field"],
                self.header["T_Field"],
                self.header["CCSDS_CDS_LEVEL2_EPOCH"],
            ).datetime
        )

    @property
    def frequencies(self):
        return numpy.flipud(numpy.arange(self.header["STEPS"]) * 4.096 + 4.096) * Unit(
            "kHz"
        )


class InterballAuroralPolradRspSweeps(Sweeps):
    @property
    def generator(self):

        ccsds_fields, ccsds_dtype = CCSDS_CDS_FIELDS
        sfa_conf_fields, sfa_conf_dtype = (
            ["STEPS", "FIRST_FREQ", "CHANNELS", "SWEEP_DURATION", "ATTENUATION"],
            ">ififi",
        )
        nsweep = 0

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
                sweep_length = struct.calcsize(data_dtype) * header_i["CHANNELS"]
                if self.load_data:
                    data_i = {
                        "EX": None,
                        "EY": None,
                        "EZ": None,
                    }
                    if header_i["CHANNELS"] == 3:
                        data_i["EX"] = _read_block(self.file, data_dtype)
                        data_i["EY"] = _read_block(self.file, data_dtype)
                    data_i["EZ"] = _read_block(self.file, data_dtype)
                else:
                    self.file.seek(sweep_length, 1)
                    data_i = None

                # Reading number of octets in the current sweep
                loctets2 = _read_sweep_length(self.file)
                if loctets2 != loctets1:
                    print("Error reading file!")
                    return None

            except EOFError:
                print("End of file reached")
                break

            else:
                yield InterballAuroralPolradRspSweep(header_i, data_i)
                nsweep += 1
