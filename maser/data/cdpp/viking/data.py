# -*- coding: utf-8 -*-
from maser.data.base import BinData
from .records import VikingV4nE5Records


class VikingV4nE5BinData(BinData, dataset="viking_v4n_e5"):
    _iter_sweep_class = VikingV4nE5Records
