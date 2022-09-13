# -*- coding: utf-8 -*-
from astropy.time import Time
from .constants import BASEDIR
from maser.data import Data
from maser.data.cdpp import (
    VikingV4nE5BinData,
)
import pytest

TEST_FILES = {
    "cdpp_viking_v4n_e5": [BASEDIR / "cdpp" / "viking" / "V4N_0101_003"],
}


# CDPP/VIKING TESTS ==== viking_v4n_e5
@pytest.mark.test_data_required
def test_viking_v4n_e5_bin_dataset():
    for filepath in TEST_FILES["cdpp_viking_v4n_e5"]:
        data = Data(filepath=filepath)
        assert isinstance(data, VikingV4nE5BinData)


@pytest.mark.test_data_required
@pytest.mark.skip(reason="not fully implemented yet")
def test_viking_v4n_e5_bin_dataset__times():
    filepath = TEST_FILES["cdpp_viking_v4n_e5"][0]
    data = Data(filepath=filepath)
    assert isinstance(data.times, Time)
    assert len(data.times) == 120
    assert data.times[0] == Time("1994-11-10 16:38:06.000")
    assert data.times[-1] == Time("1994-11-10 23:55:27.000")


@pytest.mark.test_data_required
def test_viking_v4n_e5_bin_dataset__frequencies():
    pass


@pytest.mark.test_data_required
def test_viking_v4n_e5_bin_dataset__sweeps_access_mode__error():
    with pytest.raises(ValueError):
        filepath = TEST_FILES["cdpp_viking_v4n_e5"][0]
        Data(filepath=filepath, access_mode="sweeps")
