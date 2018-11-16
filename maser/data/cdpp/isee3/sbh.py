#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read a ISEE3/SBH data file from CDPP deep archive (http://cdpp-archive.cnes.fr).
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__date__ = "10-JUL-2017"
__version__ = "0.10"

__all__ = ["ISEE3SBHData", "read_isee3_sbh_3d_radio_source"]

import struct
import os
from maser.data.cdpp import CDPPDataFromFile
from .const import *


class ISEE3SBHData(CDPPDataFromFile):

    def __init__(self, file, header, data, name, meta, orbit):
        CDPPDataFromFile.__init__(self, file, header, data, name)
        self.meta = meta
        self.orbit = orbit

    def get_datetime(self):
        return self.get_datetime_ccsds()


def read_isee3_sbh_3d_radio_source(file_path, verbose=False):
    """
    Method to read ISEE3/SBH 3D Radio Source data file from CDPP/CNES deep archive
    :param file_path:
    :param verbose:
    :return:
    """

    header_fields = ["JULIAN_SECOND", "MILLI_SECOND"]
    header_dtype = ">ih"
    header_length = 6

    header_fields += ["CALEND_YEAR", "CALEND_MONTH", "CALEND_DAY", "CALEND_HOUR", "CALEND_MINUTE", "CALEND_SECOND"]
    header_dtype += "hhhhhh"
    header_length += 12

    header_fields += ["CCSDS_PREAMBLE", "CCSDS_B0", "CCSDS_B1", "CCSDS_B2", "CCSDS_B3", "CCSDS_B4", "CCSDS_B5",
                      "CCSDS_B6", "CCSDS_B7", "CCSDS_B8"]
    header_dtype += 'BBBBBBBBBB'
    header_length += 10

    header_fields += ["DATA_RATE", "RECEIVER_MODE", "S_ANTENNA"]
    header_dtype += 'hhh'
    header_length += 6

    header_fields += ["MINOR_FRAME_DURATION", "SUN_S_ANTENNA_TIME", "SPIN_PERIOD", "CYCLE_DURATION", "STEP_DURATION",
                      "S_SAMPLE_INTERVAL"]
    header_dtype += "ffffff"
    header_length += 24

    header_fields += ["N_MEAS_STEP", "N_FREQ_PER_MEAS_STEP", "N_FREQ_STEP", "N_S", "N_Z", "N_PHI"]
    header_dtype += "hhhhhh"
    header_length += 12

    header_fields += ["DSC_27", "DSC_28", "DSC_29"]
    header_dtype += "hhh"
    header_length += 6

    header_fields += ["SUN_TIME", "SUN_PERIOD"]
    header_dtype += "hh"
    header_length += 4

    header_fields += ["SPACECRAFT_POSITION_X", "SPACECRAFT_POSITION_Y", "SPACECRAFT_POSITION_Z"]
    header_dtype += "fff"
    header_length += 12

    header_fields += ["TIME_QUALITY", "CYCLE_NUMBER", "TM_FORMAT", "NUMBER_OF_OK_STEPS"]
    header_dtype += "hhhh"
    header_length += 8

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
                block = frb.read(header_length)
                header_i = dict(zip(header_fields, struct.unpack(header_dtype, block)))

                # => Here we fix the `P_Field` which is corrupted
                # first we reverse the order of the bits in the byte
                P_Field_tmp = int('{:08b}'.format(header_i['CCSDS_PREAMBLE'])[::-1], 2)
                # Then we put back the initial 0-2 bits into bits 5-7 (defining the resolution)
                # as those bits are not in reverse order in the file...
                P_Field_tmp = (P_Field_tmp & 31) + (header_i['CCSDS_PREAMBLE'] & 7)*32

                header_i['P_Field'] = P_Field_tmp
                if header_i['CCSDS_PREAMBLE'] == 80:
                    header_i['T_Field'] = bytearray([header_i['CCSDS_B0'], header_i['CCSDS_B1'],
                                                     header_i['CCSDS_B2'], header_i['CCSDS_B3'],
                                                     header_i['CCSDS_B4'], header_i['CCSDS_B5'],
                                                     header_i['CCSDS_B6'],
                                                     ])
                elif header_i['CCSDS_PREAMBLE'] == 81:
                    header_i['T_Field'] = bytearray([header_i['CCSDS_B0'], header_i['CCSDS_B1'],
                                                     header_i['CCSDS_B2'], header_i['CCSDS_B3'],
                                                     header_i['CCSDS_B4'], header_i['CCSDS_B5'],
                                                     header_i['CCSDS_B6'], header_i['CCSDS_B7'],
                                                     ])
                elif header_i['CCSDS_PREAMBLE'] == 82:
                    header_i['T_Field'] = bytearray([header_i['CCSDS_B0'], header_i['CCSDS_B1'],
                                                     header_i['CCSDS_B2'], header_i['CCSDS_B3'],
                                                     header_i['CCSDS_B4'], header_i['CCSDS_B5'],
                                                     header_i['CCSDS_B6'], header_i['CCSDS_B7'],
                                                     header_i['CCSDS_B8'],
                                                     ])
                else:
                    raise Exception('Wrong CCSDS P_Field for this dataset')

                orbit_i = {"SC_GSE_X": header_i["SPACECRAFT_POSITION_X"],
                           "SC_GSE_Y": header_i["SPACECRAFT_POSITION_Y"],
                           "SC_GSE_Z": header_i["SPACECRAFT_POSITION_Z"]}

                # Reading Measurements in current sweep
                data_i = dict()
                data_i["FREQUENCY"] = list()
                data_i["BANDWIDTH"] = list()
                data_i["DATA_QUALITY"] = list()
                data_i["TIME"] = list()
                data_i["S_DATA"] = list()
                data_i["Z_DATA"] = list()
                data_i["PHI_DATA"] = list()

                for i in range(header_i["N_FREQ_STEP"]):

                    block = frb.read(10)
                    cur_freq, cur_band, cur_qual, cur_time = struct.unpack(">hhhf", block)
                    data_i["FREQUENCY"].append(cur_freq)
                    data_i["BANDWIDTH"].append(cur_band)
                    data_i["DATA_QUALITY"].append(cur_qual)
                    data_i["TIME"].append(cur_time)

                    block = frb.read(4 * header_i["N_S"])
                    cur_s = struct.unpack(">" + "f" * header_i["N_S"], block)
                    data_i["S_DATA"].append(cur_s)

                    block = frb.read(4 * header_i["N_Z"])
                    cur_z = struct.unpack(">" + "f" * header_i["N_Z"], block)
                    data_i["Z_DATA"].append(cur_z)

                    block = frb.read(2 * header_i["N_PHI"])
                    cur_phi = struct.unpack(">" + "h" * header_i["N_PHI"], block)
                    data_i["PHI_DATA"].append(cur_phi)

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
                orbit.append(orbit_i)
                nsweep += 1

    name = "ISEE3_SBH_3D_RADIO_SOURCE"
    meta = ISEE3_SBH_3D_RADIO_SOURCE_META

    return ISEE3SBHData(os.path.basename(file_path), header, data, name, meta, orbit)