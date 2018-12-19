import datetime
import os
import unittest

import numpy

from pathlib import Path
from maser.data import MaserDataFromFile
from maser.data.padc.lesia.cassini.kronos import CassiniKronosData, CassiniKronosLevel, CassiniKronosFile, \
    CassiniKronosRecords, CassiniKronosSweeps, load_data_from_file, load_data_from_interval, ydh_to_datetime
from maser.data.tests import load_test_data, get_data_directory

load_test_data("kronos")

os.environ['NAS_RPWS'] = str(get_data_directory() / 'kronos')
rpws_root_path = Path(os.environ['NAS_RPWS'])

verbose = False


class StaticFunctionTest(unittest.TestCase):

    """ Test case for static functions"""

    def test_from_file_result_class(self):
        input_file = rpws_root_path / '2012_181_270' / 'n2' / 'P2012181.00'
        self.assertIsInstance(load_data_from_file(str(input_file)), CassiniKronosData)

    def test_from_interval_result_class(self):
        self.assertIsInstance(load_data_from_interval(ydh_to_datetime("2012181.00"),
                                                      ydh_to_datetime("2012182.00"), 'n2'), CassiniKronosData)

    def ydh_to_datetime(self):
        self.assertEqual(ydh_to_datetime("2012181.23"), datetime.datetime(2012, 6, 29, 23, 0, 0))


class CassiniKronosLevelClassTest(unittest.TestCase):

    """Test case for CassiniKronosLevel class"""

    def test_level_name(self):
        levels = ['k', 'n1', 'n2', 'n3b', 'n3c']
        for item in levels:
            level = CassiniKronosLevel(item)
            self.assertEqual(level.name, item)

    def test_level_rec_length(self):
        levels = ['n1', 'n2', 'n3b', 'n3c']
        length = {'n1':28, 'n2':45, 'n3b':72, 'n3c':68}
        for item in levels:
            level = CassiniKronosLevel(item)
            self.assertEqual(level.record_def['length'], length[item])


class CassiniKronosDataClassTest(unittest.TestCase):

    """Test case for CassiniKronosData class"""

    # def test_init(self):
        # data = CassiniKronosData()
        # self.assertIsInstance(data.levels, list)
        # self.assertIsNone(data.start_time)
        # self.assertIsNone(data.end_time)

    def test_rpws_data_dir(self):
        data = CassiniKronosData()
        self.assertEqual(data.root_data_dir, str(rpws_root_path))

    def test_print(self):
        data = CassiniKronosData.from_file(str(rpws_root_path / '2012_181_270' / 'n2' / 'P2012181.00'))
        self.assertEqual(str(data),
                         '<CassiniKronosData object> 2012-06-29T00:00:00 to 2012-06-29T01:00:00 with level n2')

    def test_init_from_file(self):
        data = CassiniKronosData.from_file(str(rpws_root_path / '2012_181_270' / 'n2' / 'P2012181.00'), verbose=verbose)
        self.assertIsInstance(data, CassiniKronosData)
        self.assertEqual(data.start_time, datetime.datetime(2012, 6, 29, 0, 0, 0))
        self.assertEqual(data.end_time, datetime.datetime(2012, 6, 29, 1, 0, 0))
        self.assertEqual(data.level.name, 'n2')
        self.assertEqual(data.dataset_name, 'Cassini/RPWS/HFR Level 2 (Physical units)')
        self.assertEqual(len(data.data['n2']), 78262)
        self.assertEqual(len(data['t97']), 78262)
        self.assertEqual(data.data['n2'][10000]['t97'], data['t97'][10000])
        self.assertEqual(data['datetime'][0], datetime.datetime(2012, 6, 29, 0, 0, 1, 230000))
        self.assertEqual(data['datetime'][78261], datetime.datetime(2012, 6, 29, 0, 59, 45, 210000))

    def test_init_from_interval_ydh(self):
        data = CassiniKronosData.from_interval(ydh_to_datetime('2012181.00'),
                                               ydh_to_datetime('2012182.00'), 'n2', verbose=verbose)
        self.assertIsInstance(data, CassiniKronosData)
        self.assertEqual(len(data), 1730845)
        self.assertEqual(data.start_time, datetime.datetime(2012, 6, 29, 0, 0, 0))
        self.assertEqual(data.end_time, datetime.datetime(2012, 6, 30, 0, 0, 0))

    def test_init_from_interval_datetime(self):
        data = CassiniKronosData.from_interval(datetime.datetime(2012, 6, 29, 0, 0, 0),
                                               datetime.datetime(2012, 6, 30, 0, 0, 0), 'n2', verbose=verbose)
        self.assertIsInstance(data, CassiniKronosData)
        self.assertEqual(len(data), 1730845)
        self.assertEqual(data.start_time, datetime.datetime(2012, 6, 29, 0, 0, 0))
        self.assertEqual(data.end_time, datetime.datetime(2012, 6, 30, 0, 0, 0))

    def test_init_from_interval_multiple_period(self):
        data = CassiniKronosData.from_interval(datetime.datetime(2012, 6, 28, 23, 0, 0),
                                               datetime.datetime(2012, 6, 29, 2, 0, 0), 'n2', verbose=verbose)
        self.assertIsInstance(data, CassiniKronosData)
        self.assertEqual(len(data), 156883)
        self.assertEqual(data.start_time, datetime.datetime(2012, 6, 28, 23, 0, 0))
        self.assertEqual(data.end_time, datetime.datetime(2012, 6, 29, 2, 0, 0))
        #self.assertEqual(data['datetime'][0], datetime.datetime(2012, 6, 28, 23, 0, 1, 230000))
        self.assertEqual(data.periods, ['2012_091_180', '2012_181_270'])

            #    def test_load_extra_level(self):
