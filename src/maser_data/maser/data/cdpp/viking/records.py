# -*- coding: utf-8 -*-
from maser.data.base import Records
import struct
from ..const import CCSDS_CCS_FIELDS, CALDATE_FIELDS
from ..utils import _merge_dtype, _read_block


def is_empty(data):
    if type(data) is dict:
        if all([v == 0 for v in data.values()]):
            return True
        elif all([v is None for v in data.values()]):
            return True
    elif (type(data) is list) or (type(data) is tuple) or (type(data) is set):
        if all([v == 0 for v in data]):
            return True
        elif all([v is None for v in data]):
            return True
    elif data is None:
        return True
    else:
        return False


class VikingV4nE5Records(Records):
    dataset_names = [
        "VIKING_V4",
        "VIKING_V4_V1",
        "VIKING_V4H_SFA",
        "VIKING_V4H_FB",
        "VIKING_V4L_FBL",
        "VIKING_V4_V2",
        "VIKING_V4L_Ni",
        "VIKING_V4L_DFT",
        "VIKING_V4L_WF",
    ]

    @property
    def generator(self):

        header1a_fields, header1a_dtype = (["RECORD_NUMBER"], ">h")
        # WARNING: CNES/CDPP SCRIBE DESCRIPTOR IS WRONG -- CCSDS DAY_IN_YEAR_02 is not present
        # This dataset uses CCSDS-CCS Time Format.
        # year, month, day, hour, minute, second, CCSDS_B0*256 + CCSDS_B1
        header1b_fields, header1b_dtype = CCSDS_CCS_FIELDS
        header1c_fields, header1c_dtype = CALDATE_FIELDS
        header1c_fields = header1c_fields + ["CALEND_DATE_MILLI_SECOND"]
        header1c_dtype = header1c_dtype + "h"

        header1d_fields, header1d_dtype = (
            ["ORBIT_NUMBER", "SATELLITE_TIME_MSB", "SATELLITE_TIME_LSB"],
            ">hII",
        )
        # WARNING: UNUSED field is not present in header
        header1e_fields, header1e_dtype = (
            [
                "BUFFER_TYPE",
                "BUFFER_NUMBER",
                "SWEEP_NUMBER",
                "COMPLETE_SWEEP",
                "SWEEP_DURATION",
                "NUMBER_OF_SERIES_IN_CURRENT_SWEEP",
                "NUMBER_OF_SIGNIFICANT_SERIES_IN_CURRENT_RECORD",
                "ABNORMAL_END_OF_SWEEP",
            ],
            ">hhhhfhhh",
        )
        header1f_fields, header1f_dtype = (
            ["TM_LACK_BEFORE_SWEEP", "TM_LACK_AFTER_SWEEP"],
            ">BB",
        )
        header1g_fields, header1g_dtype = (
            ["NUMBER_OF_RECORDS_IN_CURRENT_SWEEP", "RANK_OF_RECORD_IN_CURRENT_SWEEP"],
            ">BB",
        )
        # WARNING: NOT_MEANINGFUL field is not present in header
        header1h_fields, header1h_dtype = (
            [
                "V4L_MODE_SWITCH_FLAGS_BEFORE_SWEEP",
                "V4L_MODE_SWITCH_FLAGS_DURING_SWEEP",
                "V4L_MODE_SWITCH_FLAGS_FIRST_SWITCH_SERIAL_NUMBER",
            ],
            ">hhh",
        )
        header1i_fields, header1i_dtype = (
            [
                "UTC_CCSDS_PREAMBLE",
                "UTC_CCSDS_YEAR",  # year
                "UTC_CCSDS_MONTH",  # month
                "UTC_CCSDS_DAY",  # day in month
                "UTC_CCSDS_HOUR",  # hour
                "UTC_CCSDS_MINUTE",  # minute
                "UTC_CCSDS_SECOND",  # second
                "UTC_CCSDS_1E2_SEC",  # 1e-2 seconds
                "UTC_CCSDS_1E4_SEC",  # 1e-4 seconds
            ],
            ">BhBBBBBBB",
        )
        # WARNING: CNES/CDPP SCRIBE DESCRIPTOR IS WRONG -- CCSDS DAY_IN_YEAR_02 is not present
        header1j_fields, header1j_dtype = (
            [
                "UTC_CALENDAR_YEAR",
                "UTC_CALENDER_MONTH",
                "UTC_CALENDAR_DAY",
                "UTC_CALENDAR_HOUR",
                "UTC_CALENDAR_MINUTE",
                "UTC_CALENDAR_SECOND",
                "UTC_CALENDAR_MILLI_SECOND",
            ],
            ">hhhhhhh",
        )

        header1_fields = (
            header1a_fields
            + header1b_fields
            + header1c_fields
            + header1d_fields
            + header1e_fields
            + header1f_fields
            + header1g_fields
            + header1g_fields
            + header1h_fields
            + header1i_fields
            + header1j_fields
        )
        header1_dtype = _merge_dtype(
            (
                header1a_dtype,
                header1b_dtype,
                header1c_dtype,
                header1d_dtype,
                header1e_dtype,
                header1f_dtype,
                header1g_dtype,
                header1g_dtype,
                header1h_dtype,
                header1i_dtype,
                header1j_dtype,
            )
        )
        header1_spare_len = 36

        header2_fields = [
            "V4H_SFA_ELEMENT_NUMBER",
            "V4H_SFA_SWEEP_TYPE",
            "V4H_SFA_NUMBER_OF_FORMATS_IN_SWEEP",
            "V4H_SFA_SWEEP_RANGE",
            "V4H_SFA_SWEEP_MODE",
            "V4H_SFA_ANTENNA",
            "V4H_SFA_NUMBER_OF_FREQUENCY_STEPS",
            "V4H_SFA_NUMBER_OF_SAMPLES",
            "GYROFREQUENCY",
            "V4H_FREQ_STEP_COEFF_MAG_OFFSET_KHZ_1",
            "V4H_FREQ_STEP_COEFF_MAG_OFFSET_KHZ_2",
            "V4H_FREQ_STEP_COEFF_MAG_OFFSET_KHZ_3",
            "V4H_FREQ_STEP_COEFF_ELE_OFFSET_KHZ_1",
            "V4H_FREQ_STEP_COEFF_ELE_OFFSET_KHZ_2",
            "V4H_FREQ_STEP_COEFF_ELE_OFFSET_KHZ_3",
            "V4H_FREQ_STEP_SYNTH_INCREMENT",
        ]  # V4H OPERATING MODE
        header2_dtype = ">hhhhhhhhffffffff"
        header2_spare_len = 16

        header3_fields = [
            "V4L_MUX_1_POSITION",
            "V4L_MUX_2_POSITION",
            "V4L_TM_MODE",
            "V4L_DFT_FREQUENCY_RANGE",
            "V4L_TIME_RESOLUTION_OF_DFT_SPECTRAL_DATA",
            "V4L_WF_FREQUENCY_RANGE",
            "V4L_NUMBER_OF_DFT_SPECTRA",
            "V4L_NUMBER_OF_DFT_SAMPLES",
            "V4L_NUMBER_OF_SERIES_PER_WF_CHANNEL",
            "V4L_NUMBER_OF_SAMPLES_PER_WF_CHANNEL",
        ]  # V4L OPERATING MODE
        header3_dtype = ">hhhhhhhhhh"
        header3_spare_len = 44

        data_v1_fields = [
            "V1_RELATIVE_TIME",
            "V1_EPAR",
            "V1_EC",
            "V1_ED",
            "V1_VFG",
            "V1_EPDIFF",
            "V1_USER_BIAS",
            "V1_VGUARD",
            "V1_IFILL",
            "V1_ID",
        ]
        data_v1_dtype = ">ffffffffhh"
        data_v1_spare_len = 184

        orbit_fields = [
            "ORBIT_RELATIVE_TIME",
            "SPACECRAFT_GEOGRAPHIC_LAT",
            "SPACECRAFT_GEOGRAPHIC_LON",
            "SPACECRAFT_GEOGRAPHIC_ALT",
            "SPACECRAFT_VEL_X",
            "SPACECRAFT_VEL_Y",
            "SPACECRAFT_VEL_Z",
            "MAGNETIC_LOCAL_TIME",
            "INVARIANT_LATITUDE",
            "SPACECRAFT_ATTITUDE_BFIELD_SPEED_ANGLE",
            "SPACECRAFT_ATTITUDE_SPIN_ANGLE",
        ]
        orbit_dtype = ">fffffffffff"
        orbit_spare_len = 212

        data_v2_fields = ["V2_AMPLITUDE", "V2_PSI", "V2_PHI", "V2_THETA"]
        data_v2_dtype = ">ffff"

        # Defining empty data dict templates

        data_v4_v1_empty = {
            "V1_RELATIVE_TIME": None,
            "V1_EPAR": None,
            "V1_EC": None,
            "V1_ED": None,
            "V1_VFG": None,
            "V1_EPDIFF": None,
            "V1_USER_BIAS": None,
            "V1_VGUARD": None,
            "V1_IFILL": None,
            "V1_ID": None,
        }

        data_v4_v2_empty = {
            "V2_AMPLITUDE": None,
            "V2_PSI": None,
            "V2_PHI": None,
            "V2_THETA": None,
        }

        data_v4h_sfa_empty = {
            "FREQUENCY_SFA": None,
            "ELECTRIC_SFA": None,
            "MAGNETIC_SFA": None,
        }

        data_v4h_fb_empty = {
            "FREQUENCY_FB": None,
            "MAGNETIC_FB": None,
            "ELECTRIC_FB": None,
        }

        data_v4l_fbl_empty = {"FREQUENCY_FBL": None, "ELECTRIC_FBL": None}

        data_v4l_ni_empty = {"N1_PROBE": None, "N2_PROBE": None}

        data_v4l_dft_empty = {"DFT": None}

        data_v4l_wf_empty = {"WF1": None, "WF2": None}

        #        header = []
        #        header_v4l = []
        #        header_v4h = []
        #        status = []
        #        data = []
        #        orbit = []
        nsweep = 0

        while True:
            read_index_start = self.file.tell()
            try:
                print("Reading sweep #{}".format(nsweep))

                # Reading header1 parameters in the current record
                header1_i = _read_block(self.file, header1_dtype, header1_fields)
                print(header1_i)
                self.file.read(header1_spare_len)

                # Reading header2 parameters in the current record
                header2_i = _read_block(self.file, header2_dtype, header2_fields)
                self.file.read(header2_spare_len)

                # Reading header3 parameters in the current record
                header3_i = _read_block(self.file, header3_dtype, header3_fields)
                self.file.read(header3_spare_len)

                # Reading status data in the current record
                status_i = list()
                for i in range(16):
                    cur_stat = dict()
                    cur_stat["G"] = _read_block(self.file, ">hhhhhhhh")
                    for j in range(3):
                        block = self.file.read(16)
                        cur_stat["ST{}".format(j + 8)] = _read_block(
                            self.file, ">hhhhhhhh"
                        )
                    for j in range(8):
                        block = self.file.read(2)
                        cur_stat["ST{}".format(j)] = _read_block(self.file, ">h")
                    status_i.append(cur_stat)

                data_i = dict()

                # Reading Viking V1 data in the current record

                data_v1 = data_v4_v1_empty
                data_v1_tmp1 = _read_block(self.file, data_v1_dtype, data_v1_fields)
                data_v1_tmp2 = _read_block(self.file, data_v1_dtype, data_v1_fields)

                if not is_empty(data_v1_tmp1) or not is_empty(data_v1_tmp2):
                    for k in data_v1_fields:
                        data_v1[k] = []
                        if not is_empty(data_v1_tmp1):
                            data_v1[k].append(data_v1_tmp1[k])
                        if not is_empty(data_v1_tmp2):
                            data_v1[k].append(data_v1_tmp2[k])

                self.file.read(data_v1_spare_len)
                data_i["VIKING_V4_V1"] = data_v1

                # Reading Viking orbit data in the current record
                orbit_i = _read_block(self.file, orbit_dtype, orbit_fields)
                self.file.read(orbit_spare_len)

                # Reading Viking V4H SFA data in the current record

                if is_empty(header2_i):
                    self.file.read(3072)
                    data_i["VIKING_V4H_SFA"] = data_v4h_sfa_empty
                else:
                    cur_dtype = ">" + "f" * 256
                    data_tmp = _read_block(self.file, cur_dtype)
                    if is_empty(data_tmp):
                        data_v4h_sfa_freq = None
                    else:
                        data_v4h_sfa_freq = data_tmp

                    data_tmp = _read_block(self.file, cur_dtype)
                    if is_empty(data_tmp):
                        data_v4h_sfa_elec = None
                    else:
                        data_v4h_sfa_elec = data_tmp

                    data_tmp = _read_block(self.file, cur_dtype)
                    if is_empty(data_tmp):
                        data_v4h_sfa_mag = None
                    else:
                        data_v4h_sfa_mag = data_tmp

                    if is_empty(data_v4h_sfa_elec) and is_empty(data_v4h_sfa_mag):
                        data_i["VIKING_V4H_SFA"] = data_v4h_sfa_empty
                    else:
                        data_i["VIKING_V4H_SFA"] = {
                            "FREQUENCY_SFA": data_v4h_sfa_freq,
                            "ELECTRIC_SFA": data_v4h_sfa_elec,
                            "MAGNETIC_SFA": data_v4h_sfa_mag,
                        }

                # Reading Viking V4H Filter Bank in the current record

                if is_empty(header2_i):
                    self.file.read(4096)
                    data_i["VIKING_V4H_FB"] = data_v4h_fb_empty
                else:
                    data_v4h_fbb = list()
                    data_v4h_fbe = list()
                    data_v4h_fbf = [2 ** (i + 2) for i in range(8)]
                    for i in range(8):
                        block = self.file.read(256)
                        data_tmp = struct.unpack(">" + "f" * 64, block)
                        if is_empty(data_tmp):
                            data_v4h_fbb.append(None)
                        else:
                            data_v4h_fbb.append(data_tmp)
                    for i in range(8):
                        block = self.file.read(256)
                        data_tmp = struct.unpack(">" + "f" * 64, block)
                        if is_empty(data_tmp):
                            data_v4h_fbe.append(None)
                        else:
                            data_v4h_fbe.append(data_tmp)

                    if is_empty(data_v4h_fbb) and is_empty(data_v4h_fbe):
                        data_i["VIKING_V4H_FB"] = data_v4h_fb_empty
                    else:
                        data_i["VIKING_V4H_FB"] = {
                            "FREQUENCY_FB": data_v4h_fbf,
                            "MAGNETIC_FB": data_v4h_fbb,
                            "ELECTRIC_FB": data_v4h_fbe,
                        }

                # Reading Viking V4L Filter Bank in the current record

                if is_empty(header3_i):
                    self.file.read(768)
                    data_i["VIKING_V4L_FBL"] = data_v4l_fbl_empty
                else:
                    data_v4l_fbl = list()
                    data_v4l_fbl_fmin = [200, 520, 1350]
                    data_v4l_fbl_fmax = [520, 1350, 3500]
                    data_v4l_fbl_freq = [
                        (data_v4l_fbl_fmin[i] + data_v4l_fbl_fmax[i]) / 2
                        for i in range(3)
                    ]
                    for i in range(3):
                        block = self.file.read(256)
                        data_tmp = struct.unpack(">" + "f" * 64, block)
                        if is_empty(data_tmp):
                            data_v4l_fbl.append(None)
                        else:
                            data_v4l_fbl.append(data_tmp)

                    if is_empty(data_v4l_fbl):
                        data_i["VIKING_V4L_FBL"] = data_v4l_fbl_empty
                    else:
                        data_i["VIKING_V4L_FBL"] = {
                            "FREQUENCY_FBL": data_v4l_fbl_freq,
                            "ELECTRIC_FBL": data_v4l_fbl,
                        }

                # Reading Viking V2 data in the current record
                data_i["VIKING_V4_V2"] = data_v4_v2_empty

                data_v2 = list()
                for i in range(16):
                    block = self.file.read(struct.calcsize(data_v2_dtype))
                    data_tmp = _read_block(self.file, data_v2_dtype, data_v2_fields)
                    if is_empty(data_tmp):
                        data_v2.append(None)
                    else:
                        data_v2.append(data_tmp)

                if is_empty(data_v2):
                    data_v2 = None

                data_i["VIKING_V4_V2"] = data_v2

                # Reading Viking V4L LP data in the current record

                if is_empty(header3_i):
                    self.file.read(2048)
                    data_i["VIKING_V4L_Ni"] = data_v4l_ni_empty
                else:
                    block = self.file.read(1024)
                    data_tmp = struct.unpack(">" + "f" * 256, block)
                    if not is_empty(data_tmp):
                        data_v4l_n1 = data_tmp
                    else:
                        data_v4l_n1 = None

                    block = self.file.read(1024)
                    data_tmp = struct.unpack(">" + "f" * 256, block)
                    if not is_empty(data_tmp):
                        data_v4l_n2 = data_tmp
                    else:
                        data_v4l_n2 = None

                    if is_empty(data_v4l_n1) and is_empty(data_v4l_n2):
                        data_i["VIKING_V4L_Ni"] = data_v4l_ni_empty
                    else:
                        data_i["VIKING_V4L_Ni"] = {
                            "N1_PROBE": data_v4l_n1,
                            "N2_PROBE": data_v4l_n2,
                        }

                # Reading Viking V4L DFT/WF data in the current record
                data_v4l_dft_wh_bytes = 16384
                data_v4l_dft_wh_floats = data_v4l_dft_wh_bytes // 4

                block = self.file.read(data_v4l_dft_wh_bytes)
                data_v4l_dft_wf = struct.unpack(
                    ">" + "f" * data_v4l_dft_wh_floats, block
                )

                if is_empty(header3_i):

                    data_i["VIKING_V4L_DFT"] = data_v4l_dft_empty
                    data_i["VIKING_V4L_WF"] = data_v4l_wf_empty

                else:

                    cur_index = 0

                    if header3_i["V4L_TM_MODE"] == 0:

                        data_v4l_wf = data_v4l_wf_empty

                        if header3_i["V4L_NUMBER_OF_DFT_SPECTRA"] != 0:
                            print("Erroneous V4L_TM_MODE...")

                        data_v4l_wf["WF1"] = list()
                        data_v4l_wf["WF2"] = list()

                        n_wf = header3_i["V4L_NUMBER_OF_SERIES_PER_WF_CHANNEL"]
                        l_wf = header3_i["V4L_NUMBER_OF_SAMPLES_PER_WF_CHANNEL"] // n_wf

                        for i in range(n_wf):
                            data_v4l_wf["WF1"].append(
                                data_v4l_dft_wf[cur_index : cur_index + l_wf]
                            )
                            cur_index = cur_index + l_wf

                        for i in range(n_wf):
                            data_v4l_wf["WF2"].append(
                                data_v4l_dft_wf[cur_index : cur_index + l_wf]
                            )
                            cur_index = cur_index + l_wf

                        data_i["VIKING_V4L_WF"] = data_v4l_wf
                        data_i["VIKING_V4L_DFT"] = data_v4l_dft_empty

                    elif header3_i["V4L_TM_MODE"] == 1 or header3_i["V4L_TM_MODE"] == 3:

                        data_v4l_dft = data_v4l_dft_empty
                        data_v4l_dft["DFT"] = list()
                        data_v4l_wf = data_v4l_wf_empty
                        data_v4l_wf["WF1"] = list()
                        data_v4l_wf["WF2"] = list()

                        n_dft = header3_i["V4L_NUMBER_OF_DFT_SPECTRA"]
                        l_dft = header3_i["V4L_NUMBER_OF_DFT_SAMPLES"] // n_dft

                        n_wf = header3_i["V4L_NUMBER_OF_SERIES_PER_WF_CHANNEL"]
                        l_wf = header3_i["V4L_NUMBER_OF_SAMPLES_PER_WF_CHANNEL"] // n_wf

                        for i in range(n_dft):
                            data_v4l_dft["DFT"].append(
                                data_v4l_dft_wf[cur_index : cur_index + l_dft]
                            )
                            cur_index = cur_index + l_dft

                        for i in range(n_wf):
                            data_v4l_wf["WF1"].append(
                                data_v4l_dft_wf[cur_index : cur_index + l_wf]
                            )
                            cur_index = cur_index + l_wf

                        for i in range(n_wf):
                            data_v4l_wf["WF2"].append(
                                data_v4l_dft_wf[cur_index : cur_index + l_wf]
                            )
                            cur_index = cur_index + l_wf

                        data_i["VIKING_V4L_DFT"] = data_v4l_dft
                        data_i["VIKING_V4L_WF"] = data_v4l_wf

                    elif header3_i["V4L_TM_MODE"] == 2:

                        data_v4l_dft = data_v4l_dft_empty
                        data_v4l_dft["DFT"] = list()

                        n_dft = header3_i["V4L_NUMBER_OF_DFT_SPECTRA"]
                        l_dft = int(header3_i["V4L_NUMBER_OF_DFT_SAMPLES"] / n_dft)

                        for i in range(n_dft):
                            data_v4l_dft["DFT"].append(
                                data_v4l_dft_wf[cur_index : cur_index + l_dft]
                            )
                            cur_index = cur_index + l_dft

                        data_i["VIKING_V4L_DFT"] = data_v4l_dft
                        data_i["VIKING_V4L_WF"] = data_v4l_wf_empty

                    else:
                        print("Erroneous V4L_TM_MODE selector...")

                read_index_stop = self.file.tell()
                if read_index_stop - read_index_start != 28672:
                    print("First byte of current record: {}".format(read_index_start))
                    print("Last byte of current record: {}".format(read_index_stop))
                    print(
                        "Number of bytes read for current record: {}".format(
                            read_index_stop - read_index_start
                        )
                    )
                    raise Exception("Wrong record length.")
            #                if read_index_stop == os.stat(file_path).st_size:
            #                    raise EOFError

            except EOFError:
                print("End of file reached")
                break

            else:

                nsweep += 1
                yield (header1_i, header2_i, header3_i), status_i, orbit_i, data_i
