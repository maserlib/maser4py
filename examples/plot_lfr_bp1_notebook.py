# -*- coding: utf-8 -*-
# %% [markdown]
# Import maser and matplotlib packages

# %%
from matplotlib import pyplot as plt
from matplotlib import colors
import matplotlib.colorbar as cbar
from maser.data import Data


# %% [markdown]
# Create a function to plot each dataset of the LFR BP1 file

# %%


def plot_lfr_bp1_data(datasets: dict) -> tuple:
    """Plot the LFR BP1 data using xarray datasets and matplotlib

    Args:
        datasets (dict): a dict containing LFR BP1 data as xarray datasets

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
    fig, axes = plt.subplots(len(datasets), 1, sharex=True, figsize=(9, 16))

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


# %% [markdown]
# Define a function to load the data and plot the datasets

# %%
def plot(filepath):

    with Data(filepath=filepath) as data:
        datasets = data.as_xarray()

    plot_lfr_bp1_data(datasets)


# %%
# use the jupyter interface to upload a file or use the following code
def download_file(url, local_filename=None, force_download=False):
    import requests
    from pathlib import Path

    if local_filename is None:
        local_filename = url.split("/")[-1]

    # check if the file already exists
    if Path(local_filename).exists() and not force_download:
        return local_filename

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


# %% [markdown]
# And finally download and plot the data

# %%
if __name__ == "__main__":
    file_url = "https://rpw.lesia.obspm.fr/roc/data/pub/solo/rpw/data/L2/lfr_bp/2020/12/solo_L2_rpw-lfr-surv-bp1_20201207_V02.cdf"
    local_filename = download_file(file_url)
    plot(local_filename)