#        data = CassiniKronosData.from_interval(ydh_to_datetime('2012181.00'), ydh_to_datetime('2012182.00'), 'n2',
#                                               verbose=verbose)
#        data.load_extra_level('n1')
#        level_list = [item.name for item in data.dataset_name]
#        self.assertEqual(level_list.sort(), ['n1', 'n2'].sort())

    def test_file_list(self):
        data = CassiniKronosData.from_file(str(rpws_root_path / '2012_181_270' / 'n2' / 'P2012181.00'))
        self.assertIsInstance(data.files, list)
        self.assertEqual(data.files[0].level.name, 'n2')
        self.assertIsInstance(data.files[0], CassiniKronosFile)
        self.assertEqual(data.files[0].get_file_name(), 'P2012181.00')

#    def test_level_path(self):
#        data = CassiniKronosData.from_file(rpws_root_path+'2012_181_270/n2/P2012181.00')
#        self.assertEqual(data.level_path(data.periods[0], data.dataset_name[0]), rpws_root_path+'2012_181_270/n2')

    def test_period(self):
        data = CassiniKronosData.from_file(str(rpws_root_path / '2012_181_270' / 'n2' / 'P2012181.00'))
        self.assertEqual(data.periods[0], '2012_181_270')

    def test_modes_from_file(self):
        data = CassiniKronosData.from_file(str(rpws_root_path / '2012_181_270' / 'n2' / 'P2012181.00'))
        modes = data.get_modes()
        self.assertEqual(len(modes.keys()), 1)
        self.assertEqual(list(modes.keys())[0], '41bc04a0e85e944f068c86e438700a05')

    def test_modes_from_interval(self):
        data = CassiniKronosData.from_interval(ydh_to_datetime('2012180.23'),
                                               ydh_to_datetime('2012181.01'), 'n2', verbose=verbose)
        modes = data.get_modes()
        self.assertEqual(len(modes.keys()), 1)
        self.assertEqual(list(modes.keys())[0], '41bc04a0e85e944f068c86e438700a05')

    def test_n3b_with_data(self):
        data = CassiniKronosData.from_file(str(rpws_root_path / '2012_181_270' / 'n3b' / 'N3b_dsq2012181.18'))
        self.assertIn('n1', list(data.data.keys()))
        self.assertIn('n2', list(data.data.keys()))
        self.assertIn('n3b', list(data.data.keys()))
        self.assertEqual(len(data), 52658)
        self.assertEqual(data['datetime'][0], datetime.datetime(2012, 6, 29, 18, 0, 6, 200000))

    def test_n3b_without_data(self):
        data = CassiniKronosData.from_file(str(rpws_root_path / '2012_181_270' / 'n3b' / 'N3b_dsq2012181.00'))
        self.assertIn('n1', list(data.data.keys()))
        self.assertIn('n2', list(data.data.keys()))
        self.assertIn('n3b', list(data.data.keys()))
        self.assertEqual(len(data), 0)

    def test_n3e_data(self):
        data = CassiniKronosData.from_file(str(rpws_root_path / '2012_181_270' / 'n3e' / 'N3e_dsq2012181.00'))
        self.assertIn('n1', list(data.data.keys()))
        self.assertIn('n2', list(data.data.keys()))
        self.assertIn('n3e', list(data.data.keys()))
        self.assertEqual(len(data), 47088)
        self.assertEqual(data['num'][1], 1)


