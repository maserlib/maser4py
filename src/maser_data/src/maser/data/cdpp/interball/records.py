# -*- coding: utf-8 -*-
from maser.data.base.records import Records, Record
from .sweeps import InterballAuroralPolradRspSweeps


class InterballAuroralPolradRspRecord(Record):
    def __init__(self, header, data, time, frequency):
        super().__init__(header, data)
        self._time = time
        self._frequency = frequency

    @property
    def frequency(self):
        return self._frequency


class InterballAuroralPolradRspRecords(Records):
    @property
    def generator(self):
        sweeps = InterballAuroralPolradRspSweeps(data_instance=self.data_reference)
        for sweep in sweeps:
            for i in range(sweep.header["STEPS"]):
                data = {
                    "EX": sweep.data["EX"][i] if sweep.data["EX"] is not None else None,
                    "EY": sweep.data["EY"][i],
                    "EZ": sweep.data["EZ"][i] if sweep.data["EZ"] is not None else None,
                }
                yield InterballAuroralPolradRspRecord(
                    sweep.header, data, sweep.time, sweep.frequencies[i]
                )
