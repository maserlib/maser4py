#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python module with methods to read STEREO/Waves data files.
@author: X.Bonnin (LESIA)
"""

import logging
import struct
import time
import numpy as np

__all__ = ['read_l2_hres', 'read_l2_60s']

logger = logging.getLogger(__name__)

def read_l2_hres(filepath):
    """
    Method to read a STEREO/Waves l2 high resolution data binary file.

    :param filepath: Path of the input STEREO/Waves L2 high resolution binary file
    :return: dictionary with header and data as lists (one row per sweep)
    """
    time0 = time.time()
    header_fields = ('i_rad',
                     'itcds_coarse', 'itcds_fine',
                     'jusecy',
                     'iamjcy_year', 'iamjcy_month', 'iamjcy_day',
                     'ihmscy_hour', 'ihmscy_minute', 'ihmscy_second',
                     'sfract',
                     'msti',
                     'npalcy',
                     'nfrpal',
                     'nfreq',
                     'nvoie',
                     'iant12_LFA', 'iant12_LFBC', 'iant12_HF12',
                     'nconfig',
                     'ncag2',
                     'nauto2',
                     'loopa',
                     'loopc')
    header_dtype = '>hiiihhhhhhffhhhhhhhhhhhh'

    # Frequency bandwith
    fband = [0.225, 0.900, 3.600, 12.50]

    # Initialize outputs
    header = []
    data = []
    nsweep = 0
    nsample = 0
    # Open input file
    logger.info(f'Parsing {filepath} ...')
    with open(filepath,'rb') as frb:
        # Loop over data in the file
        while True:
            try:
                # Init data for current sweep
                data_i = {}

                logger.debug('Reading sweep #%i' % (nsweep + 1))
                # Reading number of octets in the current sweep
                block = frb.read(4)
                if len(block) == 0:
                    break
                loctets1 = struct.unpack('>i', block)[0]
                # Reading header parameters in the current sweep
                block = frb.read(58)
                header_i = dict(zip(header_fields, struct.unpack(header_dtype, block)))
                nfreq = header_i['nfreq']
                npalcy = header_i['npalcy']
                nconfig = header_i['nconfig']
                ncag2 = header_i['ncag2']
                loopa = header_i['loopa']
                nauto2 = header_i['nauto2']
                loopc = header_i['loopc']
                # Reading frequency list (kHz) in the current sweep
                block = frb.read(4 * nfreq)
                data_i['fkhz'] = np.array(struct.unpack('>' + 'f' * nfreq, block), dtype=np.float32)
                # Reading time samples
                block = frb.read(4 * npalcy * nconfig)
                data_i['seconds'] = np.array(struct.unpack('>' + 'f' * npalcy * nconfig, block), dtype=np.float32)

                # Reading CAG1, CAG2, Auto1, Auto2, CrossR, CrossI and time values in the current sweep
                block = frb.read(4 * npalcy * nconfig)
                data_i['agc1'] = np.array(struct.unpack('>' + 'f' * npalcy * nconfig, block), dtype=np.float32)
                if ncag2 != 0:
                    block = frb.read(4 * ncag2 * nconfig)
                    data_i['agc2'] = np.array(struct.unpack('>' + 'f' * ncag2 * nconfig, block), dtype=np.float32)
                if loopa != 0:
                    block = frb.read(4 * nfreq * loopa)
                    data_i['auto1'] = np.array(struct.unpack('>' + 'f' * nfreq * loopa, block), dtype=np.float32)

                    if nauto2 != 0:
                        block = frb.read(4 * nauto2 * loopa)
                        data_i['auto2'] = np.array(struct.unpack('>' + 'f' * nauto2 * loopa, block), dtype=np.float32)

                if loopc != 0:
                    block = frb.read(4 * nfreq * loopc)
                    data_i['crosr'] = np.array(struct.unpack('>' + 'f' * nfreq * loopc, block), dtype=np.float32)
                    block = frb.read(4 * nfreq * loopc)
                    data_i['crosi'] = np.array(struct.unpack('>' + 'f' * nfreq * loopc, block), dtype=np.float32)

                # Define bandwith for list of frequencies
                ksample = nconfig * nfreq
                data_fi = np.zeros(ksample, dtype=int) + 1000 * (header_i['i_rad'] % 10)
                if header_i['i_rad'] % 10 <= 3:
                    data_fi = data_fi+np.arange(16)
                if(header_i['i_rad'] % 10) > 3:
                    data_fi = data_fi + np.int((data_i['fkhz'] - 125.) / 50)
                data_df = [fband[np.int(current_fi / 1000 - 1)] for current_fi in data_fi]

                # Add some header information in the data
                data_i['year'] = header_i['iamjcy_year']
                data_i['month'] = header_i['iamjcy_month']
                data_i['day'] = header_i['iamjcy_day']
                data_i['hour'] = header_i['ihmscy_hour']
                data_i['minute'] = header_i['ihmscy_minute']
                data_i['second'] = header_i['ihmscy_second']
                data_i['ant'] = ['iant12_LFA', 'iant12_LFBC', 'iant12_HF12']
                data_i['dt'] = header_i['msti']
                data_i['df'] = data_df
                data_i['sweep'] = nsweep + 1

                # Increment the total number of records
                nsample += ksample

                # Reading number of octets in the current sweep
                block = frb.read(4)
                loctets2 = struct.unpack('>i', block)[0]
                if loctets2 != loctets1:
                    logger.error(f'Error reading file! ({loctets1} != {loctets2})')
                    return None
            except EOFError:
                logger.debug('End of file reached')
                break
            else:
                header.append(header_i)
                data.append(data_i)
                nsweep += 1

    time1 = time.time()
    logger.info(f'{nsweep} sweeps read in {"{:.3f}".format(time1 - time0)} seconds.')
    logger.info(f'{nsample} samples stored.')

    return {'header': header, 'data': data}

def read_l2_60s(filepath):
    """
    Method to read a STEREO/Waves l2 60 seconds averaged data file

    :param filepath: Path of the STEREO/Waves L2 60SEC binary file
    :return: dictionary with header and data as lists (one row per sweep)
    """
    header = []
    data = []

    time0 = time.time()
    header_fields = ('i_rad',
                     'itcds_coarse', 'itcds_fine',
                     'jusecy',
                     'iamjcy_year', 'iamjcy_month', 'iamjcy_day',
                     'ihmscy_hour', 'ihmscy_minute', 'ihmscy_second',
                     'rua',
                     'hlat',
                     'hlon',
                     'moysec',
                     'nfreq',
                     )
    header_dtype = '>hiiihhhhhhfffhh'

    # Initialize outputs
    header = []
    data = []
    nsweep = 0
    nsample = 0
    # Open input file
    logger.info(f'Parsing {filepath} ...')
    with open(filepath,'rb') as frb:
        # Loop over data in the file
        while True:
            try:
                # Init data for current sweep
                data_i = {}

                logger.debug('Reading sweep #%i' % (nsweep + 1))
                # Reading number of octets in the current sweep
                block = frb.read(4)
                if len(block) == 0:
                    break
                loctets1 = struct.unpack('>i', block)[0]
                # Reading header parameters in the current sweep
                block = frb.read(42)
                header_i = dict(zip(header_fields, struct.unpack(header_dtype, block)))
                nfreq = header_i['nfreq']
                # Reading frequency list (kHz) in the current sweep
                block = frb.read(4 * nfreq)
                data_i['fkhz'] = np.array(struct.unpack('>' + 'f' * nfreq, block), dtype=np.float32)
                # Reading flux samples
                block = frb.read(4 * nfreq)
                data_i['flux'] = np.array(struct.unpack('>' + 'f' * nfreq, block), dtype=np.float32)

                # Add information from header
                data_i['year'] = header_i['iamjcy_year']
                data_i['month'] = header_i['iamjcy_month']
                data_i['day'] = header_i['iamjcy_day']
                data_i['hour'] = header_i['ihmscy_hour']
                data_i['minute'] = header_i['ihmscy_minute']
                data_i['second'] = header_i['ihmscy_second']
                data_i['hlat'] = header_i['hlat']
                data_i['hlon'] = header_i['hlon']

                # Increment the total number of records
                nsample += nfreq

                # Reading number of octets in the current sweep
                block = frb.read(4)
                loctets2 = struct.unpack('>i', block)[0]
                if loctets2 != loctets1:
                    logger.error(f'Error reading file! ({loctets1} != {loctets2})')
                    return None
            except EOFError:
                logger.debug('End of file reached')
                break
            else:
                header.append(header_i)
                data.append(data_i)
                nsweep += 1

    time1 = time.time()
    logger.info(f'{nsweep} sweeps read in {"{:.3f}".format(time1 - time0)} seconds.')
    logger.info(f'{nsample} samples stored.')


    return {'header': header, 'data': data}
