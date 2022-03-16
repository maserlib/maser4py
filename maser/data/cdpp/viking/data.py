# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Union
from maser.data.base import BinData
from .records import VikingV4nE5Records

from astropy.time import Time


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

    @property
    def times(self):
        if self._times is None:
            times = []
            _load_data, self._load_data = self._load_data, False
            for header, _ in self.sweeps:
                print(header)
                times.append(
                    Time(
                        f"{header[0]['CALEND_DATE_YEAR']}-{header[0]['CALEND_DATE_MONTH']}-"
                        f"{header[0]['CALEND_DATE_DAY']} {header[0]['CALEND_DATE_HOUR']}:"
                        f"{header[0]['CALEND_DATE_MINUTE']}:{header[0]['CALEND_DATE_SECOND']}"
                    )
                )
            self._load_data = _load_data
            self._times = Time(times)
        return self._times

    def frequencies(self):
        pass
