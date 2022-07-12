# -*- coding: utf-8 -*-
import datetime
from matplotlib import colors, pyplot as plt
import numpy as np

# from maser import data
from maser.data import Data
import matplotlib.colorbar as cbar

import matplotlib.dates as mdates


def quick_look_tnr_lfr_only_E_final(
    filepathtnr, filepathlfr
):  # Only E and displaying white when no values are available

    my_data_lfr = Data(filepath=filepathlfr)
    my_data_tnr = Data(filepath=filepathtnr)
    my_data_tnr.load()

    times_lfr = my_data_lfr.times

    fig, axes = plt.subplots(1, 1)

    datasets = my_data_lfr.as_xarray()

    _xarray_ = my_data_lfr.as_xarray()
    _xarray_wo_F0 = my_data_lfr.as_xarray_wo_F0()

    # keys used to loop over F0, F1, F2 frequency ranges and Burst/Normal modes
    frequency_keys = ["N_F2", "B_F1", "N_F1", "B_F0", "N_F0"]

    for key in frequency_keys:
        for index_time, time in enumerate(times_lfr[key]):
            if times_lfr[key][index_time] - times_lfr[key][
                index_time - 1
            ] > datetime.timedelta(hours=1):
                # dic[index_time-1]=time
                for physic_key in datasets:
                    _xarray_[physic_key][key].values[:, index_time - 1] = np.nan
                    _xarray_[physic_key][key].values[:, index_time] = np.nan
                    if key != "N_F0" and key != "B_F0":
                        _xarray_wo_F0[physic_key][key].values[
                            :, index_time - 1
                        ] = np.nan
                        _xarray_wo_F0[physic_key][key].values[:, index_time] = np.nan

    voltage_xarray = _xarray_["PE"]
    voltage = datasets["PE"]

    for i in voltage_xarray:
        voltage_xarray[i].values = 10 * np.log10(voltage_xarray[i])

    if "B_F0" in voltage:
        voltage["B_F0"] = voltage["B_F0"][0:6]

    if "N_F0" in voltage:
        voltage["N_F0"] = voltage["N_F0"][0:3]

    magnetic = _xarray_wo_F0["PB"]

    PB_min = None
    PB_max = None

    PE_min = None
    PE_max = None

    for key in voltage:
        voltage[key].values = 10 * np.log10(voltage[key].values)

        if PE_min is None:
            PE_min = voltage[key].values.min()
        if PE_max is None:
            PE_max = voltage[key].values.max()

        PE_min = min(PE_min, voltage[key].values.min())
        PE_max = max(PE_max, voltage[key].values.max())

    for key_B in magnetic:
        magnetic[key_B].values = 10 * np.log10(magnetic[key_B].values)

        if PB_min is None:
            PB_min = magnetic[key_B].values.min()
        if PB_max is None:
            PB_max = magnetic[key_B].values.max()

        PB_min = min(PB_min, magnetic[key_B].values.min())
        PB_max = max(PB_max, magnetic[key_B].values.max())

    dic_voltage_lfr = {}

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
        0: my_data_tnr.frequenciesA,
        1: my_data_tnr.frequenciesB,
        2: my_data_tnr.frequenciesC,
        3: my_data_tnr.frequenciesD,
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
    # print("auto_min,auto_max", auto_min, auto_max)

    auto_max = 10 * np.log10(auto_max)
    auto_min = 10 * np.log10(auto_min)

    auto_min = min(auto_min, PE_min)
    auto_max = max(auto_max, PE_max)

    cbar_ax, kw = cbar.make_axes(axes)
    cmap = plt.get_cmap("jet")
    # levels = MaxNLocator(nbins=250).tick_values(auto_min,auto_max)
    # norm=BoundaryNorm(levels,ncolors=cmap.N,clip=True)

    for key_volt_lfr in dic_voltage_lfr:
        x, y = np.meshgrid(
            dic_voltage_lfr[key_volt_lfr].time.values,
            dic_voltage_lfr[key_volt_lfr].frequency.values,
        )
        im = axes.pcolormesh(
            x,
            y,
            dic_voltage_lfr[key_volt_lfr].values,
            cmap=cmap,
            vmax=auto_max,
            vmin=auto_min,
        )

    for index_band in range(4):
        x, y = np.meshgrid(times[index_band], freq[index_band])
        auto_log = 10 * np.log10(auto[index_band])
        auto_log = np.transpose(auto_log)
        im = axes.pcolormesh(
            x,
            y,
            auto_log,
            cmap=cmap,
            vmax=auto_max,
            vmin=auto_min,
        )

    fig.colorbar(im, cax=cbar_ax)
    cbar_ax.set_ylabel("PE : V²/Hz (dB scale)")
    axes.set_yscale("log")
    axes.set_xlabel("Times")
    axes.set_ylabel("frequency[Hz]")
    axes.set_xlim(left=times[0][0], right=times[0][np.size(times[0]) - 1])

    xformatter = mdates.DateFormatter("%H:%M")
    axes.xaxis.set_major_formatter(xformatter)
    title = times[0][80]
    title = title.strftime("%m/%d/%Y")
    title_png = times[0][80].strftime("%m%d%Y")
    path = "/home/atokgozoglu/Documents/captureecran/"
    path = path + title_png
    title = title + " " + " combined TNR and LFR data"

    plt.suptitle(title, fontweight="bold", style="italic", color="grey")

    # plt.show()

    plt.savefig(path)


