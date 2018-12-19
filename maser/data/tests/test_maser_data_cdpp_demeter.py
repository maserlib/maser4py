import unittest
import datetime
from maser.data import MaserDataSweep
from maser.data.tests import load_test_data, get_data_directory
from maser.data.cdpp import CDPPDataFromFile
from maser.data.cdpp.demeter.ice import CDPPDemeterN11134Data, read_dmt_n1_1134

load_test_data("cdpp")
file_path = get_data_directory() / "cdpp" / "demeter" / "DMT_N1_1134_018401_20041105_235807_20041106_003155.DAT"


def load_demeter_ice():
    return read_dmt_n1_1134(str(file_path))


class CDPPDemeterN11134DataTest(unittest.TestCase):

    """Test case for CDPPDemeterN11134Data class"""

    def test_class(self):
        print("### Testing CDPPDemeterN11134Data class")
        a = load_demeter_ice()
        self.assertIsInstance(a, CDPPDataFromFile)

    def test_name(self):
        print("### Testing CDPPDemeterN11134Data name variable")
        a = load_demeter_ice()
        self.assertEqual(a.name, "DMT_N1_1134")

    def test_len(self):
        print("### Testing CDPPDemeterN11134Data len() method")
        a = load_demeter_ice()
        self.assertEqual(len(a), 496)

    def test_keys(self):
        print("### Testing CDPPDemeterN11134Data keys() method")
        a = load_demeter_ice()
        expected_list = ['BLOCK_2', 'BLOCK_4', 'BLOCK_1', 'BLOCK_3', 'DATETIME', 'POWER']
        self.assertCountEqual(a.keys(), expected_list)

    def test_datetime(self):
        print("### Testing CDPPDemeterN11134Data get_time_axis() method")
        a = load_demeter_ice()
        dt = a.get_time_axis()
        self.assertEqual(dt[0], datetime.datetime(2004, 11, 5, 23, 58, 6, 559000))

    def test_frequency(self):
        print("### Testing CDPPDemeterN11134Data get_frequency() method")
        a = load_demeter_ice()
        f = a.get_frequency()
        self.assertAlmostEqual(f[0], 3.255, 5)
        self.assertAlmostEqual(len(f), a.header[0]['BLOCK_4']['NBF'])

    def test_get_single_sweep(self):
        print("### Testing CDPPDemeterN11134Data get_single_sweep() method")
        a = load_demeter_ice()
        s = a.get_single_sweep(0)
        self.assertIsInstance(s, MaserDataSweep)