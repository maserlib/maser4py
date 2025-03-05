# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Union
from maser.data.base import BinData, CdfData

# from astropy.units import Quantity, Unit
from astropy.time import Time
import numpy as np
import struct


class RadioJoveSpsSweeps:
    pass


class RadioJoveSpxData(BinData, dataset="radiojove_spx"):  # type: ignore
    def extract_radiojove_spx_header(self):
        """
        Extracts fixed length header keywords from Raw data
        :param self:
        :return header: a dictionary containing the decoded header
        """

        if self.verbose:
            print("### [load_radiojove_spx_header]")

        hdr_raw = self.file_info["prim_hdr_raw"]

        hdr_fmt = "<10s6d1h10s20s20s40s1h1i"  # header format to unpack header
        hdr_values = struct.unpack(hdr_fmt, hdr_raw[0:156])

        header = dict(sft=hdr_values[0].decode("ascii"))
        # date conversion: header dates are given in decimal days since 30/12/1899 00:00 (early morning!) == day 0.0
        # date values must be corrected by adding 2415018.5 = julian date 30/12/1899 00:00
        header["start_jdtime"] = hdr_values[1] + 2415018.5
        header["start_time"] = Time(header["start_jdtime"], format="jd").datetime
        header["stop_jdtime"] = hdr_values[2] + 2415018.5
        header["stop_time"] = Time(header["stop_jdtime"], format="jd").datetime
        header["latitude"] = hdr_values[3]
        header["longitude"] = hdr_values[4]
        header["chartmax"] = hdr_values[5]
        header["chartmin"] = hdr_values[6]
        header["timezone"] = hdr_values[7]
        # For the next 4 header keywords, we remove leading and trailing null (0x00) and space characters
        header["source"] = (hdr_values[8].decode("ascii").strip("\x00")).strip(" ")
        header["author"] = (hdr_values[9].decode("ascii").strip("\x00")).strip(" ")
        header["obsname"] = (hdr_values[10].decode("ascii").strip("\x00")).strip(" ")
        header["obsloc"] = (hdr_values[11].decode("ascii").strip("\x00")).strip(" ")
        header["nchannels"] = hdr_values[12]
        header["note_length"] = hdr_values[13]
        return header

    def extract_radiojove_sps_notes(self):
        """
        Extracts the extended header information (notes) for SPS files (spectrograph)
        :param self:
        :return notes: dictionary containing the extracted header notes
        """
        if self.verbose:
            print("### [extract_radiojove_sps_notes]")

        raw_notes = self.file_info["notes_raw"]
        notes = dict()

        # The header notes are composed of a series of key and value (KV) pairs.
        # The raw notes start with a free text space.
        # The KV pairs section are starting *[[* and finishes with *]]*.
        # The delimiter between each KV pair is 0xFF.
        # There is no predefined character for separating key and value within a KV pair.
        # We must then identify the keys. Some keys have multiple values.
        # More info: http://www.radiosky.com/skypipehelp/V2/datastructure.html

        # List of known metadata keys
        key_list = [
            "SWEEPS",
            "LOWF",
            "HIF",
            "STEPS",
            "RCVR",
            "DUALSPECFILE",
            "COLORRES",
            "BANNER",
            "ANTENNATYPE",
            "ANTENNAORIENTATION",
            "COLORFILE",
            "COLOROFFSET",
            "COLORGAIN",
            "CORRECTIONFILENAME",
            "CAXF",
            "CAX1",
            "CAX2",
            "CLOCKMSG",
        ]
        # CHECK LIST WITH https://voparis-confluence.obspm.fr/display/JOVE/RadioSky+Spectrograph-SPS+Metadata

        # list of metadata keys with multiple values
        key_list_multi = [
            "BANNER",
            "COLOROFFSET",
            "COLORGAIN",
            "CAXF",
            "CAX1",
            "CAX2",
            "CLOCKMSG",
        ]

        # list of metadata keys with integer values
        key_list_int = ["SWEEPS", "STEPS", "RCVR", "COLORRES", "COLOROFFSET"]

        # list of metadata keys with floating point values
        key_list_float = ["LOWF", "HIF", "COLORGAIN"]

        # stripping raw note text stream from "*[[*" and "*]]*" delimiters, and splitting with '\xff'
        start_index = raw_notes.find(b"*[[*")
        stop_index = raw_notes.find(b"*]]*")
        notes["free_text"] = raw_notes[0:start_index].decode("ascii")
        note_list = []
        cur_note = b""
        for bb in raw_notes[start_index + 4 : stop_index]:
            if bb == 255:
                note_list.append(cur_note)
                cur_note = b""
            else:
                cur_note = b"".join([cur_note, struct.pack("B", bb)])

        # Looping on note items to identify what keys are present
        for item in note_list:

            note_item = item.decode("ascii")

            if self.debug:
                print("Current Item = {}".format(note_item))

            # looping on known key items
            for key_item in key_list:

                # getting length of key name
                key_len = len(key_item)

                # checking if current note item contains current key item
                if note_item[0:key_len] == key_item:

                    if self.debug:
                        print("Detected Key = {}".format(key_item))

                    # if current key item has multiple values, do this
                    if key_item in key_list_multi:

                        # if current key item has multiple values, initializing a list for the values
                        if key_item not in notes.keys():
                            notes[key_item] = []

                            # checking specific cases
                        if key_item[0:3] == "CAX":
                            note_item = note_item.split("|")
                            note_index = int(note_item[0][key_len:])
                            note_value = note_item[1]
                        elif key_item[0:8] == "CLOCKMSG":
                            note_item = note_item.split(" ")
                            note_index = int(note_item[0][key_len:])
                            note_value = " ".join(note_item[1:])
                        else:
                            note_index = int(note_item[key_len : key_len + 1])
                            note_value = note_item[key_len + 1 :]
                        if self.debug:
                            print("Index = {}".format(note_index))
                            print("Value = {}".format(note_value))

                        # adding value to note item
                        if key_item in key_list_int:
                            notes[key_item].append(int(note_value.strip()))
                        elif key_item in key_list_float:
                            notes[key_item].append(float(note_value.strip()))
                        else:
                            notes[key_item].append(note_value)

                    else:

                        # key has single value, extracting the value (no delimiter)
                        note_value = note_item[key_len:]

                        # special case for RCVR, empty value should be value -1
                        if key_item == "RCVR":
                            if note_value == "":
                                note_value = "-1"

                        if self.debug:
                            print("Value = {}".format(note_value))

                        # loop on keys that have numeric values
                        if key_item in key_list_int:
                            notes[key_item] = int(note_value.strip())
                        elif key_item in key_list_float:
                            notes[key_item] = float(note_value.strip())
                        else:
                            notes[key_item] = note_value

        # final special case: if not present this keyword (no value) says that we deal with single channel spectrograph data
        if "DUALSPECFILE" not in notes.keys():
            notes["DUALSPECFILE"] = False
        else:
            if notes["DUALSPECFILE"].strip() == "True":
                notes["DUALSPECFILE"] = True

        return notes

    def extract_radiojove_spd_notes(self):
        """
        Extracts the extended header information (notes) for SPD files (radiojove kits)
        :param self:
        :return notes: dictionary containing the extracted header notes
        """

        # The header notes are composed of a series of key and value (KV) pairs.
        # The raw notes start with a free text space.
        # The KV pairs section are starting *[[* and finishes with *]]*.
        # The delimiter between each KV pair is 0xFF.
        # There is no predefined character for separating key and value within a KV pair.
        # We must then identify the keys. Some keys have multiple values.
        # More info: http://www.radiosky.com/skypipehelp/V2/datastructure.html

        if self.verbose:
            print("### [extract_radiojove_spd_notes]")

        raw_notes = self.file_info["notes_raw"]

        # initializing notes with 3 sub dictionaries.
        notes = dict(CHL={}, CHO={}, MetaData={})

        start_index = raw_notes.find("*[[*")
        stop_index = raw_notes.find("*]]*")
        notes["free_text"] = raw_notes[0:start_index]
        note_list = raw_notes[start_index + 4 : stop_index].split("\xff")
        for note_item in note_list:

            if note_item == "Logged Using UT":
                notes["Logged Using UT"] = True
            else:
                notes["Logged Using UT"] = False

            if note_item == "No Time Stamps":
                notes["No Time Stamps"] = True
            else:
                notes["No Time Stamps"] = False

            if note_item[0:3] == "CHL":
                notes["CHL"][int(note_item[3])] = note_item[4:]

            if note_item[0:3] == "CHO":
                notes["CHO"][int(note_item[3])] = note_item[4:]

            if note_item == "Integer Save":
                notes["Integer Save"] = True
            else:
                notes["Integer Save"] = False

            if note_item[0:7] == "XALABEL":
                notes["XALABEL"] = note_item[7:]

            if note_item[0:7] == "YALABEL":
                notes["YALABEL"] = note_item[7:]

            # extra metadata are present with a generic syntax Metadata_[KEY][0xC8][VALUE]
            if note_item[0:9] == "MetaData_":
                item_metadata = note_item.split("\xc8")
                # removing any extra trailing character in key name (spaces or colon)
                notes["MetaData"][
                    item_metadata[0][9:].strip(" ").strip(":").strip(" ")
                ] = item_metadata[1]

        return notes

    def open_radiojove_spx(self):
        """
        Opens RadioJOVE SPS or SPD file for processing
        :return header, notes, time, frequency:
        """
        if self.verbose:
            print("### [open_radiojove_spx]")

        # Opening file:
        self.file_info["prim_hdr_length"] = 156
        self.file_info["lun"] = open(self.file_info["name"], "rb")

        # Reading header:
        self.file_info["prim_hdr_raw"] = self.file_info["lun"].read(
            self.file_info["prim_hdr_length"]
        )
        header = self.extract_radiojove_spx_header()
        header["file_name"] = self.file_info["name"]
        header["file_type"] = self.file_info["name"][-3:].upper()

        # Reading notes:
        self.file_info["notes_raw"] = self.file_info["lun"].read(header["note_length"])
        if header["file_type"] == "SPS":
            notes = self.extract_radiojove_sps_notes()
        elif header["file_type"] == "SPD":
            notes = self.extract_radiojove_spd_notes()
            header["nfreq"] = 1
        else:
            notes = ""

        if header["obsname"] == "AJ4CO DPS":
            header["obsty_id"] = "AJ4CO"
            header["instr_id"] = "DPS"
            header["gain0"] = notes["COLORGAIN"][0]
            header["gain1"] = notes["COLORGAIN"][1]
            header["offset0"] = notes["COLOROFFSET"][0]
            header["offset1"] = notes["COLOROFFSET"][1]
            header["banner0"] = notes["BANNER"][0].replace(
                "<DATE>", header["start_time"].date().isoformat()
            )
            header["banner1"] = notes["BANNER"][1].replace(
                "<DATE>", header["start_time"].date().isoformat()
            )
            header["antenna_type"] = notes["ANTENNATYPE"]
            header["color_file"] = notes["COLORFILE"]
            header["free_text"] = notes["free_text"]
        else:
            header["obsty_id"] = "ABCDE"
            header["instr_id"] = "XXX"
            header["gain0"] = 2.00
            header["gain1"] = 2.00
            header["offset0"] = 2000
            header["offset1"] = 2000
            header["banner0"] = ""
            header["banner1"] = ""
            header["antenna_type"] = ""
            header["color_file"] = ""
            header["free_text"] = ""

        if header["file_type"] == "SPS":
            header["level"] = "EDR"
        if header["file_type"] == "SPD":
            header["level"] = "DDR"

        if self.debug:
            print(header)
            print(notes)

        # Reading data:

        self.file_info["data_length"] = (
            self.file_info["size"]
            - self.file_info["prim_hdr_length"]
            - header["note_length"]
        )

        # nfeed = number of observation feeds
        # nfreq = number of frequency step (1 for SPD)
        # nstep = number of sweep (SPS) or time steps (SPD)

        # SPS files
        header["feeds"] = []

        feed_tmp = {
            "RR": {
                "FIELDNAM": "RR",
                "CATDESC": "RCP Flux Density",
                "LABLAXIS": "RCP Power Spectral Density",
            },
            "LL": {
                "FIELDNAM": "LL",
                "CATDESC": "LCP Flux Density",
                "LABLAXIS": "LCP Power Spectral Density",
            },
            "S": {
                "FIELDNAM": "S",
                "CATDESC": "Flux Density",
                "LABLAXIS": "Power Spectral Density",
            },
        }

        if header["file_type"] == "SPS":
            header["nfreq"] = header["nchannels"]
            if notes["DUALSPECFILE"]:

                header["nfeed"] = 2

                if "banner0" in header.keys():

                    if "RCP" in header["banner0"]:
                        header["polar0"] = "RR"
                    elif "LCP" in header["banner0"]:
                        header["polar0"] = "LL"

                    else:
                        header["polar0"] = "S"

                    if "RCP" in header["banner1"]:
                        header["polar1"] = "RR"
                    elif "LCP" in header["banner1"]:
                        header["polar1"] = "LL"
                    else:
                        header["polar1"] = "S"

                else:

                    header["polar0"] = "S"
                    header["polar1"] = "S"

                header["feeds"].append(feed_tmp[header["polar0"]])
                header["feeds"].append(feed_tmp[header["polar1"]])

            else:

                header["nfeed"] = 1

                if "banner0" in header.keys():

                    if "RCP" in header["banner0"]:
                        header["polar0"] = "RR"
                    elif "LCP" in header["banner0"]:
                        header["polar0"] = "RR"
                    else:
                        header["polar0"] = "S"

                else:

                    header["polar0"] = "S"

                header["feeds"].append(feed_tmp[header["polar0"]])

            self.file_info["bytes_per_step"] = (
                header["nfreq"] * header["nfeed"] + 1
            ) * 2
            self.file_info["data_format"] = ">{}H".format(
                self.file_info["bytes_per_step"] // 2
            )

            header["fmin"] = float(notes["LOWF"]) / 1.0e6  # MHz
            header["fmax"] = float(notes["HIF"]) / 1.0e6  # MHz
            frequency = [
                header["fmax"]
                - float(ifreq)
                / (header["nfreq"] - 1)
                * (header["fmax"] - header["fmin"])
                for ifreq in range(header["nfreq"])
            ]

        # SPD files

        elif header["file_type"] == "SPD":
            header["nfreq"] = 1
            header["nfeed"] = header["nchannels"]
            for i in range(header["nchannels"]):
                header["feeds"][i] = {}
                header["feeds"][i]["FIELDNAM"] = "CH{:02d}".format(i)
                header["feeds"][i]["CATDESC"] = "CH{:02d} Flux Density".format(i)
                header["feeds"][i]["LABLAXIS"] = "CH{:02d} Flux Density".format(i)

            if notes["INTEGER_SAVE_FLAG"]:
                self.file_info["bytes_per_step"] = 2
                self.file_info["data_format"] = "{}h".format(header["nfeed"])
            else:
                self.file_info["nbytes_per_sample"] = 8
                self.file_info["data_format"] = "{}d".format(header["nfeed"])

            if notes["NO_TIME_STAMPS_FLAG"]:
                self.file_info["bytes_per_step"] = (
                    header["nfeed"] * self.file_info["nbytes_per_sample"]
                )
                self.file_info["data_format"] = "<{}".format(
                    self.file_info["data_format"]
                )
            else:
                self.file_info["bytes_per_step"] = (
                    header["nfeed"] * self.file_info["nbytes_per_sample"] + 8
                )
                self.file_info["data_format"] = "<1d{}".format(
                    self.file_info["data_format"]
                )

            frequency = 20.1
            header["fmin"] = frequency  # MHz
            header["fmax"] = frequency  # MHz

        else:
            frequency = 0.0

        if header["file_type"] == "SPS":
            header["product_type"] = "sp{}_{}".format(header["nfeed"], header["nfreq"])
            self.file_info["record_data_offset"] = 0
        if header["file_type"] == "SPD":
            header["product_type"] = "ts{}".format(header["nfeed"])
            if notes["NO_TIME_STAMPS_FLAG"]:
                self.file_info["record_data_offset"] = 0
            else:
                self.file_info["record_data_offset"] = 1

        header["nstep"] = (
            self.file_info["data_length"] // self.file_info["bytes_per_step"]
        )

        if header["file_type"] == "SPS":
            time_step = (header["stop_jdtime"] - header["start_jdtime"]) / float(
                header["nstep"]
            )
            time = [
                istep * time_step + header["start_jdtime"]
                for istep in range(header["nstep"])
            ]
        elif header["file_type"] == "SPD":
            # if notes['NO_TIME_STAMPS_FLAG']:
            time_step = (header["stop_jdtime"] - header["start_jdtime"]) / float(
                header["nstep"]
            )
            time = [
                float(istep) * time_step + header["start_jdtime"]
                for istep in range(header["nstep"])
            ]
            # else:
            # time = np.array()
            # for i in range(header['nstep']):
            #     time.append(data_raw[i][0])
            # time_step = np.median(time[1:header['nstep']]-time[0:header['nstep']-1])
        else:
            time = 0.0
            time_step = 0.0

        # transforming times from JD to datetime
        # time = astime.Time(time, format='jd').datetime  # needs some checks
        time = Time(time, format="jd").datetime  # needs some checks

        # time sampling step in seconds
        header["time_step"] = time_step * 86400.0
        header["time_integ"] = header[
            "time_step"
        ]  # this will have to be checked at some point

        if self.debug:
            print("nfeed : {}".format(header["nfeed"]))
            print("nfreq : {} ({})".format(header["nfreq"], len(frequency)))
            print("nstep : {} ({})".format(header["nstep"], len(time)))

        if self.verbose:
            print("nfeed : {}".format(header["nfeed"]))
            print("nfreq : {}".format(header["nfreq"]))
            print("nstep : {}".format(header["nstep"]))

        return header, notes, time, frequency

    def close_radiojove_spx(self):
        """
        Closes the current SPS or SPD input file
        :param self:
        :return:
        """
        if self.verbose:
            print("### [close_radiojove_spx]")

        self.file_info["lun"].close()

    def extract_radiojove_spx_data(self):
        """
        :return:
        """

        packet_size = 0  # Need updates

        if self.verbose:
            print("### [extract_radiojove_spx_data]")

        nstep = self.header["nstep"]  # len(time)
        nfreq = self.header["nfreq"]  # len(freq)
        nfeed = self.header["nfeed"]
        rec_0 = self.file_info["record_data_offset"]

        var_list = [item["FIELDNAM"] for item in self.header["feeds"]]

        # reading sweeps structure
        if self.verbose:
            print(
                "Loading data into {} variable(s), from {}".format(
                    ", ".join(var_list), self.file_info["name"]
                )
            )

        data = dict()
        for var in var_list:
            data[var] = np.empty((nstep, nfreq), dtype=np.short)

        for j in range(0, self.header["nstep"], packet_size):
            j1 = j
            j2 = j + packet_size
            if j2 > nstep:
                j2 = nstep

            if self.verbose:
                if packet_size == 1:
                    print("Loading record #{}".format(j))
                else:
                    print("Loading records #{} to #{}".format(j1, j2))

            data_raw = np.array(self.read_radiojove_spx_sweep(j2 - j1))[
                :, rec_0 : rec_0 + nfreq * nfeed
            ].reshape(j2 - j1, nfreq, nfeed)

            for i in range(nfeed):
                data[var_list[i]][j1:j2, :] = data_raw[:, :, i].reshape(j2 - j1, nfreq)

        return data

    def read_radiojove_spx_sweep(self, read_size):
        """
        Reads raw data from SPS or SPD file
        :param self:
        :param read_size: number of sweep to read
        :return raw:
        """
        if self.verbose:
            print("### [read_radiojove_spx_sweep]")
            print(
                "loading packet of {} sweep(s), with format `{}`.".format(
                    read_size, self.file_info["data_format"]
                )
            )

        raw = []
        for i in range(read_size):
            raw.append(
                struct.unpack(
                    self.file_info["data_format"],
                    self.file_info["lun"].read(self.file_info["bytes_per_step"]),
                )
            )
            if raw[i][-1] != 65278:
                print(
                    "WARNING ! wrong end of sweep delimiter. (Got 0x{:04X} instead of 0x{:04X})".format(
                        raw[i][-1], 65278
                    )
                )

        if self.verbose:
            print("Size of loaded data: {}".format(len(raw)))

        return raw


class RadioJoveSpsData(RadioJoveSpxData, dataset="radiojove_sps"):  # type: ignore
    _iter_sweep_class = RadioJoveSpsSweeps

    def __init__(
        self,
        filepath: Path,
        dataset: Union[None, str] = "__auto__",
        access_mode: str = "sweeps",
    ):
        BinData.__init__(self, filepath, dataset, access_mode)
        self._data = None
        self._nsweep = None
        self._data = self._loader()
        self.fields: list = []
        self.units: list = []

    def _loader(self):
        pass


class RadioJoveCdfData(CdfData, dataset="radiojove_cdf"):  # type: ignore
    pass
