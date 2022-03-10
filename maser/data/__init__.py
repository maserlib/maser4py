# -*- coding: utf-8 -*-
from .base import Data
from pathlib import Path


if __name__ == "__main__":
    data = Data(filepath=Path("toto.txt"), dataset="cdf")
    print(type(data))
