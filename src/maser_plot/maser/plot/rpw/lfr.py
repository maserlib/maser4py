# -*- coding: utf-8 -*-
import matplotlib.colorbar as cbar
from matplotlib import colors
from matplotlib import pyplot as plt
from maser.data import Data


def plot_lfr_bp1_field(
    data_wrapper: Data,
    *,
    ax,
    cbar_ax=None,
    field: str,
    max_gap_in_sec: int = 60,
    **kwargs,
):
    """Plot a field of the LFR BP1 data using xarray datasets and matplotlib"""
    import numpy

    dataset = data_wrapper.as_xarray()

    # prepare kwargs for each dataset/plot
    default_kwargs = {
        "PB": {"norm": colors.LogNorm()},
        "PE": {"norm": colors.LogNorm()},
        "DOP": {"vmin": 0, "vmax": 1},
        "ELLIP": {"vmin": 0, "vmax": 1},
        "SX_REA": {},
    }

    merge_kwargs = {**default_kwargs[field], **kwargs}

    # create a new norm object to display the colorbar in log scale
    if "norm" in merge_kwargs and merge_kwargs["norm"] == "log":
        merge_kwargs["norm"] = colors.LogNorm()

    # create the associated colorbar
    if cbar_ax is None:
        cbar_ax, kw = cbar.make_axes(ax)

    # determine min/max for the colorbar by taking account of each dataset for each frequency range
    # use q5 and q95 for vmin and vmax to avoid outliers
    min_value = min([dataset[field][band].quantile(0.05) for band in dataset[field]])
    max_value = max([dataset[field][band].quantile(0.95) for band in dataset[field]])
    merge_kwargs.setdefault("vmin", min_value)
    merge_kwargs.setdefault("vmax", max_value)

    meshes = []

    # plot the data
    for band in dataset[field]:
        data_array = dataset[field][band]

        # handle data gaps by grouping data separated by more than `max_gap_in_sec`

        # use `cumsum` to index groups of values separated by a gap
        data_gaps_groups = (
            (
                data_array.coords["time"].diff(dim="time")
                > numpy.timedelta64(max_gap_in_sec, "s")
            )
            .cumsum(axis=0)
            .values
        )

        # and prepend a leading 0 to match the length of the dataset
        data_gaps_groups = numpy.concatenate([[0], data_gaps_groups])

        # add a new derived coordinate to the data array
        data_array = data_array.assign_coords(gaps=("time", data_gaps_groups))

        # and plot a new mesh for each group of data
        for gap, data in data_array.groupby("gaps"):

            # if there is only one value, skip this group
            if len(data.coords["time"]) < 2:
                continue

            mesh = data.plot.pcolormesh(
                ax=ax,
                x="time",
                y="frequency",
                yscale="log",
                # add_colorbar=True,
                **merge_kwargs,
                cbar_ax=None,
                add_colorbar=False,
            )

            meshes.append(mesh)

    # set the color bar title
    if data_array.attrs.get("units"):
        cbar_label = f'{field} [${data_array.attrs["units"]}$]'
    else:
        cbar_label = field
    cbar_ax.set_ylabel(cbar_label)

    return {
        "ax": ax,
        "cbar_ax": cbar_ax,
        "vmin": merge_kwargs["vmin"],
        "vmax": merge_kwargs["vmax"],
        "meshes": meshes,
    }


def plot_lfr_bp1_data(data_wrapper: Data, max_gap_in_sec: int = 60):
    """Plot the LFR BP1 data using xarray datasets and matplotlib

    Args:
        data_wrapper (Data): a MASER Data object
        max_gap_in_sec (int, optional): maximum gap in seconds between two consecutive data points. Used to group data and trigger a new mesh. Defaults to 60.

    Returns:
        tuple: matplotlib figure and axes
    """

    dataset = data_wrapper.as_xarray()

    # create figure and axes
    fig, axes = plt.subplots(len(dataset), 1, sharex=True)
    # loop over datasets
    for ax_idx, field in enumerate(dataset):

        # select the ax to plot on
        ax = axes[ax_idx]

        # create the associated colorbar
        cbar_ax, kw = cbar.make_axes(ax)

        plot_lfr_bp1_field(
            data_wrapper,
            ax=ax,
            cbar_ax=cbar_ax,
            field=field,
            max_gap_in_sec=max_gap_in_sec,
        )
    return fig, axes


if __name__ == "__main__":
    from maser.data import Data
    from pathlib import Path

    data_path = Path(__file__).parents[5] / "tests" / "data" / "solo" / "rpw"

    # lfr_file = "solo_L2_rpw-lfr-surv-bp1_20211127_V02.cdf"
    lfr_file = "solo_L2_rpw-lfr-surv-bp1_20220118_V02.cdf"
    lfr_filepath = data_path / lfr_file

    lfr_data = Data(filepath=lfr_filepath)
    plot_lfr_bp1_data(lfr_data)
    plt.show()
