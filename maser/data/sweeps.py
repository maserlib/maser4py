# -*- coding: utf-8 -*-
from maser.data.sweep import Sweep
import struct


class Sweeps:
    def __iter__(self):
        self.__call__(load_data=True)

    def __call__(self, *args, **kwargs):
        yield Sweep(*args, **kwargs)


class WindWavesL260sSweeps(Sweeps):
    def __init__(self, file, load_data=True):
        self.file = file
        self.load_data = load_data

    def __call__(self, load_data: bool = True):
        self.load_data = load_data
        self.__iter__()

    def __iter__(self):
        ccsds_fields = [
            "CCSDS_PREAMBLE",
            "CCSDS_JULIAN_DAY_B1",
            "CCSDS_JULIAN_DAY_B2",
            "CCSDS_JULIAN_DAY_B3",
            "CCSDS_MILLISECONDS_OF_DAY",
        ]
        # CCSDS_PREAMBLE [Int, 8 bits] = 76
        # CCSDS_JULIAN_DAY [Int, 24 bits] = Days since 1950/01/01 (=1)
        # CCSDS_MILLISECONDS_OF_DAY [Int, 32 bits] = Millisecond of day
        ccsds_dtype = ">bbbbi"

        caldate_fields = [
            "CALEND_DATE_YEAR",
            "CALEND_DATE_MONTH",
            "CALEND_DATE_DAY",
            "CALEND_DATE_HOUR",
            "CALEND_DATE_MINUTE",
            "CALEND_DATE_SECOND",
        ]
        # CALEND_DATE fields YEAR, MONTH, DAY, HOUR, MINUTE, SECOND: all [Int, 16bits]
        caldate_dtype = "hhhhhh"

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

        header_dtype = ccsds_dtype + "hi" + caldate_dtype + "hhh"

        orbit_fields = ["GSE_X", "GSE_Y", "GSE_Z"]
        # SPACECRAFT_COORDINATES fields GSE_X, GSE_Y, GSE_Z: all [Real, 32bits], in Earth Radii (GSE)
        orbit_dtype = ">fff"

        nsweep = 0

        while True:
            try:
                # Reading number of octets in the current sweep
                block = self.file.read(4)
                if len(block) == 0:
                    break
                loctets1 = struct.unpack(">i", block)[0]

                # Reading header parameters in the current sweep
                block = self.file.read(32)
                header_i = dict(zip(header_fields, struct.unpack(header_dtype, block)))
                nfreq = header_i["NFREQ"]

                if self.load_data:
                    # Reading orbit data for current sweep
                    block = self.file.read(12)
                    orbit = dict(zip(orbit_fields, struct.unpack(orbit_dtype, block)))

                    # Reading frequency list in the current sweep
                    block = self.file.read(4 * nfreq)
                    freq = struct.unpack(">" + "f" * nfreq, block)

                    # Reading Smoy (avg intensity)
                    block = self.file.read(4 * nfreq)
                    smoy = struct.unpack(">" + "f" * nfreq, block)

                    # Reading Smin (min intensity)
                    block = self.file.read(4 * nfreq)
                    smin = struct.unpack(">" + "f" * nfreq, block)

                    # Reading Smax (max intensity)
                    block = self.file.read(4 * nfreq)
                    smax = struct.unpack(">" + "f" * nfreq, block)

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
                nsweep += 1


class WindWaves60sSweeps(Sweeps):
    def __init__(self, file, load_data=True):
        self.file = file
        self.load_data = load_data

    def __call__(self, load_data: bool = True):
        self.load_data = load_data
        self.__iter__()

    def __iter__(self):
        ccsds_fields = [
            "CCSDS_PREAMBLE",
            "CCSDS_JULIAN_DAY_B1",
            "CCSDS_JULIAN_DAY_B2",
            "CCSDS_JULIAN_DAY_B3",
            "CCSDS_MILLISECONDS_OF_DAY",
        ]
        # CCSDS_PREAMBLE [Int, 8 bits] = 76
        # CCSDS_JULIAN_DAY [Int, 24 bits] = Days since 1950/01/01 (=1)
        # CCSDS_MILLISECONDS_OF_DAY [Int, 32 bits] = Millisecond of day
        ccsds_dtype = ">bbbbi"

        caldate_fields = [
            "CALEND_DATE_YEAR",
            "CALEND_DATE_MONTH",
            "CALEND_DATE_DAY",
            "CALEND_DATE_HOUR",
            "CALEND_DATE_MINUTE",
            "CALEND_DATE_SECOND",
        ]
        # CALEND_DATE fields YEAR, MONTH, DAY, HOUR, MINUTE, SECOND: all [Int, 16bits]
        caldate_dtype = "hhhhhh"

        header_fields = (
            ccsds_fields
            + ["RECEIVER_CODE", "JULIAN_SEC"]
            + caldate_fields
            + ["AVG_DURATION", "IUNIT", "NFREQ"]
        )

        # RECEIVER_CODE [Int, 16 bits] = Name of Receiver: 0=TNR; 1=RAD1; 2=RAD2
        # JULIAN_SEC [Int, 32 bits] = Julian date of the middle of the 60-second interval (in seconds since 1950/01/01)

        orbit_fields = ["GSE_X", "GSE_Y", "GSE_Z"]
        # SPACECRAFT_COORDINATES fields GSE_X, GSE_Y, GSE_Z: all [Real, 32bits], in Earth Radii (GSE)
        orbit_dtype = ">fff"

        header_dtype = ccsds_dtype + "hi" + caldate_dtype + "hhh"

        nsweep = 0

        while True:
            try:
                # Reading number of octets in the current sweep
                block = self.file.read(4)
                if len(block) == 0:
                    break
                loctets1 = struct.unpack(">i", block)[0]

                # Reading header parameters in the current sweep
                block = self.file.read(32)
                header_i = dict(zip(header_fields, struct.unpack(header_dtype, block)))
                nfreq = header_i["NFREQ"]

                if self.load_data:
                    # Reading orbit data for current sweep
                    block = self.file.read(12)
                    orbit = dict(zip(orbit_fields, struct.unpack(orbit_dtype, block)))

                    # Reading frequency list in the current sweep
                    block = self.file.read(4 * nfreq)
                    freq = struct.unpack(">" + "f" * nfreq, block)

                    # Reading frequency list in the current sweep
                    block = self.file.read(4 * nfreq)
                    intensity = struct.unpack(">" + "f" * nfreq, block)
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
                nsweep += 1


