#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read a INTERBALL Auroral S/C data from CDPP deep archive (http://cdpp-archive.cnes.fr).
@author: B.Cecconi(LESIA)
"""

import struct
from maser.data.cdpp.cdpp import *

__author__ = "Baptiste Cecconi"
__date__ = "10-JUL-2017"
__version__ = "0.11"

__all__ = ["InterballAuroralData", "read_int_aur_polrad"]


class InterballAuroralData(CDPPData):

    def __init__(self, header, data, name, meta):
        CDPPData.__init__(self, header, data)
        self.name = name
        self.meta = meta

    def decode_session_name(self):

        result = list()

        for cur_hdr in self.header:

            session_name = cur_hdr["SESSION_NAME"]

            tmp = dict()

            tmp["YEAR"] = int(session_name[0])
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

            result.append(tmp)

        return result

    def get_datetime(self):
        return self.get_datetime_ccsds_cds()

    def getvar_meta(self, var_name):
        """
        Method to retrieve the variable metadata
        :return: 
        """
        return self.meta[var_name]


def read_int_aur_polrad(file_path, verbose=False):
    """
    Method to read Interball Auroral POLRAD data from CDPP 
    :param file_path: input file name
    :param verbose: flag to activate verbose mode (default = False)
    :return: 
    """

    ccsds_fields = ["CCSDS_PREAMBLE", "CCSDS_JULIAN_DAY_B1", "CCSDS_JULIAN_DAY_B2", "CCSDS_JULIAN_DAY_B3",
                    "CCSDS_MILLISECONDS_OF_DAY"]
    # CCSDS_PREAMBLE [Int, 8 bits] = 76
    # CCSDS_JULIAN_DAY [Int, 24 bits] = Days since 1950/01/01 (=1)
    # CCSDS_MILLISECONDS_OF_DAY [Int, 32 bits] = Millisecond of day
    ccsds_dtype = ">bbbbi"

    header_fields = ccsds_fields
    header_dtype = ccsds_dtype

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
                block = frb.read(8)
                header_i = dict(zip(header_fields, struct.unpack(header_dtype, block)))
                block = frb.read(8)
                header_i["SESSION_NAME"] = block

                # Reading SFA_DATA configuration for the current sweep
                block = frb.read(20)
                steps, first_freq, channels, sweep_duration, attenuation = struct.unpack('>ififi', block)
                header_i["STEPS"] = steps
                header_i["FIRST_FREQ"] = first_freq
                header_i["CHANNELS"] = channels
                header_i["SWEEP_DURATION"] = sweep_duration
                header_i["ATTENUATION"] = attenuation

                # Reading SFA_DATA for current sweep
                data_i = dict()
                if header_i["CHANNELS"] == 1:
                    data_i["EX"] = list()
                    data_i["EZ"] = list()
                    block = frb.read(4 * header_i["STEPS"])
                    data_i["EY"] = struct.unpack('>' + 'f' * header_i["STEPS"], block)
                elif header_i["CHANNELS"] == 3:
                    block = frb.read(4 * header_i["STEPS"])
                    data_i["EX"] = struct.unpack('>' + 'f' * header_i["STEPS"], block)
                    block = frb.read(4 * header_i["STEPS"])
                    data_i["EY"] = struct.unpack('>' + 'f' * header_i["STEPS"], block)
                    block = frb.read(4 * header_i["STEPS"])
                    data_i["EZ"] = struct.unpack('>' + 'f' * header_i["STEPS"], block)

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
                data.append(data_i)
                nsweep += 1

    name = 'INT_AUR_POLRAD_RSP'

    meta = {"FREQ": {"unit": "kHz", "description": "Frequency"},
            "EX": {"unit": "W/m^2/Hz", "description": "Flux Density on Antenna EX"},
            "EY": {"unit": "W/m^2/Hz", "description": "Flux Density on Antenna EY"},
            "EZ": {"unit": "W/m^2/Hz", "description": "Flux Density on Antenna EZ"}}

    return InterballAuroralData(header, data, name, meta)
