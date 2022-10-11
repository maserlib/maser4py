# -*- coding: utf-8 -*-
import numpy as np

from astropy.time import Time
from astropy.units import Unit

from maser.data.base import CdfData
from maser.data.base.sweeps import Sweeps

TNR_SWEEP_DTYPE = [
    ("Epoch", ("datetime64[ns]", 4)),
    ("VOLTAGE_SPECTRAL_POWER1", ("float32", 128)),
    ("VOLTAGE_SPECTRAL_POWER2", ("float32", 128)),
    ("FLUX_DENSITY1", ("float32", 128)),
    ("FLUX_DENSITY2", ("float32", 128)),
    ("MAGNETIC_SPECTRAL_POWER1", ("float32", 128)),
    ("MAGNETIC_SPECTRAL_POWER2", ("float32", 128)),
]


class RpwTnrSurvSweeps(Sweeps):
    @property
    def generator(self):
        """
        For each time, yield a frequency range and a dictionary with the following keys:
        - VOLTAGE_SPECTRAL_POWER1 : Power spectral density at receiver + PA for channel 1 before applying antenna gain (V²/Hz)
        - VOLTAGE_SPECTRAL_POWER2 : Power spectral density at receiver + PA for channel 2 before applying antenna gain (V²/Hz)
        - FLUX_DENSITY1 : Flux of the power spectral density for channel 1 with antenna gain (W/m²/Hz)
        - FLUX_DENSITY2 : Flux of the power spectral density for channel 2 with antenna gain (W/m²/Hz)
        - MAGNETIC_SPECTRAL_POWER1 : Magnetic power spectral density from 1 search coil axis in channel 1
        - MAGNETIC_SPECTRAL_POWER1 : Magnetic power spectral density from 1 search coil axis in channel 2
        """

        def add_rec(in_data, out_data, rec_index):

            # Get frequency band range
            i_band = self.file["TNR_BAND"][rec_index]
            i0, i1 = self.data_reference.frequency_band_indices[i_band]

            # Fill values
            out_data["Epoch"][0, i_band] = in_data["Epoch"][rec_index]
            out_data["VOLTAGE_SPECTRAL_POWER1"][0, i0 : i1 + 1] = in_data["AUTO1"][
                rec_index, :
            ]
            out_data["VOLTAGE_SPECTRAL_POWER2"][0, i0 : i1 + 1] = in_data["AUTO2"][
                rec_index, :
            ]
            out_data["FLUX_DENSITY1"][0, i0 : i1 + 1] = in_data["FLUX_DENSITY1"][
                rec_index, :
            ]
            out_data["FLUX_DENSITY2"][0, i0 : i1 + 1] = in_data["FLUX_DENSITY2"][
                rec_index, :
            ]
            out_data["MAGNETIC_SPECTRAL_POWER1"][0, i0 : i1 + 1] = in_data[
                "MAGNETIC_SPECTRAL_POWER1"
            ][rec_index, :]
            out_data["MAGNETIC_SPECTRAL_POWER2"][0, i0 : i1 + 1] = in_data[
                "MAGNETIC_SPECTRAL_POWER2"
            ][rec_index, :]

            return out_data

        # First build list of frequency values for TNR (A+B+C+D bands)
        freq = self.data_reference.frequencies

        # Initialize output data vector for the first sweep
        sweep_data = np.zeros(1, dtype=TNR_SWEEP_DTYPE)

        # Loop over each record in the CDF
        sweep_completed = False
        for i in range(self.file["SWEEP_NUM"].shape[0]):
            try:
                if self.file["SWEEP_NUM"][i] != self.file["SWEEP_NUM"][i + 1]:
                    sweep_data = add_rec(self.file, sweep_data, i)
                    sweep_completed = True
                    yield (
                        sweep_data,
                        Time(sweep_data["Epoch"][0, 0]),
                        freq,
                        self.file["SENSOR_CONFIG"][i],
                        self.file["SURVEY_MODE"][i],
                    )
                else:
                    if sweep_completed:
                        sweep_completed = False
                        sweep_data = np.empty(1, dtype=TNR_SWEEP_DTYPE)

                    sweep_data = add_rec(self.file, sweep_data, i)
            except IndexError:
                # End of CDF file is reached, force yield for last record
                yield (
                    sweep_data,
                    Time(sweep_data["Epoch"][0, 0]),
                    freq,
                    self.file["SENSOR_CONFIG"][i],
                    self.file["SURVEY_MODE"][i],
                )


class RpwTnrSurv(CdfData, dataset="solo_L2_rpw-tnr-surv"):
    _iter_sweep_class = RpwTnrSurvSweeps

    # Define TNR frequency band names
    frequency_band_labels = ["A", "B", "C", "D"]

    # Define range of indices for each TNR frequency band
    frequency_band_indices = [[0, 31], [32, 63], [64, 95], [96, 127]]

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

            with self.open(self.filepath) as cdf_file:
                # if units are not specified, assume Hz
                units = Unit(cdf_file["TNR_BAND_FREQ"].attrs["UNITS"].strip() or "Hz")
                self._frequencies = (
                    np.sort(self.file["TNR_BAND_FREQ"][...].flatten()) * units
                )

        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            # Get Epoch time values for Band A
            mask = self.file["TNR_BAND"] == 0
            self._times = Time(self.file["Epoch"][mask])
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
