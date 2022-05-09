# -*- coding: utf-8 -*-
from tests.constants import BASEDIR
from matplotlib import pyplot as plt
from matplotlib import colors
from astropy.visualization import quantity_support, time_support
from astropy.time import Time
import xarray
import matplotlib.colorbar as cbar

demo_filepath = BASEDIR / "rpw" / "solo_L2_rpw-lfr-surv-bp1_20201227_V02.cdf"
from maser.data import Data

with Data(filepath=demo_filepath) as data:
    datasets = {
        "PB": {"default_units": "nT^2/Hz", 'plot_kwargs': {"norm": colors.LogNorm()}},
        "PE": {"default_units": "", 'plot_kwargs': {"norm": colors.LogNorm()}},
        "DOP": {"default_units": "", 'plot_kwargs': {'vmin': 0, 'vmax': 1}},
        "ELLIP": {"default_units": "", 'plot_kwargs': {'vmin': 0, 'vmax': 1}},
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

        for dataset_key in datasets:
            values = data.file[f"{dataset_key}_{frequency_key}"][...]
            attrs = {
                k.lower(): v
                for k, v in data.file[f"{dataset_key}_{frequency_key}"].attrs.items()
            }

            # if units are not defined, use the default ones
            if not attrs["units"].strip():
                attrs["units"] = datasets[dataset_key]["default_units"]

            if "data" not in datasets[dataset_key]:
                datasets[dataset_key]["data"] = {}

            datasets[dataset_key]["data"][frequency_key] = xarray.DataArray(
                values.T,
                coords=[
                    ("frequency", frequencies, frequency_attrs),
                    ("time", times, time_attrs),
                ],
                attrs=attrs,
                name=f"{dataset_key}_{frequency_key}",
            )


    fig, axes = plt.subplots(len(datasets), 1, sharex=True)
    for ax_idx, dataset_key in enumerate(datasets):
        ax = axes[ax_idx]
        cbar_ax, kw = cbar.make_axes(ax)

        vmin = datasets[dataset_key].setdefault('plot_kwargs', {}).get('vmin', None)
        if vmin is None:
            for data_array in datasets[dataset_key]["data"].values():
                vmin = min(vmin, data_array.min()) if vmin is not None else data_array.min()
            datasets[dataset_key]['plot_kwargs']['vmin'] = vmin

        vmax = datasets[dataset_key].setdefault('plot_kwargs', {}).get('vmax', None)
        if vmax is None:
            for data_array in datasets[dataset_key]["data"].values():
                vmax = max(vmax, data_array.max()) if vmax is not None else data_array.max()
            datasets[dataset_key]['plot_kwargs']['vmax'] = vmax

        for data_array in datasets[dataset_key]["data"].values():
            data_array.plot.pcolormesh(
                ax=ax,
                yscale="log",
                add_colorbar=True,
                **datasets[dataset_key].get("plot_kwargs", {}),
                cbar_ax=cbar_ax
            )
        if data_array.attrs["units"]: 
            cbar_label = f'{dataset_key} [${data_array.attrs["units"]}$]'
        else:
            cbar_label = dataset_key
        cbar_ax.set_ylabel(cbar_label)
    plt.show()