# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit

from maser.data import Data
from maser.data.base import (
    BinData,
    CdfData,
    FitsData,
)
from maser.data.nancay import (
    SrnNdaRoutineJupEdrCdfData,
    NenufarBstFitsData,
)
from maser.data.ecallisto import (
    ECallistoFitsData,
)
from maser.data.pds import (
    Pds3Data,
    Vg1JPra3RdrLowband6secV1Data,
)
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
)
from pathlib import Path
from spacepy import pycdf
from astropy.io import fits
import pytest


BASEDIR = Path(__file__).resolve().parent / "data"

TEST_FILES = {
    "srn_nda_routine_jup_edr": [
        BASEDIR
        / "nda"
        / "routine"
        / "srn_nda_routine_jup_edr_201601302247_201601310645_V12.cdf"
    ],
    "nenufar_bst": [
        BASEDIR
        / "nenufar"
        / "bst"
        / "20220130_112900_20220130_123100_SUN_TRACKING"
        / "20220130_112900_BST.fits"
    ],
    "vg1_j_pra_3_rdr_lowband_6sec_v1": [
        BASEDIR / "pds" / "VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1" / "PRA_I.LBL"
    ],
    "ecallisto": [BASEDIR / "e-callisto" / "BIR" / "BIR_20220130_111500_01.fit"],
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
}


def test_dataset():
    with pytest.raises(NotImplementedError):
        Data(filepath=Path("toto.txt"))


def test_cdf_dataset():
    data = Data(filepath=Path("toto.txt"), dataset="cdf")
    assert isinstance(data, Data)
    assert isinstance(data, CdfData)


def test_cdf_dataset__filepath_type():
    data = Data(filepath="toto.txt", dataset="cdf")
    assert isinstance(data.filepath, Path)


def test_fits_dataset():
    data = Data(filepath=Path("toto.txt"), dataset="fits")
    assert isinstance(data, Data)
    assert isinstance(data, FitsData)


def test_pds3_dataset():
    data = Data(filepath=Path("toto.txt"), dataset="pds3")
    assert isinstance(data, Data)
    assert isinstance(data, Pds3Data)


def test_bin_dataset():
    data = Data(filepath=Path("toto.txt"), dataset="bin")
    assert isinstance(data, Data)
    assert isinstance(data, BinData)


@pytest.mark.test_data_required
def test_srn_nda_routine_jup_edr_dataset():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        data = Data(filepath=filepath)
        assert isinstance(data, SrnNdaRoutineJupEdrCdfData)


@pytest.mark.test_data_required
def test_srn_nda_routine_jup_edr_dataset__times():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 28734
            assert data.times[0] == Time("2016-01-30 22:47:06.03")
            assert data.times[-1] == Time("2016-01-31 06:45:58.68")


@pytest.mark.test_data_required
def test_srn_nda_routine_jup_edr_dataset__frequencies():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.frequencies, Quantity)
            assert len(data.frequencies) == 400
            assert data.frequencies[0].to(Unit("MHz")).value == pytest.approx(10)
            assert data.frequencies[-1].to(Unit("MHz")).value == pytest.approx(39.925)


def test_srn_nda_routine_jup_edr_dataset__access_mode_file():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, pycdf.CDF)


@pytest.mark.test_data_required
def test_srn_nda_routine_jup_edr_dataset__iter_method__mode_file():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        data = Data(filepath=filepath, access_mode="file")
        var_labels = [item for item in data]
        assert list(data.file) == var_labels
        assert var_labels == [
            "Epoch",
            "RR",
            "LL",
            "STATUS",
            "SWEEP_TIME_OFFSET_RAMP",
            "RR_SWEEP_TIME_OFFSET",
            "Frequency",
        ]


@pytest.mark.test_data_required
def test_srn_nda_routine_jup_edr_dataset__access_mode_error():
    with pytest.raises(ValueError):
        Data(
            filepath=TEST_FILES["srn_nda_routine_jup_edr"][0],
            access_mode="toto",
        )


@pytest.mark.test_data_required
def test_nenufar_bst_dataset():
    for filepath in TEST_FILES["nenufar_bst"]:
        data = Data(filepath=filepath)
        assert isinstance(data, NenufarBstFitsData)


