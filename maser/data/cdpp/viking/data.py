# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Union
from maser.data.base import BinData
from .records import VikingV4nE5Records


class VikingV4nE5BinData(BinData, dataset="viking_v4n_e5"):
    _iter_sweep_class = VikingV4nE5Records
    _access_modes = ["file", "records"]

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "records",
        load_data: bool = True,
    ) -> None:
        super().__init__(filepath, dataset, access_mode, load_data)

    @property
    def sweeps(self):
        raise ValueError("Illegal access mode.")
