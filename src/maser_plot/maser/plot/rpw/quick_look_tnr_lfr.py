# -*- coding: utf-8 -*-
import datetime
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

# from maser import data
from maser.data import Data
import matplotlib.colorbar as cbar

import matplotlib.dates as mdates


def quick_look_tnr_lfr(lfr_filepath, tnr_filepath):
    import seaborn

    lfr_data = Data(filepath=lfr_filepath)
    tnr_data = Data(filepath=tnr_filepath)

    fields = ["PB", "PE", "DOP", "ELLIP", "SX_REA"]

    nb_plot = len(fields)

    fig, axes = plt.subplots(
        len(fields), 1, sharex=True, sharey=True, figsize=(9, 2 * nb_plot)
    )

    axes_dict = {}
    for key, ax in zip(fields, axes):
        axes_dict[key] = {"ax": ax}
        cbar_ax, kw = cbar.make_axes(ax)
        axes_dict[key]["cbar_ax"] = cbar_ax

    # prepare kwargs for each dataset/plot
    plot_kwargs = {
        "PE": {"norm": "log", "cmap": "plasma"},
        "PB": {"norm": "log", "cmap": "plasma"},
        "DOP": {"vmin": 0, "vmax": 1, "cmap": "Greens"},
        "ELLIP": {"vmin": 0, "vmax": 1, "cmap": "Blues"},
        "SX_REA": {"cmap": "plasma"},
    }

    # plot LFR and TNR data using pcolormesh
    pcolormesh_tnr_lfr(fig, axes_dict, lfr_data, tnr_data, plot_kwargs=plot_kwargs)

    # then adjust the figure ...

    # get the middle of the LFR time range
    current_date = lfr_data.file["Epoch"][len(lfr_data.file["Epoch"]) // 2].replace(
        hour=0, minute=0, second=0
    )

    xmin = current_date - datetime.timedelta(minutes=10)
    xmax = current_date + datetime.timedelta(hours=24, minutes=10)

    # set the time axis format/limits
    formatter = mdates.DateFormatter("%H:%M")
    axes[-1].xaxis.set_major_formatter(formatter)
    axes[-1].set_xlim(left=xmin, right=xmax)
    axes[-1].set_xlabel("time (UTC)")

    for ax in axes[:-1]:
        # remove the x-axis labels for all but the last axis
        ax.set_xlabel("")

        # remover ax titles
        ax.set_title("")
    axes[-1].set_title("")

    # fix PE labels
    axes_dict["PE"]["cbar_ax"].set_ylabel("PE [$V^2/Hz$]")
    axes_dict["PE"]["ax"].set_ylabel("frequency [Hz]")

    # set the y-axis limits/ticks
    ymin = lfr_data.file["N_F2"][:].min()
    ymax = tnr_data.file["FREQUENCY"][:].max()

    axes_dict["PE"]["ax"].set_ylim(bottom=ymin, top=ymax)
    axes_dict["PE"]["ax"].yaxis.set_minor_locator(ticker.FixedLocator([1e2, 1e4, 1e5]))

    # set formatter for y-axis
    axes_dict["PE"]["ax"].yaxis.set_major_formatter(
        ticker.LogFormatterSciNotation(labelOnlyBase=False)
    )

    # remove minor labels
    axes_dict["PE"]["ax"].yaxis.set_minor_formatter(ticker.NullFormatter())

    # set major ticks for y-axis
    axes_dict["PE"]["ax"].set_yticks([10, 1e3, 1e6])

    # set the plot title
    title = (
        f"{current_date.strftime('%Y-%m-%d')} | Quick look of combined TNR and LFR data"
    )

    fig.suptitle(title, y=0.92)

    for ax in axes:
        # Remove the top and right spines from plots and offset/trim axes
        seaborn.despine(ax=ax, offset=10, trim=True)
        ax.tick_params(
            axis="x", direction="inout", length=plt.rcParams["xtick.major.size"] * 2
        )


def pcolormesh_tnr_lfr(
    fig, axes, lfr_data, tnr_data, *, max_gap_in_sec=60, plot_kwargs={}
):

    for field in axes:
        lfr_plot = lfr_data.plot_lfr_bp1_field(
            **axes[field],
            field=field,
            max_gap_in_sec=max_gap_in_sec,
            **plot_kwargs.get(field, {}),
        )
        lfr_vmin, lfr_vmax = lfr_plot["vmin"], lfr_plot["vmax"]

        if field == "PE":
            # plot auto from TNR
            tnr_plot = tnr_data.plot_auto(**axes[field], **plot_kwargs.get(field, {}))
            tnr_vmin, tnr_vmax = tnr_plot["vmin"], tnr_plot["vmax"]

            # adjust the vmin and vmax
            vmin = min(tnr_vmin, lfr_vmin)
            vmax = max(tnr_vmax, lfr_vmax)

            # update amplitude limits on each sub-mesh for both LFR and TNR
            for mesh in lfr_plot["meshes"]:
                mesh.set_clim(vmin, vmax)

            for mesh in tnr_plot["meshes"]:
                mesh.set_clim(vmin, vmax)

    return fig, axes


if __name__ == "__main__":
    from pathlib import Path

    data_path = Path(__file__).parents[5] / "tests" / "data" / "solo" / "rpw"

    date = "20211127"
    # date = '20220118'

    tnr_file = f"solo_L2_rpw-tnr-surv_{date}_V02.cdf"
    lfr_file = f"solo_L2_rpw-lfr-surv-bp1_{date}_V02.cdf"

    quick_look_tnr_lfr(
        lfr_filepath=data_path / lfr_file, tnr_filepath=data_path / tnr_file
    )

    plt.show()
