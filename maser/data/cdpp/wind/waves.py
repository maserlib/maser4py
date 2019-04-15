#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read a Wind/Waves data file from CDPP deep archive (http://cdpp-archive.cnes.fr).
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__date__ = "10-JUL-2017"
__version__ = "0.11"

__all__ = ["WindWavesData", "read_wind_waves"]

import struct
import os
from maser.data.cdpp import CDPPDataFromFile
from .const import *


class WindWavesData(CDPPDataFromFile):
    """
    Class for Wind/Waves data.
    This is a class inheriting from the CDPPData class.
    """

    def __init__(self, file, header, data, name, meta, orbit=None):
        """
        This method instantiates a WindWavesData. The method overrides the __init__() method from CDPPData, adding the
        meta and orbit attributes, that are specific to the WindWavesData class
        :param file: path to the input file.
        :param header: dict() containing header
        :param data: dict() containing data
        :param name: string containing the name of dataset
        :param meta: dict() containing metadata
        :param orbit: orbital data (default to None)
        """
        CDPPDataFromFile.__init__(self, file, header, data, name)
        self.meta = meta
        if orbit:
            self.orbit = orbit

    def get_datetime(self):
        """
        Method that provides the date and time, using a datetime.datetime object.
        :returns: datetime of instance
        """
        if self.name == "WIND_WAVES_TNR_L3_NN":
            return self.get_datetime_ur8()
        elif self.name == "WIND_WAVES_TNR_L3_BQT":
            return self.get_datetime_ur8()
        elif self.name == "WIND_WAVES_RADIO_60S":
            return self.get_datetime_ccsds_cds()
        else:
            print("Unknown dataset name...")
            return None

    def getvar_meta(self, key_name):
        """
        Method to retrieve the metadata attribute
        :param key_name: named key to be fetch in the metadata attribute
        :return: value corresponding to the input key
        """
        return self.meta[key_name]


def read_wind_waves_nn(file_path, verbose=False):
    """
    Method to read a Wind/Waves NN data file from CDPP deep archive
    :param file_path: path to file.
    :param verbose: optional flag to activate verbose mode
    :returns: a WindWavesData instance built from the input file.
    """

    ccsds_fields = ["CCSDS_PREAMBLE", "CCSDS_JULIAN_DAY_B1", "CCSDS_JULIAN_DAY_B2", "CCSDS_JULIAN_DAY_B3",
                    "CCSDS_MILLISECONDS_OF_DAY"]
    # CCSDS_PREAMBLE [Int, 8 bits] = 76
    # CCSDS_JULIAN_DAY [Int, 24 bits] = Days since 1950/01/01 (=1)
    # CCSDS_MILLISECONDS_OF_DAY [Int, 32 bits] = Millisecond of day
    ccsds_dtype = ">bbbbi"

    header_fields = ccsds_fields + ["UR8_TIME", "TNR_RECEIVER", "CONNECTED_ANTENNA"]

    # UR8_TIME [Real, 64 bits] = Days since 1982/01/01 (=0)
    # TNR_RECEIVER [Int, 32 bits] = Name of TNR Receiver: 0=TNR_A; 1=TNR_B
    # CONNECTED_ANTENNA [Int, 32 bits] = Name of connected antenna: 0=EX; 1=EY; 2=EZ

    header_dtype = ccsds_dtype + "dii"

    header = []
    data = []
    nsweep = 0

    with open(file_path, 'rb') as frb:
        while True:
            try:
                if verbose:
                    print("Reading sweep #{}".format(nsweep))

                # Reading number of octets in the current sweep
                block = frb.read(4)
                if len(block) == 0:
                    break
                loctets1 = struct.unpack('>i', block)[0]

                # Reading header parameters in the current sweep
                block = frb.read(24)
                header_i = dict(zip(header_fields, struct.unpack(header_dtype, block)))

                # Reading plasma frequency in the current sweep
                block = frb.read(4)
                plasma_f = struct.unpack('>f', block)[0]
                block = frb.read(4)
                e_density = struct.unpack('>f', block)[0]

                # Reading number of octets in the current sweep
                block = frb.read(4)
                loctets2 = struct.unpack('>i', block)[0]
                if loctets2 != loctets1:
                    print("Error reading file!")
                    return None

            except EOFError:
                print("End of file reached")
                break

            else:
                header.append(header_i)
                data.append({"PLASMA_FREQ": plasma_f, "ELEC_DENSITY": e_density})
                nsweep += 1

    name = 'WIND_WAVES_TNR_L3_NN'
    meta = WIND_WAVES_TNR_L3_NN_META

    return WindWavesData(os.path.basename(file_path), header, data, name, meta)


