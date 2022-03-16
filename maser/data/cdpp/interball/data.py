# -*- coding: utf-8 -*-
from maser.data.base import BinData
from .sweeps import InterballAuroralPolradRspSweeps


class InterballAuroralPolradRspBinData(BinData, dataset="cdpp_int_aur_polrad_rspn2"):
    _iter_sweep_class = InterballAuroralPolradRspSweeps
