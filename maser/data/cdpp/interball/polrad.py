#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read a INTERBALL Auroral S/C data from CDPP deep archive (http://cdpp-archive.cnes.fr).
@author: B.Cecconi(LESIA)
"""

import struct
import numpy
from maser.data.cdpp import CDPPDataFromFile, CDPPFileFromWebServiceSync
from maser.data.data import MaserError, MaserDataSweep

__author__ = "Baptiste Cecconi"
__date__ = "26-MAR-2018"
__version__ = "0.12"

__all__ = ["load_int_aur_polrad_from_webservice", "read_int_aur_polrad"]


class CDPPInterballAuroralPOLRADRSPSweep(MaserDataSweep):

    def __init__(self, parent, index, verbose=False, debug=False):

        if debug:
            print("### This is {}.__init__()".format(__class__.__name__))

        MaserDataSweep.__init__(self, parent, index, verbose, debug)

        self.data = self.parent.data[index]
        self.header = self.parent.header[index]
        self.freq = self.parent.get_frequency(index)

    def get_datetime(self):

        if self.debug:
            print("### This is {}.get_datetime()".format(__class__.__name__))

        return self.parent.get_single_datetime(self.index)


class CDPPInterballAuroralPOLRADRSPData(CDPPDataFromFile):

    def __init__(self, file, verbose=False, debug=False):

        self.debug = debug
        if self.debug:
            print("This is {}.__init()".format(__class__.__name__))

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

        with open(file, 'rb') as frb:
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
                        raise MaserError("Error reading file!")

                except EOFError:
                    if verbose:
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

        CDPPDataFromFile.__init__(self, file, header, data, name)
        self.meta = meta
        self.time = self.get_time_axis()
        self.nsweep = nsweep
        self.debug = debug
        self.verbose = verbose

    def decode_session_name(self):

        if self.debug:
            print("This is {}.decode_session_name()".format(__class__.__name__))

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

    def get_time_axis(self):

        if self.debug:
            print("This is {}.get_time_axis()".format(__class__.__name__))

        return self.get_datetime_ccsds_cds()

    def get_single_datetime(self, index):

        if self.debug:
            print("This is {}.get_single_datetime()".format(__class__.__name__))

        return self.time[index]

    def getvar_meta(self, var_name):
        """
        Method to retrieve the variable metadata
        :return:
        """

        if self.debug:
            print("This is {}.getvar_meta()".format(__class__.__name__))

        return self.meta[var_name]

    def get_frequency(self, cur_index=0):

        if self.debug:
            print("This is {}.get_frequency()".format(__class__.__name__))

        return numpy.flipud(numpy.arange(self.header[cur_index]['STEPS'])*4.096 + 4.096)

    def get_single_sweep(self, cur_index):

        if self.debug:
            print("This is {}.get_single_sweep()".format(__class__.__name__))

        return CDPPInterballAuroralPOLRADRSPSweep(self, cur_index, debug=self.debug, verbose=self.verbose)

    def get_epncore_meta(self):

        if self.debug:
            print("This is {}.get_epncore_meta()".format(__class__.__name__))

        md = CDPPDataFromFile.get_epncore_meta(self)
        md["target_class"] = "planet"
        md["target_name"] = "Earth"
        md["target_region"] = "Magnetosphere"
        md["feature_name"] = "Auroral Kilometric Radiation#AKR"
        return md


def load_int_aur_polrad_from_webservice(file_name, user=None, password=None, check_file=True,
                                        verbose=False, debug=False):

    if debug:
        print("This is load_int_aur_polrad_from_webservice()")

    f = CDPPFileFromWebServiceSync(file_name, 'DA_TC_INT_AUR_POLRAD_RSP',
                                   user=user, password=password, check_file=check_file, debug=debug, verbose=verbose)
    return read_int_aur_polrad(f.file, verbose=verbose, debug=debug)


def read_int_aur_polrad(file_path, verbose=False, debug=False):

    if debug:
        print("This is read_int_aur_polrad()")

    return CDPPInterballAuroralPOLRADRSPData(file_path, verbose=verbose, debug=debug)
