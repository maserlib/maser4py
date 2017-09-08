#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read a Viking/V4n/E5 data file from CDPP deep archive (http://cdpp-archive.cnes.fr).
@author: B.Cecconi(LESIA)
"""

import os
import struct
from maser.data.data import *
import datetime

__author__ = "Baptiste Cecconi"
__date__ = "29-AUG-2017"
__version__ = "0.01"

__all__ = ["CassiniKronosData", "CassiniKronosLevel", "CassiniKronosFile", "CassiniKronosRecord"]

# -------------------------------------------------------------------------------------------------------------------- #
# Module variables

all_periods = dict()
all_periods['Turn_on'] = {'start_time': datetime.datetime.strptime("1997298.00", '%Y%j.%H'),
                          'end_time': datetime.datetime.strptime("1997299.06", '%Y%j.%H') + datetime.timedelta(
                              hours=1)}
all_periods['Earth'] = {'start_time': datetime.datetime.strptime("1999227.10", '%Y%j.%H'),
                        'end_time': datetime.datetime.strptime("1999257.22", '%Y%j.%H') + datetime.timedelta(
                             hours=1)}
all_periods['Ico_m14'] = {'start_time': datetime.datetime.strptime("1998364.11", '%Y%j.%H'),
                          'end_time': datetime.datetime.strptime("1999005.23", '%Y%j.%H') + datetime.timedelta(
                              hours=1)}
all_periods['Venus1'] = {'start_time': datetime.datetime.strptime("1998116.13", '%Y%j.%H'),
                         'end_time': datetime.datetime.strptime("1998116.13", '%Y%j.%H') + datetime.timedelta(
                              hours=1)}
all_periods['Venus2'] = {'start_time': datetime.datetime.strptime("1999175.19", '%Y%j.%H'),
                         'end_time': datetime.datetime.strptime("1999175.21", '%Y%j.%H') + datetime.timedelta(
                             hours=1)}
dd_list = [1, 91, 181, 271, 367]
for yy in range(18):
    for dd in range(4):
        if not (yy == 17 and dd == 3):
            all_periods['{:04d}_{:03d}_{:03d}'.format(yy + 2000, dd_list[dd], dd_list[dd + 1] - 1)] \
                = {'start_time': datetime.datetime.strptime("{:04d}{:03d}.00".
                                                            format(yy + 2000, dd_list[dd], dd_list[dd + 1] - 1),
                                                            '%Y%j.%H'),
                   'end_time': datetime.datetime.strptime("{:04d}{:03d}.23".
                                                          format(yy + 2000, dd_list[dd], dd_list[dd + 1] - 1),
                                                          '%Y%j.%H') + datetime.timedelta(hours=1)}

all_levels = dict()
all_levels['k'] = {'name': 'Kronos Level 0', 'path': 'k'}
all_levels['n1'] = {'name': 'Kronos Level 1', 'path': 'n1'}
all_levels['n2'] = {'name': 'Kronos Level 2', 'path': 'n2'}
all_levels['n3b'] = {'name': 'Kronos Level 3b', 'path': 'n3b'}
all_levels['n3c'] = {'name': 'Kronos Level 3c', 'path': 'n3c'}
all_levels['n3d'] = {'name': 'Kronos Level 3d', 'path': 'n3d'}
all_levels['n3e'] = {'name': 'Kronos Level 3e', 'path': 'n3e'}
all_levels['n3g'] = {'name': 'Kronos Level 3g', 'path': 'n3g'}
all_levels['index'] = {'name': 'Kronos Level 4 Index', 'path': 'index'}
all_levels['loc'] = {'name': 'Kronos Level 4 Loc', 'path': 'loc'}
all_levels['skr'] = {'name': 'Kronos Level 4 SKR', 'path': 'skr'}


# -------------------------------------------------------------------------------------------------------------------- #
# Module classes


class KronosError(Exception):
    pass


class CassiniKronosLevel:

    def __init__(self, level, sublevel=None):
        self.name = level
        self.sublevel = sublevel
        self.implemented = True
        self.record_def = dict()
        if self.name == 'k':
            self.file_format = 'bin-compressed'
            self.implemented = False
            self.description = "Cassini/RPWS/HFR Level 0 (Telemetry)"
        elif self.name == 'n1':
            self.file_format = 'bin-fixed-record-length'
            self.implemented = True
            self.record_def['fields'] = ["ydh", "num", "ti", "fi", "dt", "c", "ant", "agc1", "agc2",
                                         "auto1", "auto2", "cross1", "cross2"]
            self.record_def['dtype'] = "<LLLLhbbbbbbhh"
            self.record_def['length'] = 28
            self.description = "Cassini/RPWS/HFR Level 1 (Receiver units)"
        elif self.name == 'n2':
            self.file_format = 'bin-fixed-record-length'
            self.record_def['fields'] = ["ydh", "num", "t97", "f", "dt", "df", "autoX", "autoZ",
                                         "crossR", "crossI", "ant"]
            self.record_def['dtype'] = "<LLdfffffffb"
            self.record_def['length'] = 45
            self.description = "Cassini/RPWS/HFR Level 2 (Physical units)"
        elif self.name == "n3b":
            self.file_format = 'bin-fixed-record-length'
            self.record_def['fields'] = ["ydh", "num0", "num1", "s0", "s1", "q0", "q1", "u0", "u1", "v0", "v1",
                                         "th", "ph", "zr", "snx0", "snz1", "snx0", "snz1"]
            self.record_def['dtype'] = "<LLLfffffffffffffff"
            self.record_def['length'] = 72
            self.description = "Cassini/RPWS/HFR Level 3b (Generic 3 antenna GP)"
        elif self.name == "n3c":
            self.file_format = 'bin-fixed-record-length'
            self.record_def['fields'] = ["ydh", "num0", "num1", "s", "q", "u", "v0", "v1",
                                         "th0", "th1", "ph0", "ph1", "zr", "snx0", "snz1", "snx0", "snz1"]
            self.record_def['dtype'] = "<LLLffffffffffffff"
            self.record_def['length'] = 68
            self.description = "Cassini/RPWS/HFR Level 3b (Circular polarization 3 antenna GP)"
        else:
            raise KronosError("Not yet implemented error")


class CassiniKronosData(object):

    def __init__(self, start_time=None, end_time=None, levels=list()):
        self.start_time = start_time
        self.end_time = end_time
        self.levels = levels
        self.rpws_data_dir = os.environ['NAS_RPWS']

        if self.start_time is not None and self.end_time is not None:
            self.periods = self.period_dir_list()
            self.files = list()
            for item in self.levels:
                self.files.extend(self.make_file_list(item))

            self.data = list()
            for item in self.files:
                self.data.extend(item.read_data_binary())

    def __str__(self):
        return "<{} object> {} to {} with level(s) {}".\
            format(type(self).__qualname__, self.start_time.isoformat(),
                   self.end_time.isoformat(), ', '.join([item.name for item in self.levels]))

    def __repr__(self):
        print(self)

    @classmethod
    def from_file(cls, file):
        file = CassiniKronosFile(file)
        start_time, end_time = file.extract_interval_from_file_name()
        levels = [file.extract_level_from_file_name()]
        return CassiniKronosData(start_time, end_time, levels)

    @classmethod
    def from_ydh_interval(cls, start_time, end_time, levels):
        start_time = datetime.datetime.strptime(start_time, "%Y%j.%H")
        end_time = datetime.datetime.strptime(end_time, "%Y%j.%H")
        if levels is list:
            levels = [CassiniKronosLevel(item) for item in levels]
        else:
            levels = [CassiniKronosLevel(levels)]
        return CassiniKronosData(start_time, end_time, levels)

    def load_extra_level(self, level, sublevel=None):
        new_level = CassiniKronosLevel(level, sublevel)
        self.levels.append(new_level)
        self.files.extend(self.make_file_list(new_level))
        for item in self.files:
            if item.level.name == new_level.name:
                self.data.extend(item.read_data_binary())

    def period_dir_list(self):
        this_dir_list = list()
        dir_list = all_periods
        for key, val in dir_list.items():
            if val['start_time'] <= self.end_time and val['end_time'] >= self.start_time:
                this_dir_list.append(key)
        return this_dir_list

    def level_path(self, period_dir, level):
        return os.path.join(os.path.join(self.rpws_data_dir, period_dir), all_levels[level.name]['path'])

    def make_file_list(self, level):
        file_list = list()
        for dir_item in self.period_dir_list():
            dir_path = self.level_path(dir_item, level)
            if os.path.exists(dir_path):
                for file_item in os.listdir(dir_path):
                    cur_file = CassiniKronosFile(os.path.join(dir_path, file_item))
                    if cur_file.start_time <= self.end_time and cur_file.end_time >= self.start_time:
                        file_list.append(cur_file)
#            else:
#                print("Warning directory doesn't exist: {}".format(dir_path))

        # file_list.sort(key=dict(zip(file_list, [item.file_name for item in file_list])).get)
        return file_list


class CassiniKronosFile(MaserDataFromFile):

    def __init__(self, file):
        MaserDataFromFile.__init__(self, file)
        self.level = self.extract_level_from_file_name()
        self.start_time, self.end_time = self.extract_interval_from_file_name()

    def __str__(self):
        return "<{} object> {}".format(type(self).__qualname__, self.file)

    def __repr__(self):
        print(self)

    def extract_level_from_file_name(self):
        file_name = self.get_file_name()
        if file_name.startswith('K'):
            level = CassiniKronosLevel('k')
        elif file_name.startswith('R'):
            level = CassiniKronosLevel('n1')
        elif file_name.startswith('P'):
            level = CassiniKronosLevel('n2')
        elif file_name.startswith('F'):
            level = CassiniKronosLevel('n3g')
        elif file_name.startswith('N'):
            level = CassiniKronosLevel('n3{}'.format(file_name[2]), file_name[4:7])
        elif file_name.startswith('bg'):
            level = CassiniKronosLevel('bg')
        elif '.v' in file_name:
            level = CassiniKronosLevel('ephem', 'veph')
        elif '.q' in file_name:
            level = CassiniKronosLevel('ephem', 'qeph')
        elif file_name.startswith('INDEX_3A'):
            level = CassiniKronosLevel('index', '3A')
        elif file_name.startswith('INDEX'):
            level = CassiniKronosLevel('index', '2A')
        elif file_name.endswith('.lis'):
            level = CassiniKronosLevel('lis')
        elif file_name.startswith('loc'):
            if '3A' in file_name:
                sublevel = '3A'
            else:
                sublevel = '2A'
            if 'err' in file_name:
                if sublevel == '3A':
                    sublevel = file_name[4:18]
                else:
                    sublevel = "{}_{}".format(sublevel, file_name[4:15])
            else:
                if sublevel == '3A':
                    sublevel = file_name[4:10]
                else:
                    sublevel = "{}_{}".format(sublevel, file_name[4:7])
            level = CassiniKronosLevel('loc', sublevel)
        elif file_name.endswith('.pdf'):
            if 'SVb' in file_name:
                sublevel = 'SVb'
            elif 'LTb' in file_name:
                sublevel = 'LTb'
            elif 'SVe' in file_name:
                sublevel = 'SVe'
            else:
                sublevel = 'raw'
            level = CassiniKronosLevel('pdf', sublevel)
        elif file_name.startswith('SED'):
            level = CassiniKronosLevel('sed')
        else:
            raise KronosError('Unknown level')

        return level

    def extract_interval_from_file_name(self):

        if self.level.name in ['k', 'n1', 'n2', 'n3g']:
            start_time = datetime.datetime.strptime(self.get_file_name()[1:], '%Y%j.%H')
            end_time = start_time + datetime.timedelta(hours=1)
        elif self.level.name in ['n3b', 'n3c', 'n3d', 'n3e']:
            start_time = datetime.datetime.strptime(self.get_file_name()[7:], '%Y%j.%H')
            end_time = start_time + datetime.timedelta(hours=1)
        elif self.level.name in ['skr', 'pdf', 'lis', 'ephem']:
            start_time = datetime.datetime.strptime(self.get_file_name()[0:7], '%Y%j')
            end_time = start_time + datetime.timedelta(days=1)
        elif self.level.name in ['bg']:
            start_time = datetime.datetime.strptime(self.get_file_name()[3:11], '%Y_%j')
            if self.get_file_name()[8:11] == '271':
                end_time = datetime.datetime.strptime("{}1231".format(self.get_file_name()[3:7]), '%Y%m%d') + \
                           datetime.timedelta(days=1)
        elif self.level.name == 'index':
            if self.level.sublevel == '2A':
                start_time = datetime.datetime.strptime(self.get_file_name()[6:], '%Y%j.%H')
                end_time = start_time + datetime.timedelta(hours=1)
            else:
                start_time = datetime.datetime.strptime(self.get_file_name()[9:], '%Y%j.%H')
                end_time = start_time + datetime.timedelta(hours=1)
        elif self.level.name == 'loc':
            index_ydh = len(self.level.sublevel)+5
            if self.level.sublevel.startswith('2A'):
                index_ydh -= 3
            start_time = datetime.datetime.strptime(self.get_file_name()[index_ydh:], '%Y%j.%H')
            end_time = start_time + datetime.timedelta(hours=1)
        else:
            raise KronosError('Unknown level')

        return start_time, end_time

    def read_data_binary(self):

        data = list()
        with open(self.file, 'rb') as fh:
            file_size = self.get_file_size()
            rec_size = self.level.record_def['length']
            if file_size % rec_size != 0:
                raise KronosError("Wrong record size")
            nb_rec = file_size//rec_size
            raw_data = fh.read(file_size)
            for ii in range(nb_rec):
                data.append(CassiniKronosRecord(raw_data[ii*rec_size:(ii+1)*rec_size], self.level))

        return data

    def period(self):
        dir_list = all_periods
        for item in dir_list:
            val = dir_list[item]
            if val['start_time'] <= self.end_time and val['end_time'] >= self.start_time:
                return item


class CassiniKronosRecord:

    def __init__(self, raw_data, level):
        self.level = level
        self.data = self.read_binary(raw_data)

    def read_binary(self, raw_data):
        if self.level.file_format == 'bin-fixed-record-length':
            return dict(zip(self.level.record_def['fields'], struct.unpack(self.level.record_def['dtype'], raw_data)))
        else:
            raise KronosError("Not yet implemented")

    def __getitem__(self, item):
        if item in self.level.record_def['fields']:
            return self.data[item]
        else:
            raise KronosError("Field {} doesn't exist in this record ({})".format(item, self.level.name))


class CassiniKronosSweep:

    def __init__(self, data):
        data.load_extra_level('lis')
        self.mode = CassiniKronosMode(raw_mode)


class CassiniKronosMode:

    def __init__(self, raw_mode):
        self.raw_mode = raw_mode



