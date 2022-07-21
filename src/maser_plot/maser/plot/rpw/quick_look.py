# -*- coding: utf-8 -*-
import datetime
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

from maser.data import Data
import matplotlib.colorbar as cbar
import matplotlib

import matplotlib.dates as mdates
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


@matplotlib.rc_context({"axes.spines.right": False, "axes.spines.top": False})
def quick_look(
    lfr_filepath: Path,
    tnr_filepath: Path,
    *,
    fields: list = ["PB", "PE", "DOP", "ELLIP", "SX_REA"],
    bands: list = ["A", "B", "C", "D"],
):

    if len(fields) < 1:
        raise ValueError("No fields to plot")

    lfr_data = Data(filepath=lfr_filepath)
    tnr_data = Data(filepath=tnr_filepath)

    nb_plot = len(fields)

    fig, axes = plt.subplots(
        nb_plot,
        1,
        sharex=True,
        sharey=True,
        figsize=(9, 2 * nb_plot),
        constrained_layout=True,
    )

    cbar_labels = {
        "PB": "PB [$nT^2/Hz$]",
        "PE": "PE [$V^2/Hz$]",
        "DOP": "DOP",
        "ELLIP": "ELLIP",
        "SX_REA": "SX_REA",
    }

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
    pcolormesh_tnr_lfr(
        fig, axes_dict, lfr_data, tnr_data, bands=bands, plot_kwargs=plot_kwargs
    )

    # then adjust the figure ...

    # get the middle of the LFR time range
    current_date = lfr_data.file["Epoch"][len(lfr_data.file["Epoch"]) // 2].replace(
        hour=0, minute=0, second=0
    )

    xmin = current_date - datetime.timedelta(minutes=1)
    xmax = current_date + datetime.timedelta(hours=24, minutes=1)

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

    if "PE" in fields:
        # fix PE labels issues due to TNR auto data overplotting
        axes_dict["PE"]["ax"].set_ylabel("frequency [Hz]")

    # set the y-axis limits/ticks
    ymin = 1e1
    ymax = 1e5

    axes[-1].set_ylim(bottom=ymin, top=ymax)
    axes[-1].yaxis.set_minor_locator(ticker.FixedLocator([1e2, 1e4]))

    # set formatter for y-axis
    axes[-1].yaxis.set_major_formatter(
        ticker.LogFormatterSciNotation(labelOnlyBase=False)
    )

    # remove minor labels
    axes[-1].yaxis.set_minor_formatter(ticker.NullFormatter())

    # set major ticks for y-axis
    axes[-1].set_yticks([1e1, 1e3, 1e5])

    # set the plot title
    title = (
        f"{current_date.strftime('%Y-%m-%d')} | Quick look of combined TNR and LFR data"
    )

    fig.suptitle(title)

    # Remove the top and right spines from plots and offset/trim axes
    for field in axes_dict:
        ax = axes_dict[field]["ax"]
        cbar_ax = axes_dict[field]["cbar_ax"]

        ax.tick_params(
            axis="x", direction="inout", length=plt.rcParams["xtick.major.size"] * 2
        )
        cbar_ax.set_ylabel(cbar_labels[field])

    return fig, axes


def pcolormesh_tnr_lfr(
    fig,
    axes,
    lfr_data,
    tnr_data,
    *,
    bands=["A", "B", "C", "D"],
    max_gap_in_sec=60,
    plot_kwargs={},
):
    from maser.plot.rpw.lfr import plot_lfr_bp1_field
    from maser.plot.rpw.tnr import plot_auto

    for field in axes:
        lfr_plot = plot_lfr_bp1_field(
            lfr_data,
            **axes[field],
            field=field,
            max_gap_in_sec=max_gap_in_sec,
            **plot_kwargs.get(field, {}),
        )
        lfr_vmin, lfr_vmax = lfr_plot["vmin"], lfr_plot["vmax"]

        if field == "PE":
            # plot auto from TNR
            tnr_plot = plot_auto(
                tnr_data, bands=bands, **axes[field], **plot_kwargs.get(field, {})
            )
            tnr_vmin, tnr_vmax = tnr_plot["vmin"], tnr_plot["vmax"]

            # adjust the vmin and vmax
            vmin = min(tnr_vmin, lfr_vmin)
            vmax = max(tnr_vmax, lfr_vmax)

            # update amplitude limits on each sub-mesh for both LFR and TNR
            for mesh in lfr_plot["meshes"]:
                mesh.set_clim(vmin, vmax)

            for mesh in tnr_plot["meshes"]:
                mesh.set_clim(vmin, vmax)

            axes[field]["cbar_ax"].clear()

        if len(lfr_plot["meshes"]) > 0:
            plt.colorbar(mappable=lfr_plot["meshes"][0], cax=axes[field]["cbar_ax"])

    return fig, axes


if __name__ == "__main__":
    from pathlib import Path

    data_path = Path(__file__).parents[5] / "tests" / "data" / "solo" / "rpw"

    # date = "20211127"
    date = "20220118"

    tnr_file = f"solo_L2_rpw-tnr-surv_{date}_V02.cdf"
    lfr_file = f"solo_L2_rpw-lfr-surv-bp1_{date}_V02.cdf"

    quick_look(
        lfr_filepath=data_path / lfr_file,
        tnr_filepath=data_path / tnr_file,
        fields=["PB", "PE", "DOP"],
        bands=["A", "B", "C", "D"],
    )

    plt.show()
