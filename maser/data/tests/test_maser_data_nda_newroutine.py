import unittest
import datetime
from maser.data.tests import load_test_data, get_data_directory
from maser.data.nancay.nda import NDADataECube
from maser.data.nancay.nda.newroutine import NDANewRoutineData

load_test_data("nda")
file_path = get_data_directory() / "nda" / "newroutine" / "J20170101_022612_Rou.dat"

rou = NDANewRoutineData(str(file_path))
sweep_first = rou.get_first_ecube()
sweep_last = rou.get_last_ecube()
sweep_100 = rou.get_single_ecube(100)
sweep_101 = rou.get_single_ecube(101, load_data=False)


class NDANewRoutineDataClass(unittest.TestCase):

    """Test case for NDARoutineData class"""

    def test_dataset_name(self):
        self.assertEqual(rou.name, "SRN/NDA NewRoutine Dataset")

    def test_filedate(self):
        self.assertEqual(rou.file_info['filedate'], "20170101")

    def test_len(self):
        self.assertEqual(len(rou), 58188)

    def test_format(self):
        self.assertEqual(rou.file_info['format'], 'DAT')

    def test_get_time_axis(self):
        t = rou.get_time_axis()
        self.assertEqual(len(t), len(rou))
        self.assertEqual(t[0], datetime.datetime(2017, 1, 1, 2, 26, 14, 261199))
        self.assertEqual(t[-1], datetime.datetime(2017, 1, 1, 10, 26, 0, 235901))

    def test_get_freq_axis(self):
        f = rou.get_freq_axis()
        self.assertEqual(len(f), 2048)
        self.assertEqual(f[0], 0.)
        self.assertEqual(f[-1], 99.951171875)


class NDANewRoutineSweep(unittest.TestCase):

    """Test Case for NDARoutineSweep class"""

    def test_class(self):
        self.assertIsInstance(sweep_first, NDADataECube)
        self.assertIsInstance(sweep_last, NDADataECube)
        self.assertIsInstance(sweep_100, NDADataECube)

    def test_index(self):
        self.assertEqual(sweep_first.index, 0)
        self.assertEqual(sweep_last.index, -1)
        self.assertEqual(sweep_100.index, 100)

    def test_get_datetime(self):
        self.assertEqual(sweep_first.get_datetime(), datetime.datetime(2017, 1, 1, 2, 26, 14, 261199))
        self.assertEqual(sweep_last.get_datetime(), datetime.datetime(2017, 1, 1, 10, 26, 0, 235901))
        self.assertEqual(sweep_100.get_datetime(), datetime.datetime(2017, 1, 1, 2, 27, 3, 732667))

    def test_data(self):
        self.assertIsInstance(sweep_first.data, dict)
        self.assertIn('corr', sweep_first.data.keys())

    def test_load_data(self):
        self.assertEqual(len(sweep_100.data['corr']), 4)
        self.assertEqual(len(sweep_100.data['corr'][0]['data']), 2048)
        self.assertEqual(len(sweep_101.data['corr']), 4)
        self.assertEqual(len(sweep_101.data['corr'][0]['data']), 0)
