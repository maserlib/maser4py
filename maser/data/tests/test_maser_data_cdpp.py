import unittest
import datetime
from maser.data.tests import load_test_data, get_data_directory
from maser.data.cdpp import CDPPDataFromFile
from maser.data.cdpp.wind.waves import WindWavesData, read_wind_waves
from maser.data.cdpp.isee3.sbh import ISEE3SBHData, read_isee3_sbh_3d_radio_source

load_test_data("cdpp")


class CDPPDataTest(unittest.TestCase):
    """Test case for CDPPData class"""

    def test_cdpp_data_class(self):
        print("### Testing CDPPData class")
        header = {}
        data = {}
        test = CDPPDataFromFile("", header, data, "")
        self.assertIsInstance(test, CDPPDataFromFile)


def load_wind_waves_nn():
    file_path = get_data_directory() / "cdpp" / "wind" / "WI_WA_TNR_L3_NN_19941114_V02.DAT"
    return read_wind_waves(str(file_path))


def load_wind_waves_bqt():
    file_path = get_data_directory() / "cdpp" / "wind" / "WI_WA_TNR_L3_BQT_19941114_1MN.DAT"
    return read_wind_waves(str(file_path))


def load_wind_waves_radio_60s():
    file_path = get_data_directory() / "cdpp" / "wind" / "WIN_TNR_60S_19941114.B3E"
    return read_wind_waves(str(file_path))


def load_isee3_sbh_3d_radio_source():
    file_path = get_data_directory() / "cdpp" / "isee3" / "SBH_ISEE3_19780820"
    return read_isee3_sbh_3d_radio_source(str(file_path))


class WindWavesDataTest(unittest.TestCase):

    """Test case for WindWavesData class"""

    def test_cdpp_data_class(self):
        print("### Testing WindWavesData class")
        header = {}
        data = {}
        meta = {}
        name = "TEST"
        test = WindWavesData("", header, data, meta, name)
        self.assertIsInstance(test, CDPPDataFromFile)

    def test_wind_waves_nn_name(self):
        print("### Testing WindWavesData name variable on NN dataset")
        a = load_wind_waves_nn()
        self.assertEqual(a.name, "WIND_WAVES_TNR_L3_NN")

    def test_wind_waves_nn_len(self):
        print("### Testing WindWavesData len() method on NN dataset")
        a = load_wind_waves_nn()
        self.assertEqual(len(a), 38692)

    def test_wind_waves_nn_keys(self):
        print("### Testing WindWavesData keys() method on NN dataset")
        a = load_wind_waves_nn()
        expected_list = ['CCSDS_PREAMBLE', 'CCSDS_MILLISECONDS_OF_DAY', 'TNR_RECEIVER', 'UR8_TIME', 'CONNECTED_ANTENNA',
                         'CCSDS_JULIAN_DAY_B1', 'CCSDS_JULIAN_DAY_B3', 'CCSDS_JULIAN_DAY_B2', 'DATETIME', 'PLASMA_FREQ',
                         'ELEC_DENSITY']
        self.assertCountEqual(a.keys(), expected_list)

    def test_wind_waves_nn_datetime(self):
        print("### Testing WindWavesData \"DATETIME\" key on NN dataset")
        a = load_wind_waves_nn()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1994, 11, 14, 0, 0, 31, 885999))

    def test_wind_waves_bqt_name(self):
        print("### Testing WindWavesData name variable on BQT dataset")
        a = load_wind_waves_bqt()
        self.assertEqual(a.name, "WIND_WAVES_TNR_L3_BQT")

    def test_wind_waves_bqt_len(self):
        print("### Testing WindWavesData len() method on BQT dataset")
        a = load_wind_waves_bqt()
        self.assertEqual(len(a), 1366)

    def test_wind_waves_bqt_keys(self):
        print("### Testing WindWavesData keys() method on BQT dataset")
        a = load_wind_waves_bqt()
        expected_list = ['CCSDS_PREAMBLE', 'CCSDS_MILLISECONDS_OF_DAY', 'UR8_TIME', 'CCSDS_JULIAN_DAY_B1',
                         'CCSDS_JULIAN_DAY_B3', 'CCSDS_JULIAN_DAY_B2', 'DATETIME', 'COLD_ELECTRONS_TEMPERATURE',
                         'FIT_ACCUR_PARAM_3', 'ELECTRONIC_TEMPERATURE_RATIO', 'FIT_ACCUR_RMS', 'FIT_ACCUR_PARAM_1',
                         'FIT_ACCUR_PARAM_2', 'FIT_ACCUR_PARAM_8', 'SOLAR_WIND_VELOCITY', 'FIT_ACCUR_PARAM_7',
                         'PROTON_TEMPERATURE', 'FIT_ACCUR_PARAM_4', 'PLASMA_FREQUENCY', 'PLASMA_FREQUENCY_NN',
                         'ELECTRONIC_DENSITY_RATIO']
        self.assertCountEqual(a.keys(), expected_list)

    def test_wind_waves_bqt_datetime(self):
        print("### Testing WindWavesData \"DATETIME\" key on BQT dataset")
        a = load_wind_waves_bqt()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1994, 11, 14, 0, 1, 30, 397999))

    def test_wind_waves_radio_60s_name(self):
        print("### Testing WindWavesData name variable on RADIO_60S dataset")
        a = load_wind_waves_radio_60s()
        self.assertEqual(a.name, "WIND_WAVES_RADIO_60S")

    def test_wind_waves_radio_60s_len(self):
        print("### Testing WindWavesData len() method on RADIO_60S dataset")
        a = load_wind_waves_radio_60s()
        self.assertEqual(len(a), 1440)

    def test_wind_waves_radio_60s_keys(self):
        print("### Testing WindWavesData keys() method on RADIO_60S dataset")
        a = load_wind_waves_radio_60s()
        expected_list = ['CALEND_DATE_MONTH', 'CCSDS_PREAMBLE', 'CALEND_DATE_HOUR', 'IUNIT', 'AVG_DURATION',
                         'CCSDS_JULIAN_DAY_B1', 'CCSDS_JULIAN_DAY_B2', 'CALEND_DATE_YEAR', 'CALEND_DATE_MINUTE',
                         'CCSDS_MILLISECONDS_OF_DAY', 'NFREQ', 'CALEND_DATE_SECOND', 'JULIAN_SEC', 'RECEIVER_CODE',
                         'CALEND_DATE_DAY', 'CCSDS_JULIAN_DAY_B3', 'DATETIME', 'INTENSITY', 'FREQ']
        self.assertCountEqual(a.keys(), expected_list)

    def test_wind_waves_radio_60s_datetime(self):
        print("### Testing WindWavesData \"DATETIME\" key on RADIO_60S dataset")
        a = load_wind_waves_radio_60s()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1994, 11, 14, 0, 0, 30))


