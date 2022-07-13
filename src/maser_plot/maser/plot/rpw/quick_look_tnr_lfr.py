# -*- coding: utf-8 -*-
import datetime
from matplotlib import colors, pyplot as plt
import numpy
import xarray

# from maser import data
from maser.data import Data
import matplotlib.colorbar as cbar

import matplotlib.dates as mdates


def plot_combined_data(lfr_filepath, tnr_filepath):
    lfr_data = Data(filepath=lfr_filepath)
    tnr_data = Data(filepath=tnr_filepath)
    return tnr_data.as_xarray()
    # tnr_data.load()

    fields = ["PB", "PE", "DOP", "ELLIP", "SX_REA"]

    fig, axes = plt.subplots(len(fields), 1, sharex=True)

    axes_dict = {key: value for key, value in zip(fields, axes)}

    # prepare kwargs for each dataset/plot
    plot_kwargs = {
        "PE": {"norm": colors.LogNorm(), "vmin": PE_min, "vmax": PE_max},
        "PB": {"norm": colors.LogNorm(), "vmin": PB_min, "vmax": PB_max},
        "DOP": {"vmin": 0, "vmax": 1},
        "ELLIP": {"vmin": 0, "vmax": 1},
        "SX_REA": {},
    }

    quick_look_tnr_lfr(fig, axes_dict, lfr_data, tnr_data, plot_kwargs)

    # plt.savefig(savefigpath)


