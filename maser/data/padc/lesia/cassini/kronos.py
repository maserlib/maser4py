#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to read a Cassini/Kronos data files from LESIA database (http://lesia.obspm.fr/kronos).
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__date__ = "07-NOV-2018"
__version__ = "0.02"

__all__ = ["CassiniKronosData", "CassiniKronosLevel", "CassiniKronosFile",
           "CassiniKronosRecords", "CassiniKronosSweeps",
           "load_data_from_file", "load_data_from_interval", "ydh_to_datetime", "t97_to_datetime"]

import os
import struct
from maser.data.data import MaserError
from maser.data.data import MaserDataFromFile
from maser.data.data import MaserDataFromInterval
import datetime
import numpy
import hashlib
import collections.abc

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
            cur_period = '{:04d}_{:03d}_{:03d}'.format(yy + 2000, dd_list[dd], dd_list[dd + 1] - 1)
            all_periods[cur_period] = {'start_time': datetime.datetime.strptime(
                "{:04d}{:03d}.00".format(yy + 2000, dd_list[dd]), '%Y%j.%H')}
            if dd == 3:
                all_periods[cur_period]['end_time'] = datetime.datetime.strptime(
                    "{:04d}001.00".format(yy + 2000 + 1), '%Y%j.%H')
            else:
                all_periods[cur_period]['end_time'] = datetime.datetime.strptime(
                    "{:04d}{:03d}.23".format(yy + 2000, dd_list[dd+1]-1), '%Y%j.%H') + datetime.timedelta(hours=1)

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


class CassiniKronosError(MaserError):
    pass


