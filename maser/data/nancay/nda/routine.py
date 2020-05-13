#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to work with SRN/NDA/Routine data
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2017, LESIA-PADC-USN, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi", "Andree Coffre", "Laurent Lamy"]
__license__ = "GPLv3"
__version__ = "2.0b1"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Production"
__date__ = "06-SEP-2017"
__project__ = "MASER/SRN/NDA"

_cdf_version = "13"
_dat_version = "01"

__all__ = ["NDARoutineDataRT1", "NDARoutineDataCDF", "NDARoutineSweepRT1", "NDARoutineSweepCDF", "NDARoutineError",
           "load_nda_routine_from_file"]

import struct
import datetime
import os
import sys
# import numpy
from ...data import MaserDataSweep, MaserData
from ..nda import NDAError
from ..nda import NDADataFromFile
#from spacepy import pycdf as cdf
from maser.utils import cdf
import dateutil.parser

# import sunpy.sun
# get_sun_B0([time]) #	Return the B0 angle for the Sun at a specified time, which is the heliographic latitude of the Sun-disk center as seen from Earth.
# get_sun_L0([time]) #	Return the L0 angle for the Sun at a specified time, which is the Carrington longitude of the Sun-disk center as seen from Earth.


def _detect_format(file, debug=False):
    if debug:
        print("This is _detect_format()")

    file_info = dict()
    if file.endswith('.RT1'):
        if debug:
            print(" -> RT1 format detected")
        file_info['format'] = 'RT1'
        file_info['record_size'] = 405
        file_info['data_offset_in_file'] = file_info['record_size']
    elif file.endswith('.cdf'):
        if debug:
            print(" -> CDF format detected")
        file_info['format'] = 'CDF'
    else:
        raise NDARoutineError('NDA/Routine: Unknown file Extension')

    return file_info


def load_nda_routine_from_file(file, debug=False):

    if debug:
        print("This is load_nda_routine_from_file()")

    file_info = _detect_format(file, debug=debug)
    if file_info['format'] == 'RT1':
        o = NDARoutineDataRT1(file, debug=debug)
    elif file_info['format'] == 'CDF':
        o = NDARoutineDataCDF(file, debug=debug)
    else:
        o = None
    return o


class NDARoutineError(NDAError):
    pass


class NDARoutineData(NDADataFromFile):
    """
    Abstract class used by NDARoutineDataRT1 and NDARoutineDataCDF
    """

    def __init__(self, file, debug=False):

        if debug:
            print("This is {}.__init__()".format(__class__.__name__))

        header = {}
        data = []
        name = "SRN/NDA Routine Dataset"
        NDADataFromFile.__init__(self, file, header, data, name, debug=debug)

        self.file_info = {'name': self.file, 'size': self.get_file_size()}
        self.file_info.update(_detect_format(self.file, debug=debug))
        self.format = self.file_info['format']
        self._set_file_handle()
        self._set_file_date()

        self.header = self._header_from_file()

        meta = dict()
        meta['obsty_id'] = 'srn'
        meta['instr_id'] = 'nda'
        meta['recvr_id'] = 'routine'
        meta['freq_len'] = 400
        self.meta = meta

    def _set_file_handle(self):
        if self.debug:
            print("This is {}._set_file_handle()".format(__class__.__name__))
        pass

    def _set_file_date(self):
        if self.debug:
            print("This is {}._set_file_date()".format(__class__.__name__))
        pass

    def _header_from_file(self):
        if self.debug:
            print("This is {}._header_from_file()".format(__class__.__name__))
        pass

    def get_start_date(self):
        if self.debug:
            print("This is {}.get_start_date()".format(__class__.__name__))
        pass

    def get_meridian_datetime(self, from_file=True):
        if self.debug:
            print("This is {}.get_meridian_datetime()".format(__class__.__name__))
        pass

    def get_meridian_time(self):
        if self.debug:
            print("This is {}.get_meridian_time()".format(__class__.__name__))
        return self.get_meridian_datetime().time()

    def get_single_sweep(self, index=0, load_data=True):
        if self.debug:
            print("This is {}.get_single_sweep()".format(__class__.__name__))
        pass

    def get_first_sweep(self, load_data=True):
        if self.debug:
            print("This is {}.get_first_sweep()".format(__class__.__name__))
        return self.get_single_sweep(0, load_data)

    def get_last_sweep(self, load_data=True):
        if self.debug:
            print("This is {}.get_last_sweep()".format(__class__.__name__))
        return self.get_single_sweep(len(self)-1, load_data)

    def get_freq_axis(self):
        if self.debug:
            print("This is {}.get_freq_axis()".format(__class__.__name__))
        pass

    def get_time_axis(self):
        if self.debug:
            print("This is {}.get_time_axis()".format(__class__.__name__))
        pass


