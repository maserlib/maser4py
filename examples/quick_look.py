# -*- coding: utf-8 -*-
from maser.data.rpw.quick_look_tnr_lfr_corrections import (
    quick_look_tnr_lfr_argparse,
)


tnrpath = "/home/atokgozoglu/Documents/cdfsss/solo_L2_rpw-tnr-surv_20220118_V02.cdf"
lfrpath = "/home/atokgozoglu/Documents/cdfsss/solo_L2_rpw-lfr-surv-bp1_20220118_V02.cdf"


quick_look_tnr_lfr_argparse(
    tnrpath, lfrpath, "/home/atokgozoglu/Documents/captureecran/xd"
)
