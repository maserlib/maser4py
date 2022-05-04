# -*- coding: utf-8 -*-
from maser.data import Data
from maser.data.base import (
    BinData,
    CdfData,
    FitsData,
)
from .fixtures import test_filepaths, NOT_IMPLEMENTED_FILE
from pathlib import Path
import json
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


@pytest.mark.test_data_required
@pytest.mark.parametrize("filepath,dataset", test_filepaths())
def test_any_dataset(filepath, dataset):
    try:
        data = Data(filepath)
        assert data.dataset == dataset
    except NotImplementedError:
        with open(NOT_IMPLEMENTED_FILE, "r") as f:
            not_implemented = json.load(f)
        if dataset not in not_implemented:
            not_implemented.append(dataset)
        with open(NOT_IMPLEMENTED_FILE, "w") as f:
            json.dump(not_implemented, f)
        print(f"Dataset not implemented {str(filepath)}")


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
