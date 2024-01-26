# -*- coding: utf-8 -*-

from abc import ABC
from typing import Union, List
from pathlib import Path
from maser.data.base import FitsData
from astropy.units import Unit, Quantity
from astropy.time import Time
import xarray


class OrnNenufarBstFitsData(FitsData, ABC, dataset="orn_nenufar_bst"):
    """NenuFAR/BST (Beamlet Statistics) dataset"""

    _dataset_keys = ["NW", "NE"]

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
        beam: int = 0,
    ):
        super().__init__(filepath, dataset, access_mode)
        self.beam = beam

    @property
    def beam(self) -> int:
        """Returns the selected beam index."""
        return self._beam

    @beam.setter
    def beam(self, b: int) -> None:
        available_beam_indices = self.file[4].data["noBeam"]
        if b not in available_beam_indices:
            raise ValueError(
                f"Unknown beam index {b}. Please select one from {available_beam_indices}."
            )
        self._beam = b

    @property
    def frequencies(self) -> Quantity:
        beamlets = self.file[4].data["nbBeamlet"][self.beam]
        subband_half_width = 195.3125 * Unit("kHz")
        freqs = self.file[4].data["freqList"][self.beam][:beamlets] * Unit("MHz")
        self._frequencies = freqs - subband_half_width / 2
        return self._frequencies

    @property
    def times(self) -> Time:
        if self._times is None:
            self._times = Time(self.file[7].data["jd"], format="jd")
        return self._times

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def as_xarray(self):
        """Transform the data in x-arrays."""

        # Data axes should not be put in __init__ because frequencies
        # depends on the beam index selection
        _dataset_axes = {
            "Frequency": {
                "name": "frequency",
                "value": self.frequencies.value,
                "metadata": {"units": self.frequencies.unit},
            },
            "Time": {"name": "time", "value": self.times.datetime, "metadata": {}},
        }

        datasets = {}

        # Select the correct beamlets wrt. the selected beam
        n_beamlets = self.file[4].data["nbBeamlet"][self.beam]
        beamlets = self.file[4].data["BeamletList"][self.beam][:n_beamlets]

        available_polarizations = list(self.file[1].data["spol"][0])

        for dataset_key in self._dataset_keys:

            polar_index = available_polarizations.index(dataset_key)

            datasets[dataset_key] = xarray.DataArray(
                data=self.file[7].data["DATA"][:, polar_index, beamlets].T,
                name=dataset_key,
                coords=[
                    (
                        dim_name,
                        _dataset_axes[dim_name]["value"],
                        _dataset_axes[dim_name]["metadata"],
                    )
                    for dim_name in _dataset_axes.keys()
                ],
                dims=[
                    _dataset_axes[dim_name]["name"] for dim_name in _dataset_axes.keys()
                ],
                attrs={
                    "units": "",
                    "title": "",
                },
            )
        return xarray.Dataset(data_vars=datasets)

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["NW", "NE"],
        **kwargs,
    ):
        import numpy

        default_keys = ["NW", "NE"]
        db_tab = numpy.array([True, True])
        for qkey, tab in zip(["db"], [db_tab]):
            if qkey not in kwargs:
                qkey_tab = []
                for key in keys:
                    if key in default_keys:
                        qkey_tab.append(
                            tab[numpy.where(key == numpy.array(default_keys))][0]
                        )
                    else:
                        qkey_tab.append(None)
                kwargs[qkey] = list(qkey_tab)
        self._quicklook(keys=keys, file_png=file_png, **kwargs)
