# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Union, Dict
from ...pds import Pds3Data
from ...pds.utils import PDSDataTableObject
from maser.data.base.sweeps import Sweeps, Sweep
from .consts import (
    MEX_MARSIS_AIS_PROCESS_IDS,
    MEX_MARSIS_AIS_DATA_TYPES,
    MEX_MARSIS_AIS_MODE_SELECTIONS,
)
from ...psa.labels import FMT_LABELS
from astropy.time import Time
from astropy.units import Unit
from datetime import datetime
import numpy


def decode_instrument_mode(instrument_mode: int):
    data_type = (instrument_mode & 240) // 16
    mode_selection = instrument_mode & 15
    return {
        "data_type": MEX_MARSIS_AIS_DATA_TYPES[data_type],
        "mode_selection": MEX_MARSIS_AIS_MODE_SELECTIONS[mode_selection],
    }


class MexMMarsis3RdrAisV1Sweep(Sweep):
    def __init__(self, header, data, time, frequencies):
        super().__init__(header, data)
        self._time = time
        self._frequencies = frequencies


class MexMMarsis3RdrAisV1Sweeps(Sweeps):
    @property
    def generator(self):
        for sweep_id, sweep_mask in self.data_reference.sweep_mapping.items():
            if self.data_reference.fixed_frequencies:
                freqs = self.data_reference.frequencies
            else:
                freqs = self.data_reference.frequencies[sweep_id]
            table = self.data_reference.table
            times = self.data_reference.times
            header = {
                "process_id": MEX_MARSIS_AIS_PROCESS_IDS[
                    table["PROCESS_ID"][sweep_mask][0]
                ],
                "attenuation": table["RECEIVER_ATTENUATION"][sweep_mask],
                "band_number": table["BAND_NUMBER"][sweep_mask],
                "transmit_power": table["TRANSMIT_POWER"][sweep_mask][0],
            }
            header.update(
                decode_instrument_mode(table["INSTRUMENT_MODE"][sweep_mask][0])
            )
            yield MexMMarsis3RdrAisV1Sweep(
                header,
                table["SPECTRAL_DENSITY"][sweep_mask],
                times[sweep_id],
                freqs,
            )


class MexMMarsis3RdrAisV1Data(
    Pds3Data,
    dataset="MEX-M-MARSIS-3-RDR-AIS-V1.0",
):
    _iter_sweep_class = MexMMarsis3RdrAisV1Sweeps

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
            fmt_label_dict=FMT_LABELS["MEX-M-MARSIS-3-RDR-AIS-V1.0"],
        )
        self.table = PDSDataTableObject(
            self.label["AIS_TABLE"], self.pointers["AIS_TABLE"]["file_name"]
        )
        self.sweep_mapping: Dict[int, bool] = {}
        if self._load_data:
            self.load_data()

    def load_data(self):
        self.table.load_data()
        self._load_data = True

        msec0 = self.table["SCET_MSEC"][0]
        sweep_number = [0]
        for msec in self.table["SCET_MSEC"][1:]:
            if msec == msec0:
                sweep_number.append(sweep_number[-1])
            else:
                msec0 = msec
                sweep_number.append(sweep_number[-1] + 1)
        sweep_number = numpy.array(sweep_number)
        for sweep_id in sorted(set(sweep_number)):
            self.sweep_mapping[sweep_id] = sweep_number == sweep_id

    @property
    def _sweep_masks(self):
        for item in self.sweep_mapping.items():
            yield item[1]

    @property
    def times(self):
        if self._times is None:
            if self._load_data is False:
                self.load_data()
            _times = [
                datetime.strptime(
                    "".join(self.table["SCET_STRING"][sweep_mask, :][0]).strip(),
                    "%Y-%jT%H:%M:%S.%f",
                )
                for sweep_mask in self._sweep_masks
            ]
            self._times = Time(_times)
        return self._times

    @property
    def frequencies(self):
        if self._frequencies is None:
            if self._load_data is False:
                self.table.load_data()
                self._load_data = True
            freq_table_nb = self.table["FREQUENCY_TABLE_NUMBER"]
            if len(set(freq_table_nb)) == 1:
                self._frequencies = self.table["FREQUENCY"][
                    next(self._sweep_masks)
                ] * Unit("Hz")
            else:
                self.fixed_frequencies = False
                self._frequencies = [
                    self.table["FREQUENCY"][sweep_mask] * Unit("Hz")
                    for sweep_mask in self._sweep_masks
                ]
        return self._frequencies

    def as_xarray(self):
        import xarray

        datasets = xarray.DataArray(
            data=numpy.array([item.table for item in self.sweeps]).T,
            name=self.dataset,
            coords=[
                ("frequency", self.frequencies, {"units": "kHz"}),
                ("time", self.times.to_datetime()),
            ],
            dims=("frequency", "time"),
            attrs={"units": "W m^-2 Hz^-1"},
        )

        return datasets


class MexMMarsis3RdrAisExt1V1Data(
    MexMMarsis3RdrAisV1Data, dataset="MEX-M-MARSIS-3-RDR-AIS-EXT1-V1.0"
):
    pass


class MexMMarsis3RdrAisExt2V1Data(
    MexMMarsis3RdrAisV1Data, dataset="MEX-M-MARSIS-3-RDR-AIS-EXT2-V1.0"
):
    pass


class MexMMarsis3RdrAisExt3V1Data(
    MexMMarsis3RdrAisV1Data, dataset="MEX-M-MARSIS-3-RDR-AIS-EXT3-V1.0"
):
    pass


class MexMMarsis3RdrAisExt4V1Data(
    MexMMarsis3RdrAisV1Data, dataset="MEX-M-MARSIS-3-RDR-AIS-EXT4-V1.0"
):
    pass


class MexMMarsis3RdrAisExt5V1Data(
    MexMMarsis3RdrAisV1Data, dataset="MEX-M-MARSIS-3-RDR-AIS-EXT5-V1.0"
):
    pass


class MexMMarsis3RdrAisExt6V1Data(
    MexMMarsis3RdrAisV1Data, dataset="MEX-M-MARSIS-3-RDR-AIS-EXT6-V1.0"
):
    pass
