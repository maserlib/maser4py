# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.base import CdfData
from maser.data.padc.stereo.data import StWavL3Cdf
from astropy.units import Quantity
from astropy.time import Time

from .fixtures import skip_if_spacepy_not_available
from pathlib import Path
import xarray

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


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_swaves_l3_cdf_dataset_as_xarray():
    filepath = TEST_FILES["sta_l3_wav_hfr"][0]
    data = Data(filepath=filepath)
    xr = data.as_xarray()
    assert isinstance(xr, xarray.Dataset)
    assert set(xr.keys()) == {
        "STOKES_I",
        "STOKES_Q",
        "STOKES_U",
        "STOKES_V",
        "SOURCE_SIZE",
        "PSD_FLUX",
        "PSD_SFU",
        "WAVE_AZIMUTH_HCI",
        "WAVE_AZIMUTH_HEE",
        "WAVE_AZIMUTH_HEEQ",
        "WAVE_AZIMUTH_RTN",
        "WAVE_COLATITUDE_HCI",
        "WAVE_COLATITUDE_HEE",
        "WAVE_COLATITUDE_HEEQ",
        "WAVE_COLATITUDE_RTN",
    }
    assert xr["PSD_FLUX"].shape == (319, 2476)
    assert xr["PSD_FLUX"].attrs["units"] == "W/m^2/Hz"
    assert set(data.dataset_keys) == set(list(xr.keys()))


@pytest.mark.test_data_required
#  @for_each_test_l3_file
def test_swaves_l3_cdf_dataset_quicklook():
    filepath = TEST_FILES["sta_l3_wav_hfr"][0]
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