def quick_look_tnr_lfr_final(
    filepathtnr, filepathlfr
):  # plot quick_look and displaying white when no values are available
    my_data_lfr = Data(filepath=filepathlfr)
    my_data_tnr = Data(filepath=filepathtnr)
    my_data_tnr.load()

    fig, axes = plt.subplots(5, 1, sharex=True)

    times_lfr = my_data_lfr.times

    datasets = my_data_lfr.as_xarray()
    datasets_wo_F0 = my_data_lfr.as_xarray_wo_F0()

    _xarray_ = my_data_lfr.as_xarray()
    _xarray_wo_F0 = my_data_lfr.as_xarray_wo_F0()

    # keys used to loop over F0, F1, F2 frequency ranges and Burst/Normal modes
    frequency_keys = ["N_F2", "B_F1", "N_F1", "B_F0", "N_F0"]

    for key in frequency_keys:
        for index_time, time in enumerate(times_lfr[key]):
            if times_lfr[key][index_time] - times_lfr[key][
                index_time - 1
            ] > datetime.timedelta(hours=1):
                # dic[index_time-1]=time
                for physic_key in datasets:
                    _xarray_[physic_key][key].values[:, index_time - 1] = np.nan
                    _xarray_[physic_key][key].values[:, index_time] = np.nan
                    if key != "N_F0" and key != "B_F0":
                        _xarray_wo_F0[physic_key][key].values[
                            :, index_time - 1
                        ] = np.nan
                        _xarray_wo_F0[physic_key][key].values[:, index_time] = np.nan

    voltage = datasets["PE"]
    voltage_xarray = _xarray_["PE"]

    if "B_F0" in voltage:
        voltage["B_F0"] = voltage["B_F0"][0:6]

    if "N_F0" in voltage:
        voltage["N_F0"] = voltage["N_F0"][0:3]

    magnetic = datasets_wo_F0["PB"]
    magnetic_xarray = _xarray_wo_F0["PB"]
    dop = _xarray_wo_F0["DOP"]

    PB_min = None
    PB_max = None

    PE_min = None
    PE_max = None

    for key in voltage:
        voltage[key].values = 10 * np.log10(voltage[key].values)

        if PE_min is None:
            PE_min = voltage[key].values.min()
        if PE_max is None:
            PE_max = voltage[key].values.max()

        PE_min = min(PE_min, voltage[key].values.min())
        PE_max = max(PE_max, voltage[key].values.max())

    for key_B in magnetic:
        magnetic[key_B].values = 10 * np.log10(magnetic[key_B].values)

        if PB_min is None:
            PB_min = magnetic[key_B].values.min()
        if PB_max is None:
            PB_max = magnetic[key_B].values.max()

        PB_min = min(PB_min, magnetic[key_B].values.min())
        PB_max = max(PB_max, magnetic[key_B].values.max())

    for key_BB in magnetic_xarray:
        magnetic_xarray[key_BB].values = 10 * np.log10(magnetic_xarray[key_BB].values)

    dic_voltage_lfr = {}

    for key_volt in voltage_xarray:
        voltage_xarray[key_volt].values = 10 * np.log10(voltage_xarray[key_volt].values)

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
        0: my_data_tnr.frequenciesA,
        1: my_data_tnr.frequenciesB,
        2: my_data_tnr.frequenciesC,
        3: my_data_tnr.frequenciesD,
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
    # print("auto_min,auto_max", auto_min, auto_max)

    auto_max = 10 * np.log10(auto_max)
    auto_min = 10 * np.log10(auto_min)

    auto_min = min(auto_min, PE_min)
    auto_max = max(auto_max, PE_max)

    cbar_ax, kw = cbar.make_axes(axes[0])
    cmap = plt.get_cmap("jet")

    for key_volt_lfr in dic_voltage_lfr:
        x, y = np.meshgrid(
            dic_voltage_lfr[key_volt_lfr].time.values,
            dic_voltage_lfr[key_volt_lfr].frequency.values,
        )
        im = axes[0].pcolormesh(
            x,
            y,
            dic_voltage_lfr[key_volt_lfr].values,
            cmap=cmap,
            vmax=auto_max,
            vmin=auto_min,
        )

    for index_band in range(3):
        x, y = np.meshgrid(times[index_band], freq[index_band])
        auto_log = 10 * np.log10(auto[index_band])
        auto_log = np.transpose(auto_log)
        im = axes[0].pcolormesh(
            x,
            y,
            auto_log,
            cmap=cmap,
            # levels=10,
            vmax=auto_max,
            vmin=auto_min,
        )

    fig.colorbar(im, cax=cbar_ax)
    axes[0].set_yscale("log")
    # axes[0].set_xlabel("Times")
    axes[0].set_ylabel("frequency[Hz]")
    cbar_ax.set_ylabel("PE (V²/Hz)")

    # _datasets_={"PE":voltage,"PB":magnetic,"DOP":dop,"ELLIP":datasets_wo_F0["ELLIP"],"SX_REA":datasets_wo_F0["SX_REA"]}

    _datasets_ = {
        "PB": magnetic_xarray,
        "DOP": dop,
        "ELLIP": _xarray_wo_F0["ELLIP"],
        "SX_REA": _xarray_wo_F0["SX_REA"],
    }

    # prepare kwargs for each dataset/plot
    plot_kwargs = {
        "PE": {"norm": colors.LogNorm(), "vmin": PE_min, "vmax": PE_max},
        "PB": {"norm": colors.LogNorm(), "vmin": PB_min, "vmax": PB_max},
        "DOP": {"vmin": 0, "vmax": 1},
        "ELLIP": {"vmin": 0, "vmax": 1},
        "SX_REA": {},
    }

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
                # **plot_kwargs[dataset_key],
                # levels=10,
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
    axes[3].set_xlabel("")
    axes[4].set_xlabel("")

    axes[0].set_xlim(left=times[0][0], right=times[0][np.size(times[0]) - 1])

    plt.suptitle(title, fontweight="bold", style="italic", color="grey")

    plt.show()


