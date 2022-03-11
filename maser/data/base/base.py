# -*- coding: utf-8 -*-
from typing import Union, Dict
from pathlib import Path
from spacepy import pycdf
from astropy.io import fits
import numpy
from .sweeps import Sweeps
from .records import Records


class BaseData:
    dataset: Union[None, str] = None
    _registry: Dict[str, "BaseData"] = {}
    _access_modes = ["sweeps", "records", "file"]
    _iter_sweep_class = Sweeps
    _iter_record_class = Records

    def __init_subclass__(cls: "BaseData", *args, dataset: str, **kwargs) -> None:
        cls.dataset = dataset
        BaseData._registry[dataset] = cls

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
        load_data: bool = True,
    ) -> None:
        self.filepath = Path(filepath)
        if access_mode not in self._access_modes:
            raise ValueError("Illegal access mode.")
        else:
            self.access_mode = access_mode
        self._file = None
        self._times = None
        self._frequencies = None
        self._load_data = load_data

    @classmethod
    def get_dataset(cls, filepath):
        pass


class Data(BaseData, dataset="default"):
    def __new__(
        cls, filepath: Path, dataset: Union[None, str] = "__auto__", *args, **kwargs
    ) -> "Data":
        if dataset is None:
            # call the base data class __new__ method
            return super().__new__(cls)
        elif dataset == "__auto__":
            # try to guess the dataset
            dataset = cls.get_dataset(filepath)

            # get the dataset class from the registry
            dataset_class = BaseData._registry[dataset]

            # create a new instance of the dataset class
            return dataset_class(filepath, dataset=None, *args, **kwargs)
        else:
            # get the dataset class from the registry
            dataset_class = BaseData._registry[dataset]

            # create a new instance of the dataset class
            return dataset_class(filepath, dataset=None, *args, **kwargs)

    @classmethod
    def open(cls, filepath: Path, *args, **kwargs):
        return open(filepath, *args, **kwargs)

    @classmethod
    def close(cls, file):
        file.close()

    @property
    def file(self):
        if not self._file:
            self._file = self.open(self.filepath)
        return self._file

    @property
    def sweeps(self):
        for sweep in self._iter_sweep_class(file=self.file, load_data=self._load_data):
            yield sweep

    @property
    def records(self):
        for record in self._iter_record_class(
            file=self.file, load_data=self._load_data
        ):
            yield record

    @property
    def meta(self) -> dict:
        return dict()

    @property
    def times(self):
        return None

    @property
    def frequencies(self):
        return None

    def as_array(self) -> numpy.ndarray:
        return numpy.ndarray(numpy.empty)

    def __enter__(self):
        if self.access_mode == "file":
            return self.file
        else:
            return self

    def __exit__(self, *args, **kwargs):
        if self._file:
            self.close(self._file)

    def __iter__(self):
        # get the reference to the right iterator (file, sweeps or records)
        ref = getattr(self, self.access_mode)
        print(ref)
        for item in ref:
            yield item

    @staticmethod
    def get_dataset(filepath: Path):
        if filepath.suffix.lower() == ".cdf":
            dataset = BaseData._registry["cdf"].get_dataset(filepath)
        elif filepath.suffix.lower() in [".fits", ".fit"]:
            dataset = BaseData._registry["fits"].get_dataset(filepath)
        elif filepath.suffix.lower() == ".lbl":
            dataset = BaseData._registry["pds3"].get_dataset(filepath)
        elif filepath.suffix.lower() in [".dat", ".b3e", ""]:
            dataset = BaseData._registry["bin"].get_dataset(filepath)
        else:
            raise NotImplementedError()
        return dataset


class CdfData(Data, dataset="cdf"):
    @classmethod
    def open(cls, filepath: Path):
        return pycdf.CDF(str(filepath))

    @classmethod
    def get_dataset(cls, filepath):
        with cls.open(filepath) as c:
            dataset = c.attrs["Logical_source"][...][0]
        return dataset


class FitsData(Data, dataset="fits"):
    @classmethod
    def open(cls, filepath: Path):
        return fits.open(filepath)

    @classmethod
    def get_dataset(cls, filepath):
        with cls.open(filepath) as f:
            if f[0].header["INSTRUME"] == "NenuFar" and filepath.stem.endswith("_BST"):
                dataset = "nenufar_bst"
            elif "e-CALLISTO" in f[0].header["CONTENT"]:
                dataset = "ecallisto"
        return dataset


class BinData(Data, dataset="bin"):
    @classmethod
    def open(cls, filepath: Path):
        return open(filepath, "rb")

    @classmethod
    def get_dataset(cls, filepath: Path):
        if filepath.stem.lower().startswith("wi_wa_rad1_l2_60s"):
            dataset = "wi_wa_rad1_l2_60s_v2"
        elif filepath.stem.lower().startswith("wi_wa_rad1_l2"):
            dataset = "wi_wa_rad1_l2"
        elif filepath.stem.lower().startswith("wi_wa_rad2_l2_60s"):
            dataset = "wi_wa_rad2_l2_60s_v2"
        elif filepath.stem.lower().startswith("wi_wa_tnr_l2_60s"):
            dataset = "wi_wa_tnr_l2_60s_v2"
        elif filepath.stem.lower().startswith("wi_wa_tnr_l3_bqt"):
            dataset = "wi_wa_tnr_l3_bqt_1mn"
        elif filepath.stem.lower().startswith("wi_wa_tnr_l3_nn"):
            dataset = "wi_wa_tnr_l3_nn"
        elif filepath.stem.lower().startswith("win_rad1_60s"):
            dataset = "wi_wa_rad1_l2_60s_v1"
        elif filepath.stem.lower().startswith("win_rad2_60s"):
            dataset = "wi_wa_rad2_l2_60s_v1"
        elif filepath.stem.lower().startswith("win_tnr_60s"):
            dataset = "wi_wa_tnr_l2_60s_v1"
        elif filepath.stem.lower().startswith("v4n_"):
            dataset = "viking_v4n_e5"
        else:
            raise NotImplementedError()
        return dataset
