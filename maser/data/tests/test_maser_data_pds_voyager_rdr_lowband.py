import unittest
import datetime
from maser.data.tests import load_test_data, get_data_directory
from maser.data import MaserDataFromFile
from maser.data.pds.voyager.pra import PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel, \
    PDSPPIVoyagerPRADataFromLabel, PDSPPIVoyagerPRADataObject
from maser.data.pds.classes import PDSDataFromLabel, PDSLabelDict
from maser.data.pds import load_pds_from_label

load_test_data("pds")
root_data_path = get_data_directory() / 'pds'

file = root_data_path / 'VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1' / 'PRA_I.LBL'
ov1 = PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel(str(file), load_data=False)
ov1a = PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel(str(file), load_data=True)
ov1l = load_pds_from_label(str(file), load_data=False)

file = root_data_path / 'VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1' / 'PRA.LBL'
ov3 = PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel(str(file), load_data=True)
ov3l = load_pds_from_label(str(file), load_data=False)

file = root_data_path / 'VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1' / 'VG2_NEP_PRA_6SEC.LBL'
ov5 = PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel(str(file), load_data=True)
ov5l = load_pds_from_label(str(file), load_data=False)


class LoadPDSFromLabel(unittest.TestCase):
    """Test case for load_pds_from_label function"""

    def test_loader(self):
        self.assertIsInstance(ov1l, PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel)
        self.assertIsInstance(ov3l, PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel)
        self.assertIsInstance(ov5l, PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel)


class PDSPPIVoyagerPRARDRLowBand6SecDataFromLabelVG1J(unittest.TestCase):
    """Test case for PDSPPIVoyagerPRARDRLowBand6SecDataFromLabelVG1J class"""

    def test_class(self):
        self.assertIsInstance(ov1, PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel)
        self.assertIsInstance(ov1, PDSPPIVoyagerPRADataFromLabel)
        self.assertIsInstance(ov1, PDSDataFromLabel)
        self.assertIsInstance(ov1, MaserDataFromFile)

    def test_label(self):
        self.assertEqual(ov1.file, ov1.file.replace('.TAB', '.LBL'))
        self.assertIsInstance(ov1.label, PDSLabelDict)

    def test_object(self):
        self.assertIsInstance(ov1.object, dict)
        self.assertIn('TABLE', ov1.objects)
        self.assertIn('TABLE', ov1.object.keys())
        self.assertIsInstance(ov1.object['TABLE'], PDSPPIVoyagerPRADataObject)
        self.assertEqual(ov1.dataset_name, 'VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1.0')

    def test_frequency(self):
        freq_table1 = ov1.get_freq_axis()
        self.assertListEqual(list(freq_table1), list(ov1.frequency))

    def test_data(self):
        self.assertFalse(ov1.load_data_flag['TABLE'])
        self.assertFalse(ov1.object['TABLE'].data_loaded)
        ov1.load_data('TABLE')
        self.assertTrue(ov1.load_data_flag['TABLE'])
        self.assertTrue(ov1.object['TABLE'].data_loaded)
        self.assertEqual(len(ov1.get_first_sweep().data), 2)
        self.assertEqual(len(ov1.get_first_sweep().raw_sweep), 71)
        self.assertEqual(set(ov1.get_first_sweep().data.keys()), {'R', 'L'})
        self.assertEqual(set(ov1.get_first_sweep().freq.keys()), {'R', 'L', 'avg'})
        self.assertListEqual(list(ov1.get_first_sweep().raw_sweep), list(ov1.object['TABLE'].data['SWEEP1'][0]))
        self.assertListEqual(list(ov1.get_single_sweep(1).raw_sweep), list(ov1.object['TABLE'].data['SWEEP2'][0]))
        self.assertListEqual(list(ov1.get_single_sweep(8).raw_sweep), list(ov1.object['TABLE'].data['SWEEP1'][1]))
        self.assertEqual(ov1.get_first_sweep().data['R'][0], ov1.object['TABLE'].data['SWEEP1'][0][1])
        self.assertEqual(ov1.get_first_sweep().data['L'][0], ov1.object['TABLE'].data['SWEEP1'][0][2])

    def test_times(self):
        self.assertEqual(ov1a.start_time, datetime.datetime(1979, 1, 6, 0, 0, 34))
        self.assertEqual(ov1a.end_time, datetime.datetime(1979, 1, 30, 23, 59, 47))
        time_table1 = ov1a.get_time_axis()
        self.assertEqual(len(time_table1), 284552)
        self.assertEqual(time_table1[0], datetime.datetime(1979, 1, 6, 0, 0, 37, 900000))
        self.assertEqual(time_table1[-1], datetime.datetime(1979, 1, 31, 0, 0, 32, 900000))


