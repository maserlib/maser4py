# -*- coding: utf-8 -*-
from maser.data.base import Data
from pathlib import Path
from .utils import PDSLabelDict


class Pds3Data(Data, dataset="pds3"):
    @classmethod
    def open(cls, filepath: Path):
        label = PDSLabelDict(filepath)
        data = None
        return {"label": label, "data": data}

    @classmethod
    def get_dataset(cls, filepath: Path):
        file_label = cls.open(filepath)["label"]
        dataset = file_label["DATA_SET_ID"]
        return dataset

    @classmethod
    def close(cls, file):
        pass


class Vg1JPra3RdrLowband6secV1Data(
    Pds3Data, dataset="VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    pass


class Vg1JPra4SummBrowse48secV1Data(
    Pds3Data, dataset="VG1-J-PRA-4-SUMM-BROWSE-48SEC-V1.0"
):
    pass


class Vg1SPra3RdrLowband6secV1Data(
    Pds3Data, dataset="VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    pass


class Vg2NPra2RdrHighrate60msV1Data(
    Pds3Data, dataset="VG2-N-PRA-2-RDR-HIGHRATE-60MS-V1.0"
):
    pass


class Vg2NPra3RdrLowband6secV1Data(
    Pds3Data, dataset="VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1.0"
):
    pass


class CoVEJSSSRpws2RefdrWbrFullV1Data(
    Pds3Data, dataset="CO-V/E/J/S/SS-RPWS-2-REFDR-WBRFULL-V1.0"
):
    pass


class CoVEJSSSRpws3RdrLrFullV1Data(
    Pds3Data, dataset="CO-V/E/J/S/SS-RPWS-3-RDR-LRFULL-V1.0"
):
    pass
