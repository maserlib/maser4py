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
from maser.data.pds.classes import PDSDataFromLabel, PDSDataObject, PDSDataATableObject
import astropy.time as t
from . import TimeYearDoyISO

import logging
_module_logger = logging.getLogger('maser.data.psa.mex.marsis.ais')

default_root_data_path = Path("/Users/baptiste/Projets/MarsExpress/MARSIS/PSA")


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
            return PDSDataATableObject(self.product, self, self.label, self.verbose, self.debug)


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

        return t.Time(self.object['AIS_TABLE'].data.table['SCET_STRING'])

    def get_time_axis(self):
        self.logger.debug("### This is PSAMExMarsisAISDataFromLabel.get_time_axis()")

        if self.time is None:
            self.time = self._get_time_axis()

        return self.time

    def _get_freq_axis(self):
        self.logger.debug("### This is PSAMExMarsisAISDataFromLabel._get_freq_axis()")

        return self.object['AIS_TABLE'].data.table['FREQUENCY']
