# -*- coding: utf-8 -*-
from maser.data.sweep import Sweep
import struct


class Sweeps:
    def __iter__(self):
        self.__call__(load_data=True)

    def __call__(self, *args, **kwargs):
        yield Sweep(*args, **kwargs)


class WindWavesL2HighResSweeps(Sweeps):
    def __init__(self, file, load_data=True):
        self.file = file
        self.load_data = load_data

    def __call__(self):
        self.__iter__()

    def _read_data_block(self, nbytes):
        block = self.file.read(nbytes)
        Vspal = struct.unpack(">" + "f" * (nbytes // 4), block)
        block = self.file.read(nbytes)
        Tspal = struct.unpack(">" + "f" * (nbytes // 4), block)
        return Vspal, Tspal

    def __iter__(self):

        header_fields = (
            "P_FIELD",
            "JULIAN_DAY_B1",
            "JULIAN_DAY_B2",
            "JULIAN_DAY_B3",
            "MSEC_OF_DAY",
            "RECEIVER_CODE",
            "JULIAN_SEC_FRAC",
            "YEAR",
            "MONTH",
            "DAY",
            "HOUR",
            "MINUTE",
            "SECOND",
            "JULIAN_SEC_FRAC",
            "ISWEEP",
            "IUNIT",
            "NPBS",
            "SUN_ANGLE",
            "SPIN_RATE",
            "KSPIN",
            "MODE",
            "LISTFR",
            "NFREQ",
            "ICAL",
            "IANTEN",
            "IPOLA",
            "IDIPXY",
            "SDURCY",
            "SDURPA",
            "NPALCY",
            "NFRPAL",
            "NPALIF",
            "NSPALF",
            "NZPALF",
        )
        header_dtype = ">bbbbihLhhhhhhfihhffhhhhhhhhffhhhhh"
        # nsweep = 1

        while True:
            try:
                # print("Reading sweep #%i" % (nsweep))
                # Reading number of bytes in the current sweep
                block = self.file.read(4)
                if len(block) == 0:
                    break
                loctets1 = struct.unpack(">i", block)[0]
                # Reading header parameters in the current sweep
                block = self.file.read(80)
                header_i = dict(zip(header_fields, struct.unpack(header_dtype, block)))
                npalf = header_i["NPALIF"]
                nspal = header_i["NSPALF"]
                nzpal = header_i["NZPALF"]
                # Reading frequency list (kHz) in the current sweep
                block = self.file.read(4 * npalf)
                freq = struct.unpack(">" + "f" * npalf, block)
                if self.load_data:
                    # Reading intensity and time values for S/SP in the current sweep
                    Vspal, Tspal = self._read_data_block(4 * npalf * nspal)
                    # Reading intensity and time values for Z in the current sweep
                    Vzpal, Tzpal = self._read_data_block(4 * npalf * nzpal)
                    data_i = {
                        "FREQ": freq,
                        "VSPAL": Vspal,
                        "VZPAL": Vzpal,
                        "TSPAL": Tspal,
                        "TZPAL": Tzpal,
                    }
                else:
                    # Skip data section
                    self.file.seek(8 * npalf * (nspal + nzpal), 1)
                    data_i = None
                # Reading number of octets in the current sweep
                block = self.file.read(4)
                loctets2 = struct.unpack(">i", block)[0]
                if loctets2 != loctets1:
                    print("Error reading file!")
                    return None
            except EOFError:
                print("End of file reached")
                break
            else:
                yield header_i, data_i
                # nsweep += 1
