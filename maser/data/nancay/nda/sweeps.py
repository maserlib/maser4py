# -*- coding: utf-8 -*-
from maser.data.base.sweeps import Sweeps, Sweep
from astropy.time import Time
from astropy.units import Unit


class SrnNdaRoutineJupEdrSweep(Sweep):
    def __init__(self, header, data, time, frequencies):
        super().__init__(header, data)
        self._time = time
        self._frequencies = frequencies


class SrnNdaRoutineJupEdrSweeps(Sweeps):
    @property
    def generator(self):
        for time, rr, ll, status, rr_t_offset in zip(
            self.file["Epoch"],
            self.file["RR"],
            self.file["LL"],
            self.file["STATUS"],
            self.file["RR_SWEEP_TIME_OFFSET"],
        ):
            yield SrnNdaRoutineJupEdrSweep(
                {"STATUS": status, "RR_TIME_OFFSET": rr_t_offset},
                {"RR": rr, "LL": ll},
                Time(time),
                self.file["Frequency"][...]
                * Unit(self.file["Frequency"].attrs["UNITS"]),
            )
