# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Union, Type
from maser.data.base import BinData, RecordsOnly
from .records import VikingV4nE5Records

from astropy.time import Time


class VikingV4nE5BinData(RecordsOnly, BinData, dataset="cdpp_viking_v4n_e5"):
    _iter_sweep_class = Type[VikingV4nE5Records]

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "records",
        load_data: bool = True,
    ) -> None:
        super().__init__(filepath, dataset, access_mode, load_data)

    @property
    def times(self):
        if self._times is None:
            times = []
            _load_data, self._load_data = self._load_data, False
            for header, _ in self.sweeps:
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
