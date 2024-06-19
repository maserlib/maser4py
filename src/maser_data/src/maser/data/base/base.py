# -*- coding: utf-8 -*-
from typing import Union, Dict, Type, cast

from pathlib import Path
import re
import math
from astropy.io import fits
import numpy
from .sweeps import Sweeps
from .records import Records

from astropy.time import Time, TimeDelta
from astropy.units import Quantity, Unit
import xarray


class BaseData:
    """Base class for all data classes."""

    dataset: str
    _registry: Dict[str, Type["BaseData"]] = {}
    _access_modes = ["sweeps", "records", "file"]
    _iter_sweep_class = Sweeps
    _iter_record_class = Records

    def __init_subclass__(cls, *args, dataset: str, **kwargs) -> None:
        """Register subclasses to be able to instantiate them using only the dataset name

        Args:
            cls (BaseData): Subclass of BaseData
            dataset (str): Dataset name
        """
        # store the dataset name in the class
        cls.dataset = dataset

        # add the subclass to the BaseData registry
        BaseData._registry[dataset] = cls

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
        load_data: bool = True,
        fixed_frequencies: bool = True,
    ) -> None:

        # store the filepath as a Path object
        self.filepath = Path(filepath)

        # check if access_mode is valid
        if access_mode not in self._access_modes:
            raise ValueError("Illegal access mode.")
        else:
            self.access_mode = access_mode

        # a reference to the file object
        self._file = None

        # store the computed times/frequencies to avoid computing them again
        self._times = None
        self._delta_times = None
        self._frequencies = None

        # store the EPNcore metadata
        self._epncore: Union[Dict, None] = None

        # flag used to determine if are in lazy mode or not
        self._load_data = load_data

        self.fixed_frequencies = fixed_frequencies

    @property
    def load_data(self) -> bool:
        return self._load_data

    @classmethod
    def get_dataset(cls, filepath):
        pass


