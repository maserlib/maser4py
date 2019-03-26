import unittest
import datetime
from maser.data.data import *
from maser.data.padc.radiojove.radiojove_spx import RadioJoveDataSPXFromFile
from maser.data.tests import load_test_data, get_data_directory

load_test_data("radiojove")
file_path = str(get_data_directory() / "radiojove" / "sps" / "161210000000.sps")


class RadioJoveDataTest(unittest.TestCase):

    """Test case for RadioJoveData class"""

    def test_class(self):
        o = RadioJoveDataSPXFromFile(file_path)
        self.assertIsInstance(o, MaserDataFromFile)

    def test_file_info(self):
        o = RadioJoveDataSPXFromFile(file_path)
        self.assertIsInstance(o.file_info, dict)
        self.assertTrue(set(o.file_info.keys()) == {'bytes_per_step', 'data_length', 'prim_hdr_length',
                                                    'data_format', 'record_data_offset', 'name', 'size',
                                                    'prim_hdr_raw', 'notes_raw', 'lun', 'file_data_offset'})
        self.assertEqual(o.file_info['bytes_per_step'], 1202)
        self.assertEqual(o.file_info['data_length'], 12515225)
        self.assertEqual(o.file_info['prim_hdr_length'], 156)
        self.assertEqual(o.file_info['data_format'], '>601H')
        self.assertEqual(o.file_info['record_data_offset'], 0)
        self.assertEqual(o.file_info['name'], o.file)
        self.assertEqual(o.file_info['size'], 12515738)
        self.assertTrue(o.file_info['lun'].closed)

    def test_notes(self):
        o = RadioJoveDataSPXFromFile(file_path)
        self.assertIsInstance(o.notes, dict)
        self.assertEqual(o.notes['ANTENNATYPE'], 'unknown')
        self.assertIsInstance(o.notes['BANNER'], list)
        self.assertEqual(o.notes['BANNER'][0], 'AJ4CO Observatory <DATE> - DPS on TFD Array - RCP')
        self.assertEqual(o.notes['BANNER'][1], 'AJ4CO Observatory <DATE> - DPS on TFD Array - LCP')
        self.assertEqual(o.notes['COLORFILE'], 'AJ4CO-Rainbow.txt')
        self.assertIsInstance(o.notes['COLORGAIN'], list)
        self.assertEqual(o.notes['COLORGAIN'], [1.95, 1.95])
        self.assertIsInstance(o.notes['COLOROFFSET'], list)
        self.assertEqual(o.notes['COLOROFFSET'], [1975, 1975])
        self.assertEqual(o.notes['COLORRES'], 1)
        self.assertEqual(o.notes['DUALSPECFILE'], True)
        self.assertEqual(o.notes['HIF'], 32000000)
        self.assertEqual(o.notes['LOWF'], 16000000)
        self.assertEqual(o.notes['RCVR'], 5)
        self.assertEqual(o.notes['STEPS'], 300)
        self.assertEqual(o.notes['SWEEPS'], 10412)
        self.assertEqual(o.notes['free_text'], '')

    def test_header_sps(self):
        o = RadioJoveDataSPXFromFile(file_path)
        self.assertIsInstance(o.header, dict)
        self.assertEqual(o.header['antenna_type'], 'unknown')
        self.assertEqual(o.header['author'], 'Dave Typinski')
        self.assertEqual(o.header['banner0'], 'AJ4CO Observatory 2016-12-10 - DPS on TFD Array - RCP')
        self.assertEqual(o.header['banner1'], 'AJ4CO Observatory 2016-12-10 - DPS on TFD Array - LCP')
        self.assertEqual(o.header['chartmax'], 0.0)
        self.assertEqual(o.header['chartmin'], 0.0)
        self.assertEqual(o.header['color_file'], 'AJ4CO-Rainbow.txt')
        self.assertIsInstance(o.header['feeds'], list)
        self.assertIsInstance(o.header['feeds'][0], dict)
        self.assertIsInstance(o.header['feeds'][1], dict)
        self.assertEqual(o.header['feeds'][0]['CATDESC'], 'RCP Flux Density')
        self.assertEqual(o.header['feeds'][0]['FIELDNAM'], 'RR')
        self.assertEqual(o.header['feeds'][0]['LABLAXIS'], 'RCP Power Spectral Density')
        self.assertEqual(o.header['feeds'][1]['CATDESC'], 'LCP Flux Density')
        self.assertEqual(o.header['feeds'][1]['FIELDNAM'], 'LL')
        self.assertEqual(o.header['feeds'][1]['LABLAXIS'], 'LCP Power Spectral Density')
        self.assertEqual(o.header['nfeed'], 2)
        self.assertEqual(o.header['nfreq'], 300)
        self.assertEqual(o.header['nstep'], 10412)
        self.assertEqual(o.header['file_name'], o.file)
        self.assertEqual(o.header['file_type'], 'SPS')
        self.assertEqual(o.header['fmax'], 32.0)
        self.assertEqual(o.header['fmin'], 16.0)
        self.assertEqual(o.header['free_text'], '')
        self.assertEqual(o.header['gain0'], 1.95)
        self.assertEqual(o.header['gain1'], 1.95)
        self.assertEqual(o.header['instr_id'], 'DPS')
        self.assertEqual(o.header['latitude'], 29.0)
        self.assertEqual(o.header['level'], 'EDR')
        self.assertEqual(o.header['longitude'], -82.0)
        self.assertEqual(o.header['nchannels'], 300)
        self.assertEqual(o.header['nfeed'], 2)
        self.assertEqual(o.header['nfreq'], 300)
        self.assertEqual(o.header['note_length'], 357)
        self.assertEqual(o.header['nstep'], 10412)
        self.assertEqual(o.header['obsloc'], 'High Springs, FL')
        self.assertEqual(o.header['obsname'], 'AJ4CO DPS')
        self.assertEqual(o.header['obsty_id'], 'AJ4CO')
        self.assertEqual(o.header['offset0'], 1975)
        self.assertEqual(o.header['offset1'], 1975)
        self.assertEqual(o.header['polar0'], 'RR')
        self.assertEqual(o.header['polar1'], 'LL')
        self.assertEqual(o.header['product_type'], 'sp2_300')
        self.assertEqual(o.header['sft'], '0000208016')
        self.assertEqual(o.header['source'], '')
        self.assertEqual(o.header['start_jdtime'], 2457732.500009352)
        self.assertIsInstance(o.header['start_time'], datetime.datetime)
        self.assertEqual(o.header['start_time'], datetime.datetime(2016, 12, 10, 0, 0, 0, 808002))
        self.assertEqual(o.header['stop_jdtime'], 2457732.5189176155)
        self.assertIsInstance(o.header['stop_time'], datetime.datetime)
        self.assertEqual(o.header['stop_time'], datetime.datetime(2016, 12, 10, 0, 27, 14, 481981))
        self.assertEqual(o.header['time_integ'], 0.1569029945583926)
        self.assertEqual(o.header['time_step'], 0.1569029945583926)
        self.assertEqual(o.header['timezone'], 0)



