# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.base import BinData
from maser.data.padc.cassini.data import CoRpwsHfrKronosBgData

from astropy.time import Time
from pathlib import Path

from xarray.core.dataarray import DataArray
import xarray

TEST_FILES = {
    "co_rpws_hfr_kronos_bg": [
        BASEDIR / "kronos" / "2012_091_180" / "bg" / "bg_2012_091_180",
    ],
}


# Cassini/RPWS/HFR Kronos BG TESTS ==== co_rpws_hfr_kronos_bg
@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_bg_bin_dataset():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_bg"]:
        data = Data(filepath=filepath)
        assert isinstance(data, BinData)
        assert isinstance(data, CoRpwsHfrKronosBgData)
        assert data.level == "bg"


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_bg_bin_dataset__len():
    filepath = TEST_FILES["co_rpws_hfr_kronos_bg"][0]
    data = Data(filepath=filepath)
    assert data._nsweep == 1
    assert data._nrecord == 763
    assert data.file_size.value == 19624360


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_bg_bin_dataset__len_records():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_bg"]:
        data = Data(filepath=filepath, access_mode="records")
        assert len(data) == 1


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_bg_bin_dataset__len_sweeps():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_bg"]:
        data = Data(filepath=filepath, access_mode="sweeps")
        assert len(data) == data._nsweep


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_bg1_bin_dataset__times_sweeps():
    filepath = TEST_FILES["co_rpws_hfr_kronos_bg"][0]
    data = Data(filepath=filepath)
    assert isinstance(data.times, Time)
    assert data.times[0] == Time("2012-03-31 00:00:00")


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_bg_bin_dataset__as_xarray():
    filepath = TEST_FILES["co_rpws_hfr_kronos_bg"][0]
    data = Data(filepath=filepath)
    xarr = data.as_xarray()
    assert isinstance(xarr, xarray.Dataset)
    xarr_keys = xarr.keys()
    assert set(xarr_keys) == set(data._format["vars"].keys())
    for k in xarr_keys:
        assert isinstance(xarr[k], DataArray)
    assert set(data.dataset_keys) == set(list(xarr.keys()))


@pytest.mark.test_data_required
def test_co_rpws_hfr_kronos_bg_bin_dataset__quicklook():
    for filepath in TEST_FILES["co_rpws_hfr_kronos_bg"]:
        # ql_path = BASEDIR.parent / "quicklook" / "kronos" / f"{filepath.name}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        # data.quicklook(ql_path)

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        # data.quicklook(ql_path_tmp, keys=data.dataset_keys)  # will not work for bg since keys are not used as keys
        # assert ql_path_tmp.is_file()
        # ql_path_tmp.unlink()
