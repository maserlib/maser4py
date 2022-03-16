# -*- coding: utf-8 -*-
from pathlib import Path
import pytest
import requests

__all__ = ["load_test_data"]

# remote test data url
DATA_REPO_URL = "http://maser.obspm.fr/data/maser4py/tests/data"

# directory containing local test data
ROOT_DATA_DIRECTORY = Path(__file__).parent / "data"

# test data sample
DATA_FILES = {
    "cdpp": {
        "demeter": [
            (
                "DMT_N1_1134_018401_20041105_235807_20041106_003155.DAT",
                "cdpp_dmt_n1_1134",
            ),
        ],
        "interball": [
            ("POLR_RSPN2_19971116", "cdpp_int_aur_polrad_rspn2"),
            ("POLR_RSPN2_19990126", "cdpp_int_aur_polrad_rspn2"),
        ],
        "isee3": [("SBH_ISEE3_19780820", "cdpp_isee3_sbh")],
        "viking": [
            ("V4N_0101_003", "cdpp_viking_v4n_e5"),
        ],
        "wind": [
            ("wi_wa_rad1_l2_60s_19941114_v01.dat", "cdpp_wi_wa_rad1_l2_60s_v2"),
            ("wi_wa_rad1_l2_19941110_v01.dat", "cdpp_wi_wa_rad1_l2"),
            ("wi_wa_rad2_l2_60s_19941114_v01.dat", "cdpp_wi_wa_rad2_l2_60s_v2"),
            ("wi_wa_tnr_l2_60s_19941114_v01.dat", "cdpp_wi_wa_tnr_l2_60s_v2"),
            ("WI_WA_TNR_L3_BQT_19941114_1MN.DAT", "cdpp_wi_wa_tnr_l3_bqt_1mn"),
            ("WI_WA_TNR_L3_NN_19941114_V02.DAT", "cdpp_wi_wa_tnr_l3_nn"),
            ("WIN_RAD1_60S_19941114.B3E", "cdpp_wi_wa_rad1_l2_60s_v1"),
            ("WIN_RAD2_60S_19941114.B3E", "cdpp_wi_wa_rad2_l2_60s_v1"),
            ("WIN_TNR_60S_19941114.B3E", "cdpp_wi_wa_tnr_l2_60s_v1"),
        ],
    },
    "e-callisto": {
        "BIR": [
            ("BIR_20220130_111500_01.fit", "ecallisto"),
        ],
    },
    "isee3": {
        "tlm_uiowa": [
            ("telm_2014-08-09T22_uiframe.bin", "uiowa_isee3_raw"),
            ("telm_2014-08-09T23_uiframe.bin", "uiowa_isee3_raw"),
        ],
    },
    "kronos": {
        "2012_091_180/n1": [
            ("R2012180.20", "co_rpws_hfr_kronos_n1"),
            ("R2012180.21", "co_rpws_hfr_kronos_n1"),
            ("R2012180.22", "co_rpws_hfr_kronos_n1"),
        ],
        "2012_091_180/n2": [
            ("P2012180.20", "co_rpws_hfr_kronos_n2"),
            ("P2012180.21", "co_rpws_hfr_kronos_n2"),
            ("P2012180.22", "co_rpws_hfr_kronos_n2"),
        ],
        "2012_181_270/k": [
            ("K2012181.00", "co_rpws_hfr_kronos_n0"),
            ("K2012181.01", "co_rpws_hfr_kronos_n0"),
            ("K2012181.02", "co_rpws_hfr_kronos_n0"),
            ("K2012181.03", "co_rpws_hfr_kronos_n0"),
            ("K2012181.04", "co_rpws_hfr_kronos_n0"),
            ("K2012181.05", "co_rpws_hfr_kronos_n0"),
            ("K2012181.06", "co_rpws_hfr_kronos_n0"),
            ("K2012181.07", "co_rpws_hfr_kronos_n0"),
            ("K2012181.08", "co_rpws_hfr_kronos_n0"),
            ("K2012181.09", "co_rpws_hfr_kronos_n0"),
            ("K2012181.10", "co_rpws_hfr_kronos_n0"),
            ("K2012181.11", "co_rpws_hfr_kronos_n0"),
            ("K2012181.12", "co_rpws_hfr_kronos_n0"),
            ("K2012181.13", "co_rpws_hfr_kronos_n0"),
            ("K2012181.14", "co_rpws_hfr_kronos_n0"),
            ("K2012181.15", "co_rpws_hfr_kronos_n0"),
            ("K2012181.16", "co_rpws_hfr_kronos_n0"),
            ("K2012181.17", "co_rpws_hfr_kronos_n0"),
            ("K2012181.18", "co_rpws_hfr_kronos_n0"),
            ("K2012181.19", "co_rpws_hfr_kronos_n0"),
            ("K2012181.20", "co_rpws_hfr_kronos_n0"),
            ("K2012181.21", "co_rpws_hfr_kronos_n0"),
            ("K2012181.22", "co_rpws_hfr_kronos_n0"),
            ("K2012181.23", "co_rpws_hfr_kronos_n0"),
        ],
        "2012_181_270/n1": [
            ("R2012181.00", "co_rpws_hfr_kronos_n1"),
            ("R2012181.01", "co_rpws_hfr_kronos_n1"),
            ("R2012181.02", "co_rpws_hfr_kronos_n1"),
            ("R2012181.03", "co_rpws_hfr_kronos_n1"),
            ("R2012181.04", "co_rpws_hfr_kronos_n1"),
            ("R2012181.05", "co_rpws_hfr_kronos_n1"),
            ("R2012181.06", "co_rpws_hfr_kronos_n1"),
            ("R2012181.07", "co_rpws_hfr_kronos_n1"),
            ("R2012181.08", "co_rpws_hfr_kronos_n1"),
            ("R2012181.09", "co_rpws_hfr_kronos_n1"),
            ("R2012181.10", "co_rpws_hfr_kronos_n1"),
            ("R2012181.11", "co_rpws_hfr_kronos_n1"),
            ("R2012181.12", "co_rpws_hfr_kronos_n1"),
            ("R2012181.13", "co_rpws_hfr_kronos_n1"),
            ("R2012181.14", "co_rpws_hfr_kronos_n1"),
            ("R2012181.15", "co_rpws_hfr_kronos_n1"),
            ("R2012181.16", "co_rpws_hfr_kronos_n1"),
            ("R2012181.17", "co_rpws_hfr_kronos_n1"),
            ("R2012181.18", "co_rpws_hfr_kronos_n1"),
            ("R2012181.19", "co_rpws_hfr_kronos_n1"),
            ("R2012181.20", "co_rpws_hfr_kronos_n1"),
            ("R2012181.21", "co_rpws_hfr_kronos_n1"),
            ("R2012181.22", "co_rpws_hfr_kronos_n1"),
            ("R2012181.23", "co_rpws_hfr_kronos_n1"),
        ],
        "2012_181_270/n2": [
            ("P2012181.00", "co_rpws_hfr_kronos_n2"),
            ("P2012181.01", "co_rpws_hfr_kronos_n2"),
            ("P2012181.02", "co_rpws_hfr_kronos_n2"),
            ("P2012181.03", "co_rpws_hfr_kronos_n2"),
            ("P2012181.04", "co_rpws_hfr_kronos_n2"),
            ("P2012181.05", "co_rpws_hfr_kronos_n2"),
            ("P2012181.06", "co_rpws_hfr_kronos_n2"),
            ("P2012181.07", "co_rpws_hfr_kronos_n2"),
            ("P2012181.08", "co_rpws_hfr_kronos_n2"),
            ("P2012181.09", "co_rpws_hfr_kronos_n2"),
            ("P2012181.10", "co_rpws_hfr_kronos_n2"),
            ("P2012181.11", "co_rpws_hfr_kronos_n2"),
            ("P2012181.12", "co_rpws_hfr_kronos_n2"),
            ("P2012181.13", "co_rpws_hfr_kronos_n2"),
            ("P2012181.14", "co_rpws_hfr_kronos_n2"),
            ("P2012181.15", "co_rpws_hfr_kronos_n2"),
            ("P2012181.16", "co_rpws_hfr_kronos_n2"),
            ("P2012181.17", "co_rpws_hfr_kronos_n2"),
            ("P2012181.18", "co_rpws_hfr_kronos_n2"),
            ("P2012181.19", "co_rpws_hfr_kronos_n2"),
            ("P2012181.20", "co_rpws_hfr_kronos_n2"),
            ("P2012181.21", "co_rpws_hfr_kronos_n2"),
            ("P2012181.22", "co_rpws_hfr_kronos_n2"),
            ("P2012181.23", "co_rpws_hfr_kronos_n2"),
        ],
        "2012_181_270/n3b": [
            ("N3b_dsq2012181.00", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.01", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.02", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.03", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.04", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.05", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.06", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.07", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.08", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.09", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.10", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.11", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.12", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.13", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.14", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.15", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.16", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.17", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.18", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.19", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.20", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.21", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.22", "co_rpws_hfr_kronos_n3b_dsq"),
            ("N3b_dsq2012181.23", "co_rpws_hfr_kronos_n3b_dsq"),
        ],
        "2012_181_270/n3c": [
            ("N3c_dsq2012181.00", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.01", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.02", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.03", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.04", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.05", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.06", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.07", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.08", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.09", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.10", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.11", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.12", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.13", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.14", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.15", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.16", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.17", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.18", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.19", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.20", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.21", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.22", "co_rpws_hfr_kronos_n3c_dsq"),
            ("N3c_dsq2012181.23", "co_rpws_hfr_kronos_n3c_dsq"),
        ],
        "2012_181_270/n3d": [
            ("N3d_dsq2012181.00", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.01", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.02", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.03", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.04", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.05", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.06", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.07", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.08", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.09", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.10", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.11", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.12", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.13", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.14", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.15", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.16", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.17", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.18", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.19", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.20", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.21", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.22", "co_rpws_hfr_kronos_n3d_dsq"),
            ("N3d_dsq2012181.23", "co_rpws_hfr_kronos_n3d_dsq"),
        ],
        "2012_181_270/n3e": [
            ("N3e_dsq2012181.00", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.01", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.02", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.03", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.04", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.05", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.06", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.07", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.08", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.09", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.10", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.11", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.12", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.13", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.14", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.15", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.16", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.17", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.18", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.19", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.20", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.21", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.22", "co_rpws_hfr_kronos_n3e_dsq"),
            ("N3e_dsq2012181.23", "co_rpws_hfr_kronos_n3e_dsq"),
        ],
    },
    "nda": {
        "routine": [
            ("J160131.RT1", "srn_nda_routine_jup_raw"),
            (
                "srn_nda_routine_jup_edr_201601302247_201601310645_V12.cdf",
                "srn_nda_routine_jup_edr",
            ),
        ],
        "newroutine": [
            ("J20170101_022612_Rou.dat", "srn_nda_newroutine_dat"),
        ],
        "junon": [
            ("20180223_034242_extract1.dat", "srn_nda_junon_dat"),
        ],
        "mefisto": [
            ("S20130118_155927_20130118_160030_Spectro.dat", "srn_nda_mefisto_dat"),
        ],
    },
    "nenufar": {
        "bst/20190930_110700_20190930_111300_SUN_TRACKING": [
            ("20190930_110700_BST.fits", "srn_nenufar_bst"),
        ],
        "bst/20220130_112900_20220130_123100_SUN_TRACKING": [
            ("20220130_112900_BST.fits", "srn_nenufar_bst"),
        ],
    },
    "radiojove": {
        "sps": [
            ("161210000000.sps", "radiojove_sps"),
        ],
    },
    "pds": {
        "VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1": [
            ("PRA_I.LBL", "VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1.0", "PRA_I.TAB"),
        ],
        "VG1-J-PRA-4-SUMM-BROWSE-48SEC-V1": [
            (
                "T790306.LBL",
                "VG1-J-PRA-4-SUMM-BROWSE-48SEC-V1.0",
                "T790306.DAT",
                "PRADATA.FMT",
            ),
        ],
        "VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1": [
            ("PRA.LBL", "VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1.0", "PRA.TAB"),
        ],
        "VG2-N-PRA-2-RDR-HIGHRATE-60MS-V1": [
            ("C1065111.LBL", "VG2-N-PRA-2-RDR-HIGHRATE-60MS-V1.0", "C1065111.DAT"),
        ],
        "VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1": [
            (
                "VG2_NEP_PRA_6SEC.LBL",
                "VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1.0",
                "VG2_NEP_PRA_6SEC.TAB",
            ),
        ],
        "CO-V_E_J_S_SS-RPWS-2-REFDR-WBRFULL-V1": [
            (
                "T2000366_09_8025KHZ4_WBRFR.LBL",
                "CO-V/E/J/S/SS-RPWS-2-REFDR-WBRFULL-V1.0",
                "T2000366_09_8025KHZ4_WBRFR.DAT",
                "RPWS_SCLK_SCET.FMT",
                "RPWS_WBR_WFR_ROW_PREFIX.FMT",
            ),
        ],
        "CO-V_E_J_S_SS-RPWS-3-RDR-LRFULL-V1": [
            (
                "T2000366_HFR0.LBL",
                "CO-V/E/J/S/SS-RPWS-3-RDR-LRFULL-V1.0",
                "T2000366_HFR0.DAT",
                "RPWS_SCLK_SCET.FMT",
                "LRFULL_TABLE.FMT",
                "LRFC_DATA_QUALITY.FMT",
            ),
        ],
    },
}


