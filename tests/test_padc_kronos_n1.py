# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.base import BinData
from maser.data.padc.cassini.data import CoRpwsHfrKronosN1Data

# from astropy.time import Time
# from astropy.units import Quantity, Unit
# import xarray

TEST_FILES = {
    "co_rpws_hfr_kronos_n1": [
        BASEDIR / "kronos" / "2012_091_180" / "n1" / "R2012180.20",
        BASEDIR / "kronos" / "2012_091_180" / "n1" / "R2012180.21",
        BASEDIR / "kronos" / "2012_091_180" / "n1" / "R2012180.22",
    ],
}


# CDPP/INTERBALL TESTS ==== int_aur_polrad_rst
@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_n1"]:
        data = Data(filepath=filepath)
        assert isinstance(data, BinData)
        assert isinstance(data, CoRpwsHfrKronosN1Data)


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__len():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n1"][0]
    data = Data(filepath=filepath)
    assert len(data) == 219
    assert data._nrecord == 78621
    assert data.file_size == 2201388


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__len_records():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n1"][0]
    data = Data(filepath=filepath, access_mode="records")
    assert len(data) == 78621


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_n1_bin_dataset__len_file():
    filepath = TEST_FILES["co_rpws_hfr_kronos_n1"][0]
    data = Data(filepath=filepath, access_mode="file")
    assert len(data) == 2201388
