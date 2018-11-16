#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""
Python module to work with PDS-PPI/Cassini/RPWS data
@author: B.Cecconi(LESIA)
"""

__author__ = "Baptiste Cecconi"
__copyright__ = "Copyright 2017, LESIA-PADC, Observatoire de Paris"
__credits__ = ["Baptiste Cecconi", "Laurent Lamy"]
__license__ = "GPLv3"
__version__ = "1.0b0"
__maintainer__ = "Baptiste Cecconi"
__email__ = "baptiste.cecconi@obspm.fr"
__status__ = "Development"
__date__ = "28-FEB-2017"
__project__ = "MASER/PDS PDS/Cassini/RPWS"

import datetime
import dateutil.parser


def scet_day_millisecond_to_datetime(scet_day, scet_millisecond):

    date0 = datetime.datetime(1958, 1, 1)
    date = []
    for day, millisecond in zip(scet_day, scet_millisecond):
        date.append(date0 + datetime.timedelta(days=int(day))
                    + datetime.timedelta(milliseconds=int(millisecond)))
    return date


def iso_time_to_datetime(iso_string):

    # checking YYYY-DDD or YYYY-MM-DD format:
    if iso_string.count('-') == 1:
        iso_string = "{}{}".format(datetime.datetime.strptime(iso_string[:8], '%Y-%j').strftime('%Y-%m-%d'),
                                   iso_string[8:])

    return dateutil.parser.parse(iso_string, ignoretz=True)