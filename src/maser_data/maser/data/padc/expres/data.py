# -*- coding: utf-8 -*-


"""
    EXPRES Simulation data reader


    .. code-block:: python

        from maser.data import Data
        expres = Data(
            filepath='<path>/expres_juno_jupiter_ganymede_jrm09_lossc-wid1deg_3kev_20211218_v11.cdf',
            source='Ganymede NORTH'
        )


"""


from maser.data.base import CdfData
from .sweeps import ExpresCdfDataSweeps

from abc import ABC
from typing import Union
from pathlib import Path
from astropy.time import Time
from astropy.units import Unit, Quantity
import xarray
import numpy as np
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

__all__ = [
    'ExpresCdfData'
]


class ExpresCdfData(CdfData, ABC, dataset='expres'):
    """ Base class for EXPRES datasets. """


    _iter_sweep_class = ExpresCdfDataSweeps
    _dataset_keys = [
        'CML',
        'Polarization',
        'FC',
        'FP',
        'Theta',
        'ObsDistance',
        'ObsLatitude',
        'SrcFreqMax',
        'SrcFreqMaxCMI',
        'SrcLongitude',
        'VisibleSources' # Not used in 'routine' simulations
        # 'Azimuth' # WIP
        # 'ObsLocalTime' # WIP
    ]


    def __init__(self, 
        filepath: Path,
        dataset: Union[None, str] = '__auto__',
        access_mode: str = 'sweeps',
        source: str = None,
        # hemisphere: str = None
    ) -> None:
        super().__init__(filepath, dataset, access_mode)
        self.source = source
        # self.hemisphere = hemisphere
        self._dataset_axes = {
            'Epoch': {
                'name': 'time',
                'value': self.times.datetime,
                'metadata': {}
            },
            'Frequency': {
                'name': 'frequency',
                'value': self.frequencies.value,
                'metadata': {'units': self.frequencies.unit}
            },
            # 'Hemisphere_ID_Label': { # only for VisibleSources
            #     'name': 'hemisphere',
            #     'value': self.file['Hemisphere_ID_Label'][...],
            #     'metadata': {}
            # },
            'Src_ID_Label': {
                'name': 'source',
                'value': self.file['Src_ID_Label'][...],
                'metadata': {}
            }
        }


    @property
    def frequencies(self) -> Quantity:
        if self._frequencies is None:
            with self.open(self.filepath) as f:
                self._frequencies = f['Frequency'][...] * Unit(
                    f['Frequency'].attrs['UNITS']
                )
        return self._frequencies


    @property
    def times(self) -> Time:
        if self._times is None:
            with self.open(self.filepath) as f:
                self._times = Time(f['Epoch'][...])
        return self._times


    @property
    def source(self) -> str:
        return self._source
    @source.setter
    def source(self, source_name: str) -> None:
        """ Select one source or all (None). """
        available_source_values = self.file['Src_ID_Label'][...]
        if source_name is None:
            source_name = available_source_values
            self._source = None
        elif source_name not in available_source_values:
            raise ValueError(f'Source selection should be in {available_source_values}.')
        else:
            _source_id = np.argwhere(available_source_values == source_name)[0, 0]
            self._source = self.file['Src_ID_Label'][...][_source_id]


    # @property
    # def hemisphere(self) -> str:
    #     return self._hemisphere
    # @hemisphere.setter
    # def hemisphere(self, hemisphere_name: str) -> None:
    #     """ Select one hemisphere or all (None). """
    #     available_hemisphere_values = self.file['Hemisphere_ID_Label'][...]
    #     if hemisphere_name is None:
    #         hemisphere_name = available_hemisphere_values
    #         self._hemisphere = None
    #     elif hemisphere_name not in available_hemisphere_values:
    #         raise ValueError(f'Hemisphere selection should be in {available_hemisphere_values}.')
    #     else:
    #         _hemisphere_id = np.argwhere(available_hemisphere_values == hemisphere_name)[0, 0]
    #         self._hemisphere = self.file['Hemisphere_ID_Label'][...][_hemisphere_id]


    def as_xarray(self) -> dict:
        """ """

        datasets = {}

        for dataset_key in self._dataset_keys:

            # Check that the variable is in the CDF
            if dataset_key not in self.file.keys():
                continue

            # Check dependencies from CDF attributes
            dependencies = {
                int(key.split('_')[1]): axis\
                for key, axis in self.file[dataset_key].attrs.items() if key.startswith('DEPEND_')
            }
            if len(dependencies) == 0:
                log.warning(
                    f"Code maintainer bug: '{dataset_key}' should not "
                    "be put in '_dataset_keys' (no dependencies found) "
                    f"in {self.__class__.__bases__[0]}."
                )
                continue
            
            # Check that the required dataset_axes are defined
            for dim_name in dependencies.values():
                if not  dim_name in self._dataset_axes:
                    raise Exception(
                        f"Code maintainer bug: axis '{dim_name}' (a dependency "
                        f"of '{dataset_key}') is missing from '_dataset_axes' "
                        f"in {self.__class__.__bases__[0]}."
                    )

            # Sort out data and attributes
            data_ext = self.file[dataset_key]
            data_attr = self.file[dataset_key].attrs
            # exctract the data and replace the values at FILVAL by NaN
            data = data_ext[...]
            data = np.where(data == data_attr['FILLVAL'], np.nan, data)

            # Conversion in XArray
            log.info(f"Converting '{dataset_key}' to XArray.")
            datasets[dataset_key] = xarray.DataArray(
                data=data,
                name=data_attr.get('LABLAXIS', dataset_key),
                coords=[
                    (
                        dim_name,
                        self._dataset_axes[dim_name]['value'],
                        self._dataset_axes[dim_name]['metadata']
                    ) for dim_name in dependencies.values()
                ],
                dims=[
                    self._dataset_axes[dim_name]['name']\
                    for dim_name in dependencies.values()
                ],
                attrs={
                    'units': data_attr.get('UNITS', None),
                    'title': data_attr['CATDESC'],
                }
            ).transpose(
                'frequency',
                'time',
                'source',
                'hemisphere',
                missing_dims='ignore'
            )

            # Sub-select the data based on the source/hemisphere attribute
            # try:
            #     datasets[dataset_key] = datasets[dataset_key].sel(hemisphere=self.hemisphere)
            # except KeyError:
            #     # No dependency based on hemisphere
            #     pass

            try:
                datasets[dataset_key] = datasets[dataset_key].sel(source=self.source)
            except KeyError:
                # No dependency based on source
                pass

        return datasets


    def quicklook(self, file_png: Union[str, Path, None] = None, **kwargs) -> None:
        if self.source is None:
            raise ValueError(
                f"Select one source among {self.file['Src_ID_Label'][...]} before producing a quicklook."
            )
        self._quicklook(
            keys=['FC', 'FP', 'Polarization', 'Theta'],
            db=[False, False, False, False],
            file_png=file_png,
            vmin=None,#[-360, -10],
            vmax=None,#[360, 10],
            **kwargs,
        )

