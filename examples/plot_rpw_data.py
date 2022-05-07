# -*- coding: utf-8 -*-
from tests.constants import BASEDIR
from matplotlib import pyplot as plt
from matplotlib import colors
from astropy.visualization import quantity_support, time_support
from astropy.time import Time
import xarray
import matplotlib.colorbar as cbar
import fsspec

demo_filepath = BASEDIR / "rpw" / "solo_L2_rpw-lfr-surv-bp1_20201227_V02.cdf"
from maser.data import Data


of = fsspec.open("github://dask:fastparquet@main/test-data/nation.csv", "rt")
# of is an OpenFile container object. The "with" context below actually opens it
with of as f:
    # now f is a text-mode file
    for line in f:
        # iterate text lines
        print(line)

with Data(filepath=demo_filepath) as data:
    datasets_attrs = {
        "PB": { "default_units": "nT^2/Hz", 'plot_kwargs': {"norm": colors.LogNorm()}},
        "PE": {"default_units": "", 'plot_kwargs': {"norm": colors.LogNorm()}},
        "DOP": {"default_units": "",  'plot_kwargs': {'vmin': 0, 'vmax': 1}},
        "ELLIP": {"default_units": "",  'plot_kwargs': {'vmin': 0, 'vmax': 1}},
        "SX_REA": {"default_units": ""},
    }
    for frequency_key in data.frequency_keys:
        frequencies = data.file[frequency_key][...]
        if len(frequencies) == 0:
            continue
        times = data.file[f"Epoch_{frequency_key}"][...]

        # force lower keys for frequency and time attributes
        time_attrs = {
            k.lower(): v for k, v in data.file[f"Epoch_{frequency_key}"].attrs.items()
        }

        frequency_attrs = {
            k.lower(): v for k, v in data.file[frequency_key].attrs.items()
        }
        if not frequency_attrs["units"].strip():
            frequency_attrs["units"] = "Hz"

        dataset = {
                "time": {"dims": ("time"), "data": times, 'attrs': time_attrs},
                "frequency": {"dims": ("frequency"), "data": frequencies, 'attrs': frequency_attrs},
        }


        for dataset_key in datasets_attrs:
            values = data.file[f"{dataset_key}_{frequency_key}"][...]

            # force lower keys for datasets attributes
            attrs = {
                k.lower(): v.strip()
                for k, v in data.file[f"{dataset_key}_{frequency_key}"].attrs.items()
            }

            # merge datasets attributes
            attrs = {**attrs, **datasets_attrs[dataset_key]}

  
            dataset[dataset_key] = { 'dims': ("time", "frequency"), 'data': values, 'attrs': attrs}

        dataset = xarray.Dataset.from_dict(dataset)

    nb_datasets = len(datasets)
    fig, axes = plt.subplots(len(datasets), 1, sharex=True)
    for ax_idx, dataset_key in enumerate(datasets):
        ax = axes[ax_idx]

        vmin = datasets[dataset_key].get('vmin', None)
        if vmin is None:
            for data_array in datasets[dataset_key]["data"].values():
                vmin = min(vmin, data_array.min()) if vmin is not None else data_array.min()
            datasets[dataset_key]['vmin'] = vmin

        vmax = datasets[dataset_key].get('vmax', None)
        if vmax is None:
            for data_array in datasets[dataset_key]["data"].values():
                vmax = max(vmax, data_array.max()) if vmax is not None else data_array.max()
            datasets[dataset_key]['vmax'] = vmax

        cbar_ax, kw = cbar.make_axes(ax)
        for data_array in datasets[dataset_key]["data"].values():
            data_array.plot.pcolormesh(
                ax=ax,
                yscale="log",
                add_colorbar=True,
                vmin=datasets[dataset_key]['vmin'],
                vmax=datasets[dataset_key]['vmax'],
                norm=datasets[dataset_key].get("normalization", None),
                cbar_ax=cbar_ax
            )
        if data_array.attrs["units"]: 
            cbar_label = f'{dataset_key} [${data_array.attrs["units"]}$]'
        else:
            cbar_label = dataset_key
        cbar_ax.set_ylabel(cbar_label)
    plt.show()