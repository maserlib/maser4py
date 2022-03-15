# -*- coding: utf-8 -*-
from maser.data.base import Sweeps
import struct
from ..const import (
    CCSDS_CDS_FIELDS,
    CALDATE_FIELDS,
    ORBIT_FIELDS,
)
from ..utils import _read_sweep_length, _merge_dtype, _read_block


class WindWavesL260sSweeps(Sweeps):
    @property
    def generator(self):

        ccsds_fields, ccsds_dtype = CCSDS_CDS_FIELDS
        caldate_fields, caldate_dtype = CALDATE_FIELDS

        header_fields = (
            ccsds_fields
            + ["RECEIVER_CODE", "JULIAN_SEC"]
            + caldate_fields
            + ["AVG_DURATION", "IUNIT", "NFREQ"]
        )

        # JULIAN_SEC [Int, 32 bits] = Julian date of the middle of the 60-second interval (in seconds since 1950/01/01)
        # AVG_DURATION [Int, 16 bits] = Averaging duration (seconds)
        # IUNIT [Int, 16 bits] = Signal intensity unit:
        #  1: Volt TLM (N1)
        #  2: V^2/Hz @ receiver (N2-3)
        #  3: μV^2/Hz @ receiver (N2-3)
        #  4: SFU (10^-22 W/m^2/Hz) @ antenna (N2-4).
        # NFREQ [Int, 16 bits] = Number of frequencies

        header_dtype = _merge_dtype((ccsds_dtype, ">hi", caldate_dtype, ">hhh"))

        orbit_fields, orbit_dtype = ORBIT_FIELDS
        nsweep = 0

        while True:
            try:
                # Reading number of octets in the current sweep
                loctets1 = _read_sweep_length(self.file)
                if loctets1 is None:
                    break

                # Reading header parameters in the current sweep
                header_i = _read_block(self.file, header_dtype, header_fields)
                nfreq = header_i["NFREQ"]

                if self.load_data:
                    # Reading orbit data for current sweep
                    orbit = _read_block(self.file, orbit_dtype, orbit_fields)

                    # Reading frequency list in the current sweep
                    cur_dtype = ">" + "f" * nfreq
                    freq = _read_block(self.file, cur_dtype)

                    # Reading Smoy (avg intensity)
                    smoy = _read_block(self.file, cur_dtype)

                    # Reading Smin (min intensity)
                    smin = _read_block(self.file, cur_dtype)

                    # Reading Smax (max intensity)
                    smax = _read_block(self.file, cur_dtype)

                    data_i = {
                        "FREQ": freq,
                        "SMOY": smoy,
                        "SMIN": smin,
                        "SMAX": smax,
                        "ORBIT": orbit,
                    }
                else:
                    # Skip data section
                    self.file.seek(12 + (16 * nfreq), 1)
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


class WindWaves60sSweeps(Sweeps):
    @property
    def generator(self):
        ccsds_fields, ccsds_dtype = CCSDS_CDS_FIELDS

        caldate_fields, caldate_dtype = CALDATE_FIELDS

        header_fields = (
            ccsds_fields
            + ["RECEIVER_CODE", "JULIAN_SEC"]
            + caldate_fields
            + ["AVG_DURATION", "IUNIT", "NFREQ"]
        )

        # RECEIVER_CODE [Int, 16 bits] = Name of Receiver: 0=TNR; 1=RAD1; 2=RAD2
        # JULIAN_SEC [Int, 32 bits] = Julian date of the middle of the 60-second interval (in seconds since 1950/01/01)

        orbit_fields, orbit_dtype = ORBIT_FIELDS

        header_dtype = _merge_dtype((ccsds_dtype, ">hi", caldate_dtype, ">hhh"))

        nsweep = 0

        while True:
            try:
                # Reading number of octets in the current sweep
                loctets1 = _read_sweep_length(self.file)
                if loctets1 is None:
                    break

                # Reading header parameters in the current sweep
                header_i = _read_block(self.file, header_dtype, header_fields)
                nfreq = header_i["NFREQ"]

                if self.load_data:
                    # Reading orbit data for current sweep
                    orbit = _read_block(self.file, orbit_dtype, orbit_fields)

                    # Reading frequency list in the current sweep
                    cur_dtype = ">" + "f" * nfreq
                    freq = _read_block(self.file, cur_dtype)

                    # Reading frequency list in the current sweep
                    intensity = _read_block(self.file, cur_dtype)

                    data_i = {
                        "FREQ": freq,
                        "INTENSITY": intensity,
                        "ORBIT": orbit,
                    }
                else:
                    # Skip data section
                    self.file.seek(12 + 8 * nfreq, 1)
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


class WindWavesL2HighResSweeps(Sweeps):
    def _read_data_block(self, nbytes):
        block = self.file.read(nbytes)
        Vspal = struct.unpack(">" + "f" * (nbytes // 4), block)
        block = self.file.read(nbytes)
        Tspal = struct.unpack(">" + "f" * (nbytes // 4), block)
        return Vspal, Tspal

    @property
    def generator(self):
        ccsds_fields, ccsds_dtype = CCSDS_CDS_FIELDS
        caldate_fields, caldate_dtype = CALDATE_FIELDS
        header_fields = (
            ccsds_fields
            + ["RECEIVER_CODE", "JULIAN_SEC"]
            + caldate_fields
            + [
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
            ]
        )
        header_dtype = _merge_dtype(
            (ccsds_dtype, ">hL", caldate_dtype, ">fihhffhhhhhhhhffhhhhh")
        )
        # nsweep = 1

        while True:
            try:
                # Reading number of bytes in the current sweep
                loctets1 = _read_sweep_length(self.file)
                if loctets1 is None:
                    break

                # Reading header parameters in the current sweep
                header_i = _read_block(self.file, header_dtype, header_fields)
                npalf = header_i["NPALIF"]
                nspal = header_i["NSPALF"]
                nzpal = header_i["NZPALF"]

                # Reading frequency list (kHz) in the current sweep
                cur_dtype = ">" + "f" * npalf
                freq = _read_block(self.file, cur_dtype)
                print(npalf)
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
                loctets2 = _read_sweep_length(self.file)
                if loctets2 != loctets1:
                    print("Error reading file!")
                    return None
            except EOFError:
                print("End of file reached")
                break
            else:
                yield header_i, data_i
                # nsweep += 1
