# -*- coding: utf-8 -*-
from matplotlib.colors import BoundaryNorm
from maser.data.base import CdfData
from astropy.time import Time
from astropy.units import Unit
from maser.data.base.sweeps import Sweeps
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.colorbar as cbar

from maser.data.rpw.filtre_for_tnr import pre_process


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

    def load(self):  # loading all the data
        with self.open(self.filepath) as data_L2_TNR:
            # with pycdf.CDF(self.filepath) as data_L2_TNR:
            self.TNR_BAND_FREQ = data_L2_TNR["TNR_BAND_FREQ"][...]
            self.frequenciesA = self.TNR_BAND_FREQ[0, :]  # Band A
            self.frequenciesB = self.TNR_BAND_FREQ[1, :]  # Band B
            self.frequenciesC = self.TNR_BAND_FREQ[2, :]  # Band C
            self.frequenciesD = self.TNR_BAND_FREQ[3, :]  # Band D
            self._frequencies_ = np.append(self.frequenciesA, self.frequenciesB)
            self._frequencies_ = np.append(self._frequencies_, self.frequenciesC)
            self._frequencies_ = np.append(self._frequencies_, self.frequenciesD)
            self.freqtest = data_L2_TNR["FREQUENCY"][...]
            self.freq_tnr1 = np.append(self.freqtest[0, :], self.freqtest[1, :])
            self.freq_tnr2 = np.append(self.freqtest[2, :], self.freqtest[3, :])
            self.freq_tnr = np.append(self.freq_tnr1, self.freq_tnr2)
            self.epoch = data_L2_TNR["Epoch"][...]  # Epoch
            self.sensor_config = data_L2_TNR["SENSOR_CONFIG"][
                ...
            ]  # Sensor configuration at each acquisition
            self.sweep_num = data_L2_TNR["SWEEP_NUM"][
                ...
            ]  # Sweep Number (A, B, C, D for one sweep)
            self.auto1 = data_L2_TNR["AUTO1"][...]
            self.auto2 = data_L2_TNR["AUTO2"][...]
            self.flux1 = data_L2_TNR["FLUX_DENSITY1"][...]
            self.flux2 = data_L2_TNR["FLUX_DENSITY2"][...]
            self.magnetic1 = data_L2_TNR["MAGNETIC_SPECTRAL_POWER1"][...]
            self.magnetic2 = data_L2_TNR["MAGNETIC_SPECTRAL_POWER2"][...]
            self.channel_status_data = data_L2_TNR["CHANNEL_STATUS"][...]
            self.TNR_CURRENT_BAND_WORKING_ON = data_L2_TNR["TNR_BAND"][...]
            self.PHASE = data_L2_TNR["PHASE"]
            self.frequences = data_L2_TNR["FREQUENCY"][...]

    frequency_keys = ["A", "B", "C", "D"]  # Label for TNR band

    # @property
    def frequencies(self):
        if self._frequencies is None:

            self._frequencies = {}
            with self.open(self.filepath) as cdf_file:
                for band_label, frequency_key in enumerate(self.frequency_keys):
                    # if units are not specified, assume Hz
                    units = cdf_file["TNR_BAND_FREQ"].attrs["UNITS"].strip() or "Hz"
                    freq = cdf_file["TNR_BAND_FREQ"][band_label, :] * Unit(units)
                    self._frequencies[frequency_key] = freq

        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            self._times = {}
            for band_index, frequency_key in enumerate(self.frequency_keys):
                mask = self.TNR_CURRENT_BAND_WORKING_ON == band_index
                self._times[frequency_key] = Time(self.epoch[mask])
        return self._times

    def as_array(
        self, sensor
    ):  # A method that returns a dictionary containing all the data for sensor (non valid values are filtered)
        sensor_index = (self.sensor_config == sensor).nonzero()[0]
        sensor_config_ = self.sensor_config[sensor_index]
        current_TNR_band = self.TNR_CURRENT_BAND_WORKING_ON[sensor_index]
        sweep_sensor = self.sweep_num[sensor_index]
        times_sensor = self.epoch[sensor_index]
        auto1_sensor = self.auto1[sensor_index]
        auto2_sensor = self.auto2[sensor_index]
        flux1_sensor = self.flux1[sensor_index]
        flux2_sensor = self.flux2[sensor_index]
        size_data = np.size(sensor_index)
        # dic_frequencies_per_band = self.frequencies()

        if auto1_sensor[0, 0] > 0:
            auto = auto1_sensor[0, :]
        else:
            auto = auto2_sensor[0, :]

        if flux1_sensor[0, 0] > 0:
            flux = flux1_sensor[0, :]
        else:
            flux = flux2_sensor[0, :]

        frequencies_sensor = self.frequences[sensor_index]

        for index in range(1, size_data):

            # if (auto1_sensor[index][0]>=0):
            # auto=np.vstack((auto,auto1_sensor[index,:]))
            # if (auto2_sensor[index][0]>=0):
            # auto=np.vstack((auto,auto2_sensor[index,:]))

            # if (flux1_sensor[index][0]>=0):
            # flux=np.vstack((flux,flux1_sensor[index,:]))
            # if (flux2_sensor[index][0]>=0):
            # flux=np.vstack((flux,flux2_sensor[index,:]))

            # if (channel_status[index][0]==0):
            # auto=np.vstack((auto,auto1_sensor[index,:]))
            # flux=np.vstack((flux,flux1_sensor[index,:]))

            # if (channel_status[index][0]==1):
            # auto=np.vstack((auto,auto2_sensor[index,:]))
            # flux=np.vstack((flux,flux2_sensor[index,:]))

            if sensor_config_[index][0] == sensor:
                auto = np.vstack((auto, auto1_sensor[index, :]))
                flux = np.vstack((flux, flux1_sensor[index, :]))

            if sensor_config_[index][1] == sensor:
                auto = np.vstack((auto, auto2_sensor[index, :]))
                flux = np.vstack((flux, flux2_sensor[index, :]))

        # Delete the first and last values that not correspond to an entire sweep
        i = 0
        sweep_sensor_bis = sweep_sensor
        while sweep_sensor[i] != sweep_sensor[i + 3]:
            auto = auto[1:]
            times_sensor = times_sensor[1:]
            current_TNR_band = current_TNR_band[1:]
            i = i + 1
        size_data = size_data - i

        q = size_data
        k = 0
        while sweep_sensor_bis[q - 1] != sweep_sensor_bis[q - 4]:
            auto = auto[: q - 1]
            times_sensor = times_sensor[: q - 1]
            current_TNR_band = current_TNR_band[: q - 1]
            q = q - 1
            k = k + 1
        size_data = size_data - k

        dic_sensor = {
            "TNR_BAND": current_TNR_band,
            "AUTO": auto,
            "Size_data": size_data,
            "FLUX": flux,
            "times": times_sensor,
            "FREQUENCIES_SENSOR": frequencies_sensor,
        }

        # Interpolation of AUTO for each time
        auto_interpolation = np.zeros((size_data, 128))
        auto_interpolation[0][0:32] = auto[0]
        auto_interpolation[0][32:64] = auto[1]
        auto_interpolation[0][64:96] = auto[2]
        auto_interpolation[0][96:128] = auto[3]

        for i in range(1, size_data):
            if current_TNR_band[i] == current_TNR_band[0]:
                auto_interpolation[i][0:32] = auto[i]
                auto_interpolation[i][32:64] = auto_interpolation[i - 1][32:64]
                auto_interpolation[i][64:96] = auto_interpolation[i - 1][64:96]
                auto_interpolation[i][96:128] = auto_interpolation[i - 1][96:128]
            if current_TNR_band[i] == current_TNR_band[1]:
                auto_interpolation[i][32:64] = auto[i]
                auto_interpolation[i][0:32] = auto_interpolation[i - 1][0:32]
                auto_interpolation[i][64:96] = auto_interpolation[i - 1][64:96]
                auto_interpolation[i][96:128] = auto_interpolation[i - 1][96:128]
            if current_TNR_band[i] == current_TNR_band[2]:
                auto_interpolation[i][64:96] = auto[i]
                auto_interpolation[i][0:32] = auto_interpolation[i - 1][0:32]
                auto_interpolation[i][32:64] = auto_interpolation[i - 1][32:64]
                auto_interpolation[i][96:128] = auto_interpolation[i - 1][96:128]
            if current_TNR_band[i] == current_TNR_band[3]:
                auto_interpolation[i][96:128] = auto[i]
                auto_interpolation[i][32:64] = auto_interpolation[i - 1][32:64]
                auto_interpolation[i][64:96] = auto_interpolation[i - 1][64:96]
                auto_interpolation[i][0:32] = auto_interpolation[i - 1][0:32]

        dic_sensor["AUTO_INTERPOLATION"] = auto_interpolation

        return dic_sensor

    def datas_per_band(
        self, band, sensor=4
    ):  # Return a dictionnary that contains the data of a band (times,auto)

        # Filtering all the rows containing the given sensor
        sensor_index = (self.sensor_config == sensor).nonzero()[0]
        sensor_config_ = self.sensor_config[sensor_index]
        current_TNR_band = self.TNR_CURRENT_BAND_WORKING_ON[sensor_index]
        times_sensor = self.epoch[sensor_index]
        auto1_sensor = self.auto1[sensor_index]
        auto2_sensor = self.auto2[sensor_index]
        channel_status = self.channel_status_data[sensor_index]

        # Filtering all the rows containing the given band
        current_TNR_band_index = (current_TNR_band == band).nonzero()[0]
        sensor_config_ = sensor_config_[current_TNR_band_index]
        times_sensor = times_sensor[current_TNR_band_index]
        auto1_sensor = auto1_sensor[current_TNR_band_index]
        auto2_sensor = auto2_sensor[current_TNR_band_index]
        channel_status = channel_status[current_TNR_band_index]
        size = np.size(times_sensor)

        # Initialisation
        if sensor_config_[0][0] == sensor:
            auto = auto1_sensor[0, :]

        if sensor_config_[0][1] == sensor:
            auto = auto2_sensor[0, :]

        # loop and chosing the correct auto
        for index in range(1, size):
            if sensor_config_[index][0] == sensor:
                auto = np.vstack((auto, auto1_sensor[index, :]))
            else:
                auto = np.vstack((auto, auto2_sensor[index, :]))

        dict_band = {
            "Times": times_sensor,
            "Auto": auto,
            "auto_min": auto.min(),
            "auto_max": auto.max(),
        }

        return dict_band

    def datas_dic_per_band(
        self,
    ):  # a function that returns a dictionnary of all data of each band
        data_dic_per_band = {}
        for i in range(4):
            data_dic_per_band[i] = self.datas_per_band(sensor=4, band=i)
        return data_dic_per_band

    def plot_tnr_data_for_quicklook_SonnyVersion(  # Plot the spectrum by using datas_dic_per_band and pcolormesh
        self,
    ):  # 0 for band A, 1 for band B, 2 for band C, 3 for band D
        # with self.datas_dic_per_band() as dic_data:
        dic_data = self.datas_dic_per_band()
        auto = {
            0: dic_data[0]["Auto"],
            1: dic_data[1]["Auto"],
            2: dic_data[2]["Auto"],
            3: dic_data[3]["Auto"],
        }  # one dictionary for auto
        times = {
            0: dic_data[0]["Times"],
            1: dic_data[1]["Times"],
            2: dic_data[2]["Times"],
            3: dic_data[3]["Times"],
        }  # one dictionary for times
        freq = {
            0: self.frequenciesA,
            1: self.frequenciesB,
            2: self.frequenciesC,
            3: self.frequenciesD,
        }  # one dictionary for frequencies
        auto_min = min(
            dic_data[0]["auto_min"],
            dic_data[1]["auto_min"],
            dic_data[2]["auto_min"],
            dic_data[3]["auto_min"],
        )  # get minimum value of auto
        auto_max = max(
            dic_data[0]["auto_max"],
            dic_data[1]["auto_max"],
            dic_data[2]["auto_max"],
            dic_data[3]["auto_max"],
        )  # get maximum value of auto
        # print("auto_min,auto_max", auto_min, auto_max)
        fig, ax = plt.subplots(1, 1, figsize=(9, 16))
        cbar_ax, kw = cbar.make_axes(ax)
        cmap = plt.get_cmap("jet")

        # norm=BoundaryNorm(levels,ncolors=cmap.N,clip=True)

        for index_band in range(3):
            x, y = np.meshgrid(times[index_band], freq[index_band])
            auto_log = 10 * np.log10(auto[index_band])
            auto_log = np.transpose(auto_log)
            im = ax.pcolormesh(
                x,
                y,
                auto_log,
                cmap=cmap,
                vmax=10 * np.log10(auto_max),
                vmin=10 * np.log10(auto_min),
            )

        fig.colorbar(im, cax=cbar_ax)
        ax.set_yscale("log")
        ax.set_xlabel("Times")
        ax.set_ylabel("frequencies")

        plt.show()

    def plot_filtered_values(
        self,
    ):  # Plot the filtered spectrum  using pre_process function and as_array with contourf
        _times = self.as_array(sensor=4)["times"]
        FOI = self._frequencies_
        x, y = np.meshgrid(_times, FOI)
        auto_int = self.as_array(sensor=4)["AUTO_INTERPOLATION"]
        auto_int = np.transpose(auto_int)
        auto_int_log, auto_int_log_filtered = pre_process(auto_int)
        levels = MaxNLocator(nbins=250).tick_values(
            auto_int_log_filtered.min(), auto_int_log_filtered.max()
        )
        plt.contourf(x, y, auto_int_log_filtered, levels=levels, cmap="jet")
        cbar = plt.colorbar()
        cbar.set_label("Power spectral density (10*log10 V²/Hz)", fontsize=20)
        plt.yscale("log")
        plt.xlabel("Time", fontsize=20)
        plt.xticks(rotation=45)
        plt.ylabel("Frequency (MHz)", fontsize=20)
        plt.title("Power spectral density", fontsize=20)
        plt.show()

    def plot_filtered_values_pcolormesh(
        self,
    ):  # Plot the filtered spectrum  using pre_process function and as_array with pcolormesh
        _times = self.as_array(sensor=4)["times"]
        FOI = self._frequencies_
        x, y = np.meshgrid(_times, FOI)
        auto_int = self.as_array(sensor=4)["AUTO_INTERPOLATION"]
        auto_int = np.transpose(auto_int)
        auto_int_log, auto_int_log_filtered = pre_process(auto_int)
        levels = MaxNLocator(nbins=250).tick_values(
            auto_int_log_filtered.min(), auto_int_log_filtered.max()
        )
        cmap = plt.get_cmap("jet")
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        fig, ax0 = plt.subplots(nrows=1)
        im = ax0.pcolormesh(x, y, auto_int_log_filtered, cmap=cmap, norm=norm)
        fig.colorbar(im, ax=ax0)
        ax0.set_yscale("log")
        ax0.set_xlabel("Temps")
        ax0.set_ylabel("frequences")
        plt.show()

    def plot_tnr_data_for_quicklook(
        self,
    ):  # plot the spectrum using as_array and pcolormesh
        """Plot the TNR data using an array datasets and matplotlib with pcolormesh

        Args:
            datasets (dict) : a dict containing TNR-SURV data as array datasets

        Returns:
            tuple: matplotlib figure and axes
        """

        # with self.as_array(sensor=4) as datasets:
        datasets = self.as_array(sensor=4)
        auto_interpolation_log = 10 * np.log10(datasets["AUTO_INTERPOLATION"])
        _times_ = datasets["times"]
        # while self.TNR_CURRENT_BAND_WORKING_ON[i]!=0:
        # auto_interpolation_log=auto_interpolation_log[1:]
        # _times_=_times_[1:]
        # i=i+1
        # print(i)
        x, y = np.meshgrid(_times_, self._frequencies_ / 1000)
        # auto_interpolation_log = 10 * np.log10(datasets["AUTO_INTERPOLATION"])
        levels = MaxNLocator(nbins=250).tick_values(
            auto_interpolation_log.min(), auto_interpolation_log.max()
        )
        cmap = plt.get_cmap("jet")
        norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
        fig, ax0 = plt.subplots(nrows=1)
        auto_interpolation_log = np.transpose(auto_interpolation_log)
        im = ax0.pcolormesh(x, y, auto_interpolation_log, cmap=cmap, norm=norm)
        fig.colorbar(im, ax=ax0)
        ax0.set_yscale("log")
        ax0.set_xlabel("Temps")
        ax0.set_ylabel("frequences")
        plt.show()

    def plot_tnr_data_for_quicklook_bis(
        self,
    ):  # plot the spectrum using as_array and contourf
        """Plot the TNR data using an array datasets and matplotlib with contourf

        Args:
            datasets (dict) : a dict containing TNR-SURV data as array datasets

        Returns:
            tuple: matplotlib figure and axes
        """
        datasets = self.as_array(sensor=4)
        x, y = np.meshgrid(
            datasets["times"], self._frequencies_ / 1000
        )  # avec self._frequencies_ il y a un pb ...
        auto_interpolation_log = 10 * np.log10(datasets["AUTO_INTERPOLATION"])
        plt.contourf(x, y / 1000, auto_interpolation_log.T, levels=100, cmap="jet")
        cbar = plt.colorbar()
        cbar.set_label("Power spectral density (10*log10 V²/Hz)", fontsize=20)
        plt.yscale("log")
        plt.xlabel("Time", fontsize=20)
        plt.xticks(rotation=45)
        plt.ylabel("Frequency (MHz)", fontsize=20)
        plt.title("Power spectral density", fontsize=20)
        plt.show()

    def data_TNR_per_band_per_frequencies(
        self, band
    ):  # Return a dictionary that contains all data per frequencies for a given band including magnetic_data and flux_density without filtering the fillvalue
        array_index_band = (self.TNR_CURRENT_BAND_WORKING_ON == band).nonzero()[0]
        times_band = self.epoch[array_index_band]
        data_dic_per_frequencies = {}
        for index in range(32):
            frequency = self.TNR_BAND_FREQ[band][index]
            auto1_data_f = self.auto1[array_index_band][:, index]
            auto2_data_f = self.auto2[array_index_band][:, index]
            magnetic1_data_f = self.magnetic1[array_index_band][:, index]
            magnetic2_data_f = self.magnetic2[array_index_band][:, index]
            flux_density1_data_f = self.flux1[array_index_band][:, index]
            flux_density2_data_f = self.flux2[array_index_band][:, index]
            data_dic_f = {
                "epoch_record": times_band,
                "auto1_data_f": auto1_data_f,
                "auto2_data_f": auto2_data_f,
                "magnetic1_data_f": magnetic1_data_f,
                "magnetic2_data_f": magnetic2_data_f,
                "flux_density1_data_f": flux_density1_data_f,
                "flux_density2_data_f": flux_density2_data_f,
                "band": band,
            }
            data_dic_per_frequencies[frequency] = data_dic_f

        return data_dic_per_frequencies

    def as_xarray(self):  # Return the data as a xarray

        import xarray

        datasets = {
            "AUTO": {},
        }

        default_units = {"AUTO": "V^2/Hz"}

        with self.open(self.filepath) as cdf_file:

            for band_label, frequency_key in enumerate(self.frequency_keys):
                frequencies = self.frequencies()[frequency_key]
                if len(frequencies) == 0:
                    continue
                # times = self.file[f"Epoch_{frequency_key}"][...]
                _times_ = self.datas_per_band(band_label)["Times"]

                # force lower keys for frequency and time attributes
                time_attrs = {k.lower(): v for k, v in cdf_file["Epoch"].attrs.items()}

                frequency_attrs = {
                    k.lower(): v for k, v in cdf_file["TNR_BAND_FREQ"].attrs.items()
                }

                if not frequency_attrs["units"].strip():
                    frequency_attrs["units"] = "Hz"

                for dataset_key in datasets:
                    values = self.datas_per_band(band_label)["Auto"]
                    attrs = {k.lower(): v for k, v in cdf_file["AUTO1"].attrs.items()}

                    # if units are not defined, use the default ones
                    if not attrs["units"].strip():
                        attrs["units"] = default_units.get(dataset_key, "")

                    datasets[dataset_key][frequency_key] = xarray.DataArray(
                        values.T,
                        coords=[
                            ("frequency", frequencies, frequency_attrs),
                            ("time", _times_, time_attrs),
                        ],
                        attrs=attrs,
                        name=f"{dataset_key}_{frequency_key}",
                    )

        return datasets


# ----------------------------------------
