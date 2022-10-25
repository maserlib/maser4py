# -*- coding: utf-8 -*-
from maser.data import Data


def plot_auto(
    data_wrapper: Data,
    ax,
    *,
    sensor: str = "V1-V2",
    bands: list = ["A", "B", "C", "D"],
    cbar_ax=None,
    **kwargs
):
    from matplotlib import colors
    import matplotlib.colorbar as cbar

    # create a colorbar axis
    if cbar_ax is None:
        cbar_ax, kw = cbar.make_axes(ax)

    auto = data_wrapper.as_xarray()["VOLTAGE_SPECTRAL_POWER"]

    # keep only V1-V2 sensor
    v1_v2_auto = auto.where(auto.sensor == sensor, drop=True)

    # determine min/max for the colorbar
    # use q5 and q95 for vmin and vmax to avoid outliers
    positive_v1_v2_auto = v1_v2_auto.where(v1_v2_auto > 0)
    vmin, vmax = positive_v1_v2_auto.quantile([0.05, 0.95])

    plot_kwargs = {
        "cmap": "plasma",
        "norm": "log",
        "vmin": vmin,
        "vmax": vmax,
        "cbar_ax": cbar_ax,
        **kwargs,
    }

    # create a new norm object to display the colorbar in log scale
    if "norm" in plot_kwargs and plot_kwargs["norm"] == "log":
        plot_kwargs["norm"] = colors.LogNorm()

    meshes = []

    # group data by band and plot each channel
    for band, data_array in v1_v2_auto.groupby("band"):
        if band not in bands:
            # skip bands not in the list
            continue

        for channel in data_wrapper.channel_labels:
            # create a new mesh for each band/channel
            mesh = data_array.sel(channel=channel).plot.pcolormesh(
                ax=ax,
                x="time",
                y="frequency",
                yscale="log",
                add_colorbar=True,
                **plot_kwargs,
            )

            # store the mesh for future use
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

    # tnr_file = "solo_L2_rpw-tnr-surv_20211127_V02.cdf"
    tnr_file = "solo_L2_rpw-tnr-surv_20220118_V02.cdf"
    tnr_filepath = data_path / tnr_file

    tnr_data = Data(filepath=tnr_filepath)
    fig, ax = plt.subplots()
    plot_auto(tnr_data, ax)
    plt.show()