class NDARoutineDataRT1(NDARoutineData):

    def __init__(self, file, debug=False):
        if debug:
            print("This is {}.__init__()".format(__class__.__name__))

        NDARoutineData.__init__(self, file, debug=debug)
        self.name = "SRN/NDA Routine RT1 Dataset"
        self.start_time = self.get_first_sweep(load_data=False).get_datetime()
        self.end_time = self.get_last_sweep(load_data=False).get_datetime()
        self._set_meta_from_header()

    def _set_file_handle(self):
        if self.debug:
            print("This is {}._set_file_handle()".format(__class__.__name__))

        self.file_handle = open(self.file, 'rb')

    def _set_file_date(self):
        if self.debug:
            print("This is {}._set_file_date()".format(__class__.__name__))
        filedate = ((os.path.basename(self.file).split('.'))[0])[1:7]
        if int(filedate[0:2]) < 90:
            century_str = '20'
        else:
            century_str = '19'
        self.file_info['filedate'] = "{}{}".format(century_str, filedate)

    def _set_meta_from_header(self):
        """
        Adds header information to self.meta
        """
        if self.debug:
            print("This is {}._set_meta_from_header()".format(__class__.__name__))

        self.meta['freq_min'] = self.header['freq_min']  # MHz
        self.meta['freq_max'] = self.header['freq_max']  # MHz
        self.meta['freq_res'] = self.header['freq_res']  # kHz
        self.meta['freq_step'] = (self.meta['freq_max']-self.meta['freq_min'])/0.4  # kHz

        self.meta['time_min'] = self.start_time
        self.meta['time_max'] = self.end_time
        self.meta['time_step'] = 1  # sec
        self.meta['time_exp'] = 0.875  # msec

        target_dict = {"J": {"target_name": "Jupiter",
                             "target_class": "planet",
                             "target_region": "Magnetosphere",
                             "feature_name": "Aurora#Radio emissions#DAM"},
                       "S": {"target_name": "Sun",
                             "target_class": "star",
                             "target_region": "Heliosphere",
                             "feature_name": "Solar Wind#Radio emissions"},
                       "A": {"target_name": None,
                             "target_class": None,
                             "target_region": None,
                             "feature_name": None}
                       }
        short_target = self.get_file_name()[0]
        self.meta.update(target_dict[short_target])
        if short_target != "A":
            self.meta['recvr_id'] += "_" + target_dict[short_target]["target_name"][0:3].lower()

        self.meta['reference_level'] = self.header['ref_levl']
        self.meta['sweep_duration'] = self.header['swp_time']
        self.meta['power_resolution'] = self.header['powr_res']

    def __len__(self):
        if self.debug:
            print("This is {}.__len__()".format(__class__.__name__))
        return self.get_file_size()//self.file_info['record_size'] - 1

    def get_mime_type(self):
        if self.debug:
            print("This is {}.get_mime_type()".format(__class__.__name__))
        return 'application/x-binary-rt1'

    def get_start_date(self):
        if self.debug:
            print("This is {}.get_start_date()".format(__class__.__name__))
        if int(self.header['start_yr']) < 90:
            year_offset = 2000
        else:
            year_offset = 1900
        return datetime.date(int(self.header['start_yr']) + year_offset,
                             int(self.header['start_mo']), int(self.header['start_dd']))

    def get_meridian_datetime(self, from_file=True):
        if self.debug:
            print("This is {}.get_meridian_datetime()".format(__class__.__name__))
        meridian_dt = None
        if from_file:
            meridian_dt = datetime.datetime.strptime(self.file_info['filedate'], '%Y%m%d') + \
                          datetime.timedelta(hours=int(self.header['merid_hh']), minutes=int(self.header['merid_mm']))

        else:
            NDARoutineError("Ephemeris from IMCCE webservice not implemented yet")

        return meridian_dt

    def _header_from_file(self):
        """ Return file header
        :return:
        """
        if self.debug:
            print("This is {}._header_from_file()".format(__class__.__name__))
        return self._header_from_rt1()

    def _header_from_rt1(self):
        """ Return RT1 file header (format 1, see SRN NDA ROUTINE JUP documentation)
        :return header: (dict) Header data dictionary
        """
        if self.debug:
            print("This is {}._header_from_rt1()".format(__class__.__name__))

        f = self.file_handle
        self.file_info['header_raw'] = f.read(self.file_info['record_size'])
        self._fix_corrupted_header()

        if int(self.file_info['filedate']) < 19901127:
            self.file_info['header_version'] = 1
            header = self._header_from_rt1_format_1()
        elif int(self.file_info['filedate']) < 19940224:
            self.file_info['header_version'] = 2
            header = self._header_from_rt1_format_2()
        elif int(self.file_info['filedate']) < 19990119:
            self.file_info['header_version'] = 3
            header = self._header_from_rt1_format_3()
        elif int(self.file_info['filedate']) < 20001101:
            self.file_info['header_version'] = 4
            header = self._header_from_rt1_format_4()
        elif int(self.file_info['filedate']) < 20090922:
            self.file_info['header_version'] = 5
            header = self._header_from_rt1_format_5()
        else:
            self.file_info['header_version'] = 6
            header = self._header_from_rt1_format_6()

        self._fix_old_version_header()

        if self.debug:
            print('Header version is {}'.format(self.file_info['header_version']))

        return header

    def _header_from_rt1_format_1(self):

        if self.debug:
            print("This is {}._header_from_rt1_format_1()".format(__class__.__name__))

        raw = self.file_info['header_raw']
        header = dict()
        header['freq_min'] = float(raw[1:3])  # MHz
        header['freq_max'] = float(raw[3:5])  # MHz
        header['freq_res'] = float(raw[5:8])  # kHz
        header['ref_levl'] = float(raw[8:11])  # dBm
        header['swp_time'] = float(raw[11:14])  # ms
        header['powr_res'] = float(raw[14:16])  # dB/div
        return header

    def _header_from_rt1_format_2(self):

        if self.debug:
            print("This is {}._header_from_rt1_format_2()".format(__class__.__name__))

        raw = self.file_info['header_raw']
        header = self._header_from_rt1_format_1()
        header['merid_hh'] = int(raw[16:18])  # hour
        header['merid_mm'] = int(raw[18:20])  # minute
        return header

    def _header_from_rt1_format_3(self):

        if self.debug:
            print("This is {}._header_from_rt1_format_3()".format(__class__.__name__))

        raw = self.file_info['header_raw']
        header = self._header_from_rt1_format_1()
        header['swp_time'] = float(raw[13:16])  # ms
        header['powr_res'] = float(raw[16:18])  # dB/div
        header['merid_hh'] = int(raw[18:20])  # hour
        header['merid_mm'] = int(raw[20:22])  # minute
        return header

    def _header_from_rt1_format_4(self):

        if self.debug:
            print("This is {}._header_from_rt1_format_4()".format(__class__.__name__))

        raw = self.file_info['header_raw']
        header = self._header_from_rt1_format_3()
        header['swp_time'] = float(raw[11:16])  # ms
        return header

    def _header_from_rt1_format_5(self):

        if self.debug:
            print("This is {}._header_from_rt1_format_5()".format(__class__.__name__))

        raw = self.file_info['header_raw']
        header = self._header_from_rt1_format_4()
        header['rf0_sele'] = int(raw[22:23])  # RF Filter 0 (selected at start of observations)
        header['rf0_hour'] = int(raw[23:25])  # Start for RF filter 0 (hours)
        header['rf0_minu'] = int(raw[26:28])  # Start for RF filter 0 (minutes)
        header['rf1_sele'] = int(raw[28:29])  # RF Filter 1
        header['rf1_hour'] = int(raw[29:31])  # Start for RF filter 1 (hours)
        header['rf1_minu'] = int(raw[32:34])  # Start for RF filter 1 (minutes)
        header['rf2_sele'] = int(raw[34:35])  # RF Filter 2
        header['rf2_hour'] = int(raw[35:37])  # Start for RF filter 2 (hours)
        header['rf2_minu'] = int(raw[38:40])  # Start for RF filter 2 (minutes)
        return header

    def _header_from_rt1_format_6(self):

        if self.debug:
            print("This is {}._header_from_rt1_format_6()".format(__class__.__name__))

        raw = self.file_info['header_raw']
        header = self._header_from_rt1_format_5()
        header['merid_dd'] = int(raw[41:43])  # Meridian date (day)
        header['merid_mo'] = int(raw[44:46])  # Meridian date (month)
        header['merid_yr'] = int(raw[47:49])  # Meridian date (year)
        header['start_dd'] = int(raw[50:52])  # Observation start date (day)
        header['start_mo'] = int(raw[53:55])  # Observation start date (month)
        header['start_yr'] = int(raw[56:58])  # Observation start date (year)
        header['h_stp_hh'] = int(raw[59:61])  # Observation stop time (hours)
        header['h_stp_mm'] = int(raw[62:64])  # Observation stop time (minutes)
        return header

    def _fix_corrupted_header(self):
        if self.debug:
            print("This is {}._fix_corrupted_header()".format(__class__.__name__))

        if self.file_info['filedate'] == '19910725':
            self.file_info['header_raw'] = "{}08{}".format(self.file_info['header_raw'][0:18],
                                                           self.file_info['header_raw'][20:])
        elif self.file_info['filedate'] == '19940224':
            self.file_info['header_raw'] = "{}0426{}".format(self.file_info['header_raw'][0:18],
                                                             self.file_info['header_raw'][22:])
        elif self.file_info['filedate'] == '19940305':
            self.file_info['header_raw'] = "{}0351{}".format(self.file_info['header_raw'][0:18],
                                                             self.file_info['header_raw'][22:])
        elif self.file_info['filedate'] == '19940306':
            self.file_info['header_raw'] = "{}0347{}".format(self.file_info['header_raw'][0:18],
                                                             self.file_info['header_raw'][22:])

    def _fix_old_version_header(self):
        if self.debug:
            print("This is {}._fix_old_version_header()".format(__class__.__name__))
        if self.file_info['header_version'] == 1:
            self.header['merid_hh'] = 0  # hour
            self.header['merid_mm'] = 0  # minute
        if self.file_info['header_version'] < 5:
            first_sweep_time = self.get_first_sweep().get_time()
            self.header['rf0_hour'] = first_sweep_time.hour  # Start for RF filter 0 (hours)
            self.header['rf0_minu'] = first_sweep_time.minute  # Start for RF filter 0 (minutes)
        if self.file_info['header_version'] < 6:
            self.header['merid_dd'] = self.file_info['filedate'][6:8]  # Meridian date (day)
            self.header['merid_mo'] = self.file_info['filedate'][4:6]  # Meridian date (month)
            self.header['merid_yr'] = self.file_info['filedate'][2:4]  # Meridian date (year)
            first_sweep_time = self.get_first_sweep().get_time()
            last_sweep_time = self.get_last_sweep().get_time()
            meridian_time = self.get_meridian_time()
            start_date = datetime.date(int(self.header['merid_yr']),
                                       int(self.header['merid_mo']),
                                       int(self.header['merid_dd']))
            if last_sweep_time < first_sweep_time:
                if meridian_time < first_sweep_time:
                    start_date = start_date - datetime.timedelta(days=1)
            self.header['start_dd'] = start_date.day  # Observation start date (day)
            self.header['start_mo'] = start_date.month  # Observation start date (month)
            self.header['start_yr'] = start_date.year  # Observation start date (year)
            self.header['h_stp_hh'] = last_sweep_time.hour  # Observation stop time (hours)
            self.header['h_stp_mm'] = last_sweep_time.minute  # Observation stop time (minutes)

    def get_single_sweep(self, index=0, load_data=True):
        if self.debug:
            print("This is {}.get_single_sweep()".format(__class__.__name__))
        return NDARoutineSweepRT1(self, index, load_data)

    def get_freq_axis(self):
        if self.debug:
            print("This is {}.get_freq_axis()".format(__class__.__name__))
        return [i/400*(self.meta['freq_max']-self.meta['freq_min'])+self.meta['freq_min']
                for i in range(self.meta['freq_len'])]

    def get_time_axis(self):
        if self.debug:
            print("This is {}.get_time_axis()".format(__class__.__name__))
        return [cur_sweep.get_datetime() for cur_sweep in self.sweeps(load_data=False)]

    def build_edr_data(self, start_time=None, end_time=None):
        if self.debug:
            print("This is {}.build_edr_data()".format(__class__.__name__))
        edr, start_time, end_time = MaserData.build_edr_data(self)
        edr['header'] = self.meta
        edr['time'] = []
        edr['ll_flux'] = []
        edr['rr_flux'] = []
        edr['status'] = []
        edr['rr_sweep_time_offset'] = []

        # EDR data shall start with LL polar. If first sweep is RR polar we skip it.
        keep_sweep = True
        if self.get_first_sweep(load_data=False).data['polar'] == 'RR':
            keep_sweep = False

        cur_ll_time = datetime.datetime.now()
        tmp_status = []

        for cur_sweep in self.sweeps(load_data=True):
            if keep_sweep:
                keep_sweep = True
                if cur_sweep.data['polar'] == 'LL':

                    # LL sweep of current EDR record
                    edr['ll_flux'].append(cur_sweep.data['data'])

                    # Current sweep time is time of EDR record
                    cur_ll_time = cur_sweep.get_datetime()
                    edr['time'].append(cur_ll_time)

                    # Storing LL sweep status
                    tmp_status.append(cur_sweep.data['status'])

                else:

                    # RR sweep of current EDR record
                    edr['rr_flux'].append(cur_sweep.data['data'])

                    # Computing RR sweep offset from LL sweep
                    cur_rr_offset_time = (cur_sweep.get_datetime() - cur_ll_time).total_seconds()
                    edr['rr_sweep_time_offset'].append(cur_rr_offset_time)

                    # Storing RR sweep status
                    tmp_status.append(cur_sweep.data['status'])

                    # Storing status is current EDR sweep, and resetting temporary status variable
                    edr['status'].append(tmp_status)
                    tmp_status = []

        edr['sweep_time_offset_ramp'] = [float("{0:.2f}".format(0.875*i)) for i in range(400)]

        return edr, start_time, end_time

    def _cdf_file_name(self):
        """
        Create CDF file name according to local dataset convention
        :return: CDF file name
        """
        if self.debug:
            print("This is {}._cdf_file_name()".format(__class__.__name__))

        time = self.get_time_axis()
        return '{}_{}_{}_edr_{:%Y%m%d%H%M}_{:%Y%m%d%H%M}_V{}.cdf'\
            .format(self.meta["obsty_id"], self.meta["instr_id"], self.meta["recvr_id"],
                    time[0], time[-1], _cdf_version)

    def _init_cdf(self, path_out):
        """
        Initialization of the output CDF file
        :param path_out: Path to write CDF file
        :return: cdf handle
        """
        if self.debug:
            print("This is {}._init_cdf()".format(__class__.__name__))

        # removing existing CDF file with same name if necessary (PyCDF cannot overwrite a CDF file)
        cdfout_path = os.path.join(path_out, self._cdf_file_name())
        if os.path.exists(cdfout_path):
            os.remove(cdfout_path)

        if self.debug:
            print("CDF file output: {}".format(cdfout_path))

        #    Opening CDF object
        cdf.lib.set_backward(False)  # this is setting the CDF version to be used
        cdfout = cdf.CDF(cdfout_path, '')
        cdfout.col_major(True)  # Column Major
        cdfout.compress(cdf.const.NO_COMPRESSION)  # No file level compression

        return cdfout

    def _get_istp_attributes(self) -> dict:
        """
        get ISTP CDF global attributes in a dict
        :return attrs: ISTP CDF global attributes
        """
        if self.debug:
            print("This is {}._get_istp_attributes()".format(__class__.__name__))
        attrs = dict()

        attrs['TITLE'] = "SRN NDA Routine Jupiter EDR Dataset"
        attrs['Project'] = ["SRN>Station de Radioastronomie Nancay", "ObsParis>Observatoire de Paris",
                            "PADC>Paris Astronomical Data Center"]
        attrs['Discipline'] = ["Space Physics>Magnetospheric Science", "Planetary Physics>Waves"]
        attrs['Data_type'] = "EDR>Experiment Data Record"
        attrs['Descriptor'] = "{}>Routine receiver with {} pointing".format(self.meta['recvr_id'],
                                                                            self.meta['target_name'])
        attrs['Data_version'] = _dat_version
        attrs['Instrument_type'] = "Radio Telescope"
        attrs['Source_name'] = "SRN_NDA>Nancay Decametric Array"
        attrs['Logical_source'] = "{}_{}_{}".format(attrs['Source_name'].split('>')[0],
                                                    attrs['Descriptor'].split('>')[0],
                                                    attrs['Data_type'].split('>')[0]).lower()
        attrs['Logical_file_id'] = "{}_000000000000_000000000000_v00".format(attrs['Logical_source'])
        attrs['Logical_source_description'] = "Jupiter Observations from the Routine receiver of the Nancay " \
                                              "Decameter Array at Station de Radioastronomie de Nancay"
        attrs['File_naming_convention'] = "source_descriptor_datatype_yyyyMMddhhmm_yyyyMMddhhmm_vVV"
        attrs['Mission_group'] = "SRN>Station de Radioastronomie Nancay"
        attrs['PI_name'] = "L. Lamy"
        attrs['PI_affiliation'] = ["LESIA>LESIA, Observatoire de Paris, PSL, CNRS, Sorbonne Universite, "
                                   "Univ. Paris Diderot, Sorbonne Paris Cite, "
                                   "5 place Jules Janssen, 92195 Meudon, France",
                                   "SRN>Station de Radioastronomie de Nancay, Observatoire de Paris, PSL, "
                                   "CNRS, Univ. Orleans, 18330 Nancay, France"]
        attrs['TEXT'] = "http://www.obs-nancay.fr/-Le-reseau-decametrique-.html?lang=en"
        attrs['Generated_by'] = ["LESIA", "SRN>Station de Radioastronomie de Nancay", "PADC"]
        attrs['Generation_date'] = "{:%Y%m%d}".format(datetime.datetime.now())
        attrs['LINK_TEXT'] = "The NDA Routine Jupiter data are available at "
        attrs['LINK_TITLE'] = "Station de Radioastronomie de Nancay"
        attrs['HTTP_LINK'] = "http://www.obs-nancay.fr/"
        attrs['MODS'] = ""
        attrs['Rules_of_use'] = ["SRN/NDA observations in open access can be freely used for scientific purposes. "
                                 "Their acquisition, processing and distribution is ensured by the SRN/NDA team, "
                                 "which can be contacted for any questions and/or collaborative purposes. ",
                                 "Contact email : contact_nda@obs-nancay.fr ",
                                 "We kindly request the authors of any communications and publications using these "
                                 "data to let us know about them, include citation to the reference below and "
                                 "appropriate acknowledgements whenever needed.",
                                 "Reference : A. Lecacheux, The Nancay Decameter Array: A Useful Step Towards Giant, "
                                 "New Generation Radio Telescopes for Long Wavelength Radio Astronomy, "
                                 "in Radio Astronomy at Long Wavelengths, eds. R. G. Stone, K. W. Weiler, "
                                 "M. L. Goldstein, & J.-L. Bougeret, AGU Geophys. Monogr. Ser., 119, 321, 2000.",
                                 "Acknowledgements : see the acknowledgement field."]
        attrs['Skeleton_version'] = _cdf_version
        attrs['Sotfware_version'] = "Maser4py {} {}".format(__class__.__name__, __version__)
        attrs['Software_language'] = "Python {}.{}".format(sys.version_info.major, sys.version_info.minor)
        attrs['Time_resolution'] = "1 second"
        attrs['Acknowledgement'] = "The authors acknowledge the Station de Radioastronomie de Nancay of the " \
                                   "Observatoire de Paris (USR 704-CNRS, supported by Universite d'Orleans, OSUC, " \
                                   "and Region Centre in France) for providing access to NDA observations accessible " \
                                   "online at http://www.obs-nancay.fr "
        attrs['ADID_ref'] = ""
        attrs['Validate'] = ""
        attrs['Parent'] = os.path.basename(self.file)

        return attrs

    def _get_vespa_attributes(self) -> dict:
        """
        get VESPA/EPNcore CDF global attributes in a dict
        :return attrs: VESPA/EPNcore CDF global attributes
        """
        if self.debug:
            print("This is {}._get_vespa_attributes()".format(__class__.__name__))
        attrs = dict()

        attrs['VESPA_dataproduct_type'] = 'DS>Dynamic Spectra'
        attrs['VESPA_target_class'] = self.meta['target_class']
        attrs['VESPA_target_region'] = self.meta['target_region']
        attrs['VESPA_feature_name'] = self.meta['feature_name']

        attrs['VESPA_time_sampling_step'] = self.meta['time_step']  # in seconds
        attrs['VESPA_time_exp'] = self.meta['time_exp'] / 1.e3  # in seconds

        attrs['VESPA_spectral_range_min'] = self.meta['freq_min']*1e6  # In Hz
        attrs['VESPA_spectral_range_max'] = self.meta['freq_max']*1e6  # In Hz
        attrs['VESPA_spectral_sampling_step'] = self.meta['freq_step']
        attrs['VESPA_spectral_resolution'] = self.meta['freq_res']

        attrs['VESPA_instrument_host_name'] = 'SRN>Station de Radioastronomie de Nancay'
        attrs['VESPA_instrument_name'] = 'NDA>Nancay Decameter Array'
        attrs['VESPA_receiver_name'] = 'Routine{}> Routine {}'.format(self.meta['target_name'][0:3],
                                                                      self.meta['target_name'])
        attrs['VESPA_measurement_type'] = "phys.flux.density;em.radio;phys.polarization.circular"
        attrs['VESPA_access_format'] = 'application/x-cdf'
        attrs['VESPA_bib_reference'] = "2000GMS...119..321L"

        return attrs

    def _get_pds_attributes(self) -> dict:
        """
        get VESPA/EPNcore CDF global attributes in a dict
        :returns: VESPA/EPNcore CDF global attributes
        """
        if self.debug:
            print("This is {}._get_pds_attributes()".format(__class__.__name__))

        attrs = dict()

        attrs['PDS_Observation_start_time'] = self.start_time.isoformat()
        attrs['PDS_Observation_stop_time'] = self.end_time.isoformat()
        attrs['PDS_Observation_target'] = self.meta['target_name']
        attrs['PDS_Observation_type'] = self.meta['Radio']

        return attrs

    def _get_local_attributes(self) -> dict:
        """
        get local CDF global attrbutes in a dict
        :returns: Local CDF global attributes
        """
        if self.debug:
            print("This is {}._get_local_attributes()".format(__class__.__name__))

        attrs = dict()

        # attrs['NDA_rf_filter_selected'] = tmp_rf_filt
        # attrs['NDA_rf_filter_change'] = tmp_rf_filt_change

        attrs['NDA_power_resolution'] = self.meta['power_resolution']
        attrs['NDA_meridian_time'] = self.get_meridian_datetime().isoformat() + 'Z'
        attrs['NDA_reference_level'] = self.meta['reference_level']
        attrs['NDA_sweep_duration'] = self.meta['sweep_duration'] / 1000.  # in seconds
        attrs['NDA_header_version'] = self.file_info['header_version']

        return attrs

    def _write_var_epoch_cdf(self, cdf_handle):
        """
        Writes the EPOCH variable into the output CDF file
        """

        if self.debug:
            print("This is {}._write_var_epoch_cdf()".format(__class__.__name__))

        date_start_round = self.start_time.replace(minute=0, second=0, microsecond=0)
        date_stop_round = self.end_time.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)

        # SETTING UP VARIABLES AND VARIABLE ATTRIBUTES
        #   The EPOCH variable type must be CDF_TIME_TT2000
        #   PDS-CDF requires no compression for variables.
        cdf_handle.new('EPOCH', data=self.get_time_axis(), type=cdf.const.CDF_TIME_TT2000,
                       compress=cdf.const.NO_COMPRESSION)
        cdf_handle['EPOCH'].attrs.new('VALIDMIN', data=datetime.datetime(2000, 1, 1), type=cdf.const.CDF_TIME_TT2000)
        cdf_handle['EPOCH'].attrs.new('VALIDMAX', data=datetime.datetime(2100, 1, 1), type=cdf.const.CDF_TIME_TT2000)
        cdf_handle['EPOCH'].attrs.new('SCALEMIN', data=date_start_round, type=cdf.const.CDF_TIME_TT2000)
        cdf_handle['EPOCH'].attrs.new('SCALEMAX', data=date_stop_round, type=cdf.const.CDF_TIME_TT2000)
        cdf_handle['EPOCH'].attrs['CATDESC'] = "Default time (TT2000)"
        cdf_handle['EPOCH'].attrs['FIELDNAM'] = "Epoch"
        cdf_handle['EPOCH'].attrs.new('FILLVAL', data=-9223372036854775808, type=cdf.const.CDF_TIME_TT2000)
        cdf_handle['EPOCH'].attrs['LABLAXIS'] = "Epoch"
        cdf_handle['EPOCH'].attrs['UNITS'] = "ns"
        cdf_handle['EPOCH'].attrs['VAR_TYPE'] = "support_data"
        cdf_handle['EPOCH'].attrs['SCALETYP'] = "linear"
        cdf_handle['EPOCH'].attrs['MONOTON'] = "INCREASE"
        cdf_handle['EPOCH'].attrs['TIME_BASE'] = "J2000"
        cdf_handle['EPOCH'].attrs['TIME_SCALE'] = "UTC"
        cdf_handle['EPOCH'].attrs['REFERENCE_POSITION'] = "Earth"
        cdf_handle['EPOCH'].attrs['SI_CONVERSION'] = "1.0e-9>s"
        cdf_handle['EPOCH'].attrs['UCD'] = "time.epoch"

    def _write_var_frequency_cdf(self, cdf_handle):
        """
        Writes the FREQUENCY variable into the output CDF file
        """

        if self.debug:
            print("This is {}._write_var_frequency_cdf()".format(__class__.__name__))

        # PDS-CDF requires no compression for variables.
        cdf_handle.new('FREQUENCY', data=self.get_freq_axis(), type=cdf.const.CDF_FLOAT,
                       compress=cdf.const.NO_COMPRESSION, recVary=False)
        cdf_handle['FREQUENCY'].attrs['CATDESC'] = "Frequency"
        cdf_handle['FREQUENCY'].attrs['DICT_KEY'] = "electric_field>power"
        cdf_handle['FREQUENCY'].attrs['FIELDNAM'] = "FREQUENCY"
        cdf_handle['FREQUENCY'].attrs.new('FILLVAL', data=-1.0e+31, type=cdf.const.CDF_REAL4)
        cdf_handle['FREQUENCY'].attrs['FORMAT'] = "F6.3"
        cdf_handle['FREQUENCY'].attrs['LABLAXIS'] = "Frequency"
        cdf_handle['FREQUENCY'].attrs['UNITS'] = "MHz"
        cdf_handle['FREQUENCY'].attrs.new('VALIDMIN', data=0., type=cdf.const.CDF_REAL4)
        cdf_handle['FREQUENCY'].attrs.new('VALIDMAX', data=40., type=cdf.const.CDF_REAL4)
        cdf_handle['FREQUENCY'].attrs['VAR_TYPE'] = "support_data"
        cdf_handle['FREQUENCY'].attrs['SCALETYP'] = "linear"
        cdf_handle['FREQUENCY'].attrs.new('SCALEMIN', data=self.meta['freq_min'], type=cdf.const.CDF_REAL4)
        cdf_handle['FREQUENCY'].attrs.new('SCALEMAX', data=self.meta['freq_max'], type=cdf.const.CDF_REAL4)
        cdf_handle['FREQUENCY'].attrs['SI_CONVERSION'] = "1.0e6>Hz"
        cdf_handle['FREQUENCY'].attrs['UCD'] = "em.freq"

    def make_cdf(self, path_out):
        """
        Make CDF file from RT1 data
        :param path_out: Path to write CDF file
        """
        if self.debug:
            print("This is {}.make_cdf()".format(__class__.__name__))

        # Initializing CDF file
        cdf_handle = self._init_cdf(path_out)

        # Loading global attributes
        for attr_key, attr_val in self._get_istp_attributes().items():
            cdf_handle.attrs[attr_key] = attr_val
        for attr_key, attr_val in self._get_vespa_attributes().items():
            cdf_handle.attrs[attr_key] = attr_val
        for attr_key, attr_val in self._get_pds_attributes().items():
            cdf_handle.attrs[attr_key] = attr_val
        for attr_key, attr_val in self._get_local_attributes().items():
            cdf_handle.attrs[attr_key] = attr_val

        self._write_var_epoch_cdf(cdf_handle)
        self._write_var_frequency_cdf(cdf_handle)
        cdf_handle.close()
        return cdf


