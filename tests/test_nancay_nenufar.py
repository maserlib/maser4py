# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity, Unit
from .constants import BASEDIR
from maser.data import Data
from maser.data.nancay import (
    OrnNenufarBstFitsData,
)
from pathlib import Path
from astropy.io import fits
import pytest
import xarray


TEST_FILES = {
    "srn_nenufar_bst": [
        BASEDIR
        / "nenufar"
        / "bst"
        / "20220130_112900_20220130_123100_SUN_TRACKING"
        / "20220130_112900_BST.fits"
    ],
}


@pytest.mark.test_data_required
def test_nenufar_bst_dataset():
    for filepath in TEST_FILES["srn_nenufar_bst"]:
        data = Data(filepath=filepath)
        assert isinstance(data, OrnNenufarBstFitsData)


@pytest.mark.test_data_required
def test_nenufar_bst_dataset__beam():
    for filepath in TEST_FILES["srn_nenufar_bst"]:
        data = Data(filepath=filepath, beam=1)
        assert data.beam == 1


@pytest.mark.test_data_required
def test_nenufar_bst_dataset__beam__value_error():
    for filepath in TEST_FILES["srn_nenufar_bst"]:
        with pytest.raises(ValueError):
            Data(filepath=filepath, beam=1000)


@pytest.mark.test_data_required
def test_nenufar_bst_dataset__access_mode_file():
    for filepath in TEST_FILES["srn_nenufar_bst"]:
        with Data(filepath=filepath, access_mode="file") as data:
            assert isinstance(data, fits.hdu.hdulist.HDUList)


@pytest.mark.test_data_required
def test_nenufar_bst_dataset__times():
    filepath = TEST_FILES["srn_nenufar_bst"][0]
    with Data(filepath=filepath) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 3600
        assert data.times[0] == Time(2459609.9792824076, format="jd")
        assert data.times[-1] == Time(2459610.0209375, format="jd")


@pytest.mark.test_data_required
def test_nenufar_bst_dataset__times__other_beam():
    filepath = TEST_FILES["srn_nenufar_bst"][0]
    with Data(filepath=filepath, beam=1) as data:
        assert isinstance(data.times, Time)
        assert len(data.times) == 3600
        assert data.times[0] == Time(2459609.9792824076, format="jd")
        assert data.times[-1] == Time(2459610.0209375, format="jd")


@pytest.mark.test_data_required
def test_nenufar_bst_dataset__frequencies():
    filepath = TEST_FILES["srn_nenufar_bst"][0]
    with Data(filepath=filepath) as data:
        assert isinstance(data.frequencies, Quantity)
        assert len(data.frequencies) == 192
        assert data.frequencies[0] == 25 * Unit("MHz")
        assert data.frequencies[-1].value == pytest.approx(62.304688)


@pytest.mark.test_data_required
def test_nenufar_bst_dataset_as_xarray():
    for filepath in TEST_FILES["srn_nenufar_bst"]:
        data = Data(filepath=filepath)
        xr = data.as_xarray()
        assert isinstance(xr, xarray.Dataset)
        assert set(xr.keys()) == {"NW", "NE"}
        assert xr["NW"].shape == (192, 3600)
        assert xr["NW"].attrs["units"] == ""
        assert xr["NW"].attrs["title"] == ""


@pytest.mark.test_data_required
def test_nenufar_bst_dataset_quicklook():
    for filepath in TEST_FILES["srn_nenufar_bst"]:
        #  ql_path = BASEDIR.parent / "quicklook" / "nda" / f"{filepath.stem}.png"
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath)
        data.quicklook(ql_path_tmp)
        #  assert open(ql_path, "rb").read() == open(ql_path_tmp, "rb").read()
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()