@pytest.mark.test_data_required
def test_nenufar_bst_dataset__beam():
    for filepath in TEST_FILES["nenufar_bst"]:
        data = Data(filepath=filepath, beam=1)
        assert data.beam == 1


@pytest.mark.test_data_required
def test_nenufar_bst_dataset__beam__value_error():
    for filepath in TEST_FILES["nenufar_bst"]:
        with pytest.raises(ValueError):
            Data(filepath=filepath, beam=1000)


@pytest.mark.test_data_required
def test_nenufar_bst_dataset__access_mode_file():
    for filepath in TEST_FILES["nenufar_bst"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, fits.hdu.hdulist.HDUList)


@pytest.mark.test_data_required
def test_nenufar_bst_dataset__times():
    for filepath in TEST_FILES["nenufar_bst"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 3600
            assert data.times[0] == Time(2459609.9792824076, format="jd")
            assert data.times[-1] == Time(2459610.0209375, format="jd")


@pytest.mark.test_data_required
def test_nenufar_bst_dataset__times__other_beam():
    for filepath in TEST_FILES["nenufar_bst"]:
        with Data(filepath=filepath, beam=1) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 3600
            assert data.times[0] == Time(2459609.9792824076, format="jd")
            assert data.times[-1] == Time(2459610.0209375, format="jd")


@pytest.mark.test_data_required
def test_nenufar_bst_dataset__frequencies():
    for filepath in TEST_FILES["nenufar_bst"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.frequencies, Quantity)
            assert len(data.frequencies) == 192
            assert data.frequencies[0] == 25 * Unit("MHz")
            assert data.frequencies[-1].value == pytest.approx(62.304688)


@pytest.mark.test_data_required
def test_ecallisto_dataset():
    for filepath in TEST_FILES["ecallisto"]:
        data = Data(filepath=filepath)
        assert isinstance(data, ECallistoFitsData)


@pytest.mark.test_data_required
def test_ecallisto_dataset__access_mode_file():
    for filepath in TEST_FILES["ecallisto"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, fits.hdu.hdulist.HDUList)


@pytest.mark.test_data_required
def test_ecallisto_dataset__times():
    for filepath in TEST_FILES["ecallisto"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 3600
            assert data.times[0] == Time("2022-01-30 11:15:00.171")
            assert data.times[-1].jd == pytest.approx(
                Time("2022-01-30 11:29:59.921").jd
            )


@pytest.mark.test_data_required
def test_ecallisto_dataset__frequencies():
    for filepath in TEST_FILES["ecallisto"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.frequencies, Quantity)
            assert len(data.frequencies) == 200
            assert data.frequencies[0] == 105.5 * Unit("MHz")
            assert data.frequencies[-1] == 10 * Unit("MHz")


@pytest.mark.test_data_required
def test_vg1_j_pra_3_rdr_lowband_6sec_v1_dataset():
    for filepath in TEST_FILES["vg1_j_pra_3_rdr_lowband_6sec_v1"]:
        data = Data(filepath=filepath)
        assert isinstance(data, Vg1JPra3RdrLowband6secV1Data)


@pytest.mark.test_data_required
def test_vg1_j_pra_3_rdr_lowband_6sec_v1_dataset__access_mode_file():
    for filepath in TEST_FILES["vg1_j_pra_3_rdr_lowband_6sec_v1"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, dict)


@pytest.mark.test_data_required
def test_wi_wa_rad1_l2_60s_bin_dataset():
    for filepath in TEST_FILES["wi_wa_rad1_l2_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesRad1L260sV2BinData)


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


@pytest.mark.test_data_required
def test_wi_wa_rad2_l2_60s_bin_dataset():
    for filepath in TEST_FILES["wi_wa_rad2_l2_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesRad2L260sV2BinData)


@pytest.mark.test_data_required
def test_wi_wa_tnr_l2_60s_bin_dataset():
    for filepath in TEST_FILES["wi_wa_tnr_l2_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesTnrL260sV2BinData)


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


@pytest.mark.test_data_required
def test_wi_wa_tnr_l3_nn_bin_dataset():
    for filepath in TEST_FILES["wi_wa_tnr_l3_nn"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesTnrL3NnBinData)


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
