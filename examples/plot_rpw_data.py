# -*- coding: utf-8 -*-
from tests.constants import BASEDIR
from matplotlib import pyplot as plt
from matplotlib import colors
from astropy.visualization import quantity_support, time_support
from astropy.time import Time
import xarray

demo_filepath = BASEDIR / "rpw" / "solo_L2_rpw-lfr-surv-bp1_20201227_V02.cdf"
from maser.data import Data

with Data(filepath=demo_filepath) as data:
    datasets = {
        "PB": {"default_units": "nT^2/Hz", "normalization": colors.LogNorm()},
        "PE": {"default_units": "", "normalization": colors.LogNorm()},
        "DOP": {"default_units": "", 'vmin': 0, 'vmax': 1},
        "ELLIP": {"default_units": "", 'vmin': 0, 'vmax': 1},
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

        for dataset in datasets:
            values = data.file[f"{dataset}_{frequency_key}"][...]
            attrs = {
                k.lower(): v
                for k, v in data.file[f"{dataset}_{frequency_key}"].attrs.items()
            }

            # if units are not defined, use the default ones
            if not attrs["units"].strip():
                attrs["units"] = datasets[dataset]["default_units"]

            if "data" not in datasets[dataset]:
                datasets[dataset]["data"] = {}

            datasets[dataset]["data"][frequency_key] = xarray.DataArray(
                values.T,
                coords=[
                    ("frequency", frequencies, frequency_attrs),
                    ("time", times, time_attrs),
                ],
                attrs=attrs,
                name=f"{dataset}_{frequency_key}",
            )


    fig, axes = plt.subplots(len(datasets), 1, sharex=True)
    for ax_idx, dataset in enumerate(datasets):
        ax = axes[ax_idx]

        vmin = datasets[dataset].get('vmin', None)
        if vmin is None:
            for data_array in datasets[dataset]["data"].values():
                vmin = min(vmin, data_array.min()) if vmin is not None else data_array.min()
            datasets[dataset]['vmin'] = vmin

        vmax = datasets[dataset].get('vmax', None)
        if vmax is None:
            for data_array in datasets[dataset]["data"].values():
                vmax = max(vmax, data_array.max()) if vmax is not None else data_array.max()
            datasets[dataset]['vmax'] = vmax

        for data_array in datasets[dataset]["data"].values():
            data_array.plot.pcolormesh(
                ax=ax,
                yscale="log",
                add_colorbar=True,
                vmin=datasets[dataset]['vmin'],
                vmax=datasets[dataset]['vmax'],
                norm=datasets[dataset].get("normalization", None),
            )
    plt.show()
    # sweeps = list(data.sweeps)
    # print(sweeps[0:5])
    # with quantity_support():
    #     for values, time, frequencies in sweeps[0:5]:
    #         # plt.plot(sweep[2].to(Unit("Hz")), sweep[0])
    #         plt.pcolormesh(time, frequencies, values['DOP'], cmap='RdBu')
    #     plt.colorbar()
    #     plt.show()
