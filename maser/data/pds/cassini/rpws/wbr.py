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

__ALL__ = ['PDSPPICassiniRPWSWBRFullResDataFromLabel']

from maser.data.pds.cassini.rpws import iso_time_to_datetime
from maser.data.padc.lesia.cassini.rpws import agc_dB, a123
from maser.data.pds.classes import PDSDataFromLabel, PDSDataObject, PDSDataTableObject, \
    PDSError, PDSDataTimeSeriesObject
import numpy
import datetime


def is_bit_set(x, n):
    return x & 2**n != 0


class PDSPPICassiniRPWSWBRDataObject(PDSDataObject):
    """
    This class inherits from PDSDataObject and deals with PDS/PPI/Cassini/RPWS/WBR data specific features.
    """

    def __init__(self, product, parent, obj_label, obj_name, verbose=False, debug=False):

        if debug:
            print("### This is PDSPPICassiniRPWSWBRDataObject.__init__()")

        PDSDataObject.__init__(self, product, parent, obj_label, obj_name, verbose, debug)
        self.data = self.data_from_object_type()

        if self.debug:
            print("PDSPPICassiniRPWSWBRDataObject instance created")

    def data_from_object_type(self):

        if self.debug:
            print("### This is PDSPPICassiniRPWSWBRDataObject.data_from_object_type()")

        if self.obj_type == 'TIME_SERIES':
            return PDSDataTimeSeriesObject(self.product, self, self.label, self.verbose, self.debug)
        elif self.obj_type == 'WBR_ROW_PREFIX_TABLE':
            return PDSPPICassiniRPWSWBRRowPrefixTable(self.product, self, self.label, self.verbose, self.debug)

    def load_data(self):

        if self.debug:
            print("### This is PDSPPICassiniRPWSWBRDataObject.load_data()")

        self.data.load_data()


