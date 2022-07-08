# -*- coding: utf-8 -*-
from tests.constants import BASEDIR
from matplotlib import pyplot as plt
from matplotlib import colors
import matplotlib.colorbar as cbar
from maser.data import Data


def plot_lfr_bp1_data(datasets: dict) -> tuple:
    """Plot the LFR BP1 data using xarray datasets and matplotlib

    Args:
        datasets (dict): _description_

    Returns:
        tuple: matplotlib figure and axes
    """

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
    return fig, axes


def plot(filepath=BASEDIR / "rpw" / "solo_L2_rpw-lfr-surv-bp1_20201227_V02.cdf"):

    with Data(filepath=filepath) as data:
        datasets = data.as_xarray()

    plot_lfr_bp1_data(datasets)


if __name__ == "__main__":
    plot()