class ISEE3SBHDataTest(unittest.TestCase):

    """Test case for ISEE3SBHData class"""

    def test_cdpp_data_class(self):
        header = {}
        data = {}
        meta = {}
        orbit = {}
        name = "TEST"
        test = ISEE3SBHData("", header, data, meta, name, orbit)
        self.assertIsInstance(test, CDPPDataFromFile)

    def test_isee3_sbh_3d_radio_source_name(self):
        print("### Testing ISEE3SBHData name variable on 3D_RADIO_SOURCE dataset")
        a = load_isee3_sbh_3d_radio_source()
        self.assertEqual(a.name, "ISEE3_SBH_3D_RADIO_SOURCE")

    def test_isee3_sbh_3d_radio_source_len(self):
        print("### Testing ISEE3SBHData len() method on 3D_RADIO_SOURCE dataset")
        a = load_isee3_sbh_3d_radio_source()
        self.assertEqual(len(a), 665)

    def test_isee3_sbh_3d_radio_source_keys(self):
        print("### Testing ISEE3SBHData keys() method on 3D_RADIO_SOURCE dataset")
        a = load_isee3_sbh_3d_radio_source()
        expected_list = ['CALEND_MONTH', 'CCSDS_DAY', 'N_S', 'TIME_QUALITY', 'SPACECRAFT_POSITION_Z', 'N_FREQ_STEP',
                         'CALEND_MINUTE', 'CYCLE_NUMBER', 'S_SAMPLE_INTERVAL', 'N_MEAS_STEP', 'CCSDS_PREAMBLE',
                         'MILLI_SECOND', 'SPIN_PERIOD', 'SPACECRAFT_POSITION_Y', 'CALEND_DAY', 'CCSDS_HOUR',
                         'CALEND_SECOND', 'TM_FORMAT', 'CCSDS_SECOND_E_4', 'CALEND_YEAR', 'N_FREQ_PER_MEAS_STEP',
                         'NUMBER_OF_OK_STEPS', 'CALEND_HOUR', 'CCSDS_MINUTE', 'S_ANTENNA', 'CCSDS_SECOND',
                         'JULIAN_SECOND', 'SUN_TIME', 'MINOR_FRAME_DURATION', 'CCSDS_YEAR', 'DATA_RATE',
                         'CCSDS_SECOND_E_2', 'CCSDS_MONTH', 'SUN_S_ANTENNA_TIME', 'N_Z', 'RECEIVER_MODE',
                         'SPACECRAFT_POSITION_X', 'DSC_29', 'CYCLE_DURATION', 'N_PHI', 'DSC_28', 'DSC_27',
                         'STEP_DURATION', 'SUN_PERIOD', 'DATETIME', 'FREQUENCY', 'S_DATA', 'DATA_QUALITY',
                         'TIME', 'BANDWIDTH', 'PHI_DATA', 'Z_DATA']
        self.assertCountEqual(a.keys(), expected_list)

    def test_isee3_sbh_3d_radio_source_datetime(self):
        print("### Testing WindWavesData \"DATETIME\" key on RADIO_60S dataset")
        a = load_isee3_sbh_3d_radio_source()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1978, 8, 20, 0, 2, 18, 382000))


