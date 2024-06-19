# -*- coding: utf-8 -*-
from maser.data.base import CdfData, BinData, Sweeps
from astropy.units import Unit
from astropy.time import Time
from typing import List


class StWavL2Bin(BinData, dataset="st__l2_wav"):
    pass


class StaWavLfrL2Bin(StWavL2Bin, dataset="sta_l2_wav_lfr"):
    pass


class StbWavLfrL2Bin(StWavL2Bin, dataset="stb_l2_wav_lfr"):
    pass


class StaWavHfrL2Bin(StWavL2Bin, dataset="sta_l2_wav_hfr"):
    pass


class StbWavHfrL2Bin(StWavL2Bin, dataset="stb_l2_wav_hfr"):
    pass


class StWavL3CdfSweeps(Sweeps):
    pass


class StWavL3Cdf(CdfData, dataset="st__l3_wav"):

    _dataset_keys = [
        "STOKES_I",
        "STOKES_Q",
        "STOKES_U",
        "STOKES_V",
        "SOURCE_SIZE",
        "PSD_FLUX",
        "PSD_SFU",
        "WAVE_AZIMUTH_HCI",
        "WAVE_AZIMUTH_HEE",
        "WAVE_AZIMUTH_HEEQ",
        "WAVE_AZIMUTH_RTN",
        "WAVE_COLATITUDE_HCI",
        "WAVE_COLATITUDE_HEE",
        "WAVE_COLATITUDE_HEEQ",
        "WAVE_COLATITUDE_RTN",
    ]

    @property
    def frequencies(self):
        if self._frequencies is None:
            with self.open(self.filepath) as cdf_file:
                units = cdf_file["FREQUENCY"].attrs["UNITS"]
                freq = cdf_file["FREQUENCY"][...] * Unit(units)
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

        dataset_keys = self._dataset_keys
        data_vars = {}
        for key in dataset_keys:
            data_vars[key] = (
                ["frequency", "time"],
                self.file[key][...].T,
                {
                    "units": self.file[key].attrs["UNITS"],
                },
            )

        datasets = xarray.Dataset(
            data_vars=data_vars,
            coords={
                "frequency": (
                    ["frequency"],
                    self.frequencies.value,
                    {"units": self.frequencies.unit},
                ),
                "time": self.times.to_datetime(),
            },
        ).sortby("frequency")
        # for key in dataset_keys:
        #    datasets[key] = datasets[key].where(datasets[key] != self.file[key].attrs["FILLVAL"])
        return datasets

    # @property
    def epncore(self):
        import os

        md = BinData.epncore(self)
        md["obs_id"] = md["granule_uid"]
        md["instrument_host_name"] = f"stereo-{self.dataset[2]}"
        md["instrument_name"] = "waves"
        md["target_name"] = "Sun"
        md["target_class"] = "star"
        md["target_region"] = "Heliosphere"
        md["feature_name"] = "Radio Emission#Type II#Type III"

        md["dataproduct_type"] = "ds"

        md["spectral_range_min"] = min(self.frequencies.to("Hz").value)
        md["spectral_range_max"] = max(self.frequencies.to("Hz").value)

        md["publisher"] = "PADC"
        md["filepath"] = str(self.filepath)  # cdf_file

        md["creation_date"] = Time(self.file.attrs["Generation_date"][0]).iso
        md["release_date"] = Time(os.path.getmtime(self.filepath), format="unix").iso
        md["modification_date"] = Time.now().iso

        sc_id, _, exp_id, rec_id = self.file.attrs["Logical_source"][0].split("_")
        md["receiver_name"] = rec_id

        md["processing_level"] = 5  # simulation / derived data
        md["bib_reference"] = "2012JGRA..117.6101K"
        md["measurement_type"] = "#".join(
            [
                "phys.flux.density;em.radio",
                "phys.polarization;em.radio",
            ]
        )
        md["spectral_sampling_step_min"] = float(
            self.file.attrs["SPECTRAL_SAMPLING_STEP_MIN"][0]
        )
        md["spectral_sampling_step_max"] = float(
            self.file.attrs["SPECTRAL_SAMPLING_STEP_MAX"][0]
        )
        md["spectral_resolution_min"] = float(md["spectral_range_min"]) / 50e3
        md["spectral_resolution_max"] = float(md["spectral_range_max"]) / 50e3
        md["time_sampling_step_min"] = float(
            self.file.attrs["TIME_SAMPLING_STEP_MIN"][0]
        )
        md["time_sampling_step_max"] = float(
            self.file.attrs["TIME_SAMPLING_STEP_MAX"][0]
        )
        md["time_scale"] = "UTC"

        return md

    # def quicklook(self, output_format="png"):
    #    xr = self.as_xarray()
    #    #xr["L"].plot(vmin=40, vmax=70)
    #    xr["STOKES_I"].plot()
    def quicklook(
        self, file_png=None, keys: List[str] = ["PSD_FLUX", "STOKES_I"], **kwargs
    ):
        import numpy

        default_keys = ["PSD_FLUX", "STOKES_I"]
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
        self._quicklook(
            keys=keys,
            file_png=file_png,
            # vmin=[68, 68],
            # vmax=[94, 94],
            # db=[True, True],
            **kwargs,
        )


class StaWavLfrL3DfCdf(StWavL3Cdf, dataset="sta_l3_wav_lfr"):
    """PADC/MASER STEREO-A Waves LFR Level 3 Direction-Finding dataset

    - Observatory/Facility: STEREO-A
    - Experiment: Waves/LFR
    - Repository: PADC/MASER
    - Dataset-id: `sta_l3_wav_lfr`
    - Data format: CDF"""

    pass


class StbWavLfrL3DfCdf(StWavL3Cdf, dataset="stb_l3_wav_lfr"):
    """PADC/MASER STEREO-B Waves LFR Level 3 Direction-Finding dataset

    - Observatory/Facility: STEREO-B
    - Experiment: Waves/LFR
    - Repository: PADC/MASER
    - Dataset-id: `stb_l3_wav_lfr`
    - Data format: CDF"""

    pass


class StaWavHfrL3DfCdf(StWavL3Cdf, dataset="sta_l3_wav_hfr"):
    """PADC/MASER STEREO-A Waves HFR Level 3 Direction-Finding dataset

    - Observatory/Facility: STEREO-A
    - Experiment: Waves/HFR
    - Repository: PADC/MASER
    - Dataset-id: `sta_l3_wav_hfr`
    - Data format: CDF"""

    pass


class StbWavHfrL3DfCdf(StWavL3Cdf, dataset="stb_l3_wav_hfr"):
    """PADC/MASER STEREO-B Waves HFR Level 3 Direction-Finding dataset

    - Observatory/Facility: STEREO-B
    - Experiment: Waves/HFR
    - Repository: PADC/MASER
    - Dataset-id: `stb_l3_wav_hfr`
    - Data format: CDF"""

    pass
