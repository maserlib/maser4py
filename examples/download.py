# -*- coding: utf-8 -*-
from pathlib import Path

RPW_PUB_DATA_BASE_URL = "https://rpw.lesia.obspm.fr/roc/data/pub/solo/rpw/data"


def download_file(url: str, local_filepath=None, force_download: bool = False) -> Path:
    import requests

    if local_filepath is None:
        local_filepath = url.split("/")[-1]

    # check if the file already exists
    if Path(local_filepath).exists() and not force_download:
        return local_filepath

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return Path(local_filepath)
