#! /usr/bin/env python3
# -*- coding: latin-1 -*-

"""
Python library to get and read Wind/Waves data.
@author: X.Bonnin (LESIA)
"""
__author__ = "Xavier Bonnin"
__institute__ = "LESIA, Observatoire de Paris, CNRS."
__date__ = "08-MAY-2013"
__version__ = "1.0.1"

__project__ = "Wind/Waves"

import os
import re
import logging
import subprocess
import numpy as np
from copy import deepcopy
from datetime import datetime
from PIL import Image
from scipy.interpolate import barycentric_interpolate

from maser.utils.toolbox import download_data, setup_logging

CURRENT_DIRECTORY = os.getcwd()

# Distant servers where data are stored
# NASA/GSFC
GSFC_URL = "ftp://stereowaves.gsfc.nasa.gov"
# Observatoire de Paris/LESIA
LESIA_URL = "ftp://sorbet.obspm.fr"

# Date and time formats
WAVES_TFORMAT = "%Y%m%d"

# Min val
MIN_VAL = 1.0e-30

# Wind/Waves receiver parameters
RAD1_BANDWIDTH = 3.0  # kHz
RAD1_INT_TIME_S = 154  # ms
RAD1_INT_TIME_Z = 308  # ms
RAD1_FREQ_STEP = 4.0  # kHz
RAD1_FREQ_MIN = 20.0  # kHz
RAD1_FREQ_NUM = 256
RAD2_BANDWIDTH = 20.0  # kHz
RAD2_INT_TIME_S = 20  # ms
RAD2_INT_TIME_Z = 40  # ms
RAD2_FREQ_STEP = 50.0  # kHz
RAD2_FREQ_MIN = 1075.0  # kHz
RAD2_FREQ_NUM = 256
TNR_BANDWIDTH = None  # kHz --> TBD
TNR_INT_TIME = None  # ms --> TBD
TNR_FREQ_STEP = None  # kHz
TNR_FREQ_MIN = 4.0  # kHz
TNR_FREQ_NUM = 96

# logger name
logger = logging.getLogger(__name__)


