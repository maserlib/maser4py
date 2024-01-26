# -*- coding: utf-8 -*-
from astropy.time import Time
from astropy.units import Quantity
from .constants import BASEDIR
from maser.data import Data
from maser.data.base.sweeps import Sweep
from maser.data.padc import ExpresCdfData
import pytest
from .fixtures import skip_if_spacepy_not_available
import xarray
from pathlib import Path


TEST_FILES = {
    "expres_juno_jupiter_ganymede": BASEDIR
    / "maser"
    / "expres"
    / "expres_juno_jupiter_ganymede_jrm09_lossc-wid1deg_3kev_20211218_v11.cdf",
    "expres_earth_jupiter_io": BASEDIR
    / "maser"
    / "expres"
    / "expres_earth_jupiter_io_jrm09_lossc-wid1deg_3kev_20220801_v01.cdf",
}


@skip_if_spacepy_not_available
@pytest.fixture(scope="class", params=TEST_FILES.values(), ids=TEST_FILES.keys())
def get_data_instance(request):
    return Data(filepath=request.param)


@pytest.fixture(autouse=True, scope="class")
def _use_data(request, get_data_instance):
    request.cls.data = get_data_instance


@pytest.mark.usefixtures("_use_data")
class TestExpres:
    @pytest.mark.test_data_required
    def test_data_instance(self) -> None:
        assert isinstance(self.data, ExpresCdfData)

    @pytest.mark.test_data_required
    def test_access_mode(self) -> None:
        assert self.data.access_mode == "sweeps"

    @pytest.mark.test_data_required
    def test_frequencies(self) -> None:
        frequencies = self.data.frequencies
        assert isinstance(frequencies, Quantity)
        assert frequencies.ndim == 1
        assert frequencies.size == 781

    @pytest.mark.test_data_required
    def test_times(self) -> None:
        times = self.data.times
        assert isinstance(times, Time)
        assert times.ndim == 1
        assert times.size == 1440

    @pytest.mark.test_data_required
    def test_as_xarray(self) -> None:
        xarrays = self.data.as_xarray()
        assert isinstance(xarrays, xarray.Dataset)
        assert xarrays["CML"].units == "deg"
        assert xarrays["CML"].coords["time"].values.dtype.str == "<M8[ns]"
        assert set(self.data.dataset_keys) == set(list(xarrays.keys()))

    @pytest.mark.test_data_required
    @pytest.mark.parametrize(
        "source_id,expected_shape",
        [(0, (781, 1440)), (1, (781, 1440)), (None, (781, 1440, 2))],
    )
    def test_source_selection(self, source_id, expected_shape):
        sources = self.data.file["Src_ID_Label"][...]
        self.data.source = None if source_id is None else sources[source_id]
        assert self.data.as_xarray()["Theta"].shape == expected_shape

    @pytest.mark.test_data_required
    def test_source_selection_error(self):
        with pytest.raises(ValueError):
            self.data.source = "bad_value"

    @pytest.mark.test_data_required
    def test_sweep(self):
        for sweep in self.data.sweeps:
            assert isinstance(sweep, Sweep)
            sweep_data = sweep.data
            assert isinstance(sweep_data, dict)
            assert sweep.data["Theta"].shape == (781, 1, 2)
            break

    @pytest.mark.test_data_required
    def test_express_quicklook(self):
        filepath = TEST_FILES["expres_juno_jupiter_ganymede"]
        ql_path_tmp = Path("/tmp") / f"{filepath.stem}.png"
        data = Data(filepath=filepath, source="Ganymede NORTH")

        # checking default
        data.quicklook(ql_path_tmp)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()

        # checking all
        forbbiden_keys = [
            "CML",
            "ObsDistance",
            "ObsLatitude",
            "SrcFreqMax",
            "SrcFreqMaxCMI",
            "SrcLongitude",
        ]
        test_keys = []
        for key in data.dataset_keys:
            if key not in forbbiden_keys:
                test_keys.append(key)
        data.quicklook(ql_path_tmp, keys=test_keys)
        assert ql_path_tmp.is_file()
        ql_path_tmp.unlink()
