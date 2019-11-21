#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read Nancay/NDA/JunoN data from SRN/NDA.
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__date__ = "12-OCT-2017"
__version__ = "0.11"

__all__ = ["NDAJunonData", "NDAJunonECube", "NDAJunonError", "read_srn_nda_junon"]

import struct
from ..nda import NDADataECube, NDADataFromFile, NDAError


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
        self.file_info = {'name': self.file,
                          'size': self.get_file_size(),
                          'format': 'DAT',
                          }
        self.header['ncube'] = (self.get_file_size() - self.header['size']) // self.header['cube_size']
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
            desc['magic_word_head'] = 0x7F800000
            desc['magic_word_corr'] = 0xFF800001

        if desc['stream_10G'] == 2:

            desc['cube_size'] = 2048
            desc['magic_word_head'] = 0xFF800000
            desc['magic_word_corr'] = 0xFF800001

        return desc

    def __str__(self):
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

    def __len__(self):
        return len(self.ecube_ptr_in_file)

    def get_freq_axis(self):
        return self.header['freq']

    def get_time_axis(self):
        return [self.get_single_ecube(item, load_data=False).get_datetime() for item in range(len(self))]

    def get_first_ecube(self):
        return self.get_single_ecube(0)

    def get_last_ecube(self):
        return self.get_single_ecube(-1)

    def get_single_ecube(self, index_input=0, load_data=True):

        # LH = ecube['corr'][0]
        # RH = ecube['corr'][3]
        # cross = ecube['corr'][1:2]

        if self.header['stream_10G'] != 1:
            raise NDAJunonError("This file doesn't contain Spectrum data. Aborting...")
        else:
            return NDAJunonECube(self, index_input, load_data)


class NDAJunonECube(NDADataECube):
    pass


def read_srn_nda_junon(file_path):
    """

    :param file_path:
    :return:
    """

    return NDAJunonData(file_path)
