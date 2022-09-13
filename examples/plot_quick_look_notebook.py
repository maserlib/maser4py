# -*- coding: utf-8 -*-
# %% [markdown]
# Import maser and matplotlib packages

# %%
from maser.plot.rpw.quick_look import quick_look
import datetime
from typing import Dict


# %% [markdown]
# Define a function to load and plot the LFR and TNR datasets


# %%
def plot(filepaths: Dict):
    quick_look(
        lfr_filepath=filepaths["LFR"],
        tnr_filepath=filepaths["TNR"],
        fields=["PB", "PE", "DOP"],
        bands=["A", "B", "C", "D"],
    )


# %% [markdown]
# And finally download and plot the data

# %%
if __name__ == "__main__":
    # use the jupyter interface to upload a file
    # or use the 'download_file' helper function
    from download import download_file, RPW_PUB_DATA_BASE_URL

    date = datetime.datetime(2022, 1, 18)

    lfr_file_url = date.strftime(
        "/L2/lfr_bp/%Y/%m/solo_L2_rpw-lfr-surv-bp1_%Y%m%d_V02.cdf"
    )
    tnr_file_url = date.strftime("/L2/thr/%Y/%m/solo_L2_rpw-tnr-surv_%Y%m%d_V02.cdf")

    # download the file and get the filepath
    lfr_filepath = download_file(RPW_PUB_DATA_BASE_URL + lfr_file_url)
    tnr_filepath = download_file(RPW_PUB_DATA_BASE_URL + tnr_file_url)

    filepaths = {"TNR": tnr_filepath, "LFR": lfr_filepath}

    # plot the data
    plot(filepaths)
