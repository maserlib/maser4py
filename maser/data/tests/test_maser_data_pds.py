import unittest
import datetime
import astropy.units as u

from maser.data.tests import load_test_data, get_data_directory
from maser.data import MaserDataFromFile
import numpy
from maser.data.pds.voyager.pra import PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel, \
    PDSPPIVoyagerPRADataFromLabel, PDSPPIVoyagerPRADataObject, PDSPPIVoyagerPRAHighRateTimeSeriesObject
from maser.data.pds.cassini.rpws.wbr import PDSPPICassiniRPWSWBRFullResDataFromLabel, \
    PDSPPICassiniRPWSWBRDataObject, PDSPPICassiniRPWSWBRRowPrefixTable
from maser.data.pds.cassini.rpws.hfr import PDSPPICassiniRPWSHFRLowRateFullDataFromLabel, \
    PDSPPICassiniRPWSHFRDataObject
from maser.data.pds.classes import PDSDataFromLabel, PDSLabelDict, PDSDataTableObject, PDSDataTimeSeriesObject

load_test_data("pds")

root_data_path = get_data_directory() / 'pds'
file = root_data_path / 'VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1' / 'PRA_I.LBL'
ov1 = PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel(str(file), load_data=False)

file = root_data_path / 'VG1-J-PRA-4-SUMM-BROWSE-48SEC-V1' / 'T790306.LBL'
ov2 = PDSPPIVoyagerPRADataFromLabel(str(file), load_data=False)

file = root_data_path / 'VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1' / 'PRA.LBL'
ov3 = PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel(str(file), load_data=False)

file = root_data_path / 'VG2-N-PRA-2-RDR-HIGHRATE-60MS-V1' / 'C1065111.LBL'
ov4 = PDSPPIVoyagerPRADataFromLabel(str(file), load_data=False)

file = root_data_path / 'VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1' / 'VG2_NEP_PRA_6SEC.LBL'
ov5 = PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel(str(file), load_data=False)

file = root_data_path / 'CO-V_E_J_S_SS-RPWS-2-REFDR-WBRFULL-V1' / 'T2000366_09_8025KHZ4_WBRFR.LBL'
oc1 = PDSPPICassiniRPWSWBRFullResDataFromLabel(str(file), load_data=False)

file = root_data_path / 'CO-V_E_J_S_SS-RPWS-3-RDR-LRFULL-V1' / 'T2000366_HFR0.LBL'
oc2 = PDSPPICassiniRPWSHFRLowRateFullDataFromLabel(str(file), load_data=False)


