# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit

from maser.data import Data
from maser.data.cdpp import (
    WindWavesRad1L260sV2BinData,
    WindWavesRad1L2BinData,
    WindWavesRad2L260sV2BinData,
    WindWavesTnrL260sV2BinData,
    WindWavesTnrL3Bqt1mnBinData,
    WindWavesTnrL3NnBinData,
    WindWavesRad1L260sV1BinData,
    WindWavesRad2L260sV1BinData,
    WindWavesTnrL260sV1BinData,
    VikingV4nE5BinData,
    InterballAuroralPolradRspBinData,
)
from pathlib import Path
import pytest


BASEDIR = Path(__file__).resolve().parent / "data"

TEST_FILES = {
    "wi_wa_rad1_l2_60s": [
        BASEDIR / "cdpp" / "wind" / "wi_wa_rad1_l2_60s_19941114_v01.dat"
    ],
    "wi_wa_rad1_l2": [BASEDIR / "cdpp" / "wind" / "wi_wa_rad1_l2_19941110_v01.dat"],
    "wi_wa_rad2_l2_60s": [
        BASEDIR / "cdpp" / "wind" / "wi_wa_rad2_l2_60s_19941114_v01.dat"
    ],
    "wi_wa_tnr_l2_60s": [
        BASEDIR / "cdpp" / "wind" / "wi_wa_tnr_l2_60s_19941114_v01.dat"
    ],
    "wi_wa_tnr_l3_bqt_1mn": [
        BASEDIR / "cdpp" / "wind" / "WI_WA_TNR_L3_BQT_19941114_1MN.DAT"
    ],
    "wi_wa_tnr_l3_nn": [BASEDIR / "cdpp" / "wind" / "WI_WA_TNR_L3_NN_19941114_V02.DAT"],
    "win_rad1_60s": [BASEDIR / "cdpp" / "wind" / "WIN_RAD1_60S_19941114.B3E"],
    "win_rad2_60s": [BASEDIR / "cdpp" / "wind" / "WIN_RAD2_60S_19941114.B3E"],
    "win_tnr_60s": [BASEDIR / "cdpp" / "wind" / "WIN_TNR_60S_19941114.B3E"],
    "viking_v4n_e5": [BASEDIR / "cdpp" / "viking" / "V4N_0101_003"],
    "int_aur_polrad_rsp": [
        BASEDIR / "cdpp" / "interball" / "POLR_RSPN2_19971116",
        BASEDIR / "cdpp" / "interball" / "POLR_RSPN2_19990126",
    ],
}