class CassiniKronosLevel(object):

    def __init__(self, level: str, sublevel='', verbose=False, debug=False):
        self.name = level
        self.sublevel = sublevel
        self.implemented = True
        self.record_def = dict()
        self.verbose = verbose
        self.debug = debug
        if self.name == '':
            self.file_format = None
            self.implemented = False
            self.description = "Dummy empty level"
            self.depends = None
        elif self.name == 'k':
            self.file_format = 'bin-compressed'
            self.implemented = False
            self.description = "Cassini/RPWS/HFR Level 0 (Telemetry)"
            self.depends = [None]
        elif self.name == 'n1':
            self.file_format = 'bin-fixed-record-length'
            self.implemented = True
            self.record_def['fields'] = ["ydh", "num", "ti", "fi", "dti", "c", "ant", "agc1", "agc2",
                                         "auto1", "auto2", "cross1", "cross2"]
            self.record_def['dtype'] = "<LLLLhbbbbbbhh"
            self.record_def['np_dtype'] = [('ydh', '<u4'), ('num', '<u4'),
                                           ('ti', '<u4'), ('fi', '<u4'), ('dti', '<i2'), ('c', 'u1'), ('ant', 'u1'),
                                           ('agc1', 'u1'), ('agc2', 'u1'), ('auto1', 'u1'), ('auto2', 'u1'),
                                           ('cross1', '<i2'), ('cross2', '<i2')]
            self.record_def['length'] = struct.calcsize(self.record_def['dtype'])  # = 28
            self.description = "Cassini/RPWS/HFR Level 1 (Receiver units)"
            self.depends = [None]
        elif self.name == 'n2':
            self.file_format = 'bin-fixed-record-length'
            self.record_def['fields'] = ["ydh", "num", "t97", "f", "dt", "df", "autoX", "autoZ",
                                         "crossR", "crossI", "ant"]
            self.record_def['dtype'] = "<LLdfffffffb"
            self.record_def['np_dtype'] = [('ydh', '<u4'), ('num', '<u4'), ('t97', '<f8'), ('f', '<f4'),
                                           ('dt', '<f4'), ('df', '<f4'), ('autoX', '<f4'), ('autoZ', '<f4'),
                                           ('crossR', '<f4'), ('crossI', '<f4'), ('ant', 'i1')]
            self.record_def['length'] = struct.calcsize(self.record_def['dtype'])  # = 45
            self.description = "Cassini/RPWS/HFR Level 2 (Physical units)"
            self.depends = ['n1']
        elif self.name == "n3b":
            self.file_format = 'bin-fixed-record-length'
            self.record_def['fields'] = ["ydh", "num", "s", "q", "u", "v", "th", "ph", "zr", "snx", "snz"]
            self.record_def['dtype'] = "<LLLfffffffffffffff"
            self.record_def['np_dtype'] = [('ydh', '<u4'), ('num', '<u4', 2), ('s', '<f4', 2), ('q', '<f4', 2),
                                           ('u', '<f4', 2), ('v', '<f4', 2), ('th', '<f4'), ('ph', '<f4'),
                                           ('zr', '<f4'), ('snx', '<f4', 2), ('snz', '<f4', 2)]
            self.record_def['length'] = struct.calcsize(self.record_def['dtype'])  # = 72
            self.description = "Cassini/RPWS/HFR Level 3b (Generic 3 antenna GP)"
            self.depends = ['n1', 'n2']
        elif self.name == "n3c":
            self.file_format = 'bin-fixed-record-length'
            self.record_def['fields'] = ["ydh", "num", "s", "q", "u", "v", "th", "ph", "zr", "snx", "snz"]
            self.record_def['dtype'] = "<LLLffffffffffffff"
            self.record_def['np_dtype'] = [('ydh', '<i4'), ('num', '<i4', 2), ('s', '<f4'), ('q', '<f4'),
                                           ('u', '<f4'), ('v', '<f4', 2), ('th', '<f4', 2), ('ph', '<f4', 2),
                                           ('zr', '<f4'), ('snx', '<f4', 2), ('snz', '<f4', 2)]
            self.record_def['length'] = struct.calcsize(self.record_def['dtype'])  # = 68
            self.description = "Cassini/RPWS/HFR Level 3c (Circular polarization 3 antenna GP)"
            self.depends = ['n1', 'n2']
        elif self.name == "n3d":
            self.file_format = 'bin-fixed-record-length'
            self.record_def['fields'] = ["ydh", "num", "s", "q", "u", "v", "th", "ph", "snx", "snz"]
            self.record_def['dtype'] = "<LLffffffff"
            self.record_def['np_dtype'] = [('ydh', '<i4'), ('num', '<i4'), ('s', '<f4'), ('q', '<f4'),
                                           ('u', '<f4'), ('v', '<f4'), ('th', '<f4'), ('ph', '<f4'),
                                           ('snx', '<f4'), ('snz', '<f4')]
            self.record_def['length'] = struct.calcsize(self.record_def['dtype'])
            self.description = "Cassini/RPWS/HFR Level 3d (Known source position 2 antenna GP)"
            self.depends = ['n1', 'n2']
        elif self.name == "n3e":
            self.file_format = 'bin-fixed-record-length'
            self.record_def['fields'] = ["ydh", "num", "s", "q", "u", "v", "th", "ph", "snx", "snz"]
            self.record_def['dtype'] = "<LLffffffff"
            self.record_def['np_dtype'] = [('ydh', '<i4'), ('num', '<i4'), ('s', '<f4'), ('q', '<f4'),
                                           ('u', '<f4'), ('v', '<f4'), ('th', '<f4'), ('ph', '<f4'),
                                           ('snx', '<f4'), ('snz', '<f4')]
            self.record_def['length'] = struct.calcsize(self.record_def['dtype'])
            self.description = "Cassini/RPWS/HFR Level 3e (Circular polarization 2 antenna GP)"
            self.depends = ['n1', 'n2']
        else:
            raise CassiniKronosError("Not yet implemented error")


