from matplotlib import colors, pyplot as plt
import numpy as np
from maser.data import Data
from maser.data.rpw import tnr
import matplotlib.colorbar as cbar
from matplotlib.ticker import MaxNLocator

from matplotlib.colors import BoundaryNorm

from maser.data.rpw.filtre_for_tnr import pre_process

def quick_look_tnr_lfr_first_version (filepathtnr,filepathlfr):
    
    #fig, axess = plt.subplots( 7, 1, figsize=(9, 16))
    my_data_lfr=Data(filepath=filepathlfr)
    my_data_tnr=Data(filepath=filepathtnr)
    my_data_tnr._init_

    fig,axes=plt.subplots(7,1)

    datasets = my_data_lfr.as_xarray()

    # prepare kwargs for each dataset/plot
    plot_kwargs = {
        "PB": {"norm": colors.LogNorm()},
        "PE": {"norm": colors.LogNorm()},
        "DOP": {"vmin": 0, "vmax": 1},
        "ELLIP": {"vmin": 0, "vmax": 1},
        "SX_REA": {},
        }

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


    datasets = my_data_tnr.as_array(sensor=4)
    i=0
    auto_interpolation_log = 10 * np.log10(datasets["AUTO_INTERPOLATION"])
    _times_=datasets["times"]
        #while self.TNR_CURRENT_BAND_WORKING_ON[i]!=0:
            #auto_interpolation_log=auto_interpolation_log[1:]
            #_times_=_times_[1:]
            #i=i+1
            #print(i)
    x, y = np.meshgrid(_times_, my_data_tnr._frequencies_/ 1000) # je sais pas pq ça ne fonctionne pas bien avec self._frequencies_ (ordonné)
        #auto_interpolation_log = 10 * np.log10(datasets["AUTO_INTERPOLATION"])
    levels = MaxNLocator(nbins=250).tick_values(
            auto_interpolation_log.min(), auto_interpolation_log.max()
        )
    cmap = plt.get_cmap("jet")
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    #fig, ax0 = plt.subplots(nrows=1)
    auto_interpolation_log = np.transpose(auto_interpolation_log)
    im = axes[5].pcolormesh(x, y, auto_interpolation_log, cmap=cmap, norm=norm)
    fig.colorbar(im, ax=axes[5])
    axes[5].set_yscale("log")
    axes[5].set_xlabel("Temps")
    axes[5].set_ylabel("frequences")



    _times=my_data_tnr.as_array(sensor=4)["times"]
    FOI=my_data_tnr._frequencies_
    x,y=np.meshgrid(_times,FOI)
    auto_int=my_data_tnr.as_array(sensor=4)["AUTO_INTERPOLATION"]
    auto_int=np.transpose(auto_int)
    auto_int_log,auto_int_log_filtered=pre_process(auto_int)
    levels=MaxNLocator(nbins=250).tick_values(auto_int_log_filtered.min(),auto_int_log_filtered.max())
    cmap = plt.get_cmap("jet")
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    cbar_ax, kw = cbar.make_axes(axes[6])
    cbar_ax.set_ylabel("V^2/Hz")
    im = axes[6].pcolormesh(x, y, auto_int_log_filtered, cmap=cmap, norm=norm)
    fig.colorbar(im, ax=axes[6])
    axes[6].set_yscale("log")
    axes[6].set_xlabel("Temps")
    axes[6].set_ylabel("frequences")
        
    plt.show()
    


quick_look_tnr_lfr_first_version('/home/atokgozoglu/Documents/Maser/maser-data/maser/data/rpw/solo_L2_rpw-tnr-surv_20210701_V01.cdf',
                    '/home/atokgozoglu/Documents/Maser/maser-data/maser/data/rpw/solo_L2_rpw-lfr-surv-bp1_20201227_V02.cdf')