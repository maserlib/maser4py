#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Subparser for maser.data modules."""

from pathlib import Path

# ________________ Global Functions __________
# (If required, define here global functions)
def swaves_subparser(subparser):
    """cdf.cdfcompare script program."""
    swaves_parser = subparser.add_parser('swaves',
                                         description='Parse input STEREO/Waves file.')
    swaves_parser.add_argument('filepath',
                        nargs=1,
                        type=Path,
                        help='STEREO/Waves binary file path',
                        )
