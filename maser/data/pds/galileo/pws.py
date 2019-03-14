#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to work with PDS/PPI/Voyager/PRA Data
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2017, LESIA-PADC, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi"]
__license__ = "GPLv3"
__version__ = "1.0b2"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Production"
__date__ = "27-FEB-2018"
__project__ = "MASER/PADC PDS/PPI/Galileo/PWS"

import datetime
import numpy
from maser.data import MaserDataSweep
from maser.data.pds.classes import PDSDataFromLabel, PDSDataObject, PDSDataTableObject
import astropy.units as u

import logging
_module_logger = logging.getLogger('maser.data.pds.ppi.galileo.pws')


class PDSPPIGalileoPWSREDRHighResSweep(MaserDataSweep):

    def __init__(self, parent, index, verbose=False, debug=False):

        self.logger = logging.getLogger('maser.data.pds.ppi.galileo.pws.PDSPPIGalileoPWSREDRHighResSweep')
        if debug:
            self.logger.setLevel(logging.DEBUG)
        self.logger.debug('### This is PDSPPIGalileoPWSREDRHighResSweep.__init__()')

        MaserDataSweep.__init__(self, parent, index, verbose, debug)

        cur_row, cur_swp = self.parent._split_index(index)
        self.raw_sweep = self.parent.object['TABLE'].data['SWEEP{}'.format(cur_swp+1)][cur_row]
        self.status = self.raw_sweep[0]
        polar_indices = self._get_polar_indices()
        self.data = {}
        self.freq = {}
        for item in ['R', 'L']:
            self.data[item] = self.raw_sweep[1:][polar_indices[item]]
            self.freq[item] = self.parent.frequency[polar_indices[item]]
        self.freq['avg'] = (self.freq['R']+self.freq['L'])/2
        self.attenuator = self._get_attenuator_value()
        self.type = self._get_sweep_type()

        self.logger.debug("PDSPPIGalileoPWSREDRHighResSweep instance created")

    def get_datetime(self):
        self.logger.debug("### This is PDSPPIGalileoPWSREDRHighResSweep.get_datetime()")

        return self.parent.get_single_datetime(self.index)

    def _get_sweep_type(self):
        self.logger.debug("### This is PDSPPIGalileoPWSREDRHighResSweep._get_sweep_type()")

        if (self.status & 1536) // 512 in [0, 3]:
            return 'R'
        else:
            return 'L'

    def _get_polar_indices(self):
        self.logger.debug("### This is PDSPPIGalileoPWSREDRHighResSweep._get_polar_indices()")

        even_idx = numpy.linspace(0, 68, 35, dtype=numpy.int8)
        odd_idx = numpy.linspace(1, 69, 35, dtype=numpy.int8)
        if self._get_sweep_type() == 'R':
            return {'R': even_idx, 'L': odd_idx}
        else:
            return {'L': even_idx, 'R': odd_idx}

    def _get_attenuator_value(self):
        self.logger.debug("### This is PDSPPIGalileoPWSREDRHighResSweep._get_attenuator_value()")

        if self.status & 1:
            return 15
        elif (self.status//2) & 1:
            return 30
        elif (self.status//4) & 1:
            return 45
        else:
            return 0


class PDSPPIGalileoPWSDataObject(PDSDataObject):

    def __init__(self, product, parent, obj_label, obj_name, verbose=False, debug=False):

        self.logger = logging.getLogger('maser.data.pds.ppi.galileo.pws.PDSPPIGalileoPWSDataObject')
        if debug:
            self.logger.setLevel(logging.DEBUG)
        self.logger.debug('### This is PDSPPIGalileoPWSDataObject.__init__()')

        PDSDataObject.__init__(self, product, parent, obj_label, obj_name, verbose, debug)

        self.data = self.data_from_object_type()

        self.logger.debug("PDSPPIGalileoPWSDataObject instance created")

    def data_from_object_type(self):
        self.logger.debug("### This is PDSPPIGalileoPWSDataObject.data_from_object_type()")

        if self.obj_type == 'TABLE':
            return PDSDataTableObject(self.product, self, self.label, self.verbose, self.debug)


class PDSPPIGalileoPWSDataFromLabel(PDSDataFromLabel):

    def __init__(self, file, label_dict=None, load_data=True, verbose=False, debug=False):

        self.logger = logging.getLogger('maser.data.pds.ppi.galileo.pws.PDSPPIGalileoPWSDataFromLabel')
        if debug:
            self.logger.setLevel(logging.DEBUG)
        self.logger.debug('### This is PDSPPIGalileoPWSDataFromLabel.__init__()')

        PDSDataFromLabel.__init__(self, file, label_dict, load_data, PDSPPIGalileoPWSDataObject, verbose, debug)
        self.frequency = self._get_freq_axis()
        if load_data:
            self.time = self._get_time_axis()
        self._set_start_time()
        self._set_end_time()

    def _set_start_time(self):
        self.logger.debug("### This is PDSPPIGalileoPWSDataFromLabel._set_start_time()")

        if self.label['START_TIME'] == "N/A":
            self.start_time = self.get_first_sweep().get_datetime()
        else:
            PDSDataFromLabel._set_start_time(self)

    def _set_end_time(self):
        self.logger.debug("### This is PDSPPIGalileoPWSDataFromLabel._set_end_time()")

        if self.label['STOP_TIME'] == "N/A":
            self.end_time = self.get_last_sweep().get_datetime()
        else:
            PDSDataFromLabel._set_end_time(self)

    def _get_time_axis(self):
        pass

    def _get_freq_axis(self):
        pass

    def get_freq_axis(self, unit):
        pass

    def get_epncore_meta(self):
        meta = PDSDataFromLabel.get_epncore_meta(self)
        if 'TABLE' in self.objects:
            dt = (float(self.label['TABLE']['SAMPLING_PARAMETER_INTERVAL']) *
                  u.Unit(self.label['TABLE']['SAMPLING_PARAMETER_UNIT'].lower())).to(u.second)
            meta['time_sampling_step'] = dt.value

        return meta


class PDSPPIGalileoPWSREDRHighResDataFromLabel(PDSPPIGalileoPWSDataFromLabel):

    def __init__(self, file, label_dict=None, load_data=True, verbose=False, debug=False):

        self.logger = logging.getLogger('maser.data.pds.ppi.galileo.pws.PDSPPIGalileoPWSREDRHighResDataFromLabel')
        if debug:
            self.logger.setLevel(logging.DEBUG)
        self.logger.debug('### This is PDSPPIGalileoPWSREDRHighResDataFromLabel.__init__()')

        PDSPPIGalileoPWSDataFromLabel.__init__(self, file, label_dict, load_data, verbose, debug)
        self.nsweep = int(self.label['TABLE']['ROWS']) * 8

    def _split_index(self, index):
        self.logger.debug("### This is PDSPPIGalileoPWSREDRHighResDataFromLabel._split_index()")

        if index < 0:
            index += self.object['TABLE'].data.n_rows * 8
        return index // 8, index % 8

    def get_single_datetime(self, index):
        self.logger.debug("### This is PDSPPIGalileoPWSREDRHighResDataFromLabel.get_single_datetime()")

        return self._get_time_axis()[index]

    def _get_freq_axis(self):
        self.logger.debug("### This is PDSPPIGalileoPWSREDRHighResDataFromLabel._get_freq_axis()")

        return numpy.arange(1326, -18, -19.2) * u.Unit('kHz')

    def get_freq_axis(self, unit="kHz"):
        self.logger.debug("### This is PDSPPIGalileoPWSREDRHighResDataFromLabel.get_freq_axis()")

        return self.frequency.to(u.Unit(unit)).value

    def get_single_sweep(self, index=0, **kwargs):
        self.logger.debug("### This is PDSPPIGalileoPWSREDRHighResDataFromLabel.get_single_sweep()")

        return PDSPPIGalileoPWSREDRHighResSweep(self, index)

    def _get_time_axis(self):
        self.logger.debug("### This is PDSPPIGalileoPWSREDRHighResDataFromLabel._get_time_axis()")

        if not self.object['TABLE'].data_loaded:
            self.load_data('TABLE')

        times = []
        for item_date, item_second in zip(self.object['TABLE'].data['DATE'], self.object['TABLE'].data['SECOND']):
            yy = (item_date // 10000) + 1900
            if yy < 70:
                yy += 100
            mm = (item_date % 10000) // 100
            dd = item_date % 100
            sec = item_second + 3.9
            for ii in range(8):
                times.append(datetime.datetime(yy,mm, dd, 0, 0, 0) + datetime.timedelta(seconds=sec + 6 * ii))

        return numpy.array(times)

    def get_time_axis(self):
        self.logger.debug("### This is PDSPPIGalileoPWSREDRHighResDataFromLabel.get_time_axis()")

        return self.time