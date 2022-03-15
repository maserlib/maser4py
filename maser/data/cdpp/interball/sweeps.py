# -*- coding: utf-8 -*-
import struct

from maser.data.base import Sweeps
from ..const import CCSDS_CDS_FIELDS
from ..utils import _read_sweep_length, _read_block
from astropy.time import Time


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
                header_i["CCSDS_CDS_LEVEL2_EPOCH"] = Time("1950-01-01 00:00:00")
                header_i["SESSION_NAME"] = "".join(
                    [x.decode() for x in _read_block(self.file, ">cccccccc")]
                )
                header_i.update(_read_block(self.file, sfa_conf_dtype, sfa_conf_fields))

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
                yield header_i, data_i
                nsweep += 1
