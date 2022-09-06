# -*- coding: utf-8 -*-
from maser.data.base import CdfData
from astropy.time import Time
from astropy.units import Unit
from maser.data.base.sweeps import Sweeps


class RpwTnrSurvSweeps(Sweeps):
    @property
    def generator(self):
        """
        For each time, yield a frequency range and a dictionary with the following keys:
        - AUTO1 : Power spectral density at receiver + PA for channel 1 before applying antenna gain (V²/Hz)
        - AUTO2 : Power spectral density at receiver + PA for channel 2 before applying antenna gain (V²/Hz)
        - PHASE : TNR Phase in degrees, computed from the cross-correlation Im. And Real. Parts [Phase=atan2(CROSS_I/CROSS_R)*180/pi]
        - FLUX_DENSITY1 : Flux of the power spectral density for channel 1 with antenna gain (W/m²/Hz)
        - FLUX_DENSITY2 : Flux of the power spectral density for channel 2 with antenna gain (W/m²/Hz)
        - MAGNETIC_SPECTRAL_POWER1 : Magnetic power spectral density from 1 search coil axis in channel 1
        - MAGNETIC_SPECTRAL_POWER1 : Magnetic power spectral density from 1 search coil axis in channel 2
        - SENSOR_CONFIG : Indicates the THR sensor configuration

        """

        for time, freq, a1, a2, sc, ph, f1, f2, m1, m2, band_index, survey_mode in zip(
            self.file["Epoch"][...],
            self.file["TNR_BAND_FREQ"][...],
            self.file["AUTO1"][...],
            self.file["AUTO2"][...],
            self.file["SENSOR_CONFIG"][...],
            self.file["PHASE"],
            self.file["FLUX_DENSITY1"][...],
            self.file["FLUX_DENSITY1"][...],
            self.file["MAGNETIC_SPECTRAL_POWER1"],
            self.file["MAGNETIC_SPECTRAL_POWER2"],
            self.file["TNR_BAND"],
            self.file["SURVEY_MODE"],
        ):
            yield (
                {
                    "AUTO1": a1,
                    "AUTO2": a2,
                    "SENSOR_CONFIG": sc,
                    "PHASE": ph,
                    "FlUX_DENSITY1": f1,
                    "FLUX_DENSITY2": f2,
                    "MAGNETIC_SPECTRAL_POWER1": m1,
                    "MAGNETIC_SPECTRAL_POWER2": m2,
                },
                Time(time),
                freq,
                self.data_reference.frequency_band_labels[band_index],
                self.data_reference.survey_mode_labels[survey_mode],
            )


class RpwTnrSurv(CdfData, dataset="solo_L2_rpw-tnr-surv"):
    _iter_sweep_class = RpwTnrSurvSweeps

    frequency_band_labels = ["A", "B", "C", "D"]

    survey_mode_labels = ["SURVEY_NORMAL", "SURVEY_BURST"]

    channel_labels = ["1", "2"]

    sensor_mapping = {
        1: "V1",
        2: "V2",
        3: "V3",
        4: "V1-V2",
        5: "V2-V3",
        6: "V3-V1",
        7: "B_MF",
        9: "HF_V1-V2",
        10: "HF_V2-V3",
        11: "HF_V3-V1",
    }

    @property
    def frequencies(self):
        if self._frequencies is None:

            self._frequencies = {}
            with self.open(self.filepath) as cdf_file:
                for band_index, band_label in enumerate(self.frequency_band_labels):
                    # if units are not specified, assume Hz
                    units = cdf_file["TNR_BAND_FREQ"].attrs["UNITS"].strip() or "Hz"
                    freq = cdf_file["TNR_BAND_FREQ"][band_index, :] * Unit(units)
                    self._frequencies[band_label] = freq

        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            self._times = {}
            for band_index, frequency_band in enumerate(self.frequency_band_labels):
                mask = (self.file["TNR_BAND"][...] == band_index)[0]
                self._times[frequency_band] = Time(self.file["Epoch"][mask])
        return self._times

    def as_xarray(self):
        """
        Return the data as a xarray
        """
        import xarray

        band = xarray.DataArray(
            [self.frequency_band_labels[idx] for idx in self.file["TNR_BAND"][...]]
        )
        time = self.file["Epoch"][...]

        sensor_config = list(
            map(
                lambda configs: (
                    self.sensor_mapping[configs[0]],
                    self.sensor_mapping[configs[1]],
                ),
                self.file["SENSOR_CONFIG"][...],
            )
        )

        tnr_frequency_bands = self.file["TNR_BAND_FREQ"][...]
        freq_index = range(tnr_frequency_bands.shape[1])

        frequency = self.file["FREQUENCY"][...]  # (n_time, n_freq)

        auto = xarray.DataArray(
            [self.file["AUTO1"][...], self.file["AUTO2"][...]],
            coords={
                "channel": self.channel_labels,
                "time": time,
                "freq_index": freq_index,
                "band": ("time", band.data),
                "frequency": (["time", "freq_index"], frequency.data),
                "sensor": (["time", "channel"], sensor_config),
            },
            dims=["channel", "time", "freq_index"],
        )

        return xarray.Dataset({"auto": auto})
