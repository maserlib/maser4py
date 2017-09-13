#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to work with PDS/PPI/Voyager/PRA Data
@author: B.Cecconi(LESIA)
"""

import datetime
import os
from maser.data.data import *

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2017, LESIA-PADC, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi"]
__license__ = "GPLv3"
__version__ = "1.0b0"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Production"
__date__ = "11-SEP-2017"
__project__ = "MASER/PADC"

__all__ = ["PDSPPIVoyagerPRAJupiterData"]

default_root_data_path = "/Users/baptiste/Volumes/kronos-dio/voyager/data/pra/PDS_data/"


class PDSPPIVoyagerPRAJupiterData(MaserDataFromInterval):

    def __init__(self, start_time, end_time, sc_id=1, root_data_path=default_root_data_path,
                 verbose=False, debug=False):
        MaserDataFromInterval.__init__(self, start_time, end_time, verbose=verbose, debug=debug)
        if sc_id in [1, 2]:
            self.mission_name = "VG{}".format(sc_id)
            self.dataset_name = '{}-J-PRA-3-RDR-LOWBAND-6SEC-V1.0'.format(self.mission_name)
        else:
            raise MaserError("Wrong input for 'SC_ID' argument. Must be 1 or 2.")

        self.data_path = root_data_path + 'VG{}_JUPITER'.format(sc_id)
        self.data = list()
        self.files = list()

        for item in self.get_file_list():
            if item['start_time'] <= self.end_time and item['end_time'] >= self.start_time:
                start_index = 0
                end_index = os.path.getsize(item['file_path'])//2286
                frame_times = self.get_frame_times(item['file_path'])
                for i, val in enumerate(frame_times):
                    if val <= self.end_time:
                        end_index = i
                for i, val in enumerate(frame_times):
                    if val >= self.start_time:
                        start_index = i
                        break

                self.data.extend(self.load_data_frames(item['file_path'], start_index, end_index))

    def get_file_list(self):
        if self.mission_name == 'VG1':
            return [{'file_path': "{}/PRA_I/PRA_I.TAB". format(self.data_path),
                     'start_time': datetime.datetime(1979, 1, 6, 0, 0, 0),
                     'end_time': datetime.datetime(1979, 1, 30, 23, 59, 59)},
                    {'file_path': "{}/PRA_II/PRA_II.TAB".format(self.data_path),
                     'start_time': datetime.datetime(1979, 1, 31, 0, 0, 0),
                     'end_time': datetime.datetime(1979, 2, 25, 23, 59, 59)},
                    {'file_path': "{}/PRA_III/PRA_III.TAB".format(self.data_path),
                     'start_time': datetime.datetime(1979, 2, 26, 0, 0, 0),
                     'end_time': datetime.datetime(1979, 3, 22, 23, 59, 59)},
                    {'file_path': "{}/PRA_IV/PRA_IV.TAB".format(self.data_path),
                     'start_time': datetime.datetime(1979, 3, 23, 0, 0, 34),
                     'end_time': datetime.datetime(1979, 4, 13, 23, 59, 59)}]
        elif self.mission_name == "VG2":
            return [{'file_path': "{}/PRA_I/PRA_I.TAB".format(self.data_path),
                     'start_time': datetime.datetime(1979, 4, 25, 0, 0, 0),
                     'end_time': datetime.datetime(1979, 5, 28, 23, 59, 59)},
                    {'file_path': "{}/PRA_II/PRA_II.TAB".format(self.data_path),
                     'start_time': datetime.datetime(1979, 5, 29, 0, 0, 0),
                     'end_time': datetime.datetime(1979, 6, 23, 23, 59, 59)},
                    {'file_path': "{}/PRA_III/PRA_III.TAB".format(self.data_path),
                     'start_time': datetime.datetime(1979, 6, 24, 0, 0, 0),
                     'end_time': datetime.datetime(1979, 7, 12, 23, 59, 49)},
                    {'file_path': "{}/PRA_IV/PRA_IV.TAB".format(self.data_path),
                     'start_time': datetime.datetime(1979, 7, 13, 0, 0, 0),
                     'end_time': datetime.datetime(1979, 8, 4, 23, 59, 59)}]
        else:
            raise MaserError("Error: Wrong Mission Name.")

    @staticmethod
    def get_freq_list(polar=None, startpolar=None):
        f = [1326 - i*19.2 for i in range(70)]
        if polar is None:
            return f
        if polar == startpolar:
            return [f[i * 2] for i in range(35)]
        if polar != startpolar:
            return [f[i * 2 + 1] for i in range(35)]

    @staticmethod
    def get_offset_times():
        return [datetime.timedelta(milliseconds=3900+j*30) for j in range(70)]

    @staticmethod
    def load_data_frames(file, start_index, stop_index):
        frame = list()
        attenuator_dict = {0: 0, 1: 15, 2: 30, 4: 45}
        startpolar_dict = {0: 'R', 1: 'L', 2: 'L', 3: 'R'}

        with open(file, 'r') as f:
            f.seek(start_index*2286)
            for k in range(stop_index-start_index):
                line = f.read(2285)
                start_time = datetime.datetime(1900 + int(line[0:2]), int(line[2:4]), int(line[4:6])) \
                             + datetime.timedelta(seconds=int(line[6:12]))
                for i in range(8):
                    sweep = dict()
                    data_offset = 12 + 284 * i
                    raw_word = int(line[data_offset:data_offset + 4])
                    attenuator_index = raw_word & 7
                    startpolar_index = (raw_word & 1536)//512
                    if raw_word != 0 and attenuator_index in attenuator_dict.keys():
                        sweep['datetime'] = start_time + datetime.timedelta(seconds=i*6)
                        sweep['status'] = dict()
                        sweep['status']['raw_word'] = raw_word
                        sweep['status']['attenuator'] = attenuator_dict[attenuator_index]
                        sweep['status']['startpolar'] = startpolar_dict[startpolar_index]
                        sweep['data'] = [int(line[data_offset+(j+1)*4:data_offset+(j+2)*4]) for j in range(70)]
                        frame.append(sweep)
        return frame

    @staticmethod
    def get_frame_times(file):
        nb_rec = os.path.getsize(file)//2286
        frame_times = list()
        with open(file, 'r') as f:
            for i in range(nb_rec):
                f.seek(i*2286)
                block = f.read(12)
                frame_times.append(datetime.datetime(1900 + int(block[0:2]), int(block[2:4]), int(block[4:6])) \
                                   + datetime.timedelta(seconds=int(block[6:12])))
        return frame_times

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return [self.data[i][item] for i in range(len(self))]

    def get_polar_data(self, selected_polar, db=True):
        result = list()
        f = self.get_freq_list()
        if selected_polar in ['R', 'L']:
            for d, s in zip(self['data'], self['status']):
                sweep = dict()
                sweep['polar'] = s['startpolar']
                if db:
                    d = [d[i]/100 - s['attenuator'] for i in range(70)]
                if selected_polar == s['startpolar']:
                    sweep['data'] = [d[i*2] for i in range(35)]
                else:
                    sweep['data'] = [d[i*2+1] for i in range(35)]
                result.append(sweep)

        return result

