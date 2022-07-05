# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit
from .constants import BASEDIR
from maser.data import Data
from maser.data.nancay import (
    SrnNdaRoutineJupEdrCdfData,
    NenufarBstFitsData,
)
from astropy.io import fits
import pytest
from .fixtures import skip_if_nenupy_not_available, skip_if_spacepy_not_available


TEST_FILES = {
    "srn_nda_routine_jup_edr": [
        BASEDIR
        / "nda"
        / "routine"
        / "srn_nda_routine_jup_edr_201601302247_201601310645_V12.cdf"
    ],
    "srn_nenufar_bst": [
        BASEDIR
        / "nenufar"
        / "bst"
        / "20220130_112900_20220130_123100_SUN_TRACKING"
        / "20220130_112900_BST.fits"
    ],
}


# NANCAY TESTS
@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_jup_edr_dataset():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        data = Data(filepath=filepath)
        assert isinstance(data, SrnNdaRoutineJupEdrCdfData)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_jup_edr_dataset__times():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 28734
            assert data.times[0] == Time("2016-01-30 22:47:06.03")
            assert data.times[-1] == Time("2016-01-31 06:45:58.68")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_jup_edr_dataset__frequencies():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.frequencies, Quantity)
            assert len(data.frequencies) == 400
            assert data.frequencies[0].to(Unit("MHz")).value == pytest.approx(10)
            assert data.frequencies[-1].to(Unit("MHz")).value == pytest.approx(39.925)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_jup_edr_dataset__access_mode_file():
    for filepath in TEST_FILES["srn_nda_routine_jup_edr"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, pycdf.CDF)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
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


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_jup_edr_dataset__access_mode_error():
    with pytest.raises(ValueError):
        Data(
            filepath=TEST_FILES["srn_nda_routine_jup_edr"][0],
            access_mode="toto",
        )


@pytest.mark.test_data_required
@skip_if_nenupy_not_available
def test_nenufar_bst_dataset():
    for filepath in TEST_FILES["srn_nenufar_bst"]:
        data = Data(filepath=filepath)
        assert isinstance(data, NenufarBstFitsData)


@pytest.mark.test_data_required
@skip_if_nenupy_not_available
def test_nenufar_bst_dataset__beam():
    for filepath in TEST_FILES["srn_nenufar_bst"]:
        data = Data(filepath=filepath, beam=1)
        assert data.beam == 1


@pytest.mark.test_data_required
@skip_if_nenupy_not_available
def test_nenufar_bst_dataset__beam__value_error():
    for filepath in TEST_FILES["srn_nenufar_bst"]:
        with pytest.raises(ValueError):
            Data(filepath=filepath, beam=1000)


@pytest.mark.test_data_required
@skip_if_nenupy_not_available
def test_nenufar_bst_dataset__access_mode_file():
    for filepath in TEST_FILES["srn_nenufar_bst"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, fits.hdu.hdulist.HDUList)


@pytest.mark.test_data_required
@skip_if_nenupy_not_available
def test_nenufar_bst_dataset__times():
    filepath = TEST_FILES["srn_nenufar_bst"][0]
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 3600
        assert data.times[0] == Time(2459609.9792824076, format="jd")
        assert data.times[-1] == Time(2459610.0209375, format="jd")


@pytest.mark.test_data_required
@skip_if_nenupy_not_available
def test_nenufar_bst_dataset__times__other_beam():
    filepath = TEST_FILES["srn_nenufar_bst"][0]
    with Data(filepath=filepath, beam=1) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 3600
        assert data.times[0] == Time(2459609.9792824076, format="jd")
        assert data.times[-1] == Time(2459610.0209375, format="jd")


@pytest.mark.test_data_required
@skip_if_nenupy_not_available
def test_nenufar_bst_dataset__frequencies():
    filepath = TEST_FILES["srn_nenufar_bst"][0]
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 192
        assert data.frequencies[0] == 25 * Unit("MHz")
        assert data.frequencies[-1].value == pytest.approx(62.304688)