def quick_look_tnr_lfr(
    fig, axes, lfr_data, tnr_data, max_gap_in_sec=3600, plot_kwargs={}
):

    lfr_datasets = lfr_data.as_xarray()

    # loop over frequency bands F0, F1, F2 for Burst/Normal modes
    for field in ["PB", "PE", "DOP", "ELLIP", "SX_REA"]:
        for freq_band in lfr_data.frequency_bands[1:]:
            # determine data gaps larger than max_gap_in_sec
            times = lfr_datasets[field][freq_band].coords["time"].values
            gaps_indices = numpy.where(
                times[1:] - times[:-1] > numpy.timedelta64(max_gap_in_sec, "s")
            )

            # get the start time of each gap
            gaps_start_times = times[gaps_indices]

            # introduce nan values in these gaps to avoid large interpolation bands in matplotlib plots
            time_shifted = gaps_start_times + numpy.timedelta64(1, "ns")
            lfr_datasets[field][freq_band] = lfr_datasets[field][freq_band].reindex(
                time=numpy.concatenate((times, time_shifted)), fill_value=numpy.nan
            )

    tnr_datasets = tnr_data.as_xarray()

    return

    voltage = lfr_datasets["PE"]

    if "B_F0" in voltage:
        voltage["B_F0"] = voltage["B_F0"][0:6]

    if "N_F0" in voltage:
        voltage["N_F0"] = voltage["N_F0"][0:3]

    magnetic = lfr_datasets["PB"]

    dop = _xarray_wo_F0["DOP"]

    PB_min = None
    PB_max = None

    PE_min = None
    PE_max = None

    for key in voltage:
        voltage[key].values = 10 * numpy.log10(voltage[key].values)

        if PE_min is None:
            PE_min = voltage[key].values.min()
        if PE_max is None:
            PE_max = voltage[key].values.max()

        PE_min = min(PE_min, voltage[key].values.min())
        PE_max = max(PE_max, voltage[key].values.max())

    for key_B in magnetic:
        magnetic[key_B].values = 10 * numpy.log10(magnetic[key_B].values)

        if PB_min is None:
            PB_min = magnetic[key_B].values.min()
        if PB_max is None:
            PB_max = magnetic[key_B].values.max()

        PB_min = min(PB_min, magnetic[key_B].values.min())
        PB_max = max(PB_max, magnetic[key_B].values.max())

    for key_BB in magnetic_xarray:
        magnetic_xarray[key_BB].values = 10 * numpy.log10(
            magnetic_xarray[key_BB].values
        )

    dic_voltage_lfr = {}

    for key_volt in voltage_xarray:
        voltage_xarray[key_volt].values = 10 * numpy.log10(
            voltage_xarray[key_volt].values
        )

    for key_voltage_lfr in voltage_xarray:
        dic_voltage_lfr[key_voltage_lfr] = voltage_xarray[key_voltage_lfr]

    dic_data = my_data_tnr.datas_dic_per_band()
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
        0: tnr_data.frequenciesA,
        1: tnr_data.frequenciesB,
        2: tnr_data.frequenciesC,
        3: tnr_data.frequenciesD,
    }  # one dictionary for frequencies
    auto_min = min(
        # PE_min,
        dic_data[0]["auto_min"],
        dic_data[1]["auto_min"],
        dic_data[2]["auto_min"],
        dic_data[3]["auto_min"],
    )  # get minimum value of auto
    auto_max = max(
        # PE_max,
        dic_data[0]["auto_max"],
        dic_data[1]["auto_max"],
        dic_data[2]["auto_max"],
        dic_data[3]["auto_max"],
    )  # get maximum value of auto

    auto_max = 10 * numpy.log10(auto_max)
    auto_min = 10 * numpy.log10(auto_min)

    auto_min = min(auto_min, PE_min)
    auto_max = max(auto_max, PE_max)

    cbar_ax, kw = cbar.make_axes(axes[0])
    cmap = plt.get_cmap("jet")

    for key_volt_lfr in dic_voltage_lfr:
        x, y = numpy.meshgrid(
            dic_voltage_lfr[key_volt_lfr].time.values,
            dic_voltage_lfr[key_volt_lfr].frequency.values,
        )
        im = axes[0].pcolormesh(
            x,
            y,
            dic_voltage_lfr[key_volt_lfr].values,
            cmap=cmap,
            # levels=10,
            vmax=auto_max,
            vmin=auto_min,
        )

    for index_band in range(3):
        x, y = numpy.meshgrid(times[index_band], freq[index_band])
        auto_log = 10 * numpy.log10(auto[index_band])
        auto_log = numpy.transpose(auto_log)
        im = axes[0].pcolormesh(
            x,
            y,
            auto_log,
            cmap=cmap,
            vmax=auto_max,
            vmin=auto_min,
        )

    fig.colorbar(im, cax=cbar_ax)
    axes[0].set_yscale("log")

    axes[0].set_ylabel("frequency[Hz]")
    cbar_ax.set_ylabel("PE (V²/Hz)")

    _datasets_ = {"PB": magnetic_xarray, "DOP": dop}

    for ax_idx, dataset_key in enumerate(_datasets_):

        # select the ax to plot on
        ax = axes[ax_idx + 1]

        # create the associated colorbar
        cbar_ax, kw = cbar.make_axes(ax)

        # compute vmin and vmax by taking the min and max of each dataset for each frequency range
        vmin = plot_kwargs[dataset_key].get("vmin", None)
        if vmin is None:
            for data_array in _datasets_[dataset_key].values():
                vmin = (
                    min(vmin, data_array.min())
                    if vmin is not None
                    else data_array.min()
                )
            plot_kwargs[dataset_key]["vmin"] = vmin

        vmax = plot_kwargs[dataset_key].get("vmax", None)
        if vmax is None:
            for data_array in _datasets_[dataset_key].values():
                vmax = (
                    max(vmax, data_array.max())
                    if vmax is not None
                    else data_array.max()
                )
            plot_kwargs[dataset_key]["vmax"] = vmax

        # plot the data
        for data_array in _datasets_[dataset_key].values():
            data_array.plot.pcolormesh(
                ax=ax,
                cmap=cmap,
                yscale="log",
                add_colorbar=True,
                shading="flat",
                vmin=vmin,
                vmax=vmax,
                cbar_ax=cbar_ax,
            )

        # set the color bar title
        if data_array.attrs["units"]:
            cbar_label = f'{dataset_key} [${data_array.attrs["units"]}$]'
        else:
            cbar_label = dataset_key
        cbar_ax.set_ylabel(cbar_label)

    title = times[0][80]
    title = title.strftime("%m/%d/%Y")
    title = title + " " + " Quick look of combined TNR and LFR data"

    xformatter = mdates.DateFormatter("%H:%M")
    axes[0].xaxis.set_major_formatter(xformatter)

    axes[0].set_xlabel("")
    axes[1].set_xlabel("")
    axes[2].set_xlabel("")

    axes[0].set_xlim(left=times[0][0], right=times[0][numpy.size(times[0]) - 1])

    if "N_F2" in voltage:

        axes[1].set_ylim(bottom=10.5, auto=True, emit=False)
        axes[2].set_ylim(bottom=10.5)

    plt.suptitle(title, fontweight="bold", style="italic", color="grey")


if __name__ == "__main__":
    from pathlib import Path

    data_path = "D:/projet/roc/maser4py/tests/data/solo/rpw/"

    tnr_file = "solo_L2_rpw-tnr-surv_20211127_V02.cdf"
    lfr_file = "solo_L2_rpw-lfr-surv-bp1_20211127_V02.cdf"
    plot_combined_data(
        lfr_filepath=Path(data_path + lfr_file), tnr_filepath=Path(data_path + tnr_file)
    )
