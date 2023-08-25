# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit
from .constants import BASEDIR
from maser.data import Data
from maser.data.ecallisto import (
    ECallistoFitsData,
)
from pathlib import Path
from astropy.io import fits
import pytest
import xarray

TEST_FILES = {
    "ecallisto": [BASEDIR / "e-callisto" / "BIR" / "BIR_20220130_111500_01.fit"],
}


# ECALLISTO TESTS
@pytest.mark.test_data_required
def test_ecallisto_dataset():
    for filepath in TEST_FILES["ecallisto"]:
        data = Data(filepath=filepath)
        assert isinstance(data, ECallistoFitsData)


@pytest.mark.test_data_required
def test_ecallisto_dataset__access_mode_file():
    for filepath in TEST_FILES["ecallisto"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, fits.hdu.hdulist.HDUList)


@pytest.mark.test_data_required
def test_ecallisto_dataset__times():
    for filepath in TEST_FILES["ecallisto"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.times, Time)
            assert len(data.times) == 3600
            assert data.times[0].jd == pytest.approx(Time("2022-01-30 11:15:00.171").jd)
            assert data.times[-1].jd == pytest.approx(
                Time("2022-01-30 11:29:59.921").jd
            )


@pytest.mark.test_data_required
def test_ecallisto_dataset__frequencies():
    for filepath in TEST_FILES["ecallisto"]:
        with Data(filepath=filepath) as data:
            assert isinstance(data.frequencies, Quantity)
            assert len(data.frequencies) == 200
            assert data.frequencies[0] == 105.5 * Unit("MHz")
            assert data.frequencies[-1] == 10 * Unit("MHz")


@pytest.mark.test_data_required
def test_ecallisto_dataset_as_xarray():
    for filepath in TEST_FILES["ecallisto"]:
        data = Data(filepath=filepath)
        xr = data.as_xarray()
        assert isinstance(xr, xarray.Dataset)
        assert set(xr.keys()) == {"Flux Density", "Flux Density"}
        assert xr["Flux Density"].shape == (200, 3600)
        assert xr["Flux Density"].attrs["units"] == "digits"
        assert (
            xr["Flux Density"].attrs["title"]
            == "2022/01/30  Radio flux density, e-CALLISTO (BIR)"
        )


@pytest.mark.test_data_required
def test_ecallisto_dataset_quicklook():
    for filepath in TEST_FILES["ecallisto"]:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        data.quicklook(ql_path_tmp)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()