class CassiniKronosData(MaserDataFromInterval):

    def __init__(self, start_time=None, end_time=None, input_level=CassiniKronosLevel(''),
                 verbose=False, debug=False):
        MaserDataFromInterval.__init__(self, start_time, end_time, input_level.description,
                                       verbose=verbose, debug=debug)
        self.level = input_level
        self.start_time = start_time
        self.end_time = end_time
        self.root_data_dir = os.environ['NAS_RPWS']

        if self.start_time is not None and self.end_time is not None:
            self.periods = self.period_dir_list()
            self.periods.sort()
            self.files = self.make_file_list()
            file_start = [item.start_time for item in self.files]
            self.files = [x for y, x in sorted(zip(file_start, self.files))]

            self.data = dict()
            first_file = True
            for item in self.files:

                cur_data = item.read_data_binary()

                if first_file:
                    self.data[self.level.name] = cur_data.copy()
                else:
                    self.data[self.level.name] = numpy.append(self.data[self.level.name].copy(), cur_data.copy())

                for lev_item in self.level.depends:
                    dep_data = item.other_level(lev_item).read_data_binary()

                    if first_file:
                        self.data[lev_item] = dep_data[cur_data['num']].copy()
                    else:
                        self.data[lev_item] = numpy.append(self.data[lev_item].copy(), dep_data[cur_data['num']].copy())

                first_file = False

            if self.level.name == 'n3b':
                self.flatten_n3b()

    def __str__(self):
        return "<{} object> {} to {} with level {}".\
            format(type(self).__qualname__, self.start_time.isoformat(),
                   self.end_time.isoformat(), self.level.name)

    def __repr__(self):
        print(self)

    @classmethod
    def from_file(cls, input_file, verbose=False, debug=False):
        file = CassiniKronosFile(input_file, verbose=verbose, debug=debug)
        start_time, end_time = file.extract_interval_from_file_name()
        level = file.extract_level_from_file_name()
        return CassiniKronosData(start_time, end_time, level, verbose=verbose, debug=debug)

    @classmethod
    def from_interval(cls, start_time, end_time, input_level, verbose=False, debug=False):
        level = CassiniKronosLevel(input_level)
        return CassiniKronosData(start_time, end_time, level, verbose=verbose, debug=debug)

    @classmethod
    def load_n2_data(cls, start_time, end_time, verbose=False, debug=False):
        return CassiniKronosData.from_interval(start_time, end_time, 'n2', verbose=verbose, debug=debug)

    @classmethod
    def load_n3b_data(cls, start_time, end_time, n2_data=None, verbose=False, debug=False):
        return CassiniKronosData.from_interval(start_time, end_time, 'n3b',
                                               verbose=verbose, debug=debug)

    @classmethod
    def load_n3c_data(cls, start_time, end_time, n2_data=None, verbose=False, debug=False):
        return CassiniKronosData.from_interval(start_time, end_time, 'n3c',
                                               verbose=verbose, debug=debug)

    @classmethod
    def load_n3d_data(cls, start_time, end_time, n2_data=None, verbose=False, debug=False):
        return CassiniKronosData.from_interval(start_time, end_time, 'n3d',
                                               verbose=verbose, debug=debug)

    @classmethod
    def load_n3e_data(cls, start_time, end_time, n2_data=None, verbose=False, debug=False):
        return CassiniKronosData.from_interval(start_time, end_time, 'n3e',
                                               verbose=verbose, debug=debug)

#    def load_extra_level(self, input_level, input_sublevel=''):
#        new_level = CassiniKronosLevel(input_level, input_sublevel)
#        self.dataset_name.append(new_level)
#        self.files.extend(self.make_file_list(new_level))
#        self.data[input_level] = list()
#        for item in self.files:
#            if (item.level.name, item.level.sublevel) == (input_level, input_sublevel):
#                self.data[input_level].extend(item.read_data_binary())

    def period_dir_list(self):
        this_dir_list = list()
        dir_list = all_periods
        for key, val in dir_list.items():
            if (val['start_time'] < self.end_time and val['end_time'] > self.start_time) \
                    or val['start_time'] == self.start_time or val['end_time'] == self.end_time:
                this_dir_list.append(key)
        return this_dir_list

#    def level_path(self, period_dir):
#        return os.path.join(os.path.join(self.root_data_dir, period_dir), all_levels[self.level.name]['path'])

    def make_file_list(self):
        file_list = list()
        for dir_item in self.periods:
            dir_path = os.path.join(os.path.join(self.root_data_dir, dir_item), all_levels[self.level.name]['path'])
            if os.path.exists(dir_path):
                for file_item in os.listdir(dir_path):
                    cur_file = CassiniKronosFile(os.path.join(dir_path, file_item),
                                                 verbose=self.verbose, debug=self.debug)
                    if (cur_file.start_time < self.end_time and cur_file.end_time > self.start_time) \
                            or cur_file.start_time == self.start_time or cur_file.end_time == self.end_time:
                        file_list.append(cur_file)
