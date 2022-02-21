# -*- coding: utf-8 -*-
from maser.data import Data
from maser.data.data import CdfData


def test_cdf_dataset():
    data = Data(filepath="toto.txt", dataset="cdf")
    assert isinstance(data, CdfData)
