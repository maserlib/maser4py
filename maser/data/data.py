# -*- coding: utf-8 -*-
from typing import Union
from pathlib import Path


class BaseData:
    dataset: Union[None, str] = None
    _registry: dict[str, "BaseData"] = {}

    def __init_subclass__(cls: "BaseData", *args, dataset: str, **kwargs) -> None:
        cls.dataset = dataset
        BaseData._registry[dataset] = cls

    def __init__(self, filepath: Path):
        self.filepath = filepath


class Data(BaseData, dataset="default"):
    def __call__(cls, filepath: Path, dataset: str):
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
        pass


class SrnNdaRoutineJupEdrCdfData(BaseData, dataset="srn_nda_routine_jup_edr"):
    pass


if __name__ == "__main__":
    data = Data(filepath="toto.txt", dataset="cdf")
    print(type(data))
