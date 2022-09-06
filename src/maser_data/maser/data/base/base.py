# -*- coding: utf-8 -*-
from typing import Union, Dict, Type, cast, Optional

from pathlib import Path
import re
from astropy.io import fits
import numpy
from .sweeps import Sweeps
from .records import Records

from astropy.time import Time
from astropy.units import Quantity


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

    Objects of this class are instanciated from a data file. An internal resolver will detect the
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
    def times(self) -> Optional[Time]:
        """Generic method to get the time axis."""
        return None

    @property
    def frequencies(self) -> Union[Quantity, Dict, None]:
        """Generic method to get the spectral axis."""
        return None

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
    def file_size(self):
        import os

        return os.path.getsize(self.filepath)

    def __iter__(self):
        # get the reference to the right iterator (file, sweeps or records)
        ref = getattr(self, self.access_mode)
        print(ref)
        for item in ref:
            yield item

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
        return dataset


class FitsData(Data, dataset="fits"):
    """Base class for FITS formatted data. FITS formatted NenuFAR data requires `nenupy`."""

    @classmethod
    def open(cls, filepath: Path, *args, **kwargs):
        """Open method for FITS formatted data products"""
        return fits.open(filepath, *args, **kwargs)

    @classmethod
    def get_dataset(cls, filepath):
        """Dataset selector for FITS files"""
        with cls.open(filepath) as f:
            if f[0].header["INSTRUME"] == "NenuFar" and filepath.stem.endswith("_BST"):
                dataset = "srn_nenufar_bst"
            elif "e-CALLISTO" in f[0].header["CONTENT"]:
                dataset = "ecallisto"
        return dataset


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
