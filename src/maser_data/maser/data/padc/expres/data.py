# -*- coding: utf-8 -*-
from maser.data.base import CdfData
# from .sweeps import SrnNdaRoutineEdrSweeps

from astropy.time import Time
from astropy.units import Unit


__all__ = [
    'ExpresCdfData',
    'ExpresJunoJupiterEuropaCdfData'
]


class ExpresCdfData(CdfData, dataset='expres'):
    """ Base class for EXPRES datasets """

    # _iter_sweep_class = SrnNdaRoutineEdrSweeps

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as f:
                self._frequencies = f["Frequency"][...] * Unit(
                    f["Frequency"].attrs["UNITS"]
                )
        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as f:
                self._times = Time(f["Epoch"][...])
        return self._times

    def as_xarray(self):
        import xarray

        dataset_keys = ['Polarization', 'Theta', 'FP', 'FC', 'Azimuth', 'ObsLatitude', 'SrcLongitude', 'SrcFreqMax', 'ObsDistance', 'CML']
        datasets = {}

        for dataset_key in dataset_keys:
            datasets[dataset_key] = xarray.DataArray(
                data=self.file[dataset_key][...].T,
                name=self.file[dataset_key].attrs['LABLAXIS'],
                coords=[
                    (
                        'frequency',
                        self.frequencies.value,
                        {'units': self.frequencies.unit},
                    ),
                    ('time', self.times.datetime),
                ],
                dims=('frequency', 'time'),
                attrs={
                    'unit': self.file[dataset_key].attrs['UNITS'],
                    'title': self.file[dataset_key].attrs['CATDESC'],
                },
            )
        return datasets


# class ExpresJunoJupiterEuropaCdfData(
#     ExpresCdfData, dataset="expres_juno_jupiter_europa"
# ):
#     """ORN NDA Routine Jupiter dataset"""

#     pass



# def expres_class_factory(observer, source) :
#     dataset = f'{ExpresCdfData.dataset}_{observer}_{source}'
#     print(dataset)
#     class NewClass(ExpresCdfData, dataset=dataset): pass
#     class_name = f'{ExpresCdfData.dataset}{observer}{source}'
#     NewClass.__name__ = class_name
#     NewClass.__qualname__ = class_name
#     return NewClass

# new_class = expres_class_factory('Earth', 'Jupiter_Ganymede')
# globals()[new_class.__name__] = new_class