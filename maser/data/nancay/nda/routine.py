#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to work with SRN/NDA/Routine data
@author: B.Cecconi(LESIA)
"""

import struct
import datetime
import os
from maser.data.nancay.nda.nda import *

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2017, LESIA-PADC-USN, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi", "Andree Coffre", "Laurent Lamy"]
__license__ = "GPLv3"
__version__ = "2.0b1"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Production"
__date__ = "06-SEP-2017"
__project__ = "MASER/SRN/NDA"

__all__ = ["NDARoutineData", "NDARoutineSweep", "NDARoutineError"]


class NDARoutineError(NDAError):
    pass


class NDARoutineData(NDAData):

    def __init__(self, file, debug=False):
        header = {}
        data = []
        name = "SRN/NDA Routine Dataset"
        NDAData.__init__(self, file, header, data, name)
        self.file_info = {'name': self.file, 'size': self.get_file_size()}
        self.detect_format()
        self.set_filedate()
        self.debug = debug
        self.header = self.header_from_file()
        meta = dict()
        meta['obsty_id'] = 'srn'
        meta['instr_id'] = 'nda'
        meta['recvr_id'] = 'routine'
        meta['freq_min'] = float(self.header['freq_min'])  # MHz
        meta['freq_max'] = float(self.header['freq_max'])  # MHz
        meta['freq_len'] = 400
        meta['freq_stp'] = (meta['freq_max']-meta['freq_min'])/0.4  # kHz
        meta['freq_res'] = float(self.header['freq_res'])  # kHz
        self.meta = meta

    def __len__(self):
        if self.file_info['format'] == 'RT1':
            return self.get_file_size()//self.file_info['record_size'] - 1
        else:
            raise NDAError("NDA/Routine: Format {} not implemented yet".format(self.file_info['format']))

    def detect_format(self):
        if self.file.endswith('.RT1'):
            self.file_info['format'] = 'RT1'
            self.file_info['record_size'] = 405
            self.file_info['data_offset_in_file'] = self.file_info['record_size']
        elif self.file.endswith('.cdf'):
            self.file_info['format'] = 'CDF'
        else:
            raise NDAError('NDA/Routine: Unknown file Extension')

    def set_filedate(self):
        if self.file_info['format'] == 'RT1':
            filedate = ((os.path.basename(self.file).split('.'))[0])[1:7]
            if int(filedate[0:2]) < 90:
                century_str = '20'
            else:
                century_str = '19'
            self.file_info['filedate'] = century_str + filedate
        else:
            raise NDAError("NDA/Routine: Format {} not implemented yet".format(self.file_info['format']))

    def header_from_file(self):
        if self.file_info['format'] == 'RT1':
            return self.header_from_rt1()
        else:
            raise NDAError("NDA/Routine: Format {} not implemented yet".format(self.file_info['format']))

    def header_from_rt1(self):
        """
        Decodes the RT1 file header (format 1, see SRN NDA ROUTINE JUP documentation)
        :param self:
        :return header: Header data dictionary
        """

        with open(self.file, 'rb') as f:
            self.file_info['header_raw'] = f.read(self.file_info['record_size'])
            self.fix_corrupted_header()

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

        if self.debug:
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

    def fix_corrupted_header(self):
        if self.file_info['filedate'] == '19910725':
            self.file_info['header_raw'] = "{}08{}".format(self.file_info['header_raw'][0:18],
                                                           self.file_info['header_raw'][20:])
        elif self.file_info['filedate'] == '19940224':
            self.file_info['header_raw'] = "{}0426{}".format(self.file_info['header_raw'][0:18],
                                                             self.file_info['header_raw'][22:])
        elif self.file_info['filedate'] == '19940305':
            self.file_info['header_raw'] = "{}0351{}".format(self.file_info['header_raw'][0:18],
                                                             self.file_info['header_raw'][22:])
        elif self.file_info['filedate'] == '19940306':
            self.file_info['header_raw'] = "{}0347{}".format(self.file_info['header_raw'][0:18],
                                                             self.file_info['header_raw'][22:])

    def fix_old_version_header(self):
        if self.file_info['header_version'] == 1:
            self.header['merid_hh'] = 0  # hour
            self.header['merid_mm'] = 0  # minute
        if self.file_info['header_version'] < 5:
            first_sweep_time = self.get_first_sweep().get_time()
            self.header['rf0_hour'] = first_sweep_time.hour  # Start for RF filter 0 (hours)
            self.header['rf0_minu'] = first_sweep_time.minute  # Start for RF filter 0 (minutes)
        if self.file_info['header_version'] < 6:
            self.header['merid_dd'] = self.file_info['filedate'][6:8]  # Meridian date (day)
            self.header['merid_mo'] = self.file_info['filedate'][4:6]  # Meridian date (month)
            self.header['merid_yr'] = self.file_info['filedate'][2:4]  # Meridian date (year)
            first_sweep_time = self.get_first_sweep().get_time()
            last_sweep_time = self.get_last_sweep().get_time()
            meridian_time = self.get_meridian_time()
            start_date = datetime.date(int(self.header['merid_yr']),
                                       int(self.header['merid_mo']),
                                       int(self.header['merid_dd']))
            if last_sweep_time < first_sweep_time:
                if meridian_time < first_sweep_time:
                    start_date = start_date - datetime.timedelta(days=1)
            self.header['start_dd'] = start_date.day  # Observation start date (day)
            self.header['start_mo'] = start_date.month  # Observation start date (month)
            self.header['start_yr'] = start_date.year  # Observation start date (year)
            self.header['h_stp_hh'] = last_sweep_time.hour  # Observation stop time (hours)
            self.header['h_stp_mm'] = last_sweep_time.minute  # Observation stop time (minutes)

    def get_start_date(self):
        if int(self.header['start_yr']) < 90:
            year_offset = 2000
        else:
            year_offset = 1900
        return datetime.date(int(self.header['start_yr'])+year_offset,
                             int(self.header['start_mo']), int(self.header['start_dd']))

    def get_meridian_datetime(self, from_file=True):
        meridian_dt = None
        if from_file:
            meridian_dt = datetime.datetime.strptime(self.file_info['filedate'], '%Y%m%d') + \
                          datetime.timedelta(hours=int(self.header['merid_hh']), minutes=int(self.header['merid_mm']))
        else:
            NDARoutineError("Ephemeris from IMCCE webservice not implemented yet")

        return meridian_dt

    def get_meridian_time(self):
        return self.get_meridian_datetime().time()

    def get_single_sweep(self, index=0, load_data=True):
        return NDARoutineSweep(self, index, load_data)

    def get_first_sweep(self, load_data=True):
        return self.get_single_sweep(0, load_data)

    def get_last_sweep(self, load_data=True):
        return self.get_single_sweep(len(self)-1, load_data)

    def get_freq_list(self):
        return [i/400*(self.meta['freq_max']-self.meta['freq_min'])+self.meta['freq_min']
                for i in range(self.meta['freq_len'])]


class NDARoutineSweep:

    def __init__(self, parent, index_input, load_data=True):
        self.parent = parent
        self.debug = self.parent.debug
        self.data = dict()
        self.load_data = load_data

        if isinstance(index_input, int):
            self.index = index_input
        else:
            raise NDARoutineError("Unable to process provided index value... Aborting")

        data_start_pos = self.parent.file_info['data_offset_in_file'] \
                         + self.index * self.parent.file_info['record_size']
        rec_date_fields = ['hr', 'min', 'sec', 'cs']
        rec_date_dtype = '<bbbb'

        with open(self.parent.file, 'rb') as f:
            f.seek(data_start_pos, 0)
            block = f.read(self.parent.file_info['record_size'])
            rec_date = dict(zip(rec_date_fields, struct.unpack(rec_date_dtype, block[0:4])))
            rec_data = struct.unpack('<'+'b'*400, block[4:404])
            rec_status = block[404]

        self.data['hms'] = rec_date
        self.data['data'] = rec_data
        self.data['status'] = rec_status

        if self.index % 2 == 0:
            self.data['polar'] = 'LH'
        else:
            self.data['polar'] = 'RH'

    def get_time(self):
        return datetime.time(int(self.data['hms']['hr']),
                             int(self.data['hms']['min']),
                             int(self.data['hms']['sec']),
                             int(self.data['hms']['cs']) * 10000)

    def get_datetime(self):

        start_date = self.parent.get_start_date()
        meridian_date = self.parent.get_meridian_datetime().date()
        cur_time = self.get_time()
        cur_date = meridian_date
        if start_date < meridian_date:
            if self.get_time() > datetime.time(12, 0, 0):
                cur_date = start_date
        return datetime.datetime(cur_date.year, cur_date.month, cur_date.day,
                                 cur_time.hour, cur_time.minute, cur_time.second, cur_time.microsecond)

    def get_data(self):
        return self.data['data']

    def get_data_in_db(self):
        return [item * 0.3125 for item in self.data['data']]

    def fix_time(self):
        pass
