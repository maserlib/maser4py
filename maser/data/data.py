# -*- coding: utf-8 -*-
from typing import Union
from pathlib import Path
from .base import CdfData, FitsData, Pds3Data

from astropy.time import Time
from astropy.units import Unit


class SrnNdaRoutineJupEdrCdfData(CdfData, dataset="srn_nda_routine_jup_edr"):
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


class NenufarBstFitsData(FitsData, dataset="nenufar_bst"):
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


class ECallistoFitsData(FitsData, dataset="ecallisto"):
    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as f:
                self._times = f[1].data["TIME"][0] * Unit("s") + Time(
                    f"{f[0].header['DATE-OBS'].replace('/', '-')} {f[0].header['TIME-OBS']}"
                )
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as f:
                self._frequencies = f[1].data["FREQUENCY"][0] * Unit("MHz")
        return self._frequencies


class Vg1JPra3RdrLowband6secV1Data(
    Pds3Data, dataset="VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    pass
