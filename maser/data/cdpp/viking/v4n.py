#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read a Viking/V4n/E5 data file from CDPP deep archive (http://cdpp-archive.cnes.fr).
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__date__ = "10-JUL-2017"
__version__ = "0.11"

__all__ = ["VikingV4nData", "read_viking"]

# TODO: skip 1st record? => no, not for data downloaded from webservice...

import os
import struct
from maser.data.cdpp import CDPPDataFromFile
from .const import *


class VikingV4nData(CDPPDataFromFile):

    def __init__(self, file, header1, header2, header3, status, data, name, meta, orbit):
        CDPPDataFromFile.__init__(self, file, header1, data, name)
        self.header_v4l = header2
        self.header_v4h = header3
        self.status = status
        self.orbit = orbit
        self.meta = meta

    def __getitem__(self, item):
        if item == "DATETIME_UTC":
            return self.get_datetime(is_utc=True)
        else:
            return CDPPDataFromFile.__getitem__(self, item)

    def get_datetime(self, is_utc=False):
        if is_utc:
            return self.get_datetime_ccsds("UTC_P_Field", "UTC_T_Field")
        else:
            return self.get_datetime_ccsds()

    def getvar(self, var_name):
        """
        Method to retrieve the content of a variable
        :param var_name: Variable name
        :return: 
        """
        var_data = list()
        if self.name == "VIKING_V4":
            dataset_names = CDPPDataFromFile.getvar_names(self)
            for dataset in dataset_names:
                if var_name in self.meta[dataset].keys():
                    for cur_data in self.data:
                        var_data.append(cur_data[dataset][var_name])
        else:
            var_data = CDPPDataFromFile.getvar(self, var_name)
        return var_data

    def getvar_names(self):
        """
        Method to retrieve the variable names
        :return: 
        """
        if self.name == "VIKING_V4":
            dataset_names = CDPPDataFromFile.getvar_names(self)
            var_names = list()

            for dataset in dataset_names:
                var_names += self.meta[dataset].keys()

        else:
            var_names = self.meta.keys()
        return var_names

    def getvar_meta(self, var_name):
        """
        Method to retrieve the variable metadata
        :return: 
        """
        meta = None
        if self.name == "VIKING_V4":
            dataset_names = CDPPDataFromFile.getvar_names(self)
            for dataset in dataset_names:
                if var_name in self.meta[dataset].keys():
                    meta = self.meta[dataset][var_name]
        else:
            meta = self.meta[var_name]
        return meta

    def get_epncore_meta(self):
        md = CDPPDataFromFile.get_epncore_meta(self)
        md["time_min"] = self["DATETIME_UTC"][0]
        md["time_max"] = self["DATETIME_UTC"][-1]
        md["time_scale"] = "UTC"
        md["target_class"] = "planet"
        md["target_name"] = "Earth"
        md["target_region"] = "Magnetosphere"
        md["feature_name"] = "Auroral Kilometric Radiation#AKR"
        return md


def is_empty(data):
    if type(data) is dict:
        if all([v == 0 for v in data.values()]):
            return True
        elif all([v is None for v in data.values()]):
            return True
    elif (type(data) is list) or (type(data) is tuple) or (type(data) is set):
        if all([v == 0 for v in data]):
            return True
        elif all([v is None for v in data]):
            return True
    elif data is None:
        return True
    else:
        return False


def read_viking_v1_data(file_path, verbose=False):
    return read_viking(file_path, 'VIKING_V4_V1', verbose)


def read_viking_sfa_data(file_path, verbose=False):
    return read_viking(file_path, 'VIKING_V4H_SFA', verbose)


def read_viking_fbh_data(file_path, verbose=False):
    return read_viking(file_path, 'VIKING_V4H_FB', verbose)


def read_viking_fbl_data(file_path, verbose=False):
    return read_viking(file_path, 'VIKING_V4L_FBL', verbose)


def read_viking_v2_data(file_path, verbose=False):
    return read_viking(file_path, 'VIKING_V4_V2', verbose)


def read_viking_plasma_density_data(file_path, verbose=False):
    return read_viking(file_path, 'VIKING_V4L_Ni', verbose)


