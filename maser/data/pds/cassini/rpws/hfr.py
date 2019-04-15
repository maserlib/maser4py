#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to work with PDS-PPI/Cassini/RPWS data
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2017, LESIA-PADC, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi", "Laurent Lamy"]
__license__ = "GPLv3"
__version__ = "1.0b0"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Development"
__date__ = "27-FEB-2017"
__project__ = "MASER/PDS PDS/Cassini/RPWS"

__ALL__ = ['PDSPPICassiniRPWSHFRLowRateFullDataFromLabel']

from . import scet_day_millisecond_to_datetime, iso_time_to_datetime
from maser.data.pds.classes import PDSDataFromLabel, PDSDataObject, PDSDataTableObject
from maser.data.data import MaserDataSweep
import dateutil.parser


class PDSPPICassiniRPWSHFRDataObject(PDSDataObject):
    """
    This class inherits from PDSDataObject and deals with PDS/PPI/Cassini/RPWS/HFR data specific features.
    """

    def __init__(self, product, parent, obj_label, obj_name, verbose=False, debug=False):

        if debug:
            print("### This is PDSPPICassiniRPWSHFRDataObject.__init__()")

        PDSDataObject.__init__(self, product, parent, obj_label, obj_name, verbose, debug)
        self.data = self.data_from_object_type()

        if self.debug:
            print("PDSPPICassiniRPWSHFRDataObject instance created")

    def data_from_object_type(self):

        if self.debug:
            print("### This is PDSPPICassiniRPWSHFRDataObject.data_from_object_type()")

        if self.obj_type == 'FREQUENCY_TABLE':
            return PDSDataTableObject(self.product, self, self.label, self.verbose, self.debug)
        elif self.obj_type == 'LRFULL_TABLE':
            return PDSDataTableObject(self.product, self, self.label, self.verbose, self.debug)
        elif self.obj_type == 'TIME_TABLE':
            return PDSDataTableObject(self.product, self, self.label, self.verbose, self.debug)
        elif self.obj_type == 'SPECTRAL_DENSITY_TABLE':
            return PDSDataTableObject(self.product, self, self.label, self.verbose, self.debug)


class PDSPPICassiniRPWSHFRLowRateFullSweep(MaserDataSweep):

    def __init__(self, parent, index, verbose=False, debug=False):

        if debug:
            print("### This is PDSPPICassiniRPWSHFRLowRateFullSweep.__init__()")

        MaserDataSweep.__init__(self, parent, index, verbose, debug)
        self.data = self.parent.object['SPECTRAL_DENSITY_TABLE'].data['SPECTRAL_DENSITY'][index]

    def get_datetime(self):

        if self.debug:
            print("### This is PDSPPICassiniRPWSHFRLowRateFullSweep.get_datetime()")

        return self.parent.get_time_axis()[self.index]


class PDSPPICassiniRPWSHFRLowRateFullDataFromLabel(PDSDataFromLabel):

    def __init__(self, file, label_dict=None, fmt_label_dict=None, load_data=True, verbose=False, debug=False):

        if debug:
            print("### This is PDSPPICassiniRPWSHFRLowRateFullDataFromLabel.__init__()")

        PDSDataFromLabel.__init__(self, file, label_dict, fmt_label_dict, load_data,
                                  PDSPPICassiniRPWSHFRDataObject, verbose, debug)
        self._set_start_time()
        self._set_end_time()

    def _set_start_time(self):
        self.start_time = iso_time_to_datetime(self.label['START_TIME'])

    def _set_end_time(self):
        self.end_time = iso_time_to_datetime(self.label['STOP_TIME'])

    def get_freq_axis(self, unit="kHz"):

        if self.debug:
            print("### This is PDSPPICassiniRPWSHFRLowRateFullDataFromLabel.get_freq_axis()")

        unit_conversion = {'HZ': 1, 'KHZ': 1e3, 'MHZ': 1e6}

        if not self.object['FREQUENCY_TABLE'].data_loaded:
            self.load_data('FREQUENCY_TABLE')

        return self.object['FREQUENCY_TABLE'].data['FREQUENCY'][0]/unit_conversion[unit.upper()]

    def get_time_axis(self):

        if self.debug:
            print("### This is PDSPPICassiniRPWSHFRLowRateFullDataFromLabel.get_time_axis()")

        return scet_day_millisecond_to_datetime(self.object['SPECTRAL_DENSITY_TABLE'].data['SCET_DAY'],
                                                self.object['SPECTRAL_DENSITY_TABLE'].data['SCET_MILLISECOND'])

    def get_single_sweep(self, index):

        if self.debug:
            print("### This is PDSPPICassiniRPWSHFRLowRateFullDataFromLabel.get_single_sweep()")

        return PDSPPICassiniRPWSHFRLowRateFullSweep(self, index)

    def get_epncore_meta(self):

        if self.debug:
            print("### This is PDSPPICassiniRPWSHFRLowRateFullDataFromLabel.get_epncore_meta()")

        md = PDSDataFromLabel.get_epncore_meta(self)

        md['granule_uid'] = ":".join([self.label['DATA_SET_ID'], self.label['PRODUCT_ID']])
        md['granule_gid'] = self.label['STANDARD_DATA_PRODUCT_ID']

        md['instrument_host_name'] = self.label['INSTRUMENT_HOST_NAME']
        md['instrument_name'] = self.label['INSTRUMENT_ID']
        md['receiver_name'] = self.label['SECTION_ID']

        targets = {'name': set(), 'class': set(), 'region': set()}
        if 'JUPITER' in self.label['TARGET_NAME']:
            targets['name'].add('Jupiter')
            targets['class'].add('planet')
            targets['region'].add('magnetosphere')
        if 'SATURN' in self.label['TARGET_NAME']:
            targets['name'].add('Saturn')
            targets['class'].add('planet')
            targets['region'].add('magnetosphere')
        if 'EARTH' in self.label['TARGET_NAME']:
            targets['name'].add('Earth')
            targets['class'].add('planet')
            targets['region'].add('magnetosphere')
        md['target_name'] = '#'.join(targets['name'])
        md['target_class'] = '#'.join(targets['class'])
        md['target_region'] = '#'.join(targets['region'])

        md['dataproduct_type'] = 'ds'

        md['spectral_range_min'] = self.get_freq_axis(unit='Hz')[0]
        md['spectral_range_max'] = self.get_freq_axis(unit='Hz')[-1]

        md['creation_date'] = dateutil.parser.parse(self.label['PRODUCT_CREATION_TIME'], ignoretz=True)

        return md