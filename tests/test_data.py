# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit


from maser.data import Data
from maser.data.data import (
    CdfData,
    SrnNdaRoutineJupEdrCdfData,
    FitsData,
    NenufarBstFitsData,
    ECallistoFitsData,
    Pds3Data,
    Vg1JPra3RdrLowband6secV1Data,
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


def test_srn_nda_routine_jup_edr_dataset():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        data = Data(filepath=filepath)
        assert isinstance(data, SrnNdaRoutineJupEdrCdfData)


def test_srn_nda_routine_jup_edr_dataset__times():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            assert data.times[0] == Time("2016-01-30 22:47:06.03")
            assert data.times[-1] == Time("2016-01-31 06:45:58.68")


def test_srn_nda_routine_jup_edr_dataset__frequencies():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.frequencies, Quantity)
            assert data.frequencies[0].to(Unit("MHz")).value - 10.0 < 0.000001
            assert data.frequencies[-1].to(Unit("MHz")).value - 39.925 < 0.000001


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


def test_nenufar_bst_dataset__access_mode_file():
    for filepath in TEST_FILES["nenufar_bst"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, fits.hdu.hdulist.HDUList)


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
            assert data.times[0] == Time("2022-01-30 11:15:00.171")
            assert (data.times[-1] - Time("2022-01-30 11:29:59.921")).value < 1e-7


def test_vg1_j_pra_3_rdr_lowband_6sec_v1_dataset():
    for filepath in TEST_FILES["vg1_j_pra_3_rdr_lowband_6sec_v1"]:
        data = Data(filepath=filepath)
        assert isinstance(data, Vg1JPra3RdrLowband6secV1Data)


def test_vg1_j_pra_3_rdr_lowband_6sec_v1_dataset__access_mode_file():
    for filepath in TEST_FILES["vg1_j_pra_3_rdr_lowband_6sec_v1"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, dict)
