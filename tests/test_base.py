# -*- coding: utf-8 -*-
from maser.data import Data
from maser.data.base import (
    BinData,
    CdfData,
    FitsData,
)
from .fixtures import test_filepaths
from pathlib import Path
import pytest


# BASE TESTS
def test_dataset():
    with pytest.raises(NotImplementedError):
        Data(filepath=Path("toto.txt"))


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


def test_any_dataset():
    for filepath, dataset in test_filepaths():
        try:
            data = Data(filepath)
            assert data.dataset == dataset
        except NotImplementedError:
            print(f"Dataset not implemented {str(filepath)}")


# TEST TEMPLATE
@pytest.mark.test_data_required
def test___bin_dataset():
    pass


@pytest.mark.test_data_required
def test___bin_dataset__times():
    pass


@pytest.mark.test_data_required
def test___bin_dataset__frequencies():
    pass


@pytest.mark.test_data_required
def test___bin_dataset__sweeps__load_data_false():
    pass


@pytest.mark.test_data_required
def test___bin_dataset__sweeps_for_loop():
    pass


@pytest.mark.test_data_required
def test___bin_dataset__sweeps_next():
    pass
