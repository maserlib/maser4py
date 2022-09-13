# -*- coding: utf-8 -*-
# %% [markdown]
# Import maser and matplotlib packages

# %%
from maser.data import Data
from maser.plot.rpw.lfr import plot_lfr_bp1_data
from pathlib import Path
import datetime


# %% [markdown]
# Define a function to load and plot the LFR BP1 dataset


# %%
def plot(filepath: Path):
    lfr_data = Data(filepath=filepath)
    plot_lfr_bp1_data(lfr_data)


# %% [markdown]
# And finally download and plot the data

# %%
if __name__ == "__main__":
    # use the jupyter interface to upload a file
    # or use the 'download_file' helper function
    from download import download_file, RPW_PUB_DATA_BASE_URL

    date = datetime.datetime(2022, 1, 18)

    file_url = date.strftime("/L2/lfr_bp/%Y/%m/solo_L2_rpw-lfr-surv-bp1_%Y%m%d_V02.cdf")

    # download the file and get the filepath
    local_filepath = download_file(RPW_PUB_DATA_BASE_URL + file_url)

    # plot the data
    plot(local_filepath)