# Wind/Waves class
class Wind():
    def __init__(self,
                 provider="gsfc",
                 receiver="rad2",
                 dataset="l2_60s",
                 username=None,
                 password=None):

        self.provider = provider
        self.observatory = "Wind"
        self.instrument = "Waves"
        self.receiver = receiver
        self.dataset = dataset
        self.username = username
        self.password = password

    def get_filename(self, date,
                     receiver=None,
                     provider=None,
                     dataset=None):

        """
        This method returns the name of
        the Waves file providing the
        date of observation.
        """
        if not isinstance(date, datetime):
            logger.error("Input date must be a datetime object!")
            return None
        if (provider is None):
            provider = self.provider
        if (receiver is None):
            receiver = self.receiver
        if (dataset is None):
            dataset = self.dataset
        pro = provider.lower()
        rec = receiver.lower()
        ds = dataset.lower()
        if (pro == "gsfc"):
            filename = date.strftime(WAVES_TFORMAT)
            if (rec == "rad1"):
                filename += ".R1.Z"
            elif (rec == "rad2"):
                filename += ".R2.Z"
            elif (rec == "tnr"):
                filename += ".tnr.Z"
            else:
                logger.error("Unknown receiver!")
                return None
        elif (pro == "lesia"):
            filename = date.strftime(WAVES_TFORMAT)
            if (rec == "rad1"):
                if (ds == "l2_hres"):
                    filename = "WIN_RAD1_" + filename + ".B3E"
                elif (ds == "l2_60s"):
                    filename = "WIN_RAD1_60S_" + filename + ".B3E"
                elif (ds == "l3_df"):
                    filename = "WIN_RAD1_DF_" + filename + ".B3E"
                elif (ds == "l3_gp"):
                    filename = "WIN_RAD1_DF_" + filename + ".B3E"
                else:
                    logger.error("Unknown data set!")
                    return None
            elif (rec == "rad2"):
                if (ds == "l2_hres"):
                    filename = "WIN_RAD2_" + filename + ".B3E"
                elif (ds == "l2_60s"):
                    filename = "WIN_RAD2_60S_" + filename + ".B3E"
                elif (ds == "l3_sfu"):
                    filename = "WIN_RAD2_SFU_" + filename + ".B3E"
                else:
                    logger.error("Unknown data set!")
                    return None
            elif (rec == "tnr"):
                logger.warning("TNR data set not available yet!")
                return None
            else:
                logger.error("Unknown data set!")
                return None
        else:
            logger.error("Unknown data provider!")
            return None
        return filename

    def get_date(self, filename,
                 provider=None):

        """
        This method returns the date of
        observation of a given file.
        """

        if (provider is None):
            provider = self.provider
        pro = provider.lower()

        if (pro == "gsfc"):
            date = datetime.strptime(os.path.basename(filename)[0:8], WAVES_TFORMAT)
        elif (pro == "lesia"):
            date = datetime.strptime(os.path.basename(filename.split("_")[-1][0:8]), WAVES_TFORMAT)
        else:
            logger.warning("Unknown data provider!")
            return None

        return date

    def get_rec(self, filename,
                provider=None):

        """
        This method returns the receiver name
        providing the name of the file.
        """

        if (provider is None):
            provider = self.provider
        pro = provider.lower()

        basename = os.path.basename(filename)
        if (pro == "gsfc"):
            if ((re.search("\d{8}.R1", basename)) or
                    (re.search("\d{8}.R1.Z", basename))):
                return "rad1"
            elif ((re.search("\d{8}.R2", basename)) or
                  (re.search("\d{8}.R2.Z", basename))):
                return "rad2"
            elif ((re.search("\d{8}.tnr", basename)) or
                  (re.search("\d{8}.tnr.Z", basename))):
                return "tnr"
            else:
                logger.error("Wrong GSFC Waves filename!")
                return None
        elif (pro == "lesia"):
            return basename.split("_")[1].lower()
        else:
            logger.error("Unknown data provider!")
            return None

    def get_dataset(self, filename,
                    provider=None):

        """
        This method returns the dataset
        for a given filename.
        """

        if (provider is None):
            provider = self.provider
        pro = provider.lower()

        basename = os.path.basename(filename)
        if (pro == "gsfc"):
            return "l2_60s"
        elif (pro == "lesia"):
            if (re.search("WIN_\w{3,4}_\d{8}.B3E", basename)):
                return "l2_hres"
            elif (re.search("WIN_\w{3,4}_60S_\d{8}.B3E", basename)):
                return "l2_60s"
            elif (re.search("WIN_\w{3,4}_DF_\d{8}.B3E", basename)):
                return "l3_df"
            elif (re.search("WIN_\w{3,4}_GP_\d{8}.B3E", basename)):
                return "l3_gp"
            elif (re.search("WIN_\w{3,4}_SFU_\d{8}.B3E", basename)):
                return "l3_sfu"
            else:
                logger.error("Unknown type of file!")
                return None
        else:
            logger.error("Unknown data provider!")
            return None

    def get_url(self, date=None,
                receiver=None,
                filename=None,
                provider=None,
                dataset=None,
                verbose=True):

        """
        This method returns the url a
        the Waves data file.
        """

        if (provider is None):
            provider = self.provider
        pro = provider.lower()

        if (dataset is None):
            dataset = self.dataset
        ds = dataset.lower()

        if (filename is None):
            if (receiver is None):
                receiver = self.receiver
            rec = receiver.lower()
            basename = self.get_filename(date, receiver=rec,
                                         provider=provider,
                                         dataset=ds,
                                         verbose=verbose)
        else:
            rec = self.get_rec(filename)
            basename = os.path.basename(filename)

        if (pro == "gsfc"):
            url = GSFC_URL
            if (rec == "rad1"):
                url += "/wind_rad1/rad1a"
            elif (rec == "rad2"):
                url += "/wind_rad2/rad2a"
            elif (rec == "tnr"):
                url += "/wind_tnr/tnra"
            else:
                logger.error("Unknown receiver!")
                return None
        elif (pro == "lesia"):
            url = LESIA_URL
            url += "/WindServer/Data/WIND_Data/CDPP/%s" % (rec)
            if (ds == "l2_hres"):
                url += "/l2/h_res"
            elif (ds == "l2_60s"):
                url += "/l2/average"
            elif (ds == "l3_df"):
                url += "/l3/df"
            elif (ds == "l3_gp"):
                url += "/l3/gp"
            elif (ds == "l3_sfu"):
                url += "/l3/sfu"
            else:
                logger.error("Unknown dataset!")
                return None
        else:
            logger.error("Unknown data provider!")
            return None

        url += "/" + basename
        return url

    def get_file(self, date=None,
                 receiver=None,
                 filename=None,
                 dataset=None,
                 provider=None,
                 username=None,
                 password=None,
                 data_directory=CURRENT_DIRECTORY,
                 verbose=True):

        """
        This method downloads the Waves data file,
        and returns the local path to the file.
        """
        if (username is None):
            username = self.username
        if (password is None):
            password = self.password

        url = self.get_url(date=date,
                           receiver=receiver,
                           provider=provider,
                           dataset=dataset,
                           filename=filename)

        if (url is not None):
            target = download_data(url,
                                   username=username, password=password,
                                   target_directory=data_directory,
                                   verbose=verbose)
            return target
        else:
            return None

    def read_file(self, filename,
                  verbose=True):
        """
        This method read the Waves data file
        """

        basename = os.path.basename(filename)

        if (re.search("\d{8}.R\d{1}", basename)) or \
                (re.search("\d{8}.tnr", basename)) or \
                (re.search("\d{8}.R\d{1}.Z", basename)) or \
                (re.search("\d{8}.tnr.Z", basename)):
            array = self.read_gsfc(filename)

        return array

    def get_data(self, filename=None,
                 date=None, receiver=None,
                 data_directory=None,
                 download_file=False,
                 delete_file=False,
                 verbose=True,
                 prep=False,
                 interpolate=False,
                 dB=False):
        """
        This method returns the Waves data.
        """

        if (filename is None):
            filename = self.get_filename(date, receiver=receiver,
                                         verbose=verbose)
        if (data_directory is None):
            data_directory = os.path.dirname(filename)
        filename = os.path.basename(filename)

        filepath = os.path.join(data_directory, filename)
        if not (os.path.isfile(filepath)):
            if (verbose):
                print("%s not found!" % filepath)
            if (download_file):
                filepath = self.get_file(date=date, receiver=receiver,
                                         data_directory=data_directory,
                                         filename=filename, verbose=verbose)
                if (filepath is None): return None
            else:
                return None
        data = self.read_file(filepath, verbose=verbose)

        if (delete_file):
            if (os.path.isfile(filepath)):
                os.remove(filepath)
                if (verbose):
                    print("%s deleted" % filepath)

        if (prep):
            return self.prep_data(data, dB=dB, interpolate=interpolate)
        else:
            return data

    def read_lesia(self, filename):

        """
        This method reads the ObsParis/LESIA waves data file.
        """
        rec = self.get_rec(filename, provider="lesia")
        ds = self.get_dataset(filename, provider="lesia")

        # with (open(filename,'rb') as frb):
        #    content = frb.read()

        # if (rec == "rad1") and (ds == "l2_hres"):

    def read_gsfc(self, filename):

        """
        This method reads the nasa/gsfc waves data file.
        """

        basename = os.path.basename(filename)
        if (basename.endswith("Z")):
            ext = basename.split(".")[-2].lower()
            cmd = ["gzip", "-dc", filename]
            gzip_process = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE)
            output, error = gzip_process.communicate()
            if (gzip_process.wait() == 0):
                file_content = output.split("\n")[0:-1]
        else:
            ext = basename.split(".")[-1].lower()
            fr = open(filename, 'r')
            file_content = fr.read().split("\n")[0:-1]
            fr.close()
            nf = len(file_content)
            nt = len(file_content[0].split())
            array = np.zeros((nt, nf), dtype=np.float32)
            for i, line in enumerate(file_content):
                array[:, i] = np.float32(line.split())
            nt -= 1

        dt = 60.0  # sec
        time = dt * np.arange(nt, dtype=np.float32)
        if (ext == "r1"):
            receiver = "rad1"
            bandwidth = RAD1_BANDWIDTH
            integration_time = RAD1_INT_TIME_S
            if nf != RAD1_FREQ_NUM:
                return None
            df = RAD1_FREQ_STEP
            freq = RAD1_FREQ_STEP * np.arange(nf, dtype=np.float32) + RAD1_FREQ_MIN
        elif (ext == "r2"):
            receiver = "rad2"
            bandwidth = RAD2_BANDWIDTH
            integration_time = RAD2_INT_TIME_S
            if (nf != RAD2_FREQ_NUM): return None
            df = RAD2_FREQ_STEP
            freq = RAD2_FREQ_STEP * np.arange(nf, dtype=np.float32) + RAD2_FREQ_MIN
        elif (ext == "tnr"):
            receiver = "tnr"
            bandwidth = TNR_BANDWIDTH
            integration_time = TNR_INT_TIME
            if nf != TNR_FREQ_NUM:
                return None
            df = TNR_FREQ_STEP
            freq = np.power(10, np.arange(nf, dtype=np.float32) * 0.0188144 + np.log10(TNR_FREQ_MIN))
        else:
            return None

        date = self.get_date(filename)
        hmin, mmin, smin = split_time(min(time / 3600.))
        hmax, mmax, smax = split_time(max(time / 3600.))
        date_obs = datetime(day=date.day, year=date.year, month=date.month,
                            hour=hmin, minute=mmin, second=smin)
        date_end = datetime(day=date.day, year=date.year, month=date.month,
                            hour=hmax, minute=mmax, second=smax)

        data = spectrum(observatory=self.observatory,
                        instrument=self.instrument,
                        receiver=receiver,
                        intensity=array[0:-1, :],
                        background=array[-1, :],
                        time=time, frequency=freq,
                        date_obs=date_obs,
                        date_end=date_end,
                        naxis=[nt, nf],
                        cdelt=[dt, df],
                        bandwidth=bandwidth,
                        integration_time=integration_time,
                        intensity_units="Intensity above background",
                        comment="60 sec. average data produced by GSFC (NASA).")
        return data

    def prep_data(self, data,
                  quantile=0.1, nbins=1000,
                  interpolate=False, dB=False,
                  substract_background=False):
        """
        This method preprocesses data (e.g., substract background).
        """

        prov = self.provider
        prep_data = deepcopy(data)
        array = data.get_parameter("intensity")
        nt = data.naxis[0];
        nf = data.naxis[1]
        frequency = data.get_parameter("frequency")
        background = data.get_parameter("background")
        int_time = data.get_parameter("integration_time")
        bandwidth = data.get_parameter("bandwidth")
        rms = 1. / np.sqrt(int_time * bandwidth)

        if (prov == "gsfc"):
            if (interpolate):
                where_ok = np.where(background > 0.0)
                background = barycentric_interpolate(frequency[where_ok],
                                                     background[where_ok],
                                                     frequency)
        snr = np.zeros((nt, nf), dtype=np.float32)
        for j in range(nf):
            array_j = array[:, j] * background[j]
            if (sum(array_j) == 0.0): continue
            array_j = array_j - background[j]
            snr[:, j] = array_j / (background[j] * rms)
            if (substract_background):
                array[:, j] = array_j

        if (dB):
            array = to_dB(array.clip(MIN_VAL, array.max()))
            snr = to_dB(snr.clip(MIN_VAL, snr.max()))
            background = to_dB(background.clip(MIN_VAL, background.max()))
            if (substract_background):
                intensity_units = "Intensity (dB)"
            else:
                intensity_units = "Intensity above background (dB)"
        else:
            if (substract_background):
                intensity_units = "Intensity"

        prep_data.set_parameter("intensity_units", intensity_units)
        prep_data.set_parameter("intensity", array)
        prep_data.set_parameter("background", background)
        prep_data.set_parameter("snr", snr)

        return prep_data

    def write_img(self, filename=None,
                  date=None, receiver=None,
                  data=None,
                  format='jpg', quality=80,
                  data_directory=None,
                  output_filename=None,
                  output_directory=None,
                  min_val=None, max_val=None,
                  verbose=True, greyscale=True,
                  reverse_color=True,
                  download_file=False,
                  delete_file=False,
                  prep=False):
        """
        Write output image file containing the dynamical spectrum.
        """

        if (greyscale):
            mode = 'L'
        else:
            mode = 'RGB'

        ext = format.lower()

        if (data is None):
            data = self.get_data(date=date, receiver=receiver,
                                 filename=filename,
                                 data_directory=data_directory,
                                 download_file=download_file,
                                 delete_file=delete_file,
                                 verbose=verbose, prep=prep)
        if (data is None):
            return ""

        array = data.intensity
        if (min_val is None): min_val = array.min()
        if (max_val is None): max_val = array.max()

        array = array.clip(min_val, max_val)
        if not ("(db)" in data.intensity_units.lower()):
            array = to_dB(array)

        if (reverse_color):
            array = array.max() - array
            image = Image.fromarray(array, mode=mode)

        if (output_filename is None):
            if (filename is None):
                filename = self.get_filename(date, receiver=receiver)
                output_filename = os.path.basename(filename) + "." + ext

        if (output_directory is None):
            output_path = output_filename
        else:
            output_path = os.path.join(output_directory, os.path.basename(output_filename))

        image.save(output_path, quality=quality)

        return output_path

