# -*- coding: utf-8 -*-
from typing import Union, Dict, Type, cast

from pathlib import Path
import re
import math
from astropy.io import fits
import numpy
from .sweeps import Sweeps
from .records import Records

from astropy.time import Time
from astropy.units import Quantity, Unit


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
    def times(self) -> Time:
        """Generic method to get the time axis."""
        pass

    @property
    def frequencies(self) -> Union[Quantity, Dict]:
        """Generic method to get the spectral axis."""
        pass

    def as_array(self) -> numpy.ndarray:
        """Generic method to get the data as a numpy.array."""
        pass

    def as_xarray(self) -> dict:
        """Generic method to get the data as a dict with xarray.DataArray values"""
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
        **kwargs,
    ):
        from matplotlib import pyplot as plt
        import matplotlib.dates as mdates

        hhmm_format = mdates.DateFormatter("%H:%M")

        xr = self.as_xarray()
        if keys is None:
            raise ValueError()
        fig, axs = plt.subplots(
            nrows=len(keys),
            sharex=True,
            sharey=True,
            figsize=(8.27, 11.69),  # A4 portrait
            dpi=100,
        )
        for i, k in enumerate(keys):
            xr_k = xr[k]
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
                vmin_i = None
            if isinstance(vmax, list):
                vmax_i = vmax[i]
            else:
                vmax_i = None
            xr_k.plot(
                ax=axs[i],
                cmap="gray",
                vmin=vmin_i,
                vmax=vmax_i,
                cbar_kwargs={"label": clabel},
                **kwargs,
            )
            axs[i].get_xaxis().set_visible(False)
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
            if dataset == "wi_wav_rad1_l3_df":
                dataset = f"{dataset}_v{c.attrs['Skeleton_version']}"

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
            if f"VESPA_{_range_unit}_unit" in self.file.attrs.keys():
                u = Unit(self.file.attrs[f"VESPA_{_range_unit}_unit"][0])
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
