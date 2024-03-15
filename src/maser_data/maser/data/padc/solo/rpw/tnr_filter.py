# -*- coding: utf-8 -*-
import numpy


def fft_filter(x1, tlow, tup):  # x1 corresponds to the entry (auto)
    """
    Apply FFT filter on input data vector

    :param x1: Input vector to filter
    :param tlow: Lower filtering limit in the Fourier frame
    :param tup: Upper filtering limit in the Fourier frame
    :return:
    """
    npp = numpy.size(x1)  # Size of the entry
    yfo = numpy.fft.ifft(x1)  # Fourier discret + ifft
    yyf0 = yfo[0]  # Get first value f0
    # Build frequency bin values in Fourier plan
    freq = numpy.arange(
        float((npp - 1) / 2) + 1.0
    )  # numpy.arange([start, ]stop, [step, ]dtype=None, *, like=None) Return evenly spaced values within a given interval.
    freq = freq / npp
    #
    if (numpy.mod(npp, 2)) == 0:
        yyf0 = yfo[0]
        freq = numpy.arange(float(npp / 2) + 1.0)
        freq[0 : int(npp / 2)] = freq[0 : int(npp / 2)] / npp
        freq[int(npp / 2)] = 1.0 / 2.0
    fup = tup / npp
    flow = tlow / npp
    nnf = numpy.size(freq)
    if flow > freq[nnf - 1]:
        flow = freq[nnf - 1]
    pp = numpy.where((freq > flow) & (freq < fup))
    xn = numpy.size(pp)
    if xn > 0:
        yf = numpy.zeros(npp, dtype=complex)
        yf[pp] = yfo[pp]
        yf[npp - numpy.squeeze(pp)] = yfo[npp - numpy.squeeze(pp)]
        yf[0] = 0.0
        yfnull = yf * 0.0
        yfnull[0] = yyf0

    xf = numpy.fft.fft(yf)
    xf = numpy.real(xf)
    xfnull = numpy.fft.fft(yfnull)
    xfnull = numpy.real(xfnull)
    return xf, xfnull


def pre_process(V, tlow=0.01, tup=280.0):
    """
    Mask and filter TNR data to remove artifacts
    Note: output data are in log scale

    :param V: Input TNR data 2D array (linear scale) with frequency along X-axis and time along Y-axis.
    :param tlow: Lower frequency filtering limit in the Fourier plan
    :param tup: Upper frequency filtering limit in the Fourier plan
    :return: VV = Input data in dB with some values set to FILLVAL for known polluted frequencies. Vfil = Input data but after FFT filtering
    """
    # Get the size of the input data array
    ndim = numpy.shape(V)
    # Initialize temporary 2D arrays Vf and Vf0 with V dimensions
    Vf = (ndim[0], ndim[1])
    Vf = numpy.zeros(Vf)
    Vf0 = (ndim[0], ndim[1])
    Vf0 = numpy.zeros(Vf0)

    # Convert V to dB (instead of linear scale)
    V2o = 10.0 * numpy.log10(V)
    # Initialize V2 array with V2o values as default
    V2 = V2o
    # Get Boolean array (mask) of infinity values of V2o
    nap = numpy.isinf(V2o)

    # Loop over each TNR frequency
    for ii in range(128):
        # Get mask Boolean values for current frequency
        napp = nap[ii, :]
        # Fill V2 with mean value of finite V2o data
        V2[ii, napp] = numpy.mean(V2o[numpy.isfinite(V2o)])

    # Loop over each TNR frequency
    for ii in range(128):
        # Make sure to have a vector
        x = numpy.squeeze(V2[ii, :])
        # Apply fft_filter method on data array
        xf, xfnull = fft_filter(x, tlow, tup)
        # Fill Vf array with non-null filtered data
        Vf[ii, :] = xf
        # Fill Vf0 array with null filtered data
        Vf0[ii, :] = xfnull

    # Apply
    V[75:80, :] = 1e-31
    V[85:86, :] = 1e-31
    V[103:104, :] = 1e-31
    V[110:111, :] = 1e-31
    V[115:116, :] = 1e-31
    V[118:119, :] = 1e-31

    # Convert output data array VV into dB
    VV = 10.0 * numpy.log10(V)

    Vfil = Vf + numpy.median(Vf0)
    return VV, Vfil
