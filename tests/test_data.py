# -*- coding: utf-8 -*-
from maser.data import Data
from maser.data.data import (
    CdfData,
    SrnNdaRoutineJupEdrCdfData,
    FitsData,
    NenufarBstFitsData,
    Pds3Data,
    Vg1JPra3RdrLowband6secV1Data,
)
from pathlib import Path
from spacepy import pycdf
from astropy.io import fits


BASEDIR = Path(__file__).resolve().parent / "data"


def test_cdf_dataset():
    data = Data(filepath=Path("toto.txt"), dataset="cdf")
    assert isinstance(data, Data)
    assert isinstance(data, CdfData)


def test_fits_dataset():
    data = Data(filepath=Path("toto.txt"), dataset="fits")
    assert isinstance(data, Data)
    assert isinstance(data, FitsData)


def test_pds3_dataset():
    data = Data(filepath=Path("toto.txt"), dataset="pds3")
    assert isinstance(data, Data)
    assert isinstance(data, Pds3Data)


def test_srn_nda_routine_jup_edr_dataset():
    data = Data(
        filepath=BASEDIR
        / "nda"
        / "routine"
        / "srn_nda_routine_jup_edr_201601302247_201601310645_V12.cdf"
    )
    assert isinstance(data, SrnNdaRoutineJupEdrCdfData)


def test_srn_nda_routine_jup_edr_dataset__access_mode_raw():
    with Data(
        filepath=BASEDIR
        / "nda"
        / "routine"
        / "srn_nda_routine_jup_edr_201601302247_201601310645_V12.cdf",
        access_mode="raw",
    ) as data:
        assert isinstance(data, pycdf.CDF)


def test_nenufar_bst_dataset():
    data = Data(
        filepath=BASEDIR
        / "nenufar"
        / "bst"
        / "20220130_112900_20220130_123100_SUN_TRACKING"
        / "20220130_112900_BST.fits"
    )
    assert isinstance(data, NenufarBstFitsData)


def test_nenufar_bst_dataset__access_mode_raw():
    with Data(
        filepath=BASEDIR
        / "nenufar"
        / "bst"
        / "20220130_112900_20220130_123100_SUN_TRACKING"
        / "20220130_112900_BST.fits",
        access_mode="raw",
    ) as data:
        assert isinstance(data, list)
        for item in data:
            assert isinstance(item, fits.hdu.base._BaseHDU)


def test_pds_vg1_j_pra_3_rdr_lowband_6sec_v1_dataset():
    data = Data(
        filepath=BASEDIR / "pds" / "VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1" / "PRA_I.LBL"
    )
    assert isinstance(data, Vg1JPra3RdrLowband6secV1Data)
