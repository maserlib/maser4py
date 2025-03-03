# -*- coding: utf-8 -*-
from maser.data.base.sweeps import Sweeps, Sweep
from ..ccsds import decode_ccsds_date
import numpy
from astropy.time import Time
from astropy.units import Unit


class InterballAuroralPolradRspSweep(Sweep):
    @property
    def time(self):
        return Time(
            decode_ccsds_date(
                self.header["P_Field"],
                self.header["T_Field"],
                self.header["CCSDS_CDS_LEVEL2_EPOCH"],
            ).datetime
        )

    @property
    def frequencies(self):
        return numpy.flipud(numpy.arange(self.header["STEPS"]) * 4.096 + 4.096) * Unit(
            "kHz"
        )


class InterballAuroralPolradRspSweeps(Sweeps):
    @property
    def generator(self):
        for sweep in self.data_reference._data:
            yield InterballAuroralPolradRspSweep(*sweep)