#            else:
#                print("Warning directory doesn't exist: {}".format(dir_path))

        # file_list.sort(key=dict(zip(file_list, [item.file_name for item in file_list])).get)
        return file_list

    def flatten_n3b(self):

        self.data['n1'] = self.data['n1'].flatten()
        self.data['n2'] = self.data['n2'].flatten()

        flatten_n3b = numpy.empty(len(self.data['n2']),
                                  dtype=[('ydh', '<u4'), ('num', '<u4'),
                                         ('s', '<f4'), ('q', '<f4'), ('u', '<f4'), ('v', '<f4'),
                                         ('th', '<f4'), ('ph', '<f4'),
                                         ('zr', '<f4'), ('snx', '<f4'), ('snz', '<f4')])
        flatten_n3b['ydh'] = numpy.array([self.data['n3b']['ydh'], self.data['n3b']['ydh']]).T.flatten()
        flatten_n3b['num'] = self.data['n3b']['num'].flatten()
        flatten_n3b['s'] = self.data['n3b']['s'].flatten()
        flatten_n3b['q'] = self.data['n3b']['q'].flatten()
        flatten_n3b['u'] = self.data['n3b']['u'].flatten()
        flatten_n3b['v'] = self.data['n3b']['v'].flatten()
        flatten_n3b['th'] = numpy.array([self.data['n3b']['th'], self.data['n3b']['th']]).T.flatten()
        flatten_n3b['ph'] = numpy.array([self.data['n3b']['ph'], self.data['n3b']['ph']]).T.flatten()
        flatten_n3b['zr'] = numpy.array([self.data['n3b']['zr'], self.data['n3b']['zr']]).T.flatten()
        flatten_n3b['snx'] = self.data['n3b']['snx'].flatten()
        flatten_n3b['snz'] = self.data['n3b']['snz'].flatten()

        self.data['n3b'] = flatten_n3b

    def __getitem__(self, item):
        if item in self.level.record_def['fields']:
            return numpy.array([self.data[self.level.name][i][item] for i in range(len(self))])
        elif item == 'datetime':
            return numpy.array([t97_to_datetime(tt) for tt in self['t97']])
        elif self.level.depends is not None:
            for lev_item in self.level.depends:
                if item in CassiniKronosLevel(lev_item).record_def['fields']:
                    return numpy.array([self.data[lev_item][i][item] for i in range(len(self))])
        else:
            raise CassiniKronosError("Field {} doesn't exist".format(item))

    def __len__(self):
        return len(self.data[self.level.name])

    def __add__(self, other):
        # checking class
        if not isinstance(other, CassiniKronosData):
            raise CassiniKronosError("Can't concatenate <CassiniKronosData> with <{}>".format(type(other).__qualname__))
        # checking level
        elif self.dataset_name != other.dataset_name:
            raise CassiniKronosError("Can't concatenate levels {} and {}".format(self.dataset_name, other.dataset_name))
        else:
            self.periods.extend([p for p in other.periods if p not in self.periods])
            self.files.extend([p for p in other.files if p not in self.files])
            if self.start_time > other.end_time:
                # case 1: "other" ends before "self" starts
                self.start_time = other.start_time
                self.data = other.data.extend(self.data)
            elif self.end_time < other.start_time:
                # case 2: "other" starts after "self" ends
                self.end_time = other.end_time
                self.data.extend(other.data)
            elif self.end_time > other.start_time:
                # case 3: "other" starts before "self" ends
                self.end_time = other.end_time
                sd = self.data[-1]
                other_start_index = 0
                for i, od in enumerate(other.data):
                    if od['ydh'] <= sd['ydh'] and od['num'] <= sd['num']:
                        other_start_index = i
                    else:
                        break
                if other_start_index == len(other):
                    # case 3a: "other" is included in "self"
                    pass
                else:
                    # case 3b: "other" ends after "self" ends
                    self.data.extend(other.data[other_start_index+1:])
            elif self.start_time < other.end_time:
                # case 4: "self" starts before "other" ends
                self.start_time = other.start_time
                sd = self.data[-1]
                other_stop_index = 0
                for i, od in enumerate(other.data):
                    if od['ydh'] <= sd['ydh'] and od['num'] <= sd['num']:
                        other_stop_index = i
                    else:
                        break
                if other_stop_index == len(other):
                    # case 4a: "self" is included in "other"
                    self.data = other.data
                else:
                    # case 4b: "self" ends after "other" ends
                    self.data = other.data[0:other_stop_index-1].extend(self.data)

    def sweeps(self):
        return CassiniKronosSweeps(self)

    def records(self):
        return CassiniKronosRecords(self)

    def get_modes(self):
        modes = dict()
        for t, d in self.sweeps():
            hh = hashlib.md5(repr(d['n1']['fi']).encode('utf-8')).hexdigest()
            if hh not in modes.keys():
                modes[hh] = dict()
                modes[hh]['fi'] = d['n1']['fi']
                modes[hh]['dti'] = d['n1']['dti']
                modes[hh]['ant'] = d['n1']['ant']
                if self.level.name != 'n1':
                    modes[hh]['f'] = d['n2']['f']
                    modes[hh]['df'] = d['n2']['df']
                    modes[hh]['dt'] = d['n2']['dt']

        return modes


