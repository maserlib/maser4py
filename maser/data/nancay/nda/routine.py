#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to work with SRN/NDA/Routine data
@author: B.Cecconi(LESIA)
"""

import datetime
import os
from maser.data.nancay.nda.nda import *

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2017, LESIA-PADC-USN, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi", "Andree Coffre", "Laurent Lamy"]
__license__ = "GPLv3"
__version__ = "2.0b0"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Production"
__date__ = "30-JUL-2017"
__project__ = "MASER/SRN/NDA"

__all__ = ["NDARoutineData"]


class NDARoutineData(NDAData):

    def __init__(self, file, debug=False):
        header = {}
        data = []
        name = "SRN/NDA Routine Dataset"
        meta = {}
        NDAData.__init__(self, file, header, data, name)
        self.file_info = {'name': self.file, 'size': self.file_size(), 'file_data_offset': 0}
        self.detect_format()
        self.set_filedate()
        self.debug = debug
        self.header = self.header_from_file()
        self.meta = meta
        self.cur_ptr_in_file = 0

    def detect_format(self):
        try:
            if self.file.endswith('.RT1'):
                self.file_into['format'] = 'RT1'
                self.file_info['record_size'] = 405
            elif self.file.endswith('.cdf'):
                self.file_info['format'] = 'CDF'
            else:
                raise WrongFormatException('Unknown file Extension')

        except WrongFormatException as e:
            print("Error in nda.routine.detect_format()")
            print("Trying: {}".format(self.file))
            print(e)

    def set_filedate(self):
        try:
            if self.file_info['format'] == 'RT1':
                filedate = ((os.path.basename(self.file).split('.'))[0])[1:7]
                if int(filedate[0:2]) < 90:
                    century_str = '20'
                else:
                    century_str = '19'
                self.file_info['filedate'] = century_str + filedate
            else:
                raise NotImplemented("Format {} not implemented yet")

        except NotImplemented as e:
            print("Error in nda.routine.set_filedate()")
            print("Trying: {}".format(self.file))
            print(e)

    def header_from_file(self):
        try:
            if self.file_info['format'] == 'RT1':
                return self.header_from_rt1()
            else:
                raise NotImplemented("Format {} not implemented yet")

        except NotImplemented as e:
            print("Error in nda.routine.header_from_file()")
            print("Trying: {}".format(self.file))
            print(e)

    def header_from_rt1(self):
        """
        Decodes the RT1 file header (format 1, see SRN NDA ROUTINE JUP documentation)
        :param self:
        :return header: Header data dictionary
        """

        with open(self.file, 'rb') as f:
            self.file_info['header_raw'] = f.read(self.file_info['record_size'])

            if int(self.file_info['filedate']) < 19901127:
                self.file_info['header_version'] = 1
                header = self.header_from_rt1_format_1()
            elif int(self.file_info['filedate']) < 19940224:
                self.file_info['header_version'] = 2
                header = self.header_from_rt1_format_2()
            elif int(self.file_info['filedate']) < 19990119:
                self.file_info['header_version'] = 3
                header = self.header_from_rt1_format_3()
            elif int(self.file_info['filedate']) < 20001101:
                self.file_info['header_version'] = 4
                header = self.header_from_rt1_format_4()
            elif int(self.file_info['filedate']) < 20090922:
                self.file_info['header_version'] = 5
                header = self.header_from_rt1_format_5()
            else:
                self.file_info['header_version'] = 6
                header = self.header_from_rt1_format_6()

        print('Header version is {}'.format(self.file_info['header_version']))
        return header


    def header_from_rt1_format_1(self):

        raw = self.file_info['header_raw']
        header = dict()
        header['freq_min'] = raw[1:3]  # MHz
        header['freq_max'] = raw[3:5]  # MHz
        header['freq_res'] = raw[5:8]  # kHz
        header['ref_levl'] = raw[8:11]  # dBm
        header['swp_time'] = raw[11:14]  # ms
        header['powr_res'] = raw[14:16]  # dB/div
        return header

    def header_from_rt1_format_2(self):

        raw = self.file_info['header_raw']
        header = self.header_from_rt1_format_1()
        header['merid_hh'] = raw[16:18]  # hour
        header['merid_mm'] = raw[18:20]  # minute
        return header

    def header_from_rt1_format_3(self):

        raw = self.file_info['header_raw']
        header = self.header_from_rt1_format_1()
        header['swp_time'] = raw[13:16]  # ms
        header['powr_res'] = raw[16:18]  # dB/div
        header['merid_hh'] = raw[18:20]  # hour
        header['merid_mm'] = raw[20:22]  # minute
        return header

    def header_from_rt1_format_4(self):

        raw = self.file_info['header_raw']
        header = self.header_from_rt1_format_3()
        header['swp_time'] = raw[11:16]  # ms
        return header

    def header_from_rt1_format_5(self):

        raw = self.file_info['header_raw']
        header = self.header_from_rt1_format_4()
        header['rf0_sele'] = raw[22:23]  # RF Filter 0 (selected at start of observations)
        header['rf0_hour'] = raw[23:25]  # Start for RF filter 0 (hours)
        header['rf0_minu'] = raw[26:28]  # Start for RF filter 0 (minutes)
        header['rf1_sele'] = raw[28:29]  # RF Filter 1
        header['rf1_hour'] = raw[29:31]  # Start for RF filter 1 (hours)
        header['rf1_minu'] = raw[32:34]  # Start for RF filter 1 (minutes)
        header['rf2_sele'] = raw[34:35]  # RF Filter 2
        header['rf2_hour'] = raw[35:37]  # Start for RF filter 2 (hours)
        header['rf2_minu'] = raw[38:40]  # Start for RF filter 2 (minutes)
        return header

    def header_from_rt1_format_6(self):

        raw = self.file_info['header_raw']
        header = self.header_from_rt1_format_5()
        header['merid_dd'] = raw[41:43]  # Meridian date (day)
        header['merid_mo'] = raw[44:46]  # Meridian date (month)
        header['merid_yr'] = raw[47:49]  # Meridian date (year)
        header['start_dd'] = raw[50:52]  # Observation start date (day)
        header['start_mo'] = raw[53:55]  # Observation start date (month)
        header['start_yr'] = raw[56:58]  # Observation start date (year)
        header['h_stp_hh'] = raw[59:61]  # Observation stop time (hours)
        header['h_stp_mm'] = raw[62:64]  # Observation stop time (minutes)
        return header

