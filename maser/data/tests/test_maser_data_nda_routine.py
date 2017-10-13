import unittest
import datetime
import os
from maser.data.data import *
from maser.data.nancay.nda.routine import *

test_file = 'data/nda/J160131.RT1'
rou = NDARoutineData(test_file)


class NancayNDARoutineDataClass(unittest.TestCase):

    """Test case for NDARoutineData class"""

    def test_dataset_name(self):
        self.assertEqual(rou.name, "SRN/NDA Routine Dataset")

    def test_filedate(self):
        self.assertEqual(rou.file_info['filedate'], "20160131")

    def test_len(self):
        self.assertEqual(len(rou), 57469)

    def test_format(self):
        self.assertEqual(rou.file_info['format'], 'RT1')

    def test_header_version(self):
        self.assertEqual(rou.file_info['header_version'], 6)

    def test_meridian(self):
        self.assertEqual(rou.get_meridian_datetime(), datetime.datetime(2016, 1, 31, 2, 46))
        self.assertEqual(rou.get_meridian_time(), datetime.time(2, 46))

    def test_get_single_sweep(self):
        sweep = rou.get_single_sweep(0)
        self.assertIsInstance(sweep, NDARoutineSweep)

    def test_get_freq_axis(self):
        f = rou.get_freq_axis()
        self.assertEqual(len(f), 400)
        self.assertEqual(f[0], 10)
        self.assertEqual(f[-1], 39.925)

    def test_get_time_axis(self):
        t = rou.get_time_axis()
        self.assertEqual(len(t), 57469)
        self.assertEqual(t[0], datetime.datetime(2016, 1, 30, 22, 47, 6, 30000))
        self.assertEqual(t[-1], datetime.datetime(2016, 1, 31, 6, 45, 59, 680000))

    def test_get_first_sweep(self):
        sweep = rou.get_first_sweep()
        self.assertEqual(sweep.index, 0)

    def test_get_last_sweep(self):
        sweep = rou.get_last_sweep()
        self.assertEqual(sweep.index, 57468)

    def test_get_start_date(self):
        self.assertEqual(rou.get_start_date(), datetime.date(2016, 1, 30))


class NancayNDARoutineSweepClass(unittest.TestCase):

    """Test case for NDARoutineSweep class"""

    def test_polar(self):
        sweep = NDARoutineSweep(rou, 0)
        self.assertEqual(sweep.data['polar'], 'LH')
        sweep = NDARoutineSweep(rou, 1)
        self.assertEqual(sweep.data['polar'], 'RH')
        sweep = NDARoutineSweep(rou, 1234)
        self.assertEqual(sweep.data['polar'], 'LH')
        sweep = NDARoutineSweep(rou, 2345)
        self.assertEqual(sweep.data['polar'], 'RH')

    def test_load_data(self):
        sweep = NDARoutineSweep(rou, 0, False)
        self.assertEqual(len(sweep.data['data']), 0)
        sweep.load_data()
        self.assertEqual(len(sweep.data['data']), 400)

    def test_get_data(self):
        sweep = NDARoutineSweep(rou, 0)
        direct = sweep.data['data']
        method = sweep.get_data()
        self.assertEqual(direct, method)
        self.assertEqual(direct[0], 32)
        self.assertEqual(direct[399], 69)

    def test_get_data_in_db(self):
        sweep = NDARoutineSweep(rou, 0)
        data = sweep.get_data_in_db()
        self.assertEqual(data[0], 10.0)

    def test_get_time(self):
        sweep = NDARoutineSweep(rou, 0)
        self.assertEqual(sweep.get_time(), datetime.time(22, 47, 6, 30000))
        self.assertEqual(sweep.get_time().hour, sweep.data['hms']['hr'])
        self.assertEqual(sweep.get_time().minute, sweep.data['hms']['min'])
        self.assertEqual(sweep.get_time().second, sweep.data['hms']['sec'])
        self.assertEqual(sweep.get_time().microsecond, sweep.data['hms']['cs'] * 10000)

    def test_get_datetime(self):
        sweep = rou.get_first_sweep()
        self.assertEqual(sweep.get_datetime(), datetime.datetime(2016, 1, 30, 22, 47, 6, 30000))
        sweep = rou.get_last_sweep()
        self.assertEqual(sweep.get_datetime(), datetime.datetime(2016, 1, 31, 6, 45, 59, 680000))