import datetime
import numpy as np
from maser.data import Data

my_data=Data('/home/atokgozoglu/Documents/formationPython/solo_L2_rpw-lfr-surv-bp1_20211127_V01.cdf')
xarray=my_data.as_xarray()
_xarray_=xarray
voltage=xarray['PE']

for i in voltage:
    print (i)

times=my_data.times

for key in xarray:
    print(key)

#print (xarray['DOP']['N_F2'].values)

z=np.nan

#xarray['DOP']['N_F2'].values[0]=z

#print(xarray['DOP']['N_F2'].values[1236])


dic={}


for key in voltage:
    for index_time,time in enumerate (times[key]):
        if times[key][index_time]-times[key][index_time-1]>datetime.timedelta(hours=1):
            dic[index_time-1]=time
            for physic_key in xarray:
                _xarray_[physic_key][key].values[:,index_time-1]=np.nan
                _xarray_[physic_key][key].values[:,index_time]=np.nan

print (np.shape(_xarray_['PE']['N_F2'].values))
print(_xarray_['PE']['N_F2'].values[:,1236])



