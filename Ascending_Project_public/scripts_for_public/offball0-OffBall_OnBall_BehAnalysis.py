import numpy as np
import os
import sys
import pickle
import matplotlib.pyplot as plt
plt.switch_backend('agg')

import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.math_utils as math_utils
import utils.sync_utils as sync_utils
import utils.EventDetection_utils as EventDetection_utils
import utils.list_twoP_exp as list_twoP_exp








def save_offball_move_rest_dic(filename='offball_move_rest_dic.p'):


	dicData={}

	# Proboscis original coordinate
	dicData.update({'rest':rest_bin_trace})
	dicData.update({'move':move_bin_trace})

	pickle.dump( dicData, open( outDir_hangedfly + filename, "wb" ) ) 


	return
	





off_ball_active_lines_ONBALL=list_twoP_exp.off_ball_active_lines_ONBALL
off_ball_active_lines_OFFBALL=list_twoP_exp.off_ball_active_lines_OFFBALL


experiments=off_ball_active_lines_ONBALL+off_ball_active_lines_OFFBALL



NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_Dir

hanged_fly_beh_filename='beh_rest_move_hangedFly.p'


for date, genotype, fly, recrd_num in experiments:


	Gal4=genotype.split('-')[0]
	fly_beh=fly[0].upper()+fly[1:]

	outDir_AN_recrd=NAS_AN_Proj_Dir+Gal4+'/2P/'+date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num+'/output/'
	fly_beh=fly[0].upper()+fly[1:]
	CamDir = NAS_Dir+'CLC/'+date[2:]+'_'+genotype+'/'+fly+'/'+'CO2xzGG/behData_'+recrd_num+'/images/'



	outDir_hangedfly=outDir_AN_recrd+'hanged_fly_analysis/'
	if not os.path.exists(outDir_hangedfly):
		os.makedirs(outDir_hangedfly)

	print('outDir_hangedfly', outDir_hangedfly)

	print('outDir_AN_recrd+hanged_fly_beh_filename', outDir_AN_recrd+hanged_fly_beh_filename)



	camPhoto_stacks=general_utils.import_camPhotos_into_stack(CamDir, cam_num=6)
	print('type camPhoto_stacks', type(camPhoto_stacks))

	rest_bin_trace, move_bin_trace=EventDetection_utils.detect_moving_resting_hangedfly_from_sideCam_video(camPhoto_stacks, outDir_hangedfly, var_thrsld=2.3, corner_dur_s=1, crop=True)

	# bool_rest_trace=np.array(rest_bin_trace)>0.tolist()
	# bool_move_trace=np.array(move_bin_trace)>0.tolist()

	# print('bool_rest_trace', bool_rest_trace)

	save_offball_move_rest_dic(filename=hanged_fly_beh_filename)












	# #Beh_Jpos_GC_DicData=general_utils.open_Beh_Jpos_GC_DicData(outDir_AN_recrd, 'SyncDic_7CamBeh_BW_20210619_GC-RES.p')












