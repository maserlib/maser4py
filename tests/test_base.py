# -*- coding: utf-8 -*-
from maser.data import Data
from maser.data.base import (
    BinData,
    CdfData,
    FitsData,
)
from .fixtures import filepaths_test
from pathlib import Path
import pytest
from .fixtures import skip_if_spacepy_not_available


# BASE TESTS
def test_dataset():
    with pytest.raises(NotImplementedError):
        Data(filepath=Path("toto.txt"))


@skip_if_spacepy_not_available
def test_cdf_dataset():
    data = Data(filepath=Path("toto.txt"), dataset="cdf")
    assert isinstance(data, Data)
    assert isinstance(data, CdfData)


def test_cdf_dataset__filepath_type():
    data = Data(filepath="toto.txt", dataset="cdf")
    assert isinstance(data.filepath, Path)


def test_fits_dataset():
    data = Data(filepath=Path("toto.txt"), dataset="fits")
    assert isinstance(data, Data)
    assert isinstance(data, FitsData)


def test_bin_dataset():
    data = Data(filepath=Path("toto.txt"), dataset="bin")
    assert isinstance(data, Data)
    assert isinstance(data, BinData)


@pytest.mark.test_data_required
@pytest.mark.parametrize("filepath,dataset", filepaths_test())
def test_any_dataset(filepath, dataset):
    data = Data(filepath)
    assert data.dataset == dataset


# TEST TEMPLATE
@pytest.mark.test_data_required
@pytest.mark.skip(reason="not implemented")
def test___bin_dataset():
    pass


@pytest.mark.test_data_required
@pytest.mark.skip(reason="not implemented")
def test___bin_dataset__times():
    pass


@pytest.mark.test_data_required
@pytest.mark.skip(reason="not implemented")
def test___bin_dataset__frequencies():
    pass


@pytest.mark.test_data_required
@pytest.mark.skip(reason="not implemented")
def test___bin_dataset__sweeps__load_data_false():
    pass


@pytest.mark.test_data_required
@pytest.mark.skip(reason="not implemented")
def test___bin_dataset__sweeps_for_loop():
    pass


@pytest.mark.test_data_required
@pytest.mark.skip(reason="not implemented")
def test___bin_dataset__sweeps_next():
    pass
