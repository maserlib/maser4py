#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Maser4py time module."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)
from pytz import timezone
import numpy
from numpy import datetime64, timedelta64
from datetime import datetime, timedelta
import logging

from ..toolbox import print_exception

from .leapsec import Lstable

from .const import MJD_EPOCH, \
    JD_TO_MJD, TT2000_EPOCH, DELTA_NSEC_TAI_TT

__all__ = ["set_tzone",
           "local_to_utc",
           "jd_to_mjd",
           "jd_to_tt2000",
           "mjd_to_jd",
           "tai_to_tt",
           "tt_to_tai",
           "tt_to_utc",
           "tt_to_tt2000",
           "utc_to_tt2000",
           "utc_to_tt",
           "tt2000_to_tt",
           "tt2000_to_utc",
           "tt2000_to_jd",
           "get_leapsec"]

# ________________ HEADER _________________________

# Mandatory
__version__ = "0.1.0"
__author__ = "X.Bonnin"
__date__ = "2017-03-31"

# Optional
__license__ = ""
__credit__ = [""]
__maintainer__ = ""
__email__ = ""
__project__ = "MASER"
__institute__ = "LESIA"
__changes__ = ""


# ________________ Global Variables _____________
# (define here the global variables)
logger = logging.getLogger(__name__)

# ________________ Class Definition __________
# (If required, define here classes)


class TimeException(Exception):
    pass

# ________________Global Functions __________
# (If required, define here classes)


def cast_timedelta(fr=None, to=None):
    """
    cast_timedelta decorator.

    Decorator to set the first input/output argument of a
    function as a datetime.timedelta or
    numpy.timedelta64 type object depending of
    the decorator input keywords.

    Inputs:
        fr -- keyword to indicate the type to be passed to
              the function.
              (Possible values = timedelta, timedelta64 or None).
              If 'fr=None', then use the input type.
        to -- keyword to indicate the type to be returned by
              the function.
              (Possible values = timedelta, timedelta64 or None).
              If 'fr=None', then use the input type.

    Example:

        from datetime import timedelta
        from numpy import timedelta64

        @cast_timedelta(to=timedelta, fr=timedelta64)
        def func(td_in):
            ...
            return td_out

        Calling 'td_out = func(td_in)' will force the input 'td_in'
        parameter to be passed to the function as a
        datetime.timedelta object and to
        return the td_out output as a numpy.timedelta64 object.
    """
    def decorated(func):
        """Decorated method."""
        def wrapper(*args, **kwargs):
            args = list(args)
            """Decorator wrapper."""
            type_in = type(args[0])
            try:
                if type_in is not timedelta and type_in is not timedelta64:
                    # Only timedelta and timedelta64 objects are allowed as
                    # input.
                    raise TypeError(
                        "Input argument format is not valid [{0}]!".format(
                            type_in))

                if type_in is timedelta64 and fr is timedelta:
                    td_in = td64_to_td(args[0])
                elif type_in is timedelta and fr is timedelta64:
                    td_in = td_to_td64(args[0])
                elif type_in is timedelta64 and fr is timedelta64:
                    td_in = args[0]
                elif type_in is timedelta and fr is timedelta:
                    td_in = args[0]
                elif fr is None:
                    td_in = args[0]
                else:
                    raise TypeError("Input argument is not valid!")
            except:
                print_exception()
            else:
                # Execute the function with the right input time type
                args[0] = td_in
                td_out = func(*args, **kwargs)

            # Depending of the decorator input and function I/O
            # return the output timedelta with the right time type
            type_out = type(td_out)
            if type_out is timedelta64 and to is timedelta:
                return td64_to_td(td_out)
            elif type_out is timedelta and to is timedelta64:
                return td_to_td64(td_out)
            elif type_out is timedelta and to is timedelta:
                return td_out
            elif type_out is timedelta64 and to is timedelta64:
                return td_out
            # If output type is not defined, then return as an input type
            elif (type_out is timedelta and to is None and
                  type_in is timedelta):
                return td_out
            elif (type_out is timedelta and to is None and
                  type_in is timedelta64):
                return td_to_td64(td_out)
            elif (type_out is timedelta64 and to is None and
                  type_in is timedelta):
                return td64_to_td(td_out)
            elif (type_out is timedelta64 and to is None and
                  type_in is timedelta64):
                return td_out
            else:
                return td_out

        return wrapper
    return decorated