class PDSPPICassiniRPWSWBRRowPrefixTable(PDSDataTableObject):

    def __init__(self, product, parent, obj_label, verbose=True, debug=False):

        if debug:
            print("### This is PDSPPICassiniRPWSWBRRowPrefixTable.__init__()")

        PDSDataTableObject.__init__(self, product, parent, obj_label, verbose=verbose, debug=debug)
        self.validity = None
        self.status = None
        self.gain = None

    def load_data(self):

        if self.debug:
            print("### This is PDSPPICassiniRPWSWBRRowPrefixTable.__init__()")

        PDSDataTableObject.load_data(self)
        self.validity = self._decode_validity_flag()
        self.status = self._decode_status_flag()
        self.gain = self._decode_gain_byte()

    def _decode_validity_flag(self):

        validity_dict = dict()
        validity_dict[0] = {'NAME': 'MSF', True: "Fields may contain valid data",
                            False: 'Fields do not contain valid data'}
        validity_dict[1] = {'NAME': 'WBR', True: "WBR data", False: 'Not WBR data'}
        validity_dict[2] = {'NAME': 'WFR', True: "WFR data", False: 'Not WFR data'}
        validity_dict[3] = {'NAME': 'VALID_WALSH_DGF', True: "WALSH_DGF contains valid data",
                            False: "WALSH_DGF not in use (contents invalid)"}
        validity_dict[4] = {'NAME': 'VALID_SUB_RTI', True: "SUB_RTI contains valid data",
                            False: "SUB_RTI not in use (contents invalid)"}
        validity_dict[5] = {'NAME': 'VALID_HFR_XLATE', True: "HFR_XLATE contains valid data",
                            False: "HFR_XLATE not in use (contents invalid)"}
        validity_dict[6] = {'NAME': 'VALID_LP_DAC_0', True: "LP_DAC_0 contains valid data",
                            False: "LP_DAC_0 not in use (contents invalid)"}
        validity_dict[7] = {'NAME': 'VALID_LP_DAC_1', True: "LP_DAC_1 contains valid data",
                            False: "LP_DAC_1 not in use (contents invalid)"}

        validity = []
        for item in self['VALIDITY_FLAG']:
            cur_dict = {}
            for i in range(8):
                value = is_bit_set(item, 7-i)
                cur_dict[validity_dict[i]['NAME']] = (value, validity_dict[i][value])
            validity.append(cur_dict)
        return validity

    def _decode_status_flag(self):
        status_dict = dict()
        status_dict[0] = {'NAME': 'AGC_ENABLE', True: "AGC enabled", False: "AGC disabled"}
        status_dict[1] = {'NAME': 'FINE_TIME_QUALITY', True: "SUB_RTI is accurate to approximately 10 milliseconds",
                          False: "SUB_RTI is accurate to approximately 1 millisecond"}
        status_dict[2] = {'NAME': 'TIMEOUT', True: "time series is corrupt and should be discarded",
                          False: "time series is correctly acquired"}
        status_dict[3] = {'NAME': 'SUSPECT', True: "time series is may be corrupt; may be best to discard",
                          False: "time series is correctly acquired"}
        status_dict[4] = {'NAME': 'HFR_H2', True: "HFR/H2 is connected to the WBR HF antenna input",
                          False: "HFR/H2 is not connected to the WBR HF antenna input"}
        status_dict[5] = {'NAME': 'HFR_H1', True: "HFR/H1 is connected to the WBR HF antenna input",
                          False: "HFR/H1 is not connected to the WBR HF antenna input"}
        status_dict[6] = {'NAME': "EU_CURRENT", True: "electric current measurement on EU",
                          False: "electric voltage measurement on EU"}
        status_dict[7] = {'NAME': "EV_CURRENT", True: "electric current measurement on EV",
                          False: "electric voltage measurement on EV"}

        status = []
        for item in self['STATUS_FLAG']:
            cur_dict = {}
            for i in range(8):
                value = is_bit_set(item, 7-i)
                cur_dict[status_dict[i]['NAME']] = (value, status_dict[i][value])
            status.append(cur_dict)
        return status

    def get_frequency_bandwidth(self, unit=None):
        if unit is None:
            unit = 'kHz'
        frequency_band_values = [26, 2500, 10000, 80000]

        frequency_band = []
        for item in self['FREQUENCY_BAND']:
            if unit == 'Hz':
                frequency_band.append(frequency_band_values[item])
            elif unit == 'kHz':
                frequency_band.append(frequency_band_values[item]/1000)
        return frequency_band

    def _decode_gain_byte(self):
        walsh_dgf_values_db = [0, 6, 12, 18]
        analog_gain_values_db = [0, 10, 20, 30, 40, 50, 60, 70]
        gain = []
        for item in self['GAIN']:
            item = int('{:08b}'.format(item)[::-1], 2)
            walsh_dgf_cur_value = walsh_dgf_values_db[(item >> 2) & 3]
            analog_gain_cur_value = analog_gain_values_db[item >> 5]
            gain.append({'WALSH_DGF': walsh_dgf_cur_value,
                         'ANALOG_GAIN': analog_gain_cur_value,
                         'TOTAL_GAIN': walsh_dgf_cur_value+analog_gain_cur_value})
        return gain

    def get_band(self):
        band = []
        for item in self.status:
            if item['HFR_H2']:
                band.append(4)
            elif item['HFR_H1']:
                band.append(3)
            else:
                raise PDSError("Wring HFR band")
        return band

    def get_antenna(self):
        antenna = []
        for item in self['ANTENNA']:
            if item == 0:
                antenna.append(3)
            elif item == 8:
                antenna.append(2)
            elif item <= 3:
                antenna.append(item - 1)
            else:
                PDSError("Magnetic and LP cases not yet implemented")
        return antenna

    def get_agc_gain(self):
        gain = []
        agc = self['AGC']
        band = self.get_band()
        ant = self.get_antenna()

        for cur_agc, cur_band, cur_ant in zip(agc, band, ant):
            a1, a2, a3 = a123(0, cur_band, cur_ant//3)
            gain.append(agc_dB(cur_agc, a1, a2, a3))

        return gain

    def get_central_frequency(self):

        frequency = []

        for status, hf_step in zip(self.status, self['HFR_XLATE']):
            if status['HFR_H1'][0]:
                frequency.append(hf_step * 25)
            elif status['HFR_H2'][0]:
                frequency.append(hf_step * 50 + 4025)

        return frequency


class PDSPPICassiniRPWSWBRFullResDataFromLabel(PDSDataFromLabel):

    def __init__(self, file, label_dict=None, fmt_label_dict=None, load_data=True, verbose=False, debug=False):

        if debug:
            print("### This is PDSPPICassiniRPWSWBRFullResDataFromLabel.__init__()")

        PDSDataFromLabel.__init__(self, file, label_dict, fmt_label_dict, load_data,
                                  PDSPPICassiniRPWSWBRDataObject, verbose, debug)
        self._set_start_time()
        self._set_end_time()

    def _set_start_time(self):
        self.start_time = iso_time_to_datetime(self.label['START_TIME'])

    def _set_end_time(self):
        self.end_time = iso_time_to_datetime(self.label['STOP_TIME'])

    def get_start_sample_datetime(self):
        date0 = datetime.datetime(1958, 1, 1)
        date_sample = []
        for day, millisecond in zip(self.object['WBR_ROW_PREFIX_TABLE'].data['SCET_DAY'],
                                    self.object['WBR_ROW_PREFIX_TABLE'].data['SCET_MILLISECOND']):
            date_sample.append(date0 + datetime.timedelta(days=int(day))
                               + datetime.timedelta(milliseconds=int(millisecond)))
        return date_sample

    def get_sample_time_axis(self):
        waveform_length = int(self.label['TIME_SERIES']['COLUMN'][0]['ITEMS'])
        time_sampling_step = float(self.label['TIME_SERIES']['SAMPLING_PARAMETER_INTERVAL'])
        return numpy.arange(waveform_length) * time_sampling_step

    def get_central_frequency(self):
        return self.object['WBR_ROW_PREFIX_TABLE'].data.get_central_frequency()

