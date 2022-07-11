# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from .sweeps import SrnNdaRoutineJupEdrSweeps

from astropy.time import Time
from astropy.units import Unit


class SrnNdaRoutineJupEdrCdfData(CdfData, dataset="srn_nda_routine_jup_edr"):
    """ORN NDA Routine Jupiter dataset"""

    _iter_sweep_class = SrnNdaRoutineJupEdrSweeps

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as f:
                self._frequencies = f["Frequency"][...] * Unit(
                    f["Frequency"].attrs["UNITS"]
                )
        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as f:
                self._times = Time(f["Epoch"][...])
        return self._times
