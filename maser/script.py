#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Main script program for maser4py."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
import sys
import os
import argparse
import logging
from datetime import datetime

from maser.settings import MASER_VERSION
from maser.utils.toolbox import setup_logging
from maser.utils.cdf.serializer import skeletoncdf, skeletontable, \
    add_skeletoncdf_subparser, add_skeletontable_subparser
from maser.utils.cdf.serializer.exceptions import CDFSerializerError
from maser.utils.cdf.cdfcompare import cdf_compare, add_cdfcompare_subparser
from maser.utils.cdf.validator import cdfvalidator, ValidatorException, add_cdfvalidator_subparser
from maser.utils.time import Lstable, add_leapsec_subparser
#from maser.services.helio.hfc import hfcviewer, add_hfcviewer_subparser
from pprint import pformat

# ________________ HEADER _________________________


# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)

INPUT_DATE = '%Y-%m-%dT%H:%M:%S'

# ________________ Class Definition __________
# (If required, define here classes)


# ________________ Global Functions __________
# (If required, define here global functions)
def main():
    """Main program."""
    parser = argparse.ArgumentParser(add_help=True,
                                     description='MASER4PY application')
    parser.add_argument('--version', action='store_true',
                        help='Print MASER4PY version')
    parser.add_argument('-l', '--log-file', nargs=1,
                        default=[None],
                        help='log file path')
    parser.add_argument('-Q', '--quiet',
                        action='store_true',
                        help='Quiet mode')
    parser.add_argument('-D', '--debug',
                        action='store_true',
                        help='Debug mode')

    # Add maser subparsers
    subparsers = parser.add_subparsers(dest='maser',
                                       description='maser sub-commands')

    # Initializing subparsers
    add_skeletoncdf_subparser(subparsers)
    add_skeletontable_subparser(subparsers)
    add_leapsec_subparser(subparsers)
    add_cdfcompare_subparser(subparsers)
    add_cdfvalidator_subparser(subparsers)
