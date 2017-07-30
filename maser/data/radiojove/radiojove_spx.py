#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read RadioJOVE SPS and SPD raw data files
"""

import numpy as np
import os
import struct
import pprint as pp
import datetime
from astropy import time as astime
from maser.data.data import *
from maser.utils.cdf import cdf
import json

__author__ = "Baptiste Cecconi"
__date__ = "26-JUL-2017"
__version__ = "0.10"

__all__ = ["RadioJoveData"]

packet_size = 10000


class RadioJoveError(Exception):
    pass


################################################################################
# Defining the generic class for RadioJove Data (inherited from MaserData)
################################################################################
class RadioJoveData(MaserData):
    """
    Class for RadioJove data
    """

    def __init__(self, file, verbose=True, debug=False):
        MaserData.__init__(self, file, verbose, debug)
        self.file_info = {'name': self.file, 'size': self.file_size(), 'file_data_offset': 0}
        self.header, self.notes, self.time, self.frequency = self.open_radiojove_spx()
        self.data = self.extract_radiojove_spx_data()
        self.dataset = "_".join(["radiojove", self.header['obsty_id'].lower(), self.header['instr_id'].lower(),
                                 self.header['level'].lower(), self.header['product_type'].lower()])
        self.close_radiojove_spx()

    def extract_radiojove_spx_header(self):
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

        header = dict(sft=hdr_values[0].decode('ascii'))
        # date conversion: header dates are given in decimal days since 30/12/1899 00:00 (early morning!) == day 0.0
        # date values must be corrected by adding 2415018.5 = julian date 30/12/1899 00:00
        header['start_jdtime'] = hdr_values[1] + 2415018.5
        header['start_time'] = astime.Time(header['start_jdtime'], format='jd').datetime
        header['stop_jdtime'] = hdr_values[2] + 2415018.5
        header['stop_time'] = astime.Time(header['stop_jdtime'], format='jd').datetime
        header['latitude'] = hdr_values[3]
        header['longitude'] = hdr_values[4]
        header['chartmax'] = hdr_values[5]
        header['chartmin'] = hdr_values[6]
        header['timezone'] = hdr_values[7]
        # For the next 4 header keywords, we remove leading and trailing null (0x00) and space characters
        header['source'] = (hdr_values[8].decode('ascii').strip('\x00')).strip(' ')
        header['author'] = (hdr_values[9].decode('ascii').strip('\x00')).strip(' ')
        header['obsname'] = (hdr_values[10].decode('ascii').strip('\x00')).strip(' ')
        header['obsloc'] = (hdr_values[11].decode('ascii').strip('\x00')).strip(' ')
        header['nchannels'] = hdr_values[12]
        header['note_length'] = hdr_values[13]

        return header

    def extract_radiojove_sps_notes(self):
        """
        Extracts the extended header information (notes) for SPS files (spectrograph)
        :param self:
        :return notes: dictionary containing the extracted header notes
        """
        if self.verbose:
            print("### [extract_radiojove_sps_notes]")

        raw_notes = self.file_info['notes_raw']
        notes = dict()

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
        # CHECK LIST WITH https://voparis-confluence.obspm.fr/display/JOVE/RadioSky+Spectrograph-SPS+Metadata

        # list of metadata keys with multiple values
        key_list_multi = ['BANNER', 'COLOROFFSET', 'COLORGAIN', 'CAXF', 'CAX1', 'CAX2', 'CLOCKMSG']

        # list of metadata keys with integer values
        key_list_int = ['SWEEPS', 'STEPS', 'RCVR', 'COLORRES', 'COLOROFFSET']

        # list of metadata keys with floating point values
        key_list_float = ['LOWF', 'HIF', 'COLORGAIN']

        # stripping raw note text stream from "*[[*" and "*]]*" delimiters, and splitting with '\xff'
        start_index = raw_notes.find(b'*[[*')
        stop_index = raw_notes.find(b'*]]*')
        notes['free_text'] = raw_notes[0:start_index].decode('ascii')
        note_list = []
        cur_note = b''
        for bb in raw_notes[start_index + 4:stop_index]:
            if bb == 255:
                note_list.append(cur_note)
                cur_note = b''
            else:
                cur_note = b''.join([cur_note, struct.pack("B", bb)])

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

                        # if current key item has multiple values, initializing a list for the values
                        if key_item not in notes.keys():
                            notes[key_item] = []

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
                            notes[key_item].append(int(note_value.strip()))
                        elif key_item in key_list_float:
                            notes[key_item].append(float(note_value.strip()))
                        else:
                            notes[key_item].append(note_value)

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
                            notes[key_item] = int(note_value.strip())
                        elif key_item in key_list_float:
                            notes[key_item] = float(note_value.strip())
                        else:
                            notes[key_item] = note_value

# final special case: if not present this keyword (no value) says that we deal with single channel spectrograph data
        if 'DUALSPECFILE' not in notes.keys():
            notes['DUALSPECFILE'] = False
        else:
            if notes['DUALSPECFILE'].strip() == 'True':
                notes['DUALSPECFILE'] = True

        return notes

    def extract_radiojove_spd_notes(self):
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

        raw_notes = self.file_info['notes_raw']

        # initializing notes with 3 sub dictionaries.
        notes = dict(CHL={}, CHO={}, MetaData={})

        start_index = raw_notes.find('*[[*')
        stop_index = raw_notes.find('*]]*')
        notes['free_text'] = raw_notes[0:start_index]
        note_list = raw_notes[start_index + 4:stop_index].split('\xff')
        for note_item in note_list:

            if note_item == 'Logged Using UT':
                notes['Logged Using UT'] = True
            else:
                notes['Logged Using UT'] = False

            if note_item == 'No Time Stamps':
                notes['No Time Stamps'] = True
            else:
                notes['No Time Stamps'] = False

            if note_item[0:3] == 'CHL':
                notes['CHL'][int(note_item[3])] = note_item[4:]

            if note_item[0:3] == 'CHO':
                notes['CHO'][int(note_item[3])] = note_item[4:]

            if note_item == 'Integer Save':
                notes['Integer Save'] = True
            else:
                notes['Integer Save'] = False

            if note_item[0:7] == 'XALABEL':
                notes['XALABEL'] = note_item[7:]

            if note_item[0:7] == 'YALABEL':
                notes['YALABEL'] = note_item[7:]

            # extra metadata are present with a generic syntax Metadata_[KEY][0xC8][VALUE]
            if note_item[0:9] == 'MetaData_':
                item_metadata = note_item.split('\xc8')
                # removing any extra trailing character in key name (spaces or colon)
                notes['MetaData'][item_metadata[0][9:].strip(' ').strip(':').strip(' ')] = item_metadata[1]

        return notes

    def open_radiojove_spx(self):
        """
        Opens RadioJOVE SPS or SPD file for processing
        :return header, notes, time, frequency:
        """
        if self.verbose:
            print("### [open_radiojove_spx]")

        # Opening file:
        self.file_info['prim_hdr_length'] = 156
        self.file_info['lun'] = open(self.file_info['name'], 'rb')

        # Reading header:
        self.file_info['prim_hdr_raw'] = self.file_info['lun'].read(self.file_info['prim_hdr_length'])
        header = self.extract_radiojove_spx_header()
        header['file_name'] = self.file_info['name']
        header['file_type'] = self.file_info['name'][-3:].upper()

        # Reading notes:
        self.file_info['notes_raw'] = self.file_info['lun'].read(header['note_length'])
        if header['file_type'] == 'SPS':
            notes = self.extract_radiojove_sps_notes()
        elif header['file_type'] == 'SPD':
            notes = self.extract_radiojove_spd_notes()
            header['nfreq'] = 1
        else:
            notes = ''

        if header['obsname'] == 'AJ4CO DPS':
            header['obsty_id'] = 'AJ4CO'
            header['instr_id'] = 'DPS'
            header['gain0'] = notes['COLORGAIN'][0]
            header['gain1'] = notes['COLORGAIN'][1]
            header['offset0'] = notes['COLOROFFSET'][0]
            header['offset1'] = notes['COLOROFFSET'][1]
            header['banner0'] = notes['BANNER'][0].replace('<DATE>', header['start_time'].date().isoformat())
            header['banner1'] = notes['BANNER'][1].replace('<DATE>', header['start_time'].date().isoformat())
            header['antenna_type'] = notes['ANTENNATYPE']
            header['color_file'] = notes['COLORFILE']
            header['free_text'] = notes['free_text']
        else:
            header['obsty_id'] = 'ABCDE'
            header['instr_id'] = 'XXX'
            header['gain0'] = 2.00
            header['gain1'] = 2.00
            header['offset0'] = 2000
            header['offset1'] = 2000
            header['banner0'] = ''
            header['banner1'] = ''
            header['antenna_type'] = ''
            header['color_file'] = ''
            header['free_text'] = ''

        if header['file_type'] == 'SPS':
            header['level'] = 'EDR'
        if header['file_type'] == 'SPD':
            header['level'] = 'DDR'

        if self.debug:
            print(header)
            print(notes)

        # Reading data:

        self.file_info['data_length'] = self.file_info['size']-self.file_info['prim_hdr_length']-header['note_length']

        # nfeed = number of observation feeds
        # nfreq = number of frequency step (1 for SPD)
        # nstep = number of sweep (SPS) or time steps (SPD)

        # SPS files
        header['feeds'] = []

        feed_tmp = {'RR': {'FIELDNAM': 'RR', 'CATDESC': 'RCP Flux Density', 'LABLAXIS': 'RCP Power Spectral Density'},
                    'LL': {'FIELDNAM': 'LL', 'CATDESC': 'LCP Flux Density', 'LABLAXIS': 'LCP Power Spectral Density'},
                    'S': {'FIELDNAM': 'S', 'CATDESC': 'Flux Density', 'LABLAXIS': 'Power Spectral Density'}}

        if header['file_type'] == 'SPS':
            header['nfreq'] = header['nchannels']
            if notes['DUALSPECFILE']:

                header['nfeed'] = 2

                if 'banner0' in header.keys():

                    if 'RCP' in header['banner0']:
                        header['polar0'] = 'RR'
                    elif 'LCP' in header['banner0']:
                        header['polar0'] = 'LL'

                    else:
                        header['polar0'] = 'S'

                    if 'RCP' in header['banner1']:
                        header['polar1'] = 'RR'
                    elif 'LCP' in header['banner1']:
                        header['polar1'] = 'LL'
                    else:
                        header['polar1'] = 'S'

                else:

                    header['polar0'] = 'S'
                    header['polar1'] = 'S'

                header['feeds'].append(feed_tmp[header['polar0']])
                header['feeds'].append(feed_tmp[header['polar1']])

            else:

                header['nfeed'] = 1

                if 'banner0' in header.keys():

                    if 'RCP' in header['banner0']:
                        header['polar0'] = 'RR'
                    elif 'LCP' in header['banner0']:
                        header['polar0'] = 'RR'
                    else:
                        header['polar0'] = 'S'

                else:

                    header['polar0'] = 'S'

                header['feeds'].append(feed_tmp[header['polar0']])

            self.file_info['bytes_per_step'] = (header['nfreq'] * header['nfeed'] + 1) * 2
            self.file_info['data_format'] = '>{}H'.format(self.file_info['bytes_per_step'] // 2)

            header['fmin'] = float(notes['LOWF']) / 1.E6  # MHz
            header['fmax'] = float(notes['HIF']) / 1.E6  # MHz
            frequency = [header['fmax'] - float(ifreq) / (header['nfreq'] - 1) * (header['fmax'] - header['fmin'])
                         for ifreq in range(header['nfreq'])]

        # SPD files

        elif header['file_type'] == 'SPD':
            header['nfreq'] = 1
            header['nfeed'] = header['nchannels']
            for i in range(header['nchannels']):
                header['feeds'][i] = {}
                header['feeds'][i]['FIELDNAM'] = 'CH{:02d}'.format(i)
                header['feeds'][i]['CATDESC'] = 'CH{:02d} Flux Density'.format(i)
                header['feeds'][i]['LABLAXIS'] = 'CH{:02d} Flux Density'.format(i)

            if notes['INTEGER_SAVE_FLAG']:
                self.file_info['bytes_per_step'] = 2
                self.file_info['data_format'] = '{}h'.format(header['nfeed'])
            else:
                self.file_info['nbytes_per_sample'] = 8
                self.file_info['data_format'] = '{}d'.format(header['nfeed'])

            if notes['NO_TIME_STAMPS_FLAG']:
                self.file_info['bytes_per_step'] = header['nfeed'] * self.file_info['nbytes_per_sample']
                self.file_info['data_format'] = '<{}'.format(self.file_info['data_format'])
            else:
                self.file_info['bytes_per_step'] = header['nfeed'] * self.file_info['nbytes_per_sample'] + 8
                self.file_info['data_format'] = '<1d{}'.format(self.file_info['data_format'])

            frequency = 20.1
            header['fmin'] = frequency  # MHz
            header['fmax'] = frequency  # MHz

        else:
            frequency = 0.

        if header['file_type'] == 'SPS':
            header['product_type'] = ('sp{}_{}'.format(header['nfeed'], header['nfreq']))
            self.file_info['record_data_offset'] = 0
        if header['file_type'] == 'SPD':
            header['product_type'] = ('ts{}'.format(header['nfeed']))
            if notes['NO_TIME_STAMPS_FLAG']:
                self.file_info['record_data_offset'] = 0
            else:
                self.file_info['record_data_offset'] = 1

        header['nstep'] = self.file_info['data_length'] // self.file_info['bytes_per_step']

        if header['file_type'] == 'SPS':
            time_step = (header['stop_jdtime'] - header['start_jdtime']) / float(header['nstep'])
            time = [istep * time_step + header['start_jdtime'] for istep in range(header['nstep'])]
        elif header['file_type'] == 'SPD':
            # if notes['NO_TIME_STAMPS_FLAG']:
            time_step = (header['stop_jdtime'] - header['start_jdtime']) / float(header['nstep'])
            time = [float(istep) * time_step + header['start_jdtime'] for istep in range(header['nstep'])]
            # else:
            # time = np.array()
            # for i in range(header['nstep']):
            #     time.append(data_raw[i][0])
            # time_step = np.median(time[1:header['nstep']]-time[0:header['nstep']-1])
        else:
            time = 0.
            time_step = 0.

        # transforming times from JD to datetime
        time = astime.Time(time, format='jd').datetime

        # time sampling step in seconds
        header['time_step'] = time_step * 86400.
        header['time_integ'] = header['time_step']  # this will have to be checked at some point

        if self.debug:
            print("nfeed : {}".format(header['nfeed']))
            print("nfreq : {} ({})".format(header['nfreq'], len(frequency)))
            print("nstep : {} ({})".format(header['nstep'], len(time)))

        if self.verbose:
            print("nfeed : {}".format(header['nfeed']))
            print("nfreq : {}".format(header['nfreq']))
            print("nstep : {}".format(header['nstep']))

        return header, notes, time, frequency

    def display_header(self):
        """
        Displays header information from a given SPD or SPS file.
        """

        if self.verbose:
            print("### [display_header]")

        pp.pprint(self.header)
        pp.pprint(self.notes)

    def close_radiojove_spx(self):
        """
        Closes the current SPS or SPD input file
        :param self:
        :return:
        """
        if self.verbose:
            print("### [close_radiojove_spx]")

        self.file_info['lun'].close()

    def extract_radiojove_spx_data(self):
        """
        :return:
        """

        if self.verbose:
            print("### [extract_radiojove_spx_data]")

        nstep = self.header['nstep']  # len(time)
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

        for j in range(0, self.header['nstep'], packet_size):
            j1 = j
            j2 = j + packet_size
            if j2 > nstep:
                j2 = nstep

            if self.verbose:
                if packet_size == 1:
                    print("Loading record #{}".format(j))
                else:
                    print("Loading records #{} to #{}".format(j1, j2))

            data_raw = np.array(self.read_radiojove_spx_sweep(j2-j1))[:, rec_0:rec_0 + nfreq * nfeed].\
                reshape(j2 - j1, nfreq, nfeed)

            for i in range(nfeed):
                data[var_list[i]][j1:j2, :] = data_raw[:, :, i].reshape(j2 - j1, nfreq)

        return data

    def read_radiojove_spx_sweep(self, read_size):
        """
        Reads raw data from SPS or SPD file
        :param self:
        :param read_size: number of sweep to read
        :return raw:
        """
        if self.verbose:
            print("### [read_radiojove_spx_sweep]")
            print("loading packet of {} sweep(s), with format `{}`.".format(read_size, self.file_info['data_format']))

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


################################################################################
# Loading local config file
################################################################################
def load_local_config(config_file, debug=False):
    """
    Loads the local config file (example in ../config)
    :param config_file: file path to the local config file to be loaded
    :param debug: Set to True to have verbose output
    :return config: a dictionary with the local config file content

    The config file must have the following content:
    {
    "path":
        {
        "out": "where/to/output/cdf/files/",
        "bin": "/path/to/cdf/library/bin/",
        "pds": "/path/to/cdf-pds/library/bin/"
        },
    "vers":
        {
        "cdf": "00", (version of CDF file)
        "dat": "00", (version of original data file)
        "sft": "00"  (version of processing software, this one)
        },
    "proc":
        {
        "packet_size": 10000  (number of time steps to be loaded at once in the main loop)
        }
    }
    """

    if debug:
        print("### [load_local_config]")

    with open(config_file) as f:
        config = json.load(f)

    if debug:
        print(config)

    return config


################################################################################
# function to display header information
################################################################################

################################################################################
# Read SPx sweep
################################################################################

################################################################################
# Close SPx file
################################################################################

################################################################################
# Check CDF file with PDS script
################################################################################

################################################################################
# Check CDF file with PDS script
################################################################################

################################################################################
# Init CDF output file
################################################################################
def init_radiojove_cdf(file_info, header, start_time, config, debug=False):
    """
    Initialization of the output CDF file
    :param file_info: a dictionary containing the input file information
    :param header: a dictionary containing the input file header
    :param start_time: datetime object (starting of observation)
    :param config: a dictionary containing the local configuration
    :param debug: Set to True to have verbose output
    :return cdfout: the CDF handle to be used for further CDF operations
    """
    if debug:
        print("### [init_radiojove_cdf]")

    # Setting up the CDF output name
    if file_info['daily']:
        file_info['cdfout_file'] = "radiojove_{}_{}_{}_{}_{:%Y%m%d}_V{}.cdf".format(header['obsty_id'],
                                                                                    header['instr_id'],
                                                                                    header['level'],
                                                                                    header['product_type'],
                                                                                    start_time.date(),
                                                                                    config['vers']['cdf']).lower()
    else:
        file_info['cdfout_file'] = "radiojove_{}_{}_{}_{}_{:%Y%m%d%H%M}_V{}.cdf".format(header['obsty_id'],
                                                                                        header['instr_id'],
                                                                                        header['level'],
                                                                                        header['product_type'],
                                                                                        start_time,
                                                                                        config['vers']['cdf']).lower()

    # removing existing CDF file with same name if necessary (PyCDF cannot overwrite a CDF file)
    if os.path.exists(config['path']['out']+file_info['cdfout_file']):
        os.remove(config['path']['out']+file_info['cdfout_file'])
    
    print("CDF file output: {}".format(config['path']['out']+file_info['cdfout_file']))
        
#    Opening CDF object 
    cdf.lib.set_backward(False)  # this is setting the CDF version to be used
    cdfout = cdf.CDF(config['path']['out']+file_info['cdfout_file'], '')
    cdfout.col_major(True)                         # Column Major
    cdfout.compress(cdf.const.NO_COMPRESSION)    # No file level compression

    return cdfout
    

################################################################################
# Close CDF output file
################################################################################
def close_radiojove_cdf(cdfout, debug=False):
    """
    Closes the current output CDF file
    :param cdfout: CDF file handle to be closed
    :param debug: Set to True to have verbose output
    :return:
    """
    if debug:
        print("### [close_radiojove_cdf]")

    cdfout.close()
    

################################################################################
# Global Attributes for CDF 
################################################################################
def write_gattr_radiojove_cdf(cdfout, header, time, freq, config, debug=False):
    """
    Writes the Global Attributes into the CDF file
    :param cdfout: CDF file handle to be used
    :param header: a dictionary containing the input file header
    :param time: a datetime array (1 value for each sweep)
    :param freq: an array of frequency values (1 value for each step in a sweep)
    :param config: a dictionary containing the local configuration
    :param debug: Set to True to have verbose output
    :return:
    """
    if debug:
        print("### [write_gattr_radiojove_cdf]")

    # Creating Time and Frequency Axes 
    ndata = len(time)
    jul_date = astime.Time(time, format="datetime", scale="utc").jd.tolist()

    # SETTING ISTP GLOBAL ATTRIBUTES
    cdfout.attrs['Project'] = ["PDS>Planetary Data System", "PADC>Paris Astronomical Data Centre"]
    cdfout.attrs['Discipline'] = "Space Physics>Magnetospheric Science"
    cdfout.attrs['Data_type'] = "{}_{}".format(header['level'], header['product_type']).upper()
    cdfout.attrs['Descriptor'] = "{}_{}".format(header['obsty_id'], header['instr_id']).upper()
    cdfout.attrs['Data_version'] = config['vers']['cdf']
    cdfout.attrs['Instrument_type'] = "Radio Telescope"
    cdfout.attrs['Logical_source'] = "radiojove_{}_{}".format(cdfout.attrs['Descriptor'],
                                                              cdfout.attrs['Data_type']).lower()
    cdfout.attrs['Logical_file_id'] = "{}_00000000_v00".format(cdfout.attrs['Logical_source'])
    cdfout.attrs['Logical_source_description'] = obs_description(header['obsty_id'], header['instr_id'])
    cdfout.attrs['File_naming_convention'] = "source_descriptor_datatype_yyyyMMdd_vVV"
    cdfout.attrs['Mission_group'] = "RadioJOVE"
    cdfout.attrs['PI_name'] = header['author']
    cdfout.attrs['PI_affiliation'] = "RadioJOVE"
    cdfout.attrs['Source_name'] = "RadioJOVE"
    cdfout.attrs['TEXT'] = "RadioJOVE Project data. More info at http://radiojove.org and " + \
                           "http://radiojove.gsfc.nasa.gov"
    cdfout.attrs['Generated_by'] = ["SkyPipe", "RadioJOVE", "PADC"]
    cdfout.attrs['Generation_date'] = "{:%Y%m%d}".format(datetime.datetime.now())
    cdfout.attrs['LINK_TEXT'] = ["Radio-SkyPipe Software available on ", "More info on RadioJOVE at ",
                                 "More info on Europlanet at "]
    cdfout.attrs['LINK_TITLE'] = ["Radio-SkyPipe website", "NASA/GSFC web page",
                                  "Paris Astronomical Data Centre"]
    cdfout.attrs['HTTP_LINK'] = ["http://www.radiosky.com/skypipeishere.html",
                                 "http://radiojove.gsfc.nasa.gov", "http://www.europlanet-vespa.eu"]
    cdfout.attrs['MODS'] = ""
    cdfout.attrs['Rules_of_use'] = "RadioJOVE Data are provided for scientific use. As part of a amateur community " + \
                                   "project, the RadioJOVE data should be used with careful attention. The " + \
                                   "RadioJOVE observer of this particular file must be cited or added as a " + \
                                   "coauthor if the data is central to the study. The RadioJOVE team " + \
                                   "(radiojove-data@lists.nasa.gov) should also be contacted for any details about " + \
                                   "publication of studies using this data."
    cdfout.attrs['Skeleton_version'] = config['vers']['cdf']
    cdfout.attrs['Sotfware_version'] = config['vers']['sft']
    cdfout.attrs['Time_resolution'] = "{} Seconds".format(str(header['time_step']))
    cdfout.attrs['Acknowledgement'] = "This study is using data from RadioJOVE project data, that are distributed " + \
                                      "by NASA/PDS/PPI and PADC at Observatoire de Paris (France)."
    cdfout.attrs['ADID_ref'] = ""
    cdfout.attrs['Validate'] = ""
    if isinstance(header['file_name'], str):
        cdfout.attrs['Parent'] = os.path.basename(header['file_name'])
    else:
        cdfout.attrs['Parent'] = [os.path.basename(item) for item in header['file_name']]
    cdfout.attrs['Software_language'] = 'python'

    # SETTING PDS GLOBAL ATTRIBUTES
    cdfout.attrs['PDS_Start_time'] = time[0].isoformat()+'Z'
    cdfout.attrs['PDS_Stop_time'] = time[ndata-1].isoformat()+'Z'
    cdfout.attrs['PDS_Observation_target'] = 'Jupiter'
    cdfout.attrs['PDS_Observation_type'] = 'Radio'
    
    # SETTING VESPA GLOBAL ATTRIBUTES
    cdfout.attrs['VESPA_dataproduct_type'] = "ds>Dynamic Spectra"
    cdfout.attrs['VESPA_target_class'] = "planet"
    cdfout.attrs['VESPA_target_region'] = "Magnetosphere"
    cdfout.attrs['VESPA_feature_name'] = "Radio Emissions#Aurora"

    cdfout.attrs['VESPA_time_min'] = jul_date[0]
    cdfout.attrs['VESPA_time_max'] = jul_date[ndata-1]
    cdfout.attrs['VESPA_time_sampling_step'] = header['time_step']
    cdfout.attrs['VESPA_time_exp'] = header['time_integ']

    cdfout.attrs['VESPA_spectral_range_min'] = np.amin(freq)*1e6
    cdfout.attrs['VESPA_spectral_range_max'] = np.amax(freq)*1e6
    cdfout.attrs['VESPA_spectral_sampling_step'] = np.median([freq[i+1]-freq[i] for i in range(len(freq)-1)])*1e6
    cdfout.attrs['VESPA_spectral_resolution'] = 50.e3

    cdfout.attrs['VESPA_instrument_host_name'] = header['obsty_id']
    cdfout.attrs['VESPA_instrument_name'] = header['instr_id']
    cdfout.attrs['VESPA_measurement_type'] = "phys.flux;em.radio"
    cdfout.attrs['VESPA_access_format'] = "application/x-cdf"
        
    # SETTING RADIOJOVE GLOBAL ATTRIBUTES

    cdfout.attrs['RadioJOVE_observer_name'] = header['author']
    cdfout.attrs['RadioJOVE_observatory_loc'] = header['obsloc']
    cdfout.attrs['RadioJOVE_observatory_lat'] = header['latitude']
    cdfout.attrs['RadioJOVE_observatory_lon'] = header['longitude']
    cdfout.attrs['RadioJOVE_sft_version'] = header['sft']
    cdfout.attrs['RadioJOVE_chartmin'] = header['chartmin']
    cdfout.attrs['RadioJOVE_chartmax'] = header['chartmax']
    cdfout.attrs['RadioJOVE_nchannels'] = header['nfeed']

    cdfout.attrs['RadioJOVE_rcvr'] = -1
    cdfout.attrs['RadioJOVE_banner0'] = header['banner0']
    cdfout.attrs['RadioJOVE_banner1'] = header['banner1']
    cdfout.attrs['RadioJOVE_antenna_type'] = header['antenna_type']
    cdfout.attrs['RadioJOVE_antenna_beam_az'] = 0
    cdfout.attrs['RadioJOVE_antenna_beam_el'] = 0
    cdfout.attrs['RadioJOVE_antenna_polar0'] = header['polar0']
    cdfout.attrs['RadioJOVE_antenna_polar1'] = header['polar1']
    cdfout.attrs['RadioJOVE_color_file'] = header['color_file']
    cdfout.attrs['RadioJOVE_color_offset0'] = header['offset0']
    cdfout.attrs['RadioJOVE_color_offset1'] = header['offset1']
    cdfout.attrs['RadioJOVE_color_gain0'] = header['gain0']
    cdfout.attrs['RadioJOVE_color_gain1'] = header['gain1']
    cdfout.attrs['RadioJOVE_correction_filename'] = ""
    cdfout.attrs['RadioJOVE_caxf'] = ""
    cdfout.attrs['RadioJOVE_cax1'] = ""
    cdfout.attrs['RadioJOVE_cax2'] = ""
    cdfout.attrs['RadioJOVE_clockmsg'] = ""

    if debug:
        print(cdfout.attrs)
    

################################################################################
# EPOCH variable for CDF
################################################################################
def write_epoch_radiojove_cdf(cdfout, time, debug=False):
    """
    Writes the EPOCH variable into the output CDF file
    :param cdfout: CDF file handle to be used
    :param time: a datetime array (1 value for each sweep)
    :param debug: Set to True to have verbose output
    :return:
    """
    if debug:
        print("### [write_epoch_radiojove_cdf]")

    ndata = len(time)
    date_start_round = time[0].replace(minute=0, second=0, microsecond=0)
    date_stop_round = time[ndata-1].replace(minute=0, second=0, microsecond=0)+datetime.timedelta(hours=1)
    
    # SETTING UP VARIABLES AND VARIABLE ATTRIBUTES
    #   The EPOCH variable type must be CDF_TIME_TT2000
    #   PDS-CDF requires no compression for variables.
    cdfout.new('EPOCH', data=time, type=cdf.const.CDF_TIME_TT2000, compress=cdf.const.NO_COMPRESSION)
    cdfout['EPOCH'].attrs.new('VALIDMIN', data=datetime.datetime(2000, 1, 1), type=cdf.const.CDF_TIME_TT2000)
    cdfout['EPOCH'].attrs.new('VALIDMAX', data=datetime.datetime(2100, 1, 1), type=cdf.const.CDF_TIME_TT2000)
    cdfout['EPOCH'].attrs.new('SCALEMIN', data=date_start_round, type=cdf.const.CDF_TIME_TT2000)
    cdfout['EPOCH'].attrs.new('SCALEMAX', data=date_stop_round, type=cdf.const.CDF_TIME_TT2000)
    cdfout['EPOCH'].attrs['CATDESC'] = "Default time (TT2000)"
    cdfout['EPOCH'].attrs['FIELDNAM'] = "Epoch"
    cdfout['EPOCH'].attrs.new('FILLVAL', data=-9223372036854775808, type=cdf.const.CDF_TIME_TT2000)
    cdfout['EPOCH'].attrs['LABLAXIS'] = "Epoch"
    cdfout['EPOCH'].attrs['UNITS'] = "ns"
    cdfout['EPOCH'].attrs['VAR_TYPE'] = "support_data"
    cdfout['EPOCH'].attrs['SCALETYP'] = "linear" 
    cdfout['EPOCH'].attrs['MONOTON'] = "INCREASE"
    cdfout['EPOCH'].attrs['TIME_BASE'] = "J2000" 
    cdfout['EPOCH'].attrs['TIME_SCALE'] = "UTC" 
    cdfout['EPOCH'].attrs['REFERENCE_POSITION'] = "Earth"
    cdfout['EPOCH'].attrs['SI_CONVERSION'] = "1.0e-9>s" 
    cdfout['EPOCH'].attrs['UCD'] = "time.epoch"
    
    if debug:
        print(cdfout['EPOCH'])
        print(cdfout['EPOCH'].attrs)
    

################################################################################
# FREQUENCY variable for CDF
################################################################################
def write_frequency_radiojove_cdf(cdfout, header, freq, debug=False):
    """
    Writes the FREQUENCY variable into the output CDF file
    :param cdfout: CDF file handle to be used
    :param header: a dictionary containing the input file header
    :param freq: an array of frequency values (1 value for each step in a sweep)
    :param debug: Set to True to have verbose output
    :return:
    """
    if debug:
        print("### [write_frequency_radiojove_cdf]")

    # PDS-CDF requires no compression for variables.
    cdfout.new('FREQUENCY', data=freq, type=cdf.const.CDF_FLOAT, compress=cdf.const.NO_COMPRESSION, recVary=False)
    cdfout['FREQUENCY'].attrs['CATDESC'] = "Frequency"
    cdfout['FREQUENCY'].attrs['DICT_KEY'] = "electric_field>power"
    cdfout['FREQUENCY'].attrs['FIELDNAM'] = "FREQUENCY" 
    cdfout['FREQUENCY'].attrs.new('FILLVAL', data=-1.0e+31, type=cdf.const.CDF_REAL4)
    cdfout['FREQUENCY'].attrs['FORMAT'] = "F6.3"
    cdfout['FREQUENCY'].attrs['LABLAXIS'] = "Frequency" 
    cdfout['FREQUENCY'].attrs['UNITS'] = "MHz" 
    cdfout['FREQUENCY'].attrs.new('VALIDMIN', data=0., type=cdf.const.CDF_REAL4)
    cdfout['FREQUENCY'].attrs.new('VALIDMAX', data=40., type=cdf.const.CDF_REAL4)
    cdfout['FREQUENCY'].attrs['VAR_TYPE'] = "support_data"
    cdfout['FREQUENCY'].attrs['SCALETYP'] = "linear"
    cdfout['FREQUENCY'].attrs.new('SCALEMIN', data=header['fmin'], type=cdf.const.CDF_REAL4)
    cdfout['FREQUENCY'].attrs.new('SCALEMAX', data=header['fmax'], type=cdf.const.CDF_REAL4)
    cdfout['FREQUENCY'].attrs['SI_CONVERSION'] = "1.0e6>Hz" 
    cdfout['FREQUENCY'].attrs['UCD'] = "em.freq"

    if debug:
        print(cdfout['FREQUENCY'])
        print(cdfout['FREQUENCY'].attrs)


################################################################################
# Data variables for CDF
################################################################################
def write_data_radiojove_cdf(cdfout, header, file_info, packet_size, debug=False):
    """
    Writes DATA variables into output CDF file
    :param cdfout: CDF file handle to be used
    :param header: a dictionary containing the input file header
    :param file_info: a dictionary containing the input file information
    :param packet_size: how many sweeps to load at once
    :param debug: Set to True to have verbose output
    :return:
    """
    if debug:
        print("### [write_data_radiojove_cdf]")

    nt = header['nstep']  # len(time)
    nf = header['nfreq']  # len(freq)

    var_name_list = []
    # defining variables
    for feed in header['feeds']:
        var_name = feed['FIELDNAM']
        var_name_list.append(var_name)

        if var_name in cdfout.keys():
            if debug:
                print("Updating {} variable".format(var_name))
        else:
            if debug:
                print("Creating {} variable".format(var_name))

        # We deal with EDR data (direct output from experiment) in Unsigned 2-byte integers.
        #   PDS-CDF requires no compression for variables.
            cdfout.new(var_name, data=np.zeros((nt, nf)), type=cdf.const.CDF_UINT2,
                       compress=cdf.const.NO_COMPRESSION)
            cdfout[var_name].attrs['CATDESC'] = feed['CATDESC']
            cdfout[var_name].attrs['DEPEND_0'] = "EPOCH"
            cdfout[var_name].attrs['DEPEND_1'] = "FREQUENCY"
            cdfout[var_name].attrs['DICT_KEY'] = "electric_field>power"
            cdfout[var_name].attrs['DISPLAY_TYPE'] = "spectrogram"
            cdfout[var_name].attrs['FIELDNAM'] = var_name
            cdfout[var_name].attrs.new('FILLVAL', data=65535, type=cdf.const.CDF_UINT2)
            cdfout[var_name].attrs['FORMAT'] = "E12.2"
            cdfout[var_name].attrs['LABLAXIS'] = feed['LABLAXIS']
            cdfout[var_name].attrs['UNITS'] = "ADU"
            cdfout[var_name].attrs.new('VALIDMIN', data=0, type=cdf.const.CDF_UINT2)
            cdfout[var_name].attrs.new('VALIDMAX', data=4096, type=cdf.const.CDF_UINT2)
            cdfout[var_name].attrs['VAR_TYPE'] = "data"
            cdfout[var_name].attrs['SCALETYP'] = "linear"
            cdfout[var_name].attrs.new('SCALEMIN', data=2050, type=cdf.const.CDF_UINT2)
            cdfout[var_name].attrs.new('SCALEMAX', data=2300, type=cdf.const.CDF_UINT2)
            cdfout[var_name].attrs['FORMAT'] = "E12.2"
            cdfout[var_name].attrs['FORM_PTR'] = ""
            cdfout[var_name].attrs['SI_CONVERSION'] = " "
            cdfout[var_name].attrs['UCD'] = "phys.flux;em.radio"

    # reading sweeps structure
    if debug:
        print("Loading data into {} variable(s), from {}".format(', '.join(var_name_list), file_info['name']))

    for j in range(0, header['nstep'], packet_size):
        j1 = j
        j2 = j+packet_size
        if j2 > nt:
            j2 = nt

        if debug:
            if packet_size == 1:
                print("Loading record #{}".format(j))
            else: 
                print("Loading records #{} to #{}".format(j1, j2))

        data_raw = np.array(
            read_radiojove_spx_sweep(file_info, j2-j1, debug))[
                :, file_info['record_data_offset']:file_info['record_data_offset']+header['nfreq']*header['nfeed']
                ].reshape(j2-j1, header['nfreq'], header['nfeed'])
                
        for i in range(header['nfeed']):
            cdfout[header['feeds'][i]['FIELDNAM']][file_info['offset']+j1:file_info['offset']+j2, :] = data_raw[:, :, i]


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
# Merge SPS or SPD headers
################################################################################
def merge_headers(header0, header1, debug=False):
    """

    :param header0:
    :param header1:
    :return:
    """

    header = header0.copy()

    for kk in header1.keys():

        if debug:
            print("Merging header: key = {}".format(kk))

        if kk in header0.keys():

            if kk.endswith('time'):

                if kk.startswith('start'):

                    if header0[kk] > header1[kk]:
                        header[kk] = header1[kk]
                    else:
                        header[kk] = header0[kk]

                if kk.startswith('stop'):

                    if header0[kk] > header1[kk]:
                        header[kk] = header0[kk]
                    else:
                        header[kk] = header1[kk]

            elif kk == "time_step":

                header[kk] = (header0[kk] + header1[kk]) / 2

            elif kk == "time_integ":

                header[kk] = (header0[kk] + header1[kk]) / 2

            elif kk == "nstep":

                header[kk] = header0[kk] + header1[kk]

            elif header0[kk] != header1[kk]:

                if not isinstance(header0[kk], list):
                    header[kk] = [header0[kk]]

                if isinstance(header1[kk], list):
                    header[kk].extend(header1[kk])
                else:
                    header[kk].append(header1[kk])

                if kk == 'antenna_type' and len(header[kk]) > 1:
                    if 'unknown' in header[kk]:
                        header[kk].remove('unknown')

                print("Warning, merging mismatched header['{}']".format(kk))
                print("Header0:")
                print(header0[kk])
                print("Header1:")
                print(header1[kk])

        else:

            header[kk] = header1[kk]

        if debug:
            print("Merged header:")
            print(header[kk])

    return header


################################################################################
# Merge SPS or SPD notes
################################################################################
def merge_notes(notes0, notes1, debug=False):
    """

    :param notes0:
    :param notes1:
    :return:
    """

    notes = notes0.copy()

    for kk in notes1.keys():

        if debug:
            print("Merging notes: key = {}".format(kk))

        if kk in notes0.keys():

            if kk == "SWEEPS":

                notes[kk] = notes0[kk] + notes1[kk]

            elif notes0[kk] != notes1[kk]:

                if not isinstance(notes0[kk], list):
                    notes[kk] = [notes0[kk]]

                if isinstance(notes1[kk], list):
                    notes[kk].extend(notes1[kk])
                else:
                    notes[kk].append(notes1[kk])

                if kk == "ANTENNATYPE" and len(notes[kk]) > 1:
                    if 'unknown' in notes[kk]:
                        notes[kk].remove('unknown')

                print("Warning, merging mismatched notes['{}']".format(kk))
                print("Notes0:")
                print(notes0[kk])
                print("Notes1:")
                print(notes1[kk])

            else:
                pass

        else:
            notes[kk] = notes1[kk]

        if debug:
            print(notes[kk])

    return notes


################################################################################
# SPX to CDF Conversion for daily set of files
################################################################################
def spx_to_cdf_daily(file_list, config, debug=False):
    """
    Computes CDF file from a set of SPS or SPD file(s) on the same day
    :param file_list: list of files to process
    :param config:
    :param debug: Set to True to have verbose output
    :return:
    """

    nfiles = len(file_list)

    file_info = list()
    for item in file_list:
        file_info.append({'daily': True, 'name': item})

    # Checking file set consistency

    header_list = list()
    notes_list = list()
    time_list = list()
    frequency_list = list()

    for ii in range(nfiles):
        # Opening file, initializing file info and loading header + notes
        h_tmp, n_tmp, t_tmp, f_tmp = open_radiojove_spx(file_info[ii], debug)

        header_list.append(h_tmp)
        notes_list.append(n_tmp)
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
            print("all: {} to {}".format(start_time.isoformat(),stop_time.isoformat()))

    if stop_time - start_time > datetime.timedelta(hours=24):
        raise RadioJoveError("Data interval > 24h")

    if start_time.date() != stop_time.date():
        raise RadioJoveError("Files Not On Same Date")

    # merging headers
    header = dict()
    notes = dict()
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
def spx_to_cdf_single(file_spx, config, debug=False):
    """

    :param file_spx:
    :param config:
    :param debug:
    :return:
    """

    file_info = dict(daily=False)
    file_info['name'] = file_spx
    file_info['offset'] = 0

    # Opening file, initializing file info and loading header + notes
    header, notes, time, frequency = open_radiojove_spx(file_info, debug)

    # initializing CDF file
    cdfout = init_radiojove_cdf(file_info, header, time[0], config, debug)

    write_gattr_radiojove_cdf(cdfout, header, time, frequency, config, debug)
    write_epoch_radiojove_cdf(cdfout, time, debug)
    write_data_radiojove_cdf(cdfout, header, file_info, config['proc']['packet_size'], debug)
    write_frequency_radiojove_cdf(cdfout, header, frequency, debug)

    close_radiojove_cdf(cdfout, debug)

    check_radiojove_cdf(file_info, config)


################################################################################
# Main SPX to CDF 
################################################################################
def spx_to_cdf(file_spx, config_file='local_config_bc.json', daily=False, debug=False):
    """
    Main script that transforms an SPS or SPD file(s) into a CDF file(s)
    :param file_spx: path of input SPS or SPD file(s)
    :param config_file: path of local configuration file
    :param daily: Set to True to output daily file (CDF name contains only the date)
    :param debug: Set to True to have verbose output
    :return:
    """
    if debug:
        print("### [spx_to_cdf]")

    try:
        # setting up local paths, versions and processing parameters
        config = load_local_config(config_file, debug)

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

            spx_to_cdf_daily(file_list, config, debug)

        else:

            if nfiles != 1:
                raise RadioJoveError("Regular processing (not daily) must include a single file")
            else:
                spx_to_cdf_single(file_spx, config, debug)

    except RadioJoveError as e:
        print(e)