def cast_datetime(fr=None, to=None):
    """
    cast_datetime decorator.

    Decorator to set the first input/output argument of a
    function as a datetime.datetime or
    numpy.datetime64 type object depending of
    the decorator input keywords.

    Inputs:
        fr -- keyword to indicate the type to be passed to
              the function.
              (Possible values = datetime, datetime64 or None).
              If 'fr=None', then use the input type.
        to -- keyword to indicate the type to be returned by
              the function.
              (Possible values = datetime, datetime64 or None).
              If 'fr=None', then use the input type.

    Example:

        from datetime import datetime
        from numpy import datetime64

        @cast_datetime(to=datetime, fr=datetime64)
        def func(dt_in):
            ...
            return dt_out

        Calling 'dt_out = func(dt_in)' will force the 'dt_in' input parameter
        to be passed to the function as a datetime.datetime object and to
        return the dt_out output as a numpy.datetime64 object.
    """
    def decorated(func):
        """Decorated method."""
        def wrapper(*args, **kwargs):
            args = list(args)
            """Decorator wrapper."""
            args = list(args)
            type_in = type(args[0])
            try:
                if type_in is not datetime and type_in is not datetime64:
                    # Only datetime and datetime64 objects are allowed as
                    # input.
                    raise TypeError(
                        "Input argument format is not valid [{0}]!".format(
                            type_in))

                if type_in is datetime64 and fr is datetime:
                    dt_in = dt64_to_dt(args[0])
                elif type_in is datetime and fr is datetime64:
                    dt_in = dt_to_dt64(args[0])
                elif type_in is datetime64 and fr is datetime64:
                    dt_in = args[0]
                elif type_in is datetime and fr is datetime:
                    dt_in = args[0]
                elif fr is None:
                    dt_in = args[0]
                else:
                    raise TypeError("Input argument is not valid!")
            except:
                print_exception()
            else:
                # Execute the function with the right input time type
                args[0] = dt_in
                dt_out = func(*args, **kwargs)

            # Depending of the decorator input and function I/O
            # return the output datetime with the right time type
            type_out = type(dt_out)
            if type_out is datetime64 and to is datetime:
                return dt64_to_dt(dt_out)
            elif type_out is datetime and to is datetime64:
                return dt_to_dt64(dt_out)
            elif type_out is datetime and to is datetime:
                return dt_out
            elif type_out is datetime64 and to is datetime64:
                return dt_out
            # If output type is not defined, then return as an input type
            elif (type_out is datetime and to is None and
                  type_in is datetime):
                return dt_out
            elif (type_out is datetime and to is None and
                  type_in is datetime64):
                return dt_to_dt64(dt_out)
            elif (type_out is datetime64 and to is None and
                  type_in is datetime):
                return dt64_to_dt(dt_out)
            elif (type_out is datetime64 and to is None and
                  type_in is datetime64):
                return dt_out
            else:
                return dt_out

        return wrapper
    return decorated


@cast_datetime(fr=datetime)
def get_leapsec(date, leapsec_file=None, to_timedelta64=False):
    """Return leap seconds in timedelta format for a given datetime.

    Leapsec are returned in the timedelta64 format if
    to_timedelta64 keyword is set to True.
    """
    leapsec = Lstable(file=leapsec_file).get_leapsec(date)

    # Convert seconds in float to timedelta object
    leapsec = timedelta(microseconds=leapsec * 1000000)

    if to_timedelta64:
        leapsec = numpy.timedelta64(leapsec)

    # get leapsec.
    return leapsec


@cast_datetime(fr=datetime)
def set_tzone(date, tzone):
    """Change the current time zone."""
    return date.replace(timezone(tzone))


def td64_to_td(td64):
    """
    td64_to_td.

    Convert a numpy.timedelta64 object into a
    datetime.timedelta object.
    """
    return td64.astype(timedelta)


def td_to_td64(td):
    """
    td_to_td64.

    Convert a numpy.timedelta object into a
    numpy.timedelta64 object.
    """
    return numpy.timedelta64(td)


def dt64_to_dt(dt64):
    """
    dt64_to_dt.

    Convert a numpy.datetime64 object into a
    datetime.datetime object.

    Note that the time resolution of a datetime.datetime
    object is microsecond.
    """
    return dt64.astype('M8[us]').astype('O')


def dt_to_dt64(dt):
    """
    dt_to_dt64.

    Convert a numpy.datetime object into a
    numpy.datetime64 object.

    Note that the time resolution of a numpy.datetime
    object is attosecond.
    """
    return numpy.datetime64(dt)


@cast_datetime(fr=datetime)
def local_to_utc(local_time, tzone=None):
    """
    local_to_utc.

    From a given local time and timezone,
    returns the corresponding UTC time.

    Input parameter local_time must be a
    datetime.datetime object.

    See pytz module documentation for allowed values
    of the input optional parameter timezone

    UTC time is returned as a datetime.datetime object.
    """
    if tzone is not None:
        tz = timezone(tzone)
        ltime = tz.localize(local_time.replace(tzinfo=None))

    return ltime.astimezone(timezone('UTC'))


@cast_timedelta(fr=timedelta64)
def jd_to_mjd(jd):
    """Convert Julian Days (JD) to modified JD.

    Be awared that the best time resolution is
    microsec.
    """
    return numpy.timedelta64(jd, 'us') - JD_TO_MJD