#    add_hfcviewer_subparser(subparsers)

    # Parse args
    args = parser.parse_args()

    # Setup the logging
    setup_logging(
        filename=args.log_file[0],
        quiet=args.quiet,
        debug=args.debug,
    )

    if args.version:
        print('This is MASER4PY V{0}'.format(MASER_VERSION))
    elif args.maser is not None:
        # skeletoncdf sub-command
        if 'skeletoncdf' in args.maser:
            skeletons = args.skeletons
            nskt = len(skeletons)
            logger.info('{0} input file(s) found.'.format(nskt))
            # Initializing list of bad conversion encountered
            bad_skt = []
            # Loop over the input skeleton files
            for i, skt in enumerate(skeletons):
                logger.info(
                    'Executing skeletoncdf for {0}... [{1}/{2}]'.format(skt, i + 1, nskt))
                try:
                    cdf = skeletoncdf(skt,
                                      output_dir=args.output_dir[0],
                                      overwrite=args.overwrite,
                                      exe=args.executable[0],
                                      auto_pad=not args.no_auto_pad,
                                      no_cdf=args.no_cdf)
                except CDFSerializerError as strerror:
                    logger.exception('SkeletonCDF error has occurred!')
                    cdf = None
                except ValueError as strerror:
                    logger.exception('Value error has occurred!')
                    cdf = None
                except:
                    logger.exception('skeletoncdf has failed!')
                    cdf = None
                finally:
                    if cdf is None:
                        bad_skt.append(skt)
                        logger.error(
                            'Converting {0} has failed, aborting!'.format(skt))
                        if not args.force:
                            sys.exit(-1)

            if len(bad_skt) > 0:
                logger.warning(
                    'Following files have not been converted correctly:')
                for bad in bad_skt:
                    logger.warning(bad)
        elif 'skeletontable' in args.maser:
            cdfs = args.cdf
            ncdf = len(cdfs)
            logger.info('{0} input file(s) found.'.format(ncdf))
            # Initializing list of bad conversion encountered
            bad_cdf = []
            # Loop over the input CDF files
            for i, cdf in enumerate(cdfs):
                logger.info(
                    'Executing skeletontable for {0}... [{1}/{2}]'.format(cdf, i + 1, ncdf))
                skt = skeletontable(cdf,
                                    to_xlsx=args.to_xlsx,
                                    output_dir=args.output_dir[0],
                                    overwrite=args.overwrite,
                                    exe=args.executable[0])
                try:
                    pass
                except CDFSerializerError as strerror:
                    logger.error('SkeletonCDF error -- {0}'.format(strerror))
                    cdf = None
                except ValueError as strerror:
                    logger.error('Value error -- {0}'.format(strerror))
                    cdf = None
                except:
                    logger.error(sys.exc_info()[0])
                    cdf = None
                finally:
                    if cdf is None:
                        bad_cdf.append(cdf)
                        logger.error(
                            'Converting {0} has failed, aborting!'.format(cdf))
                        if not args.force:
                            sys.exit(-1)

            if len(bad_cdf) > 0:
                logger.warning(
                    'Following files have not been converted correctly:')
                for bad in bad_cdf:
                    logger.warning(bad)
        # leapsec sub-command
        elif 'leapsec' in args.maser:
            # If get_file then download CDFLeapSeconds.txt file and exit
            if args.DOWNLOAD_FILE:
                target_dir = os.path.dirname(args.filepath[0])
                Lstable.get_lstable_file(target_dir=target_dir,
                                         overwrite=args.OVERWRITE)
                sys.exit()
            lst = Lstable(file=args.filepath[0])
            if args.date[0] is not None:
                date = datetime.strptime(args.date[0], INPUT_DATE)
                print('{0} sec.'.format(lst.get_leapsec(date=date)))
            elif args.SHOW_TABLE:
                print(lst)
            else:
                parser.print_help()
                # leapsec sub-command
        # cdf_compare sub-command
        elif 'cdf_compare' in args.maser:
            result = None
            try:
                result = cdf_compare(args.cdf_filepath1, args.cdf_filepath2,
                                     list_ignore_gatt=args.ignore_gatt,
                                     list_ignore_zvar=args.ignore_zvar,
                                     list_ignore_vatt=args.ignore_vatt,
                                     list_numerical_precision=args.precision)

                if result:
                    logger.info('CDF compare final result :\n %s',
                                pformat(result, width=1000))
                else:
                    logger.info('CDF compare final result : no differences')

            except Exception as err:
                logger.error('cdf_compare error -- {0}, aborting!'.format(err))
            finally:
                if result is None:
                    logger.error('CDF compare : Failure !')
                    sys.exit(-1)
        elif 'cdf_validator' in args.maser:
            cdfvalidator(args.cdf_file[0],
                         is_istp=args.istp,
                         model_json_file=args.model_file[0],
                         cdfvalidate_bin=args.cdfvalidate_bin[0],
                         run_cdf_validate=args.run_cdfvalidate)
            try:
                cdfvalidator(args.cdf_file[0],
                             is_istp=args.istp,
                             model_json_file=args.model_file[0],
                             cdfvalidate_bin=args.cdfvalidate_bin[0],
                             run_cdf_validate=args.run_cdfvalidate)
            except ValidatorException as strerror:
                logger.error(
                    'cdf_validator error -- {0}, aborting!'.format(strerror))
                sys.exit(-1)
            except:
                logger.error('cannot run cdf_validator, aborting!')
                sys.exit(-1)
#        elif 'hfcviewer' in args.maser:
            #hfcviewer(**args.__dict__)
        else:
            print('Unknown maser sub-command')
            parser.print_help()

    else:
        parser.print_help()

    # _________________ Main ____________________________


if __name__ == '__main__':
    main()
