# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit


from maser.data import Data
from maser.data.data import (
    BinData,
    CdfData,
    SrnNdaRoutineJupEdrCdfData,
    FitsData,
    NenufarBstFitsData,
    ECallistoFitsData,
    Pds3Data,
    Vg1JPra3RdrLowband6secV1Data,
    WindWavesRad1L260sBinData,
    WindWavesRad1L2BinData,
    WindWavesRad2L260sBinData,
    WindWavesTnrL260sBinData,
    WindWavesTnrL3Bqt1mnBinData,
    WindWavesTnrL3NnBinData,
    WindWavesRad160sBinData,
    WindWavesRad260sBinData,
    WindWavesTnr60sBinData,
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
    "ecallisto": [BASEDIR / "e-callisto" / "BIR_20220130_111500_01.fit"],
    "wi_wa_rad1_l2_60s": [BASEDIR / "wind" / "wi_wa_rad1_l2_60s_19941114_v01.dat"],
    "wi_wa_rad1_l2": [BASEDIR / "wind" / "wi_wa_rad1_l2_19941110_v01.dat"],
    "wi_wa_rad2_l2_60s": [BASEDIR / "wind" / "wi_wa_rad2_l2_60s_19941114_v01.dat"],
    "wi_wa_tnr_l2_60s": [BASEDIR / "wind" / "wi_wa_tnr_l2_60s_19941114_v01.dat"],
    "wi_wa_tnr_l3_bqt_1mn": [BASEDIR / "wind" / "WI_WA_TNR_L3_BQT_19941114_1MN.DAT"],
    "wi_wa_tnr_l3_nn": [BASEDIR / "wind" / "WI_WA_TNR_L3_NN_19941114_V02.DAT"],
    "win_rad1_60s": [BASEDIR / "wind" / "WIN_RAD1_60S_19941114.B3E"],
    "win_rad2_60s": [BASEDIR / "wind" / "WIN_RAD2_60S_19941114.B3E"],
    "win_tnr_60s": [BASEDIR / "wind" / "WIN_TNR_60S_19941114.B3E"],
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


def test_wi_wa_rad1_l2_60s_bin_dataset():
    for filepath in TEST_FILES["wi_wa_rad1_l2_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesRad1L260sBinData)


def test_wi_wa_rad1_l2_bin_dataset():
    for filepath in TEST_FILES["wi_wa_rad1_l2"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesRad1L2BinData)


def test_wi_wa_rad1_l2_bin_dataset__sweeps():
    for filepath in TEST_FILES["wi_wa_rad1_l2"]:
        sweeps = Data(filepath=filepath).sweeps
        sweep = next(sweeps)
        assert isinstance(sweep, tuple)
        header_i, data_i = sweep
        assert header_i == {
            "DAY": 10,
            "HOUR": 16,
            "IANTEN": 2,
            "ICAL": 0,
            "IDIPXY": 1,
            "IPOLA": 1,
            "ISWEEP": 1,
            "IUNIT": 3,
            "JULIAN_DAY_B1": 0,
            "JULIAN_DAY_B2": 18,
            "JULIAN_DAY_B3": 88,
            "JULIAN_SEC_FRAC": 0.8779999613761902,
            "KSPIN": 0,
            "LISTFR": 0,
            "MINUTE": 38,
            "MODE": 3,
            "MONTH": 11,
            "MSEC_OF_DAY": 59886877,
            "NFREQ": 16,
            "NFRPAL": 1,
            "NPALCY": 64,
            "NPALIF": 64,
            "NPBS": 11130,
            "NSPALF": 16,
            "NZPALF": 8,
            "P_FIELD": 76,
            "RECEIVER_CODE": 1,
            "SDURCY": 183.23672485351562,
            "SDURPA": 2.8630738258361816,
            "SECOND": 6,
            "SPIN_RATE": 129.59471130371094,
            "SUN_ANGLE": 190.1953125,
            "YEAR": 1994,
        }
        assert list(data_i.keys()) == ["FREQ", "VSPAL", "VZPAL", "TSPAL", "TZPAL"]
        assert data_i["FREQ"][0] == 1040.0
        assert data_i["FREQ"][-1] == 20.0


def test_wi_wa_rad2_l2_60s_bin_dataset():
    for filepath in TEST_FILES["wi_wa_rad2_l2_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesRad2L260sBinData)


def test_wi_wa_tnr_l2_60s_bin_dataset():
    for filepath in TEST_FILES["wi_wa_tnr_l2_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesTnrL260sBinData)


def test_wi_wa_tnr_l3_bqt_1mn_bin_dataset():
    for filepath in TEST_FILES["wi_wa_tnr_l3_bqt_1mn"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesTnrL3Bqt1mnBinData)


def test_wi_wa_tnr_l3_nn_bin_dataset():
    for filepath in TEST_FILES["wi_wa_tnr_l3_nn"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesTnrL3NnBinData)


def test_win_rad1_60s_bin_dataset():
    for filepath in TEST_FILES["win_rad1_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesRad160sBinData)


def test_win_rad2_60s_bin_dataset():
    for filepath in TEST_FILES["win_rad2_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesRad260sBinData)


def test_win_tnr_60s_bin_dataset():
    for filepath in TEST_FILES["win_tnr_60s"]:
        data = Data(filepath=filepath)
        assert isinstance(data, WindWavesTnr60sBinData)


def test_srn_nda_routine_jup_edr_dataset():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        data = Data(filepath=filepath)
        assert isinstance(data, SrnNdaRoutineJupEdrCdfData)


def test_srn_nda_routine_jup_edr_dataset__times():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 28734
            assert data.times[0] == Time("2016-01-30 22:47:06.03")
            assert data.times[-1] == Time("2016-01-31 06:45:58.68")


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


def test_srn_nda_routine_jup_edr_dataset__access_mode_error():
    with pytest.raises(ValueError):
        Data(
            filepath=TEST_FILES["srn_nda_routine_jup_edr"][0],
            access_mode="toto",
        )


def test_nenufar_bst_dataset():
    for filepath in TEST_FILES["nenufar_bst"]:
        data = Data(filepath=filepath)
        assert isinstance(data, NenufarBstFitsData)


def test_nenufar_bst_dataset__beam():
    for filepath in TEST_FILES["nenufar_bst"]:
        data = Data(filepath=filepath, beam=1)
        assert data.beam == 1


def test_nenufar_bst_dataset__beam__value_error():
    for filepath in TEST_FILES["nenufar_bst"]:
        with pytest.raises(ValueError):
            Data(filepath=filepath, beam=1000)


def test_nenufar_bst_dataset__access_mode_file():
    for filepath in TEST_FILES["nenufar_bst"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, fits.hdu.hdulist.HDUList)


def test_nenufar_bst_dataset__times():
    for filepath in TEST_FILES["nenufar_bst"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 3600
            assert data.times[0] == Time(2459609.9792824076, format="jd")
            assert data.times[-1] == Time(2459610.0209375, format="jd")


def test_nenufar_bst_dataset__times__other_beam():
    for filepath in TEST_FILES["nenufar_bst"]:
        with Data(filepath=filepath, beam=1) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 3600
            assert data.times[0] == Time(2459609.9792824076, format="jd")
            assert data.times[-1] == Time(2459610.0209375, format="jd")


def test_nenufar_bst_dataset__frequencies():
    for filepath in TEST_FILES["nenufar_bst"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.frequencies, Quantity)
            assert len(data.frequencies) == 192
            assert data.frequencies[0] == 25 * Unit("MHz")
            assert data.frequencies[-1].value == pytest.approx(62.304688)


def test_ecallisto_dataset():
    for filepath in TEST_FILES["ecallisto"]:
        data = Data(filepath=filepath)
        assert isinstance(data, ECallistoFitsData)


def test_ecallisto_dataset__access_mode_file():
    for filepath in TEST_FILES["ecallisto"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, fits.hdu.hdulist.HDUList)


def test_ecallisto_dataset__times():
    for filepath in TEST_FILES["ecallisto"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 3600
            assert data.times[0] == Time("2022-01-30 11:15:00.171")
            assert data.times[-1].jd == pytest.approx(
                Time("2022-01-30 11:29:59.921").jd
            )


def test_ecallisto_dataset__frequencies():
    for filepath in TEST_FILES["ecallisto"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.frequencies, Quantity)
            assert len(data.frequencies) == 200
            assert data.frequencies[0] == 105.5 * Unit("MHz")
            assert data.frequencies[-1] == 10 * Unit("MHz")


def test_vg1_j_pra_3_rdr_lowband_6sec_v1_dataset():
    for filepath in TEST_FILES["vg1_j_pra_3_rdr_lowband_6sec_v1"]:
        data = Data(filepath=filepath)
        assert isinstance(data, Vg1JPra3RdrLowband6secV1Data)


def test_vg1_j_pra_3_rdr_lowband_6sec_v1_dataset__access_mode_file():
    for filepath in TEST_FILES["vg1_j_pra_3_rdr_lowband_6sec_v1"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, dict)