class CassiniKronosSweeps(collections.abc.Iterator):

    def __init__(self, parent):
        collections.abc.Iterator.__init__(self)
        self.parent = parent
        self.times, self.indices = numpy.unique(self.parent['datetime'], return_inverse=True)
        self.cur_index = 0
        self.max_index = len(self.times)

    def __next__(self):
        if self.cur_index == self.max_index-1:
            raise StopIteration
        else:
            self.cur_index += 1
            data = dict()
            for key in self.parent.data.keys():
                data[key] = self.parent.data[key][self.indices == self.cur_index]
            return self.times[self.cur_index], data

    def __len__(self):
        return self.max_index

    def get_mode_hash(self):
        d = self.parent.data['n1'][self.indices == self.cur_index]
        return hashlib.md5(repr(d['fi']).encode('utf-8')).hexdigest()


class CassiniKronosRecords(collections.abc.Iterator):

    def __init__(self, parent):
        collections.abc.Iterator.__init__(self)
        self.parent = parent
        self.times = self.parent['datetime']
        self.freqs = self.parent['f']
        self.cur_index = 0
        self.max_index = len(self.parent.data[self.parent.level.name])

    def __next__(self):
        if self.cur_index == self.max_index-1:
            raise StopIteration
        else:
            self.cur_index += 1
            data = dict()
            for key in self.parent.data.keys():
                data[key] = self.parent.data[key][self.cur_index]
            return self.times[self.cur_index], self.freqs[self.cur_index], data

    def __len__(self):
        return self.max_index