# CDPP/WIND TESTS ===== wi_wa_rad1_l2_60s
@pytest.mark.test_data_required
def test_wi_wa_rad1_l2_60s_bin_dataset():
    for filepath in TEST_FILES["wi_wa_rad1_l2_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesRad1L260sV2BinData)


# CDPP/WIND TESTS ===== wi_wa_rad1_l2
@pytest.mark.test_data_required
def test_wi_wa_rad1_l2_bin_dataset():
    for filepath in TEST_FILES["wi_wa_rad1_l2"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesRad1L2BinData)


@pytest.mark.test_data_required
def test_wi_wa_rad1_l2_bin_dataset__times():
    filepath = TEST_FILES["wi_wa_rad1_l2"][0]
    data = Data(filepath=filepath)
    assert isinstance(data.times, Time)
    assert len(data.times) == 120
    assert data.times[0] == Time("1994-11-10 16:38:06.000")
    assert data.times[-1] == Time("1994-11-10 23:55:27.000")


@pytest.mark.test_data_required
def test_wi_wa_rad1_l2_bin_dataset__frequencies():
    filepath = TEST_FILES["wi_wa_rad1_l2"][0]
    data = Data(filepath=filepath)
    assert isinstance(data.frequencies, Quantity)
    assert len(data.frequencies) == 64
    assert data.frequencies[0] == 1040 * Unit("kHz")
    assert data.frequencies[-1] == 20 * Unit("kHz")


@pytest.mark.test_data_required
def test_wi_wa_rad1_l2_bin_dataset__sweeps__load_data_false():
    for filepath in TEST_FILES["wi_wa_rad1_l2"]:
        sweeps = Data(filepath=filepath, load_data=False).sweeps
        sweep = next(sweeps)
        assert isinstance(sweep, tuple)
        _, data_i = sweep
        assert data_i is None


@pytest.mark.test_data_required
def test_wi_wa_rad1_l2_bin_dataset__sweeps_for_loop():
    for filepath in TEST_FILES["wi_wa_rad1_l2"]:
        for sweep in Data(filepath=filepath):
            assert isinstance(sweep, tuple)


@pytest.mark.test_data_required
def test_wi_wa_rad1_l2_bin_dataset__sweeps_next():
    for filepath in TEST_FILES["wi_wa_rad1_l2"]:
        sweeps = Data(filepath=filepath).sweeps
        sweep = next(sweeps)
        assert isinstance(sweep, tuple)
        header_i, data_i = sweep
        assert header_i == {
            "CCSDS_PREAMBLE": 76,
            "CCSDS_JULIAN_DAY_B1": 0,
            "CCSDS_JULIAN_DAY_B2": 18,
            "CCSDS_JULIAN_DAY_B3": 88,
            "CCSDS_MILLISECONDS_OF_DAY": 59886877,
            "RECEIVER_CODE": 1,
            "JULIAN_SEC": 405794286,
            "CALEND_DATE_YEAR": 1994,
            "CALEND_DATE_MONTH": 11,
            "CALEND_DATE_DAY": 10,
            "CALEND_DATE_HOUR": 16,
            "CALEND_DATE_MINUTE": 38,
            "CALEND_DATE_SECOND": 6,
            "JULIAN_SEC_FRAC": 0.8779999613761902,
            "IANTEN": 2,
            "ICAL": 0,
            "IDIPXY": 1,
            "IPOLA": 1,
            "ISWEEP": 1,
            "IUNIT": 3,
            "KSPIN": 0,
            "LISTFR": 0,
            "MODE": 3,
            "NFREQ": 16,
            "NFRPAL": 1,
            "NPALCY": 64,
            "NPALIF": 64,
            "NPBS": 11130,
            "NSPALF": 16,
            "NZPALF": 8,
            "SDURCY": 183.23672485351562,
            "SDURPA": 2.8630738258361816,
            "SPIN_RATE": 129.59471130371094,
            "SUN_ANGLE": 190.1953125,
        }
        assert list(data_i.keys()) == ["FREQ", "VSPAL", "VZPAL", "TSPAL", "TZPAL"]
        assert len(data_i["FREQ"]) == 64
        assert data_i["FREQ"][0] == 1040.0
        assert data_i["FREQ"][-1] == 20.0


# CDPP/WIND TESTS ===== wi_wa_rad2_l2_60s
@pytest.mark.test_data_required
def test_wi_wa_rad2_l2_60s_bin_dataset():
    for filepath in TEST_FILES["wi_wa_rad2_l2_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesRad2L260sV2BinData)


# CDPP/WIND TESTS ===== wi_wa_tnr_l2_60s
@pytest.mark.test_data_required
def test_wi_wa_tnr_l2_60s_bin_dataset():
    for filepath in TEST_FILES["wi_wa_tnr_l2_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesTnrL260sV2BinData)


# CDPP/WIND TESTS ===== wi_wa_tnr_l3_bqt_1mn
@pytest.mark.test_data_required
def test_wi_wa_tnr_l3_bqt_1mn_bin_dataset():
    for filepath in TEST_FILES["wi_wa_tnr_l3_bqt_1mn"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesTnrL3Bqt1mnBinData)


@pytest.mark.test_data_required
def test_wi_wa_tnr_l3_bqt_1mn_bin_dataset__sweeps_access_mode__error():
    with pytest.raises(ValueError):
        filepath = TEST_FILES["wi_wa_tnr_l3_bqt_1mn"][0]
        Data(filepath=filepath, access_mode="sweeps")


@pytest.mark.test_data_required
def test_wi_wa_tnr_l3_bqt_1mn_bin_dataset__sweeps_property__error():
    with pytest.raises(ValueError):
        filepath = TEST_FILES["wi_wa_tnr_l3_bqt_1mn"][0]
        Data(filepath=filepath).sweeps


@pytest.mark.test_data_required
def test_wi_wa_tnr_l3_bqt_1mn_bin_dataset__records__load_data_false():
    for filepath in TEST_FILES["wi_wa_tnr_l3_bqt_1mn"]:
        records = Data(filepath=filepath, load_data=False).records
        record = next(records)
        assert isinstance(record, tuple)
        _, data_i = record
        assert data_i is None


@pytest.mark.test_data_required
def test_wi_wa_tnr_l3_bqt_1mn_bin_dataset__records_for_loop():
    for filepath in TEST_FILES["wi_wa_tnr_l3_bqt_1mn"]:
        for record in Data(filepath=filepath):
            assert isinstance(record, tuple)


@pytest.mark.test_data_required
def test_wi_wa_tnr_l3_bqt_1mn_bin_dataset__records_next():
    for filepath in TEST_FILES["wi_wa_tnr_l3_bqt_1mn"]:
        records = Data(filepath=filepath).records
        record = next(records)
        assert isinstance(record, tuple)
        header_i, data_i = record
        assert header_i == {
            "CCSDS_JULIAN_DAY_B1": 0,
            "CCSDS_JULIAN_DAY_B2": 64,
            "CCSDS_JULIAN_DAY_B3": 4,
            "CCSDS_MILLISECONDS_OF_DAY": 90398,
            "CCSDS_PREAMBLE": 76,
            "UR8_TIME": 4700.001046273147,
        }
        assert data_i == {
            "PLASMA_FREQUENCY_NN": pytest.approx(19.773975372314453),
            "PLASMA_FREQUENCY": pytest.approx(19.697528839111328),
            "COLD_ELECTRONS_TEMPERATURE": pytest.approx(16.3936824798584),
            "ELECTRONIC_DENSITY_RATIO": pytest.approx(0.015176571905612946),
            "ELECTRONIC_TEMPERATURE_RATIO": pytest.approx(20.851478576660156),
            "PROTON_TEMPERATURE": pytest.approx(68.4000015258789),
            "SOLAR_WIND_VELOCITY": 0.0,
            "FIT_ACCUR_PARAM_1": pytest.approx(0.41681724786758423),
            "FIT_ACCUR_PARAM_2": pytest.approx(7.388779640197754),
            "FIT_ACCUR_PARAM_3": pytest.approx(36.1054573059082),
            "FIT_ACCUR_PARAM_4": pytest.approx(17.359872817993164),
            "FIT_ACCUR_PARAM_7": 0.0,
            "FIT_ACCUR_PARAM_8": 0.0,
            "FIT_ACCUR_RMS": pytest.approx(3.1150150299072266),
        }


# CDPP/WIND TESTS ===== wi_wa_tnr_l3_nn
@pytest.mark.test_data_required
def test_wi_wa_tnr_l3_nn_bin_dataset():
    for filepath in TEST_FILES["wi_wa_tnr_l3_nn"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesTnrL3NnBinData)


# CDPP/WIND TESTS ===== win_rad1_60s
@pytest.mark.test_data_required
def test_win_rad1_60s_bin_dataset():
    for filepath in TEST_FILES["win_rad1_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesRad1L260sV1BinData)


@pytest.mark.test_data_required
def test_win_rad1_60s_bin_dataset__sweeps__load_data_false():
    for filepath in TEST_FILES["win_rad1_60s"]:
        sweeps = Data(filepath=filepath, load_data=False).sweeps
        sweep = next(sweeps)
        assert isinstance(sweep, tuple)
        _, data_i = sweep
        assert data_i is None


@pytest.mark.test_data_required
def test_win_rad1_60s_bin_dataset__sweeps_for_loop():
    for filepath in TEST_FILES["win_rad1_60s"]:
        for sweep in Data(filepath=filepath):
            assert isinstance(sweep, tuple)


@pytest.mark.test_data_required
def test_win_rad1_60s_bin_dataset__sweeps_next():
    for filepath in TEST_FILES["win_rad1_60s"]:
        sweeps = Data(filepath=filepath).sweeps
        sweep = next(sweeps)
        assert isinstance(sweep, tuple)
        header_i, data_i = sweep
        assert header_i == {
            "AVG_DURATION": 60,
            "CALEND_DATE_DAY": 14,
            "CALEND_DATE_HOUR": 0,
            "CALEND_DATE_MINUTE": 0,
            "CALEND_DATE_MONTH": 11,
            "CALEND_DATE_SECOND": 30,
            "CALEND_DATE_YEAR": 1994,
            "CCSDS_JULIAN_DAY_B1": 0,
            "CCSDS_JULIAN_DAY_B2": 64,
            "CCSDS_JULIAN_DAY_B3": 4,
            "CCSDS_MILLISECONDS_OF_DAY": 30000,
            "CCSDS_PREAMBLE": 76,
            "IUNIT": 3,
            "JULIAN_SEC": 1415923230,
            "NFREQ": 256,
            "RECEIVER_CODE": 1,
        }
        assert list(data_i.keys()) == ["FREQ", "INTENSITY", "ORBIT"]
        assert len(data_i["FREQ"]) == 256
        assert data_i["FREQ"][0] == 20.0
        assert data_i["FREQ"][-1] == 1040.0
        assert data_i["ORBIT"] == {
            "GSE_X": 54.18845748901367,
            "GSE_Y": -5.07206392288208,
            "GSE_Z": -2.4311723709106445,
        }


# CDPP/WIND TESTS ===== win_rad2_60s
@pytest.mark.test_data_required
def test_win_rad2_60s_bin_dataset():
    for filepath in TEST_FILES["win_rad2_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesRad2L260sV1BinData)


@pytest.mark.test_data_required
def test_win_rad2_60s_bin_dataset__sweeps__load_data_false():
    for filepath in TEST_FILES["win_rad2_60s"]:
        sweeps = Data(filepath=filepath, load_data=False).sweeps
        sweep = next(sweeps)
        assert isinstance(sweep, tuple)
        _, data_i = sweep
        assert data_i is None


@pytest.mark.test_data_required
def test_win_rad2_60s_bin_dataset__sweeps_for_loop():
    for filepath in TEST_FILES["win_rad2_60s"]:
        for sweep in Data(filepath=filepath):
            assert isinstance(sweep, tuple)


@pytest.mark.test_data_required
def test_win_rad2_60s_bin_dataset__sweeps_next():
    for filepath in TEST_FILES["win_rad2_60s"]:
        sweeps = Data(filepath=filepath).sweeps
        sweep = next(sweeps)
        assert isinstance(sweep, tuple)
        header_i, data_i = sweep
        assert header_i == {
            "AVG_DURATION": 60,
            "CALEND_DATE_DAY": 14,
            "CALEND_DATE_HOUR": 0,
            "CALEND_DATE_MINUTE": 0,
            "CALEND_DATE_MONTH": 11,
            "CALEND_DATE_SECOND": 30,
            "CALEND_DATE_YEAR": 1994,
            "CCSDS_JULIAN_DAY_B1": 0,
            "CCSDS_JULIAN_DAY_B2": 64,
            "CCSDS_JULIAN_DAY_B3": 4,
            "CCSDS_MILLISECONDS_OF_DAY": 30000,
            "CCSDS_PREAMBLE": 76,
            "IUNIT": 3,
            "JULIAN_SEC": 1415923230,
            "NFREQ": 256,
            "RECEIVER_CODE": 2,
        }
        assert list(data_i.keys()) == ["FREQ", "INTENSITY", "ORBIT"]
        assert len(data_i["FREQ"]) == 256
        assert data_i["FREQ"][0] == 1075.0
        assert data_i["FREQ"][-1] == 13825.0
        assert data_i["ORBIT"] == {
            "GSE_X": 54.18845748901367,
            "GSE_Y": -5.07206392288208,
            "GSE_Z": -2.4311723709106445,
        }


# CDPP/WIND TESTS ===== win_tnr_60s
@pytest.mark.test_data_required
def test_win_tnr_60s_bin_dataset():
    for filepath in TEST_FILES["win_tnr_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesTnrL260sV1BinData)


@pytest.mark.test_data_required
def test_win_tnr_60s_bin_dataset__sweeps__load_data_false():
    for filepath in TEST_FILES["win_tnr_60s"]:
        sweeps = Data(filepath=filepath, load_data=False).sweeps
        sweep = next(sweeps)
        assert isinstance(sweep, tuple)
        _, data_i = sweep
        assert data_i is None


@pytest.mark.test_data_required
def test_win_tnr_60s_bin_dataset__sweeps_for_loop():
    for filepath in TEST_FILES["win_tnr_60s"]:
        for sweep in Data(filepath=filepath):
            assert isinstance(sweep, tuple)


@pytest.mark.test_data_required
def test_win_tnr_60s_bin_dataset__sweeps_next():
    for filepath in TEST_FILES["win_tnr_60s"]:
        sweeps = Data(filepath=filepath).sweeps
        sweep = next(sweeps)
        assert isinstance(sweep, tuple)
        header_i, data_i = sweep
        assert header_i == {
            "AVG_DURATION": 60,
            "CALEND_DATE_DAY": 14,
            "CALEND_DATE_HOUR": 0,
            "CALEND_DATE_MINUTE": 0,
            "CALEND_DATE_MONTH": 11,
            "CALEND_DATE_SECOND": 30,
            "CALEND_DATE_YEAR": 1994,
            "CCSDS_JULIAN_DAY_B1": 0,
            "CCSDS_JULIAN_DAY_B2": 64,
            "CCSDS_JULIAN_DAY_B3": 4,
            "CCSDS_MILLISECONDS_OF_DAY": 30000,
            "CCSDS_PREAMBLE": 76,
            "IUNIT": 3,
            "JULIAN_SEC": 1415923230,
            "NFREQ": 96,
            "RECEIVER_CODE": 0,
        }
        assert list(data_i.keys()) == ["FREQ", "INTENSITY", "ORBIT"]
        assert len(data_i["FREQ"]) == 96
        assert data_i["FREQ"][0] == pytest.approx(4.087588787078857)
        assert data_i["FREQ"][-1] == pytest.approx(250.5144500732422)
        assert data_i["ORBIT"] == {
            "GSE_X": 54.18845748901367,
            "GSE_Y": -5.07206392288208,
            "GSE_Z": -2.4311723709106445,
        }


# CDPP/VIKING TESTS ==== viking_v4n_e5
@pytest.mark.test_data_required
def test_viking_v4n_e5_bin_dataset():
    for filepath in TEST_FILES["viking_v4n_e5"]:
        data = Data(filepath=filepath)
        assert isinstance(data, VikingV4nE5BinData)


@pytest.mark.test_data_required
def test_viking_v4n_e5_bin_dataset__times():
    filepath = TEST_FILES["viking_v4n_e5"][0]
    data = Data(filepath=filepath)
    assert isinstance(data.times, Time)
    assert len(data.times) == 120
    assert data.times[0] == Time("1994-11-10 16:38:06.000")
    assert data.times[-1] == Time("1994-11-10 23:55:27.000")


@pytest.mark.test_data_required
def test_viking_v4n_e5_bin_dataset__sweeps_access_mode__error():
    with pytest.raises(ValueError):
        filepath = TEST_FILES["viking_v4n_e5"][0]
        Data(filepath=filepath, access_mode="sweeps")


# CDPP/INTERBALL TESTS ==== int_aur_polrad_rst
@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset():
    for filepath in TEST_FILES["int_aur_polrad_rsp"]:
        data = Data(filepath=filepath)
        assert isinstance(data, InterballAuroralPolradRspBinData)


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__sweeps__load_data_false():
    for filepath in TEST_FILES["int_aur_polrad_rsp"]:
        sweeps = Data(filepath=filepath, load_data=False).sweeps
        sweep = next(sweeps)
        assert isinstance(sweep, tuple)
        _, data_i = sweep
        assert data_i is None


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__sweeps_for_loop():
    for filepath in TEST_FILES["int_aur_polrad_rsp"]:
        for sweep in Data(filepath=filepath):
            assert isinstance(sweep, tuple)


@pytest.mark.test_data_required
def test_int_aur_polrad_rsp_bin_dataset__sweeps_next():
    header_result = {
        TEST_FILES["int_aur_polrad_rsp"][0]: {
            "CCSDS_PREAMBLE": 76,
            "CCSDS_JULIAN_DAY_B1": 0,
            "CCSDS_JULIAN_DAY_B2": 68,
            "CCSDS_JULIAN_DAY_B3": 78,
            "CCSDS_MILLISECONDS_OF_DAY": 5417,
            "ATTENUATION": 0,
            "CHANNELS": 1,
            "SWEEP_DURATION": 3.249000072479248,
            "STEPS": 240,
            "SESSION_NAME": "73204S21",
            "FIRST_FREQ": 987.1360473632812,
            "CCSDS_CDS_LEVEL2_EPOCH": Time("1950-01-01 00:00:00.000"),
        },
        TEST_FILES["int_aur_polrad_rsp"][1]: {
            "CCSDS_PREAMBLE": 76,
            "CCSDS_JULIAN_DAY_B1": 0,
            "CCSDS_JULIAN_DAY_B2": 70,
            "CCSDS_JULIAN_DAY_B3": 2,
            "CCSDS_MILLISECONDS_OF_DAY": 18381394,
            "ATTENUATION": 0,
            "CHANNELS": 3,
            "SWEEP_DURATION": 6.5,
            "STEPS": 240,
            "SESSION_NAME": "90262S21",
            "FIRST_FREQ": 987.1360473632812,
            "CCSDS_CDS_LEVEL2_EPOCH": Time("1950-01-01 00:00:00.000"),
        },
    }
    for filepath in TEST_FILES["int_aur_polrad_rsp"]:
        sweeps = Data(filepath=filepath).sweeps
        sweep = next(sweeps)
        assert isinstance(sweep, tuple)
        header_i, data_i = sweep
        assert header_i == header_result[filepath]
        assert list(data_i.keys()) == ["EX", "EY", "EZ"]
        assert len(data_i["EZ"]) == 240
        if header_i["CHANNELS"] == 1:
            assert data_i["EX"] is None
            assert data_i["EY"] is None
        else:
            assert len(data_i["EX"]) == 240
            assert len(data_i["EY"]) == 240
