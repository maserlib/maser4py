# -*- coding: utf-8 -*-
from typing import Union, Dict, Type, cast

from pathlib import Path
from maser.data import Data
import re

# import math
from astropy.io import fits
import numpy

# from astropy.time import Time, TimeDelta
# from astropy.units import Quantity, Unit
# import xarray


class BasePlot:
    """Base class for all plots"""

    dataset: str
    _registry: Dict[str, Type["BasePlot"]] = {}

    def __init_subclass__(cls, *args, dataset: str, **kwargs) -> None:
        """Register subclasses to be able to instantiate them using only the dataset name

        Args:
            cls (BaseData): Subclass of BaseData
            dataset (str): Dataset name
        """
        # store the dataset name in the class
        cls.dataset = dataset

        # add the subclass to the BaseData registry
        BasePlot._registry[dataset] = cls

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
    ) -> None:

        # store the filepath as a Path object
        self.filepath = Path(filepath)

        # store the EPNcore metadata
        self._epncore: Union[Dict, None] = None

    @classmethod
    def get_dataset(cls, filepath):
        pass

    @property
    def Dfigures(self) -> list:
        """Generic method to return list of figures."""
        return []

    @property
    def Ddata(self) -> dict():
        """Generic method to return dict of data"""
        return dict()


class Plot(BasePlot, dataset="default"):
    def __new__(
        cls, filepath: Path, dataset: Union[None, str] = "__auto__", *args, **kwargs
    ) -> "Plot":
        if dataset is None:
            # call the base data class __new__ method
            return super().__new__(cls)
        elif dataset == "__auto__":
            # try to guess the dataset
            dataset = cls.get_dataset(cls, filepath)

            # get the dataset class from the registry
            # we need an explicit cast to make mypy happy
            dataset_class = BasePlot._registry[cast(str, dataset)]

            # create a new instance of the dataset class
            # ignore 'gets multiple values for keyword argument "dataset"'
            return dataset_class(filepath, dataset=None, *args, **kwargs)  # type: ignore
        else:
            # get the dataset class from the registry
            dataset_class = BasePlot._registry[cast(str, dataset)]

            # create a new instance of the dataset class
            # ignore 'gets multiple values for keyword argument "dataset"'
            return dataset_class(filepath, dataset=None, *args, **kwargs)  # type: ignore

    def _main_plot(
        self,
        keys: Union[None, list] = None,
        db: Union[None, list] = None,
        file_png: Union[None, Path, str] = None,
        vmin: Union[None, list] = None,
        vmax: Union[None, list] = None,
        vmin_quantile: Union[None, list] = None,
        vmax_quantile: Union[None, list] = None,
        iter_on_selection: Union[None, dict] = None,
        force_new_units: Union[None, dict] = None,
        data_factor: Union[None, dict] = None,
        force_new_keyname: Union[None, dict] = None,
        landscape: bool = False,
        **kwargs,
    ):
        from matplotlib import pyplot as plt
        import matplotlib
        import matplotlib.dates as mdates

        hhmm_format = mdates.DateFormatter("%H:%M")

        data = Data(self.filepath)

        # setting defaults
        if "nan_color" not in kwargs:
            nan_color = "black"
        else:
            nan_color = kwargs["nan_color"]
            del kwargs["nan_color"]

        # cmap management
        if "cmap" not in kwargs:
            kwargs["cmap"] = "gray"
        cmap_name = kwargs[
            "cmap"
        ]  # Necessary for iteration plots where using the same cmap object is an issue
        del kwargs["cmap"]  # Necessary to avoir giving two times cmap key

        xr = data.as_xarray()
        if keys is None:
            raise ValueError()
        if landscape:
            figsize = (11.69, 8.27)
        else:
            figsize = (8.27, 11.69)  # A4 portrait
        fig, axs = plt.subplots(
            nrows=len(keys),
            sharex=True,
            sharey=True,
            figsize=figsize,
            dpi=100,
        )
        for i, k in enumerate(keys):
            xr_k = xr[k]
            if isinstance(data_factor, list):
                xr_k *= data_factor[i]
            if isinstance(force_new_units, list):
                xr_k_unit_label = force_new_units[i]
            else:
                xr_k_unit_label = f"{xr_k.units}" if xr_k.units is not None else ""
            if isinstance(force_new_keyname, list):
                kname = force_new_keyname[i]
            else:
                kname = k
            if db is not None and db[i]:
                xr_k.values = 10.0 * numpy.log10(xr_k)
                clabel = (
                    f"{kname} [dB({xr_k_unit_label})]"
                    if xr_k_unit_label != ""
                    else f"{kname} [dB]"
                )
            else:
                clabel = (
                    f"{kname} [{xr_k_unit_label}]"
                    if xr_k_unit_label != ""
                    else f"{kname}"
                )
            if isinstance(vmin, list):
                vmin_i = vmin[i]
            else:
                if isinstance(vmin_quantile, list):
                    vmin_i = numpy.nanquantile(
                        xr_k.where(xr_k > -numpy.inf), vmin_quantile[i]
                    )
                else:
                    vmin_i = None
            if isinstance(vmax, list):
                vmax_i = vmax[i]
            else:
                if isinstance(vmax_quantile, list):
                    vmax_i = numpy.nanquantile(
                        xr_k.where(xr_k > -numpy.inf), vmax_quantile[i]
                    )
                else:
                    vmax_i = None
            if len(keys) == 1:
                axx = axs
            else:
                axx = axs[i]
            if iter_on_selection is None:
                # cmap = plt.cm.get_cmap(cmap_name).copy() # Deprecated
                cmap = matplotlib.colormaps[cmap_name]
                cmap.set_bad(nan_color, 1.0)
                xr_k.plot(
                    ax=axx,
                    cmap=cmap,  # cmap="gray", set by default in kwargs
                    vmin=vmin_i,
                    vmax=vmax_i,
                    cbar_kwargs={"label": clabel},
                    **kwargs,
                )
            else:
                first_loop = 1
                for selkey, selval, seldim, selhow in zip(
                    iter_on_selection["select_key"],
                    iter_on_selection["select_value"],
                    iter_on_selection["select_dim"],
                    iter_on_selection["select_how"],
                ):
                    # cmap = plt.cm.get_cmap(cmap_name).copy() # Deprecated
                    cmap = matplotlib.colormaps[cmap_name]
                    cmap.set_bad(nan_color, 1.0)
                    if first_loop == 1:
                        (
                            xr_k.where(xr[selkey] == selval).dropna(seldim, how=selhow)
                        ).plot(
                            ax=axx,
                            cmap=cmap,  # cmap="gray", set by default in kwargs
                            vmin=vmin_i,
                            vmax=vmax_i,
                            cbar_kwargs={"label": clabel},
                            **kwargs,
                        )
                        first_loop = 0
                    else:
                        # fig.delaxes(fig.axes[1])
                        (
                            xr_k.where(xr[selkey] == selval).dropna(seldim, how=selhow)
                        ).plot(
                            ax=axx,
                            cmap=cmap_name,  # cmap_name required here else it would replace the first iter by nan_color
                            vmin=vmin_i,
                            vmax=vmax_i,
                            # cbar_kwargs={"label": clabel},
                            add_colorbar=False,
                            **kwargs,
                        )
            axx.get_xaxis().set_visible(False)
        if len(keys) == 1:
            axs.set_title(f"{data.filepath.name} [{data.dataset}]")
            axs.get_xaxis().set_visible(True)
            axs.set_xlabel(f"time of day ({data.times[0].isot.split('T')[0]})")
            axs.xaxis.set_major_formatter(hhmm_format)
        else:
            axs[0].set_title(f"{data.filepath.name} [{data.dataset}]")
            axs[-1].get_xaxis().set_visible(True)
            axs[-1].set_xlabel(f"time of day ({data.times[0].isot.split('T')[0]})")
            axs[-1].xaxis.set_major_formatter(hhmm_format)
        plt.tight_layout()
        if file_png is None:
            plt.show()
        else:
            plt.savefig(file_png)
            plt.close(fig)

    def main_plot(self, file_png: Union[str, Path, None] = None):
        pass

    @staticmethod
    def get_dataset(cls, filepath):
        """Dataset selector method.

        This method identifies CdfData, FitsData and Pds3Data.
        Other datasets are treated as BinData.
        """
        filepath = Path(filepath)
        if filepath.suffix.lower() == ".cdf":
            dataset = BasePlot._registry["cdf"].get_dataset(filepath)
        elif filepath.suffix.lower() in [".fits", ".fit"]:
            dataset = BasePlot._registry["fits"].get_dataset(filepath)
        elif filepath.suffix.lower() == ".lbl":
            dataset = BasePlot._registry["pds3"].get_dataset(filepath)
        else:
            dataset = BasePlot._registry["bin"].get_dataset(filepath)
        return dataset


