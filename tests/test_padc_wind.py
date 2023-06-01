# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.base import CdfData
from maser.data.padc.wind.data import WindWavesRad1L3AkrData, WindWavesRad1L3DfV01Data
from astropy.units import Quantity
from astropy.time import Time
import xarray


from .fixtures import skip_if_spacepy_not_available

TEST_FILES = {
    "wi_wa_rad1_l3-akr": [
        BASEDIR / "maser" / "wind" / "wi_wa_rad1_l3-akr_19990101_v01.cdf",
    ],
    "wi_wav_rad1_l3_df_v01": [
        BASEDIR / "maser" / "wind" / "wi_wa_rad1_l3_df_19950119_v01.cdf",
    ],
}


@pytest.fixture
def wind_waves_l3_akr_file():
    return TEST_FILES["wi_wa_rad1_l3-akr"][0]


@pytest.fixture
def wind_waves_l3_df_file():
    return TEST_FILES["wi_wav_rad1_l3_df_v01"][0]


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_akr_dataset(wind_waves_l3_akr_file):
    data = Data(filepath=wind_waves_l3_akr_file)
    assert isinstance(data, CdfData)
    assert isinstance(data, WindWavesRad1L3AkrData)


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_akr_dataset__frequencies(wind_waves_l3_akr_file):
    data = Data(filepath=wind_waves_l3_akr_file)
    assert isinstance(data.frequencies, Quantity)
    assert len(data.frequencies) == 32
    assert data.frequencies.unit == "kHz"
    assert data.frequencies.value[0] == 20
    assert data.frequencies.value[-1] == 1040


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_akr_dataset__times(wind_waves_l3_akr_file):
    data = Data(filepath=wind_waves_l3_akr_file)
    assert isinstance(data.times, Time)
    assert len(data.times) == 471
    assert data.times[0].iso == "1999-01-01 00:00:52.605"
    assert data.times[1].iso == "1999-01-01 00:03:55.867"


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_akr_dataset__as_xarray(wind_waves_l3_akr_file):
    data = Data(filepath=wind_waves_l3_akr_file)
    xr = data.as_xarray()
    assert isinstance(xr, xarray.Dataset)
    assert set(xr.keys()) == {"FLUX_DENSITY", "SNR"}
    assert xr.coords.dims == {"time": 471, "frequency": 32}
    assert xr["SNR"].dims == ("frequency", "time")
    assert xr["SNR"].shape == (32, 471)
    assert xr["FLUX_DENSITY"].units == "Wm2Hz-1"


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_df_dataset(wind_waves_l3_df_file):
    data = Data(filepath=wind_waves_l3_df_file)
    assert isinstance(data, CdfData)
    assert isinstance(data, WindWavesRad1L3DfV01Data)


@skip_if_spacepy_not_available
@pytest.mark.test_data_required
def test_wind_waves_l3_df_dataset__frequencies(wind_waves_l3_df_file):
    data = Data(filepath=wind_waves_l3_df_file)
    assert isinstance(data.frequencies, Quantity)
    # assert len(data.frequencies) == 32
    assert data.frequencies.unit == "kHz"
