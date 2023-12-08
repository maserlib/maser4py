# -*- coding: utf-8 -*-
from maser.data.base import CdfData, Sweeps
from astropy.units import Unit
from astropy.time import Time
from datetime import datetime
from typing import Union, List
from pathlib import Path


class JnoWavLesiaL3aV02Sweeps(Sweeps):
    @property
    def generator(self):
        attrs = self.file["Data"].attrs
        for t, d in zip(self.data_reference.times, self.file["Data"][...]):
            yield (
                t,
                self.data_reference.frequencies,
                d[...] * Unit(attrs["UNITS"]),
            )


class JnoWavLesiaL3aV02Data(CdfData, dataset="jno_wav_cdr_lesia"):
    _iter_sweep_class = JnoWavLesiaL3aV02Sweeps

    _dataset_keys = [
        "INTENSITY",
        "BACKGROUND",
        "INTENSITY_BG_COR",
    ]

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as cdf_file:
                units = cdf_file["Frequency"].attrs["UNITS"]
                freq = cdf_file["Frequency"][...] * Unit(units)
                self._frequencies = freq
        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            self._times = Time([], format="jd")
            with self.open(self.filepath) as cdf_file:
                self._times = Time(cdf_file["Epoch"][...])
        return self._times

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def as_xarray(self):
        import xarray
        import numpy

        datasets = {}
        background = self.file["Background"][...]
        bg_table = (numpy.tile(background, (len(self.times), 1))).T
        # gain = self.file["Gain"][...]
        # sigma = self.file["Sigma"][...]

        for dataset_key in self._dataset_keys:
            if dataset_key == "INTENSITY":
                values = self.file["Data"][...].T
            elif dataset_key == "BACKGROUND":
                values = bg_table
            elif dataset_key == "INTENSITY_BG_COR":
                values = self.file["Data"][...].T - bg_table
            dataset = xarray.DataArray(
                data=values,
                name=self.dataset,
                coords=[
                    (
                        "frequency",
                        self.frequencies.value,
                        {"units": self.frequencies.unit},
                    ),
                    ("time", self.times.to_datetime()),
                ],
                dims=("frequency", "time"),
                attrs={"units": self.file["Data"].attrs["UNITS"]},
            )
            datasets[dataset_key] = dataset.sortby("frequency")
        return xarray.Dataset(data_vars=datasets)

    # @property
    def epncore(self):
        import os
        import numpy

        md = CdfData.epncore(self)
        md["obs_id"] = md["granule_uid"]
        # md["instrument_host_name"] = "juno"
        # md["instrument_name"] = "waves"
        md["target_name"] = str(self.file.attrs["PDS_Observation_target"])  # "Jupiter"
        # md["target_class"] = "planet"
        # md["target_region"] = "TBD"
        # md["feature_name"] = "Radio Emission#Type II#Type III"

        md["dataproduct_type"] = "ds"

        # md["spectral_range_min"] = min(self.frequencies.to("Hz").value)
        # md["spectral_range_max"] = max(self.frequencies.to("Hz").value)

        md["publisher"] = "PADC"
        md["filepath"] = str(self.filepath)  # cdf_file

        datetmp = str(self.file.attrs["Generation_date"])
        md["creation_date"] = Time(
            # datetime(int(datetmp[0:4]), int(datetmp[5:6]), int(datetmp[7:8]))
            datetime.strptime(datetmp, "%Y%m%d")
        ).iso
        # md["creation_date"] = Time(self.file.attrs["Generation_date"][0], format="datetime").iso
        md["release_date"] = Time(os.path.getmtime(self.filepath), format="unix").iso
        md["modification_date"] = Time.now().iso

        md["processing_level"] = 5  # simulation / derived data

        md["spectral_resolution_min"] = float(md["spectral_range_min"]) / 1.0
        md["spectral_resolution_max"] = float(md["spectral_range_max"]) / 1.0

        freq = numpy.sort(self.frequencies.to("Hz").value)  # .sort()
        sampling_step = freq[1:] - freq[:-1]
        md["spectral_sampling_step_min"] = min(sampling_step)

        md["spectral_sampling_step_max"] = max(sampling_step)

        md["time_scale"] = "UTC"

        return md

    def quicklook(
        self,
        file_png: Union[str, Path, None] = None,
        keys: List[str] = ["INTENSITY", "BACKGROUND", "INTENSITY_BG_COR"],
        # db: List[bool] = [True, True, True],
        # vmin: List[float] = [-137,-137, 0, -137],
        # vmax: List[float] = [-71,-71, 7e-8, -71],
        # vmin_quantile: List[float] = [0.35, 0.35, 0.35],
        # vmax_quantile: List[float] = [0.95, 0.95, 0.95],
        yscale: str = "log",
        **kwargs,
    ):
        import numpy

        default_keys = ["INTENSITY", "BACKGROUND", "INTENSITY_BG_COR"]
        db_tab = numpy.array([True, True, True])
        vmin_quantile_tab = numpy.array([0.35, 0.35, 0.35])
        vmax_quantile_tab = numpy.array([0.95, 0.95, 0.95])
        for qkey, tab in zip(
            ["db", "vmin_quantile", "vmax_quantile"],
            [db_tab, vmin_quantile_tab, vmax_quantile_tab],
        ):
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
        self._quicklook(
            keys=keys,
            file_png=file_png,
            # db=db,
            # vmin_quantile=vmin_quantile,
            # vmax_quantile=vmax_quantile,
            yscale=yscale,
            **kwargs,
        )
