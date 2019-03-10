#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to work with PSA/MEx/MARSIS/AIS Data
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2019, LESIA-PADC, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Production"
__date__ = "08-MAR-2018"
__project__ = "MASER/PADC PSA/MEx/MARSIS/AIS"

from pathlib import Path
import numpy
from maser.data import MaserDataSweep
from maser.data.pds.classes import PDSDataFromLabel, PDSDataObject, PDSDataTableObject
from .const import MEX_MARSIS_AIS_FREQUENCY_TABLES
import astropy.units as u
import astropy.time as t

import logging
_module_logger = logging.getLogger('maser.data.psa.mex.marsis.ais')

default_root_data_path = Path("/Users/baptiste/Projets/MarsExpress/MARSIS/PSA")


class PSAMExMarsisAISSweep(MaserDataSweep):

    def __init__(self, parent, index, verbose=False, debug=False):

        self.logger = logging.getLogger('maser.data.psa.mex.marsis.ais.PSAMExMarsisAISSweep')
        if debug:
            self.logger.setLevel(logging.DEBUG)
        self.logger.debug('### This is PSAMExMarsisAISSweep.__init__()')

        MaserDataSweep.__init__(self, parent, index, verbose, debug)

        self.raw_sweep = self.parent.object['AIS_TABLE'].data[index]
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

        self.logger.debug("PSAMExMarsisAISSweep instance created")

    def get_datetime(self):
        self.logger.debug("### This is PSAMExMarsisAISSweep.get_datetime()")

        return self.parent.get_single_datetime(self.index)

    def _get_sweep_type(self):
        self.logger.debug("### This is PSAMExMarsisAISSweep._get_sweep_type()")

        if (self.status & 1536) // 512 in [0, 3]:
            return 'R'
        else:
            return 'L'

    def _get_polar_indices(self):
        self.logger.debug("### This is PSAMExMarsisAISSweep._get_polar_indices()")

        even_idx = numpy.linspace(0, 68, 35, dtype=numpy.int8)
        odd_idx = numpy.linspace(1, 69, 35, dtype=numpy.int8)
        if self._get_sweep_type() == 'R':
            return {'R': even_idx, 'L': odd_idx}
        else:
            return {'L': even_idx, 'R': odd_idx}

    def _get_attenuator_value(self):
        self.logger.debug("### This is PSAMExMarsisAISSweep._get_attenuator_value()")

        if self.status & 1:
            return 15
        elif (self.status//2) & 1:
            return 30
        elif (self.status//4) & 1:
            return 45
        else:
            return 0


class PSAMExMarsisAISDataObject(PDSDataObject):

    def __init__(self, product, parent, obj_label, obj_name, verbose=False, debug=False):

        self.logger = logging.getLogger('maser.data.psa.mex.marsis.ais.PSAMExMarsisAISDataObject')
        if debug:
            self.logger.setLevel(logging.DEBUG)
        self.logger.debug('### This is PSAMExMarsisAISDataObject.__init__()')

        PDSDataObject.__init__(self, product, parent, obj_label, obj_name, verbose, debug)

        self.data = self.data_from_object_type()

        self.logger.debug("PSAMExMarsisAISDataObject instance created")

    def data_from_object_type(self):
        self.logger.debug("### This is PSAMExMarsisAISDataObject.data_from_object_type()")

        if self.obj_type == 'AIS_TABLE':
            return PDSDataTableObject(self.product, self, self.label, self.verbose, self.debug)


class PSAMExMarsisAISDataFromLabel(PDSDataFromLabel):

    def __init__(self, file, label_dict=None, fmt_label_dict=None, load_data=True, verbose=False, debug=False):

        self.logger = logging.getLogger('maser.data.psa.mex.marsis.ais.PSAMExMarsisAISDataFromLabel')
        if debug:
            self.logger.setLevel(logging.DEBUG)
        self.logger.debug('### This is PSAMExMarsisAISDataFromLabel.__init__()')

        PDSDataFromLabel.__init__(self, file, label_dict, fmt_label_dict, load_data,
                                  PSAMExMarsisAISDataObject, verbose, debug)
        self.frequency = self._get_freq_axis()
        if load_data:
            self.time = self._get_time_axis()
        self._set_start_time()
        self._set_end_time()

    def _set_start_time(self):
        self.start_time = t.Time(self.label['START_TIME'])

    def _set_end_time(self):
        self.start_time = t.Time(self.label['STOP_TIME'])

    def _get_time_axis(self):
        self.logger.debug("### This is PSAMExMarsisAISDataFromLabel._get_time_axis()")

        if not self.object['AIS_TABLE'].data_loaded:
            self.load_data('AIS_TABLE')

        #times = []
        #for item_date in self.object['AIS_TABLE'].data['SCET_STRING']:
        #        times.append(dateutil.parser.parse(item_date))

        #return numpy.array(times)

    def get_time_axis(self):
        self.logger.debug("### This is PSAMExMarsisAISDataFromLabel.get_time_axis()")

        if self.time is None:
            self.time = self._get_time_axis()

        return self.time

    def _get_freq_axis(self):
        self.logger.debug("### This is PSAMExMarsisAISDataFromLabel._get_freq_axis()")

        return numpy.array(MEX_MARSIS_AIS_FREQUENCY_TABLES[1]) * u.Unit('kHz')
