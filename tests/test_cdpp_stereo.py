# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.base import BinData
from maser.data.cdpp.stereo.data import (
    StereoWavesL2HighResBinData,
)
from pathlib import Path
import xarray

TEST_FILES = {
    "cdpp_sta_l2_wav_h_res_lfr": [
        BASEDIR / "cdpp" / "stereo" / "STA_WAV_LFR_20070131.B3E",
    ],
    "cdpp_stb_l2_wav_h_res_lfr": [
        BASEDIR / "cdpp" / "stereo" / "STB_WAV_LFR_20070131.B3E",
    ],
    "cdpp_sta_l2_wav_h_res_hfr": [
        BASEDIR / "cdpp" / "stereo" / "STA_WAV_HFR_20070131.B3E",
    ],
    "cdpp_stb_l2_wav_h_res_hfr": [
        BASEDIR / "cdpp" / "stereo" / "STB_WAV_HFR_20070131.B3E",
    ],
}

# create a decorator to test each file in the list
for_each_test_l2_file = pytest.mark.parametrize(
    "filepath",
    TEST_FILES["cdpp_sta_l2_wav_h_res_lfr"]
    + TEST_FILES["cdpp_stb_l2_wav_h_res_lfr"]
    + TEST_FILES["cdpp_sta_l2_wav_h_res_hfr"]
    + TEST_FILES["cdpp_stb_l2_wav_h_res_hfr"],
)


@pytest.mark.test_data_required
@for_each_test_l2_file
def test_swaves_l2_bin_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, BinData)
    assert isinstance(data, StereoWavesL2HighResBinData)


@pytest.mark.test_data_required
def test_swaves_l2_bin_dataset__frequencies():
    filepath = TEST_FILES["cdpp_sta_l2_wav_h_res_lfr"][0]
    data = Data(filepath)
    freq = data.frequencies
    assert isinstance(freq, list)


@pytest.mark.test_data_required
def test_swaves_l2_bin_dataset__as_xarray():
    filepath = TEST_FILES["cdpp_sta_l2_wav_h_res_lfr"][0]
    # with Data(filepath=filepath, access_mode="file") as data:
    #    assert isinstance(data, dict)
    datax = Data(filepath=filepath)
    xr = datax.as_xarray()
    assert isinstance(xr, xarray.Dataset)
    assert set(xr.keys()) == {"agc1", "agc2", "auto1", "auto2", "crossr", "crossi"}
    assert xr["agc1"].attrs["units"] == "ADU"
    assert set(datax.dataset_keys) == set(list(xr.keys()))


@pytest.mark.test_data_required
#  @for_each_test_l2_file
def test_swaves_l2_bin_dataset_quicklook():  # filepath):
    filepath = TEST_FILES["cdpp_sta_l2_wav_h_res_lfr"][0]
    ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
    data = Data(filepath=filepath)

    # checking default
    data.quicklook(ql_path_tmp)
    assert ql_path_tmp.is_file()
    ql_path_tmp.unlink()

    # checking all
    data.quicklook(ql_path_tmp, keys=data.dataset_keys)
    assert ql_path_tmp.is_file()
    ql_path_tmp.unlink()
