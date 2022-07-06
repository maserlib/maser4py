# -*- coding: utf-8 -*-
from examples.plot_rpw_data import plot_lfr_bp1_data
from maser.data.base import CdfData

from astropy.time import Time
from astropy.units import Unit
from maser.data.base.sweeps import Sweeps
import matplotlib.colorbar as cbar
from matplotlib import colors
from matplotlib import pyplot as plt
from maser.data import Data


class RpwLfrSurvBp1Sweeps(Sweeps):
    @property
    def generator(self):
        """
        For each time, yield a frequency range and a dictionary with the following keys:
        - PB: power spectrum of the magnetic field (nT^2/Hz),
        - PE: the power spectrum of the electric field (V^2/Hz),
        - DOP: the degree of polarization of the waves (unitless),
        - ELLIP: the wave ellipticity (unitless),
        - SX_REA: the real part of the radial component of the Poynting flux (V nT/Hn, QF=1),

        """
        for frequency_key in self.data_reference.frequency_keys:
            for time, pb, pe, dop, ellip, sx_rea in zip(
                self.data_reference.times[frequency_key],
                self.file[f"PB_{frequency_key}"][...],
                self.file[f"PE_{frequency_key}"][...],
                self.file[f"DOP_{frequency_key}"][...],
                self.file[f"ELLIP_{frequency_key}"][...],
                self.file[f"SX_REA_{frequency_key}"][...],
            ):
                yield (
                    {"PB": pb, "PE": pe, "DOP": dop, "ELLIP": ellip, "SX_REA": sx_rea},
                    Time(time),
                    self.data_reference.frequencies[frequency_key],
                )