class PDSDataFromLabelClassTest(unittest.TestCase):
    """Test case for PDSDataFromFile class"""

    def test_class(self):
        self.assertIsInstance(ov1, PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel)
        self.assertIsInstance(ov1, PDSPPIVoyagerPRADataFromLabel)
        self.assertIsInstance(ov1, PDSDataFromLabel)
        self.assertIsInstance(ov1, MaserDataFromFile)

        self.assertIsInstance(ov2, PDSPPIVoyagerPRADataFromLabel)
        self.assertIsInstance(ov2, PDSDataFromLabel)
        self.assertIsInstance(ov2, MaserDataFromFile)

        self.assertIsInstance(ov3, PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel)
        self.assertIsInstance(ov3, PDSPPIVoyagerPRADataFromLabel)
        self.assertIsInstance(ov3, PDSDataFromLabel)
        self.assertIsInstance(ov3, MaserDataFromFile)

        self.assertIsInstance(ov4, PDSPPIVoyagerPRADataFromLabel)
        self.assertIsInstance(ov4, PDSDataFromLabel)
        self.assertIsInstance(ov4, MaserDataFromFile)

        self.assertIsInstance(ov5, PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel)
        self.assertIsInstance(ov5, PDSPPIVoyagerPRADataFromLabel)
        self.assertIsInstance(ov5, PDSDataFromLabel)
        self.assertIsInstance(ov5, MaserDataFromFile)

        self.assertIsInstance(oc1, PDSPPICassiniRPWSWBRFullResDataFromLabel)
        self.assertIsInstance(oc1, PDSDataFromLabel)
        self.assertIsInstance(oc1, MaserDataFromFile)

        self.assertIsInstance(oc2, PDSPPICassiniRPWSHFRLowRateFullDataFromLabel)
        self.assertIsInstance(oc2, PDSDataFromLabel)
        self.assertIsInstance(oc2, MaserDataFromFile)

    def test_label(self):
        self.assertEqual(ov1.file, ov1.file.replace('.TAB', '.LBL'))
        self.assertIsInstance(ov1.label, PDSLabelDict)

        self.assertEqual(oc1.file, oc1.file.replace('.TAB', '.LBL'))
        self.assertIsInstance(oc1.label, PDSLabelDict)

        self.assertEqual(oc2.file, oc2.file.replace('.TAB', '.LBL'))
        self.assertIsInstance(oc2.label, PDSLabelDict)

    def test_object(self):
        self.assertIsInstance(ov1.object, dict)
        self.assertIn('TABLE', ov1.objects)
        self.assertIn('TABLE', ov1.object.keys())
        self.assertIsInstance(ov1.object['TABLE'], PDSPPIVoyagerPRADataObject)

        self.assertIsInstance(ov2.object, dict)
        self.assertIn('TIME_SERIES', ov2.objects)
        self.assertIn('TIME_SERIES', ov2.object.keys())
        self.assertIsInstance(ov2.object['TIME_SERIES'], PDSPPIVoyagerPRADataObject)

        self.assertIsInstance(ov3.object, dict)
        self.assertIn('TABLE', ov3.objects)
        self.assertIn('TABLE', ov3.object.keys())
        self.assertIsInstance(ov3.object['TABLE'], PDSPPIVoyagerPRADataObject)

        self.assertIsInstance(ov4.object, dict)
        self.assertSetEqual({'HEADER_TABLE', 'F3_F4_TIME_SERIES', 'F1_F2_TIME_SERIES'}, set(ov4.objects))
        self.assertSetEqual({'HEADER_TABLE', 'F3_F4_TIME_SERIES', 'F1_F2_TIME_SERIES'}, set(ov4.object.keys()))
        self.assertIsInstance(ov4.object['HEADER_TABLE'], PDSPPIVoyagerPRADataObject)
        self.assertIsInstance(ov4.object['HEADER_TABLE'].data, PDSDataTableObject)
        self.assertIsInstance(ov4.object['F1_F2_TIME_SERIES'], PDSPPIVoyagerPRADataObject)
        self.assertIsInstance(ov4.object['F1_F2_TIME_SERIES'].data, PDSDataTableObject)
        self.assertIsInstance(ov4.object['F1_F2_TIME_SERIES'].data, PDSDataTimeSeriesObject)
        self.assertIsInstance(ov4.object['F1_F2_TIME_SERIES'].data, PDSPPIVoyagerPRAHighRateTimeSeriesObject)
        self.assertIsInstance(ov4.object['F3_F4_TIME_SERIES'], PDSPPIVoyagerPRADataObject)
        self.assertIsInstance(ov4.object['F3_F4_TIME_SERIES'].data, PDSDataTableObject)
        self.assertIsInstance(ov4.object['F3_F4_TIME_SERIES'].data, PDSDataTimeSeriesObject)
        self.assertIsInstance(ov4.object['F3_F4_TIME_SERIES'].data, PDSPPIVoyagerPRAHighRateTimeSeriesObject)

        self.assertIsInstance(ov5.object, dict)
        self.assertIn('TABLE', ov5.objects)
        self.assertIn('TABLE', ov5.object.keys())
        self.assertIsInstance(ov5.object['TABLE'], PDSPPIVoyagerPRADataObject)

        self.assertIsInstance(oc1.object, dict)
        self.assertSetEqual({'TIME_SERIES', 'WBR_ROW_PREFIX_TABLE'}, set(oc1.objects))
        self.assertSetEqual({'TIME_SERIES', 'WBR_ROW_PREFIX_TABLE'}, set(oc1.object.keys()))
        self.assertIsInstance(oc1.object['TIME_SERIES'], PDSPPICassiniRPWSWBRDataObject)
        self.assertIsInstance(oc1.object['TIME_SERIES'].data, PDSDataTimeSeriesObject)
        self.assertIsInstance(oc1.object['WBR_ROW_PREFIX_TABLE'], PDSPPICassiniRPWSWBRDataObject)
        self.assertIsInstance(oc1.object['WBR_ROW_PREFIX_TABLE'].data, PDSPPICassiniRPWSWBRRowPrefixTable)

        self.assertIsInstance(oc2.object, dict)
        self.assertSetEqual({'LRFULL_TABLE', 'FREQUENCY_TABLE', 'SPECTRAL_DENSITY_TABLE', 'TIME_TABLE'},
                            set(oc2.objects))
        self.assertSetEqual({'LRFULL_TABLE', 'FREQUENCY_TABLE', 'SPECTRAL_DENSITY_TABLE', 'TIME_TABLE'},
                            set(oc2.object.keys()))
        self.assertIsInstance(oc2.object['LRFULL_TABLE'], PDSPPICassiniRPWSHFRDataObject)
        self.assertIsInstance(oc2.object['LRFULL_TABLE'].data, PDSDataTableObject)
        self.assertIsInstance(oc2.object['FREQUENCY_TABLE'], PDSPPICassiniRPWSHFRDataObject)
        self.assertIsInstance(oc2.object['FREQUENCY_TABLE'].data, PDSDataTableObject)
        self.assertIsInstance(oc2.object['TIME_TABLE'], PDSPPICassiniRPWSHFRDataObject)
        self.assertIsInstance(oc2.object['TIME_TABLE'].data, PDSDataTableObject)
        self.assertIsInstance(oc2.object['SPECTRAL_DENSITY_TABLE'], PDSPPICassiniRPWSHFRDataObject)
        self.assertIsInstance(oc2.object['SPECTRAL_DENSITY_TABLE'].data, PDSDataTableObject)

    def test_load_data(self):

        # OV1 : pra.PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel

        self.assertEqual(ov1.load_data_flag['TABLE'], False)
        self.assertEqual(ov1.object['TABLE'].data_loaded, False)
        ov1.load_data('TABLE')
        self.assertEqual(ov1.load_data_flag['TABLE'], True)
        self.assertEqual(ov1.object['TABLE'].data_loaded, True)

        # OV2 : pra.PDSPPIVoyagerPRADataFromLabel

        self.assertEqual(ov2.load_data_flag['TIME_SERIES'], False)
        self.assertEqual(ov2.object['TIME_SERIES'].data_loaded, False)
        ov2.load_data('TIME_SERIES')
        self.assertEqual(ov2.load_data_flag['TIME_SERIES'], True)
        self.assertEqual(ov2.object['TIME_SERIES'].data_loaded, True)

        # OV3 : pra.PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel

        self.assertEqual(ov3.load_data_flag['TABLE'], False)
        self.assertEqual(ov3.object['TABLE'].data_loaded, False)
        ov3.load_data()
        self.assertEqual(ov3.load_data_flag['TABLE'], False)
        self.assertEqual(ov3.object['TABLE'].data_loaded, False)
        ov3.load_data(True)
        self.assertEqual(ov3.load_data_flag['TABLE'], True)
        self.assertEqual(ov3.object['TABLE'].data_loaded, True)

        # OV4 : pra.PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel

        self.assertEqual(ov4.load_data_flag['HEADER_TABLE'], False)
        self.assertEqual(ov4.object['HEADER_TABLE'].data_loaded, False)
        ov4.load_data('HEADER_TABLE')
        self.assertEqual(ov4.load_data_flag['HEADER_TABLE'], True)
        self.assertEqual(ov4.object['HEADER_TABLE'].data_loaded, True)
        self.assertEqual(ov4.load_data_flag['F1_F2_TIME_SERIES'], False)
        self.assertEqual(ov4.object['F1_F2_TIME_SERIES'].data_loaded, False)
        ov4.load_data(['HEADER_TABLE', 'F1_F2_TIME_SERIES'])
        self.assertEqual(ov4.load_data_flag['F1_F2_TIME_SERIES'], True)
        self.assertEqual(ov4.object['F1_F2_TIME_SERIES'].data_loaded, True)


