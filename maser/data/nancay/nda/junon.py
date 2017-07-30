#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read Nancay/NDA/JunoN data from SRN/NDA.
@author: B.Cecconi(LESIA)
"""

import struct
import sys
import os
from maser.data.nancay.nda.nda import *

__author__ = "Baptiste Cecconi"
__date__ = "25-JUL-2017"
__version__ = "0.10"

__all__ = ["NDAJunonData", "read_srn_nda_junon"]


class NDAJunonData(NDAData):

    def __init__(self, file, debug=False):
        header = {}
        data = []
        name = "SRN/NDA JunoN Dataset"
        meta = {}
        NDAData.__init__(self, file, header, data, name)
        self.debug = debug
        self.header = self.header_from_file()
        self.meta = meta
        self.cur_ptr_in_file = 0

    def header_from_file(self):
        """

        :param file_path:
        :param debug:
        :return:
        """

        desc = dict()

        try:

            with open(self.file, 'rb') as f:

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
                    raise WrongFormatException("Wrong stream_10G mode (read value = {}".format(desc['stream_10G']))

                if desc['stream_10G'] == 1:

                    desc_fields = ['nbchan','acc']
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
                        print("freq = ({}, ..., {}) MHz".format(desc['freq'][0],desc['freq'][-1]))

                if desc['stream_10G'] == 1:

                    desc['cube_size'] = 8 + desc['nbchan']*(desc['nfreq']+2)
                    desc['magic_word'] = 0x7F800000

                if desc['stream_10G'] == 2:

                    desc['cube_size'] = 2048
                    desc['magic_word'] = 0xFF800000

        except WrongFormatException as e:

            print(e.message)

        return desc

    def file_info(self):
        """

        :param debug:
        :return:
        """

        print('')
        print('File Description:')
        print('-- File:          {}'.format(self.file))
        print('-- Path:          {}'.format(self.path))
        print('-- File size:     {}'.format(self.str_file_size()))
        print('-- Header size:   {}'.format(self.header['size']))
        str_data = ['Nothing', 'Spectrum', 'Waveform']
        print('-- Data content:  {}'.format(str_data[self.header['stream_10G']]))

    def first_ecube_position_in_file(self):
        """

        :return:
        """

        with open(self.absolute_path(), 'rb') as f:
            f.seek(self.header['size'], 0)
            word = 0x00000000
            fpos = f.tell()
            epos = self.header['cube_size']*4+self.header['size']
            while word != self.header['magic_word'] and fpos < epos:
                fpos = f.tell()
                block = f.read(4)
                word = struct.unpack("<L", block)[0]
                if self.debug:
                    print("{}: {}".format(fpos, word))

        return fpos

    def get_first_ecube(self):
        return self.get_single_ecube(0)

    def get_last_ecube(self):
        return self.get_single_ecube(-1)

    def get_single_ecube(self, index_input=0, debug=False):

        #cpos0 = self.first_ecube_position_in_file()  # position of 1st cube
        cpos0 = self.header['size'] # position of 1st cube (= after end of header)
        csize = self.header['cube_size']  # size of a cube
        fsize = os.path.getsize(self.absolute_path())  # size of file
        ncube = int((fsize - cpos0) / csize)  # nb of cubes in file
        if self.debug:
            print("{} eCubes in current file".format(ncube))

        ecube_positions_in_file = [cpos0 + ii * csize for ii in range(ncube)]

        ecube = dict()

        if isinstance(index_input, int):
            index = index_input
        else:
            print("Unable to process provided index value... Aborting")
            return ecube

        if self.header['stream_10G'] != 1:
            print("This file doesn't contain Spectrum data. Aborting...")
            return ecube

        ecube_hdr_fields = ['magic', 'id', 'date_jd', 'date_sec', 'date_nsub', 'date_dsub']
        ecube_hdr_dtype = '<LLLLLL'
        ecube_hdr_length = 24
        ecube_hdr_skip = 8

        corr_hdr_fields = ['magic', 'no']
        corr_hdr_dtype = '<LL'
        corr_hdr_length = 8

        with open(self.absolute_path(), 'rb') as f:

            f.seek(ecube_positions_in_file[index], 0)

            block = f.read(ecube_hdr_length)
            ecube.update(dict(zip(ecube_hdr_fields, struct.unpack(ecube_hdr_dtype, block))))
            f.read(ecube_hdr_skip)
            ecube['corr'] = list()

            for i in range(self.header['nbchan']):
                block = f.read(corr_hdr_length)
                corr_tmp = dict(zip(corr_hdr_fields, struct.unpack(corr_hdr_dtype, block)))
                block = f.read(self.header['nfreq']*4)
                corr_tmp['data'] = struct.unpack('<{}f'.format(self.header['nfreq']), block)
                ecube['corr'].append(corr_tmp)

        return ecube


def read_srn_nda_junon(file_path, verbose=False):
    """

    :param file_path:
    :param verbose:
    :return:
    """

    return NDAJunonData(file_path)