def read_wind_waves_bqt(file_path, verbose=False):
    """
    Method to read a Wind/Waves BQT data file from CDPP deep archive
    :param file_path: path to file.
    :param verbose: optional flag to activate verbose mode
    :returns: a WindWavesData instance built from the input file.
    """

    ccsds_fields = ["CCSDS_PREAMBLE", "CCSDS_JULIAN_DAY_B1", "CCSDS_JULIAN_DAY_B2", "CCSDS_JULIAN_DAY_B3",
                    "CCSDS_MILLISECONDS_OF_DAY"]
    # CCSDS_PREAMBLE [Int, 8 bits] = 76
    # CCSDS_JULIAN_DAY [Int, 24 bits] = Days since 1950/01/01 (=1)
    # CCSDS_MILLISECONDS_OF_DAY [Int, 32 bits] = Millisecond of day
    ccsds_dtype = ">bbbbi"

    header_fields = ccsds_fields + ["UR8_TIME"]

    # UR8_TIME [Real, 64 bits] = Days since 1982/01/01 (=0)

    header_dtype = ccsds_dtype + "d"

    header = []
    data = []
    nsweep = 0

    with open(file_path, 'rb') as frb:
        while True:
            try:
                if verbose:
                    print("Reading sweep #{}".format(nsweep))

                # Reading number of octets in the current sweep
                block = frb.read(4)
                if len(block) == 0:
                    break
                loctets1 = struct.unpack('>i', block)[0]

                # Reading header parameters in the current sweep
                block = frb.read(16)
                header_i = dict(zip(header_fields, struct.unpack(header_dtype, block)))

                # Reading data from NN in the current sweep
                block = frb.read(4)
                data_from_nn = struct.unpack('>f', block)
                plasma_freq_nn = data_from_nn[0]

                # Reading data from Fit in the current sweep
                block = frb.read(16)
                data_from_fit = struct.unpack('>ffff', block)
                plasma_freq_fit = data_from_fit[0]
                cold_elec_temp_fit = data_from_fit[1]
                elec_dens_ratio = data_from_fit[2]
                elec_temp_ratio = data_from_fit[3]

                # Reading data from 3dp in the current sweep
                block = frb.read(8)
                data_from_3dp = struct.unpack('>ff', block)
                proton_temp_3dp = data_from_3dp[0]
                sw_veloc_3dp = data_from_3dp[1]

                # Reading fit accuracy in the current sweep
                block = frb.read(28)
                params = struct.unpack('>fffffff', block)
                accur_param_1 = params[0]
                accur_param_2 = params[1]
                accur_param_3 = params[2]
                accur_param_4 = params[3]
                accur_param_7 = params[4]
                accur_param_8 = params[5]
                accur_rms = params[6]

                # Reading number of octets in the current sweep
                block = frb.read(4)
                loctets2 = struct.unpack('>i', block)[0]
                if loctets2 != loctets1:
                    print("Error reading file!")
                    return None

            except EOFError:
                print("End of file reached")
                break

            else:
                header.append(header_i)
                data.append({"PLASMA_FREQUENCY_NN": plasma_freq_nn,
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
                             "FIT_ACCUR_RMS": accur_rms})
                nsweep += 1

    name = 'WIND_WAVES_TNR_L3_BQT'
    meta = WIND_WAVES_TNR_L3_BQT_META

    return WindWavesData(os.path.basename(file_path), header, data, name, meta)