class PDSPPICassiniRPWSHFRLowRateFullDataFromLabelClassTest(unittest.TestCase):
    """Test case for PDS PPI Cassini RPWS HFR Low Rate Full"""

    def test_frequency(self):
        freq_table = oc2.object['FREQUENCY_TABLE']
        self.assertLessEqual((freq_table.data['FREQUENCY'][0, 0] - 3954.83422852)/3954.83422852, 1e-10)
        self.assertLessEqual((freq_table.data['FREQUENCY'][0, 23] - 298616.8125)/298616.8125, 1e-10)
        self.assertEqual(len(freq_table.data['FREQUENCY']), 1)
        self.assertEqual(numpy.shape(freq_table.data['FREQUENCY']), (1, 24))
        self.assertListEqual(list(oc2.get_freq_axis(unit='Hz')), list(freq_table.data['FREQUENCY'][0]))

    def test_times(self):
        oc2.load_data(True)
        self.assertEqual(oc2.object['TIME_TABLE'].data['SCET_DAY'][0], 15705)
        self.assertEqual(oc2.object['FREQUENCY_TABLE'].data['SCET_DAY'][0], 15705)
        self.assertEqual(oc2.object['SPECTRAL_DENSITY_TABLE'].data['SCET_DAY'][0], 15705)

        self.assertEqual(oc2.object['TIME_TABLE'].data['SCET_MILLISECOND'][0], 11999)
        self.assertEqual(oc2.object['FREQUENCY_TABLE'].data['SCET_MILLISECOND'][0], 32395775)
        self.assertEqual(oc2.object['SPECTRAL_DENSITY_TABLE'].data['SCET_MILLISECOND'][0], 11999)
        self.assertEqual(len(oc2.object['SPECTRAL_DENSITY_TABLE'].data['SCET_MILLISECOND']), 3784)

        self.assertEqual(len(oc2.object['TIME_TABLE'].data['TIME'][0]), 24)
        self.assertEqual(oc2.object['TIME_TABLE'].data['TIME'][0, 0], 0)
        self.assertLessEqual((oc2.object['TIME_TABLE'].data['TIME'][0, 23] - 1.1266667) / 1.1266667, 1e-10)

        self.assertEqual(len(oc2.get_time_axis()), 3784)
        self.assertEqual(oc2.get_time_axis()[0], datetime.datetime(2000, 12, 31, 0, 0, 11, 999000))
        self.assertEqual(oc2.get_time_axis()[-1], datetime.datetime(2000, 12, 31, 8, 59, 56, 56000))
        self.assertEqual(oc2.start_time, datetime.datetime(2000, 12, 31, 0, 0))
        self.assertEqual(oc2.end_time, datetime.datetime(2001, 1, 1, 0, 0))


