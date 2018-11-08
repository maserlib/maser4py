import unittest
import datetime
from maser.data.tests import load_test_data, get_data_directory
from maser.data.cdpp import CDPPDataFromFile
from maser.data.cdpp.wind.waves import WindWavesData, read_wind_waves
from maser.data.cdpp.isee3.sbh import ISEE3SBHData, read_isee3_sbh_3d_radio_source
from maser.data.cdpp.viking.v4n import VikingV4nData, read_viking

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


def load_viking_v4():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path))


def load_viking_v4_v1():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4_V1")


def load_viking_v4_v2():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4_V2")


def load_viking_v4l_fbl():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4L_FBL")


def load_viking_v4l_ni():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4L_Ni")


def load_viking_v4l_dft():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4L_DFT")


def load_viking_v4l_wf():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4L_WF")


def load_viking_v4h_sfa():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4H_SFA")


def load_viking_v4h_fb():
    file_path = get_data_directory() / "cdpp" / "viking" / "V4N_0101_003"
    return read_viking(str(file_path), "VIKING_V4H_FB")


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


class VikingV4nDataTest(unittest.TestCase):

    """Test case for VikingV4nData class"""
    def test_cdpp_data_class(self):
        header1 = {}
        header2 = {}
        header3 = {}
        data = {}
        meta = {}
        status = {}
        orbit = {}
        name = "TEST"
        test = VikingV4nData("", header1, header2, header3, status, data, name, meta, orbit)
        self.assertIsInstance(test, CDPPDataFromFile)

    """VIKING_V4"""

    def test_viking_v4_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4 dataset")
        a = load_viking_v4()
        self.assertEqual(a.name, "VIKING_V4")

    def test_viking_v4_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4 dataset")
        a = load_viking_v4()
        self.assertEqual(len(a), 12)

    def test_viking_v4_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4 dataset")
        a = load_viking_v4()
        expected_list = ['V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'UTC_CCSDS_SECOND_E_2', 'RECORD_NUMBER',
                         'CCSDS_MINUTE', 'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                         'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'UTC_CCSDS_MONTH', 'ABNORMAL_END_OF_SWEEP',
                         'UTC_CCSDS_MINUTE', 'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                         'BUFFER_NUMBER', 'UTC_CCSDS_SECOND_E_4', 'SATELLITE_TIME_MSB', 'UTC_CCSDS_HOUR',
                         'TM_LACK_AFTER_SWEEP', 'CCSDS_SECOND', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                         'UTC_CALENDAR_DAY', 'UTC_CCSDS_YEAR', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                         'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                         'UTC_CCSDS_DAY', 'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                         'UTC_CCSDS_SECOND', 'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                         'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP', 'CCSDS_SECOND_E_2', 'CCSDS_HOUR',
                         'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CCSDS_DAY', 'CALENDAR_YEAR', 'CCSDS_YEAR',
                         'CCSDS_MONTH', 'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND', 'CCSDS_SECOND_E_4',
                         'UTC_CALENDER_MONTH', 'DATETIME', 'FREQUENCY_FB', 'ELECTRIC_FB', 'MAGNETIC_FB', 'V2_THETA',
                         'V2_AMPLITUDE', 'V2_PHI', 'V2_PSI', 'FREQUENCY_FBL', 'ELECTRIC_FBL', 'MAGNETIC_SFA',
                         'ELECTRIC_SFA', 'FREQUENCY_SFA', 'V1_ED', 'V1_EPDIFF', 'V1_EPAR', 'V1_EC', 'V1_VFG', 'V1_ID',
                         'V1_IFILL', 'V1_USER_BIAS', 'V1_RELATIVE_TIME', 'V1_VGUARD', 'DFT', 'N2_PROBE', 'N1_PROBE',
                         'WF1', 'WF2']
        self.assertCountEqual(a.keys(), expected_list)

    def test_viking_v4_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4 dataset")
        a = load_viking_v4()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    """VIKING_V4_V1"""

    def test_viking_v4_v1_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4_V1 dataset")
        a = load_viking_v4_v1()
        self.assertEqual(a.name, "VIKING_V4_V1")

    def test_viking_v4_v1_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4_V1 dataset")
        a = load_viking_v4_v1()
        self.assertEqual(len(a), 12)

    def test_viking_v4_v1_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4_V1 dataset")
        a = load_viking_v4_v1()
        expected_list = ['V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'UTC_CCSDS_SECOND_E_2', 'RECORD_NUMBER',
                         'CCSDS_MINUTE', 'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                         'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'UTC_CCSDS_MONTH', 'ABNORMAL_END_OF_SWEEP',
                         'UTC_CCSDS_MINUTE', 'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                         'BUFFER_NUMBER', 'UTC_CCSDS_SECOND_E_4', 'SATELLITE_TIME_MSB', 'UTC_CCSDS_HOUR',
                         'TM_LACK_AFTER_SWEEP', 'CCSDS_SECOND', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                         'UTC_CALENDAR_DAY', 'UTC_CCSDS_YEAR', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                         'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                         'UTC_CCSDS_DAY', 'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                         'UTC_CCSDS_SECOND', 'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                         'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP', 'CCSDS_SECOND_E_2', 'CCSDS_HOUR',
                         'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CCSDS_DAY', 'CALENDAR_YEAR', 'CCSDS_YEAR',
                         'CCSDS_MONTH', 'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND', 'CCSDS_SECOND_E_4',
                         'UTC_CALENDER_MONTH', 'DATETIME', 'V1_ED', 'V1_EPDIFF', 'V1_EPAR', 'V1_EC', 'V1_VFG', 'V1_ID',
                         'V1_IFILL', 'V1_USER_BIAS', 'V1_RELATIVE_TIME', 'V1_VGUARD']
        self.assertCountEqual(a.keys(), expected_list)

    def test_viking_v4_v1_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4_V1 dataset")
        a = load_viking_v4_v1()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    """VIKING_V4_V2"""

    def test_viking_v4_v2_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4_V2 dataset")
        a = load_viking_v4_v2()
        self.assertEqual(a.name, "VIKING_V4_V2")

    def test_viking_v4_v2_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4_V2 dataset")
        a = load_viking_v4_v2()
        self.assertEqual(len(a), 12)

    def test_viking_v4_v2_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4_V2 dataset")
        a = load_viking_v4_v2()
        expected_list = ['V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'UTC_CCSDS_SECOND_E_2', 'RECORD_NUMBER',
                         'CCSDS_MINUTE', 'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                         'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'UTC_CCSDS_MONTH', 'ABNORMAL_END_OF_SWEEP',
                         'UTC_CCSDS_MINUTE', 'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                         'BUFFER_NUMBER', 'UTC_CCSDS_SECOND_E_4', 'SATELLITE_TIME_MSB', 'UTC_CCSDS_HOUR',
                         'TM_LACK_AFTER_SWEEP', 'CCSDS_SECOND', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                         'UTC_CALENDAR_DAY', 'UTC_CCSDS_YEAR', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                         'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                         'UTC_CCSDS_DAY', 'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                         'UTC_CCSDS_SECOND', 'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                         'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP', 'CCSDS_SECOND_E_2', 'CCSDS_HOUR',
                         'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CCSDS_DAY', 'CALENDAR_YEAR', 'CCSDS_YEAR',
                         'CCSDS_MONTH', 'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND', 'CCSDS_SECOND_E_4',
                         'UTC_CALENDER_MONTH', 'DATETIME', 'V2_THETA', 'V2_AMPLITUDE', 'V2_PHI', 'V2_PSI']
        self.assertCountEqual(a.keys(), expected_list)

    def test_viking_v4_v2_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4_V2 dataset")
        a = load_viking_v4_v2()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    """VIKING_V4H_SFA"""

    def test_viking_v4h_sfa_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4H_SFA dataset")
        a = load_viking_v4h_sfa()
        self.assertEqual(a.name, "VIKING_V4H_SFA")

    def test_viking_v4h_sfa_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4H_SFA dataset")
        a = load_viking_v4h_sfa()
        self.assertEqual(len(a), 12)

    def test_viking_v4h_sfa_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4H_SFA dataset")
        a = load_viking_v4h_sfa()
        expected_list = ['V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'UTC_CCSDS_SECOND_E_2', 'RECORD_NUMBER',
                         'CCSDS_MINUTE', 'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                         'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'UTC_CCSDS_MONTH', 'ABNORMAL_END_OF_SWEEP',
                         'UTC_CCSDS_MINUTE', 'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                         'BUFFER_NUMBER', 'UTC_CCSDS_SECOND_E_4', 'SATELLITE_TIME_MSB', 'UTC_CCSDS_HOUR',
                         'TM_LACK_AFTER_SWEEP', 'CCSDS_SECOND', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                         'UTC_CALENDAR_DAY', 'UTC_CCSDS_YEAR', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                         'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                         'UTC_CCSDS_DAY', 'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                         'UTC_CCSDS_SECOND', 'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                         'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP', 'CCSDS_SECOND_E_2', 'CCSDS_HOUR',
                         'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CCSDS_DAY', 'CALENDAR_YEAR', 'CCSDS_YEAR',
                         'CCSDS_MONTH', 'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND', 'CCSDS_SECOND_E_4',
                         'UTC_CALENDER_MONTH', 'DATETIME', 'MAGNETIC_SFA', 'ELECTRIC_SFA', 'FREQUENCY_SFA']
        self.assertCountEqual(a.keys(), expected_list)

    def test_viking_v4h_sfa_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4H_SFA dataset")
        a = load_viking_v4h_sfa()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    """VIKING_V4H_FB"""

    def test_viking_v4h_fb_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4H_FB dataset")
        a = load_viking_v4h_fb()
        self.assertEqual(a.name, "VIKING_V4H_FB")

    def test_viking_v4h_fb_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4H_FB dataset")
        a = load_viking_v4h_fb()
        self.assertEqual(len(a), 12)

    def test_viking_v4h_fb_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4H_FB dataset")
        a = load_viking_v4h_fb()
        expected_list = ['V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'UTC_CCSDS_SECOND_E_2', 'RECORD_NUMBER',
                         'CCSDS_MINUTE', 'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                         'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'UTC_CCSDS_MONTH', 'ABNORMAL_END_OF_SWEEP',
                         'UTC_CCSDS_MINUTE', 'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                         'BUFFER_NUMBER', 'UTC_CCSDS_SECOND_E_4', 'SATELLITE_TIME_MSB', 'UTC_CCSDS_HOUR',
                         'TM_LACK_AFTER_SWEEP', 'CCSDS_SECOND', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                         'UTC_CALENDAR_DAY', 'UTC_CCSDS_YEAR', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                         'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                         'UTC_CCSDS_DAY', 'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                         'UTC_CCSDS_SECOND', 'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                         'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP', 'CCSDS_SECOND_E_2', 'CCSDS_HOUR',
                         'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CCSDS_DAY', 'CALENDAR_YEAR', 'CCSDS_YEAR',
                         'CCSDS_MONTH', 'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND', 'CCSDS_SECOND_E_4',
                         'UTC_CALENDER_MONTH', 'DATETIME', 'FREQUENCY_FB', 'ELECTRIC_FB', 'MAGNETIC_FB']
        self.assertCountEqual(a.keys(), expected_list)

    def test_viking_v4h_fba_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4H_FB dataset")
        a = load_viking_v4h_fb()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    """VIKING_V4L_FBL"""

    def test_viking_v4l_fbl_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4L_FBL dataset")
        a = load_viking_v4l_fbl()
        self.assertEqual(a.name, "VIKING_V4L_FBL")

    def test_viking_v4l_fbl_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4L_FBL dataset")
        a = load_viking_v4l_fbl()
        self.assertEqual(len(a), 12)

    def test_viking_v4l_fbl_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4L_FBL dataset")
        a = load_viking_v4l_fbl()
        expected_list = ['V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'UTC_CCSDS_SECOND_E_2', 'RECORD_NUMBER',
                         'CCSDS_MINUTE', 'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                         'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'UTC_CCSDS_MONTH', 'ABNORMAL_END_OF_SWEEP',
                         'UTC_CCSDS_MINUTE', 'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                         'BUFFER_NUMBER', 'UTC_CCSDS_SECOND_E_4', 'SATELLITE_TIME_MSB', 'UTC_CCSDS_HOUR',
                         'TM_LACK_AFTER_SWEEP', 'CCSDS_SECOND', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                         'UTC_CALENDAR_DAY', 'UTC_CCSDS_YEAR', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                         'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                         'UTC_CCSDS_DAY', 'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                         'UTC_CCSDS_SECOND', 'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                         'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP', 'CCSDS_SECOND_E_2', 'CCSDS_HOUR',
                         'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CCSDS_DAY', 'CALENDAR_YEAR', 'CCSDS_YEAR',
                         'CCSDS_MONTH', 'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND', 'CCSDS_SECOND_E_4',
                         'UTC_CALENDER_MONTH', 'DATETIME', 'FREQUENCY_FBL', 'ELECTRIC_FBL']
        self.assertCountEqual(a.keys(), expected_list)

    def test_viking_v4l_fbl_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4L_FBL dataset")
        a = load_viking_v4l_fbl()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    """VIKING_V4L_Ni"""

    def test_viking_v4l_ni_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4L_Ni dataset")
        a = load_viking_v4l_ni()
        self.assertEqual(a.name, "VIKING_V4L_Ni")

    def test_viking_v4l_ni_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4L_Ni dataset")
        a = load_viking_v4l_ni()
        self.assertEqual(len(a), 12)

    def test_viking_v4l_ni_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4L_Ni dataset")
        a = load_viking_v4l_ni()
        expected_list = ['V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'UTC_CCSDS_SECOND_E_2', 'RECORD_NUMBER',
                         'CCSDS_MINUTE', 'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                         'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'UTC_CCSDS_MONTH', 'ABNORMAL_END_OF_SWEEP',
                         'UTC_CCSDS_MINUTE', 'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                         'BUFFER_NUMBER', 'UTC_CCSDS_SECOND_E_4', 'SATELLITE_TIME_MSB', 'UTC_CCSDS_HOUR',
                         'TM_LACK_AFTER_SWEEP', 'CCSDS_SECOND', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                         'UTC_CALENDAR_DAY', 'UTC_CCSDS_YEAR', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                         'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                         'UTC_CCSDS_DAY', 'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                         'UTC_CCSDS_SECOND', 'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                         'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP', 'CCSDS_SECOND_E_2', 'CCSDS_HOUR',
                         'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CCSDS_DAY', 'CALENDAR_YEAR', 'CCSDS_YEAR',
                         'CCSDS_MONTH', 'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND', 'CCSDS_SECOND_E_4',
                         'UTC_CALENDER_MONTH', 'DATETIME', 'N1_PROBE', 'N2_PROBE']
        self.assertCountEqual(a.keys(), expected_list)

    def test_viking_v4l_ni_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4L_Ni dataset")
        a = load_viking_v4l_ni()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    def test_viking_v4l_ni_datetime_utc(self):
        print("### Testing VikingV4nData \"DATETIME_UTC\" key on VIKING_V4L_Ni dataset")
        a = load_viking_v4l_ni()
        dt = a["DATETIME_UTC"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 0, 393000))

    """VIKING_V4L_DFT"""

    def test_viking_v4l_dft_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4L_DFT dataset")
        a = load_viking_v4l_dft()
        self.assertEqual(a.name, "VIKING_V4L_DFT")

    def test_viking_v4l_dft_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4L_DFT dataset")
        a = load_viking_v4l_dft()
        self.assertEqual(len(a), 12)

    def test_viking_v4l_dft_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4L_DFT dataset")
        a = load_viking_v4l_dft()
        expected_list = ['V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'UTC_CCSDS_SECOND_E_2', 'RECORD_NUMBER',
                         'CCSDS_MINUTE', 'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                         'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'UTC_CCSDS_MONTH', 'ABNORMAL_END_OF_SWEEP',
                         'UTC_CCSDS_MINUTE', 'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                         'BUFFER_NUMBER', 'UTC_CCSDS_SECOND_E_4', 'SATELLITE_TIME_MSB', 'UTC_CCSDS_HOUR',
                         'TM_LACK_AFTER_SWEEP', 'CCSDS_SECOND', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                         'UTC_CALENDAR_DAY', 'UTC_CCSDS_YEAR', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                         'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                         'UTC_CCSDS_DAY', 'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                         'UTC_CCSDS_SECOND', 'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                         'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP', 'CCSDS_SECOND_E_2', 'CCSDS_HOUR',
                         'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CCSDS_DAY', 'CALENDAR_YEAR', 'CCSDS_YEAR',
                         'CCSDS_MONTH', 'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND', 'CCSDS_SECOND_E_4',
                         'UTC_CALENDER_MONTH', 'DATETIME', 'DFT']
        self.assertCountEqual(a.keys(), expected_list)

    def test_viking_v4l_dft_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4L_DFT dataset")
        a = load_viking_v4l_dft()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    def test_viking_v4l_dft_datetime_utc(self):
        print("### Testing VikingV4nData \"DATETIME_UTC\" key on VIKING_V4L_DFT dataset")
        a = load_viking_v4l_dft()
        dt = a["DATETIME_UTC"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 0, 393000))

    """VIKING_V4L_WF"""

    def test_viking_v4l_wf_name(self):
        print("### Testing VikingV4nData name variable on VIKING_V4L_WF dataset")
        a = load_viking_v4l_wf()
        self.assertEqual(a.name, "VIKING_V4L_WF")

    def test_viking_v4l_wf_len(self):
        print("### Testing VikingV4nData len() method on VIKING_V4L_WF dataset")
        a = load_viking_v4l_wf()
        self.assertEqual(len(a), 12)

    def test_viking_v4l_wf_keys(self):
        print("### Testing VikingV4nData keys() method on VIKING_V4L_WF dataset")
        a = load_viking_v4l_wf()
        expected_list = ['V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER', 'UTC_CCSDS_SECOND_E_2', 'RECORD_NUMBER',
                         'CCSDS_MINUTE', 'CALENDAR_MINUTE', 'SATELLITE_TIME_LSB', 'UTC_CALENDAR_SECOND',
                         'SWEEP_DURATION', 'CCSDS_PREAMBLE', 'UTC_CCSDS_MONTH', 'ABNORMAL_END_OF_SWEEP',
                         'UTC_CCSDS_MINUTE', 'V4L_MODE_SWITCH_FLAGS_DURING_SWEEP', 'ORBIT_NUMBER', 'CALENDAR_HOUR',
                         'BUFFER_NUMBER', 'UTC_CCSDS_SECOND_E_4', 'SATELLITE_TIME_MSB', 'UTC_CCSDS_HOUR',
                         'TM_LACK_AFTER_SWEEP', 'CCSDS_SECOND', 'BUFFER_TYPE', 'NUMBER_OF_SERIES_IN_CURRENT_SWEEP',
                         'UTC_CALENDAR_DAY', 'UTC_CCSDS_YEAR', 'NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD',
                         'TM_LACK_BEFORE_SWEEP', 'CALENDAR_MILLI_SECOND', 'RANK_OF_RECORD_IN_CURRENT_SWEEP',
                         'UTC_CCSDS_DAY', 'CALENDER_MONTH', 'UTC_CALENDAR_MINUTE', 'CALENDAR_DAY',
                         'UTC_CCSDS_SECOND', 'UTC_CALENDAR_YEAR', 'UTC_CALENDAR_MILLI_SECOND', 'UTC_CALENDAR_HOUR',
                         'COMPLETE_SWEEP', 'V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP', 'CCSDS_SECOND_E_2', 'CCSDS_HOUR',
                         'NUMBER_OF_RECORDS_IN_CURRENT_SWEEP', 'CCSDS_DAY', 'CALENDAR_YEAR', 'CCSDS_YEAR',
                         'CCSDS_MONTH', 'UTC_CCSDS_PREAMBLE', 'SWEEP_NUMBER', 'CALENDAR_SECOND', 'CCSDS_SECOND_E_4',
                         'UTC_CALENDER_MONTH', 'DATETIME', 'WF1', 'WF2']
        self.assertCountEqual(a.keys(), expected_list)

    def test_viking_v4l_wf_datetime(self):
        print("### Testing VikingV4nData \"DATETIME\" key on VIKING_V4L_WF dataset")
        a = load_viking_v4l_wf()
        dt = a["DATETIME"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 3, 179000))

    def test_viking_v4l_wf_datetime_utc(self):
        print("### Testing VikingV4nData \"DATETIME_UTC\" key on VIKING_V4L_WF dataset")
        a = load_viking_v4l_wf()
        dt = a["DATETIME_UTC"]
        self.assertEqual(dt[0], datetime.datetime(1986, 3, 12, 7, 43, 0, 393000))
