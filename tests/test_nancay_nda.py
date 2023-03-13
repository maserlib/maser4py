# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit
from .constants import BASEDIR
from maser.data import Data
from maser.data.nancay import (
    OrnNdaRoutineJupEdrCdfData,
    OrnNdaNewRoutineJupEdrFitsData,
)
import pytest
from .fixtures import skip_if_spacepy_not_available


TEST_FILES = {
    "orn_nda_routine_jup_edr": [
        BASEDIR
        / "nda"
        / "routine"
        / "srn_nda_routine_jup_edr_201601302247_201601310645_V12.cdf"
    ],
    "orn_nda_newroutine_jup_edr": [
        BASEDIR
        / "nda"
        / "newroutine"
        / "orn_nda_newroutine_jup_edr_202303060945_202303061745_v1.1.fits",
    ],
}


# NDA Routine TESTS


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_jup_edr_dataset():
    for filepath in TEST_FILES["orn_nda_routine_jup_edr"]:
        data = Data(filepath=filepath)
        assert isinstance(data, OrnNdaRoutineJupEdrCdfData)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_jup_edr_dataset__times():
    for filepath in TEST_FILES["orn_nda_routine_jup_edr"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 28734
            assert data.times[0] == Time("2016-01-30 22:47:06.03")
            assert data.times[-1] == Time("2016-01-31 06:45:58.68")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_jup_edr_dataset__frequencies():
    for filepath in TEST_FILES["orn_nda_routine_jup_edr"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.frequencies, Quantity)
            assert len(data.frequencies) == 400
            assert data.frequencies[0].to(Unit("MHz")).value == pytest.approx(10)
            assert data.frequencies[-1].to(Unit("MHz")).value == pytest.approx(39.925)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_jup_edr_dataset__access_mode_file():
    from spacepy import pycdf

    for filepath in TEST_FILES["orn_nda_routine_jup_edr"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, pycdf.CDF)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_jup_edr_dataset__iter_method__mode_file():
    for filepath in TEST_FILES["orn_nda_routine_jup_edr"]:
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
            filepath=TEST_FILES["orn_nda_routine_jup_edr"][0],
            access_mode="toto",
        )


# NDA NewRoutine TESTS


@pytest.mark.test_data_required
def test_orn_nda_newroutine_jup_edr_dataset():
    for filepath in TEST_FILES["orn_nda_newroutine_jup_edr"]:
        data = Data(filepath=filepath)
        assert isinstance(data, OrnNdaNewRoutineJupEdrFitsData)
