# -*- coding: utf-8 -*-
from maser.data.base.sweeps import Sweeps, Sweep
from astropy.units import Unit
import numpy


class VgPra3RdrLowband6secV1Sweep(Sweep):
    def __init__(self, header, data):
        super().__init__(header, data)
        self._frequencies = header["frequencies"]
        self._time = header["time"]
        self.header["sweep_type"] = self._get_sweep_type()
        self.header["attenuator"] = self._get_attenuator_value()

    def _get_sweep_type(self):
        if (self.header["status_word"] & 1536) // 512 in [0, 3]:
            return "R"
        else:
            return "L"

    def _get_attenuator_value(self):
        if self.header["status_word"] & 1:
            return 15 * Unit("dB")
        elif (self.header["status_word"] // 2) & 1:
            return 30 * Unit("dB")
        elif (self.header["status_word"] // 4) & 1:
            return 45 * Unit("dB")
        else:
            return 0 * Unit("dB")

    def _get_polar_indices(self):
        even_mask = (numpy.arange(70) % 2) == 0
        odd_mask = (numpy.arange(70) % 2) == 1
        if self._get_sweep_type() == "R":
            return {"R": even_mask, "L": odd_mask}
        else:
            return {"L": even_mask, "R": odd_mask}

    def __getitem__(self, key):
        valid_keys = ["R", "L"]
        if key not in valid_keys:
            raise KeyError()
        polar_idx = self._get_polar_indices()
        return {
            "data": self.data[polar_idx[key]],
            "frequencies": self.header["frequencies"][polar_idx[key]],
        }


class VgPra3RdrLowband6secV1Sweeps(Sweeps):
    @property
    def generator(self):
        for t, sm in zip(
            self.data_reference.times,
            self.data_reference.sweep_mapping,
        ):
            header = {"frequencies": self.data_reference.frequencies, "time": t}
            data = self.data_reference.table[f"SWEEP{sm[1]+1}"][sm[0], :]
            header["status_word"] = data[0]

            yield VgPra3RdrLowband6secV1Sweep(header, data[1:] / 100 * Unit("dB"))


class VgPra4SummBrowse48secV1Sweeps(Sweeps):
    @property
    def generator(self):
        for i, t in enumerate(self.data_reference.times):
            header = {
                "frequencies": self.data_reference.frequencies,
                "time": t,
            }
            data = {
                "L": self.data_reference.table["LH_DATA"][i],
                "R": self.data_reference.table["RH_DATA"][i],
            }
            yield Sweep(header, data)