def download_file(url: str, filepath: Path, chunk_size=8192):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
    return filepath


def test_filepaths():
    filepaths = []
    for database_name in DATA_FILES.keys():
        cur_db_name = Path(ROOT_DATA_DIRECTORY) / database_name
        for dataset_name in DATA_FILES[database_name].keys():
            cur_dir_name = cur_db_name / dataset_name
            for file_data in DATA_FILES[database_name][dataset_name]:
                file_name, file_dataset = file_data[0:2]
                filepaths.append((cur_dir_name / file_name, file_dataset))
    return filepaths


def download_data_sample(database_name: str, reload: bool = False):
    try:
        files = DATA_FILES[database_name]
    except KeyError as err:
        raise KeyError(
            f"database '{database_name}' is not in the test data sample"
        ) from err

    # set up local directory variable, and create directory if necessary
    test_data_path = Path(ROOT_DATA_DIRECTORY) / database_name
    test_data_url_path = f"{DATA_REPO_URL}/{database_name}"
    test_data_path.mkdir(exist_ok=True)

    # loop on subdirs and fix directory separator, depending on local platform:
    for cur_dir, file_items in files.items():

        # local path of current sub-directory (fix path separator for non unix os)
        cur_local_path = test_data_path / Path(cur_dir)

        # URL of current sub-directory
        cur_url_path = f"{test_data_url_path}/{cur_dir}"

        # create cur_local_path if it doesn't exist:
        if not cur_local_path.exists():
            cur_local_path.mkdir(parents=True)

        # loop on files to be downloaded
        for cur_file in file_items:

            # local path to file
            cur_file_path = cur_local_path / cur_file[0]

            # download is file doesn't exist or reload=True
            if not cur_file_path.exists() or reload:
                download_url = f"{cur_url_path}/{cur_file}"
                print(f"Trying to download URL: {download_url}")
                print(f"into: {cur_file_path}")
                download_file(download_url, cur_file_path)
                print("Done.\n")


def check_pytest_marker(test_item_list, *, marker):
    return any([item.get_closest_marker(marker) for item in test_item_list])


@pytest.fixture(scope="session", autouse=True)
def load_test_data(request, pytestconfig):
    """Load test data for Maser4py.maser.data tests suite

    Use 'pytest -m "not test_data_required"' to skip tests that require test data (and to skip auto download).

    Args:
        database_name (str, optional): name of the database to be tested (cdpp, kronos, pds...). Defaults to 'all'.
        reload (bool, optional): set to True to reload data. Defaults to False.
    """
    # skip download if no tests are marked with the 'test_data_required' marker
    if not check_pytest_marker(request.session.items, marker="test_data_required"):
        print("Skipping test data download")
        return

    # loop on test_data_files first level entries
    for database in DATA_FILES:
        download_data_sample(database, reload=False)