def read_viking_dft_data(file_path, verbose=False):
    return read_viking(file_path, 'VIKING_V4L_DFT', verbose)


def read_viking_wf_data(file_path, verbose=False):
    return read_viking(file_path, 'VIKING_V4L_WF', verbose)


def read_viking(file_path, dataset="VIKING_V4", verbose=False):
    """
    Method to read Viking V4 data from CDPP (E5 records)
    :param file_path: input file name
    :param dataset: name of the dataset to be extracted
    :param verbose: set to True for verbose output (default to False)
    :return: 
    """

    dataset_names = ["VIKING_V4", "VIKING_V4_V1", "VIKING_V4H_SFA", "VIKING_V4H_FB", "VIKING_V4L_FBL",
                     "VIKING_V4_V2", "VIKING_V4L_Ni", "VIKING_V4L_DFT", "VIKING_V4L_WF"]

    if dataset not in dataset_names:
        print("Wrong dataset name.")
        print("Allowed values = {}".format(', '.join(dataset_names)))
        return None
    else:
        print("Loading {} dataset.".format(dataset))

    header1_fields = ["RECORD_NUMBER"]
    header1_dtype = ">h"

    # WARNING: CNES/CDPP SCRIBE DESCRIPTOR IS WRONG -- CCSDS DAY_IN_YEAR_02 is not present
    # This dataset uses CCSDS-CCS Time Format.
    # year, month, day, hour, minute, second, CCSDS_B0*256 + CCSDS_B1
    header1_fields += ["CCSDS_PREAMBLE", "CCSDS_B0", "CCSDS_B1", "CCSDS_B2", "CCSDS_B3", "CCSDS_B4", "CCSDS_B5",
                       "CCSDS_B6", "CCSDS_B7", "CCSDS_B8"]
    header1_dtype += 'BBBBBBBBBB'

    header1_fields += ["CALENDAR_YEAR", "CALENDER_MONTH", "CALENDAR_DAY", "CALENDAR_HOUR",
                       "CALENDAR_MINUTE", "CALENDAR_SECOND", "CALENDAR_MILLI_SECOND"]
    header1_dtype += 'hhhhhhh'

    header1_fields += ["ORBIT_NUMBER", "SATELLITE_TIME_MSB", "SATELLITE_TIME_LSB"]
    header1_dtype += 'hii'

    # WARNING: UNUSED field is not present in header
    header1_fields += ["BUFFER_TYPE", "BUFFER_NUMBER", "SWEEP_NUMBER",
                       "COMPLETE_SWEEP", "SWEEP_DURATION", "NUMBER_OF_SERIES_IN_CURRENT_SWEEP",
                       "NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD", "ABNORMAL_END_OF_SWEEP"]
    header1_dtype += 'hhhhfhhh'

    header1_fields += ["TM_LACK_BEFORE_SWEEP", "TM_LACK_AFTER_SWEEP"]
    header1_dtype += 'hh'

    header1_fields += ["NUMBER_OF_RECORDS_IN_CURRENT_SWEEP", "RANK_OF_RECORD_IN_CURRENT_SWEEP"]
    header1_dtype += 'hh'

    # WARNING: NOT_MEANINGFUL field is not present in header
    header1_fields += ["V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP", "V4L_MODE_SWITCH_FLAGS_DURING_SWEEP",
                       "V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER"]
    header1_dtype += 'hhh'

    header1_fields += ["UTC_CCSDS_PREAMBLE", "UTC_CCSDS_B0", "UTC_CCSDS_B1", "UTC_CCSDS_B2",
                       "UTC_CCSDS_B3", "UTC_CCSDS_B4", "UTC_CCSDS_B5", "UTC_CCSDS_B6",
                       "UTC_CCSDS_B7", "UTC_CCSDS_B8"]
    header1_dtype += 'BBBBBBBBBB'

    # WARNING: CNES/CDPP SCRIBE DESCRIPTOR IS WRONG -- CCSDS DAY_IN_YEAR_02 is not present
    header1_fields += ["UTC_CALENDAR_YEAR", "UTC_CALENDER_MONTH", "UTC_CALENDAR_DAY", "UTC_CALENDAR_HOUR",
                       "UTC_CALENDAR_MINUTE", "UTC_CALENDAR_SECOND", "UTC_CALENDAR_MILLI_SECOND"]
    header1_dtype += 'hhhhhhh'
    header1_length = 92
    header1_spare_len = 36

    header2_fields = ["V4H_SFA_ELEMENT_NUMBER", "V4H_SFA_SWEEP_TYPE", "V4H_SFA_NUMBER_OF_FORMATS_IN_SWEEP",
                      "V4H_SFA_SWEEP_RANGE", "V4H_SFA_SWEEP_MODE", "V4H_SFA_ANTENNA",
                      "V4H_SFA_NUMBER_OF_FREQUENCY_STEPS", "V4H_SFA_NUMBER_OF_SAMPLES",
                      "GYROFREQUENCY", "V4H_FREQ_STEP_COEFF_MAG_OFFSET_KHZ_1", "V4H_FREQ_STEP_COEFF_MAG_OFFSET_KHZ_2",
                      "V4H_FREQ_STEP_COEFF_MAG_OFFSET_KHZ_3", "V4H_FREQ_STEP_COEFF_ELE_OFFSET_KHZ_1",
                      "V4H_FREQ_STEP_COEFF_ELE_OFFSET_KHZ_2", "V4H_FREQ_STEP_COEFF_ELE_OFFSET_KHZ_3",
                      "V4H_FREQ_STEP_SYNTH_INCREMENT"]  # V4H OPERATING MODE
    header2_dtype = '>hhhhhhhhffffffff'
    header2_length = 48
    header2_spare_len = 16

    header3_fields = ["V4L_MUX_1_POSITION", "V4L_MUX_2_POSITION", "V4L_TM_MODE", "V4L_DFT_FREQUENCY_RANGE",
                      "V4L_TIME_RESOLUTION_OF_DFT_SPECTRAL_DATA", "V4L_WF_FREQUENCY_RANGE",
                      "V4L_NUMBER_OF_DFT_SPECTRA", "V4L_NUMBER_OF_DFT_SAMPLES", "V4L_NUMBER_OF_SERIES_PER_WF_CHANNEL",
                      "V4L_NUMBER_OF_SAMPLES_PER_WF_CHANNEL"]  # V4L OPERATING MODE
    header3_dtype = '>hhhhhhhhhh'
    header3_length = 20
    header3_spare_len = 44

    data_v1_fields = ["V1_RELATIVE_TIME", "V1_EPAR", "V1_EC", "V1_ED", "V1_VFG", "V1_EPDIFF", "V1_USER_BIAS",
                      "V1_VGUARD", "V1_IFILL", "V1_ID"]
    data_v1_dtype = '>ffffffffhh'
    data_v1_length = 36
    data_v1_spare_len = 184

    orbit_fields = ["ORBIT_RELATIVE_TIME", "SPACECRAFT_GEOGRAPHIC_LAT", "SPACECRAFT_GEOGRAPHIC_LON",
                    "SPACECRAFT_GEOGRAPHIC_ALT", "SPACECRAFT_VEL_X", "SPACECRAFT_VEL_Y", "SPACECRAFT_VEL_Z",
                    "MAGNETIC_LOCAL_TIME", "INVARIANT_LATITUDE", "SPACECRAFT_ATTITUDE_BFIELD_SPEED_ANGLE",
                    "SPACECRAFT_ATTITUDE_SPIN_ANGLE"]
    orbit_dtype = ">fffffffffff"
    orbit_length = 44
    orbit_spare_len = 212

    data_v2_fields = ["V2_AMPLITUDE", "V2_PSI", "V2_PHI", "V2_THETA"]
    data_v2_dtype = '>ffff'
    data_v2_length = 16

    # Defining empty data dict templates

    data_v4_v1_empty = {"V1_RELATIVE_TIME": None,
                        "V1_EPAR": None,
                        "V1_EC": None,
                        "V1_ED": None,
                        "V1_VFG": None,
                        "V1_EPDIFF": None,
                        "V1_USER_BIAS": None,
                        "V1_VGUARD": None,
                        "V1_IFILL": None,
                        "V1_ID": None}

    data_v4_v2_empty = {"V2_AMPLITUDE": None,
                        "V2_PSI": None,
                        "V2_PHI": None,
                        "V2_THETA": None}

    data_v4h_sfa_empty = {"FREQUENCY_SFA": None,
                          "ELECTRIC_SFA": None,
                          "MAGNETIC_SFA": None}

    data_v4h_fb_empty = {"FREQUENCY_FB": None,
                         "MAGNETIC_FB": None,
                         "ELECTRIC_FB": None}

    data_v4l_fbl_empty = {"FREQUENCY_FBL": None,
                          "ELECTRIC_FBL": None}

    data_v4l_ni_empty = {"N1_PROBE": None,
                         "N2_PROBE": None}

    data_v4l_dft_empty = {"DFT": None}

    data_v4l_wf_empty = {"WF1": None,
                         "WF2": None}

    header = []
    header_v4l = []
    header_v4h = []
    status = []
    data = []
    orbit = []
    nsweep = 0
    name = dataset

    with open(file_path, 'rb') as frb:
        while True:
            read_index_start = frb.tell()
            try:
                if verbose:
                    print("Reading sweep #{}".format(nsweep))

                # Reading header1 parameters in the current record
                block = frb.read(header1_length)
                header1_i = dict(zip(header1_fields, struct.unpack(header1_dtype, block)))
                # => Here we fix the `P_Field` which is corrupted
                # we reverse the order of the bits in the byte
                header1_i['P_Field'] = int('{:08b}'.format(header1_i['CCSDS_PREAMBLE'])[::-1], 2)
                header1_i['T_Field'] = bytearray([header1_i['CCSDS_B0'], header1_i['CCSDS_B1'],
                                                  header1_i['CCSDS_B2'], header1_i['CCSDS_B3'],
                                                  header1_i['CCSDS_B4'], header1_i['CCSDS_B5'],
                                                  header1_i['CCSDS_B6'], header1_i['CCSDS_B7'],
                                                  header1_i['CCSDS_B8'],
                                                  ])
                header1_i['UTC_P_Field'] = int('{:08b}'.format(header1_i['UTC_CCSDS_PREAMBLE'])[::-1], 2)
                header1_i['UTC_T_Field'] = bytearray([header1_i['UTC_CCSDS_B0'], header1_i['UTC_CCSDS_B1'],
                                                      header1_i['UTC_CCSDS_B2'], header1_i['UTC_CCSDS_B3'],
                                                      header1_i['UTC_CCSDS_B4'], header1_i['UTC_CCSDS_B5'],
                                                      header1_i['UTC_CCSDS_B6'], header1_i['UTC_CCSDS_B7'],
                                                      header1_i['UTC_CCSDS_B8'],
                                                      ])
                frb.read(header1_spare_len)

                # Reading header2 parameters in the current record
                block = frb.read(header2_length)
                header2_i = dict(zip(header2_fields, struct.unpack(header2_dtype, block)))
                frb.read(header2_spare_len)

                # Reading header3 parameters in the current record
                block = frb.read(header3_length)
                header3_i = dict(zip(header3_fields, struct.unpack(header3_dtype, block)))
                frb.read(header3_spare_len)

                # Reading status data in the current record
                status_i = list()
                for i in range(16):
                    cur_stat = dict()
                    block = frb.read(16)
                    cur_stat["G"] = struct.unpack(">hhhhhhhh", block)
                    for j in range(3):
                        block = frb.read(16)
                        cur_stat["ST{}".format(j+8)] = struct.unpack(">hhhhhhhh", block)
                    for j in range(8):
                        block = frb.read(2)
                        cur_stat["ST{}".format(j)] = struct.unpack(">h", block)[0]
                    status_i.append(cur_stat)

                data_i = dict()

                # Reading Viking V1 data in the current record

                data_v1 = data_v4_v1_empty

                block = frb.read(data_v1_length)
                data_v1_tmp1 = dict(zip(data_v1_fields, struct.unpack(data_v1_dtype, block)))
                block = frb.read(data_v1_length)
                data_v1_tmp2 = dict(zip(data_v1_fields, struct.unpack(data_v1_dtype, block)))

                if not is_empty(data_v1_tmp1) or not is_empty(data_v1_tmp2):
                    for k in data_v1_fields:
                        data_v1[k] = list()
                        if not is_empty(data_v1_tmp1):
                            data_v1[k].append(data_v1_tmp1[k])
                        if not is_empty(data_v1_tmp2):
                            data_v1[k].append(data_v1_tmp2[k])

                frb.read(data_v1_spare_len)
                data_i["VIKING_V4_V1"] = data_v1

                # Reading Viking orbit data in the current record
                block = frb.read(orbit_length)
                orbit_i = dict(zip(orbit_fields, struct.unpack(orbit_dtype, block)))
                frb.read(orbit_spare_len)

                # Reading Viking V4H SFA data in the current record

                if is_empty(header2_i):
                    frb.read(3072)
                    data_i["VIKING_V4H_SFA"] = data_v4h_sfa_empty
                else:
                    block = frb.read(1024)
                    data_tmp = struct.unpack('>' + 'f' * 256, block)
                    if is_empty(data_tmp):
                        data_v4h_sfa_freq = None
                    else:
                        data_v4h_sfa_freq = data_tmp

                    block = frb.read(1024)
                    data_tmp = struct.unpack('>' + 'f' * 256, block)
                    if is_empty(data_tmp):
                        data_v4h_sfa_elec = None
                    else:
                        data_v4h_sfa_elec = data_tmp

                    block = frb.read(1024)
                    data_tmp = struct.unpack('>' + 'f' * 256, block)
                    if is_empty(data_tmp):
                        data_v4h_sfa_mag = None
                    else:
                        data_v4h_sfa_mag = data_tmp

                    if is_empty(data_v4h_sfa_elec) and is_empty(data_v4h_sfa_mag):
                        data_i["VIKING_V4H_SFA"] = data_v4h_sfa_empty
                    else:
                        data_i["VIKING_V4H_SFA"] = {"FREQUENCY_SFA": data_v4h_sfa_freq,
                                                    "ELECTRIC_SFA": data_v4h_sfa_elec,
                                                    "MAGNETIC_SFA": data_v4h_sfa_mag}

                # Reading Viking V4H Filter Bank in the current record

                if is_empty(header2_i):
                    frb.read(4096)
                    data_i["VIKING_V4H_FB"] = data_v4h_fb_empty
                else:
                    data_v4h_fbb = list()
                    data_v4h_fbe = list()
                    data_v4h_fbf = [2**(i+2) for i in range(8)]
                    for i in range(8):
                        block = frb.read(256)
                        data_tmp = struct.unpack('>' + 'f' * 64, block)
                        if is_empty(data_tmp):
                            data_v4h_fbb.append(None)
                        else:
                            data_v4h_fbb.append(data_tmp)
                    for i in range(8):
                        block = frb.read(256)
                        data_tmp = struct.unpack('>' + 'f' * 64, block)
                        if is_empty(data_tmp):
                            data_v4h_fbe.append(None)
                        else:
                            data_v4h_fbe.append(data_tmp)

                    if is_empty(data_v4h_fbb) and is_empty(data_v4h_fbe):
                        data_i["VIKING_V4H_FB"] = data_v4h_fb_empty
                    else:
                        data_i["VIKING_V4H_FB"] = {"FREQUENCY_FB": data_v4h_fbf, "MAGNETIC_FB": data_v4h_fbb,
                                                   "ELECTRIC_FB": data_v4h_fbe}

                # Reading Viking V4L Filter Bank in the current record

                if is_empty(header3_i):
                    frb.read(768)
                    data_i["VIKING_V4L_FBL"] = data_v4l_fbl_empty
                else:
                    data_v4l_fbl = list()
                    data_v4l_fbl_fmin = [200, 520, 1350]
                    data_v4l_fbl_fmax = [520, 1350, 3500]
                    data_v4l_fbl_freq = [(data_v4l_fbl_fmin[i] + data_v4l_fbl_fmax[i])/2 for i in range(3)]
                    for i in range(3):
                        block = frb.read(256)
                        data_tmp = struct.unpack('>' + 'f' * 64, block)
                        if is_empty(data_tmp):
                            data_v4l_fbl.append(None)
                        else:
                            data_v4l_fbl.append(data_tmp)

                    if is_empty(data_v4l_fbl):
                        data_i["VIKING_V4L_FBL"] = data_v4l_fbl_empty
                    else:
                        data_i["VIKING_V4L_FBL"] = {"FREQUENCY_FBL": data_v4l_fbl_freq,
                                                    "ELECTRIC_FBL": data_v4l_fbl}

                # Reading Viking V2 data in the current record
                data_i["VIKING_V4_V2"] = data_v4_v2_empty

                data_v2 = list()
                for i in range(16):
                    block = frb.read(data_v2_length)
                    data_tmp = dict(zip(data_v2_fields, struct.unpack(data_v2_dtype, block)))
                    if is_empty(data_tmp):
                        data_v2.append(None)
                    else:
                        data_v2.append(data_tmp)

                if is_empty(data_v2):
                    data_v2 = None

                data_i["VIKING_V4_V2"] = data_v2

                # Reading Viking V4L LP data in the current record

                if is_empty(header3_i):
                    frb.read(2048)
                    data_i["VIKING_V4L_Ni"] = data_v4l_ni_empty
                else:
                    block = frb.read(1024)
                    data_tmp = struct.unpack('>' + 'f' * 256, block)
                    if not is_empty(data_tmp):
                        data_v4l_n1 = data_tmp
                    else:
                        data_v4l_n1 = None

                    block = frb.read(1024)
                    data_tmp = struct.unpack('>' + 'f' * 256, block)
                    if not is_empty(data_tmp):
                        data_v4l_n2 = data_tmp
                    else:
                        data_v4l_n2 = None

                    if is_empty(data_v4l_n1) and is_empty(data_v4l_n2):
                        data_i["VIKING_V4L_Ni"] = data_v4l_ni_empty
                    else:
                        data_i["VIKING_V4L_Ni"] = {"N1_PROBE": data_v4l_n1, "N2_PROBE": data_v4l_n2}

                # Reading Viking V4L DFT/WF data in the current record
                data_v4l_dft_wh_bytes = 16384
                data_v4l_dft_wh_floats = data_v4l_dft_wh_bytes // 4

                block = frb.read(data_v4l_dft_wh_bytes)
                data_v4l_dft_wf = struct.unpack('>' + 'f' * data_v4l_dft_wh_floats, block)

                if is_empty(header3_i):

                    data_i["VIKING_V4L_DFT"] = data_v4l_dft_empty
                    data_i["VIKING_V4L_WF"] = data_v4l_wf_empty

                else:

                    cur_index = 0

                    if header3_i["V4L_TM_MODE"] == 0:

                        data_v4l_wf = data_v4l_wf_empty

                        if header3_i["V4L_NUMBER_OF_DFT_SPECTRA"] != 0:
                            print("Erroneous V4L_TM_MODE...")

                        data_v4l_wf["WF1"] = list()
                        data_v4l_wf["WF2"] = list()

                        n_wf = header3_i["V4L_NUMBER_OF_SERIES_PER_WF_CHANNEL"]
                        l_wf = header3_i["V4L_NUMBER_OF_SAMPLES_PER_WF_CHANNEL"] // n_wf

                        for i in range(n_wf):
                            data_v4l_wf["WF1"].append(data_v4l_dft_wf[cur_index:cur_index+l_wf])
                            cur_index = cur_index+l_wf

                        for i in range(n_wf):
                            data_v4l_wf["WF2"].append(data_v4l_dft_wf[cur_index:cur_index+l_wf])
                            cur_index = cur_index + l_wf

                        data_i["VIKING_V4L_WF"] = data_v4l_wf
                        data_i["VIKING_V4L_DFT"] = data_v4l_dft_empty

                    elif header3_i["V4L_TM_MODE"] == 1 or header3_i["V4L_TM_MODE"] == 3:

                        data_v4l_dft = data_v4l_dft_empty
                        data_v4l_dft["DFT"] = list()
                        data_v4l_wf = data_v4l_wf_empty
                        data_v4l_wf["WF1"] = list()
                        data_v4l_wf["WF2"] = list()

                        n_dft = header3_i["V4L_NUMBER_OF_DFT_SPECTRA"]
                        l_dft = header3_i["V4L_NUMBER_OF_DFT_SAMPLES"] // n_dft

                        n_wf = header3_i["V4L_NUMBER_OF_SERIES_PER_WF_CHANNEL"]
                        l_wf = header3_i["V4L_NUMBER_OF_SAMPLES_PER_WF_CHANNEL"] // n_wf

                        for i in range(n_dft):
                            data_v4l_dft["DFT"].append(data_v4l_dft_wf[cur_index:cur_index+l_dft])
                            cur_index = cur_index + l_dft

                        for i in range(n_wf):
                            data_v4l_wf["WF1"].append(data_v4l_dft_wf[cur_index:cur_index+l_wf])
                            cur_index = cur_index + l_wf

                        for i in range(n_wf):
                            data_v4l_wf["WF2"].append(data_v4l_dft_wf[cur_index:cur_index+l_wf])
                            cur_index = cur_index + l_wf

                        data_i["VIKING_V4L_DFT"] = data_v4l_dft
                        data_i["VIKING_V4L_WF"] = data_v4l_wf

                    elif header3_i["V4L_TM_MODE"] == 2:

                        data_v4l_dft = data_v4l_dft_empty
                        data_v4l_dft["DFT"] = list()

                        n_dft = header3_i["V4L_NUMBER_OF_DFT_SPECTRA"]
                        l_dft = int(header3_i["V4L_NUMBER_OF_DFT_SAMPLES"] / n_dft)

                        for i in range(n_dft):
                            data_v4l_dft["DFT"].append(data_v4l_dft_wf[cur_index:cur_index+l_dft])
                            cur_index = cur_index + l_dft

                        data_i["VIKING_V4L_DFT"] = data_v4l_dft
                        data_i["VIKING_V4L_WF"] = data_v4l_wf_empty

                    else:
                        print("Erroneous V4L_TM_MODE selector...")

                read_index_stop = frb.tell()
                if read_index_stop - read_index_start != 28672:
                    print("First byte of current record: {}".format(read_index_start))
                    print("Last byte of current record: {}".format(read_index_stop))
                    print("Number of bytes read for current record: {}".format(read_index_stop - read_index_start))
                    raise Exception('Wrong record length.')
                if read_index_stop == os.stat(file_path).st_size:
                    raise EOFError

            except EOFError:
                print("End of file reached")
                break

#            except Exception as inst:
#                print(inst)
#                import pdb
#                pdb.set_trace()

            else:

                nsweep += 1
                header.append(header1_i)
                header_v4l.append(header2_i)
                header_v4h.append(header3_i)
                status.append(status_i)
                orbit.append(orbit_i)
                if dataset != "VIKING_V4":
                    data.append(data_i[dataset])
                else:
                    data.append(data_i)

    meta = {"VIKING_V4_V1": VIKING_V1_META,
            "VIKING_V4H_SFA": VIKING_V4H_SFA_META,
            "VIKING_V4H_FB": VIKING_V4H_FB_META,
            "VIKING_V4L_FBL": VIKING_V4L_FBL_PHYS_META,
            "VIKING_V4_V2": VIKING_V2_META,
            "VIKING_V4L_Ni": VIKING_V4L_NI_META,
            "VIKING_V4L_DFT": VIKING_V4L_DFT_PHYS_META,
            "VIKING_V4L_WF": VIKING_V4L_WF_PHYS_META}

    if dataset != "VIKING_V4":
        meta = meta[dataset]

    return VikingV4nData(os.path.basename(file_path), header, header_v4l, header_v4h, status, data, name, meta, orbit)
