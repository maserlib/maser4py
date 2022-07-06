
import datetime
from maser.data.rpw.tnr import RpwTnrSurv
from maser.data import Data
import numpy as np
import matplotlib.pyplot as plt


def cross_time(tnr_filepath,lfr_filepath,mode,margin=5,desired_time=datetime.datetime(2021,10,28,0,0,0,0)):
   
    my_tnr_data=Data(filepath=tnr_filepath)
    my_lfr_data=Data(filepath=lfr_filepath)
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

    frequencies=np.hstack((freq[0],freq[1]))
    frequencies=np.hstack((frequencies,freq[2]))
    frequencies=np.hstack((frequencies,freq[3]))

    index_tnr=0

    while np.abs(desired_time-times[0][index_tnr])>datetime.timedelta(seconds=margin):
        index_tnr=index_tnr+1


    print(index_tnr)
    print(times[0][index_tnr])
    print(times[1][index_tnr])
    print(times[2][index_tnr])
    print(times[3][index_tnr])

    Auto_A=auto[0][index_tnr]
    Auto_B=auto[1][index_tnr]
    Auto_C=auto[2][index_tnr]
    Auto_D=auto[3][index_tnr]

    Auto=np.hstack((Auto_A,Auto_B))
    Auto=np.hstack((Auto,Auto_C))
    Auto=np.hstack((Auto,Auto_D))

    print(Auto)
    print(frequencies)
    print(np.size(Auto))
    print(np.size(frequencies))
    print(Auto.max())

    Auto=10*np.log10(Auto)

    #plt.plot(frequencies,Auto)
    #plt.show()
    

    xarray_lfr=my_lfr_data.as_xarray()

    voltage=xarray_lfr["PE"]

    freq_lfr=my_lfr_data.frequencies
    times_lfr=my_lfr_data.times

    index_lfr_N=0
    index_lfr_B=0

    if mode==0:
        freq_N=np.hstack((freq_lfr["N_F2"],freq_lfr["N_F1"]))
        freq_N=np.hstack((freq_N,freq_lfr["N_F0"]))
        voltage_N_F0=voltage["N_F0"].T
        voltage_N_F1=voltage["N_F1"].T
        voltage_N_F2=voltage["N_F2"].T
        while np.abs(desired_time-times_lfr["N_F2"][index_lfr_N])>datetime.timedelta(seconds=margin):
            index_lfr_N=index_lfr_N+1
        voltage_N=np.hstack((voltage_N_F2[index_lfr_N],voltage_N_F1[index_lfr_N]))
        voltage_N=np.hstack((voltage_N,voltage_N_F0[index_lfr_N]))
        voltage_N=10*np.log10(voltage_N)
        plt.plot(freq_N,voltage_N)

    if mode==1:
        freq_B=np.hstack((freq_lfr["B_F1"],freq_lfr["B_F0"]))
        voltage_B_F0=voltage["B_F0"].T
        voltage_B_F1=voltage["B_F1"].T
        times_B_F0=times_lfr["B_F0"].T
        times_B_F1=times_lfr["B_F1"].T
        #print(times_B_F0)
        while np.abs(desired_time-times_B_F0[index_lfr_B])>datetime.timedelta(seconds=margin-1):
            index_lfr_B=index_lfr_B +1
        print (times_B_F0[index_lfr_B])
        print (times_B_F1[index_lfr_B])
        voltage_B=np.hstack((voltage_B_F1[index_lfr_B],voltage_B_F0[index_lfr_B]))
        voltage_B=10*np.log10(voltage_B)
        print(voltage_B)
        print(freq_B)
        t_lfr=times_B_F0[index_lfr_B]
        plt.plot(freq_B,voltage_B,label=t_lfr)
        plt.legend()

    plt.plot(frequencies,Auto,label=times[0][index_tnr])
    plt.legend()
    plt.xlabel('frequencies')
    plt.ylabel('V^2/Hz (DB)')
    plt.title(desired_time)
    #plt.yscale('log')
    plt.xscale('log')
    print(times_B_F0[index_lfr_B])
    print(times[0][index_tnr])
    plt.show()

        
        


    









cross_time('/home/atokgozoglu/Documents/formationPython/solo_L2_rpw-tnr-surv_20201227_V01.cdf','/home/atokgozoglu/Documents/Maser/maser-data/maser/data/rpw/solo_L2_rpw-lfr-surv-bp1_20201227_V02.cdf'
            ,mode=1,margin=2,desired_time=datetime.datetime(2020,12,27,12,58,1,1))


# REMARQUE: LA CORRESPONDANCE DEPEND BIEN DU TEMPS ................
