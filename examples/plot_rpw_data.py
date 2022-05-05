from tests.constants import BASEDIR
from matplotlib import pyplot as plt
from astropy.visualization import quantity_support, time_support
from astropy.time import Time

demo_filepath = BASEDIR / "rpw" / "solo_L2_rpw-lfr-surv-bp1_20201227_V02.cdf"
from maser.data import Data

with Data(filepath=demo_filepath) as data:
    sweeps = list(data.sweeps)
    print(sweeps[0:5])
    with quantity_support():
        for values, time, frequencies in sweeps[0:5]:
            # plt.plot(sweep[2].to(Unit("Hz")), sweep[0])
            plt.pcolormesh(time, frequencies, values['DOP'], cmap='RdBu')
        plt.colorbar()
        plt.show()