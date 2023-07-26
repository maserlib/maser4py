# -*- coding: utf-8 -*-
from .constants import BASEDIR
import pytest
from maser.data import Data
from maser.data.base import CdfData
from maser.data.padc.juno import JnoWavLesiaL3aV02Data
from astropy.time import Time
from astropy.units import Quantity, Unit
import xarray
from .fixtures import skip_if_spacepy_not_available

TEST_FILES = {
    "jno_wav_cdr_lesia": [
        BASEDIR / "maser" / "juno" / "jno_wav_cdr_lesia_20170329_v02.cdf"
    ],
}

# create a decorator to test each file in the list
for_each_test_file = pytest.mark.parametrize(
    "filepath", TEST_FILES["jno_wav_cdr_lesia"]
)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_jno_wav_cdr_lesia_dataset(filepath):
    data = Data(filepath=filepath)
    assert isinstance(data, CdfData)
    assert isinstance(data, JnoWavLesiaL3aV02Data)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_jno_wav_cdr_lesia_dataset__times(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 86400
        assert data.times[0] == Time("2017-03-29 00:00:00.000")
        assert data.times[-1] == Time("2017-03-29 23:59:59.000")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_jno_wav_cdr_lesia__frequencies(filepath):
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 126
        assert data.frequencies[0].to(Unit("Hz")).value == pytest.approx(48.82799834)
        assert data.frequencies[-1].to(Unit("Hz")).value == pytest.approx(40500000.0)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_jno_wav_cdr_lesia__sweeps(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        sweep = next(data.sweeps)

        # check the sweep content
        assert isinstance(sweep, tuple)
        assert isinstance(sweep[0], Time)
        assert isinstance(sweep[1], Quantity)
        assert isinstance(sweep[2], Quantity)
        assert len(sweep[2]) == 126


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
@for_each_test_file
def test_jno_wav_cdr_lesia__as_xarray(filepath):
    with Data(filepath=filepath) as data:
        # get only the first sweep
        test_array = data.as_xarray()

        # check the sweep content
        assert isinstance(test_array, xarray.Dataset)
        assert test_array.coords["frequency"].data[0] == pytest.approx(0.048828)
        assert test_array["DEFAULT"].attrs["units"] == "V**2 m**-2 Hz**-1"
        assert test_array["DEFAULT"].data[0][0] == pytest.approx(3.211884e-06)