def read_wind_waves_radio_60s(file_path, verbose=False):
    """
    Method to read a Wind/Waves BQT data file from CDPP deep archive
    :param file_path: input file name (full path)
    :param verbose: optional flag to activate verbose mode
    :returns: a WindWavesData instance built from the input file.
    """

    ccsds_fields = ["CCSDS_PREAMBLE", "CCSDS_JULIAN_DAY_B1", "CCSDS_JULIAN_DAY_B2", "CCSDS_JULIAN_DAY_B3",
                    "CCSDS_MILLISECONDS_OF_DAY"]
    # CCSDS_PREAMBLE [Int, 8 bits] = 76
    # CCSDS_JULIAN_DAY [Int, 24 bits] = Days since 1950/01/01 (=1)
    # CCSDS_MILLISECONDS_OF_DAY [Int, 32 bits] = Millisecond of day
    ccsds_dtype = ">bbbbi"

    caldate_fields = ["CALEND_DATE_YEAR", "CALEND_DATE_MONTH", "CALEND_DATE_DAY", "CALEND_DATE_HOUR",
                      "CALEND_DATE_MINUTE", "CALEND_DATE_SECOND"]
    # CALEND_DATE fields YEAR, MONTH, DAY, HOUR, MINUTE, SECOND: all [Int, 16bits]
    caldate_dtype = "hhhhhh"

    header_fields = ccsds_fields + ["RECEIVER_CODE", "JULIAN_SEC"] + caldate_fields + \
        ["AVG_DURATION", "IUNIT", "NFREQ"]

    # RECEIVER_CODE [Int, 16 bits] = Name of Receiver: 0=TNR; 1=RAD1; 2=RAD2
    # JULIAN_SEC [Int, 32 bits] = Julian date of the middle of the 60-second interval (in seconds since 1950/01/01)

    orbit_fields = ["GSE_X", "GSE_Y", "GSE_Z"]
    # SPACECRAFT_COORDINATES fields GSE_X, GSE_Y, GSE_Z: all [Real, 32bits], in Earth Radii (GSE)
    orbit_dtype = ">fff"

    header_dtype = ccsds_dtype + "hi" + caldate_dtype + "hhh"

    header = []
    data = []
    orbit = []
    nsweep = 0

    with open(file_path, 'rb') as frb:
        while True:
            try:
                if verbose:
                    print("Reading sweep #{}".format(nsweep))

                # Reading number of octets in the current sweep
                block = frb.read(4)
                if len(block) == 0:
                    break
                loctets1 = struct.unpack('>i', block)[0]

                # Reading header parameters in the current sweep
                block = frb.read(32)
                header_i = dict(zip(header_fields, struct.unpack(header_dtype, block)))

                # Reading orbit data for current sweep
                block = frb.read(12)
                orbit_i = dict(zip(orbit_fields, struct.unpack(orbit_dtype, block)))

                # Reading frequency list in the current sweep
                nfreq = header_i["NFREQ"]
                block = frb.read(4 * nfreq)
                freq = struct.unpack('>' + 'f' * nfreq, block)

                # Reading frequency list in the current sweep
                block = frb.read(4 * nfreq)
                intensity = struct.unpack('>' + 'f' * nfreq, block)

                # Reading number of octets in the current sweep
                block = frb.read(4)
                loctets2 = struct.unpack('>i', block)[0]
                if loctets2 != loctets1:
                    print("Error reading file!")
                    return None

            except EOFError:
                print("End of file reached")
                break

            else:
                header.append(header_i)
                data.append({"FREQ": freq,
                             "INTENSITY": intensity})
                orbit.append(orbit_i)
                nsweep += 1

    name = 'WIND_WAVES_RADIO_60S'
    meta = WIND_WAVES_RADIO_60S_META

    return WindWavesData(os.path.basename(file_path), header, data, name, meta)