def quick_look_tnr_lfr_final_PE_PB_DOP(
    filepathtnr, filepathlfr
):  # Displaying only PE, PB and DOP and set a bottom limit on y axis (10.5 Hz)
    my_data_lfr = Data(filepath=filepathlfr)
    my_data_tnr = Data(filepath=filepathtnr)
    my_data_tnr.load()

    fig, axes = plt.subplots(3, 1, sharex=True)

    times_lfr = my_data_lfr.times

    datasets = my_data_lfr.as_xarray()
    datasets_wo_F0 = my_data_lfr.as_xarray_wo_F0()

    _xarray_ = my_data_lfr.as_xarray()
    _xarray_wo_F0 = my_data_lfr.as_xarray_wo_F0()

    # keys used to loop over F0, F1, F2 frequency ranges and Burst/Normal modes
    frequency_keys = ["N_F2", "B_F1", "N_F1", "B_F0", "N_F0"]

    for key in frequency_keys:
        for index_time, time in enumerate(times_lfr[key]):
            if times_lfr[key][index_time] - times_lfr[key][
                index_time - 1
            ] > datetime.timedelta(hours=1):
                # dic[index_time-1]=time
                for physic_key in datasets:
                    _xarray_[physic_key][key].values[:, index_time - 1] = np.nan
                    _xarray_[physic_key][key].values[:, index_time] = np.nan
                    if key != "N_F0" and key != "B_F0":
                        _xarray_wo_F0[physic_key][key].values[
                            :, index_time - 1
                        ] = np.nan
                        _xarray_wo_F0[physic_key][key].values[:, index_time] = np.nan

    voltage = datasets["PE"]
    voltage_xarray = _xarray_["PE"]

    if "B_F0" in voltage:
        voltage["B_F0"] = voltage["B_F0"][0:6]

    if "N_F0" in voltage:
        voltage["N_F0"] = voltage["N_F0"][0:3]

    magnetic = datasets_wo_F0["PB"]
    magnetic_xarray = _xarray_wo_F0["PB"]
    dop = _xarray_wo_F0["DOP"]

    PB_min = None
    PB_max = None

    PE_min = None
    PE_max = None

    for key in voltage:
        voltage[key].values = 10 * np.log10(voltage[key].values)

        if PE_min is None:
            PE_min = voltage[key].values.min()
        if PE_max is None:
            PE_max = voltage[key].values.max()

        PE_min = min(PE_min, voltage[key].values.min())
        PE_max = max(PE_max, voltage[key].values.max())

    for key_B in magnetic:
        magnetic[key_B].values = 10 * np.log10(magnetic[key_B].values)

        if PB_min is None:
            PB_min = magnetic[key_B].values.min()
        if PB_max is None:
            PB_max = magnetic[key_B].values.max()

        PB_min = min(PB_min, magnetic[key_B].values.min())
        PB_max = max(PB_max, magnetic[key_B].values.max())

    for key_BB in magnetic_xarray:
        magnetic_xarray[key_BB].values = 10 * np.log10(magnetic_xarray[key_BB].values)

    dic_voltage_lfr = {}

    for key_volt in voltage_xarray:
        voltage_xarray[key_volt].values = 10 * np.log10(voltage_xarray[key_volt].values)

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
        0: my_data_tnr.frequenciesA,
        1: my_data_tnr.frequenciesB,
        2: my_data_tnr.frequenciesC,
        3: my_data_tnr.frequenciesD,
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
    # print("auto_min,auto_max", auto_min, auto_max)

    auto_max = 10 * np.log10(auto_max)
    auto_min = 10 * np.log10(auto_min)

    auto_min = min(auto_min, PE_min)
    auto_max = max(auto_max, PE_max)

    cbar_ax, kw = cbar.make_axes(axes[0])
    cmap = plt.get_cmap("jet")

    for key_volt_lfr in dic_voltage_lfr:
        x, y = np.meshgrid(
            dic_voltage_lfr[key_volt_lfr].time.values,
            dic_voltage_lfr[key_volt_lfr].frequency.values,
        )
        im = axes[0].pcolormesh(
            x,
            y,
            dic_voltage_lfr[key_volt_lfr].values,
            cmap=cmap,
            vmax=auto_max,
            vmin=auto_min,
        )

    for index_band in range(3):
        x, y = np.meshgrid(times[index_band], freq[index_band])
        auto_log = 10 * np.log10(auto[index_band])
        auto_log = np.transpose(auto_log)
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

    # prepare kwargs for each dataset/plot
    plot_kwargs = {
        "PE": {"norm": colors.LogNorm(), "vmin": PE_min, "vmax": PE_max},
        "PB": {"norm": colors.LogNorm(), "vmin": PB_min, "vmax": PB_max},
        "DOP": {"vmin": 0, "vmax": 1},
        "ELLIP": {"vmin": 0, "vmax": 1},
        "SX_REA": {},
    }

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

    axes[0].set_xlim(left=times[0][0], right=times[0][np.size(times[0]) - 1])

    if "N_F2" in voltage:

        axes[1].set_ylim(bottom=10.5, auto=True, emit=False)
        axes[2].set_ylim(bottom=10.5, auto=True, emit=False)

    plt.suptitle(title, fontweight="bold", style="italic", color="grey")

    plt.show()


