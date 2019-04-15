#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read a DEMETER S/C data from CDPP deep archive (http://cdpp-archive.cnes.fr).
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__date__ = "30-MAR-2017"
__version__ = "0.02"

__all__ = ["CDPPDemeterN11134Data", "load_dmt_n1_1134_from_webservice", "read_dmt_n1_1134"]

import struct
import numpy
from maser.data import MaserError, MaserDataSweep
from maser.data.cdpp import CDPPDataFromFile, CDPPFileFromWebServiceSync
from .const import *


class CDPPDemeterN11134Sweep(MaserDataSweep):

    def __init__(self, parent, index, verbose=False, debug=False):

        if debug:
            print("### This is {}.__init__()".format(__class__.__name__))

        MaserDataSweep.__init__(self, parent, index, verbose, debug)

        self.data = self.parent.data[index]
        self.header = self.parent.header[index]
        self.freq = self.parent.get_frequency(index)


class CDPPDemeterN11134Data(CDPPDataFromFile):

    def __init__(self, file, verbose=False, debug=False):

        self.debug = debug
        if self.debug:
            print("This is {}.__init()".format(__class__.__name__))

        # Definition of data structure:
        # https://cdpp-archive.cnes.fr/project/data/documents/PLAS-DED-DMT_ICE-00535-CN/dmt_n1_1134_1.html

        ccsds_fields = ["CCSDS_PREAMBLE", "CCSDS_JULIAN_DAY_B1", "CCSDS_JULIAN_DAY_B2", "CCSDS_JULIAN_DAY_B3",
                        "CCSDS_MILLISECONDS_OF_DAY"]
        # CCSDS_PREAMBLE [Int, 8 bits] = 76
        # CCSDS_JULIAN_DAY [Int, 24 bits] = Days since 1950/01/01 (=1)
        # CCSDS_MILLISECONDS_OF_DAY [Int, 32 bits] = Millisecond of day
        ccsds_dtype = ">bbbbi"

        calend_fields = ["CALEND_YEAR", "CALEND_MONTH", "CALEND_DAY", "CALEND_HOUR", "CALEND_MINUTE", "CALEND_SECOND",
                         "CALEND_MILLISECOND"]
        # CALEND_DATE [7 * (16 bits Int)]
        calend_dtype = ">hhhhhhh"

        orbit_fields = ["ORBIT_NUMBER", "SUB_ORBIT_TYPE"]
        orbit_dtype = ">hh"
        # Next header word is TM_STATION: 8 char (64 bits)

        version_fields = ["SFT_VERSION", "SFT_SUB_VERSION", "CAL_VERSION", "CAL_SUB_VERSION"]
        version_dtype = ">bbbb"

        orb_param_fields = ["GEOC_LAT", "GEOC_LONG", "ALTITUDE", "LOCAL_TIME"]
        orb_param_dtype = ">ffff"

        geomag_param_fields = ["GEOMAG_LAT", "GEOMAG_LONG", "MLT", "INV_LAT", "MC_ILWAIN_L", "CONJSAT_GEOC_LAT",
                               "CONJSAT_GEOC_LONG", "NCONJ110_GEOC_LAT", "NCONJ110_GEOC_LONG", "SCONJ110_GEOC_LAT",
                               "SCONJ110_GEOC_LONG", "B_FIELD_MODEL_X", "B_FIELD_MODEL_Y", "B_FIELD_MODEL_Z",
                               "GYROFREQ"]
        geomag_param_dtype = ">fffffffffffffff"

        solar_param_fields = ["SOLAR_POSITION_X", "SOLAR_POSITION_Y", "SOLAR_POSITION_Z"]
        solar_param_dtype = ">fff"

        code_version_fields = ["SFT_VERSION", "SFT_SUB_VERSION"]
        code_version_dtype = ">bb"

        data_header_num_fields = ["NB", "NBF", "TOTAL_DUR", "FREQ_RES", "LOWER_FREQ", "UPPER_FREQ"]
        data_header_num_dtype = ">bhffff"

        header = []
        data = []
        nsweep = 0

        with open(file, 'rb') as frb:
            while True:
                try:
                    if verbose:
                        print("Reading sweep #{}".format(nsweep))

                    header_b1_i = dict()
                    # Reading Block_1 / CCSDS_date
                    block = frb.read(8)

                    # quick fix for triggering EOFError
                    if len(block) == 0:
                        raise EOFError

                    header_b1_i["CCSDS_DATE"] = dict(zip(ccsds_fields, struct.unpack(ccsds_dtype, block)))

                    # Reading Block_1 / Time_Orb_Info
                    block = frb.read(14)
                    header_b1_i["TIME_ORB_INFO"] = {"CALEND_DATE":
                                                        dict(zip(calend_fields, struct.unpack(calend_dtype, block)))}
                    block = frb.read(4)
                    header_b1_i["TIME_ORB_INFO"].update(dict(zip(orbit_fields, struct.unpack(orbit_dtype, block))))
                    block = frb.read(8)
                    header_b1_i["TIME_ORB_INFO"]['TM_STATION'] = block.decode('ascii')

                    # Reading Block_1 / Product_versions
                    block = frb.read(4)
                    header_b1_i["PRODUCT_VERSIONS"] = dict(zip(version_fields, struct.unpack(version_dtype, block)))

                    if debug:
                        print(header_b1_i)

                    header_b2_i = dict()
                    # Reading Block_2 / Orb_Param
                    block = frb.read(16)
                    header_b2_i["ORB_PARAM"] = dict(zip(orb_param_fields, struct.unpack(orb_param_dtype, block)))

                    # Reading Block_2 / Geomag_Param
                    block = frb.read(60)
                    header_b2_i["GEOMAG_PARAM"] = dict(zip(geomag_param_fields, struct.unpack(geomag_param_dtype, block)))

                    # Reading Block_2 / Solar_Param
                    block = frb.read(12)
                    header_b2_i["SOLAR_PARAM"] = dict(zip(solar_param_fields, struct.unpack(solar_param_dtype, block)))

                    # Reading Block_2 / Code_version
                    block = frb.read(2)
                    header_b2_i["CODE_VERSION"] = dict(zip(code_version_fields, struct.unpack(code_version_dtype, block)))

                    if debug:
                        print(header_b2_i)

                    header_b3_i = dict()
                    # Reading Block_3 / Att_Param
                    block = frb.read(36)
                    header_b3_i["M_SAT2GEO"] = numpy.array(struct.unpack(">fffffffff", block)).reshape((3, 3))
                    block = frb.read(36)
                    header_b3_i["M_GEO2LGM"] = numpy.array(struct.unpack(">fffffffff", block)).reshape((3, 3))
                    block = frb.read(2)
                    header_b3_i["QUALITY"] = struct.unpack(">h", block)

                    # Reading Block_3 / Code_version
                    block = frb.read(2)
                    header_b3_i["CODE_VERSION]"] = dict(zip(code_version_fields,
                                                            struct.unpack(code_version_dtype, block)))

                    if debug:
                        print(header_b3_i)

                    # Reading Block_4 / Data_Header
                    block = frb.read(21)
                    data_header_i = {"DATA_TYPE": block.decode('ascii')}
                    block = frb.read(32)
                    data_header_i["HK_TABLE"] = struct.unpack(">bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", block)
                    block = frb.read(9)
                    data_header_i["COORD_SYST"] = block.decode('ascii')
                    block = frb.read(3)
                    data_header_i["COMP_NAME"] = block.decode('ascii')
                    block = frb.read(16)
                    data_header_i["DATA_UNIT"] = block.decode('latin_1')
                    block = frb.read(19)
                    data_header_i.update(dict(zip(data_header_num_fields, struct.unpack(data_header_num_dtype, block))))
                    block = frb.read(14)
                    data_header_i["SP_CALEND_DATE"] = dict(zip(calend_fields, struct.unpack(calend_dtype, block)))

                    if debug:
                        print(data_header_i)

                    # Reading Block_4 / Power_Spectra_data
                    data_length = int(data_header_i["NB"]) * int(data_header_i["NBF"])
                    block = frb.read(data_length * 4)
                    data_dtype = ">{}".format(''.join(['f' for i in range(data_length)]))
                    data_i = {"POWER": numpy.array(struct.unpack(data_dtype, block)).\
                        reshape((int(data_header_i["NB"]),int(data_header_i["NBF"])))}

                except EOFError:
                    if verbose:
                        print("End of file reached")
                    break

                else:
                    header.append({"BLOCK_1": header_b1_i,
                                   "BLOCK_2": header_b2_i,
                                   "BLOCK_3": header_b3_i,
                                   "BLOCK_4": data_header_i})
                    data.append(data_i)
                    nsweep += 1

        name = 'DMT_N1_1134'
        meta = {
            "ORB_PARAM": DMT_ICE_N1_1134_ORB_PARAM_META,
            "GEOMAG_PARAM": DMT_ICE_N1_1134_GEOMAG_PARAM_META,
            "SOLAR_PARAM": DMT_ICE_N1_1134_SOLAR_PARAM_META,
            "ATT_PARAM": DMT_ICE_N1_1134_ATT_PARAM_META,
            "DATA_HEADER": DMT_ICE_N1_1134_DATA_HEADER_META,
            "POWER_SPECTRA": DMT_ICE_N1_1134_POWER_SPECTRA_META,
        }
        CDPPDataFromFile.__init__(self, file, header, data, name)
        self.meta = meta
        self.time = self.get_time_axis()
        self.nsweep = nsweep
        self.debug = debug
        self.verbose = verbose

    def get_time_axis(self):

        if self.debug:
            print("This is {}.get_time_axis()".format(__class__.__name__))

        return self.get_datetime_ccsds_cds(['BLOCK_1', 'CCSDS_DATE'])

    def get_single_datetime(self, index):

        if self.debug:
            print("This is {}.get_single_datetime()".format(__class__.__name__))

        return self.time[index]

    def get_single_sweep(self, cur_index=0, **kwargs):

        if self.debug:
            print("This is {}.get_single_sweep()".format(__class__.__name__))

        return CDPPDemeterN11134Sweep(self, cur_index, debug=self.debug, verbose=self.verbose)

    def get_frequency(self, cur_index=0):

        if self.debug:
            print("This is {}.get_frequency()".format(__class__.__name__))

        return numpy.linspace(self.header[cur_index]["BLOCK_4"]['LOWER_FREQ'],
                              self.header[cur_index]["BLOCK_4"]['UPPER_FREQ'],
                              num=self.header[cur_index]["BLOCK_4"]['NBF'])

    def __len__(self):

        if self.debug:
            print("This is {}.__len__()".format(__class__.__name__))

        return self.nsweep



def load_dmt_n1_1134_from_webservice(file_name, user='cecconi', password=None, check_file=True,
                                     verbose=False, debug=False):

    if debug:
        print("This is load_dmt_n1_1134_from_webservice()")

    f = CDPPFileFromWebServiceSync(file_name, 'DA_TC_DMT_N1_1134',
                                   user=user, password=password, check_file=check_file, debug=debug, verbose=verbose)

    return read_dmt_n1_1134(f.file, verbose=verbose, debug=debug)


def read_dmt_n1_1134(file_path, verbose=False, debug=False):
    """
    Method to read Demeter N1_1134 data from CDPP
    :param file_path: input file name
    :param debug: flag to activate debug mode (default = False)
    :param verbose: flag to activate verbose mode (default = False)
    :return: a DemeterN11134Data object
    """
    if debug:
        print("This is read_dmt_n1()")

    return CDPPDemeterN11134Data(file_path, verbose=verbose, debug=debug)


