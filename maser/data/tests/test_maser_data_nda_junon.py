import unittest
import datetime
from maser.data.tests import load_test_data, get_data_directory
from maser.data.nancay.nda import NDADataECube
from maser.data.nancay.nda.junon import NDAJunonData

load_test_data("nda")
file_path = get_data_directory() / "nda" / "junon" / "20180223_034242_extract1.dat"

o = NDAJunonData(str(file_path))

sweep_first = o.get_first_ecube()
sweep_last = o.get_last_ecube()
sweep_100 = o.get_single_ecube(100)
sweep_101 = o.get_single_ecube(101, load_data=False)


class NDAJunonDataClass(unittest.TestCase):

    """Test case for NDARoutineData class"""

    def test_dataset_name(self):
        self.assertEqual(o.name, "SRN/NDA JunoN Dataset")

    def test_len(self):
        self.assertEqual(len(o), 128)

    def test_format(self):
        self.assertEqual(o.file_info['format'], 'DAT')

    def test_get_time_axis(self):
        t = o.get_time_axis()
        self.assertEqual(len(t), len(o))
        self.assertEqual(t[0], datetime.datetime(2018, 2, 23, 3, 42, 42, 963809))
        self.assertEqual(t[-1], datetime.datetime(2018, 2, 23, 3, 42, 53, 617342))

    def test_get_freq_axis(self):
        f = o.get_freq_axis()
        self.assertEqual(len(f), 3072)
        self.assertEqual(f[0], 6.25457763671875)
        self.assertEqual(f[-1], 43.74237060546875)


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
        self.assertEqual(sweep_first.get_datetime(), datetime.datetime(2018, 2, 23, 3, 42, 42, 963809))
        self.assertEqual(sweep_last.get_datetime(), datetime.datetime(2018, 2, 23, 3, 42, 53, 617342))
        self.assertEqual(sweep_100.get_datetime(), datetime.datetime(2018, 2, 23, 3, 42, 51, 352458))

    def test_data(self):
        self.assertIsInstance(sweep_first.data, dict)
        self.assertIn('corr', sweep_first.data.keys())

    def test_load_data(self):
        self.assertEqual(len(sweep_100.data['corr']), 4)
        self.assertEqual(len(sweep_100.data['corr'][0]['data']), 3072)
        self.assertEqual(len(sweep_101.data['corr']), 4)
        self.assertEqual(len(sweep_101.data['corr'][0]['data']), 0)
