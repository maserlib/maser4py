# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit
from .constants import BASEDIR
from maser.data import Data
from maser.data.nancay import (
    OrnNdaRoutineJupEdrCdfData,
    OrnNdaRoutineSunEdrCdfData,
    OrnNdaNewRoutineJupEdrFitsData,
)
import pytest
from .fixtures import skip_if_spacepy_not_available
import xarray
from pathlib import Path

TEST_FILES = {
    "orn_nda_routine_jup_edr": [
        BASEDIR
        / "nda"
        / "routine"
        / "srn_nda_routine_jup_edr_201601302247_201601310645_V12.cdf"
    ],
    "orn_nda_routine_sun_edr": [
        BASEDIR
        / "nda"
        / "routine"
        / "srn_nda_routine_sun_edr_202305231352_202305231534_V17.cdf"
    ],
    "orn_nda_newroutine_jup_edr": [
        BASEDIR
        / "nda"
        / "newroutine"
        / "orn_nda_newroutine_jup_edr_202303060945_202303061745_v1.1.fits",
    ],
    "orn_nda_newroutine_sun_edr": [
        BASEDIR
        / "nda"
        / "newroutine"
        / "orn_nda_newroutine_sun_edr_202303070802_202303070936_v1.1.fits",
    ],
    "orn_nda_mefisto_sun_edr": [
        BASEDIR
        / "nda"
        / "mefisto"
        / "orn_nda_mefisto_sun_edr_202303070802_202303070937_v1.0.fits",
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


@pytest.mark.test_data_required
def test_orn_nda_routine_jup_edr_dataset_as_xarray():
    for filepath in TEST_FILES["orn_nda_routine_jup_edr"]:
        data = Data(filepath=filepath)
        xr = data.as_xarray()
        assert isinstance(xr, xarray.Dataset)
        assert set(xr.keys()) == {"LL", "RR"}
        assert xr["LL"].shape == (400, 28734)
        assert xr["LL"].attrs["units"] == "dB"
        assert (
            xr["LL"].attrs["title"]
            == "Flux density spectrogram measured on the LH polarized array."
        )
        assert set(data.dataset_keys) == set(list(xr.keys()))


@pytest.mark.test_data_required
def test_orn_nda_routine_jup_edr_dataset_quicklook():
    for filepath in TEST_FILES["orn_nda_routine_jup_edr"]:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_sun_edr_dataset():
    for filepath in TEST_FILES["orn_nda_routine_sun_edr"]:
        data = Data(filepath=filepath)
        assert isinstance(data, OrnNdaRoutineSunEdrCdfData)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_sun_edr_dataset__times():
    for filepath in TEST_FILES["orn_nda_routine_sun_edr"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 6169
            assert data.times[0] == Time("2023-05-23 13:52:11.60")
            assert data.times[-1] == Time("2023-05-23 15:34:59.56")


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_sun_edr_dataset__frequencies():
    for filepath in TEST_FILES["orn_nda_routine_sun_edr"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.frequencies, Quantity)
            assert len(data.frequencies) == 400
            assert data.frequencies[0].to(Unit("MHz")).value == pytest.approx(10)
            assert data.frequencies[-1].to(Unit("MHz")).value == pytest.approx(79.825)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_sun_edr_dataset__access_mode_file():
    from spacepy import pycdf

    for filepath in TEST_FILES["orn_nda_routine_sun_edr"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, pycdf.CDF)


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_sun_edr_dataset__iter_method__mode_file():
    for filepath in TEST_FILES["orn_nda_routine_sun_edr"]:
        data = Data(filepath=filepath, access_mode="file")
        var_labels = [item for item in data]
        assert list(data.file) == var_labels
        assert var_labels == [
            "Epoch",
            "Frequency",
            "RR",
            "LL",
            "STATUS",
            "SWEEP_TIME_OFFSET_RAMP",
            "RR_SWEEP_TIME_OFFSET",
        ]


@pytest.mark.test_data_required
@skip_if_spacepy_not_available
def test_srn_nda_routine_sun_edr_dataset__access_mode_error():
    with pytest.raises(ValueError):
        Data(
            filepath=TEST_FILES["orn_nda_routine_sun_edr"][0],
            access_mode="toto",
        )


@pytest.mark.test_data_required
def test_orn_nda_routine_sun_edr_dataset_as_xarray():
    for filepath in TEST_FILES["orn_nda_routine_sun_edr"]:
        data = Data(filepath=filepath)
        xr = data.as_xarray()
        assert isinstance(xr, xarray.Dataset)
        assert set(xr.keys()) == {"LL", "RR"}
        assert xr["LL"].shape == (400, 6169)  # 28734)
        assert xr["LL"].attrs["units"] == "dB"
        assert (
            xr["LL"].attrs["title"]
            == "Flux density spectrogram measured on the LH polarized array."
        )
        assert set(data.dataset_keys) == set(list(xr.keys()))


@pytest.mark.test_data_required
def test_orn_nda_routine_sun_edr_dataset_quicklook():
    for filepath in TEST_FILES["orn_nda_routine_sun_edr"]:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# NDA NewRoutine TESTS


@pytest.mark.test_data_required
def test_orn_nda_newroutine_jup_edr_dataset():
    for filepath in TEST_FILES["orn_nda_newroutine_jup_edr"]:
        data = Data(filepath=filepath)
        assert isinstance(data, OrnNdaNewRoutineJupEdrFitsData)


@pytest.mark.test_data_required
def test_orn_nda_newroutine_jup_edr_dataset_times():
    for filepath in TEST_FILES["orn_nda_newroutine_jup_edr"]:
        data = Data(filepath=filepath)
        times = data.times
        assert isinstance(times, Time)
        assert len(times) == 58186
        assert times[0].iso == "2023-03-06 09:45:15.260"
        assert times[-1].iso == "2023-03-06 17:45:00.246"


@pytest.mark.test_data_required
def test_orn_nda_newroutine_jup_edr_dataset_frequencies():
    for filepath in TEST_FILES["orn_nda_newroutine_jup_edr"]:
        data = Data(filepath=filepath)
        freqs = data.frequencies
        assert isinstance(freqs, Quantity)
        assert len(freqs) == 615
        assert freqs[0].value == pytest.approx(10.009766)
        assert freqs[-1].value == pytest.approx(39.990234)
        assert freqs.unit == "MHz"


@pytest.mark.test_data_required
def test_orn_nda_newroutine_jup_edr_dataset_as_xarray():
    for filepath in TEST_FILES["orn_nda_newroutine_jup_edr"]:
        data = Data(filepath=filepath)
        xr = data.as_xarray()
        assert isinstance(xr, xarray.Dataset)
        assert set(xr.keys()) == {"LL", "RR", "LR_RE", "LR_IM"}
        assert xr["LL"].shape == (615, 58186)
        assert xr["LL"].attrs["units"] == "V**2/Hz"
        assert (
            xr["LL"].attrs["title"]
            == "ORN NDA newroutine JUPITER EDR Dataset (LL component)"
        )
        assert set(data.dataset_keys) == set(list(xr.keys()))


@pytest.mark.test_data_required
def test_orn_nda_newroutine_jup_edr_dataset_quicklook():
    for filepath in TEST_FILES["orn_nda_newroutine_jup_edr"]:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


@pytest.mark.test_data_required
def test_orn_nda_newroutine_sun_edr_dataset_as_xarray():
    for filepath in TEST_FILES["orn_nda_newroutine_sun_edr"]:
        data = Data(filepath=filepath)
        xr = data.as_xarray()
        assert isinstance(xr, xarray.Dataset)
        assert set(xr.keys()) == {"LL", "RR"}
        assert xr["LL"].shape == (1598, 11538)
        assert xr["LL"].attrs["units"] == "V**2/Hz"
        assert (
            xr["LL"].attrs["title"]
            == "ORN NDA newroutine SUN EDR Dataset (LL component)"
        )
        assert set(data.dataset_keys) == set(list(xr.keys()))


@pytest.mark.test_data_required
def test_orn_nda_newroutine_sun_edr_dataset_quicklook():
    for filepath in TEST_FILES["orn_nda_newroutine_sun_edr"]:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()


# NDA Mefisto TESTS


@pytest.mark.test_data_required
def test_orn_nda_mefisto_sun_edr_dataset_as_xarray():
    for filepath in TEST_FILES["orn_nda_mefisto_sun_edr"]:
        data = Data(filepath=filepath)
        xr = data.as_xarray()
        assert isinstance(xr, xarray.Dataset)
        assert set(xr.keys()) == {"LL", "RR"}
        assert xr["LL"].shape == (390, 53066)
        assert xr["LL"].attrs["units"] == "V**2/Hz"
        assert (
            xr["LL"].attrs["title"] == "ORN NDA mefisto SUN EDR Dataset (LL component)"
        )
        assert set(data.dataset_keys) == set(list(xr.keys()))


@pytest.mark.test_data_required
def test_orn_nda_mefisto_sun_edr_dataset_quicklook():
    for filepath in TEST_FILES["orn_nda_mefisto_sun_edr"]:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        data.quicklook(ql_path_tmp, keys=data.dataset_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()
