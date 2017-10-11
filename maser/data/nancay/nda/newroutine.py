#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read Nancay/NDA/NewRoutine data from SRN/NDA.
@author: B.Cecconi(LESIA)
"""

import struct
import datetime
import os
from maser.data.data import *
from maser.data.nancay.nda.nda import *

__author__ = "Baptiste Cecconi"
__date__ = "03-OCT-2017"
__version__ = "0.10"

__all__ = ["NDANewRoutineData", "NDANewRoutineError"] #, "read_srn_nda_new_routine"]


class NDANewRoutineError(NDAError):
    pass


class NDANewRoutineData(NDADataFromFile):

    def __init__(self, file, debug=False):
        header = {}
        data = []
        name = "SRN/NDA NewRoutine Dataset"
        # meta = {}
        NDADataFromFile.__init__(self, file, header, data, name)
        self.file_handle = open(self.file, 'rb')

        self.file_info = {'name': self.file, 'size': self.get_file_size()}
        self.detect_format()
        self.set_filedate()
        self.debug = debug
        self.header = self.header_from_file()
        self.file_info['record_format'] = self.header['record_fmt']

        ifrq_min = 0
        ifrq_max = 0
        for i in range(2048):
            if self.header['freq'][i] < 10:
                ifrq_min = i + 1
            if self.header['freq'][i] <= 40:
                ifrq_max = i

        self.header['ncube'] = (self.get_file_size() - self.header['size']) // self.header['cube_size']

        self.cur_ptr_in_file = 0

        if self.debug:
            print("{} eCubes in current file".format(self.header['ncube']))

        self.ecube_ptr_in_file = [self.header['size'] + ii * self.header['cube_size']
                                  for ii in range(self.header['ncube'])]

        meta = dict()
        meta['obsty_id'] = 'srn'
        meta['instr_id'] = 'nda'
        meta['recvr_id'] = 'newroutine'
        meta['freq_min'] = float(self.header['freq'][ifrq_min])  # MHz
        meta['freq_max'] = float(self.header['freq'][ifrq_max])  # MHz
        meta['freq_len'] = ifrq_max - ifrq_min + 1
        meta['freq_stp'] = 48.828125  # kHz
        meta['freq_res'] = 48.828125  # kHz
        self.meta = meta

    def get_mime_type(self):
        if self.file_info['format'] == 'DAT':
            return 'application/x-binary'
        elif self.file_info['format'] == 'CDF':
            return 'application/x-cdf'
        else:
            raise NDANewRoutineError("Wrong file format")

    def __len__(self):
        if self.file_info['format'] == 'DAT':
            return (self.get_file_size()-self.file_info['header_size'])//self.file_info['record_size']
        else:
            raise NDANewRoutineError("NDA/NewRoutine: Format {} not implemented yet".format(self.file_info['format']))

    def detect_format(self):
        if self.file.endswith('.dat'):
            self.file_info['format'] = 'DAT'
            self.file_info['record_size'] = 32832
            self.file_info['header_size'] = 16660
            self.file_info['data_offset_in_file'] = self.file_info['record_size']
        elif self.file.endswith('.cdf'):
            self.file_info['format'] = 'CDF'
        else:
            raise NDANewRoutineError('NDA/NewRoutine: Unknown file Extension')

    def set_filedate(self):
        if self.file_info['format'] == 'DAT':
            self.file_info['filedate'] = ((os.path.basename(self.file).split('.'))[0])[1:9]
        else:
            raise NDANewRoutineError("NDA/NewRoutine: Format {} not implemented yet".format(self.file_info['format']))

    def header_from_file(self):
        if self.file_info['format'] == 'DAT':
            return self.header_from_dat()
        else:
            raise NDANewRoutineError("NDA/NewRoutine: Format {} not implemented yet".format(self.file_info['format']))

    def header_from_dat(self):

        f = self.file_handle
        self.file_info['header_raw'] = f.read(self.file_info['header_size'])

        hdr_fmt = '<68I1l2048f2048l'
        hdr_val = struct.unpack(hdr_fmt, self.file_info['header_raw'])

        header = dict()
        header['size'] = hdr_val[0]  # Header Size
        header['sel_prod0'] = hdr_val[1]  # selected products 0
        header['sel_prod1'] = hdr_val[2]  # selected products 1
        header['acc'] = hdr_val[3]  # accumulating factor
        header['subband'] = hdr_val[4:68]  # selected sub-bands
        header['nfreq'] = hdr_val[68]  # Number of FFT points
        header['freq'] = hdr_val[69:2117]  # frequency values
        header['ifrq'] = hdr_val[2117:4165]  # frequency indices

        sel_chan = [int(ii) for ii in
                    list('{:032b}'.format(header['sel_prod0'])[::-1] +
                         '{:032b}'.format(header['sel_prod1'])[::-1])]
        nbchan = sum(sel_chan)

        record_fmt = '<8I'
        for iichan in range(0, nbchan):
            record_fmt = '{}{}'.format(record_fmt, '2I2048f')

        header['nbchan'] = nbchan
        header['cube_size'] = 4 * (8 + header['nbchan'] * (header['nfreq'] + 2))
        header['magic_word'] = 0x7F800000
        header['record_fmt'] = record_fmt

        return header

    def get_first_ecube(self):
        return self.get_single_ecube(0)

    def get_last_ecube(self):
        return self.get_single_ecube(-1)

    def get_single_ecube(self, index_input=0, load_data=True):
        return NDANewRoutineECube(self, index_input, load_data)

    def get_freq_axis(self):
        return self.header['freq']

    def get_time_axis(self):
        return [self.get_single_ecube(item, load_data=False).get_datetime() for item in range(len(self))]


class NDANewRoutineECube(MaserDataSweep):

    def __init__(self, newroutine_data, index_input, load_data=True):
        MaserDataSweep.__init__(self, newroutine_data, index_input)
        self.debug = self.parent.debug
        self.data = dict()

        ecube_hdr_read_param = {'fields': ['magic', 'id', 'date_jd', 'date_sec', 'date_nsub', 'date_dsub'],
                                'dtype': '<LLLLLL', 'length': 24, 'skip': 8}

        corr_hdr_read_param = {'fields': ['magic', 'no'], 'dtype': '<LL', 'length': 8}

        f = self.parent.file_handle

        corr_data_length = self.parent.header['nfreq'] * 4

        f.seek(self.parent.ecube_ptr_in_file[self.index], 0)

        block = f.read(ecube_hdr_read_param['length'])
        self.data.update(dict(zip(ecube_hdr_read_param['fields'],
                                  struct.unpack(ecube_hdr_read_param['dtype'], block))))
        f.read(ecube_hdr_read_param['skip'])
        self.data['corr'] = list()

        for i in range(self.parent.header['nbchan']):
            block = f.read(corr_hdr_read_param['length'])

            corr_tmp = dict(zip(corr_hdr_read_param['fields'],
                                struct.unpack(corr_hdr_read_param['dtype'], block)))
            corr_tmp['data_pos_in_file'] = f.tell()

            self.data['corr'].append(corr_tmp)

            if load_data:
                self.load_data(i)
            else:
                self.data['corr'][i]['data'] = list()
                f.seek(corr_data_length, 1)

        self.check_magic()

    def get_datetime(self):
        dt_epoch = datetime.datetime(1970, 1, 1)
        return dt_epoch + datetime.timedelta(days=self.data['date_jd'] + self.data['date_sec'] / 86400 +
                                                  self.data['date_nsub'] / (self.data['date_dsub'] * 86400) - 2440587.5)

    def load_data(self, index):

        corr_data_length = self.parent.header['nfreq'] * 4

        f = self.parent.file_handle

        f.seek(self.data['corr'][index]['data_pos_in_file'], 0)
        block = f.read(corr_data_length)
        corr_tmp_data = struct.unpack('<{}f'.format(self.parent.header['nfreq']), block)
        self.data['corr'][index]['data'] = corr_tmp_data

    def check_magic(self):

        if self.data['magic'] != 0x7F800000:
            raise NDANewRoutineError('[{}:{}] Wrong eCube Magic Word (Header) [0x{:08X}]'
                                .format(self.parent.get_file_name(), self.index, self.data['magic']))

        for i in range(self.parent.header['nbchan']):
            if self.data['corr'][i]['magic'] != 0xFF800001:
                raise NDANewRoutineError('[{}:{}] Wrong eCube Magic Word (Corr[{}]) [0x{:08X}]'
                                    .format(self.parent.get_file_name(), self.index,
                                            i, self.data['corr'][i]['magic']))