class CassiniKronosFileClassTest(unittest.TestCase):

    """Test case for CassiniKronosFile class"""

    def test_inherited_class(self):
        file = CassiniKronosFile(str(rpws_root_path / '2012_181_270' / 'n1' / 'R2012181.00'))
        self.assertIsInstance(file, MaserDataFromFile)

    def test_file_k(self):
        file = CassiniKronosFile(str(rpws_root_path / '2012_181_270' / 'k' / 'K2012181.00'))
        self.assertEqual(file.level.name, 'k')
        self.assertEqual(file.level.sublevel, '')
        self.assertFalse(file.level.implemented)

    def test_file_n1(self):
        file = CassiniKronosFile(str(rpws_root_path / '2012_181_270' / 'n1' / 'R2012181.00'))
        self.assertEqual(file.level.name, 'n1')
        self.assertEqual(file.level.sublevel, '')
        self.assertEqual(file.start_time, datetime.datetime(2012, 6, 29, 0, 0, 0))
        self.assertEqual(file.end_time, datetime.datetime(2012, 6, 29, 1, 0, 0))

    def test_file_n2(self):
        file = CassiniKronosFile(str(rpws_root_path / '2012_181_270' / 'n2' / 'P2012181.23'))
        self.assertEqual(file.level.name, 'n2')
        self.assertEqual(file.level.sublevel, '')
        self.assertEqual(file.start_time, datetime.datetime(2012, 6, 29, 23, 0, 0))
        self.assertEqual(file.end_time, datetime.datetime(2012, 6, 30, 0, 0, 0))

    def test_file_n3b(self):
        file = CassiniKronosFile(str(rpws_root_path / '2012_181_270' / 'n3b' / 'N3b_dsq2012181.00'))
        self.assertEqual(file.level.name, 'n3b')
        self.assertEqual(file.level.sublevel, 'dsq')

    def test_read_data_binary(self):
        file = CassiniKronosFile(str(rpws_root_path / '2012_181_270' / 'n2' / 'P2012181.23'))
        data = file.read_data_binary()
        self.assertIsInstance(data, numpy.ndarray)
        self.assertIsInstance(data[0], numpy.void)
        self.assertEqual(data[0]['t97'], 5659.958341550926)
        self.assertEqual(len(data), file.get_file_size() // file.level.record_def['length'])

    def test_period(self):
        file = CassiniKronosFile(str(rpws_root_path / '2012_181_270' / 'n2' / 'P2012181.23'))
        self.assertEqual(file.period(), '2012_181_270')


class CassiniKronosRecordsClassTest(unittest.TestCase):

    """Test case for CassiniKronosRecords class"""

    def test_iterator(self):
        o = CassiniKronosData.from_file(str(rpws_root_path / '2012_181_270' / 'n2' / 'P2012181.00'), verbose=verbose)
        records = o.records()
        self.assertIsInstance(records, CassiniKronosRecords)
        t, f, d = next(records)
        self.assertEqual(t, datetime.datetime(2012, 6, 29, 0, 0, 1, 230000))
        self.assertAlmostEqual(f, 3.8629999)
        self.assertEqual(d['n1']['auto1'], 194)
        self.assertEqual(d['n2']['f'], f)
        self.assertEqual(d['n1']['fi'], 3201)
        t, f, d = next(records)
        self.assertEqual(t, datetime.datetime(2012, 6, 29, 0, 0, 1, 230000))
        self.assertAlmostEqual(f, 4.0489001)
        self.assertEqual(d['n1']['auto1'], 188)
        self.assertEqual(d['n2']['f'], f)
        self.assertEqual(d['n1']['fi'], 3202)


class CassiniKronosSweepsClassTest(unittest.TestCase):

    """Test case for CassiniKronosRecords class"""

    def test_iterator(self):
        o = CassiniKronosData.from_file(str(rpws_root_path / '2012_181_270' / 'n2' / 'P2012181.00'), verbose=verbose)
        sweeps = o.sweeps()
        self.assertIsInstance(sweeps, CassiniKronosSweeps)
        t, d = next(sweeps)
        self.assertEqual(t, datetime.datetime(2012, 6, 29, 0, 0, 17, 230000))
        self.assertEqual(len(d['n2']), 359)
        self.assertAlmostEqual(d['n2'][0]['f'], 3.6856)
        self.assertAlmostEqual(d['n2'][0]['crossR'], 0.12749861)
        self.assertEqual(d['n1'][0]['auto1'], 201)
        self.assertEqual(d['n1'][0]['fi'], 3200)
        hh = sweeps.get_mode_hash()
        self.assertEqual(hh, '41bc04a0e85e944f068c86e438700a05')
        t, d = next(sweeps)
        self.assertEqual(t, datetime.datetime(2012, 6, 29, 0, 0, 33, 230000))
        self.assertEqual(len(d['n2']), 359)
        self.assertAlmostEqual(d['n2'][0]['f'], 3.6856)
        self.assertAlmostEqual(d['n2'][0]['crossR'], 0.13842489)
        self.assertEqual(d['n1'][0]['auto1'], 204)
        self.assertEqual(d['n1'][0]['fi'], 3200)
