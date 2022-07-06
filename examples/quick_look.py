from maser.data import Data
from maser.data.rpw.quick_look_tnr_lfr_corrections import quick_look_tnr_lfr_argparse, quick_look_tnr_lfr_corrections, quick_look_tnr_lfr_final, quick_look_tnr_lfr_final_PE_PB_DOP, quick_look_tnr_lfr_final_bis, quick_look_tnr_lfr_fusion, quick_look_tnr_lfr_only_E, quick_look_tnr_lfr_only_E_white, quick_look_tnr_lfr_wo_F0

#quick_look_tnr_lfr_final_bis('/home/atokgozoglu/Documents/formationPython/solo_L2_rpw-tnr-surv_20200711_V03.cdf',
                            #'/home/atokgozoglu/Documents/formationPython/solo_L2_rpw-lfr-surv-bp1_20200711_V04.cdf')


tnrpath='/home/atokgozoglu/Documents/cdfsss/solo_L2_rpw-tnr-surv_20220118_V02.cdf'
lfrpath='/home/atokgozoglu/Documents/cdfsss/solo_L2_rpw-lfr-surv-bp1_20220118_V02.cdf'








quick_look_tnr_lfr_argparse(tnrpath,
                        lfrpath,'/home/atokgozoglu/Documents/captureecran/xd')

#quick_look_tnr_lfr_final(tnrpath,lfrpath)


#quick_look_tnr_lfr_final_bis('/home/atokgozoglu/Documents/Maser/maser-data/maser/data/rpw/solo_L2_rpw-tnr-surv_20210701_V01.cdf'
                            #,'/home/atokgozoglu/Documents/formationPython/solo_L2_rpw-lfr-surv-bp1_20210701_V03.cdf')



#quick_look_tnr_lfr_only_E_white( tnrpath,lfrpath)