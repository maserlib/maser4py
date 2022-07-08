# -*- coding: utf-8 -*-
import numpy


def fft_filter(x1, tlow, tup):  # x1 represente l'entrée (auto)
    npp = numpy.size(x1)  # taille de l'entrée
    yfo = numpy.fft.ifft(x1)  # Fourier discret + ifft
    yyf0 = yfo[0]  # recuperation de la premiere valeur f0
    freq = numpy.arange(
        float((npp - 1) / 2) + 1.0
    )  # numpy.arange([start, ]stop, [step, ]dtype=None, *, like=None) Return evenly spaced values within a given interval.
    freq = freq / (npp)
    if (numpy.mod(npp, 2)) == 0:
        yyf0 = yfo[0]
        freq = numpy.arange(float(npp / 2) + 1.0)
        freq[0 : int(npp / 2)] = freq[0 : int(npp / 2)] / (npp)
        freq[int(npp / 2)] = 1.0 / (2.0)
    fup = tup / npp
    flow = tlow / (npp)
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
    Mask and filter data to remove artifacts

    Note: output data are in log scale
    """

    ndim = numpy.shape(V)
    Vf = (ndim[0], ndim[1])
    Vf = numpy.zeros(Vf)
    Vf0 = (ndim[0], ndim[1])
    Vf0 = numpy.zeros(Vf0)

    V2o = 10.0 * numpy.log10(V)
    V2 = V2o
    nap = numpy.isinf(V2o)

    for ii in range(128):
        napp = nap[ii, :]
        V2[ii, napp] = numpy.mean(V2o[numpy.isfinite(V2o)])

    for ii in range(128):
        x = numpy.squeeze(V2[ii, :])
        outf = fft_filter(x, tlow, tup)
        xf = outf[0]
        xfnull = outf[1]
        Vf[ii, :] = xf
        Vf0[ii, :] = xfnull

    V[75:80, :] = 1e-25
    V[85:86, :] = 1e-25
    V[103:104, :] = 1e-25
    V[110:111, :] = 1e-25
    V[115:116, :] = 1e-25
    V[118:119, :] = 1e-25

    VV = 10.0 * numpy.log10(V)

    Vfil = Vf + numpy.median(Vf0)
    return VV, Vfil
