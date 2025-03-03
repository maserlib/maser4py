# -*- coding: utf-8 -*-

from abc import ABC
from typing import Union, List
from pathlib import Path
from maser.plot.base import FitsPlot

# from plot.base import FitsPlot


class OrnNenufarBstFitsPlot(FitsPlot, ABC, dataset="orn_nenufar_bst"):
    """NenuFAR/BST (Beamlet Statistics) dataset"""

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["NW", "NE"],
        **kwargs,
    ):
        self._quicklook(keys=keys, file_png=file_png, db=[True, True], **kwargs)