# class PDSPPIVoyagerPRAJupiterDataTest(unittest.TestCase):
#
#     """Test case for PDS Jupiter Voyager PRA-LB"""
#
#     def test_class(self):
#         obj = maser.data.pds.ppi.voyager.pra.PDSPPIVoyagerPRAJupiterData(
#             "1979-01-06T00:00:00", "1979-01-06T01:00:00", 1, root_data_path=root_data_path)
#         self.assertIsInstance(obj, maser.data.data.MaserDataFromInterval)
#         self.assertEqual(obj.data_path, os.path.join(root_data_path, 'VG1_JUPITER'))
#
#     def test_get_frame_times(self):
#         frame_times = maser.data.pds.ppi.voyager.pra.PDSPPIVoyagerPRAJupiterData.get_frame_times(file)
#         self.assertEqual(frame_times[0], datetime.datetime(1979, 1, 6, 0, 0, 34))
#         self.assertEqual(frame_times[-1], datetime.datetime(1979, 1, 30, 23, 59, 47))
#         self.assertEqual(len(frame_times), 35569)
#
#     def test_get_freq_list(self):
#         frequency = maser.data.pds.ppi.voyager.pra.PDSPPIVoyagerPRAJupiterData.get_freq_list()
#         self.assertEqual(frequency[0], 1326)
#         self.assertAlmostEqual(frequency[-1], 1.2)
#         self.assertEqual(len(frequency), 70)
#
#     def test_load_data_frames(self):
#         frames = maser.data.pds.ppi.voyager.pra.PDSPPIVoyagerPRAJupiterData.load_data_frames(file, 1, 2)
#         self.assertEqual(len(frames), 8)
#         self.assertEqual(frames[0]['datetime'], datetime.datetime(1979, 1, 6, 0, 1, 22))
#         self.assertEqual(frames[1]['datetime'], datetime.datetime(1979, 1, 6, 0, 1, 28))
#         self.assertEqual(frames[7]['datetime'], datetime.datetime(1979, 1, 6, 0, 2, 4))
#
#     def test_data_content(self):
#         obj = maser.data.pds.ppi.voyager.pra.PDSPPIVoyagerPRAJupiterData(
#             "1979-01-06T00:00:00", "1979-01-06T01:00:00", 1, root_data_path=root_data_path)
#         self.assertEqual(len(obj), 528)
#         self.assertEqual(obj['datetime'][0], datetime.datetime(1979, 1, 6, 0, 1, 22))
#         self.assertEqual(obj['datetime'][-1], datetime.datetime(1979, 1, 6, 0, 59, 40))
#         self.assertEqual(obj['data'][0][0], 2730)
#
#     def test_get_polar_data(self):
#         obj = maser.data.pds.ppi.voyager.pra.PDSPPIVoyagerPRAJupiterData(
#             "1979-01-06T00:00:00", "1979-01-06T01:00:00", 1, root_data_path=root_data_path)
#         data = obj.get_polar_data('R')
#         self.assertEqual(data[0]['polar'], 'R')