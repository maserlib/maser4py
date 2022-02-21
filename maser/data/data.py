# -*- coding: utf-8 -*-
from typing import Union, Dict
from pathlib import Path
from spacepy import pycdf
from astropy.io import fits


class BaseData:
    dataset: Union[None, str] = None
    _registry: Dict[str, "BaseData"] = {}

    def __init_subclass__(cls: "BaseData", *args, dataset: str, **kwargs) -> None:
        cls.dataset = dataset
        BaseData._registry[dataset] = cls

    def __init__(self, filepath: Path):
        self.filepath = filepath

    @staticmethod
    def get_dataset(filepath):
        pass


class Data(BaseData, dataset="default"):
    def __new__(cls, filepath: Path, dataset: Union[None, str] = None):
        if dataset is None:
            dataset = cls.get_dataset(filepath)
        return BaseData._registry[dataset](filepath)

    @staticmethod
    def get_dataset(filepath):
        if filepath.name.endswith(".cdf"):
            dataset = BaseData._registry["cdf"].get_dataset(filepath)
        elif filepath.name.endswith(".fits"):
            dataset = BaseData._registry["fits"].get_dataset(filepath)
        else:
            raise NotImplementedError()
        return dataset


class CdfData(BaseData, dataset="cdf"):
    @staticmethod
    def get_dataset(filepath):
        with pycdf.CDF(str(filepath)) as c:
            dataset = c.attrs["Logical_source"][...][0]
        return dataset


class FitsData(BaseData, dataset="fits"):
    @staticmethod
    def get_dataset(filepath):
        with fits.open(filepath) as f:
            if f[0].header["INSTRUME"] == "NenuFar" and filepath.stem.endswith("_BST"):
                dataset = "nenufar_bst"
        return dataset


class SrnNdaRoutineJupEdrCdfData(BaseData, dataset="srn_nda_routine_jup_edr"):
    pass


class NenufarBstFitsData(BaseData, dataset="nenufar_bst"):
    pass


if __name__ == "__main__":
    data = Data(filepath=Path("toto.txt"), dataset="cdf")
    print(type(data))
