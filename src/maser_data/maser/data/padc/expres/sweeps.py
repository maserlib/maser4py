# -*- coding: utf-8 -*-

from maser.data.base.sweeps import Sweeps, Sweep


class ExpresCdfDataSweep(Sweep):
    def __init__(self, header, data, time, frequencies):
        super().__init__(header, data)
        self._time = time
        self._frequencies = frequencies


class ExpresCdfDataSweeps(Sweeps):
    @property
    def generator(self):
        frequencies = self.data_reference.frequencies

        # Convert the data to XArray
        xdata = self.data_reference.as_xarray()

        for i, time in enumerate(self.data_reference.times):
            yield ExpresCdfDataSweep(
                header={"header_keyword": "x-array generate data"},
                data={datakey: xdata[datakey].isel(time=[i]) for datakey in xdata},
                time=time,
                frequencies=frequencies,
            )
