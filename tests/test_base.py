# -*- coding: utf-8 -*-
from maser.data import Data
from maser.data.base import (
    BinData,
    CdfData,
    FitsData,
)
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
