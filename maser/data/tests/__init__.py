import os
import urllib.request
from pathlib import Path

# definition of download URL root:
_test_data_root_url = 'http://maser.obspm.fr/data/maser4py/tests/data'

# definition of local test data path (in a "data" direction of this directory):
_test_data_root_local = Path(__file__).parent / 'data'

# data directories and files to be downloaded
_test_data_files = {'cdpp': {'demeter': ['DMT_N1_1134_018401_20041105_235807_20041106_003155.DAT'],
                             'interball': ['POLR_RSPN2_19971116', 'POLR_RSPN2_19990126'],
                             'isee3': ['SBH_ISEE3_19780820'],
                             'viking': ['V4N_0101_003'],
                             'wind': ['WI_WA_TNR_L3_BQT_19941114_1MN.DAT', 'WI_WA_TNR_L3_NN_19941114_V02.DAT',
                                      'WIN_TNR_60S_19941114.B3E'],
                             },
                    'isee3': {'tlm_uiowa': ['telm_2014-08-09T22_uiframe.bin', 'telm_2014-08-09T23_uiframe.bin'],
                              },
                    'kronos': {'2012_091_180/n1': ['R2012180.20', 'R2012180.21', 'R2012180.22'],
                               '2012_091_180/n2': ['P2012180.20', 'P2012180.21', 'P2012180.22'],
                               '2012_181_270/k': ['K2012181.00', 'K2012181.01', 'K2012181.02', 'K2012181.03',
                                                  'K2012181.04', 'K2012181.05', 'K2012181.06', 'K2012181.07',
                                                  'K2012181.08', 'K2012181.09', 'K2012181.10', 'K2012181.11',
                                                  'K2012181.12', 'K2012181.13', 'K2012181.14', 'K2012181.15',
                                                  'K2012181.16', 'K2012181.17', 'K2012181.18', 'K2012181.19',
                                                  'K2012181.20', 'K2012181.21', 'K2012181.22', 'K2012181.23'],
                               '2012_181_270/n1': ['R2012181.00', 'R2012181.01', 'R2012181.02', 'R2012181.03',
                                                  'R2012181.04', 'R2012181.05', 'R2012181.06', 'R2012181.07',
                                                  'R2012181.08', 'R2012181.09', 'R2012181.10', 'R2012181.11',
                                                  'R2012181.12', 'R2012181.13', 'R2012181.14', 'R2012181.15',
                                                  'R2012181.16', 'R2012181.17', 'R2012181.18', 'R2012181.19',
                                                  'R2012181.20', 'R2012181.21', 'R2012181.22', 'R2012181.23'],
                               '2012_181_270/n2': ['P2012181.00', 'P2012181.01', 'P2012181.02', 'P2012181.03',
                                                   'P2012181.04', 'P2012181.05', 'P2012181.06', 'P2012181.07',
                                                   'P2012181.08', 'P2012181.09', 'P2012181.10', 'P2012181.11',
                                                   'P2012181.12', 'P2012181.13', 'P2012181.14', 'P2012181.15',
                                                   'P2012181.16', 'P2012181.17', 'P2012181.18', 'P2012181.19',
                                                   'P2012181.20', 'P2012181.21', 'P2012181.22', 'P2012181.23'],
                               '2012_181_270/n3b': ['N3b_dsq2012181.00', 'N3b_dsq2012181.01', 'N3b_dsq2012181.02',
                                                    'N3b_dsq2012181.03', 'N3b_dsq2012181.04', 'N3b_dsq2012181.05',
                                                    'N3b_dsq2012181.06', 'N3b_dsq2012181.07', 'N3b_dsq2012181.08',
                                                    'N3b_dsq2012181.09', 'N3b_dsq2012181.10', 'N3b_dsq2012181.11',
                                                    'N3b_dsq2012181.12', 'N3b_dsq2012181.13', 'N3b_dsq2012181.14',
                                                    'N3b_dsq2012181.15', 'N3b_dsq2012181.16', 'N3b_dsq2012181.17',
                                                    'N3b_dsq2012181.18', 'N3b_dsq2012181.19', 'N3b_dsq2012181.20',
                                                    'N3b_dsq2012181.21', 'N3b_dsq2012181.22', 'N3b_dsq2012181.23'],
                               '2012_181_270/n3c': ['N3c_dsq2012181.00', 'N3c_dsq2012181.01', 'N3c_dsq2012181.02',
                                                    'N3c_dsq2012181.03', 'N3c_dsq2012181.04', 'N3c_dsq2012181.05',
                                                    'N3c_dsq2012181.06', 'N3c_dsq2012181.07', 'N3c_dsq2012181.08',
                                                    'N3c_dsq2012181.09', 'N3c_dsq2012181.10', 'N3c_dsq2012181.11',
                                                    'N3c_dsq2012181.12', 'N3c_dsq2012181.13', 'N3c_dsq2012181.14',
                                                    'N3c_dsq2012181.15', 'N3c_dsq2012181.16', 'N3c_dsq2012181.17',
                                                    'N3c_dsq2012181.18', 'N3c_dsq2012181.19', 'N3c_dsq2012181.20',
                                                    'N3c_dsq2012181.21', 'N3c_dsq2012181.22', 'N3c_dsq2012181.23'],
                               '2012_181_270/n3d': ['N3d_dsq2012181.00', 'N3d_dsq2012181.01', 'N3d_dsq2012181.02',
                                                    'N3d_dsq2012181.03', 'N3d_dsq2012181.04', 'N3d_dsq2012181.05',
                                                    'N3d_dsq2012181.06', 'N3d_dsq2012181.07', 'N3d_dsq2012181.08',
                                                    'N3d_dsq2012181.09', 'N3d_dsq2012181.10', 'N3d_dsq2012181.11',
                                                    'N3d_dsq2012181.12', 'N3d_dsq2012181.13', 'N3d_dsq2012181.14',
                                                    'N3d_dsq2012181.15', 'N3d_dsq2012181.16', 'N3d_dsq2012181.17',
                                                    'N3d_dsq2012181.18', 'N3d_dsq2012181.19', 'N3d_dsq2012181.20',
                                                    'N3d_dsq2012181.21', 'N3d_dsq2012181.22', 'N3d_dsq2012181.23'],
                               '2012_181_270/n3e': ['N3e_dsq2012181.00', 'N3e_dsq2012181.01', 'N3e_dsq2012181.02',
                                                    'N3e_dsq2012181.03', 'N3e_dsq2012181.04', 'N3e_dsq2012181.05',
                                                    'N3e_dsq2012181.06', 'N3e_dsq2012181.07', 'N3e_dsq2012181.08',
                                                    'N3e_dsq2012181.09', 'N3e_dsq2012181.10', 'N3e_dsq2012181.11',
                                                    'N3e_dsq2012181.12', 'N3e_dsq2012181.13', 'N3e_dsq2012181.14',
                                                    'N3e_dsq2012181.15', 'N3e_dsq2012181.16', 'N3e_dsq2012181.17',
                                                    'N3e_dsq2012181.18', 'N3e_dsq2012181.19', 'N3e_dsq2012181.20',
                                                    'N3e_dsq2012181.21', 'N3e_dsq2012181.22', 'N3e_dsq2012181.23'],
                               },
                    'nda': {'routine': ['J160131.RT1', 'srn_nda_routine_jup_edr_201601302247_201601310645_V12.cdf'],
                            'newroutine': ['J20170101_022612_Rou.dat'],
                            'junon': ['20180223_034242_extract1.dat'],
                            'mefisto': ['S20130118_155927_20130118_160030_Spectro.dat']
                            },
                    'radiojove': {'sps': ['161210000000.sps'],
                                  },
                    'pds': {'VG1-J-PRA-3-RDR-LOWBAND-6SEC-V1': ['PRA_I.TAB','PRA_I.LBL'],
                            'VG1-J-PRA-4-SUMM-BROWSE-48SEC-V1': ['T790306.DAT','T790306.LBL', 'PRADATA.FMT'],
                            'VG1-S-PRA-3-RDR-LOWBAND-6SEC-V1': ['PRA.TAB','PRA.LBL'],
                            'VG2-N-PRA-2-RDR-HIGHRATE-60MS-V1': ['C1065111.LBL', 'C1065111.DAT'],
                            'VG2-N-PRA-3-RDR-LOWBAND-6SEC-V1': ['VG2_NEP_PRA_6SEC.LBL', 'VG2_NEP_PRA_6SEC.TAB'],
                            'CO-V_E_J_S_SS-RPWS-2-REFDR-WBRFULL-V1': ['T2000366_09_8025KHZ4_WBRFR.LBL',
                                                                      'T2000366_09_8025KHZ4_WBRFR.DAT',
                                                                      'RPWS_SCLK_SCET.FMT',
                                                                      'RPWS_WBR_WFR_ROW_PREFIX.FMT'],
                            'CO-V_E_J_S_SS-RPWS-3-RDR-LRFULL-V1': ['T2000366_HFR0.LBL',
                                                                   'T2000366_HFR0.DAT',
                                                                   'RPWS_SCLK_SCET.FMT',
                                                                   'LRFULL_TABLE.FMT',
                                                                   'LRFC_DATA_QUALITY.FMT'],
                            },
                    }