class NDARoutineDataCDF(NDARoutineData):

    def __init__(self, file, debug=False):
        NDARoutineData.__init__(self, file, debug=debug)
        self.name = "SRN/NDA Routine EDR CDF Dataset"
        self.meta['freq_min'] = float(self.header['VESPA_spectral_range_min']) / 1e6  # MHz
        self.meta['freq_max'] = float(self.header['VESPA_spectral_range_max']) / 1e6  # MHz
        self.meta['freq_res'] = float(self.header['VESPA_spectral_resolution']) / 1e3  # kHz
        self.meta['freq_stp'] = (self.meta['freq_max']-self.meta['freq_min'])/0.4  # kHz
        self.edr = None

    def _set_file_handle(self):
        self.file_handle = cdf.CDF(self.file)

    def _set_file_date(self):
        parent_name = self.file_handle.attrs['Parents'][0]
        filedate = ((parent_name.split('.'))[0])[1:7]
        if int(filedate[0:2]) < 90:
            century_str = '20'
        else:
            century_str = '19'
        self.file_info['filedate'] = "{}{}".format(century_str, filedate)

    def __len__(self):
        return len(self.file_handle['Epoch'])

    def get_mime_type(self):
        return 'application/x-cdf'

    def get_start_date(self):
        return self.get_first_sweep().get_datetime().date()

    def get_meridian_datetime(self, from_file=True):
        meridian_dt = None
        if from_file:
            meridian_dt = dateutil.parser.parse(self.file_handle.attrs['NDA_meridian_time'][0], ignoretz=True)
        else:
            NDARoutineError("Ephemeris from IMCCE webservice not implemented yet")

        return meridian_dt

    def _header_from_file(self):
        tmp_header = self.file_handle.attrs
        header = dict()
        header_keys = list()
        for key in tmp_header:
            if len(tmp_header[key]) == 1:
                header[key] = tmp_header[key][0]
            elif len(tmp_header[key]) > 1:
                header[key] = list()
                for item in tmp_header[key]:
                    header[key].append(item)
            else:
                header[key] = None
        return header

    def get_single_sweep(self, index=0, load_data=True):
        return NDARoutineSweepCDF(self, index, load_data)

    def sweeps(self):
        return (self.get_single_sweep(cur_sweep_id) for cur_sweep_id in range(len(self)))

    def get_freq_axis(self):
        freq = list()
        for item in self.file_handle['Frequency']:
            freq.append(float(item))
        return freq

    def get_time_axis(self):
        time = list()
        for item in self.file_handle['Epoch']:
            time.append(item)
        return time


