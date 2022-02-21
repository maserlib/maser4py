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
    def __new__(cls, filepath: Path, dataset: str):

        return BaseData._registry[dataset](filepath)


class CdfData(BaseData, dataset="cdf"):
    pass


if __name__ == "__main__":
    data = Data(filepath="toto.txt", dataset="cdf")
    print(type(data))