def get_data_directory():
    return _test_data_root_local


def load_test_data(database_name='all', reload=False):
    """
    load test data for Maser4py.maser.data tests suite
    :param database_name: name of the database to be tested (cdpp, kronos, pds...). default to 'all'
    :param reload: set to True to reload data (default to False)
    """

    # loop on test_data_files first level entries
    for database, files in _test_data_files.items():

        # check input database_name to decide on processing this database entry
        if database_name == database or database_name == 'all':

            # set up local directory variable, and create directory if necessary
            test_data_path = Path(_test_data_root_local) / database
            test_data_url_path = '{}/{}'.format(_test_data_root_url, database)
            if not test_data_path.exists():
                test_data_path.mkdir()

            # loop on subdirs and fix directory separator, depending on local platform:
            for cur_dir, file_items in files.items():

                # local path of current sub-directory (fix path separator for non unix os)
                cur_local_path = test_data_path / Path(cur_dir)

                # URL of current sub-directory
                cur_url_path = '{}/{}'.format(test_data_url_path, cur_dir)

                # create cur_local_path if it doesn't exist:
                if not cur_local_path.exists():
                    cur_local_path.mkdir(parents=True)

                # loop on files to be downloaded
                for cur_file in file_items:

                    # local path to file
                    cur_file_path = cur_local_path / cur_file

                    # download is file doesn't exist or reload=True
                    if not cur_file_path.exists() or reload:
                        download_url = '{}/{}'.format(cur_url_path, cur_file)
                        print("Trying to download URL: {}".format(download_url))
                        print("into: {}".format(cur_file_path))
                        urllib.request.urlretrieve(download_url, str(cur_file_path))
                        print("Done.\n")