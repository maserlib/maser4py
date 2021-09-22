#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python module to read a Wind/Waves data file.
@author: X.Bonnin (LESIA)
"""

import logging
import struct

__all__ = ['read_l2_hres', 'read_l2_60s']

logger = logging.getLogger(__name__)

def read_l2_hres(filepath):
    """
    Method to read a Wind/Waves l2 high resolution data file

    :param filepath: Path of the input Wind Waves L2 high resolution binary file
    :return: dictionary with header and data as lists (one row per sweep)
    """
    header_fields = ('P_FIELD','JULIAN_DAY_B1','JULIAN_DAY_B2','JULIAN_DAY_B3','MSEC_OF_DAY',
                     'RECEIVER_CODE','JULIAN_SEC_FRAC','YEAR','MONTH','DAY',
                     'HOUR','MINUTE','SECOND','JULIAN_SEC_FRAC',
                     'ISWEEP','IUNIT','NPBS','SUN_ANGLE','SPIN_RATE','KSPIN','MODE','LISTFR','NFREQ',
                     'ICAL','IANTEN','IPOLA','IDIPXY','SDURCY','SDURPA',
        'NPALCY','NFRPAL','NPALIF','NSPALF','NZPALF')
    header_dtype = '>bbbbihLhhhhhhfihhffhhhhhhhhffhhhhh'

    header = [] ; data = [] ; nsweep=1
    with open(filepath,'rb') as frb:
        while (True):
            try:
                logger.info('Reading sweep #%i' % (nsweep))
                # Reading number of octets in the current sweep
                block = frb.read(4)
                if (len(block) == 0): break
                loctets1 = struct.unpack('>i',block)[0]
                # Reading header parameters in the current sweep
                block = frb.read(80)
                header_i = dict(zip(header_fields,struct.unpack(header_dtype,block)))
                npalf = header_i['NPALIF'] ; nspal = header_i['NSPALF'] ; nzpal = header_i['NZPALF']
                # Reading frequency list (kHz) in the current sweep
                block = frb.read(4*npalf)
                freq = struct.unpack('>'+'f'*npalf,block)
                # Reading intensity and time values for S/SP in the current sweep
                block = frb.read(4*npalf*nspal)
                Vspal = struct.unpack('>'+'f'*npalf*nspal,block)
                block = frb.read(4*npalf*nspal)
                Tspal = struct.unpack('>'+'f'*npalf*nspal,block)
                # Reading intensity and time values for Z in the current sweep
                block = frb.read(4*npalf*nzpal)
                Vzpal = struct.unpack('>'+'f'*npalf*nzpal,block)
                block = frb.read(4*npalf*nzpal)
                Tzpal = struct.unpack('>'+'f'*npalf*nzpal,block)
                # Reading number of octets in the current sweep
                block = frb.read(4)
                loctets2 = struct.unpack('>i',block)[0]
                if (loctets2 != loctets1):
                    logger.error(f'Error reading file! ({loctets1} != {loctets2}')
                    return None
            except EOFError:
                logger.exception('End of file reached')
                break
            else:
                header.append(header_i)
                data.append({'FREQ':freq,'VSPAL':Vspal,'VZPAL':Vzpal,'TSPAL':Tspal,'TZPAL':Tzpal})
                nsweep+=1

    output = {'header': header, 'data': data}
    return output

def read_l2_60s(filepath):
    """
    Method to read a Wind/Waves l2 60 seconds averaged data file

    :param filepath: Path of the Wind/Waves L2 60SEC binary file
    :return: dictionary with header and data as lists (one row per sweep)
    """
    header_fields = ('P_FIELD','JULIAN_DAY_B1','JULIAN_DAY_B2','JULIAN_DAY_B3','MSEC_OF_DAY',
                     'RECEIVER_CODE',
                     'JULIAN_SEC',
                     'YEAR','MONTH','DAY',
                     'HOUR','MINUTE','SECOND',
                     'MOYSEC','IUNIT','NFREQ',
                     'X_GSE', 'Y_GSE', 'Z_GSE')
    header_dtype = '>bbbbihLhhhhhhhhhfff'

    header = [] ; data = [] ; nsweep=1
    with open(filepath,'rb') as frb:
        while (True):
            try:
                logger.info('Reading sweep #%i' % (nsweep))
                # Reading number of octets in the current sweep
                block = frb.read(4)
                if (len(block) == 0): break
                loctets1 = struct.unpack('>i',block)[0]
                # Reading header parameters in the current sweep
                block = frb.read(44)
                header_i = dict(zip(header_fields,struct.unpack(header_dtype,block)))
                nfreq = header_i['NFREQ']
                # Reading frequency list (kHz) in the current sweep
                block = frb.read(4*nfreq)
                freq = struct.unpack('>'+'f'*nfreq,block)
                # Reading mean, min, max intensity
                block = frb.read(4*nfreq)
                Smoy = struct.unpack('>'+'f'*nfreq,block)
                block = frb.read(4*nfreq)
                Smin = struct.unpack('>'+'f'*nfreq,block)
                block = frb.read(4*nfreq)
                Smax = struct.unpack('>'+'f'*nfreq,block)
                # Reading number of octets in the current sweep
                block = frb.read(4)
                loctets2 = struct.unpack('>i',block)[0]
                if (loctets2 != loctets1):
                    logger.error(f'Error reading file! ({loctets1} != {loctets2})')
                    return None
            except EOFError:
                logger.exception('End of file reached')
                break
            else:
                header.append(header_i)
                data.append({'FKHZ':freq,'SMEAN':Smoy,'SMIN':Smin,'SMAX':Smax})
                nsweep+=1

    output = {'header': header, 'data': data}
    return output


if (__name__=='__main__'):
    print('Python module to read Wind/Waves data file.')
