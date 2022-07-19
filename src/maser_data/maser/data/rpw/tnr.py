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

        for band_index in range(
            4
        ):  # 0 for band A, 1 for band B, 2 for band C and 3 for band D
            array_band_index = (
                self.data_reference.TNR_CURRENT_BAND_WORKING_ON == band_index
            ).nonzero()[0]
            auto_1 = self.data_reference.auto1[array_band_index]
            auto_2 = self.data_reference.auto2[array_band_index]
            sensor_config = self.data_reference.sensor_config[array_band_index]
            phase = self.data_reference.PHASE[array_band_index]
            flux_1 = self.data_reference.flux1[array_band_index]
            flux_2 = self.data_reference.flux2[array_band_index]
            magnetic_1 = self.data_reference.magnetic1[array_band_index]
            magnetic_2 = self.data_reference.magnetic2[array_band_index]
            times = self.data_reference.epoch[array_band_index]
            for time, a1, a2, sc, ph, f1, f2, m1, m2 in zip(
                times,
                auto_1,
                auto_2,
                sensor_config,
                phase,
                flux_1,
                flux_2,
                magnetic_1,
                magnetic_2,
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
                    band_index,
                )


class RpwTnrSurv(CdfData, dataset="solo_L2_rpw-tnr-surv"):
    _iter_sweep_class = RpwTnrSurvSweeps

    frequency_band_labels = ["A", "B", "C", "D"]

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

    # @property
    def frequencies(self):
        if self._frequencies is None:

            self._frequencies = {}
            with self.open(self.filepath) as cdf_file:
                for band_label, frequency_band in enumerate(self.frequency_bands):
                    # if units are not specified, assume Hz
                    units = cdf_file["TNR_BAND_FREQ"].attrs["UNITS"].strip() or "Hz"
                    freq = cdf_file["TNR_BAND_FREQ"][band_label, :] * Unit(units)
                    self._frequencies[frequency_band] = freq

        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            self._times = {}
            for band_index, frequency_band in enumerate(self.frequency_bands):
                mask = self.TNR_CURRENT_BAND_WORKING_ON == band_index
                self._times[frequency_band] = Time(self.epoch[mask])
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
        # print(len(list(sensor_config)))

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

    def plot_auto(self, ax, sensor="V1-V2", cbar_ax=None, **kwargs):
        from matplotlib import colors
        import matplotlib.colorbar as cbar

        # create a colorbar axis
        if cbar_ax is None:
            cbar_ax, kw = cbar.make_axes(ax)

        auto = self.as_xarray()["auto"]

        # keep only V1-V2 sensor
        v1_v2_auto = auto.where(auto.sensor == sensor, drop=True)

        # determine min/max for the colorbar
        vmin = v1_v2_auto.where(v1_v2_auto > 0).min()
        vmax = v1_v2_auto.max()

        print("kwargs:", kwargs)

        plot_kwargs = {
            "cmap": "jet",
            "norm": "log",
            "vmin": vmin,
            "vmax": vmax,
            **kwargs,
        }

        # create a new norm object to display the colorbar in log scale
        if "norm" in plot_kwargs and plot_kwargs["norm"] == "log":
            plot_kwargs["norm"] = colors.LogNorm()

        print("plot_kwargs:", plot_kwargs)

        meshes = []

        # group data by band and plot each channel
        for band, data_array in v1_v2_auto.groupby("band"):
            for channel in self.channel_labels:
                mesh = data_array.sel(channel=channel).plot.pcolormesh(
                    cbar_ax=cbar_ax,
                    ax=ax,
                    x="time",
                    y="frequency",
                    yscale="log",
                    add_colorbar=True,
                    **plot_kwargs,
                )

                meshes.append(mesh)

        return {
            "ax": ax,
            "cbar_ax": cbar_ax,
            "vmin": vmin,
            "vmax": vmax,
            "meshes": meshes,
        }


if __name__ == "__main__":
    from maser.data import Data
    from pathlib import Path
    import matplotlib.pyplot as plt

    data_path = Path(__file__).parents[5] / "tests" / "data" / "solo" / "rpw"

    print(data_path)

    # tnr_file = "solo_L2_rpw-tnr-surv_20211127_V02.cdf"
    tnr_file = "solo_L2_rpw-tnr-surv_20220118_V02.cdf"
    tnr_filepath = data_path / tnr_file

    tnr_data = Data(filepath=tnr_filepath)
    fig, ax = plt.subplots()
    tnr_data.plot_auto(ax)
    plt.show()
