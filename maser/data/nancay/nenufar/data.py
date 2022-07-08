# -*- coding: utf-8 -*-

from typing import Union
from pathlib import Path
from maser.data.base import FitsData


class NenufarBstFitsData(FitsData, dataset="srn_nenufar_bst"):
    """NenuFAR/BST (Beam Statistics) dataset"""

    @classmethod
    def _nenupy_open(cls, filepath):
        from nenupy.beamlet import BST_Data

        return BST_Data(str(filepath))

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
        beam: int = 0,
    ):
        super().__init__(filepath, dataset, access_mode)
        self.beam = beam

    @property
    def beam(self):
        return self._beam

    @beam.setter
    def beam(self, beam):
        data = NenufarBstFitsData._nenupy_open(self.filepath)
        if beam <= len(data.dbeams):
            self._beam = beam
        else:
            raise ValueError(f"Beam #{beam} doesn't exist.")

    @property
    def times(self):
        if self._times is None:
            bst = NenufarBstFitsData._nenupy_open(self.filepath)
            bst.dbeam = self.beam
            self._times = bst.time
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            bst = NenufarBstFitsData._nenupy_open(self.filepath)
            bst.dbeam = self.beam
            self._frequencies = bst.freqs
        return self._frequencies
