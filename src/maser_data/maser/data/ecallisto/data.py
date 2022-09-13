# -*- coding: utf-8 -*-

"""Classes for e-Callisto datasets"""

from maser.data.base import FitsData

from astropy.time import Time
from astropy.units import Unit


class ECallistoFitsData(FitsData, dataset="ecallisto"):
    """Class for `ecallisto` FITS files."""

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
