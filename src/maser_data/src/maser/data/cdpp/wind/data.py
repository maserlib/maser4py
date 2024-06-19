# -*- coding: utf-8 -*-
from typing import Union, List
from pathlib import Path
from maser.data.base import BinData, RecordsOnly, VariableFrequencies
from .sweeps import (
    WindWavesL260sSweeps,
    WindWavesL2HighResSweeps,
    WindWaves60sSweeps,
)
from .records import WindWavesTnrL3Bqt1mnRecords
from astropy.time import Time, TimeDelta
from astropy.units import Unit
from ..utils import _read_sweep_length, _merge_dtype, _read_block
from ..const import (
    CCSDS_CDS_FIELDS,
    CALDATE_FIELDS,
    ORBIT_FIELDS,
)
import numpy as np


class WindWavesRad1L260sV2BinData(BinData, dataset="cdpp_wi_wa_rad1_l2_60s_v2"):
    """CDPP Wind Waves RAD1 Level 2 60s-Average (version 2) dataset

    - Observatory/Facility: WIND
    - Experiment: Waves
    - Repository: CDPP (Centre de Données de la Physique des Plasmas)
    - Dataset-id: `cdpp_wi_wa_rad1_l2_60s_v2`
    - Data format: Binary"""

    _iter_sweep_class = WindWavesL260sSweeps