# Spectrum class
class spectrum():
    def __init__(self,
                 observatory="",
                 instrument="",
                 receiver="",
                 intensity=None,
                 background=None,
                 snr=None,
                 time=None,
                 frequency=None,
                 date_obs=None,
                 date_end=None,
                 naxis=None,
                 cdelt=None,
                 bandwidth=None,
                 integration_time=None,
                 intensity_units="",
                 comment=""):

        self.observatory = observatory
        self.instrument = instrument
        self.receiver = receiver
        self.intensity = intensity
        self.background = background
        self.snr = snr
        self.time = time
        self.frequency = frequency
        self.date_obs = date_obs
        self.date_end = date_end
        self.naxis = naxis
        self.cdelt = cdelt
        self.bandwidth = bandwidth
        self.integration_time = integration_time
        self.intensity_units = intensity_units
        self.comment = comment

    # Method to set input parameter
    def set_parameter(self, parameter, value):
        if (parameter in self.__dict__):
            self.__dict__[parameter] = value

    # Method to get an attribute's value
    def get_parameter(self, parameter):
        value = None
        if (parameter in self.__dict__):
            value = self.__dict__[parameter]
        return value


# Method to compute the 100*Q% quantile of a set X of values
def get_quantile(X, Q, nbins=None, dX=None):
    nX = len(X)
    if (dX is None):
        dX = 2.0 * np.median(abs(np.diff(X)))

    if (nbins is None):
        nbins = int((max(X) - min(X)) / dX) + 1

    h, xh = np.histogram(X, bins=nbins)
    threshold = Q * sum(h)
    i = 0;
    hsum = 0.0;
    nh = len(h)
    while (hsum < threshold):
        hsum += h[i]
        i += 1
        if (i == (nh)): break

    return xh[i - 1]


# Method to convert in dB
def to_dB(array):
    arr = np.log10(np.array(array))
    ylog = np.multiply(10.0, arr)
    return ylog


# Method tot split float hours into hour, minute, second
def split_time(float_time):
    hour = int(float_time)
    minute = int((float_time - float(hour)) * 60.0)
    second = int(float_time * 3600.0 - float(hour) * 3600.0 - float(minute) * 60.0)

    return hour, minute, second

