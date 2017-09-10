#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read Nancay/NDA/JunoN data from SRN/NDA.
@author: B.Cecconi(LESIA)
"""

import struct
import datetime
import os
from maser.data.data import *
from maser.data.nancay.nda.nda import *

__author__ = "Baptiste Cecconi"
__date__ = "25-JUL-2017"
__version__ = "0.10"

__all__ = ["NDAJunonData", "NDAJunonECube", "NDAJunonError", "read_srn_nda_junon"]


class NDAJunonError(NDAError):
    pass


class NDAJunonData(NDADataFromFile):

    def __init__(self, file, debug=False):
        header = {}
        data = []
        name = "SRN/NDA JunoN Dataset"
        # meta = {}
        NDADataFromFile.__init__(self, file, header, data, name)
        self.file_handle = open(self.file, 'rb')

        self.debug = debug
        self.header = self.header_from_file()
        self.header['ncube'] = (os.path.getsize(self.file) - self.header['size']) // self.header['cube_size']
        # self.meta = meta
        self.cur_ptr_in_file = 0

        if self.debug:
            print("{} eCubes in current file".format(self.header['ncube']))

        self.ecube_ptr_in_file = [self.header['size'] + ii * self.header['cube_size']
                                  for ii in range(self.header['ncube'])]

    def header_from_file(self):
        """

        :return:
        """
        desc = dict()

        f = self.file_handle
        f.seek(0, 0)

        desc_fields = ['size', 'stream_10G']
        desc_dtype = '<LL'
        block = f.read(8)
        desc.update(dict(zip(desc_fields, struct.unpack(desc_dtype, block))))

        if self.debug:
            print("size = {}".format(desc['size']))
            print("stream_10G = {}".format(desc['stream_10G']))

            # stream_10G = 1 => spectrum
            # stream_10G = 2 => waveform

        if desc['stream_10G'] == 0:
            return desc

        if desc['stream_10G'] != 1 and desc['stream_10G'] != 2:
            raise NDAJunonError("Wrong stream_10G mode (read value = {}".format(desc['stream_10G']))

        if desc['stream_10G'] == 1:

            desc_fields = ['nbchan', 'acc']
            desc_dtype = '<LL'
            block = f.read(8)
            desc.update(dict(zip(desc_fields, struct.unpack(desc_dtype, block))))
            if self.debug:
                print("nbchan = {}".format(desc['nbchan']))
                print("acc = {}".format(desc['acc']))

        desc_fields = ['bw', 'fech', 'f0']
        desc_dtype = '<fff'
        block = f.read(12)
        desc.update(dict(zip(desc_fields, struct.unpack(desc_dtype, block))))

        if self.debug:
            print("bw = {} MHz".format(desc['bw']))
            print("fech = {} MHz".format(desc['fech']))
            print("f0 = {} MHz".format(desc['f0']))

        if desc['stream_10G'] == 1:

            desc_fields = ['dt', 'nfreq']
            desc_dtype = '<fL'
            block = f.read(8)
            desc.update(dict(zip(desc_fields, struct.unpack(desc_dtype, block))))
            if self.debug:
                print("dt = {} ms".format(desc['dt']))
                print("nfreq = {}".format(desc['nfreq']))

            freq_dtype = '<{}f'.format(desc['nfreq'])
            block = f.read(desc['nfreq']*4)
            desc['freq'] = struct.unpack(freq_dtype, block)
            if self.debug:
                print("freq = ({}, ..., {}) MHz".format(desc['freq'][0], desc['freq'][-1]))

        if desc['stream_10G'] == 1:

            desc['cube_size'] = 4 * (8 + desc['nbchan']*(desc['nfreq']+2))
            desc['magic_word'] = 0x7F800000

        if desc['stream_10G'] == 2:

            desc['cube_size'] = 2048
            desc['magic_word'] = 0xFF800000

        return desc

    def file_info(self):
        """

        :return:
        """

        print('')
        print('File Description:')
        print('-- File:          {}'.format(self.file))
        print('-- Path:          {}'.format(self.get_file_path()))
        print('-- File size:     {}'.format(self.get_str_file_size()))
        print('-- Header size:   {}'.format(self.header['size']))
        str_data = ['Nothing', 'Spectrum', 'Waveform']
        print('-- Data content:  {}'.format(str_data[self.header['stream_10G']]))

#    def first_ecube_ptr_in_file(self):
#        """
#
#        :return:
#        """
#
#        f = self.file_handle
#        f.seek(self.header['size'], 0)
#        word = 0x00000000
#        fpos = f.tell()
#        epos = self.header['cube_size']*4+self.header['size']
#        while word != self.header['magic_word'] and fpos < epos:
#            fpos = f.tell()
#            block = f.read(4)
#            word = struct.unpack("<L", block)[0]
#            if self.debug:
#                print("{}: {}".format(fpos, word))
#
#        return fpos

    def get_first_ecube(self):
        return self.get_single_ecube(0)

    def get_last_ecube(self):
        return self.get_single_ecube(-1)

    def get_single_ecube(self, index_input=0, load_data=True):

        # LH = ecube['corr'][0]
        # RH = ecube['corr'][3]
        # cross = ecube['corr'][1:2]

        return NDAJunonECube(self, index_input, load_data)


class NDAJunonECube(MaserDataSweep):

    def __init__(self, junon_data, index_input, load_data=True):
        MaserDataSweep.__init__(self, junon_data, index_input)
        self.debug = self.parent.debug
        self.data = dict()

        if self.parent.header['stream_10G'] != 1:
            raise NDAJunonError("This file doesn't contain Spectrum data. Aborting...")

        ecube_hdr_read_param = {'fields': ['magic', 'id', 'date_jd', 'date_sec', 'date_nsub', 'date_dsub'],
                                'dtype': '<LLLLLL', 'length': 24, 'skip': 8}

        corr_hdr_read_param = {'fields': ['magic', 'no'], 'dtype': '<LL', 'length': 8}

        corr_data_length = self.parent.header['nfreq'] * 4

        f = self.parent.file_handle

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
            raise NDAJunonError('[{}:{}] Wrong eCube Magic Word (Header) [0x{:08X}]'
                                .format(self.parent.get_file_name(), self.index, self.data['magic']))

        for i in range(self.parent.header['nbchan']):
            if self.data['corr'][i]['magic'] != 0xFF800001:
                raise NDAJunonError('[{}:{}] Wrong eCube Magic Word (Corr[{}]) [0x{:08X}]'
                                    .format(self.parent.get_file_name(), self.index,
                                            i, self.data['corr'][i]['magic']))


def read_srn_nda_junon(file_path):
    """

    :param file_path:
    :return:
    """

    return NDAJunonData(file_path)
