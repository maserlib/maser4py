#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to define classes for the Nancay Decameter Array (NDA) datasets at Obs-Nancay.
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__institute__ = "LESIA, Observatoire de Paris, PSL Research University, CNRS."
__date__ = "12-OCT-2017"
__version__ = "0.11"
__project__ = "MASER/SRN/NDA"

__all__ = ["NDADataFromFile", "NDAError", "NDADataECube"]

import struct
import datetime
from maser.data.data import MaserError
from maser.data.data import MaserDataFromFile
from maser.data.data import MaserDataSweep


class NDAError(MaserError):
    pass


class NDADataFromFile(MaserDataFromFile):

    def __init__(self, file, header, data, name, verbose=True, debug=False):
        MaserDataFromFile.__init__(self, file, verbose=verbose, debug=debug)
        self.header = header
        self.data = data
        self.name = name

    def __len__(self):
        return len(self.data)


class NDADataECube(MaserDataSweep):
    def __init__(self, parent_obj, index_input, load_data=True, filter_frequency=False):
        MaserDataSweep.__init__(self, parent_obj, index_input)
        self.debug = self.parent.debug
        self.filter_frequency = filter_frequency
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
        if self.filter_frequency:
            self.data['corr'][index]['data'] = \
                corr_tmp_data[self.parent.header['ifrq_min']:self.parent.header['ifrq_max']]
        else:
            self.data['corr'][index]['data'] = corr_tmp_data

    def check_magic(self):

        if self.data['magic'] != self.parent.header['magic_word_head']:
            raise NDAError('[{}:{}] Wrong eCube Magic Word (Header) [0x{:08X}]'
                           .format(self.parent.get_file_name(), self.index, self.data['magic']))

        for i in range(self.parent.header['nbchan']):
            if self.data['corr'][i]['magic'] != self.parent.header['magic_word_corr']:
                raise NDAError('[{}:{}] Wrong eCube Magic Word (Corr[{}]) [0x{:08X}]'
                               .format(self.parent.get_file_name(), self.index,
                                       i, self.data['corr'][i]['magic']))