class NDARoutineSweepRT1(MaserDataSweep):

    def __init__(self, parent, index_input, load_data=True):
        MaserDataSweep.__init__(self, parent, index_input)
        self.debug = self.parent.debug
        self.data = dict()

        self.data_start_pos = self.parent.file_info['data_offset_in_file'] + \
                              self.index * self.parent.file_info['record_size']
        rec_date_fields = ['hr', 'min', 'sec', 'cs']
        rec_date_dtype = '<bbbb'

        f = self.parent.file_handle

        f.seek(self.data_start_pos, 0)
        block = f.read(4)
        rec_date = dict(zip(rec_date_fields, struct.unpack(rec_date_dtype, block)))
        rec_data = list()
        rec_status = 0

        self.data['loaded'] = False
        self.data['hms'] = rec_date
        self.data['data'] = rec_data
        self.data['status'] = rec_status

        self.fix_hms_time()

        if load_data:
            self.load_data()

        if self.index % 2 == 0:
            self.data['polar'] = 'LL'
        else:
            self.data['polar'] = 'RR'

    def load_data(self):

        f = self.parent.file_handle

        f.seek(self.data_start_pos+4, 0)
        block = f.read(401)
        self.data['data'] = struct.unpack('<' + 'b' * 400, block[0:400])
        self.data['status'] = int(block[400])

        self.data['loaded'] = True

    def get_time(self):
        return datetime.time(int(self.data['hms']['hr']),
                             int(self.data['hms']['min']),
                             int(self.data['hms']['sec']),
                             int(self.data['hms']['cs']) * 10000)

    def get_datetime(self):

        start_date = self.parent.get_start_date()
        start_time = self.parent.get_first_sweep().get_time()
        end_time = self.parent.get_first_sweep().get_time()
        cur_time = self.get_time()
        meridian_date = self.parent.get_meridian_datetime().date()
        cur_date = meridian_date
        if start_date < meridian_date:
            if self.get_time() > datetime.time(12, 0, 0):
                cur_date = start_date

        return datetime.datetime(cur_date.year, cur_date.month, cur_date.day,
                                 cur_time.hour, cur_time.minute, cur_time.second, cur_time.microsecond)

    def get_data(self):
        if not self.data['loaded']:
            self.load_data()
        return self.data['data']

    def get_data_in_db(self):
        if not self.data['loaded']:
            self.load_data()
        return [item * 0.3125 for item in self.data['data']]

    def fix_hms_time(self):
        hms = self.data['hms']
        ts_error = False
        if hms['hr'] > 23:
            ts_error = True
        if hms['min'] > 59:
            ts_error = True
        if hms['sec'] > 59:
            ts_error = True
        if hms['cs'] > 99:
            ts_error = True

        if ts_error:
            if hms['cs'] == 100:
                hms['cs'] = 0
                hms['sec'] += 1
            if hms['sec'] == 60:
                hms['sec'] = 0
                hms['min'] += 1
            if hms['min'] == 60:
                hms['min'] = 0
                hms['hr'] += 1
            if hms['hr'] == 24:
                hms['hr'] = 0

        self.data['hms'] = hms


