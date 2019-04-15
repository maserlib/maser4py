import unittest
import datetime
from maser.data import MaserDataSweep
from maser.data.tests import load_test_data, get_data_directory
from maser.data.cdpp import CDPPDataFromFile
from maser.data.cdpp.interball.polrad import CDPPInterballAuroralPOLRADRSPData, read_int_aur_polrad

load_test_data("cdpp")
file_path = get_data_directory() / "cdpp" / "interball" / "POLR_RSPN2_19990126"


def load_polrad():
    return read_int_aur_polrad(str(file_path))


class CDPPInterballAuroralPOLRADRSPDataTest(unittest.TestCase):

    """Test case for CDPPInterballAuroralPOLRADRSPData class"""

    def test_class(self):
        print("### Testing CDPPInterballAuroralPOLRADRSPData class")
        a = load_polrad()
        self.assertIsInstance(a, CDPPDataFromFile)

    def test_name(self):
        print("### Testing CDPPInterballAuroralPOLRADRSPData name variable")
        a = load_polrad()
        self.assertEqual(a.name, "INT_AUR_POLRAD_RSP")

    def test_len(self):
        print("### Testing CDPPInterballAuroralPOLRADRSPData len() method")
        a = load_polrad()
        self.assertEqual(len(a), 367)

    def test_keys(self):
        print("### Testing CDPPInterballAuroralPOLRADRSPData keys() method")
        a = load_polrad()
        expected_list = ['CCSDS_JULIAN_DAY_B3', 'CCSDS_PREAMBLE', 'SWEEP_DURATION', 'SESSION_NAME', 'ATTENUATION',
                         'FIRST_FREQ', 'CCSDS_MILLISECONDS_OF_DAY_B0', 'CCSDS_MILLISECONDS_OF_DAY_B1',
                         'CCSDS_MILLISECONDS_OF_DAY_B2', 'CCSDS_MILLISECONDS_OF_DAY_B3', 'CCSDS_JULIAN_DAY_B2',
                         'STEPS', 'CHANNELS', 'T_Field', 'P_Field', 'CSSDS_CDS_LEVEL_2_EPOCH',
                         'CCSDS_JULIAN_DAY_B1', 'DATETIME', 'EY', 'EZ', 'EX']
        self.assertCountEqual(a.keys(), expected_list)
        self.assertSetEqual(set(a.keys()), set(expected_list))

    def test_datetime(self):
        print("### Testing CDPPInterballAuroralPOLRADRSPData get_time_axis() method")
        a = load_polrad()
        dt = a.get_time_axis()
        self.assertEqual(dt[0], datetime.datetime(1999, 1, 26, 5, 6, 21, 394000))

    def test_frequency(self):
        print("### Testing CDPPInterballAuroralPOLRADRSPData get_frequency() method")
        a = load_polrad()
        f = a.get_frequency()
        self.assertAlmostEqual(f[0], 983.04, 5)
        self.assertAlmostEqual(len(f), a.header[0]['STEPS'])

    def test_get_single_sweep(self):
        print("### Testing CDPPInterballAuroralPOLRADRSPData get_single_sweep() method")
        a = load_polrad()
        s = a.get_single_sweep(0)
        self.assertIsInstance(s, MaserDataSweep)
        self.assertSetEqual(set(s.data.keys()), {'EX', 'EY', 'EZ'})
        self.assertEqual(len(s.data['EX']), 240)
        self.assertAlmostEqual(s.data['EX'][0], 6.211469825662024e-20)


