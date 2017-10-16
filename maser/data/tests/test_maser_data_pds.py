import unittest
import datetime
from maser.data.data import *
from maser.data.pds.ppi.voyager.pra import *

root_data_path = 'data/'
file = root_data_path + 'VG1_JUPITER/PRA_I/PRA_I.TAB'


class PDSPPIVoyagerPRAJupiterDataTest(unittest.TestCase):

    """Test case for PDS Jupiter Voyager PRA-LB"""

    def test_class(self):
        obj = PDSPPIVoyagerPRAJupiterData("1979-01-06T00:00:00", "1979-01-06T01:00:00", 1, root_data_path=root_data_path)
        self.assertIsInstance(obj, MaserDataFromInterval)
        self.assertEqual(obj.data_path, root_data_path+'VG1_JUPITER')

    def test_get_frame_times(self):
        frame_times = PDSPPIVoyagerPRAJupiterData.get_frame_times(file)
        self.assertEqual(frame_times[0], datetime.datetime(1979, 1, 6, 0, 0, 34))
        self.assertEqual(frame_times[-1], datetime.datetime(1979, 1, 30, 23, 59, 47))
        self.assertEqual(len(frame_times), 35569)

    def test_get_freq_list(self):
        frequency = PDSPPIVoyagerPRAJupiterData.get_freq_list()
        self.assertEqual(frequency[0], 1326)
        self.assertAlmostEqual(frequency[-1], 1.2)
        self.assertEqual(len(frequency), 70)

    def test_load_data_frames(self):
        frames = PDSPPIVoyagerPRAJupiterData.load_data_frames(file, 1, 2)
        self.assertEqual(len(frames), 8)
        self.assertEqual(frames[0]['datetime'], datetime.datetime(1979, 1, 6, 0, 1, 22))
        self.assertEqual(frames[1]['datetime'], datetime.datetime(1979, 1, 6, 0, 1, 28))
        self.assertEqual(frames[7]['datetime'], datetime.datetime(1979, 1, 6, 0, 2, 4))

    def test_data_content(self):
        obj = PDSPPIVoyagerPRAJupiterData("1979-01-06T00:00:00", "1979-01-06T01:00:00", 1, root_data_path=root_data_path)
        self.assertEqual(len(obj), 528)
        self.assertEqual(obj['datetime'][0], datetime.datetime(1979, 1, 6, 0, 1, 22))
        self.assertEqual(obj['datetime'][-1], datetime.datetime(1979, 1, 6, 0, 59, 40))
        self.assertEqual(obj['data'][0][0], 2730)

    def test_get_polar_data(self):
        obj = PDSPPIVoyagerPRAJupiterData("1979-01-06T00:00:00", "1979-01-06T01:00:00", 1, root_data_path=root_data_path)
        data = obj.get_polar_data('R')
        self.assertEqual(data[0]['polar'], 'R')