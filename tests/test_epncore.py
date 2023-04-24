# -*- coding: utf-8 -*-
from .fixtures import test_filepaths
from .constants import BASEDIR
import pytest
from maser.data import Data


@pytest.fixture
def epncore_expected():
    import csv

    data = {}
    with open(BASEDIR / "epncore.csv") as csvfile:
        # load EPNcore data from `epncore.csv` (with option to treat non-quoted elements as floats)pi
        reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            # set the `dataset` and `file` names
            _dataset = row.pop("_dataset")
            _file = row.pop("_file")
            # create the `dataset` dict at first pass
            if _dataset not in data.keys():
                data[_dataset] = {}
            # fill in for each `file`, removing empty keywords on the fly
            data[_dataset][_file] = dict(
                [(k, v) for k, v in row.items() if v is not None]
            )
    return data


@pytest.mark.test_data_required
@pytest.mark.parametrize("filepath,dataset", test_filepaths())
def test_any_dataset(filepath, dataset, epncore_expected):
    if (expected_md := epncore_expected[dataset][filepath.name])[
        "granule_uid"
    ] is not None:
        data = Data(filepath)
        md = data.epncore()
        assert isinstance(md, dict)
        print(dataset, filepath)
        md_keys = set(md.keys())
        # Check metadata (key,value) are as expected
        print(md)
        print(expected_md)
        assert md == pytest.approx(expected_md)
        # Check mandatory keys are present
        assert {"granule_uid", "granule_gid", "obs_id"}.issubset(md_keys)