class RpwLfrSurvBp1(CdfData, dataset="solo_L2_rpw-lfr-surv-bp1"):
    _iter_sweep_class = RpwLfrSurvBp1Sweeps

    # keys used to loop over F0, F1, F2 frequency ranges and Burst/Normal modes
    frequency_keys = ["N_F2", "B_F1", "N_F1", "B_F0", "N_F0"]

    #keys used to loop over F0 and F1 frequency ranges and Burst/Normal modes

    frequency_keys_wo_F0=["N_F2","B_F1","N_F1"]

    @property
    def frequencies(self):
        if self._frequencies is None:

            self._frequencies = {}

            with self.open(self.filepath) as cdf_file:
                for frequency_key in self.frequency_keys:
                    # if units are not specified, assume Hz
                    units = cdf_file[frequency_key].attrs["UNITS"].strip() or "Hz"
                    freq = cdf_file[frequency_key][...] * Unit(units)
                    self._frequencies[frequency_key] = freq

        return self._frequencies

    @property
    def times(self):
        if self._times is None:
            with self.open(self.filepath) as cdf_file:
                self._times = {}
                for frequency_key in self.frequency_keys:
                    #self._times[frequency_key] = Time(
                        #cdf_file[f"Epoch_{frequency_key}"][...]
                    #)
                    self._times[frequency_key] = cdf_file[f"Epoch_{frequency_key}"][...]
                    
        return self._times

    def as_xarray(self):
        import xarray

        datasets = {
            #"PB": {},
            "PE": {},
            "PB": {},
            "DOP": {},
            "ELLIP": {},
            "SX_REA": {},
        }

        default_units = {"PB": "nT^2/Hz"}

        for frequency_key in self.frequency_keys:
            frequencies = self.file[frequency_key][...]
            if len(frequencies) == 0:
                continue
            times = self.file[f"Epoch_{frequency_key}"][...]

            # force lower keys for frequency and time attributes
            time_attrs = {
                k.lower(): v
                for k, v in self.file[f"Epoch_{frequency_key}"].attrs.items()
            }

            frequency_attrs = {
                k.lower(): v for k, v in self.file[frequency_key].attrs.items()
            }
            if not frequency_attrs["units"].strip():
                frequency_attrs["units"] = "Hz"

            for dataset_key in datasets:
                values = self.file[f"{dataset_key}_{frequency_key}"][...]
                attrs = {
                    k.lower(): v
                    for k, v in self.file[
                        f"{dataset_key}_{frequency_key}"
                    ].attrs.items()
                }

                # if units are not defined, use the default ones
                if not attrs["units"].strip():
                    attrs["units"] = default_units.get(dataset_key, "")

                datasets[dataset_key][frequency_key] = xarray.DataArray(
                    values.T,
                    coords=[
                        ("frequency", frequencies, frequency_attrs),
                        ("time", times, time_attrs),
                    ],
                    attrs=attrs,
                    name=f"{dataset_key}_{frequency_key}",
                )
        return datasets



    def as_xarray_wo_F0(self):
        import xarray

        datasets = {
            #"PB": {},
            "PE": {},
            "PB": {},
            "DOP": {},
            "ELLIP": {},
            "SX_REA": {},
        }

        default_units = {"PB": "nT^2/Hz"}

        for frequency_key in self.frequency_keys_wo_F0:
            frequencies = self.file[frequency_key][...]
            if len(frequencies) == 0:
                continue
            times = self.file[f"Epoch_{frequency_key}"][...]

            # force lower keys for frequency and time attributes
            time_attrs = {
                k.lower(): v
                for k, v in self.file[f"Epoch_{frequency_key}"].attrs.items()
            }

            frequency_attrs = {
                k.lower(): v for k, v in self.file[frequency_key].attrs.items()
            }
            if not frequency_attrs["units"].strip():
                frequency_attrs["units"] = "Hz"

            for dataset_key in datasets:
                values = self.file[f"{dataset_key}_{frequency_key}"][...]
                attrs = {
                    k.lower(): v
                    for k, v in self.file[
                        f"{dataset_key}_{frequency_key}"
                    ].attrs.items()
                }

                # if units are not defined, use the default ones
                if not attrs["units"].strip():
                    attrs["units"] = default_units.get(dataset_key, "")

                datasets[dataset_key][frequency_key] = xarray.DataArray(
                    values.T,
                    coords=[
                        ("frequency", frequencies, frequency_attrs),
                        ("time", times, time_attrs),
                    ],
                    attrs=attrs,
                    name=f"{dataset_key}_{frequency_key}",
                )
        return datasets


    #def plot_lfr_bp1_data(self,datasets: dict) -> tuple:
    def plot_lfr_bp1_data(self):
        """Plot the LFR BP1 data using xarray datasets and matplotlib

        Args:
            datasets (dict): a dict containing LFR BP1 data as xarray datasets

        Returns:
            tuple: matplotlib figure and axes
        """
        datasets = self.as_xarray()

        # prepare kwargs for each dataset/plot
        plot_kwargs = {
            "PB": {"norm": colors.LogNorm()},
            "PE": {"norm": colors.LogNorm()},
            "DOP": {"vmin": 0, "vmax": 1},
            "ELLIP": {"vmin": 0, "vmax": 1},
            "SX_REA": {},
        }

        # create figure and axes
        fig, axes = plt.subplots(len(datasets), 1, sharex=True)
        # loop over datasets
        for ax_idx, dataset_key in enumerate(datasets):

            # select the ax to plot on
            ax = axes[ax_idx]

            # create the associated colorbar
            cbar_ax, kw = cbar.make_axes(ax)

            # compute vmin and vmax by taking the min and max of each dataset for each frequency range
            vmin = plot_kwargs[dataset_key].get("vmin", None)
            if vmin is None:
                for data_array in datasets[dataset_key].values():
                    vmin = (
                        min(vmin, data_array.min())
                        if vmin is not None
                        else data_array.min()
                    )
                plot_kwargs[dataset_key]["vmin"] = vmin

            vmax = plot_kwargs[dataset_key].get("vmax", None)
            if vmax is None:
                for data_array in datasets[dataset_key].values():
                    vmax = (
                        max(vmax, data_array.max())
                        if vmax is not None
                        else data_array.max()
                    )
                plot_kwargs[dataset_key]["vmax"] = vmax

            # plot the data
            for data_array in datasets[dataset_key].values():
                data_array.plot.pcolormesh(
                    ax=ax,
                    yscale="log",
                    add_colorbar=True,
                    **plot_kwargs[dataset_key],
                    cbar_ax=cbar_ax,
                )

            # set the color bar title
            if data_array.attrs["units"]:
                cbar_label = f'{dataset_key} [${data_array.attrs["units"]}$]'
            else:
                cbar_label = dataset_key
            cbar_ax.set_ylabel(cbar_label)
        return fig,axes

    def plot(self):
        datasets = self.as_xarray()
        #plot_lfr_bp1_data(datasets)
        fig,axes=self.plot_lfr_bp1_data()
        plt.show()