class NDARoutineSweepCDF(MaserDataSweep):

    def __init__(self, parent, index_input, load_data=True):
        MaserDataSweep.__init__(self, parent, index_input)
        self.debug = self.parent.debug
        self.data = dict()

        f = self.parent.file_handle
        self.data['epoch'] = f['Epoch'][self.index]
        self.data['data'] = dict()
        self.data['loaded'] = False
        self.data['status'] = {'LL': 0, 'RR': 0}

        if load_data:
            self.load_data()

        self.data['polar'] = ['LL', 'RR']

    def load_data(self, polar=None):
        # if (data has not been loaded yet) or (data has been loaded, but not this polar):
        if (not self.data['loaded']) or (self.data['loaded'] and polar not in self.data['polar']):
            f = self.parent.file_handle
            if polar is not None:
                self.data['data'][polar] = f[polar][self.index]
            else:
                self.data['data']['LL'] = f['LL'][self.index]
                self.data['data']['RR'] = f['RR'][self.index]
            self.data['RR_SWEEP_TIME_OFFSET'] = float(f['RR_SWEEP_TIME_OFFSET'][self.index])
            self.data['status'] = f['STATUS'][self.index]
            self.data['loaded'] = True

    def get_data(self):
        if not self.data['loaded']:
            self.load_data()
        return self.data['data']

    def get_data_in_db(self):
        if not self.data['loaded']:
            self.load_data()
        data_in_db = dict()
        data_in_db['LL'] = [item * 0.3125 for item in self.data['data']['LL']]
        data_in_db['RR'] = [item * 0.3125 for item in self.data['data']['RR']]
        return data_in_db

    def get_datetime(self):
        return self.data['epoch']

    def get_time(self):
        return self.get_datetime().time()


################################################################################
# Main RT1 to CDF
################################################################################
def convert_rt1_to_cdf(file_rt1, debug=False):
    """
    Main script that transforms an RT1 file into a CDF file
    :param file_rt1: path of input RT1 file
    :param debug: Set to True to have verbose output
    """
    if debug:
        print("This is convert_rt1_to_cdf()")

    o = NDARoutineDataRT1(file_rt1, debug=debug)
    c = o.make_cdf('/tmp/')
    c.check_cdf()
