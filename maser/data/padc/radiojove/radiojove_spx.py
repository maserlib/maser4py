#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read RadioJOVE SPS and SPD raw data files
"""

import numpy as np
import csv
import os
import struct
import pprint as pp
import datetime
import dateutil.parser
import astropy.time
from maser.data.data import MaserDataFromFile, MaserData
from maser.utils.cdf import cdf

__author__ = "Baptiste Cecconi"
__date__ = "11-MAY-2018"
__version__ = "0.21"

__all__ = ["RadioJoveDataSPXFromFile", "RadioJoveDataCDF", "convert_spx_to_cdf"]

_packet_size = 10000


class RadioJoveError(Exception):
    pass


########################################################################################################################
#
#     Defining the generic class for RadioJove Data (inherited from MaserData)FromFile
#
########################################################################################################################

class RadioJoveDataSPXFromFile(MaserDataFromFile):
    """
    Class for RadioJove data
    """

    def __init__(self, file, load_data=True, obsty_config=None, verbose=True, debug=False):
        MaserDataFromFile.__init__(self, file, verbose, debug)
        self.file_info = {'name': self.file, 'size': self.get_file_size(), 'file_data_offset': 0}
        if obsty_config is not None:
            self.obsty_config = self._load_obsty_config(obsty_config)
        else:
            self.obsty_config = None
        self.header = dict()
        self.load_data = load_data
        self.header['notes'] = {}
        self.time = []
        self.frequency = []
        self._open_radiojove_spx()
        self.start_time = self.header['start_time']
        self.end_time = self.header['stop_time']
        self.sweep_ptr_in_file = [self.file_info['prim_hdr_length'] + self.header['note_length']
                                  + ii * self.file_info['bytes_per_step'] for ii in range(self.header['nsweep'])]
        self.data = []

        if self.debug:
            print("{} sweeps in current file".format(self.header['nsweep']))

        self.dataset_name = "_".join(["radiojove", self.header['obsty_id'].lower(), self.header['instr_id'].lower(),
                                      self.header['level'].lower(), self.header['product_type'].lower()])

        self.data_loaded = False
        if self.load_data:
            self.data = self._extract_radiojove_spx_data()
            self.data_loaded = True

        if self.data_loaded:
            self._close_radiojove_spx()

    def close(self):
        self._close_radiojove_spx()

    def _load_obsty_config(self, obsty_config_file):
        obsty_config = []
        with open(obsty_config_file, 'r') as f:
            buffer = csv.reader(f)
            for row in buffer:
                if row[0].startswith('#'):
                    pass
                else:
                    tmp_config = {}
                    tmp_config['start_time'] = dateutil.parser.parse(row[0])
                    tmp_config['end_time'] = dateutil.parser.parse(row[1])
                    tmp_config['polar0'] = row[2]
                    tmp_config['polar1'] = row[3]
                    obsty_config.append(tmp_config)
        return obsty_config

    def _extract_radiojove_spx_header(self):
        """
        Extracts fixed length header keywords from Raw data
        :param self:
        :return header: a dictionary containing the decoded header
        """

        if self.verbose:
            print("### [load_radiojove_spx_header]")

        hdr_raw = self.file_info['prim_hdr_raw']

        hdr_fmt = '<10s6d1h10s20s20s40s1h1i'  # header format to unpack header
        hdr_values = struct.unpack(hdr_fmt, hdr_raw[0:156])

        self.header['rss_sw_version'] = hdr_values[0].decode('ascii')
        # date conversion: header dates are given in decimal days since 30/12/1899 00:00 (early morning!) == day 0.0
        # date values must be corrected by adding 2415018.5 = julian date 30/12/1899 00:00
        self.header['start_jdtime'] = hdr_values[1] + 2415018.5
        self.header['start_time'] = astropy.time.Time(self.header['start_jdtime'], format='jd').datetime
        self.header['stop_jdtime'] = hdr_values[2] + 2415018.5
        self.header['stop_time'] = astropy.time.Time(self.header['stop_jdtime'], format='jd').datetime
        self.header['latitude'] = hdr_values[3]
        self.header['longitude'] = hdr_values[4]
        self.header['chartmax'] = hdr_values[5]
        self.header['chartmin'] = hdr_values[6]
        self.header['timezone'] = hdr_values[7]
        # For the next 4 header keywords, we remove leading and trailing null (0x00) and space characters
        self.header['source'] = (hdr_values[8].decode('ascii').strip('\x00')).strip(' ')
        self.header['author'] = (hdr_values[9].decode('ascii').strip('\x00')).strip(' ')
        self.header['obsname'] = (hdr_values[10].decode('ascii').strip('\x00')).strip(' ')
        self.header['obsloc'] = (hdr_values[11].decode('ascii').strip('\x00')).strip(' ')
        self.header['nchannels'] = hdr_values[12]
        self.header['note_length'] = hdr_values[13]

    def _extract_raw_radiojove_spx_notes(self):
        """
        Extracts the extended header information (notes) for SPS or SPD files.
        :return free_text, note_list: list of items extracted from the raw notes
        """
        if self.verbose:
            print("### [extract_raw_radiojove_spx_notes]")

        raw_notes = self.file_info['notes_raw']

        # stripping raw note text stream from "*[[*" and "*]]*" delimiters, and splitting result with '\xff'
        start_index = raw_notes.find(b'*[[*')
        stop_index = raw_notes.find(b'*]]*')
        free_text = raw_notes[0:start_index].decode('ascii')
        note_list = []
        cur_note = b''
        for bb in raw_notes[start_index + 4:stop_index]:
            if bb == 255:
                note_list.append(cur_note)
                cur_note = b''
            else:
                cur_note = b''.join([cur_note, struct.pack("B", bb)])

        return free_text, note_list

    def _extract_radiojove_sps_notes(self):
        """
        Extracts the extended header information (notes) for SPS files (spectrograph)
        :param self:
        :return notes: dictionary containing the extracted header notes
        """
        if self.verbose:
            print("### [extract_radiojove_sps_notes]")

        free_text, note_list = self._extract_raw_radiojove_spx_notes()
        self.header['notes']['free_text'] = free_text

        # The header notes are composed of a series of key and value (KV) pairs.
        # The raw notes start with a free text space.
        # The KV pairs section are starting *[[* and finishes with *]]*.
        # The delimiter between each KV pair is 0xFF.
        # There is no predefined character for separating key and value within a KV pair.
        # We must then identify the keys. Some keys have multiple values.
        # More info: http://www.radiosky.com/skypipehelp/V2/datastructure.html

        # List of known metadata keys
        key_list = ['SWEEPS', 'LOWF', 'HIF', 'STEPS', 'RCVR', 'DUALSPECFILE', 'COLORRES', 'BANNER', 'ANTENNATYPE',
                    'ANTENNAORIENTATION', 'COLORFILE', 'COLOROFFSET', 'COLORGAIN', 'CORRECTIONFILENAME', 'CAXF',
                    'CAX1', 'CAX2', 'CLOCKMSG']
        val_list = [0, 0., 0., 0, 0, True, 0, [], '', '', '', [], [], '', [], [], [], []]
        self.header['notes'].update(dict(zip(key_list, val_list)))
        # CHECK LIST WITH https://voparis-confluence.obspm.fr/display/JOVE/RadioSky+Spectrograph-SPS+Metadata

        # list of metadata keys with multiple values
        key_list_multi = ['BANNER', 'COLOROFFSET', 'COLORGAIN', 'CAXF', 'CAX1', 'CAX2', 'CLOCKMSG']

        # list of metadata keys with integer values
        key_list_int = ['SWEEPS', 'STEPS', 'RCVR', 'COLORRES', 'COLOROFFSET']

        # list of metadata keys with floating point values
        key_list_float = ['LOWF', 'HIF', 'COLORGAIN']

        # Looping on note items to identify what keys are present
        for item in note_list:

            note_item = item.decode('ascii')

            if self.debug:
                print('Current Item = {}'.format(note_item))

            # looping on known key items
            for key_item in key_list:

                # getting length of key name
                key_len = len(key_item)

                # checking if current note item contains current key item
                if note_item[0:key_len] == key_item:

                    if self.debug:
                        print('Detected Key = {}'.format(key_item))

                    # if current key item has multiple values, do this
                    if key_item in key_list_multi:

                        # checking specific cases
                        if key_item[0:3] == 'CAX':
                            note_item = note_item.split('|')
                            note_index = int(note_item[0][key_len:])
                            note_value = note_item[1]
                        elif key_item[0:8] == 'CLOCKMSG':
                            note_item = note_item.split(' ')
                            note_index = int(note_item[0][key_len:])
                            note_value = ' '.join(note_item[1:])
                        else:
                            note_index = int(note_item[key_len:key_len + 1])
                            note_value = note_item[key_len + 1:]
                        if self.debug:
                            print('Index = {}'.format(note_index))
                            print('Value = {}'.format(note_value))

                        # adding value to note item
                        if key_item in key_list_int:
                            self.header['notes'][key_item].append(int(note_value.strip()))
                        elif key_item in key_list_float:
                            self.header['notes'][key_item].append(float(note_value.strip()))
                        else:
                            self.header['notes'][key_item].append(note_value)

                    else:

                        # key has single value, extracting the value (no delimiter)
                        note_value = note_item[key_len:]

                        # special case for RCVR, empty value should be value -1
                        if key_item == 'RCVR':
                            if note_value == '':
                                note_value = '-1'

                        if self.debug:
                            print('Value = {}'.format(note_value))

                        # loop on keys that have numeric values
                        if key_item in key_list_int:
                            self.header['notes'][key_item] = int(note_value.strip())
                        elif key_item in key_list_float:
                            self.header['notes'][key_item] = float(note_value.strip())
                        else:
                            self.header['notes'][key_item] = note_value

        # final special case:
        # if not present this keyword (no value) says that we deal with single channel spectrograph data
        if 'DUALSPECFILE' not in self.header['notes'].keys():
            self.header['notes']['DUALSPECFILE'] = False
        else:
            if self.header['notes']['DUALSPECFILE'].strip() == 'True':
                self.header['notes']['DUALSPECFILE'] = True

        # adding default "COLORGAIN" and "COLOROFFSET" notes elements for older versions than 2.8.16
        if int(self.header['rss_sw_version']) < 208016:
            self.header['notes']['COLORGAIN'] = [2.0, 2.0]
            self.header['notes']['COLOROFFSET'] = [2000, 2000]

        # adding default "BANNER" notes elements for older versions than 2.4.16
        if int(self.header['rss_sw_version']) < 204016:
            self.header['notes']['BANNER'].append('{} - <DATE> - RCP'.format(self.header['obsname']))
            self.header['notes']['BANNER'].append('{} - <DATE> - LCP'.format(self.header['obsname']))

    def _extract_radiojove_spd_notes(self):
        """
        Extracts the extended header information (notes) for SPD files (radiojove kits)
        :param self:
        :return notes: dictionary containing the extracted header notes
        """

        # The header notes are composed of a series of key and value (KV) pairs.
        # The raw notes start with a free text space.
        # The KV pairs section are starting *[[* and finishes with *]]*.
        # The delimiter between each KV pair is 0xFF.
        # There is no predefined character for separating key and value within a KV pair.
        # We must then identify the keys. Some keys have multiple values.
        # More info: http://www.radiosky.com/skypipehelp/V2/datastructure.html

        if self.verbose:
            print("### [extract_radiojove_spd_notes]")

        free_text, note_list = self._extract_raw_radiojove_spx_notes()

        # initializing notes with 3 sub dictionaries.
        self.header['notes']['CHL'] = {}
        self.header['notes']['CHO'] = {}
        self.header['notes']['MetaData'] = {}
        self.header['notes']['free_text'] = free_text

        for item in note_list:

            note_item = item.decode('ascii')

            if note_item == 'Logged Using UT':
                self.header['notes']['Logged Using UT'] = True
            else:
                self.header['notes']['Logged Using UT'] = False

            if note_item == 'No Time Stamps':
                self.header['notes']['No Time Stamps'] = True
            else:
                self.header['notes']['No Time Stamps'] = False

            if note_item[0:3] == 'CHL':
                self.header['notes']['CHL'][int(note_item[3])] = note_item[4:]

            if note_item[0:3] == 'CHO':
                self.header['notes']['CHO'][int(note_item[3])] = note_item[4:]

            if note_item == 'Integer Save':
                self.header['notes']['Integer Save'] = True
            else:
                self.header['notes']['Integer Save'] = False

            if note_item[0:7] == 'XALABEL':
                self.header['notes']['XALABEL'] = note_item[7:]

            if note_item[0:7] == 'YALABEL':
                self.header['notes']['YALABEL'] = note_item[7:]

            # extra metadata are present with a generic syntax Metadata_[KEY][0xC8][VALUE]
            if note_item[0:9] == 'MetaData_':
                item_metadata = note_item.split('\xc8')
                # removing any extra trailing character in key name (spaces or colon)
                self.header['notes']['MetaData'][item_metadata[0][9:].strip(' ').strip(':').strip(' ')] \
                    = item_metadata[1]

    def _open_radiojove_spx(self):
        """
        Opens RadioJOVE SPS or SPD file for processing
        """
        if self.verbose:
            print("### [open_radiojove_spx]")

        # Opening file:
        self.file_info['prim_hdr_length'] = 156
        self.file_info['lun'] = open(self.file_info['name'], 'rb')

        # Reading header:
        self.file_info['prim_hdr_raw'] = self.file_info['lun'].read(self.file_info['prim_hdr_length'])
        self._extract_radiojove_spx_header()
        self.header['file_name'] = self.file_info['name']
        self.header['file_type'] = self.file_info['name'][-3:].upper()

        # Reading notes:
        self.file_info['notes_raw'] = self.file_info['lun'].read(self.header['note_length'])
        if self.header['file_type'] == 'SPS':
            self._extract_radiojove_sps_notes()
        elif self.header['file_type'] == 'SPD':
            self._extract_radiojove_spd_notes()
            self.header['nfreq'] = 1

        if self.header['obsname'] == 'AJ4CO DPS':
            self.header['obsty_id'] = 'AJ4CO'
            self.header['instr_id'] = 'DPS'
            self.header['gain0'] = 1.95
            self.header['gain1'] = 1.95
            self.header['offset0'] = 1975
            self.header['offset1'] = 1975
            self.header['polar0'] = 'RHC'
            self.header['polar1'] = 'LHC'
            self.header['banner0'] = 'AJ4CO Observatory <DATE> - DPS on TFD Array - RCP'.\
                replace('<DATE>', self.header['start_time'].date().isoformat())
            self.header['banner1'] = 'AJ4CO Observatory <DATE> - DPS on TFD Array - RCP'.\
                replace('<DATE>', self.header['start_time'].date().isoformat())
            self.header['antenna_type'] = '8-element TFD array'
            self.header['color_file'] = 'AJ4CO-Rainbow.txt'
        elif self.header['obsname'] == 'HNRAO LWA':
            self.header['obsty_id'] = 'HNRAO'
            self.header['instr_id'] = 'LWA'
            self.header['gain0'] = 2.00
            self.header['gain1'] = 2.00
            self.header['offset0'] = 2000
            self.header['offset1'] = 2000
            self.header['polar0'] = 'RHC'
            self.header['polar1'] = 'LHC'
            self.header['banner0'] = '<DATE>  - RCP'.\
                replace('<DATE>', self.header['start_time'].date().isoformat())
            self.header['banner1'] = self.header['notes']['BANNER'][1].\
                replace('<DATE>', self.header['start_time'].date().isoformat())
            self.header['antenna_type'] = self.header['notes']['ANTENNATYPE']
            self.header['color_file'] = self.header['notes']['COLORFILE']
            self.header['free_text'] = self.header['notes']['free_text']
        elif self.header['obsname'] == 'LGM Radio Alachua':
            self.header['obsty_id'] = 'LGM'
            self.header['instr_id'] = 'FSX-1S'
            self.header['gain0'] = self.header['notes']['COLORGAIN'][0]
            self.header['gain1'] = self.header['notes']['COLORGAIN'][1]
            self.header['offset0'] = self.header['notes']['COLOROFFSET'][0]
            self.header['offset1'] = self.header['notes']['COLOROFFSET'][1]
            self.header['banner0'] = self.header['notes']['BANNER'][0].\
                replace('<DATE>', self.header['start_time'].date().isoformat())
            self.header['banner1'] = self.header['notes']['BANNER'][1].\
                replace('<DATE>', self.header['start_time'].date().isoformat())
            self.header['antenna_type'] = self.header['notes']['ANTENNATYPE']
            self.header['color_file'] = self.header['notes']['COLORFILE']
            self.header['free_text'] = self.header['notes']['free_text']
        elif self.header['obsname'] == 'MTSU':
            self.header['obsty_id'] = 'MTSU'
            self.header['instr_id'] = 'FSX-6S'
            self.header['gain0'] = self.header['notes']['COLORGAIN'][0]
            self.header['gain1'] = self.header['notes']['COLORGAIN'][1]
            self.header['offset0'] = self.header['notes']['COLOROFFSET'][0]
            self.header['offset1'] = self.header['notes']['COLOROFFSET'][1]
            self.header['polar0'] = 'RHC'
            self.header['polar1'] = 'LHC'
            self.header['banner0'] = self.header['notes']['BANNER'][0]. \
                replace('<DATE>', self.header['start_time'].date().isoformat())
            self.header['banner1'] = self.header['notes']['BANNER'][1]. \
                replace('<DATE>', self.header['start_time'].date().isoformat())
            self.header['antenna_type'] = self.header['notes']['ANTENNATYPE']
            self.header['color_file'] = self.header['notes']['COLORFILE']
            self.header['free_text'] = self.header['notes']['free_text']
        else:
            self.header['obsty_id'] = 'ABCDE'
            self.header['instr_id'] = 'XXX'
            self.header['gain0'] = 2.00
            self.header['gain1'] = 2.00
            self.header['offset0'] = 2000
            self.header['offset1'] = 2000
            self.header['banner0'] = ''
            self.header['banner1'] = ''
            self.header['antenna_type'] = ''
            self.header['color_file'] = ''
            self.header['free_text'] = ''

        if self.header['file_type'] == 'SPS':
            self.header['level'] = 'EDR'
        if self.header['file_type'] == 'SPD':
            self.header['level'] = 'DDR'

        if self.debug:
            print(self.header)
            print(self.header['notes'])

        # Reading data:

        self.file_info['data_length'] = self.file_info['size'] - self.file_info['prim_hdr_length'] - self.header[
            'note_length']

        # nfeed = number of observation feeds
        # nfreq = number of frequency step (1 for SPD)
        # nstep = number of sweep (SPS) or time steps (SPD)

        # SPS files
        self.header['feeds'] = []

        feed_tmp = {'RR': {'FIELDNAM': 'RR', 'CATDESC': 'RCP Flux Density', 'LABLAXIS': 'RCP Power Spectral Density'},
                    'LL': {'FIELDNAM': 'LL', 'CATDESC': 'LCP Flux Density', 'LABLAXIS': 'LCP Power Spectral Density'},
                    'S': {'FIELDNAM': 'S', 'CATDESC': 'Flux Density', 'LABLAXIS': 'Power Spectral Density'}}

        if self.header['file_type'] == 'SPS':
            self.header['nfreq'] = self.header['nchannels']
            if self.header['notes']['DUALSPECFILE']:

                self.header['nfeed'] = 2

                if 'banner0' in self.header.keys():

                    if 'RCP' in self.header['banner0']:
                        self.header['polar0'] = 'RR'
                    elif 'LCP' in self.header['banner0']:
                        self.header['polar0'] = 'LL'

                    else:
                        self.header['polar0'] = 'S'

                    if 'RCP' in self.header['banner1']:
                        self.header['polar1'] = 'RR'
                    elif 'LCP' in self.header['banner1']:
                        self.header['polar1'] = 'LL'
                    else:
                        self.header['polar1'] = 'S'

                else:

                    self.header['polar0'] = 'S'
                    self.header['polar1'] = 'S'

                if self.header['polar0'] == self.header['polar1']:
                    self.header['polar0'] = '{}0'.format(self.header['polar0'])
                    self.header['polar1'] = '{}1'.format(self.header['polar1'])

                self.header['feeds'].append(feed_tmp[self.header['polar0']])
                self.header['feeds'].append(feed_tmp[self.header['polar1']])

            else:

                self.header['nfeed'] = 1

                if 'banner0' in self.header.keys():

                    if 'RCP' in self.header['banner0']:
                        self.header['polar0'] = 'RR'
                    elif 'LCP' in self.header['banner0']:
                        self.header['polar0'] = 'RR'
                    else:
                        self.header['polar0'] = 'S'

                else:

                    self.header['polar0'] = 'S'

                self.header['feeds'].append(feed_tmp[self.header['polar0']])

            self.file_info['bytes_per_step'] = (self.header['nfreq'] * self.header['nfeed'] + 1) * 2
            self.file_info['data_format'] = '>{}H'.format(self.file_info['bytes_per_step'] // 2)

            self.header['fmin'] = float(self.header['notes']['LOWF']) / 1.E6  # MHz
            self.header['fmax'] = float(self.header['notes']['HIF']) / 1.E6  # MHz
            self.frequency = [self.header['fmax'] - float(ifreq) / (self.header['nfreq'] - 1)
                              * (self.header['fmax'] - self.header['fmin'])
                              for ifreq in range(self.header['nfreq'])]

        # SPD files

        elif self.header['file_type'] == 'SPD':
            self.header['nfreq'] = 1
            self.header['nfeed'] = self.header['nchannels']
            for i in range(self.header['nchannels']):
                self.header['feeds'][i] = {}
                self.header['feeds'][i]['FIELDNAM'] = 'CH{:02d}'.format(i)
                self.header['feeds'][i]['CATDESC'] = 'CH{:02d} Flux Density'.format(i)
                self.header['feeds'][i]['LABLAXIS'] = 'CH{:02d} Flux Density'.format(i)

            if self.header['notes']['INTEGER_SAVE_FLAG']:
                self.file_info['bytes_per_step'] = 2
                self.file_info['data_format'] = '{}h'.format(self.header['nfeed'])
            else:
                self.file_info['nbytes_per_sample'] = 8
                self.file_info['data_format'] = '{}d'.format(self.header['nfeed'])

            if self.header['notes']['NO_TIME_STAMPS_FLAG']:
                self.file_info['bytes_per_step'] = self.header['nfeed'] * self.file_info['nbytes_per_sample']
                self.file_info['data_format'] = '<{}'.format(self.file_info['data_format'])
            else:
                self.file_info['bytes_per_step'] = self.header['nfeed'] * self.file_info['nbytes_per_sample'] + 8
                self.file_info['data_format'] = '<1d{}'.format(self.file_info['data_format'])

            self.frequency = 20.1
            self.header['fmin'] = self.frequency  # MHz
            self.header['fmax'] = self.frequency  # MHz

        else:
            self.frequency = 0.

        if self.header['file_type'] == 'SPS':
            self.header['product_type'] = ('sp{}_{}'.format(self.header['nfeed'], self.header['nfreq']))
            self.file_info['record_data_offset'] = 0
        if self.header['file_type'] == 'SPD':
            self.header['product_type'] = ('ts{}'.format(self.header['nfeed']))
            if self.header['notes']['NO_TIME_STAMPS_FLAG']:
                self.file_info['record_data_offset'] = 0
            else:
                self.file_info['record_data_offset'] = 1

        self.header['nsweep'] = self.file_info['data_length'] // self.file_info['bytes_per_step']

        if self.header['file_type'] == 'SPS':
            time_step = (self.header['stop_jdtime'] - self.header['start_jdtime']) / float(self.header['nsweep'])
            time = [istep * time_step + self.header['start_jdtime'] for istep in range(self.header['nsweep'])]
        elif self.header['file_type'] == 'SPD':
            # if notes['NO_TIME_STAMPS_FLAG']:
            time_step = (self.header['stop_jdtime'] - self.header['start_jdtime']) / float(self.header['nsweep'])
            time = [float(istep) * time_step + self.header['start_jdtime']
                    for istep in range(self.header['nsweep'])]
            # else:
            # time = np.array()
            # for i in range(header['nstep']):
            #     time.append(data_raw[i][0])
            # time_step = np.median(time[1:header['nstep']]-time[0:header['nstep']-1])
        else:
            time = 0.
            time_step = 0.

        # transforming times from JD to datetime
        self.time = astropy.time.Time(time, format='jd').datetime

        # time sampling step in seconds
        self.header['time_step'] = time_step * 86400.
        self.header['time_integ'] = self.header['time_step']  # this will have to be checked at some point

        if self.debug:
            print("nfeed  : {}".format(self.header['nfeed']))
            print("nfreq  : {} ({})".format(self.header['nfreq'], len(self.frequency)))
            print("nsweep : {} ({})".format(self.header['nsweep'], len(self.time)))

        if self.verbose:
            print("nfeed  : {}".format(self.header['nfeed']))
            print("nfreq  : {}".format(self.header['nfreq']))
            print("nsweep : {}".format(self.header['nsweep']))

    def _close_radiojove_spx(self):
        """
        Closes the current SPS or SPD input file
        """
        if self.verbose:
            print("### [close_radiojove_spx]")

        self.file_info['lun'].close()

    def __len__(self):
        return self.header['nsweep']

    def _extract_radiojove_spx_data(self) -> dict:
        """
        :return:
        """

        if self.verbose:
            print("### [extract_radiojove_spx_data]")

        nstep = self.header['nsweep']  # len(time)
        nfreq = self.header['nfreq']  # len(freq)
        nfeed = self.header['nfeed']
        rec_0 = self.file_info['record_data_offset']

        var_list = [item['FIELDNAM'] for item in self.header['feeds']]

        # reading sweeps structure
        if self.verbose:
            print("Loading data into {} variable(s), from {}".format(', '.join(var_list), self.file_info['name']))

        data = dict()
        for var in var_list:
            data[var] = np.empty((nstep, nfreq), dtype=np.short)

        for j in range(0, self.header['nsweep'], _packet_size):
            j1 = j
            j2 = j + _packet_size
            if j2 > nstep:
                j2 = nstep

            if self.verbose:
                if _packet_size == 1:
                    print("Loading record #{}".format(j))
                else:
                    print("Loading records #{} to #{}".format(j1, j2))

            data_raw = np.array(self._read_radiojove_spx_sweep(j2 - j1))[:, rec_0:rec_0 + nfreq * nfeed]. \
                reshape(j2 - j1, nfreq, nfeed)

            for i in range(nfeed):
                data[var_list[i]][j1:j2, :] = data_raw[:, :, i].reshape(j2 - j1, nfreq)

        return data

    def _read_radiojove_spx_sweep(self, offset=None, read_size=_packet_size):
        """
        Reads raw data from SPS or SPD file
        :param read_size: number of sweep to read
        :return raw:
        """
        if self.verbose:
            print("### [read_radiojove_spx_sweep]")
            print("loading packet of {} sweep(s), with format `{}`.".format(read_size, self.file_info['data_format']))

        if offset is not None:
            self.file_info['lun'].seek(offset, 0)

        raw = []
        for i in range(read_size):
            raw.append(struct.unpack(self.file_info['data_format'],
                                     self.file_info['lun'].read(self.file_info['bytes_per_step'])))
            if raw[i][-1] != 65278:
                print("WARNING ! wrong end of sweep delimiter. (Got 0x{:04X} instead of 0x{:04X})".format(raw[i][-1],
                                                                                                          65278))

        if self.verbose:
            print("Size of loaded data: {}".format(len(raw)))

        return raw

    def display_header(self):
        """
        Displays header information from a given SPD or SPS file.
        """

        if self.verbose:
            print("### [display_header]")

        pp.pprint(self.header)

    def get_freq_axis(self):
        return self.frequency

    def get_time_axis(self):
        return self.time

    def get_first_sweep(self):
        return self.get_single_sweep(0)

    def get_last_sweep(self):
        return self.get_single_sweep(-1)

    def get_single_sweep(self, index_input=0):
        var_list = [item['FIELDNAM'] for item in self.header['feeds']]
        nfreq = self.header['nfreq']  # len(freq)
        nfeed = self.header['nfeed']
        rec_0 = self.file_info['record_data_offset']

        data_raw = np.array(
            self._read_radiojove_spx_sweep(offset=self.sweep_ptr_in_file[index_input], read_size=1)
        )[0, rec_0:rec_0 + nfreq * nfeed].reshape(nfreq, nfeed)
        data = dict()
        for i in range(nfeed):
            data[var_list[i]] = data_raw[:, i]
        return data

    def build_edr_data(self, start_time=None, end_time=None) -> dict:
        """
        Builds EDR (Experiment Data Record) elements.
        :param start_time: start time (datetime); using self.start_time if set to None
        :param end_time: end time (datetime); using self.end_time if set to None
        :return var: a dictionary containing: a header dictionary, a time list and a data dictionary
        """
        var, edr_start_time, edr_end_time = MaserData.build_edr_data(start_time, end_time)

        # loading time axis
        time_axis = self.get_time_axis()

        # adding header
        var['header'].update(self.header)

        # selecting channels on their names (e.g., remove extra channels)
        for chan_item in self.header['feeds']:
            var['data'][chan_item['FIELDNAM']] = list()

        # looping on time axis
        for ii, cur_time in enumerate(time_axis):

            # if cur_time is in input interval
            if edr_start_time <= cur_time < edr_end_time:

                var['time'].append(cur_time)
                for chan_item in var['data'].keys():
                    var['data'][chan_item].append(self.data[chan_item][ii])

        return var

    def _merge_check(self, other):

        if not isinstance(other, RadioJoveDataSPXFromFile):
            raise RadioJoveError('Trying to merge inconsistent objects')
        elif self.dataset_name != other.dataset_name:
            raise RadioJoveError('Trying to merge inconsistent datasets')
        elif self.start_time <= other.start_time < self.end_time:
            raise RadioJoveError('Trying to merge overlapping data')
        elif self.start_time < other.end_time <= self.end_time:
            raise RadioJoveError('Trying to merge overlapping data')
        elif self.start_time >= other.start_time and self.end_time <= other.end_time:
            raise RadioJoveError('Trying to merge overlapping data')
        elif self.start_time <= other.start_time and self.end_time >= other.end_time:
            raise RadioJoveError('Trying to merge overlapping data')
        else:
            return True

    def _merge_header(self, other):
        s_header = self.header.copy()
        o_header = other.header.copy()

        s_header_keys = list(s_header.keys())
        o_header_keys = list(o_header.keys())

        if s_header_keys != o_header_keys:
            if self.verbose:
                print("Warning, inconsistent header dict keys, trying to merge anyway...")
            if self.debug:

                s_key_missing = []
                for s_key in s_header_keys:
                    if s_key not in o_header_keys:
                        s_key_missing.append(s_key)
                if len(s_key_missing) > 0:
                    print("Missing header attributes in new file: {}".format(', '.join(s_key_missing)))

                o_key_missing = []
                for o_key in o_header_keys:
                    if o_key not in s_header_keys:
                        o_key_missing.append(o_key)
                if len(o_key_missing) > 0:
                    print("Missing header attributes in current file: {}".format(', '.join(s_key_missing)))

        for o_key in o_header.keys():

            if self.debug:
                print("Merging header: key = {}".format(o_key))

            if o_key in s_header.keys():

                if o_key.endswith('time'):
                    if o_key.startswith('start'):
                        if s_header[o_key] > o_header[o_key]:
                            self.header[o_key] = o_header[o_key]

                    if o_key.startswith('stop'):
                        if s_header[o_key] < o_header[o_key]:
                            self.header[o_key] = o_header[o_key]

            elif o_key in ["time_step", "time_integ"]:
                self.header[o_key] = (s_header[o_key] + o_header[o_key]) / 2

            elif o_key == "nsweep":
                self.header[o_key] = s_header[o_key] + o_header[o_key]

            elif o_key == "notes":
                self._merge_notes(other)

            elif s_header[o_key] != o_header[o_key]:

                if self.debug:
                    print("Warning:\n"
                          "self.header['{}'] = {}\n"
                          "other.header['{}'] = {}".format(o_key, s_header[o_key], o_key, o_header[o_key]))
                    print("Keeping original (self) value.")

            if self.debug:
                print("Merged header:")
                print(self.header[o_key])

    def _merge_notes(self, other):
        s_notes = self.header['notes'].copy()
        o_notes = other.header['notes'].copy()

        s_notes_keys = list(s_notes.keys())
        o_notes_keys = list(o_notes.keys())

        for o_key in o_notes_keys:

            if self.debug:
                print("Merging notes: key = {}".format(o_key))

            if o_key in s_notes_keys:

                if o_key == "SWEEPS":
                    self.header['notes'][o_key] = s_notes[o_key] + o_notes[o_key]

                elif s_notes[o_key] != o_notes[o_key]:

                    if self.debug:
                        print("Warning:\n"
                              "self.header['notes']['{}'] = {}\n"
                              "other.header['notes']['{}'] = {}".format(o_key, s_notes[o_key], o_key, o_notes[o_key]))
                        print("Keeping original (self) value.")

            if self.debug:
                print("Merged Notes:")
                print(self.header['notes'][o_key])

    def _merge_data(self, other):

        self.time = np.hstack((self.time.copy(), other.time))
        self.end_time = other.end_time
        for d_key in self.data.keys():
            self.data[d_key] = np.vstack((self.data[d_key].copy(), other.data[d_key]))
        self.file_info = [self.file_info.copy(), other.file_info]

    def append(self, other):

        if self._merge_check(other):
            self._merge_header(other)
            self._merge_data(other)


class RadioJoveDataCDF(MaserData):

    def __init__(self, parent, daily=False, cdf_version="01", data_version="01", verbose=True, debug=False):
        MaserData.__init__(self, verbose, debug)
        if daily:
            self.parent = self._merge_parents(parent)
        else:
            self.parent = RadioJoveDataSPXFromFile(parent, verbose=verbose, debug=debug)
        self.start_time = self.parent.start_time
        self.end_time = self.parent.end_time

        self.config = self._load_config()
        self.config['vers']['cdf'] = cdf_version
        self.config['vers']['dat'] = data_version
        if self.debug:
            print(self.config)

        self.file_info = dict()
        self.file_info['daily'] = daily
        self.file_info['parent'] = parent
        self.file_info['offset'] = 0
        self.file_info['name'] = self._cdf_file_name()
        if self.debug:
            print(self.file_info)

        if self.file_info['daily']:
            pass
        else:
            # Creating CDF file
            self.cdf_handle = self._init_cdf()

            # Filling Global Attributes from Parent file
            self._write_global_attr_cdf()

            # Creating and writing out Variables in CDF file
            self._write_var_epoch_cdf()
            self._write_var_frequency_cdf()
            self._write_var_data_cdf()

            # Closing CDF file
            self._close_cdf()

    def _load_config(self):

        config = dict()
        config['path'] = dict()
        config['path'] = self._lib_path()
        config['path']['out'] = os.environ.get('CDF_OUTPUT_DIR', '.')
        config['vers'] = {'cdf': "00", 'dat': "00", 'sft': __version__}
        config['proc'] = {'packet_size': os.environ.get('CDF_PROCESSING_PACKET_SIZE', _packet_size)}

        return config

    def _merge_parents(self, parent):

        parent.sort()
        first_parent = parent.pop(0)
        o = RadioJoveDataSPXFromFile(first_parent, verbose=self.verbose, debug=self.debug)
        for item in parent:
            o_tmp = RadioJoveDataSPXFromFile(item, verbose=self.verbose, debug=self.debug)

            # first test some obvious cases that would not be valid for merging
            if o_tmp.start_time < o.end_time:
                raise RadioJoveError("Inconsistent intervals (overlapping or files not correctly sorted)")
            elif o_tmp.dataset_name != o.dataset_name:
                raise RadioJoveError("Inconsistent datasets")

            # then do the merge:
            else:
                o.append(o_tmp)

        return o

    def _cdf_file_name(self):

        # Setting up the CDF output name
        if self.file_info['daily']:
            cdfout_name = "radiojove_{}_{}_{}_{}_{:%Y%m%d}_V{}.cdf".\
                format(self.parent.header['obsty_id'], self.parent.header['instr_id'], self.parent.header['level'],
                       self.parent.header['product_type'], self.start_time.date(), self.config['vers']['cdf']).lower()
        else:
            cdfout_name = "radiojove_{}_{}_{}_{}_{:%Y%m%d%H%M}_V{}.cdf"\
                .format(self.parent.header['obsty_id'], self.parent.header['instr_id'], self.parent.header['level'],
                        self.parent.header['product_type'], self.start_time, self.config['vers']['cdf']).lower()

        return cdfout_name

    def _init_cdf(self):
        """
        Initialization of the output CDF file
        """
        if self.debug:
            print("### [init_radiojove_cdf]")

        # removing existing CDF file with same name if necessary (PyCDF cannot overwrite a CDF file)
        cdfout_path = os.path.join(self.config['path']['out'], self.file_info['name'])
        if os.path.exists(cdfout_path):
            os.remove(cdfout_path)

        print("CDF file output: {}".format(cdfout_path))

        #    Opening CDF object
        cdf.lib.set_backward(False)  # this is setting the CDF version to be used
        cdfout = cdf.CDF(cdfout_path, '')
        cdfout.col_major(True)  # Column Major
        cdfout.compress(cdf.const.NO_COMPRESSION)  # No file level compression

        return cdfout

    def _close_cdf(self):
        """
        Closes the current output CDF file
        """

        if self.debug:
            print("### [close_radiojove_cdf]")

        self.cdf_handle.close()

    def _write_global_attr_cdf(self):
        """
        Writes the Global Attributes into the CDF file
        """

        if self.debug:
            print("### [write_gattr_radiojove_cdf]")

        # Creating Time and Frequency Axes
        jul_date = astropy.time.Time(self.parent.time, format="datetime", scale="utc").jd.tolist()

        # SETTING ISTP GLOBAL ATTRIBUTES
        self.cdf_handle.attrs['Project'] = ["PDS>Planetary Data System", "PADC>Paris Astronomical Data Centre"]
        self.cdf_handle.attrs['Discipline'] = "Space Physics>Magnetospheric Science"
        self.cdf_handle.attrs['Data_type'] = "{}_{}".format(self.parent.header['level'],
                                                            self.parent.header['product_type']).upper()
        self.cdf_handle.attrs['Descriptor'] = "{}_{}".format(self.parent.header['obsty_id'],
                                                             self.parent.header['instr_id']).upper()
        self.cdf_handle.attrs['Data_version'] = self.config['vers']['dat']
        self.cdf_handle.attrs['Instrument_type'] = "Radio Telescope"
        self.cdf_handle.attrs['Logical_source'] = "radiojove_{}_{}".format(self.cdf_handle.attrs['Descriptor'],
                                                                           self.cdf_handle.attrs['Data_type']).lower()
        self.cdf_handle.attrs['Logical_file_id'] = "{}_00000000_v00".format(self.cdf_handle.attrs['Logical_source'])
        self.cdf_handle.attrs['Logical_source_description'] = obs_description(self.parent.header['obsty_id'],
                                                                              self.parent.header['instr_id'])
        self.cdf_handle.attrs['File_naming_convention'] = "source_descriptor_datatype_yyyyMMdd_vVV"
        self.cdf_handle.attrs['Mission_group'] = "RadioJOVE"
        self.cdf_handle.attrs['PI_name'] = self.parent.header['author']
        self.cdf_handle.attrs['PI_affiliation'] = "RadioJOVE"
        self.cdf_handle.attrs['Source_name'] = "RadioJOVE"
        self.cdf_handle.attrs['TEXT'] = "RadioJOVE Project data. More info at http://radiojove.org and " + \
                                 "http://radiojove.gsfc.nasa.gov"
        self.cdf_handle.attrs['Generated_by'] = ["SkyPipe", "RadioJOVE", "PADC"]
        self.cdf_handle.attrs['Generation_date'] = "{:%Y%m%d}".format(datetime.datetime.now())
        self.cdf_handle.attrs['LINK_TEXT'] = ["Radio-SkyPipe Software available on ", "More info on RadioJOVE at ",
                                       "More info on Europlanet at "]
        self.cdf_handle.attrs['LINK_TITLE'] = ["Radio-SkyPipe website", "NASA/GSFC web page",
                                        "Paris Astronomical Data Centre"]
        self.cdf_handle.attrs['HTTP_LINK'] = ["http://www.radiosky.com/skypipeishere.html",
                                       "http://radiojove.gsfc.nasa.gov", "http://www.europlanet-vespa.eu"]
        self.cdf_handle.attrs['MODS'] = ""
        self.cdf_handle.attrs[
            'Rules_of_use'] = "RadioJOVE Data are provided for scientific use. As part of a amateur community " + \
                              "project, the RadioJOVE data should be used with careful attention. The " + \
                              "RadioJOVE observer of this particular file must be cited or added as a " + \
                              "coauthor if the data is central to the study. The RadioJOVE team " + \
                              "(radiojove-data@lists.nasa.gov) should also be contacted for any details about " + \
                              "publication of studies using this data."
        self.cdf_handle.attrs['Skeleton_version'] = self.config['vers']['cdf']
        self.cdf_handle.attrs['Sotfware_version'] = self.config['vers']['sft']
        self.cdf_handle.attrs['Time_resolution'] = "{} Seconds".format(str(self.parent.header['time_step']))
        self.cdf_handle.attrs[
            'Acknowledgement'] = "This study is using data from RadioJOVE project data, that are distributed " + \
                                 "by NASA/PDS/PPI and PADC at Observatoire de Paris (France)."
        self.cdf_handle.attrs['ADID_ref'] = ""
        self.cdf_handle.attrs['Validate'] = ""
        if isinstance(self.parent.header['file_name'], str):
            self.cdf_handle.attrs['Parent'] = os.path.basename(self.parent.header['file_name'])
        else:
            self.cdf_handle.attrs['Parent'] = [os.path.basename(item) for item in self.parent.header['file_name']]
        self.cdf_handle.attrs['Software_language'] = 'python'

        # SETTING PDS GLOBAL ATTRIBUTES
        self.cdf_handle.attrs['PDS_Start_time'] = self.parent.time[0].isoformat() + 'Z'
        self.cdf_handle.attrs['PDS_Stop_time'] = self.parent.time[-1].isoformat() + 'Z'
        self.cdf_handle.attrs['PDS_Observation_target'] = 'Jupiter'
        self.cdf_handle.attrs['PDS_Observation_type'] = 'Radio'

        # SETTING VESPA GLOBAL ATTRIBUTES
        self.cdf_handle.attrs['VESPA_dataproduct_type'] = "ds>Dynamic Spectra"
        self.cdf_handle.attrs['VESPA_target_class'] = "planet"
        self.cdf_handle.attrs['VESPA_target_region'] = "Magnetosphere"
        self.cdf_handle.attrs['VESPA_feature_name'] = "Radio Emissions#Aurora"

        self.cdf_handle.attrs['VESPA_time_min'] = jul_date[0]
        self.cdf_handle.attrs['VESPA_time_max'] = jul_date[-1]
        self.cdf_handle.attrs['VESPA_time_sampling_step'] = self.parent.header['time_step']
        self.cdf_handle.attrs['VESPA_time_exp'] = self.parent.header['time_integ']

        self.cdf_handle.attrs['VESPA_spectral_range_min'] = np.amin(self.parent.frequency) * 1e6
        self.cdf_handle.attrs['VESPA_spectral_range_max'] = np.amax(self.parent.frequency) * 1e6
        self.cdf_handle.attrs['VESPA_spectral_sampling_step'] = np.median(
            [self.parent.frequency[i + 1] - self.parent.frequency[i]
             for i in range(len(self.parent.frequency) - 1)]) * 1e6
        self.cdf_handle.attrs['VESPA_spectral_resolution'] = 50.e3

        self.cdf_handle.attrs['VESPA_instrument_host_name'] = self.parent.header['obsty_id']
        self.cdf_handle.attrs['VESPA_instrument_name'] = self.parent.header['instr_id']
        self.cdf_handle.attrs['VESPA_measurement_type'] = "phys.flux;em.radio"
        self.cdf_handle.attrs['VESPA_access_format'] = "application/x-cdf"

        # SETTING RADIOJOVE GLOBAL ATTRIBUTES

        self.cdf_handle.attrs['RadioJOVE_observer_name'] = self.parent.header['author']
        self.cdf_handle.attrs['RadioJOVE_observatory_loc'] = self.parent.header['obsloc']
        self.cdf_handle.attrs['RadioJOVE_observatory_lat'] = self.parent.header['latitude']
        self.cdf_handle.attrs['RadioJOVE_observatory_lon'] = self.parent.header['longitude']
        self.cdf_handle.attrs['RadioJOVE_sft_version'] = self.parent.header['rss_sw_version']
        self.cdf_handle.attrs['RadioJOVE_chartmin'] = self.parent.header['chartmin']
        self.cdf_handle.attrs['RadioJOVE_chartmax'] = self.parent.header['chartmax']
        self.cdf_handle.attrs['RadioJOVE_nchannels'] = self.parent.header['nfeed']

        self.cdf_handle.attrs['RadioJOVE_rcvr'] = -1
        self.cdf_handle.attrs['RadioJOVE_banner0'] = self.parent.header['banner0']
        self.cdf_handle.attrs['RadioJOVE_banner1'] = self.parent.header['banner1']
        self.cdf_handle.attrs['RadioJOVE_antenna_type'] = self.parent.header['antenna_type']
        self.cdf_handle.attrs['RadioJOVE_antenna_beam_az'] = 0
        self.cdf_handle.attrs['RadioJOVE_antenna_beam_el'] = 0
        self.cdf_handle.attrs['RadioJOVE_antenna_polar0'] = self.parent.header['polar0']
        self.cdf_handle.attrs['RadioJOVE_antenna_polar1'] = self.parent.header['polar1']
        self.cdf_handle.attrs['RadioJOVE_color_file'] = self.parent.header['color_file']
        self.cdf_handle.attrs['RadioJOVE_color_offset0'] = self.parent.header['offset0']
        self.cdf_handle.attrs['RadioJOVE_color_offset1'] = self.parent.header['offset1']
        self.cdf_handle.attrs['RadioJOVE_color_gain0'] = self.parent.header['gain0']
        self.cdf_handle.attrs['RadioJOVE_color_gain1'] = self.parent.header['gain1']
        self.cdf_handle.attrs['RadioJOVE_correction_filename'] = ""
        self.cdf_handle.attrs['RadioJOVE_caxf'] = ""
        self.cdf_handle.attrs['RadioJOVE_cax1'] = ""
        self.cdf_handle.attrs['RadioJOVE_cax2'] = ""
        self.cdf_handle.attrs['RadioJOVE_clockmsg'] = ""

        if self.debug:
            print(self.cdf_handle.attrs)

    def _write_var_epoch_cdf(self):
        """
        Writes the EPOCH variable into the output CDF file
        """

        if self.debug:
            print("### [write_epoch_radiojove_cdf]")

        date_start_round = self.parent.time[0].replace(minute=0, second=0, microsecond=0)
        date_stop_round = self.parent.time[-1].replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)

        # SETTING UP VARIABLES AND VARIABLE ATTRIBUTES
        #   The EPOCH variable type must be CDF_TIME_TT2000
        #   PDS-CDF requires no compression for variables.
        self.cdf_handle.new('EPOCH', data=self.parent.time, type=cdf.const.CDF_TIME_TT2000, compress=cdf.const.NO_COMPRESSION)
        self.cdf_handle['EPOCH'].attrs.new('VALIDMIN', data=datetime.datetime(2000, 1, 1), type=cdf.const.CDF_TIME_TT2000)
        self.cdf_handle['EPOCH'].attrs.new('VALIDMAX', data=datetime.datetime(2100, 1, 1), type=cdf.const.CDF_TIME_TT2000)
        self.cdf_handle['EPOCH'].attrs.new('SCALEMIN', data=date_start_round, type=cdf.const.CDF_TIME_TT2000)
        self.cdf_handle['EPOCH'].attrs.new('SCALEMAX', data=date_stop_round, type=cdf.const.CDF_TIME_TT2000)
        self.cdf_handle['EPOCH'].attrs['CATDESC'] = "Default time (TT2000)"
        self.cdf_handle['EPOCH'].attrs['FIELDNAM'] = "Epoch"
        self.cdf_handle['EPOCH'].attrs.new('FILLVAL', data=-9223372036854775808, type=cdf.const.CDF_TIME_TT2000)
        self.cdf_handle['EPOCH'].attrs['LABLAXIS'] = "Epoch"
        self.cdf_handle['EPOCH'].attrs['UNITS'] = "ns"
        self.cdf_handle['EPOCH'].attrs['VAR_TYPE'] = "support_data"
        self.cdf_handle['EPOCH'].attrs['SCALETYP'] = "linear"
        self.cdf_handle['EPOCH'].attrs['MONOTON'] = "INCREASE"
        self.cdf_handle['EPOCH'].attrs['TIME_BASE'] = "J2000"
        self.cdf_handle['EPOCH'].attrs['TIME_SCALE'] = "UTC"
        self.cdf_handle['EPOCH'].attrs['REFERENCE_POSITION'] = "Earth"
        self.cdf_handle['EPOCH'].attrs['SI_CONVERSION'] = "1.0e-9>s"
        self.cdf_handle['EPOCH'].attrs['UCD'] = "time.epoch"

        if self.debug:
            print(self.cdf_handle['EPOCH'])
            print(self.cdf_handle['EPOCH'].attrs)

    def _write_var_frequency_cdf(self):
        """
        Writes the FREQUENCY variable into the output CDF file
        """

        if self.debug:
            print("### [write_frequency_radiojove_cdf]")

        # PDS-CDF requires no compression for variables.
        self.cdf_handle.new('FREQUENCY', data=self.parent.frequency, type=cdf.const.CDF_FLOAT,
                            compress=cdf.const.NO_COMPRESSION, recVary=False)
        self.cdf_handle['FREQUENCY'].attrs['CATDESC'] = "Frequency"
        self.cdf_handle['FREQUENCY'].attrs['DICT_KEY'] = "electric_field>power"
        self.cdf_handle['FREQUENCY'].attrs['FIELDNAM'] = "FREQUENCY"
        self.cdf_handle['FREQUENCY'].attrs.new('FILLVAL', data=-1.0e+31, type=cdf.const.CDF_REAL4)
        self.cdf_handle['FREQUENCY'].attrs['FORMAT'] = "F6.3"
        self.cdf_handle['FREQUENCY'].attrs['LABLAXIS'] = "Frequency"
        self.cdf_handle['FREQUENCY'].attrs['UNITS'] = "MHz"
        self.cdf_handle['FREQUENCY'].attrs.new('VALIDMIN', data=0., type=cdf.const.CDF_REAL4)
        self.cdf_handle['FREQUENCY'].attrs.new('VALIDMAX', data=40., type=cdf.const.CDF_REAL4)
        self.cdf_handle['FREQUENCY'].attrs['VAR_TYPE'] = "support_data"
        self.cdf_handle['FREQUENCY'].attrs['SCALETYP'] = "linear"
        self.cdf_handle['FREQUENCY'].attrs.new('SCALEMIN', data=self.parent.header['fmin'], type=cdf.const.CDF_REAL4)
        self.cdf_handle['FREQUENCY'].attrs.new('SCALEMAX', data=self.parent.header['fmax'], type=cdf.const.CDF_REAL4)
        self.cdf_handle['FREQUENCY'].attrs['SI_CONVERSION'] = "1.0e6>Hz"
        self.cdf_handle['FREQUENCY'].attrs['UCD'] = "em.freq"

        if self.debug:
            print(self.cdf_handle['FREQUENCY'])
            print(self.cdf_handle['FREQUENCY'].attrs)

    def _write_var_data_cdf(self):
        """
        Writes DATA variables into output CDF file
        """

        if self.debug:
            print("### [write_data_radiojove_cdf]")

        nt = self.parent.header['nsweep']  # len(time)
        nf = self.parent.header['nfreq']  # len(freq)

        var_name_list = []
        # defining variables
        for feed in self.parent.header['feeds']:
            var_name = feed['FIELDNAM']
            var_name_list.append(var_name)

            if self.debug:
                print("Creating {} variable".format(var_name))

            # We deal with EDR data (direct output from experiment) in Unsigned 2-byte integers.
            #   PDS-CDF requires no compression for variables.
            self.cdf_handle.new(var_name, data=np.zeros((nt, nf)), type=cdf.const.CDF_UINT2,
                                compress=cdf.const.NO_COMPRESSION)
            self.cdf_handle[var_name].attrs['CATDESC'] = feed['CATDESC']
            self.cdf_handle[var_name].attrs['DEPEND_0'] = "EPOCH"
            self.cdf_handle[var_name].attrs['DEPEND_1'] = "FREQUENCY"
            self.cdf_handle[var_name].attrs['DICT_KEY'] = "electric_field>power"
            self.cdf_handle[var_name].attrs['DISPLAY_TYPE'] = "spectrogram"
            self.cdf_handle[var_name].attrs['FIELDNAM'] = var_name
            self.cdf_handle[var_name].attrs.new('FILLVAL', data=65535, type=cdf.const.CDF_UINT2)
            self.cdf_handle[var_name].attrs['FORMAT'] = "E12.2"
            self.cdf_handle[var_name].attrs['LABLAXIS'] = feed['LABLAXIS']
            self.cdf_handle[var_name].attrs['UNITS'] = "ADU"
            self.cdf_handle[var_name].attrs.new('VALIDMIN', data=0, type=cdf.const.CDF_UINT2)
            self.cdf_handle[var_name].attrs.new('VALIDMAX', data=4096, type=cdf.const.CDF_UINT2)
            self.cdf_handle[var_name].attrs['VAR_TYPE'] = "data"
            self.cdf_handle[var_name].attrs['SCALETYP'] = "linear"
            self.cdf_handle[var_name].attrs.new('SCALEMIN', data=2050, type=cdf.const.CDF_UINT2)
            self.cdf_handle[var_name].attrs.new('SCALEMAX', data=2300, type=cdf.const.CDF_UINT2)
            self.cdf_handle[var_name].attrs['FORMAT'] = "E12.2"
            self.cdf_handle[var_name].attrs['FORM_PTR'] = ""
            self.cdf_handle[var_name].attrs['SI_CONVERSION'] = " "
            self.cdf_handle[var_name].attrs['UCD'] = "phys.flux;em.radio"

            if self.debug:
                print("Loading data into {} variable, from {}".
                      format(var_name, self.parent.file_info['name']))

            self.cdf_handle[feed['FIELDNAM']] = self.parent.data[feed['FIELDNAM']]
#
#     def check_cdf(self):


################################################################################
# Observatory Descriptions
################################################################################
def obs_description(obsty, instr, debug=False):
    """
    Loads observatory description
    :param obsty: Observatory short name (call sign)
    :param instr: Instrument short name
    :param debug: Set to True to have verbose output
    :return desc: a character string with the description of the observatory and instrument
    """
    if debug:
        print("### [obs_description]")

    desc = "RadioJOVE {}".format(obsty.upper())

    # At the moment, only AJ4CO/DPS has been tested.
    if instr.upper() == 'DPS':
        desc = "{} Dual Polarization Spectrograph".format(desc)
    elif instr.upper() == "TWB":
        desc = "{} Tunable Wide Band Receiver".format(desc)
    elif instr.upper() == "RSP":
        desc = "{} RadioJOVE kit".format(desc)
    else:
        desc = "{} {} Spectrograph".format(desc, instr.upper())
    return desc


################################################################################
# SPX to CDF Conversion for daily set of files
################################################################################
def convert_spx_to_cdf_daily(file_list, debug=False):
    """
    Computes CDF file from a set of SPS or SPD file(s) on the same day
    :param file_list: list of files to process
    :param debug: Set to True to have verbose output
    :return:
    """

    nfiles = len(file_list)

    file_info = list()
    for item in file_list:
        file_info.append({'daily': True, 'name': item})

    # Checking file set consistency

    header_list = list()
    time_list = list()
    frequency_list = list()

    start_time = datetime.datetime.now()
    stop_time = datetime.datetime.now()

    for ii in range(nfiles):
        # Opening file, initializing file info and loading header + notes
        o = RadioJoveDataSPXFromFile(file_info[ii], debug)
        h_tmp, t_tmp, f_tmp = o.header, o.time, o.frequency

        header_list.append(h_tmp)
        time_list.append(t_tmp)
        frequency_list.append(f_tmp)

        if debug:
            print("{}: {} to {}".format(ii, h_tmp['start_time'].isoformat(), h_tmp['stop_time'].isoformat()))

        if ii == 0:

            start_time = h_tmp['start_time']
            stop_time = h_tmp['stop_time']

        else:

            if h_tmp['start_time'] < stop_time:
                raise RadioJoveError("Overlaping Files")
            else:
                stop_time = h_tmp['stop_time']

        if debug:
            print("all: {} to {}".format(start_time.isoformat(), stop_time.isoformat()))

    if stop_time - start_time > datetime.timedelta(hours=24):
        raise RadioJoveError("Data interval > 24h")

    if start_time.date() != stop_time.date():
        raise RadioJoveError("Files Not On Same Date")

    # merging headers
    header = dict()
    time = list()
    frequency = frequency_list[0]

    for ii in range(nfiles):
        header = merge_headers(header, header_list[ii], debug=debug)
        notes = merge_notes(notes, notes_list[ii], debug=debug)
        file_info[ii]['offset'] = len(time)
        time.extend(time_list[ii])

        if set(frequency) != set(frequency_list[ii]):
            raise RadioJoveError("Inconsistent Frequency list {}".format(ii))

    # Fixing duplicate headers

    # Processing files

    # initializing CDF file
    cdfout = init_radiojove_cdf(file_info[0], header, time[0], config, debug)
    write_gattr_radiojove_cdf(cdfout, header, time, frequency, config, debug)
    write_epoch_radiojove_cdf(cdfout, time, debug)

    write_data_radiojove_cdf(cdfout, header_list[0], file_info[0], config['proc']['packet_size'], debug)

    for ii in range(nfiles):
        if ii == 0:
            pass
        else:
            write_data_radiojove_cdf(cdfout, header_list[ii], file_info[ii], config['proc']['packet_size'], debug)

    write_frequency_radiojove_cdf(cdfout, header, frequency, debug)

    close_radiojove_cdf(cdfout, debug)

    fix_radiojove_cdf(file_info[0], config, debug)
    check_radiojove_cdf(file_info[0], config, debug)


################################################################################
# SPX to CDF Conversion for single files
################################################################################
def convert_spx_to_cdf_single(file_spx, verbose=True, debug=False):
    """
    Converts single SPx (SPS or SPD) files into single CDF file
    :param file_spx:
    :param debug:
    """

    cdf = RadioJoveDataCDF(file_spx, daily=False, verbose=verbose, debug=debug)
    # cdf.check_cdf()
    return cdf.file_info['name']


################################################################################
# Main SPX to CDF
################################################################################
def convert_spx_to_cdf(file_spx, daily=False, debug=False):
    """
    Main script that transforms an SPS or SPD file(s) into a CDF file(s)
    :param file_spx: path of input SPS or SPD file(s)
    :param daily: Set to True to output daily file (CDF name contains only the date)
    :param debug: Set to True to have verbose output
    """
    if debug:
        print("### [spx_to_cdf]")

    try:
        # file_sps='/Users/baptiste/Projets/VOParis/RadioJove/data/CDF/data/dat/V01/spectrogram/AJ4CO_DPS_150101071000_corrected_using_CA_2014_12_18_B.sps'
        # file_spd='/Users/baptiste/Projets/VOParis/RadioJove/data/CDF/data/dat/V01/timeseries/AJ4CO_RSP_UT150101000009.spd'

        # if daily => a list of files is passed in file_spx
        if isinstance(file_spx, str):
            file_list = [file_spx]
        elif isinstance(file_spx, list):
            file_list = file_spx
        else:
            raise RadioJoveError("Wrong Input (must be single path to file (string) or list of paths).")
        nfiles = len(file_list)

        file_info = dict(daily=daily)
        file_info['name'] = ''

        if daily:

            convert_spx_to_cdf_daily(file_list, debug)

        else:

            if nfiles != 1:
                raise RadioJoveError("Regular processing (not daily) must include a single file")
            else:
                convert_spx_to_cdf_single(file_spx, debug)

    except RadioJoveError as e:
        print(e)