class Data(BaseData, dataset="default"):
    """Generic Data class
    =====================

    Objects of this class are instantiated from a data file. An internal resolver will detect the
    dataset and provide adequate support. If the file is not recognized, an NotImplementedError is
    raised.

    """

    def __new__(
        cls, filepath: Path, dataset: Union[None, str] = "__auto__", *args, **kwargs
    ) -> "Data":
        if dataset is None:
            # call the base data class __new__ method
            return super().__new__(cls)
        elif dataset == "__auto__":
            # try to guess the dataset
            dataset = cls.get_dataset(cls, filepath)

            # get the dataset class from the registry
            # we need an explicit cast to make mypy happy
            dataset_class = BaseData._registry[cast(str, dataset)]

            # create a new instance of the dataset class
            # ignore 'gets multiple values for keyword argument "dataset"'
            return dataset_class(filepath, dataset=None, *args, **kwargs)  # type: ignore
        else:
            # get the dataset class from the registry
            dataset_class = BaseData._registry[cast(str, dataset)]

            # create a new instance of the dataset class
            # ignore 'gets multiple values for keyword argument "dataset"'
            return dataset_class(filepath, dataset=None, *args, **kwargs)  # type: ignore

    @classmethod
    def open(cls, filepath: Path, *args, **kwargs):
        """Generic open() method."""
        return open(filepath, *args, **kwargs)

    @classmethod
    def close(cls, file):
        """Generic close() method."""
        file.close()

    @property
    def file(self):
        """Generic open method (using the default open class)."""
        if not self._file:
            self._file = self.open(self.filepath)
        return self._file

    @property
    def sweeps(self):
        """Generic iterator method to access sweeps."""
        for sweep in self._iter_sweep_class(data_instance=self):
            yield sweep

    @property
    def records(self):
        """Generic iterator method to access records."""
        for record in self._iter_record_class(data_instance=self):
            yield record

    @property
    def meta(self) -> dict:
        """Generic method to metadata."""
        return dict()

    @property
    def dataset_keys(self) -> list:
        """Generic method to get the keys for this dataset's quicklook."""
        pass

    @property
    def times(self) -> Time:
        """Generic method to get the time axis."""
        pass

    @property
    def delta_times(self) -> TimeDelta:
        """Generic method to get the difference to referential time."""
        pass

    @property
    def frequencies(self) -> Union[Quantity, Dict]:
        """Generic method to get the spectral axis."""
        pass

    def __len__(self) -> int:
        """Generic method to get the length of the data as a time series."""
        return len(self.times)

    def as_array(self) -> numpy.ndarray:
        """Generic method to get the data as a numpy.array."""
        pass

    def as_xarray(self) -> xarray.Dataset:
        """Generic method to get the data as a xarray.Dataset object (an efficient "dict", filled with xarray.DataArray)"""
        pass

    def __enter__(self):
        if self.access_mode == "file":
            return self.file
        else:
            return self

    def __exit__(self, *args, **kwargs):
        if self._file:
            self.close(self._file)

    @property
    def file_size(self) -> Quantity:
        import os

        return os.path.getsize(self.filepath) * Unit("byte")

    @property
    def mime_type(self) -> str:
        return "application/octet-stream"

    def __iter__(self):
        # get the reference to the right iterator (file, sweeps or records)
        ref = getattr(self, self.access_mode)
        print(ref)
        for item in ref:
            yield item

    def tfcat(self):
        """Method to get a TFCat feature for the file spectral-temporal coverage using the TFCat format.

        :return tfcat: a FeatureCollection object
        """
        pass

    def moc(self):
        """Method to get a MOC (T-MOC ot FT-MOC) object containing the spectral-temporal coverage.

        :return moc: an MOC string representation
        """
        pass

    def epncore(self) -> Dict:
        """
        Method to get EPNcore metadata from the MaserData object instance. This method is extended in classes inheriting
        from MaserData.

        :returns: a dict with time_min, time_max and granule_gid (from dataset_name attribute) keys.
        """

        if self._epncore is None:
            sampling_step = (self.times[1:] - self.times[:-1]).to("s").value
            self._epncore = {
                "time_min": self.times[0].jd.astype(float),
                "time_max": self.times[-1].jd.astype(float),
                "time_sampling_step_min": numpy.min(sampling_step),
                "time_sampling_step_max": numpy.max(sampling_step),
                "granule_gid": self.dataset,
                "granule_uid": f"{self.dataset}:{self.filepath.name}",
                "file_name": self.filepath.name,
                "access_format": self.mime_type,
                "access_estsize": math.ceil(self.file_size.to("KiB").value),
            }

        return self._epncore

    def _quicklook(
        self,
        keys: Union[None, list] = None,
        db: Union[None, list] = None,
        file_png: Union[None, Path, str] = None,
        vmin: Union[None, list] = None,
        vmax: Union[None, list] = None,
        vmin_quantile: Union[None, list] = None,
        vmax_quantile: Union[None, list] = None,
        iter_on_selection: Union[None, dict] = None,
        **kwargs,
    ):
        from matplotlib import pyplot as plt
        import matplotlib
        import matplotlib.dates as mdates
        import warnings

        hhmm_format = mdates.DateFormatter("%H:%M")

        params = {
            "db": db,
            "file_png": file_png,
            "vmin": vmin,
            "vmax": vmax,
            "vmin_quantile": vmin_quantile,
            "vmax_quantile": vmax_quantile,
            "iter_on_selection": iter_on_selection,
        }
        params_nn = {
            k: v for k, v in params.items() if v is not None
        }  # select not None parameters
        args_to_test = {**params_nn, **kwargs}  # combine kwargs and default keys
        self.check_input_param(keys, args_to_test)  # check that inputs are coherent

        # *** setting defaults ***
        # keys and landscape
        if keys is None:
            raise ValueError()
        else:
            if "landscape" not in kwargs:
                if len(keys) == 1:
                    landscape = True
                else:
                    landscape = False
            else:
                landscape = kwargs["landscape"]
                del kwargs["landscape"]

        # nan_color
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

        xr = self.as_xarray()
        if landscape:
            figsize = (11.69, 8.27)
        else:
            figsize = (8.27, 11.69)  # A4 portrait
        fig, axs = plt.subplots(
            nrows=len(keys),
            sharex=True,
            sharey=True,
            figsize=figsize,  # A4 portrait
            dpi=100,
        )
        for i, k in enumerate(keys):
            xr_k = xr[k]
            if xr_k.dims != ("frequency", "time"):
                if xr_k.dims != ("freq_index", "time"):  # Cassini
                    warnings.warn(
                        "WARNING: Dimensions for key: "
                        + str(k)
                        + " are not frequency - time. Quicklook should fail."
                    )
            xr_k_unit_label = f"{xr_k.units}" if xr_k.units is not None else ""
            if db is not None and db[i]:
                xr_k.values = 10.0 * numpy.log10(xr_k)
                clabel = (
                    f"{k} [dB({xr_k_unit_label})]"
                    if xr_k_unit_label != ""
                    else f"{k} [dB]"
                )
            else:
                clabel = f"{k} [{xr_k_unit_label}]" if xr_k_unit_label != "" else f"{k}"
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
                            cmap=cmap,  # _name,  # cmap="gray", set by default in kwargs
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
            axs.set_title(f"{self.filepath.name} [{self.dataset}]")
            axs.get_xaxis().set_visible(True)
            axs.set_xlabel(f"time of day ({self.times[0].isot.split('T')[0]})")
            axs.xaxis.set_major_formatter(hhmm_format)
        else:
            axs[0].set_title(f"{self.filepath.name} [{self.dataset}]")
            axs[-1].get_xaxis().set_visible(True)
            axs[-1].set_xlabel(f"time of day ({self.times[0].isot.split('T')[0]})")
            axs[-1].xaxis.set_major_formatter(hhmm_format)
        plt.tight_layout()
        if file_png is None:
            plt.show()
        else:
            plt.savefig(file_png)
            plt.close(fig)

    def quicklook(self, file_png: Union[str, Path, None] = None):
        """Generic method to display data.

        This method selects main keys for each data set and display corresponding data from the file.
        It is based on xarray.plot, which in turn uses pcolormesh.
        Keyword arguments:
        keys -- List of str -- gives which keys to be displayed. See or use Data.dataset_keys for list of usable keys.
        file_png -- Path/str -- will save the created plot on file_png if given (default None).
        Additionnal display keyword arguments:
        cmap -- str -- select the corresponding matplotlib colormap (default: "gray").
        nan_color -- str -- gives the color to be used to display nan (default: "black").
        db -- List of bool -- if True, display the data for this key in db (10*log10(data)).
        vmin_quantile -- List of float -- select for each key the lower limit of the colormap based on quantile.
        vmax_quantile -- List of float -- select for each key the upper limit of the colormap based on quantile.
        kwargs -- any kwargs of xarray.plot or pcolormesh can be given to this function.
        """
        pass

    @staticmethod
    def get_dataset(cls, filepath):
        """Dataset selector method.

        This method identifies CdfData, FitsData and Pds3Data.
        Other datasets are treated as BinData.
        """
        filepath = Path(filepath)
        if filepath.suffix.lower() == ".cdf":
            dataset = BaseData._registry["cdf"].get_dataset(filepath)
        elif filepath.suffix.lower() in [".fits", ".fit"]:
            dataset = BaseData._registry["fits"].get_dataset(filepath)
        elif filepath.suffix.lower() == ".lbl":
            dataset = BaseData._registry["pds3"].get_dataset(filepath)
        else:
            dataset = BaseData._registry["bin"].get_dataset(filepath)
        return dataset

    def check_input_param(self, keys, kwargs):
        """
        Method to test that all the inputs given to quicklook are consistent.
        Mainly, it consists in checking that "keys" are corrects and match the known
        dataset keys ; and that all the other keywords are compatible with these keys.
        """
        import matplotlib
        import warnings

        arg_list_list = [
            "vmin",
            "vmax",
            "vmin_quantile",
            "vmax_quantile",
            "db",
        ]

        for key in keys:
            if key is None:
                raise KeyError("Key must be specified and cannot be None.")
            if key not in self.dataset_keys:
                raise KeyError(
                    "Given key: "
                    + key
                    + " not in dataset keys. Use Data.dataset_keys for full list."
                )

        for arg in kwargs.keys():
            if kwargs[arg] is not None:
                if arg == "iter_on_selection":
                    if not type(kwargs["iter_on_selection"]) == dict:
                        raise KeyError("iter_on_selection must be a dictionnary.")
                    elif "nan_color" in kwargs:
                        warnings.warn(
                            "WARNING: nan_color and iter_on_selection may be incompatible. Result may look strange."
                        )
                elif arg == "cmap":
                    if kwargs["cmap"] not in matplotlib.colormaps:
                        raise KeyError(
                            "cmap: "
                            + kwargs["cmap"]
                            + " unknwon, must be a matplotlib cmap."
                        )
                elif arg == "nan_color":
                    if not matplotlib.colors.is_color_like(kwargs["nan_color"]):
                        raise KeyError("nan_color must be a matplotlib color.")
                elif arg == "file_png" in kwargs:
                    if (
                        type(kwargs["file_png"]) != str
                    ):  # if file_png was given as a str
                        if kwargs["file_png"] != Path(
                            kwargs["file_png"]
                        ):  # if file_png was given as a Path()
                            raise KeyError(
                                "file_png must be a Path (str or Path object)."
                            )
                elif arg == "landscape":
                    if type(kwargs[arg]) != bool:
                        raise KeyError("landscape must be a bool.")
                else:  # all the args that should have same dimension as keys
                    if arg in arg_list_list:  # Prevent checking matplotlib kwargs
                        if len(kwargs[arg]) != len(keys):
                            raise KeyError(
                                "Wrong list size for "
                                + arg
                                + ", should be the same size as keys (len: "
                                + str(len(keys))
                                + ")"
                            )


