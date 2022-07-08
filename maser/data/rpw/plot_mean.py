# -*- coding: utf-8 -*-
import datetime
from maser.data import Data
import numpy as np
import matplotlib.pyplot as plt


def plot_mean(
    tnr_filepath,
    lfr_filepath,
    mode,
    margin=5,
    desired_time_start=datetime.datetime(2021, 10, 28, 0, 0, 0, 0),
    desired_time_end=datetime.datetime(2021, 10, 28, 23, 59, 59, 0),
):

    my_tnr_data = Data(filepath=tnr_filepath)
    my_lfr_data = Data(filepath=lfr_filepath)
    my_tnr_data._init_

    dic_data = my_tnr_data.datas_dic_per_band()
    auto = {
        0: dic_data[0]["Auto"],
        1: dic_data[1]["Auto"],
        2: dic_data[2]["Auto"],
        3: dic_data[3]["Auto"],
    }  # one dictionary for auto
    times = {
        0: dic_data[0]["Times"],
        1: dic_data[1]["Times"],
        2: dic_data[2]["Times"],
        3: dic_data[3]["Times"],
    }  # one dictionary for times

    freq = {
        0: my_tnr_data.frequenciesA,
        1: my_tnr_data.frequenciesB,
        2: my_tnr_data.frequenciesC,
        3: my_tnr_data.frequenciesD,
    }

    frequencies = np.hstack((freq[0], freq[1]))
    frequencies = np.hstack((frequencies, freq[2]))
    frequencies = np.hstack((frequencies, freq[3]))

    index_tnr_start = 0

    while np.abs(desired_time_start - times[0][index_tnr_start]) > datetime.timedelta(
        seconds=margin
    ):
        index_tnr_start = index_tnr_start + 1

    index_tnr_end = index_tnr_start

    while np.abs(desired_time_end - times[0][index_tnr_end]) > datetime.timedelta(
        seconds=margin
    ):
        index_tnr_end = index_tnr_end + 1

    times_A = times[0][index_tnr_start : index_tnr_end + 1]
    times_B = times[1][index_tnr_start : index_tnr_end + 1]
    times_C = times[2][index_tnr_start : index_tnr_end + 1]
    times_D = times[3][index_tnr_start : index_tnr_end + 1]


    Auto_A = auto[0][index_tnr_start:index_tnr_end, :]
    Auto_B = auto[1][index_tnr_start:index_tnr_end, :]
    Auto_C = auto[2][index_tnr_start:index_tnr_end, :]
    Auto_D = auto[3][index_tnr_start:index_tnr_end, :]

    Auto_A_mean = np.mean(Auto_A, 0)
    Auto_B_mean = np.mean(Auto_B, 0)
    Auto_C_mean = np.mean(Auto_C, 0)
    Auto_D_mean = np.mean(Auto_D, 0)

    Auto_mean = np.hstack((Auto_A_mean, Auto_B_mean))
    Auto_mean = np.hstack((Auto_mean, Auto_C_mean))
    Auto_mean = np.hstack((Auto_mean, Auto_D_mean))

    Auto_mean = 10 * np.log10(Auto_mean)

    xarray_lfr = my_lfr_data.as_xarray()

    voltage = xarray_lfr["PE"]

    freq_lfr = my_lfr_data.frequencies
    times_lfr = my_lfr_data.times

    index_lfr_N_start = 0
    index_lfr_B_start = 0

    if mode == 0:
        freq_N = np.hstack((freq_lfr["N_F2"], freq_lfr["N_F1"]))
        freq_N = np.hstack((freq_N, freq_lfr["N_F0"]))
        voltage_N_F0 = voltage["N_F0"].T
        voltage_N_F1 = voltage["N_F1"].T
        voltage_N_F2 = voltage["N_F2"].T
        times_N_F1 = times_lfr["N_F1"].T
        while np.abs(
            desired_time_start - times_N_F1[index_lfr_N_start]
        ) > datetime.timedelta(seconds=margin):
            index_lfr_N_start = index_lfr_N_start + 1
        index_lfr_N_end = index_lfr_N_start
        while np.abs(
            desired_time_end - times_N_F1[index_lfr_N_end]
        ) > datetime.timedelta(seconds=margin):
            index_lfr_N_end = index_lfr_N_end + 1
        voltage_N_F2 = voltage_N_F2[index_lfr_N_start : index_lfr_N_end + 1]
        voltage_N_F1 = voltage_N_F1[index_lfr_N_start : index_lfr_N_end + 1]
        voltage_N_F0 = voltage_N_F0[index_lfr_N_start : index_lfr_N_end + 1]
        voltage_N_F2_mean = np.mean(voltage_N_F2.values, 0)
        voltage_N_F1_mean = np.mean(voltage_N_F1.values, 0)
        voltage_N_F0_mean = np.mean(voltage_N_F0.values, 0)
        voltage_N_mean = np.hstack((voltage_N_F2_mean, voltage_N_F1_mean))
        voltage_N_mean = np.hstack((voltage_N_mean, voltage_N_F0_mean))
        voltage_N_mean = 10 * np.log10(voltage_N_mean)
        plt.plot(freq_N, voltage_N_mean)


    if mode == 1:
        freq_B = np.hstack((freq_lfr["B_F1"], freq_lfr["B_F0"]))
        voltage_B_F0 = voltage["B_F0"].T
        voltage_B_F1 = voltage["B_F1"].T
        times_B_F0 = times_lfr["B_F0"].T
        times_B_F1 = times_lfr["B_F1"].T

        while np.abs(
            desired_time_start - times_B_F0[index_lfr_B_start]
        ) > datetime.timedelta(seconds=margin):
            index_lfr_B_start = index_lfr_B_start + 1
        index_lfr_B_end = index_lfr_B_start
        while np.abs(
            desired_time_end - times_B_F0[index_lfr_B_end]
        ) > datetime.timedelta(seconds=margin):
            index_lfr_B_end = index_lfr_B_end + 1

        voltage_B_F1 = voltage_B_F1[index_lfr_B_start : index_lfr_B_end + 1]
        voltage_B_F0 = voltage_B_F0[index_lfr_B_start : index_lfr_B_end + 1]
        voltage_B_F1_mean = np.mean(voltage_B_F1.values, 0)
        voltage_B_F0_mean = np.mean(voltage_B_F0.values, 0)
        voltage_B_mean = np.hstack((voltage_B_F1_mean, voltage_B_F0_mean))
        print(np.shape(voltage_B_mean))
        print(freq_B)
        voltage_B_mean = 10 * np.log10(voltage_B_mean)
        plt.plot(freq_B, voltage_B_mean)

    plt.plot(frequencies, Auto_mean)
    plt.xlabel("frequencies")
    plt.ylabel("V^2/Hz")
    plt.xscale("log")
    plt.title(desired_time_start)
    plt.show()


plot_mean(
    "/home/atokgozoglu/Documents/Maser/maser-data/maser/data/rpw/solo_L2_rpw-tnr-surv_20210701_V01.cdf",
    "/home/atokgozoglu/Documents/formationPython/solo_L2_rpw-lfr-surv-bp1_20210701_V03.cdf",
    mode=0,
    margin=19,
    desired_time_start=datetime.datetime(2021, 7, 1, 0, 49, 44, 1),
    desired_time_end=datetime.datetime(2021, 7, 1, 5, 50, 55, 1),
)
