# -*- coding: utf-8 -*-
from maser.data.base import CdfData, BinData, Sweeps
from astropy.units import Unit
from astropy.time import Time


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
            with self.open(self.filepath) as cdf_file:
                self._times = Time(cdf_file["Epoch"][...])
        return self._times

    def as_xarray(self):
        import xarray

        dataset_keys = [
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
            coords=dict(
                frequency=(self.frequencies.value, {"units": self.frequencies.unit}),
                time=self.times.to_datetime(),
            ),
        ).sortby("frequency")
        # for key in dataset_keys:
        #    datasets[key] = datasets[key].where(datasets[key] != self.file[key].attrs["FILLVAL"])
        return datasets

    def quicklook(self, output_format="png"):
        xr = self.as_xarray()
        xr["L"].plot(vmin=40, vmax=70)


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