class WindWavesL2HighResSweeps(Sweeps):
    def __init__(self, file, load_data=True):
        self.file = file
        self.load_data = load_data

    def __call__(self, load_data: bool = True):
        self.load_data = load_data
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


class WindWavesTnrL3Bqt1mnSweeps(Sweeps):
    def __init__(self, file, load_data=True):
        self.file = file
        self.load_data = load_data

    def __call__(self, load_data: bool = True):
        self.load_data = load_data
        self.__iter__()

    def __iter__(self):
        ccsds_fields = [
            "CCSDS_PREAMBLE",
            "CCSDS_JULIAN_DAY_B1",
            "CCSDS_JULIAN_DAY_B2",
            "CCSDS_JULIAN_DAY_B3",
            "CCSDS_MILLISECONDS_OF_DAY",
        ]
        # CCSDS_PREAMBLE [Int, 8 bits] = 76
        # CCSDS_JULIAN_DAY [Int, 24 bits] = Days since 1950/01/01 (=1)
        # CCSDS_MILLISECONDS_OF_DAY [Int, 32 bits] = Millisecond of day
        ccsds_dtype = ">bbbbi"

        header_fields = ccsds_fields + ["UR8_TIME"]

        # UR8_TIME [Real, 64 bits] = Days since 1982/01/01 (=0)

        header_dtype = ccsds_dtype + "d"

        nsweep = 0

        while True:
            try:
                # Reading number of octets in the current sweep
                block = self.file.read(4)
                if len(block) == 0:
                    break
                loctets1 = struct.unpack(">i", block)[0]

                # Reading header parameters in the current sweep
                block = self.file.read(16)
                header_i = dict(zip(header_fields, struct.unpack(header_dtype, block)))

                if self.load_data:
                    # Reading data from NN in the current sweep
                    block = self.file.read(4)
                    data_from_nn = struct.unpack(">f", block)
                    plasma_freq_nn = data_from_nn[0]

                    # Reading data from Fit in the current sweep
                    block = self.file.read(16)
                    data_from_fit = struct.unpack(">ffff", block)
                    plasma_freq_fit = data_from_fit[0]
                    cold_elec_temp_fit = data_from_fit[1]
                    elec_dens_ratio = data_from_fit[2]
                    elec_temp_ratio = data_from_fit[3]

                    # Reading data from 3dp in the current sweep
                    block = self.file.read(8)
                    data_from_3dp = struct.unpack(">ff", block)
                    proton_temp_3dp = data_from_3dp[0]
                    sw_veloc_3dp = data_from_3dp[1]

                    # Reading fit accuracy in the current sweep
                    block = self.file.read(28)
                    params = struct.unpack(">fffffff", block)
                    accur_param_1 = params[0]
                    accur_param_2 = params[1]
                    accur_param_3 = params[2]
                    accur_param_4 = params[3]
                    accur_param_7 = params[4]
                    accur_param_8 = params[5]
                    accur_rms = params[6]

                    data_i = {
                        "PLASMA_FREQUENCY_NN": plasma_freq_nn,
                        "PLASMA_FREQUENCY": plasma_freq_fit,
                        "COLD_ELECTRONS_TEMPERATURE": cold_elec_temp_fit,
                        "ELECTRONIC_DENSITY_RATIO": elec_dens_ratio,
                        "ELECTRONIC_TEMPERATURE_RATIO": elec_temp_ratio,
                        "PROTON_TEMPERATURE": proton_temp_3dp,
                        "SOLAR_WIND_VELOCITY": sw_veloc_3dp,
                        "FIT_ACCUR_PARAM_1": accur_param_1,
                        "FIT_ACCUR_PARAM_2": accur_param_2,
                        "FIT_ACCUR_PARAM_3": accur_param_3,
                        "FIT_ACCUR_PARAM_4": accur_param_4,
                        "FIT_ACCUR_PARAM_7": accur_param_7,
                        "FIT_ACCUR_PARAM_8": accur_param_8,
                        "FIT_ACCUR_RMS": accur_rms,
                    }
                else:
                    # Skip data section
                    self.file.seek(56, 1)
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
                nsweep += 1