class CdfData(Data, dataset="cdf"):
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
            if dataset == "solo_l3_rpw-hfr":
                if "tnr" in str(filepath):
                    dataset = "solo_L3_rpw-tnr-flux_"
                else:
                    dataset = "solo_L3_rpw-hfr-flux_"

        return dataset

    @property
    def mime_type(self) -> str:
        return "application/cdf"

    def _convert_epncore_ranges(self, k, v, range_type):
        range_types = ["time_sampling_step", "spectral_range", "spectral_sampling_step"]
        range_units = {
            "time_sampling_step": "s",
            "spectral_range": "Hz",
            "spectral_sampling_step": "Hz",
        }
        md = {}

        if range_type in range_types:
            _range_min = f"{range_type}_min"
            _range_max = f"{range_type}_max"
            _range_unit = f"{range_type}_unit"
            _u = range_units[range_type]
            if f"VESPA_{_range_unit}" in self.file.attrs.keys():
                u = Unit(self.file.attrs[f"VESPA_{_range_unit}"][0])
            else:
                u = Unit(_u)
            _v = (float(v) * u).to(_u).value
            if k == range_type:
                md[_range_min] = _v
                md[_range_max] = md[_range_min]
            elif k in [_range_min, _range_max]:
                md[k] = _v
        else:
            raise ValueError()
        return md

    def epncore(self):
        if self._epncore is None:
            self._epncore = Data.epncore(self)

        for _k, _v in self.file.attrs.items():

            if _k.upper().startswith("VESPA"):
                k = _k.replace("VESPA_", "").lower()

                if k == "dataproduct_type":
                    self._epncore["dataproduct_type"] = "#".join(
                        [v.split(">")[0].lower() for v in _v]
                    )
                elif k in [
                    "instrument_name",
                    "instrument_host_name",
                    "target_class",
                    "target_name",
                    "target_region",
                    "feature_name",
                    "receiver_name",
                    "measurement_type",
                    "time_origin",
                    "bib_reference",
                    "time_scale",
                ]:
                    values = set()
                    for v in _v:
                        values.update(v.split(">"))
                    self._epncore[k] = "#".join(values)
                elif k.startswith("time_sampling_step") and not k.endswith("unit"):
                    self._epncore.update(
                        self._convert_epncore_ranges(k, _v[0], "time_sampling_step")
                    )
                elif k.startswith("spectral_range") and not k.endswith("unit"):
                    self._epncore.update(
                        self._convert_epncore_ranges(k, _v[0], "spectral_range")
                    )
                elif k.startswith("spectral_sampling_step") and not k.endswith("unit"):
                    self._epncore.update(
                        self._convert_epncore_ranges(k, _v[0], "spectral_sampling_step")
                    )
        return self._epncore


class FitsData(Data, dataset="fits"):
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


class BinData(Data, dataset="bin"):
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
