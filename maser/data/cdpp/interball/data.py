# -*- coding: utf-8 -*-
from maser.data.base import BinData
from .sweeps import InterballAuroralPolradRspSweeps


class InterballAuroralPolradRspBinData(BinData, dataset="int_aur_polrad_rsp"):
    _iter_sweep_class = InterballAuroralPolradRspSweeps