def read_wind_waves(file_path):
    """
    Generic method to read Wind/Waves data from CDPP deep archive, using file name convention to recognize data level
    :param file_path: path of the file to read
    :returns: a WindWavesData instance built from the input file
    """

    file_name = os.path.basename(file_path)
    file_extension = file_name.split('.')[1]
    file_name_elements = file_name.split('_')
    file_name_check = False
    result = None
    print("Processing file: {}".format(file_name))

    file_name_mis = "Unk"
    file_name_exp = "Unk"
    file_name_rec = "Unk"
    file_name_lev = "Unk"
    file_name_dat = "Unk"

    # Analyzing file name elements
    if file_name_elements[0] == 'WI':
        file_name_mis = 'Wind'
    elif file_name_elements[0] == 'WIN':
        file_name_mis = 'Wind'
    else:
        print("Unknown mission: '{}'".format(file_name_elements[0]))

    if file_name_elements[1] == 'WA':
        file_name_exp = 'Waves'
        if file_name_elements[2] == 'TNR':
            file_name_rec = 'TNR'
            if file_name_elements[3] == 'L3':
                file_name_lev = 'L3'
                if file_name_elements[4] == 'BQT':
                    file_name_dat = 'BQT'
                    if file_extension != 'DAT':
                        print("Wrong extension: '.{}' (expected '.DAT')".format(file_extension))
                    else:
                        file_name_check = True
                        print("Detected Wind/Waves/TNR/L3/BQT data.")
                        result = read_wind_waves_bqt(file_path)

                elif file_name_elements[4] == 'NN':
                    file_name_dat = 'NN'
                    if file_extension != 'DAT':
                        print("Wrong extension: '.{}' (expected '.DAT')".format(file_extension))
                    else:
                        file_name_check = True
                        print("Detected Wind/Waves/TNR/L3/NN data.")
                        result = read_wind_waves_nn(file_path)

                else:
                    print("Unknown dataset: '{}'".format(file_name_elements[4]))
            else:
                print("Unknown level: '{}'".format(file_name_elements[3]))
        else:
            print("Unknown receiver: '{}'".format(file_name_elements[2]))

    elif file_name_elements[1] == 'TNR':
        if file_name_elements[2] == '60S':
            file_name_exp = 'Waves'
            file_name_rec = 'TNR'
            file_name_lev = 'Average'
            file_name_dat = '60S'
            if file_extension != 'B3E':
                print("Wrong extension: '.{}' (expected '.B3E')".format(file_extension))
            else:
                file_name_check = True
                print("Detected Wind/Waves/TNR/60s data.")
                result = read_wind_waves_radio_60s(file_path)
        else:
            print("Unknown dataset: '{}'".format(file_name_elements[4]))

    elif file_name_elements[1] == 'RAD1':
        if file_name_elements[2] == '60S':
            file_name_exp = 'Waves'
            file_name_rec = 'RAD1'
            file_name_lev = 'Average'
            file_name_dat = '60S'
            if file_extension != 'B3E':
                print("Wrong extension: '.{}' (expected '.B3E')".format(file_extension))
            else:
                file_name_check = True
                print("Detected Wind/Waves/RAD1/60s data.")
                result = read_wind_waves_radio_60s(file_path)
        else:
            print("Unknown dataset: '{}'".format(file_name_elements[4]))

    elif file_name_elements[1] == 'RAD2':
        if file_name_elements[2] == '60S':
            file_name_exp = 'Waves'
            file_name_rec = 'RAD2'
            file_name_lev = 'Average'
            file_name_dat = '60S'
            if file_extension != 'B3E':
                print("Wrong extension: '.{}' (expected '.B3E')".format(file_extension))
            else:
                file_name_check = True
                print("Detected Wind/Waves/RAD2/60s data.")
                result = read_wind_waves_radio_60s(file_path)
        else:
            print("Unknown dataset: '{}'".format(file_name_elements[4]))

    else:
        print("Unknown receiver: '{}'".format(file_name_elements[2]))

    if file_name_check:
        print("Import result: {} {}/{}/{}/{} {} data records loaded (from {} file format)".
              format(len(result), file_name_mis, file_name_exp, file_name_rec, file_name_dat, file_name_lev,
                     file_extension))
    else:
        print("Import result: No data loaded.")

    return result
