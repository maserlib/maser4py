# -*- coding: utf-8 -*-
from .fixtures import test_filepaths
from .constants import BASEDIR
import pytest
from maser.data import Data
import numpy

EPNCORE_TYPES = {
    "_dataset": str,
    "_file": str,
    "access_estsize": int,
    "access_format": str,
    "dataproduct_type": str,
    "feature_name": str,
    "file_name": str,
    "granule_gid": str,
    "granule_uid": str,
    "obs_id": str,
    "instrument_host_name": str,
    "instrument_name": str,
    "publisher": str,
    "spectral_range_max": float,
    "spectral_range_min": float,
    "target_class": str,
    "target_name": str,
    "target_region": str,
    "time_max": float,
    "time_min": float,
    "time_sampling_step_max": float,
    "time_sampling_step_min": float,
}


@pytest.fixture
def epncore_expected():
    import csv

    data = {}
    with open(BASEDIR / "epncore.csv") as csvfile:
        # load EPNcore data from `epncore.csv` (with option to treat non-quoted elements as floats)
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
                [
                    (k, EPNCORE_TYPES[k](v))
                    for k, v in row.items()
                    if ((v != "") and (v is not None))
                ]
            )
    return data


@pytest.mark.test_data_required
@pytest.mark.parametrize("filepath,dataset", test_filepaths())
def test_any_dataset(filepath, dataset, epncore_expected):
    if (expected_md := epncore_expected[dataset][filepath.name])[
        "granule_uid"
    ] != "__skip__":
        data = Data(filepath)
        md = data.epncore()
        assert isinstance(md, dict)
        print(dataset, filepath)
        md_keys = set(md.keys())
        # Check metadata (key,value) are as expected
        for k, v in expected_md.items():
            if isinstance(v, float) or isinstance(v, numpy.float64):
                assert md[k] == pytest.approx(v, rel=1e-5)
            elif isinstance(v, int):
                assert md[k] == v
            else:
                assert set(md[k].split("#")) == set(v.split("#"))
                # Check mandatory keys are present
        assert {"granule_uid", "granule_gid", "obs_id"}.issubset(md_keys)
