import sys
import pickle
#import sys
import os
import re
import numpy as np
import pandas as pd
import random
from PIL import Image
Image.Image.tostring = Image.Image.tobytes
import matplotlib
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from skimage import io
from multiprocessing import Pool
import math
import more_itertools as mit
import time
from matplotlib import colors as mcolors
import scipy
import scikit_posthocs
from statsmodels.stats import weightstats as stests


import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.plot_setting as plot_setting
import utils.math_utils as math_utils
import utils.sync_utils as sync_utils

import utils.list_twoP_exp as list_twoP_exp




TwoP_recordings_sparseLine_list=list_twoP_exp.TwoP_recordings_sparseLine_list

Representative_TwoP_recordings_sparseLine_list=[



('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '001'), # no video
('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '002'),
('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '003'),
('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '004'),
('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '005'),
('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '006'),


('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '001'), # no video
('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '002'), # no video
('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '003'), # no video
('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '004'),
('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '005'),
('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '006'),
('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '007'),
('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '008'),
('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '009'),

('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '001'), 
('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '002'), 
('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '003'),
('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '004'),
('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '005'),
('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '006'),
('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '007'),
('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '008'),


('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '001'),
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '002'),
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '004'),
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '005'),
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '006'), 
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '007'),
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '008'),
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '009'),
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '010'),
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '011'),
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '012'),
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '013'),

('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '001'), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '002'), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '003'), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '004'), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '005'), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '006'), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '007'), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '008'), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '009'), # no video


('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '001'),
('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '002'),
('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '003'),
('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '004'),
('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '005'),
('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '006'),
('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '007'),
('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '008'),
('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '009'),


('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '001'),
('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '002'),
('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '003'),
('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '004'),
('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '005'), # no video
('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '006'), # no video


]

# experiments=TwoP_recordings_sparseLine_list
experiments=Representative_TwoP_recordings_sparseLine_list
 



##main##

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_public_Dir
workstation_dir=general_utils.workstation_dir



experiments_group_per_fly=general_utils.group_expList_per_fly(Representative_TwoP_recordings_sparseLine_list)
print('experiments_group_per_fly', experiments_group_per_fly)





ROI_id_list=[] #[Gal4-neuron (1 x n)]


count_ROI=0
count_fly=0
count_recrd=0
num_ROI_ls=[]

print('\n#counting ROIs#\n')
for exp_lists_per_fly in experiments_group_per_fly:

	print('exp_lists_per_fly', exp_lists_per_fly)

	count_recrd+=len(exp_lists_per_fly)

	for date, genotype, fly, recrd_num in exp_lists_per_fly:


		Gal4=genotype.split('-')[0]
		fly_beh=fly[0].upper()+fly[1:]

		outDir_AN_recrd=NAS_AN_Proj_Dir+'03_general_2P_exp/'+Gal4+'/2P/'+date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num+'/output'
		print('outDir_AN_recrd', outDir_AN_recrd)


		Beh_Jpos_GC_DicData=general_utils.open_Beh_Jpos_GC_DicData(outDir_AN_recrd, 'SyncDic_7CamBeh_BW_20210619_GC-RES.p')


		GC_set = Beh_Jpos_GC_DicData['GCset']
	
		count_ROI+=len(GC_set)
		
		
		
		num_ROI_ls.append(len(GC_set))	

		for neuron_ID in range(len(GC_set)):
			ROI_id_list.append(Gal4+'-ROI#'+str(neuron_ID))


		break



	count_fly+=1


print('There are ', count_fly, 'flys in total...')
print('There are ', count_ROI, 'ROIs in total...')
print('There are ', count_recrd, 'recordings in total...')

print('ROI_id_list', ROI_id_list)





for exp_lists_per_fly in experiments_group_per_fly:
	print('Processing per fly for ... ', exp_lists_per_fly )


	Etho_time_fly_Dic={}
	Etho_time_fly_Dic['FW_evt']=[]
	Etho_time_fly_Dic['BW_evt']=[]
	Etho_time_fly_Dic['rest_evt']=[]
	Etho_time_fly_Dic['E_groom_evt']=[]
	Etho_time_fly_Dic['A_groom_evt']=[]
	Etho_time_fly_Dic['FL_groom_evt']=[]
	Etho_time_fly_Dic['HL_groom_evt']=[]
	Etho_time_fly_Dic['Abd_groom_evt']=[]
	Etho_time_fly_Dic['PER_evt']=[]
	Etho_time_fly_Dic['Push_evt']=[]
	Etho_time_fly_Dic['CO2puff_evt']=[]

	Etho_time_fly_Dic['F_groom_evt']=[]
	Etho_time_fly_Dic['H_groom_evt']=[]
	Etho_time_fly_Dic['SixLeg_Move_evt']=[]



	F_Walk_GCevt_fly=[]
	B_Walk_GCevt_fly=[]
	Rest_GCevt_fly=[]
	E_groom_GCevt_fly=[]
	A_groom_GCevt_fly=[]
	FL_groom_GCevt_fly=[]
	HL_groom_GCevt_fly=[]
	Abd_groom_GCevt_fly=[]
	PER_GCevt_fly=[]
	Push_GCevt_fly=[]
	CO2puff_GCevt_fly=[]

	F_groom_GCevt_fly=[]
	H_groom_GCevt_fly=[]
	SixLeg_Move_GCevt_fly=[]



	F_Walk_GCevtNorm01_fly=[]
	B_Walk_GCevtNorm01_fly=[]
	Rest_GCevtNorm01_fly=[]
	E_groom_GCevtNorm01_fly=[]
	A_groom_GCevtNorm01_fly=[]
	FL_groom_GCevtNorm01_fly=[]
	HL_groom_GCevtNorm01_fly=[]
	Abd_groom_GCevtNorm01_fly=[]
	PER_GCevtNorm01_fly=[]
	Push_GCevtNorm01_fly=[]
	CO2puff_GCevtNorm01_fly=[]

	F_groom_GCevtNorm01_fly=[]
	H_groom_GCevtNorm01_fly=[]
	SixLeg_Move_GCevtNorm01_fly=[]



	GC_gapfree_fly=[]
	GC_all_fly_perROI=[]
	GCnorm01_all_fly_perROI=[]



	maxGC_fly=[]
	minGC_fly=[]

	recrdcount=0
	i=0
	#todo: append individual GC event into these array for summarize all data

	### Find the max GC per fly
	GC_fly_preSum=[]
	for date, genotype, fly, recrd_num in exp_lists_per_fly:
		Gal4=genotype.split('-')[0]
		dataDir = NAS_AN_Proj_Dir + '03_general_2P_exp/' +Gal4 +'/2P/' + date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num + '/'
		outDirGC6_axoid = dataDir+'/output/GC6_auto/final/'
		GC_set = general_utils.readGCfile(outDirGC6_axoid)

		data_rawGC_freq=4

		if len(GC_fly_preSum)<len(GC_set):
			for roi_i, trace in enumerate(GC_set):
				GC_fly_preSum.append([])
		for roi_i, trace in enumerate(GC_set):
			GC_trace=math_utils.smooth_data(trace, windowlen=int(data_rawGC_freq*0.7)) # original = 0.7
			GC_fly_preSum[roi_i].extend(GC_trace)


	maxGC_fly=np.nanmax(GC_fly_preSum, axis=1)
	print('maxGC_fly', maxGC_fly)






	for date, genotype, fly, recrd_num in exp_lists_per_fly:

		Gal4=genotype.split('-')[0]

		flyDir = NAS_AN_Proj_Dir + '03_general_2P_exp/' + Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'
		dataDir = NAS_AN_Proj_Dir + '03_general_2P_exp/' + Gal4 +'/2P/' + date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num + '/'
		pathForDic = dataDir+'/output/'

		print('dataDir', dataDir)


		Plot_overlay_each_recrd=False
		if Plot_overlay_each_recrd==True:

			outDirEvents = NAS_AN_Proj_Dir + 'output/Fig4b_5b_6b_7d_8b_9b-Beh_avgDFF/'+ Gal4 +'/'+Gal4+'-'+genotype+'-'+fly+'-'+recrd_num + '/'
			if not os.path.exists(outDirEvents):
				os.makedirs(outDirEvents)


		outDirEventsSumFly = NAS_AN_Proj_Dir + 'output/Fig4b_5b_6b_7d_8b_9b-Beh_avgDFF/'+Gal4+'/Summary_Fly/'
		if not os.path.exists(outDirEventsSumFly):
			os.makedirs(outDirEventsSumFly)


	


		Beh_Jpos_GC_DicData=general_utils.open_Beh_Jpos_GC_DicData(pathForDic, 'SyncDic_7CamBeh_BW_20210619_GC-RES.p')



		GC_set = Beh_Jpos_GC_DicData['GCset']

		rest = Beh_Jpos_GC_DicData['rest']
		f_walk = Beh_Jpos_GC_DicData['forward_walk']
		b_walk = Beh_Jpos_GC_DicData['backward_walk']
		eye_groom = Beh_Jpos_GC_DicData['eye_groom']
		antennae_groom = Beh_Jpos_GC_DicData['antennae_groom']
		foreleg_groom = Beh_Jpos_GC_DicData['foreleg_groom']
		hindleg_groom = Beh_Jpos_GC_DicData['hindleg_groom']
		Abd_groom = Beh_Jpos_GC_DicData['Abd_groom']
		Push = Beh_Jpos_GC_DicData['Push']	
		PER=Beh_Jpos_GC_DicData['PER']

		CO2puff = Beh_Jpos_GC_DicData['CO2puff']
		PER_exten_len = Beh_Jpos_GC_DicData['PER_exten_len']

		F_groom = Beh_Jpos_GC_DicData['F_groom']
		H_groom = Beh_Jpos_GC_DicData['H_groom']
		print('type H_groom', type(H_groom))

		F_groom = np.asarray(eye_groom)+np.asarray(foreleg_groom)
		SixLeg_move = np.asarray(f_walk)+np.asarray(b_walk)+np.asarray(Push)
		print('type SixLeg_move', type(SixLeg_move))
		


		timeSec = Beh_Jpos_GC_DicData['timeSec']
		velForw_mm = Beh_Jpos_GC_DicData['velForw']
		velSide_mm = Beh_Jpos_GC_DicData['velSide']
		velTurn_deg = Beh_Jpos_GC_DicData['velTurn']



		Etho_Timesec_Dic = Beh_Jpos_GC_DicData['Etho_Timesec_Dic']
		Etho_Idx_Dic = Beh_Jpos_GC_DicData['Etho_Idx_Dic']

		data_freq=len(rest)/timeSec[-1]
		print('data_freq', data_freq)



		F_Walk_LP=math_utils.hysteresis_filter(f_walk, n=int(data_freq*0.5))*1
		B_Walk_LP=math_utils.hysteresis_filter(b_walk, n=int(data_freq*0.5))*1
		Rest_LP=math_utils.hysteresis_filter(rest, n=int(data_freq*0.5))*1
		E_Groom_LP=math_utils.hysteresis_filter(eye_groom, n=int(data_freq*0.5))*1
		A_Groom_LP=math_utils.hysteresis_filter(antennae_groom, n=int(data_freq*0.5))*1
		FL_Groom_LP=math_utils.hysteresis_filter(foreleg_groom, n=int(data_freq*0.6))*1
		HL_Groom_LP=math_utils.hysteresis_filter(hindleg_groom, n=int(data_freq*0.5))*1
		Abd_Groom_LP=math_utils.hysteresis_filter(Abd_groom, n=int(data_freq*0.5))*1
		Push_LP=math_utils.hysteresis_filter(Push, n=int(data_freq*0.5))*1

		H_Groom_LP=math_utils.hysteresis_filter(H_groom, n=int(data_freq*0.5))*1
		F_Groom_LP=math_utils.hysteresis_filter(F_groom, n=int(data_freq*0.5))*1	
		SixLeg_move_LP = math_utils.hysteresis_filter(SixLeg_move, n=int(data_freq*0.5))*1	




		idx_f_walk_evt, timesec_f_walk_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(F_Walk_LP, timeSec)
		idx_b_walk_evt, timesec_b_walk_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(B_Walk_LP, timeSec)
		idx_rest_evt, timesec_rest_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(Rest_LP, timeSec)
		idx_E_groom_evt, timesec_E_groom_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(E_Groom_LP, timeSec)
		idx_A_groom_evt, timesec_A_groom_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(A_Groom_LP, timeSec)
		idx_FL_groom_evt, timesec_FL_groom_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(FL_Groom_LP, timeSec)
		idx_HL_groom_evt, timesec_HL_groom_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(HL_Groom_LP, timeSec)
		idx_Abd_groom_evt, timesec_Abd_groom_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(Abd_Groom_LP, timeSec)
		idx_Push_evt, timesec_Push_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(Push_LP, timeSec)
		idx_PER_evt, timesec_PER_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(PER, timeSec)
		idx_CO2puff_evt, timesec_CO2puff_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(CO2puff, timeSec)

		idx_H_groom_evt, timesec_H_groom_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(H_Groom_LP, timeSec)	
		idx_F_groom_evt, timesec_F_groom_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(F_Groom_LP, timeSec)
		idx_SixLeg_move_evt, timesec_SixLeg_move_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(SixLeg_move_LP, timeSec)



		EthoLP_Idx_Dic={}
		EthoLP_Idx_Dic.update({'rest_evt':idx_rest_evt})
		EthoLP_Idx_Dic.update({'FW_evt':idx_f_walk_evt})
		EthoLP_Idx_Dic.update({'BW_evt':idx_b_walk_evt})
		EthoLP_Idx_Dic.update({'E_groom_evt':idx_E_groom_evt})
		EthoLP_Idx_Dic.update({'A_groom_evt':idx_A_groom_evt})
		EthoLP_Idx_Dic.update({'FL_groom_evt':idx_FL_groom_evt})
		EthoLP_Idx_Dic.update({'HL_groom_evt':idx_HL_groom_evt})
		EthoLP_Idx_Dic.update({'Abd_groom_evt':idx_Abd_groom_evt})
		EthoLP_Idx_Dic.update({'PER_evt':idx_PER_evt})
		EthoLP_Idx_Dic.update({'Push_evt':idx_Push_evt})
		EthoLP_Idx_Dic.update({'CO2puff_evt':idx_CO2puff_evt})

		EthoLP_Idx_Dic.update({'F_groom_evt':idx_F_groom_evt})
		EthoLP_Idx_Dic.update({'H_groom_evt':idx_H_groom_evt})	
		EthoLP_Idx_Dic.update({'SixLeg_Move_evt':idx_SixLeg_move_evt})	


		EthoLP_Timesec_Dic={}
		EthoLP_Timesec_Dic.update({'rest_evt':timesec_rest_evt})
		EthoLP_Timesec_Dic.update({'FW_evt':timesec_f_walk_evt})
		EthoLP_Timesec_Dic.update({'BW_evt':timesec_b_walk_evt})
		EthoLP_Timesec_Dic.update({'E_groom_evt':timesec_E_groom_evt})
		EthoLP_Timesec_Dic.update({'A_groom_evt':timesec_A_groom_evt})
		EthoLP_Timesec_Dic.update({'FL_groom_evt':timesec_FL_groom_evt})
		EthoLP_Timesec_Dic.update({'HL_groom_evt':timesec_HL_groom_evt})
		EthoLP_Timesec_Dic.update({'Abd_groom_evt':timesec_Abd_groom_evt})
		EthoLP_Timesec_Dic.update({'PER_evt':timesec_PER_evt})
		EthoLP_Timesec_Dic.update({'Push_evt':timesec_Push_evt})
		EthoLP_Timesec_Dic.update({'CO2puff_evt':timesec_CO2puff_evt})

		EthoLP_Timesec_Dic.update({'F_groom_evt':timesec_F_groom_evt})
		EthoLP_Timesec_Dic.update({'H_groom_evt':timesec_H_groom_evt})
		EthoLP_Timesec_Dic.update({'SixLeg_Move_evt':timesec_SixLeg_move_evt})		


		# Plot_overlay_each_recrd=False
		# if Plot_overlay_each_recrd==True:
		# 	plot_utils.Plot_whole_trace(GC_set, CO2puff, PER_exten_len, timeSec, velForw_mm, velSide_mm, velTurn_deg, EthoLP_Timesec_Dic, 'whole_trace_7CamBeh_BW_20210619', filepath=outDirEvents)


		GC_set_norm01=[]

		for ROI_i, GC_trace in enumerate(GC_set):
			GC_trace=math_utils.smooth_data(GC_trace, windowlen=int(data_freq*0.7)) # original = 0.7
			#GC_trace=math_utils.norm_to_max(GC_trace, percentile_th_to_norm=100)
			GC_trace=math_utils.norm_to_val(GC_trace, val=maxGC_fly[ROI_i])
			GC_set_norm01.append(GC_trace)

		# GC_set=GC_set_norm01



		bsl_s=1 #s
		event_dur_s=3 #s

		GC_rest_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'rest_evt', GC_set, baseline=bsl_s, fps=data_freq)
		GC_f_walk_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'FW_evt', GC_set, baseline=bsl_s, fps=data_freq)
		GC_b_walk_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'BW_evt', GC_set, baseline=bsl_s, fps=data_freq)
		GC_E_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'E_groom_evt', GC_set, baseline=bsl_s, fps=data_freq)
		GC_A_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'A_groom_evt', GC_set, baseline=bsl_s, fps=data_freq)
		GC_FL_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'FL_groom_evt', GC_set, baseline=bsl_s, fps=data_freq)
		GC_HL_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'HL_groom_evt', GC_set, baseline=bsl_s, fps=data_freq)
		GC_Abd_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'Abd_groom_evt', GC_set, baseline=bsl_s, fps=data_freq)
		GC_Push_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'Push_evt', GC_set, baseline=bsl_s, fps=data_freq)

		GC_PER_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'PER_evt', GC_set, baseline=bsl_s, fps=data_freq)
		GC_CO2puff_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'CO2puff_evt', GC_set, baseline=bsl_s, fps=data_freq)

		GC_F_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'F_groom_evt', GC_set, baseline=bsl_s, fps=data_freq)
		GC_H_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'H_groom_evt', GC_set, baseline=bsl_s, fps=data_freq)
		GC_SixLeg_Move_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'SixLeg_Move_evt', GC_set, baseline=bsl_s, fps=data_freq)


		GCnorm01_rest_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'rest_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)
		GCnorm01_f_walk_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'FW_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)
		GCnorm01_b_walk_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'BW_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)
		GCnorm01_E_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'E_groom_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)
		GCnorm01_A_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'A_groom_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)
		GCnorm01_FL_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'FL_groom_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)
		GCnorm01_HL_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'HL_groom_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)
		GCnorm01_Abd_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'Abd_groom_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)
		GCnorm01_Push_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'Push_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)

		GCnorm01_PER_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'PER_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)
		GCnorm01_CO2puff_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'CO2puff_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)

		GCnorm01_F_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'F_groom_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)
		GCnorm01_H_groom_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'H_groom_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)
		GCnorm01_SixLeg_Move_evt_set, _ =general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'SixLeg_Move_evt', GC_set_norm01, baseline=bsl_s, fps=data_freq)



		for neuron_idx, GC_per_neruon in enumerate(GC_set):
			if len(F_Walk_GCevt_fly)!=len(GC_set): 
				F_Walk_GCevt_fly.append([])
				F_Walk_GCevtNorm01_fly.append([])

			if len(B_Walk_GCevt_fly)!=len(GC_set): 
				B_Walk_GCevt_fly.append([])
				B_Walk_GCevtNorm01_fly.append([])

			if len(Rest_GCevt_fly)!=len(GC_set):
				Rest_GCevt_fly.append([])
				Rest_GCevtNorm01_fly.append([])

			if len(E_groom_GCevt_fly)!=len(GC_set):
				E_groom_GCevt_fly.append([])
				E_groom_GCevtNorm01_fly.append([])

			if len(A_groom_GCevt_fly)!=len(GC_set): 
				A_groom_GCevt_fly.append([])
				A_groom_GCevtNorm01_fly.append([])

			if len(FL_groom_GCevt_fly)!=len(GC_set):
				FL_groom_GCevt_fly.append([])
				FL_groom_GCevtNorm01_fly.append([])

			if len(HL_groom_GCevt_fly)!=len(GC_set):
				HL_groom_GCevt_fly.append([])
				HL_groom_GCevtNorm01_fly.append([])

			if len(Abd_groom_GCevt_fly)!=len(GC_set):
				Abd_groom_GCevt_fly.append([])
				Abd_groom_GCevtNorm01_fly.append([])

			if len(PER_GCevt_fly)!=len(GC_set):
				PER_GCevt_fly.append([])
				PER_GCevtNorm01_fly.append([])

			if len(Push_GCevt_fly)!=len(GC_set):
				Push_GCevt_fly.append([])
				Push_GCevtNorm01_fly.append([])

			if len(CO2puff_GCevt_fly)!=len(GC_set):
				CO2puff_GCevt_fly.append([])
				CO2puff_GCevtNorm01_fly.append([])

			if len(F_groom_GCevt_fly)!=len(GC_set): 
				F_groom_GCevt_fly.append([])
				F_groom_GCevtNorm01_fly.append([])

			if len(H_groom_GCevt_fly)!=len(GC_set):
				H_groom_GCevt_fly.append([])
				H_groom_GCevtNorm01_fly.append([])

			if len(SixLeg_Move_GCevt_fly)!=len(GC_set):
				SixLeg_Move_GCevt_fly.append([])
				SixLeg_Move_GCevtNorm01_fly.append([])


			if len(GC_all_fly_perROI)!=len(GC_set):
				GC_all_fly_perROI.append([])			
				GCnorm01_all_fly_perROI.append([])	

			for evt_idx, GC_evt in enumerate(GC_f_walk_evt_set[neuron_idx]):
				F_Walk_GCevt_fly[neuron_idx].append(GC_evt)
				F_Walk_GCevtNorm01_fly[neuron_idx].append(GCnorm01_f_walk_evt_set[neuron_idx][evt_idx])            

			for evt_idx, GC_evt in enumerate(GC_b_walk_evt_set[neuron_idx]):
				B_Walk_GCevt_fly[neuron_idx].append(GC_evt)  
				B_Walk_GCevtNorm01_fly[neuron_idx].append(GCnorm01_b_walk_evt_set[neuron_idx][evt_idx]) 

			for evt_idx, GC_evt in enumerate(GC_rest_evt_set[neuron_idx]):
				Rest_GCevt_fly[neuron_idx].append(GC_evt)
				Rest_GCevtNorm01_fly[neuron_idx].append(GCnorm01_rest_evt_set[neuron_idx][evt_idx]) 

			for evt_idx, GC_evt in enumerate(GC_E_groom_evt_set[neuron_idx]):
				E_groom_GCevt_fly[neuron_idx].append(GC_evt)
				E_groom_GCevtNorm01_fly[neuron_idx].append(GCnorm01_E_groom_evt_set[neuron_idx][evt_idx]) 

			for evt_idx, GC_evt in enumerate(GC_A_groom_evt_set[neuron_idx]):
				A_groom_GCevt_fly[neuron_idx].append(GC_evt)            
				A_groom_GCevtNorm01_fly[neuron_idx].append(GCnorm01_A_groom_evt_set[neuron_idx][evt_idx]) 

			for evt_idx, GC_evt in enumerate(GC_FL_groom_evt_set[neuron_idx]):
				FL_groom_GCevt_fly[neuron_idx].append(GC_evt)
				FL_groom_GCevtNorm01_fly[neuron_idx].append(GCnorm01_FL_groom_evt_set[neuron_idx][evt_idx]) 

			for evt_idx, GC_evt in enumerate(GC_HL_groom_evt_set[neuron_idx]):
				HL_groom_GCevt_fly[neuron_idx].append(GC_evt)
				HL_groom_GCevtNorm01_fly[neuron_idx].append(GCnorm01_HL_groom_evt_set[neuron_idx][evt_idx]) 

			for evt_idx, GC_evt in enumerate(GC_Abd_groom_evt_set[neuron_idx]):
				Abd_groom_GCevt_fly[neuron_idx].append(GC_evt)
				Abd_groom_GCevtNorm01_fly[neuron_idx].append(GCnorm01_Abd_groom_evt_set[neuron_idx][evt_idx]) 

			for evt_idx, GC_evt in enumerate(GC_PER_evt_set[neuron_idx]):
				PER_GCevt_fly[neuron_idx].append(GC_evt)    
				PER_GCevtNorm01_fly[neuron_idx].append(GCnorm01_PER_evt_set[neuron_idx][evt_idx])         

			for evt_idx, GC_evt in enumerate(GC_Push_evt_set[neuron_idx]):
				Push_GCevt_fly[neuron_idx].append(GC_evt)
				Push_GCevtNorm01_fly[neuron_idx].append(GCnorm01_Push_evt_set[neuron_idx][evt_idx]) 

			for evt_idx, GC_evt in enumerate(GC_CO2puff_evt_set[neuron_idx]):
				CO2puff_GCevt_fly[neuron_idx].append(GC_evt)
				CO2puff_GCevtNorm01_fly[neuron_idx].append(GCnorm01_CO2puff_evt_set[neuron_idx][evt_idx]) 

			for evt_idx, GC_evt in enumerate(GC_F_groom_evt_set[neuron_idx]):
				F_groom_GCevt_fly[neuron_idx].append(GC_evt)
				F_groom_GCevtNorm01_fly[neuron_idx].append(GCnorm01_F_groom_evt_set[neuron_idx][evt_idx]) 

			for evt_idx, GC_evt in enumerate(GC_H_groom_evt_set[neuron_idx]):
				H_groom_GCevt_fly[neuron_idx].append(GC_evt)
				H_groom_GCevtNorm01_fly[neuron_idx].append(GCnorm01_H_groom_evt_set[neuron_idx][evt_idx]) 

			for evt_idx, GC_evt in enumerate(GC_SixLeg_Move_evt_set[neuron_idx]):
				SixLeg_Move_GCevt_fly[neuron_idx].append(GC_evt)
				SixLeg_Move_GCevtNorm01_fly[neuron_idx].append(GCnorm01_SixLeg_Move_evt_set[neuron_idx]) 



		for ROI_i, GC_trace in enumerate(GC_set):
			GC_trace=math_utils.smooth_data(GC_trace, windowlen=int(data_freq*0.7))
			GC_all_fly_perROI[ROI_i].append(GC_trace)

			GCnorm01_all_fly_perROI[ROI_i].append(GC_set_norm01[ROI_i])



		Etho_time_fly_Dic['FW_evt'].extend(EthoLP_Timesec_Dic['FW_evt'])
		Etho_time_fly_Dic['BW_evt'].extend(EthoLP_Timesec_Dic['BW_evt'])
		Etho_time_fly_Dic['rest_evt'].extend(EthoLP_Timesec_Dic['rest_evt'])
		Etho_time_fly_Dic['E_groom_evt'].extend(EthoLP_Timesec_Dic['E_groom_evt'])
		Etho_time_fly_Dic['A_groom_evt'].extend(EthoLP_Timesec_Dic['A_groom_evt'])
		Etho_time_fly_Dic['FL_groom_evt'].extend(EthoLP_Timesec_Dic['FL_groom_evt'])
		Etho_time_fly_Dic['HL_groom_evt'].extend(EthoLP_Timesec_Dic['HL_groom_evt'])
		Etho_time_fly_Dic['Abd_groom_evt'].extend(EthoLP_Timesec_Dic['Abd_groom_evt'])
		Etho_time_fly_Dic['PER_evt'].extend(EthoLP_Timesec_Dic['PER_evt'])
		Etho_time_fly_Dic['Push_evt'].extend(EthoLP_Timesec_Dic['Push_evt'])
		Etho_time_fly_Dic['CO2puff_evt'].extend(EthoLP_Timesec_Dic['CO2puff_evt'])

		Etho_time_fly_Dic['F_groom_evt'].extend(EthoLP_Timesec_Dic['F_groom_evt'])
		Etho_time_fly_Dic['H_groom_evt'].extend(EthoLP_Timesec_Dic['H_groom_evt'])
		Etho_time_fly_Dic['SixLeg_Move_evt'].extend(EthoLP_Timesec_Dic['SixLeg_Move_evt'])


		# print('EthoLP_Timesec_Dic.keys()', EthoLP_Timesec_Dic.keys())




		GC_gapfree=[]
		for neuron_idx, GC in enumerate(GC_set):
			GC_gapfree.extend(GC)
			GC_gapfree_fly.extend(GC)

		# maxGC=sorted(GC_gapfree)[int(len(GC_gapfree)*0.99)] 
		# minGC=sorted(GC_gapfree)[int(len(GC_gapfree)*0.01)]

		maxGC=np.nanmax(GC_gapfree)
		minGC=np.nanmin(GC_gapfree)

		GC_lim=[minGC, maxGC]

		Plot_overlay_each_recrd=False
		if Plot_overlay_each_recrd==True:

			## Plot event overlay per behavior class for individual recording
			if len(GC_f_walk_evt_set[0])>0:
				plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_f_walk_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='FW_evt', filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			if len(GC_b_walk_evt_set[0])>0:
				plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_b_walk_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='BW_evt', filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			if len(GC_rest_evt_set[0])>0:
				plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_rest_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='rest_evt',filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			if len(GC_E_groom_evt_set[0])>0:
				plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_E_groom_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='E_groom_evt',filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			if len(GC_A_groom_evt_set[0])>0:
				plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_A_groom_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='A_groom_evt', filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			if len(GC_FL_groom_evt_set[0])>0:
				plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_FL_groom_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='FL_groom_evt',filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			if len(GC_HL_groom_evt_set[0])>0:
				plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_HL_groom_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='HL_groom_evt',filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			if len(GC_Abd_groom_evt_set[0])>0:
				plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_Abd_groom_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='Abd_groom_evt', filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			if len(GC_PER_evt_set[0])>0:
				plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_PER_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='PER_evt',filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			if len(GC_Push_evt_set[0])>0:
				plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_Push_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='Push_evt',filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			if len(GC_CO2puff_evt_set[0])>0:
				plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_CO2puff_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='CO2puff_evt',filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			# if len(GC_F_groom_evt_set[0])>0:
			# 	plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_F_groom_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='F_groom_evt',filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			# if len(GC_H_groom_evt_set[0])>0:
			# 	plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_H_groom_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='H_groom_evt',filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)
			# if len(GC_SixLeg_Move_evt_set[0])>0:
			# 	plot_utils.Plot_Evtavg_overlay(EthoLP_Timesec_Dic, GC_SixLeg_Move_evt_set, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='SixLeg_Move_evt',filename=date+'-'+genotype+'-'+fly+'-'+recrd_num, filepath=outDirEvents)


		GC_gapfree=[]




	maxGC=np.nanmax(GC_gapfree_fly)
	minGC=np.nanmin(GC_gapfree_fly)

	# maxGC=sorted(GC_gapfree_fly)[int(len(GC_gapfree_fly)*0.99)]
	# minGC=sorted(GC_gapfree_fly)[int(len(GC_gapfree_fly)*0.01)]

	GC_lim=[minGC, maxGC]
	GC_lim=[minGC, 100]



	Plot_overlay_each_fly=True
	if Plot_overlay_each_fly==True:

		## Plot event overlay per behavior class for individual fly
		if len(F_Walk_GCevt_fly[0])>0:
			plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, F_Walk_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='FW_evt', filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		if len(B_Walk_GCevt_fly[0])>0:
			plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, B_Walk_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='BW_evt', filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		if len(Rest_GCevt_fly[0])>0:
			plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, Rest_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='rest_evt',filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		if len(E_groom_GCevt_fly[0])>0:
			plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, E_groom_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='E_groom_evt',filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		if len(A_groom_GCevt_fly[0])>0:
			plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, A_groom_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='A_groom_evt', filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		if len(FL_groom_GCevt_fly[0])>0:
			plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, FL_groom_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='FL_groom_evt',filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		if len(HL_groom_GCevt_fly[0])>0:
			plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, HL_groom_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='HL_groom_evt',filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		if len(Abd_groom_GCevt_fly[0])>0:
			plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, Abd_groom_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='Abd_groom_evt', filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		if len(PER_GCevt_fly[0])>0:
			plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, PER_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='PER_evt',filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		if len(Push_GCevt_fly[0])>0:
			plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, Push_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='Push_evt',filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		if len(CO2puff_GCevt_fly[0])>0:
			plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, CO2puff_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='CO2puff_evt',filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		# if len(F_groom_GCevt_fly[0])>0:
		# 	plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, F_groom_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='F_groom_evt',filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		# if len(H_groom_GCevt_fly[0])>0:
		# 	plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, H_groom_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='H_groom_evt',filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
		# if len(SixLeg_Move_GCevt_fly[0])>0:
		# 	plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, SixLeg_Move_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='SixLeg_Move_evt',filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)



	print('shape GC_all_fly_perROI', np.shape(GC_all_fly_perROI))
	print('shape GCnorm01_all_fly_perROI', np.shape(GCnorm01_all_fly_perROI))
	print('shape GC_gapfree_fly', np.shape(GC_gapfree_fly))

	