@cast_timedelta(fr=timedelta64)
def mjd_to_jd(mjd):
    """Convert Modified Julian Days (MJD) to JD.

    Be awared that the best time resolution is
    microsec.
    """
    return numpy.timedelta64(mjd, 'us') + JD_TO_MJD


@cast_datetime(fr=datetime64)
def tai_to_tt(tai):
    """Convert TAI time to TT time."""
    return tai + DELTA_NSEC_TAI_TT


@cast_datetime(fr=datetime64)
def tt_to_tai(tt):
    """Convert TT time to TAI time."""
    return tt - DELTA_NSEC_TAI_TT


# Works with np.datetime64 object I/O only
@cast_datetime(fr=datetime64, to=datetime64)
def utc_to_tt(utc):
    """
    utc_to_tt.

    Convert UTC time to Terrestrial Time (TT).
    TT = TAI + DELTA_NSEC_TAI_TT;
    TT = UTC + delta_LeapSec + DELTA_NSEC_TAI_TT
    where DELTA_NSEC_TAI_TT = 32.184s

    TT time is returned as a numpy.datetime64 object.
    """
    return utc + \
        get_leapsec(utc, to_timedelta64=True) + \
        DELTA_NSEC_TAI_TT


@cast_datetime(fr=datetime64)
def tt_to_utc(tt):
    """
    utc_to_tt.

    Convert UTC time to Terrestrial Time (TT).
    TT = TAI + DELTA_NSEC_TAI_TT;
    TT = UTC + delta_LeapSec + DELTA_NSEC_TAI_TT
    where DELTA_NSEC_TAI_TT = 32.184s

    """
    return tt - \
        get_leapsec(tt, to_timedelta64=True) - \
        DELTA_NSEC_TAI_TT


@cast_datetime(fr=datetime64)
def utc_to_jd(utc, to_mjd=True):
    """
    utc_to_jd.

    Convert UTC time into Julian days.

    Returns MJD instead of JD if to_mjd keyword is set.

    Returned value is always a numpy.timedelta64 object.
    """
    mjd = utc - MJD_EPOCH

    if not to_mjd:
        return mjd_to_jd(mjd)
    else:
        return mjd


@cast_timedelta(fr=timedelta64)
def jd_to_utc(jd, from_mjd=True):
    """
    jd_to_utc.

    Convert Julian Days into UTC time.

    Use MJD instead of JD as input if from_mjd keyword is set.

    Returned value is always a numpy.datetime64 object.
    """
    if not from_mjd:
        return jd_to_mjd(jd) + MJD_EPOCH
    else:
        return jd + MJD_EPOCH


@cast_datetime(fr=datetime64)
def utc_to_tt2000(utc):
    """
    utc_to_tt2000 method.

    Convert UTC time into TT2000 time.

    Returned value is a numpy.timedelta64 object.
    """
    tt = utc_to_tt(utc)
    return tt_to_tt2000(tt)


# Works with np.datetime64 object I/O only
@cast_timedelta(fr=timedelta64)
def tt2000_to_utc(tt2000):
    """
    tt2000_to_utc method.

    Convert TT2000 time into UTC.

    Returned value is a numpy.datetime64 object.
    """
    tt = tt2000_to_tt(tt2000)
    return tt_to_utc(tt)


@cast_timedelta(fr=timedelta64)
def tt2000_to_tt(tt2000):
    """
    tt2000_to_tt.

    Convert TT2000 time into TT.

    Returns TT in timedelta64 format.
    """
    return tt2000 + TT2000_EPOCH


@cast_datetime(fr=datetime64)
def tt_to_tt2000(tt):
    """
    tt_to_tt2000.

    Convert TT time into TT2000.

    Returns TT2000 in timedelta64 format.
    """
    return tt - TT2000_EPOCH


@cast_timedelta(fr=timedelta64)
def tt2000_to_jd(tt2000,
                 to_mjd=False):
    """
    tt2000_to_jd.

    Convert TT2000 time into Julian days.

    Returns MJD instead of JD if to_mjd keyword is set.

    Returned value is a numpy.timedelta64 object
    with microsec. time resolution.

    """
    # Convert TT2000 in MJD
    utc = tt2000_to_utc(tt2000)
    return utc_to_jd(utc, to_mjd=to_mjd)


@cast_timedelta(fr=timedelta64)
def jd_to_tt2000(jd,
                 from_mjd=False):
    """
    jd_to_tt2000.

    Convert Julian Days (JD) into TT2000.

    Use MJD instead of JD if from_mjd keyword is set.

    Returned value is always a numpy.timedelta64 object.

    The best time resolution of input JD must be microsec.

    """
    # Convert to MJD, if from_mjd keyword is not set
    utc = jd_to_utc(jd, from_mjd=from_mjd)
    return utc_to_tt2000(utc)


# _________________ Main ____________________________
# if (__name__ == "__main__"):
    # print ""
    # main()