def quick_look_tnr_lfr_savefig(filepathtnr, filepathlfr, savefigpath):
    my_data_lfr = Data(filepath=filepathlfr)
    my_data_tnr = Data(filepath=filepathtnr)
    my_data_tnr.load()

    fig, axes = plt.subplots(3, 1, sharex=True)

    times_lfr = my_data_lfr.times

    datasets = my_data_lfr.as_xarray()
    datasets_wo_F0 = my_data_lfr.as_xarray_wo_F0()

    _xarray_ = my_data_lfr.as_xarray()
    _xarray_wo_F0 = my_data_lfr.as_xarray_wo_F0()

    # keys used to loop over F0, F1, F2 frequency ranges and Burst/Normal modes
    frequency_keys = ["N_F2", "B_F1", "N_F1", "B_F0", "N_F0"]

    for key in frequency_keys:
        for index_time, time in enumerate(times_lfr[key]):
            if times_lfr[key][index_time] - times_lfr[key][
                index_time - 1
            ] > datetime.timedelta(hours=1):
                # dic[index_time-1]=time
                for physic_key in datasets:
                    _xarray_[physic_key][key].values[:, index_time - 1] = np.nan
                    _xarray_[physic_key][key].values[:, index_time] = np.nan
                    if key != "N_F0" and key != "B_F0":
                        _xarray_wo_F0[physic_key][key].values[
                            :, index_time - 1
                        ] = np.nan
                        _xarray_wo_F0[physic_key][key].values[:, index_time] = np.nan

    # print(datasets['PE'])

    voltage = datasets["PE"]
    voltage_xarray = _xarray_["PE"]

    if "B_F0" in voltage:
        voltage["B_F0"] = voltage["B_F0"][0:6]

    if "N_F0" in voltage:
        voltage["N_F0"] = voltage["N_F0"][0:3]

    magnetic = datasets_wo_F0["PB"]
    magnetic_xarray = _xarray_wo_F0["PB"]
    dop = _xarray_wo_F0["DOP"]

    PB_min = None
    PB_max = None

    PE_min = None
    PE_max = None

    for key in voltage:
        voltage[key].values = 10 * np.log10(voltage[key].values)

        if PE_min is None:
            PE_min = voltage[key].values.min()
        if PE_max is None:
            PE_max = voltage[key].values.max()

        PE_min = min(PE_min, voltage[key].values.min())
        PE_max = max(PE_max, voltage[key].values.max())

    for key_B in magnetic:
        magnetic[key_B].values = 10 * np.log10(magnetic[key_B].values)

        if PB_min is None:
            PB_min = magnetic[key_B].values.min()
        if PB_max is None:
            PB_max = magnetic[key_B].values.max()

        PB_min = min(PB_min, magnetic[key_B].values.min())
        PB_max = max(PB_max, magnetic[key_B].values.max())

    for key_BB in magnetic_xarray:
        magnetic_xarray[key_BB].values = 10 * np.log10(magnetic_xarray[key_BB].values)

    dic_voltage_lfr = {}

    for key_volt in voltage_xarray:
        voltage_xarray[key_volt].values = 10 * np.log10(voltage_xarray[key_volt].values)

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
        0: my_data_tnr.frequenciesA,
        1: my_data_tnr.frequenciesB,
        2: my_data_tnr.frequenciesC,
        3: my_data_tnr.frequenciesD,
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

    auto_max = 10 * np.log10(auto_max)
    auto_min = 10 * np.log10(auto_min)

    auto_min = min(auto_min, PE_min)
    auto_max = max(auto_max, PE_max)

    cbar_ax, kw = cbar.make_axes(axes[0])
    cmap = plt.get_cmap("jet")

    for key_volt_lfr in dic_voltage_lfr:
        x, y = np.meshgrid(
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
        x, y = np.meshgrid(times[index_band], freq[index_band])
        auto_log = 10 * np.log10(auto[index_band])
        auto_log = np.transpose(auto_log)
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

    # prepare kwargs for each dataset/plot
    plot_kwargs = {
        "PE": {"norm": colors.LogNorm(), "vmin": PE_min, "vmax": PE_max},
        "PB": {"norm": colors.LogNorm(), "vmin": PB_min, "vmax": PB_max},
        "DOP": {"vmin": 0, "vmax": 1},
        "ELLIP": {"vmin": 0, "vmax": 1},
        "SX_REA": {},
    }

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

    axes[0].set_xlim(left=times[0][0], right=times[0][np.size(times[0]) - 1])

    if "N_F2" in voltage:

        axes[1].set_ylim(bottom=10.5, auto=True, emit=False)
        axes[2].set_ylim(bottom=10.5)

    plt.suptitle(title, fontweight="bold", style="italic", color="grey")

    plt.savefig(savefigpath)