class PDSPPIVoyagerPRARDRLowBand6SecDataFromLabelVG1S(unittest.TestCase):
    """Test case for PDSPPIVoyagerPRARDRLowBand6SecDataFromLabelVG1S class"""

    def test_class(self):

        self.assertIsInstance(ov3, PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel)
        self.assertIsInstance(ov3, PDSPPIVoyagerPRADataFromLabel)
        self.assertIsInstance(ov3, PDSDataFromLabel)
        self.assertIsInstance(ov3, MaserDataFromFile)

    def test_label(self):
        self.assertEqual(ov3.file, ov3.file.replace('.TAB', '.LBL'))
        self.assertIsInstance(ov3.label, PDSLabelDict)

    def test_object(self):
        self.assertIsInstance(ov3.object, dict)
        self.assertIn('TABLE', ov3.objects)
        self.assertIn('TABLE', ov3.object.keys())
        self.assertIsInstance(ov3.object['TABLE'], PDSPPIVoyagerPRADataObject)
        self.assertEqual(ov3.dataset_name, 'VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1.0')

    def test_frequency(self):
        freq_table3 = ov3.get_freq_axis()
        self.assertListEqual(list(freq_table3), list(ov3.frequency))

    def test_times(self):
        self.assertEqual(ov3.start_time, datetime.datetime(1980, 11, 11, 22, 9, 23))
        self.assertEqual(ov3.end_time, datetime.datetime(1980, 11, 16, 23, 59, 47))
        time_table3 = ov3.get_time_axis()
        self.assertEqual(len(time_table3), 49824)
        self.assertEqual(time_table3[0], datetime.datetime(1980, 11, 11, 22, 9, 26, 900000))
        self.assertEqual(time_table3[-1], datetime.datetime(1980, 11, 17, 0, 0, 32, 900000))

    def test_data(self):
        self.assertEqual(len(ov3.get_first_sweep().data), 2)
        self.assertEqual(len(ov3.get_first_sweep().raw_sweep), 71)
        self.assertEqual(set(ov3.get_first_sweep().data.keys()), {'R', 'L'})
        self.assertEqual(set(ov3.get_first_sweep().freq.keys()), {'R', 'L', 'avg'})
        self.assertListEqual(list(ov3.get_first_sweep().raw_sweep), list(ov3.object['TABLE'].data['SWEEP1'][0]))
        self.assertListEqual(list(ov3.get_single_sweep(1).raw_sweep), list(ov3.object['TABLE'].data['SWEEP2'][0]))
        self.assertListEqual(list(ov3.get_single_sweep(8).raw_sweep), list(ov3.object['TABLE'].data['SWEEP1'][1]))
        self.assertEqual(ov3.get_first_sweep().data['R'][0], ov3.object['TABLE'].data['SWEEP1'][0][1])
        self.assertEqual(ov3.get_first_sweep().data['L'][0], ov3.object['TABLE'].data['SWEEP1'][0][2])


class PDSPPIVoyagerPRARDRLowBand6SecDataFromLabelVG2N(unittest.TestCase):
    """Test case for PDSPPIVoyagerPRARDRLowBand6SecDataFromLabelVG2N class"""

    def test_class(self):

        self.assertIsInstance(ov5, PDSPPIVoyagerPRARDRLowBand6SecDataFromLabel)
        self.assertIsInstance(ov5, PDSPPIVoyagerPRADataFromLabel)
        self.assertIsInstance(ov5, PDSDataFromLabel)
        self.assertIsInstance(ov5, MaserDataFromFile)

    def test_label(self):
        self.assertEqual(ov5.file, ov5.file.replace('.TAB', '.LBL'))
        self.assertIsInstance(ov5.label, PDSLabelDict)

    def test_object(self):
        self.assertIsInstance(ov5.object, dict)
        self.assertIn('TABLE', ov5.objects)
        self.assertIn('TABLE', ov5.object.keys())
        self.assertIsInstance(ov5.object['TABLE'], PDSPPIVoyagerPRADataObject)
        self.assertEqual(ov5.dataset_name, 'VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1.0')

    def test_frequency(self):
        freq_table5 = ov5.get_freq_axis()
        self.assertListEqual(list(freq_table5), list(ov5.frequency))

    def test_times(self):
        self.assertEqual(ov5.start_time, datetime.datetime(1989, 8, 11, 0, 0))
        self.assertEqual(ov5.end_time, datetime.datetime(1989, 8, 31, 0, 0))
        time_table5 = ov5.get_time_axis()
        self.assertEqual(len(time_table5), 288224)
        self.assertEqual(time_table5[0], datetime.datetime(1989, 8, 11, 0, 0, 3, 900000))
        self.assertEqual(time_table5[-1], datetime.datetime(1989, 8, 31, 23, 59, 55, 900000))

    def test_data(self):
        self.assertEqual(len(ov5.get_first_sweep().data), 2)
        self.assertEqual(len(ov5.get_first_sweep().raw_sweep), 71)
        self.assertEqual(set(ov5.get_first_sweep().data.keys()), {'R', 'L'})
        self.assertEqual(set(ov5.get_first_sweep().freq.keys()), {'R', 'L', 'avg'})
        self.assertListEqual(list(ov5.get_first_sweep().raw_sweep), list(ov5.object['TABLE'].data['SWEEP1'][0]))
        self.assertListEqual(list(ov5.get_single_sweep(1).raw_sweep), list(ov5.object['TABLE'].data['SWEEP2'][0]))
        self.assertListEqual(list(ov5.get_single_sweep(8).raw_sweep), list(ov5.object['TABLE'].data['SWEEP1'][1]))
        self.assertEqual(ov5.get_first_sweep().data['R'][0], ov5.object['TABLE'].data['SWEEP1'][0][1])
        self.assertEqual(ov5.get_first_sweep().data['L'][0], ov5.object['TABLE'].data['SWEEP1'][0][2])
