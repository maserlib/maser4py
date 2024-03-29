# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.base import CdfData
from maser.data.padc.stereo.data import StWavL3Cdf
from astropy.units import Quantity
from astropy.time import Time

from .fixtures import skip_if_spacepy_not_available

TEST_FILES = {
    "sta_l3_wav_lfr": [
        BASEDIR / "swaves" / "l3_cdf" / "sta_l3_wav_lfr_20200711_v01.cdf",
    ],
    "stb_l3_wav_lfr": [
        BASEDIR / "swaves" / "l3_cdf" / "stb_l3_wav_lfr_20200711_v01.cdf",
    ],
    "sta_l3_wav_hfr": [
        BASEDIR / "swaves" / "l3_cdf" / "sta_l3_wav_hfr_20200711_v01.cdf",
    ],
    "stb_l3_wav_hfr": [
        BASEDIR / "swaves" / "l3_cdf" / "stb_l3_wav_hfr_20200711_v01.cdf",
    ],
}

# create a decorator to test each file in the list
for_each_test_l3_file = pytest.mark.parametrize(
    "filepath",
    TEST_FILES["sta_l3_wav_lfr"]
    + TEST_FILES["stb_l3_wav_lfr"]
    + TEST_FILES["sta_l3_wav_hfr"]
    + TEST_FILES["stb_l3_wav_hfr"],
)


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
@for_each_test_l3_file
def test_swaves_l3_df_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, CdfData)
    assert isinstance(data, StWavL3Cdf)


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_swaves_l3_cdf_dataset__frequencies():
    filepath = TEST_FILES["sta_l3_wav_hfr"][0]
    data = Data(filepath=filepath)
    assert isinstance(data.frequencies, Quantity)
    assert len(data.frequencies) == 319
    assert data.frequencies.unit == "Hz"


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_swaves_l3_cdf_dataset__times():
    filepath = TEST_FILES["sta_l3_wav_hfr"][0]
    data = Data(filepath=filepath)
    assert isinstance(data.times, Time)
    assert len(data.times) == 2476
