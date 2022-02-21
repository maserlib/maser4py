# -*- coding: utf-8 -*-
from typing import Union, Dict
from pathlib import Path
from spacepy import pycdf


class BaseData:
    dataset: Union[None, str] = None
    _registry: Dict[str, "BaseData"] = {}

    def __init_subclass__(cls: "BaseData", *args, dataset: str, **kwargs) -> None:
        cls.dataset = dataset
        BaseData._registry[dataset] = cls

    def __init__(self, filepath: Path):
        self.filepath = filepath


class Data(BaseData, dataset="default"):
    def __new__(cls, filepath: Path, dataset: Union[None, str] = None):
        if dataset is None:
            cls.get_dataset(filepath)
        return BaseData._registry[dataset](filepath)

    @staticmethod
    def get_dataset(filepath):
        if filepath.name.endswith(".cdf"):
            BaseData._registry["cdf"].get_dataset(filepath)


class CdfData(BaseData, dataset="cdf"):
    @staticmethod
    def get_dataset(filepath):
        with pycdf.CDF(str(filepath)) as c:
            dataset = c.attrs["Logical_source"][...][0]
        return dataset


class SrnNdaRoutineJupEdrCdfData(BaseData, dataset="srn_nda_routine_jup_edr"):
    pass


if __name__ == "__main__":
    data = Data(filepath="toto.txt", dataset="cdf")
    print(type(data))