class CassiniKronosFile(MaserDataFromFile):

    def __init__(self, file, verbose=False, debug=False):
        MaserDataFromFile.__init__(self, file, verbose=verbose, debug=debug)
        self.level = self.extract_level_from_file_name()
        self.start_time, self.end_time = self.extract_interval_from_file_name()

    def __str__(self):
        return "<{} object> {}".format(type(self).__qualname__, self.file)

    def __repr__(self):
        print(str(self))

    def extract_level_from_file_name(self, verbose=False, debug=False):
        file_name = self.get_file_name()
        if file_name.startswith('K'):
            level = CassiniKronosLevel('k', verbose=self.verbose, debug=self.debug)
        elif file_name.startswith('R'):
            level = CassiniKronosLevel('n1', verbose=self.verbose, debug=self.debug)
        elif file_name.startswith('P'):
            level = CassiniKronosLevel('n2', verbose=self.verbose, debug=self.debug)
        elif file_name.startswith('F'):
            level = CassiniKronosLevel('n3g', verbose=self.verbose, debug=self.debug)
        elif file_name.startswith('N'):
            level = CassiniKronosLevel('n3{}'.format(file_name[2]), file_name[4:7],
                                       verbose=self.verbose, debug=self.debug)
        elif file_name.startswith('bg'):
            level = CassiniKronosLevel('bg', verbose=self.verbose, debug=self.debug)
        elif '.v' in file_name:
            level = CassiniKronosLevel('ephem', 'veph', verbose=self.verbose, debug=self.debug)
        elif '.q' in file_name:
            level = CassiniKronosLevel('ephem', 'qeph', verbose=self.verbose, debug=self.debug)
        elif file_name.startswith('INDEX_3A'):
            level = CassiniKronosLevel('index', '3A', verbose=self.verbose, debug=self.debug)
        elif file_name.startswith('INDEX'):
            level = CassiniKronosLevel('index', '2A', verbose=self.verbose, debug=self.debug)
        elif file_name.endswith('.lis'):
            level = CassiniKronosLevel('lis', verbose=self.verbose, debug=self.debug)
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
            level = CassiniKronosLevel('loc', sublevel, verbose=self.verbose, debug=self.debug)
        elif file_name.endswith('.pdf'):
            if 'SVb' in file_name:
                sublevel = 'SVb'
            elif 'LTb' in file_name:
                sublevel = 'LTb'
            elif 'SVe' in file_name:
                sublevel = 'SVe'
            else:
                sublevel = 'raw'
            level = CassiniKronosLevel('pdf', sublevel, verbose=self.verbose, debug=self.debug)
        elif file_name.startswith('SED'):
            level = CassiniKronosLevel('sed', verbose=self.verbose, debug=self.debug)
        else:
            raise CassiniKronosError('Unknown level')

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
            raise CassiniKronosError('Unknown level')

        return start_time, end_time

    def other_level(self, input_level):
        ydh = datetime.datetime.strftime(self.start_time, '%Y%j.%H')
        if input_level == 'n1':
            input_file = "../n1/R{}".format(ydh)
        elif input_level == 'n2':
            input_file = "../n2/P{}".format(ydh)
        else:
            raise CassiniKronosError("Not implemented yet")
        file = os.path.join(self.get_file_path(), input_file)
        return CassiniKronosFile(file, verbose=self.verbose, debug=self.debug)

    def read_data_binary(self):

        file_size = self.get_file_size()
        rec_size = self.level.record_def['length']
        if file_size % rec_size != 0:
            raise CassiniKronosError("Wrong record size")

        if self.verbose:
            print("Loading {} {} records from {}...".format(file_size//rec_size, self.level.name, self.get_file_name()))
        t0 = datetime.datetime.now()

        data = numpy.fromfile(self.file, dtype=self.level.record_def['np_dtype'])

        if self.debug:
            print("*** done: {} seconds elapsed".format((datetime.datetime.now()-t0).total_seconds()))

        return data

    def period(self):
        dir_list = all_periods
        for item in dir_list:
            val = dir_list[item]
            if val['start_time'] <= self.end_time and val['end_time'] >= self.start_time:
                return item

# class CassiniKronosRecord(MaserDataRecord):
#
#    def __init__(self, parent, raw_data):
#        MaserDataRecord.__init__(self, parent, raw_data)
#        self.data = self.read_binary(raw_data)
#        self.verbose = parent.verbose
#        self.debug = parent.debug
#
#    def read_binary(self, raw_data):
#        if self.parent.level.file_format == 'bin-fixed-record-length':
#            return dict(zip(self.parent.level.record_def['fields'],
#                            struct.unpack(self.parent.level.record_def['dtype'], raw_data)))
#        else:
#            raise CassiniKronosError("Not yet implemented")
#
#    def __getitem__(self, item):
#        if item in self.parent.level.record_def['fields']:
#            return self.data[item]
#        else:
#            raise CassiniKronosError("Field {} doesn't exist in this record ({})".format(item, self.parent.level.name))
#
#    def merge(self, extra):
#        if isinstance(extra, CassiniKronosRecord):
#            for ext_k in extra.data.keys():
#                if ext_k in self.data.keys():
#                    if extra.data[ext_k] != self.data[ext_k]:
#                        print("cur[{}] = {}".format(ext_k, self.data[ext_k]))
#                        print("ext[{}] = {}".format(ext_k, extra.data[ext_k]))
#                        raise CassiniKronosError("Inconsistent records while merging")
#                else:
#                    self.data[ext_k] = extra.data[ext_k]

# class CassiniKronosSweep:
#
#    def __init__(self, data):
#        data.load_extra_level('lis')
#        self.mode = CassiniKronosMode(raw_mode)
#
#
# class CassiniKronosMode:
#
#    def __init__(self, raw_mode):
#        self.raw_mode = raw_mode


def load_data_from_file(file, verbose=False, debug=False):
    return CassiniKronosData.from_file(file, verbose=verbose, debug=debug)


def load_data_from_interval(start_time, end_time, input_level, verbose=False, debug=False):
    return CassiniKronosData.from_interval(start_time, end_time, input_level, verbose=verbose, debug=debug)


def ydh_to_datetime(ydh_time):
    return datetime.datetime.strptime(ydh_time, '%Y%j.%H')


def t97_to_datetime(t97_time):
    return datetime.datetime(1997,1,1) + datetime.timedelta(days=t97_time - 1)