class WindWavesL2BinData(VariableFrequencies, BinData, dataset="cdpp_wi_wa_l2"):
    """Placeholder class for `cdpp_wi_wa_XXX_l2` binary data."""

    _iter_sweep_class = WindWavesL2HighResSweeps

    _multiple_mode = None
    # _dataset_keys = ["VSPAL", "VZPAL", "TSPAL", "TZPAL"]
    _dataset_keys = [
        "VS",
        "VSP",
        "VZ",
        "TS",
        "TSP",
        "TZ",
        "MODE",
    ]  # , "MODE", "FREQ_DEGEN"]

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        BinData.__init__(self, filepath, dataset, access_mode)
        VariableFrequencies.__init__(self)
        self._data = None
        self._nsweep = None
        self._data = self._loader()
        self.fields = ["VS", "VSP", "VZ", "TS", "TSP", "TZ"]
        self.units = ["uV2/Hz", "uV2/Hz", "uV2/Hz", "s", "s", "s"]

    @property
    def _parse_file_name(self):
        pieces = self.filepath.stem.split("_")
        return dict(
            zip(
                ["facility", "instrument", "receiver", "level", "date", "version"],
                ["wind", "waves", pieces[2], pieces[3], pieces[4], pieces[5]],
            )
        )

    def _read_data_block(self, nbytes):
        import struct

        block = self.file.read(nbytes)
        Vspal = struct.unpack(">" + "f" * (nbytes // 4), block)
        block = self.file.read(nbytes)
        Tspal = struct.unpack(">" + "f" * (nbytes // 4), block)
        return np.array(Vspal, dtype=float), np.array(Tspal, dtype=float)

    def _loader(self, count_only=False):
        data = []
        nsweep = 0

        ccsds_fields, ccsds_dtype = CCSDS_CDS_FIELDS
        caldate_fields, caldate_dtype = CALDATE_FIELDS
        header_fields = (
            ccsds_fields
            + ["RECEIVER_CODE", "JULIAN_SEC"]
            + caldate_fields
            + [
                "JULIAN_SEC_FRAC",
                "ISWEEP",
                "IUNIT",
                "NPBS",
                "SUN_ANGLE",
                "SPIN_RATE",
                "KSPIN",
                "MODE",
                "LISTFR",
                "NFREQ",
                "ICAL",
                "IANTEN",
                "IPOLA",
                "IDIPXY",
                "SDURCY",
                "SDURPA",
                "NPALCY",
                "NFRPAL",
                "NPALIF",
                "NSPALF",
                "NZPALF",
            ]
        )
        header_dtype = _merge_dtype(
            (ccsds_dtype, ">hL", caldate_dtype, ">fihhffhhhhhhhhffhhhhh")
        )

        while True:
            try:
                # Reading number of bytes in the current sweep
                loctets1 = _read_sweep_length(self.file)
                if loctets1 is None:
                    break

                # Reading header parameters in the current sweep
                header_i = _read_block(self.file, header_dtype, header_fields)
                npalf = header_i["NPALIF"]
                nspal = header_i["NSPALF"]
                nzpal = header_i["NZPALF"]

                # Reading frequency list (kHz) in the current sweep
                cur_dtype = ">" + "f" * npalf
                freq = np.array(_read_block(self.file, cur_dtype), dtype=float)

                if self.load_data:
                    # Reading intensity and time values for S/SP in the current sweep
                    Vspal, Tspal = self._read_data_block(4 * npalf * nspal)
                    # Reading intensity and time values for Z in the current sweep
                    Vzpal, Tzpal = self._read_data_block(4 * npalf * nzpal)

                    # Get indices of S and SP channels
                    index_s = (2 * np.arange(nspal / 2)).astype(int)
                    index_sp = (2 * np.arange(nspal / 2) + 1).astype(int)

                    # Reshape Vspal, Tspal, Vzpal, Tzpal into 2D arrays
                    Vspal = Vspal.reshape((npalf, nspal)).T
                    Vzpal = Vzpal.reshape((npalf, nzpal)).T
                    Tspal = Tspal.reshape((npalf, nspal)).T
                    Tzpal = Tzpal.reshape((npalf, nzpal)).T

                    data_i = {
                        "FREQ": np.tile(freq, (nzpal, 1)).T,
                        "VST": Vspal,
                        "VS": np.take(Vspal, index_s, axis=0),
                        "VSP": np.take(Vspal, index_sp, axis=0),
                        "VZ": Vzpal,  # .T works
                        "TS": np.take(Tspal, index_s, axis=0),
                        "TSP": np.take(Tspal, index_sp, axis=0),
                        "TZ": Tzpal,  # .T works
                    }

                else:
                    # Skip data section
                    self.file.seek(8 * npalf * (nspal + nzpal), 1)
                    data_i = None
                # Reading number of octets in the current sweep
                loctets2 = _read_sweep_length(self.file)
                if loctets2 != loctets1:
                    print("Error reading file!")
                    return None
            except EOFError:
                print("End of file reached")
                break
            else:
                data.append({"hdr": header_i, "dat": data_i})
                nsweep += 1

        self._nsweep = nsweep
        return data

    @property
    def multiple_mode(self):
        if self._multiple_mode is None:
            modes = []
            for s in self.sweeps:
                modes.append(s.header["MODE"])
            if 2 in modes and 3 in modes:
                self._multiple_mode = 1
            else:
                self._multiple_mode = 0
        return self._multiple_mode

    @property
    def max_sweep_length(self):
        if self._max_sweep_length is None:
            self._max_sweep_length = np.max(
                [len(f.flatten()) for f in self.tmp_frequencies]
            )
        return self._max_sweep_length

    @property
    def times(self):

        if self._times is None:
            times = Time([], format="jd")
            for s in self.sweeps:
                header = s.header
                nzpalf = header["NZPALF"]
                nspalf = header["NSPALF"]
                if nspalf != nzpalf * 2:
                    print(
                        "WARNING: Wind data has unexpected dimensions, process might fail."
                    )
                sweep_degen_level = 0
                sweep_freqs = s.data["FREQ"][:, 0]  # Freqs in the current sweep
                sweep_freq_list = np.sort(list(set(sweep_freqs)))  # unique freqs
                index = []
                for i in range(len(sweep_freq_list)):
                    index = np.append(
                        index, int(np.count_nonzero(sweep_freqs == sweep_freq_list[i]))
                    )
                sweep_degen_level = int(
                    np.max(index)
                )  # max number of time a freq is measured
                sub_sweep_len = int(
                    header["NPALIF"] // sweep_degen_level
                )  # time between measuring the same freq

                dts = s.data["TS"]
                dtsp = s.data["TSP"]
                dtz = s.data["TZ"]
                dtmin = np.min(
                    [dts.T.flatten(), dtsp.T.flatten(), dtz.T.flatten()], axis=0
                )

                tsweep = Time(
                    f"{header['CALEND_DATE_YEAR']}-{header['CALEND_DATE_MONTH']}-"
                    f"{header['CALEND_DATE_DAY']} {header['CALEND_DATE_HOUR']}:"
                    f"{header['CALEND_DATE_MINUTE']}:{header['CALEND_DATE_SECOND']}"
                )

                for i in range(sweep_degen_level):
                    loc = i * sub_sweep_len * nzpalf
                    times = np.append(
                        times,
                        tsweep + TimeDelta(dtmin[loc : loc + nzpalf], format="sec"),
                    )
            self._times = Time(times)
        return self._times

    @property
    def tmp_times(self):
        import numpy

        tmp_times = Time([], format="jd")
        for s in self.sweeps:
            header = s.header
            tmp_times = numpy.append(
                tmp_times,
                Time(
                    f"{header['CALEND_DATE_YEAR']}-{header['CALEND_DATE_MONTH']}-"
                    f"{header['CALEND_DATE_DAY']} {header['CALEND_DATE_HOUR']}:"
                    f"{header['CALEND_DATE_MINUTE']}:{header['CALEND_DATE_SECOND']}"
                ),
            )
        tmp_times = Time(tmp_times)
        return tmp_times

    @property
    def frequencies(self):
        if self._frequencies is None:
            self._frequencies = []
            raw_frequencies = []
            for s in self.sweeps:
                raw_frequencies.append(s.data["FREQ"] * Unit("kHz"))
                for f in s.data["FREQ"][:, 0]:
                    if f not in self._frequencies:
                        self._frequencies.append(f)
            self._frequencies = np.array(
                list(np.sort(list(self._frequencies)))
            )  # * Unit("kHz")[...] # return the unique freq list
            self._frequencies = [self._frequencies[...] * Unit("kHz")]
        return self._frequencies

    @property
    def tmp_frequencies(self):
        raw_frequencies = []
        for s in self.sweeps:
            raw_frequencies.append(s.data["FREQ"] * Unit("kHz"))
        return raw_frequencies

    @property
    def dataset_keys(self):
        return self._dataset_keys

    def as_xarray(self, replicate=True, tmp_out=False):
        import xarray

        fields = self.fields
        units = self.units
        fields.append("MODE")
        units.append("#")
        if False:
            fields.append("FREQ_DEGEN")
            units.append("#")
            fields.append("FREQ")
            units.append("kHz")

        if tmp_out:
            freq_arr = np.full((self._nsweep, self.max_sweep_length), np.nan)

            for i in range(self._nsweep):
                f = self.tmp_frequencies[i].value.flatten()
                freq_arr[i, : len(f)] = f
                freq_arr[i, len(f) :] = f[-1]

            freq_index = range(self.max_sweep_length)

            datasets = {}
            for dataset_key, dataset_unit in zip(fields, units):
                data_arr = np.full((self._nsweep, self.max_sweep_length), np.nan)
                if dataset_key != "MODE":
                    for i, sweep in enumerate(self.sweeps):
                        d = sweep.data[dataset_key].flatten()
                        data_arr[i, : len(d)] = d
                else:
                    for i, sweep in enumerate(self.sweeps):
                        d = sweep.header["MODE"]
                        data_arr[i, :] = d

                datasets[dataset_key] = xarray.DataArray(
                    data=data_arr.T,
                    name=dataset_key,
                    coords={
                        "freq_index": freq_index,
                        "time": self.tmp_times.to_datetime(),
                        "frequency": (
                            ["time", "freq_index"],
                            freq_arr,
                            {"units": "kHz"},
                        ),
                    },
                    attrs={"units": dataset_unit},
                    dims=("freq_index", "time"),
                )

            return xarray.Dataset(data_vars=datasets)

        else:
            # Final data reorganisation from tmp to final
            data_reorg = {}
            for dataset_key in fields:
                data_reorg[dataset_key] = np.full(
                    (np.shape(self.frequencies[0])[0], len(self.times)), np.nan
                )
            sweep_loc = 0
            freq_ref = self.frequencies[0].value[...]
            for s in self.sweeps:
                header = s.header
                nzpalf = header["NZPALF"]
                nspalf = header["NSPALF"]
                if nspalf != nzpalf * 2:
                    print(
                        "WARNING: Wind data has unexpected dimensions, process might fail."
                    )
                sweep_degen_level = 0
                sweep_freqs = s.data["FREQ"][:, 0]  # Freqs in the current sweep
                sweep_freq_list = np.sort(list(set(sweep_freqs)))  # unique freqs
                freq_degen = []
                freq_loc = {}
                for i in range(len(sweep_freq_list)):
                    freq_degen = np.append(
                        freq_degen,
                        int(np.count_nonzero(sweep_freqs == sweep_freq_list[i])),
                    )
                    freq_loc[sweep_freq_list[i]] = np.where(
                        sweep_freqs == sweep_freq_list[i]
                    )
                sweep_degen_level = int(
                    np.max(freq_degen)
                )  # max number of time a freq is measured
                sub_sweep_len = int(
                    header["NPALIF"] // sweep_degen_level
                )  # time between measuring the same freq
                sweep_degen_frac = np.array(sweep_degen_level // freq_degen, dtype=int)

                dts = s.data["TS"]
                dtsp = s.data["TSP"]
                dtz = s.data["TZ"]
                dtmin = np.min(
                    [dts.T.flatten(), dtsp.T.flatten(), dtz.T.flatten()], axis=0
                )
                t_out_min = sweep_loc
                t_out_max = sweep_loc + sweep_degen_level * nzpalf
                delta_times = []

                for i in range(sweep_degen_level):
                    loc = i * sub_sweep_len * nzpalf
                    delta_times = np.append(
                        delta_times,
                        dtmin[loc : loc + nzpalf],
                    )
                for i in range(len(sweep_freq_list)):
                    freq_out = int(np.where(sweep_freq_list[i] == freq_ref)[0])
                    freq = sweep_freq_list[i]
                    freq_in = []
                    time_out_final = np.arange(t_out_min, t_out_max, 1)
                    if False:
                        # Technically works, probably faster
                        # but copy each subsweep as is and thus not the last measurement (full nzpalf vector is used)
                        freq_in = (
                            np.tile(
                                freq_loc[freq], (sweep_degen_frac[i], 1)
                            ).T.flatten(),
                        )
                        time_out = time_out_final
                    else:
                        freq_in = freq_loc[freq]
                        nztab = np.tile(
                            np.arange(0, nzpalf, 1), (len(freq_loc[freq][0]), 1)
                        )
                        time_out = np.tile(
                            np.array(freq_loc[freq]) // sub_sweep_len * nzpalf,
                            (nzpalf, 1),
                        ).T
                        time_out = (time_out + nztab + t_out_min).flatten()
                    if replicate:
                        # replace all NaN by the last previous value
                        nan_mask = np.in1d(time_out_final, time_out)
                        nan_loc = time_out_final[np.where(~nan_mask)[0]]
                        replace_loc = np.copy(nan_loc)
                        for k in range(len(replace_loc)):
                            replace_loc[k] = (
                                time_out.searchsorted(replace_loc[k], "right") - 1
                            )
                        if sweep_loc == 0:
                            replace_loc = replace_loc[np.where(replace_loc > 0)]
                            nan_loc = nan_loc[np.where(replace_loc > 0)]
                        replace_loc = np.append(time_out, [np.min(time_out_final) - 1])[
                            replace_loc
                        ]
                    for dataset_key in fields:
                        if dataset_key == "MODE":
                            d = np.full(np.shape(dts), np.nan)
                            d[:] = int(header["MODE"])
                        elif dataset_key == "FREQ_DEGEN":
                            d = np.full(np.shape(dts), np.nan)
                            d[:] = int(sweep_degen_frac[i])
                        elif dataset_key == "FREQ":
                            d = np.full(np.shape(dts), np.nan)
                            d[:] = freq
                        else:
                            d = s.data[dataset_key]
                        data_reorg[dataset_key][freq_out, time_out] = d[
                            :, freq_in
                        ].T.flatten()
                        if replicate:
                            # replace all NaN by the last previous value
                            data_reorg[dataset_key][freq_out, nan_loc] = data_reorg[
                                dataset_key
                            ][freq_out, replace_loc]
                        if dataset_key in ["TS", "TSP", "TZ"]:
                            data_reorg[dataset_key][
                                freq_out, time_out_final
                            ] -= delta_times
                sweep_loc += sweep_degen_level * nzpalf

            datasets = {}
            for dataset_key, dataset_unit in zip(fields, units):
                data_arr = data_reorg[dataset_key]

                datasets[dataset_key] = xarray.DataArray(
                    data=data_arr,
                    name=dataset_key,
                    coords=[
                        ("frequency", self.frequencies[0].value, {"units": "kHz"}),
                        ("time", self.times.to_datetime(), {}),
                    ],
                    attrs={"units": dataset_unit},
                    dims=("frequency", "time"),
                )
            return xarray.Dataset(data_vars=datasets)

    def quicklook(
        self,
        file_png=None,
        keys: Union[List[str], None] = None,
        yscale: str = "log",
        **kwargs,
    ):
        if keys is None:
            keys = self.dataset_keys
        default_keys = self.dataset_keys
        selection = None
        if self.multiple_mode == 1:
            selection = {
                "select_key": ["MODE", "MODE"],
                "select_value": [3, 2],
                "select_dim": ["frequency", "frequency"],
                "select_how": ["all", "all"],
            }
        db_tab = np.array([True, True, True, False, False, False, False, False])
        vmin_tab = np.array([-50, -50, -50, 0, 0, 0, 0, 0])
        vmax_tab = np.array([50, 50, 50, 170, 170, 170, 4, 10])
        for qkey, tab in zip(["db", "vmin", "vmax"], [db_tab, vmin_tab, vmax_tab]):
            if qkey not in kwargs:
                qkey_tab = []
                for key in keys:
                    if key in default_keys:
                        qkey_tab.append(tab[np.where(key == np.array(default_keys))][0])
                    else:
                        qkey_tab.append(None)
                kwargs[qkey] = list(qkey_tab)
        self._quicklook(
            file_png=file_png,
            keys=keys,
            iter_on_selection=selection,
            yscale=yscale,
            y="frequency",
            ylim=[15, 1200],
            **kwargs,
        )

    def epncore(self):
        md = BinData.epncore(self)
        md["granule_uid"] = f"{self.dataset}:{self.filepath.stem}"
        md[
            "obs_id"
        ] = f"wi_wa_{self._parse_file_name['receiver']}_{self._parse_file_name['date']}"

        md["instrument_host_name"] = "wind"
        md["instrument_name"] = "waves"
        md["target_name"] = "Earth#Sun"
        md["target_class"] = "planet#star"
        md["target_region"] = "magnetosphere#heliopshere"
        md[
            "feature_name"
        ] = "AKR#Auroral Kilometric Radiation#Solar bursts#Type II#Type III"

        md["dataproduct_type"] = "ds"

        md["spectral_range_min"] = min(
            [min(item.to("Hz").value) for item in self.frequencies]
        )
        md["spectral_range_max"] = max(
            [max(item.to("Hz").value) for item in self.frequencies]
        )

        md["publisher"] = "CNES/CDPP"
        return md


class WindWavesRad1L2BinData(WindWavesL2BinData, dataset="cdpp_wi_wa_rad1_l2"):
    """Class for `cdpp_wi_wa_rad1_l2` binary data."""

    pass


class WindWavesRad2L260sV2BinData(BinData, dataset="cdpp_wi_wa_rad2_l2_60s_v2"):
    """Class for `cdpp_wi_wa_rad2_l2_60s_v2` binary data."""

    pass


class WindWavesTnrL260sV2BinData(BinData, dataset="cdpp_wi_wa_tnr_l2_60s_v2"):
    """Class for `cdpp_wi_wa_tnr_l2_60s_v2` binary data."""

    pass


class WindWavesTnrL3Bqt1mnBinData(
    RecordsOnly, BinData, dataset="cdpp_wi_wa_tnr_l3_bqt_1mn"
):
    """Class for `cdpp_wi_wa_tnr_l3_bqt_1mn` data."""

    _iter_record_class = WindWavesTnrL3Bqt1mnRecords

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "records",
        load_data: bool = True,
    ) -> None:
        super().__init__(filepath, dataset, access_mode, load_data)


class WindWavesTnrL3NnBinData(BinData, dataset="cdpp_wi_wa_tnr_l3_nn"):
    """Class for `cdpp_wi_wa_tnr_l3_nn` data."""

    pass


class WindWavesL260sV1BinData(BinData, dataset="cdpp_wi_wa___l2_60s_v1"):
    """Class for `cdpp_wi_wa_rad1_l2_60s_v1` binary data"""

    _iter_sweep_class = WindWaves60sSweeps

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        super().__init__(filepath, dataset, access_mode, fixed_frequencies=False)
        self._data = None
        self._nsweep = None
        self.__max_sweep_length = None
        self._data = self._loader()

    def _loader(self):
        data = []

        ccsds_fields, ccsds_dtype = CCSDS_CDS_FIELDS

        caldate_fields, caldate_dtype = CALDATE_FIELDS

        header_fields = (
            ccsds_fields
            + ["RECEIVER_CODE", "JULIAN_SEC"]
            + caldate_fields
            + ["AVG_DURATION", "IUNIT", "NFREQ"]
        )

        # RECEIVER_CODE [Int, 16 bits] = Name of Receiver: 0=TNR; 1=RAD1; 2=RAD2
        # JULIAN_SEC [Int, 32 bits] = Julian date of the middle of the 60-second interval (in seconds since 1950/01/01)

        orbit_fields, orbit_dtype = ORBIT_FIELDS

        header_dtype = _merge_dtype((ccsds_dtype, ">hi", caldate_dtype, ">hhh"))

        nsweep = 0

        while True:
            try:
                # Reading number of octets in the current sweep
                loctets1 = _read_sweep_length(self.file)
                if loctets1 is None:
                    break

                # Reading header parameters in the current sweep
                header_i = _read_block(self.file, header_dtype, header_fields)
                nfreq = header_i["NFREQ"]

                if self.load_data:
                    # Reading orbit data for current sweep
                    orbit = _read_block(self.file, orbit_dtype, orbit_fields)

                    # Reading frequency list in the current sweep
                    cur_dtype = ">" + "f" * nfreq
                    freq = _read_block(self.file, cur_dtype)

                    # Reading frequency list in the current sweep
                    intensity = _read_block(self.file, cur_dtype)

                    data_i = {
                        "FREQ": freq,
                        "INTENSITY": intensity,
                        "ORBIT": orbit,
                    }
                else:
                    # Skip data section
                    self.file.seek(12 + 8 * nfreq, 1)
                    data_i = None

                # Reading number of octets in the current sweep
                loctets2 = _read_sweep_length(self.file)
                if loctets2 != loctets1:
                    print("Error reading file!")
                    return None

            except EOFError:
                print("End of file reached")
                break

            else:
                data.append({"hdr": header_i, "dat": data_i})
                nsweep += 1

        self._nsweep = nsweep
        return data


class WindWavesRad1L260sV1BinData(
    WindWavesL260sV1BinData, dataset="cdpp_wi_wa_rad1_l2_60s_v1"
):
    """Class for `cdpp_wi_wa_rad1_l2_60s_v1` binary data"""

    pass


class WindWavesRad2L260sV1BinData(
    WindWavesL260sV1BinData, dataset="cdpp_wi_wa_rad2_l2_60s_v1"
):
    """Class for `cdpp_wi_wa_rad2_l2_60s_v1` binary data"""

    pass


class WindWavesTnrL260sV1BinData(
    WindWavesL260sV1BinData, dataset="cdpp_wi_wa_tnr_l2_60s_v1"
):
    """Class for `cdpp_wi_wa_tnr_l2_60s_v1` binary data"""

    pass
