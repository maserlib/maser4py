# -*- coding: utf-8 -*-
from typing import Union

from maser.data.base import BinData, Sweeps
from maser.data.base.records import Records

# from astropy.units import Unit
# from astropy.time import Time
import numpy
import json
from pathlib import Path


KRONOS_LEVEL_FORMAT_JSON_FILE = Path(__file__).parent / "kronos_level_format.json"

with open(KRONOS_LEVEL_FORMAT_JSON_FILE, "r") as f:
    kronos_level_format = json.load(f)


class Kronos:
    @property
    def _format(self):
        return kronos_level_format[self.level]

    def read_data_binary(self):
        file_size = self.file_size
        rec_size = self._format["record_def"]["length"]
        dtype = list(
            zip(
                self._format["record_def"]["fields"],
                self._format["record_def"]["np_dtype"],
            )
        )
        if file_size % rec_size != 0:
            raise IOError("Corrupted file...")

        data = numpy.fromfile(
            self.filepath,
            dtype=dtype,
        )
        return data


class CoRpwsHfrKronosN1DataSweeps(Sweeps):
    @property
    def generator(self):
        for sweep_mask in self.data_reference._sweep_masks:
            yield self.data_reference_data[sweep_mask]


class CoRpwsHfrKronosDataRecords(Records):
    @property
    def generator(self):
        for row in self.data_reference._data:
            yield dict(
                zip(
                    self.data_reference._format["record_def"]["fields"],
                    row,
                )
            )


class CoRpwsHfrKronosN1Data(BinData, Kronos, dataset="co_rpws_hfr_kronos_n1"):

    _iter_sweep_class = CoRpwsHfrKronosN1DataSweeps
    _iter_record_class = CoRpwsHfrKronosDataRecords

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        super().__init__(
            filepath,
            dataset,
            access_mode,
            fixed_frequencies=False,
        )
        self.level = "n1"
        self._data = self.read_data_binary()
        self._sweep_masks = None
        self._nrecord = len(self._data)
        self._nsweep = len(self.sweep_masks)

    @property
    def sweep_masks(self):
        if self._sweep_masks is None:
            sweep_masks = []
            ti_values = numpy.unique(self._data["ti"])
            for ti in ti_values:
                sweep_masks.append(self._data["ti"] == ti)
            self._sweep_masks = sweep_masks
        return self._sweep_masks

    def __len__(self):
        if self.access_mode == "sweeps":
            return self._nsweep
        elif self.access_mode == "records":
            return self._nrecord
        else:
            return self.file_size


class CoRpwsHfrKronosN2Data(BinData, dataset="co_rpws_hfr_kronos_n2"):
    pass