class CdfPlot(Plot, dataset="cdf"):
    """Base class for CDF formatted data. Requires `spacepy`."""

    @classmethod
    def open(cls, filepath: Path, *args, **kwargs):
        """Open method for CDF formatted data products"""
        from spacepy import pycdf

        return pycdf.CDF(str(filepath))

    @classmethod
    def get_dataset(cls, filepath):
        """Dataset selector for CDF files (must be ISTP compliant)"""
        with cls.open(filepath) as c:
            dataset = c.attrs["Logical_source"][...][0]

            # required dataset mapping
            if dataset == "srn_nda_routine_jup_edr":
                dataset = "orn_nda_routine_jup_edr"
            if dataset == "srn_nda_routine_sun_edr":
                dataset = "orn_nda_routine_sun_edr"
            if dataset == "wi_wav_rad1_l3_df":
                dataset = f"{dataset}_v{c.attrs['Skeleton_version']}"

        return dataset

    @property
    def mime_type(self) -> str:
        return "application/cdf"


class FitsPlot(Plot, dataset="fits"):
    """Base class for FITS formatted data."""

    @classmethod
    def open(cls, filepath: Path, *args, **kwargs):
        """Open method for FITS formatted data products"""
        return fits.open(filepath, *args, **kwargs)

    @classmethod
    def get_dataset(cls, filepath):
        """Dataset selector for FITS files"""
        with cls.open(filepath) as f:
            if f[0].header["INSTRUME"] == "NenuFar" and filepath.stem.endswith("_BST"):
                dataset = "orn_nenufar_bst"
            elif (
                f[0].header["INSTRUME"] == "newroutine"
                and f[0].header["TELESCOP"] == "NDA"
                and f[0].header["OBJECT"] == "Jupiter"
            ):
                dataset = "orn_nda_newroutine_jup_edr"
            elif (
                f[0].header["INSTRUME"] == "newroutine"
                and f[0].header["TELESCOP"] == "NDA"
                and f[0].header["OBJECT"] == "Sun"
            ):
                dataset = "orn_nda_newroutine_sun_edr"
            elif (
                f[0].header["INSTRUME"] == "mefisto"
                and f[0].header["TELESCOP"] == "NDA"
                and f[0].header["OBJECT"] == "Sun"
            ):
                dataset = "orn_nda_mefisto_sun_edr"
            elif "e-CALLISTO" in f[0].header["CONTENT"]:
                dataset = "ecallisto"
            else:
                raise NotImplementedError()
        return dataset

    @property
    def mime_type(self) -> str:
        return "application/fits"


class BinPlot(Plot, dataset="bin"):
    """Base class for custom binary data."""

    @classmethod
    def open(cls, filepath: Path, *args, mode: str = "rb", **kwargs):
        # ignore 'No overload variant of "open" ...'
        return filepath.open(*args, mode=mode, **kwargs)  # type: ignore

    @classmethod
    def get_dataset(cls, filepath):
        """Dataset selector for Binary files.

        If the dataset is not recognized, a NotImplementedError is raised.
        """
        filepath = Path(filepath)

        import json

        with open(Path(__file__).parent / "dataset_filename_regex.json") as f:
            filename_regex = json.load(f)

        for dataset, regex in filename_regex["bin"]:
            if re.match(regex, filepath.name) is not None:
                return dataset
        else:
            raise NotImplementedError()
