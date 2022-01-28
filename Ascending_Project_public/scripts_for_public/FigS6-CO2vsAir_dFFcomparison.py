import sys
import pickle
#import sys
import os
import re
import numpy as np
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



import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.math_utils as math_utils
import utils.sync_utils as sync_utils
import utils.list_twoP_exp as list_twoP_exp



experiments=list_twoP_exp.SS36112_air_vs_co2_puff




##main##

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_Dir

experiments_group_per_fly=general_utils.group_expList_per_fly(experiments)
print('experiments_group_per_fly', experiments_group_per_fly)


for exp_lists_per_fly in experiments_group_per_fly:
	print('Processing per fly for ... ', exp_lists_per_fly )


	Etho_time_fly_Dic={}
	Etho_time_fly_Dic['co2_evt']=[]
	Etho_time_fly_Dic['air_evt']=[]


	AirPuff_GCevt_fly=[]
	CO2Puff_GCevt_fly=[]

	Air_meanGC_fly=[]
	CO2_meanGC_fly=[]



	GC_gapfree_fly=[]

	Gal4_labels=[]


	maxGC_fly=0
	minGC_fly=0


	for date, genotype, fly, recrd_num, puff_type in exp_lists_per_fly:

		Gal4=genotype.split('-')[0]

		#dataDir = '/Users/clc/Documents/EPFL/NeLy/Data/ANproj/20180824/SS25451-tdTomGC6fopt-fly1/SS25451-tdTomGC6fopt-fly1-007'
		flyDir = NAS_AN_Proj_Dir + '06_SS36112-air_vs_co2_puff/' +Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'
		dataDir = flyDir+genotype+'-'+fly+'-'+recrd_num + '/'
		pathForDic = dataDir+'/output/'

		print('dataDir', dataDir)

		outDirEventsSumFly = NAS_AN_Proj_Dir + 'output/FigS6-air_vs_CO2_puff_comparison/plots/'
		if not os.path.exists(outDirEventsSumFly):
			os.makedirs(outDirEventsSumFly)




		Beh_Jpos_GC_DicData=general_utils.open_Beh_Jpos_GC_DicData(pathForDic, 'DicDataForMovie_Beh_GC-RES.p')


		rest = Beh_Jpos_GC_DicData['rest']
		CO2puff = Beh_Jpos_GC_DicData['CO2puff']


		timeSec = Beh_Jpos_GC_DicData['timeSec']
		Etho_Timesec_Dic = Beh_Jpos_GC_DicData['Etho_Timesec_Dic']
		Etho_Idx_Dic = Beh_Jpos_GC_DicData['Etho_Idx_Dic']


		
		data_freq=len(rest)/timeSec[-1]
		print('data_freq_DD', data_freq)



		GC_set_ori = Beh_Jpos_GC_DicData['GCset']
		GC_set=[]
		for i , GC_trace in enumerate(GC_set_ori):
			#GC_trace=math_utils.smooth_data(GC_trace, windowlen=int(data_freq*0.7)) # original = 0.7
			GC_set.append(GC_trace)
			if len(Gal4_labels)<len(GC_set_ori):
				Gal4_labels.append('ROI_'+str(i))

		absGC_set = Beh_Jpos_GC_DicData['absGCset']




		idx_puff_evt, timesec_puff_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(CO2puff, timeSec)



		


		bsl_s=1 #s
		event_dur_s=2.3 #s
		cutting_head_s=0.7







		EthoLP_Idx_Dic={}
		EthoLP_Timesec_Dic={}
		

		if puff_type=='co2':
			EthoLP_Idx_Dic.update({'co2_evt':idx_puff_evt})
			EthoLP_Timesec_Dic.update({'co2_evt':timesec_puff_evt})
			Etho_time_fly_Dic['co2_evt'].extend(EthoLP_Timesec_Dic['co2_evt'])
			GC_co2_evt_set, _ = general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'co2_evt', GC_set, baseline=bsl_s, fps=data_freq)

			for neuron_idx, GC_per_neruon in enumerate(GC_set):
				if len(CO2Puff_GCevt_fly)!=len(GC_set):
					CO2Puff_GCevt_fly.append([])
					CO2_meanGC_fly.append([])
				for evt_idx, GC_evt in enumerate(GC_co2_evt_set[neuron_idx]):
					CO2Puff_GCevt_fly[neuron_idx].append(GC_evt)

				co2evt_mean_list=math_utils.compute_mean_with_diffrerent_row_length(GC_co2_evt_set[neuron_idx], samplerate=data_freq, cutting_head_s=bsl_s+cutting_head_s)
				CO2_meanGC_fly[neuron_idx].extend(co2evt_mean_list)
			


		elif puff_type=='air':
			EthoLP_Idx_Dic.update({'air_evt':idx_puff_evt})
			EthoLP_Timesec_Dic.update({'air_evt':timesec_puff_evt})
			Etho_time_fly_Dic['air_evt'].extend(EthoLP_Timesec_Dic['air_evt'])

			GC_air_evt_set, _ = general_utils.find_corresponding_evt_from_groupIdxs(EthoLP_Idx_Dic, 'air_evt', GC_set, baseline=bsl_s, fps=data_freq)

			for neuron_idx, GC_per_neruon in enumerate(GC_set):
				if len(AirPuff_GCevt_fly)!=len(GC_set):
					AirPuff_GCevt_fly.append([])
					Air_meanGC_fly.append([])
				for evt_idx, GC_evt in enumerate(GC_air_evt_set[neuron_idx]):
					AirPuff_GCevt_fly[neuron_idx].append(GC_evt)

				airevt_mean_list=math_utils.compute_mean_with_diffrerent_row_length(GC_air_evt_set[neuron_idx], samplerate=data_freq, cutting_head_s=bsl_s+cutting_head_s)
				Air_meanGC_fly[neuron_idx].extend(airevt_mean_list)
			




		GC_gapfree=[]
		for neuron_idx, GC in enumerate(GC_set):
			GC_gapfree.extend(GC)
			GC_gapfree_fly.extend(GC)

		maxGC=np.nanmax(GC_gapfree)
		minGC=np.nanmin(GC_gapfree)

		GC_lim=[minGC, maxGC]



		GC_gapfree=[]

		



	maxGC=sorted(GC_gapfree_fly)[int(len(GC_gapfree_fly)*0.9975)]
	minGC=sorted(GC_gapfree_fly)[int(len(GC_gapfree_fly)*0.001)]
	maxGC=3
	minGC=-0.5
	GC_lim=[minGC, maxGC]

	print('GC_lim', GC_lim)



	## Plot event overlay per behavior class for individual fly


	if len(CO2Puff_GCevt_fly[0])>0:
		plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, CO2Puff_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='co2_evt',filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
	
	if len(AirPuff_GCevt_fly[0])>0:
		plot_utils.Plot_Evtavg_overlay_err(Etho_time_fly_Dic, AirPuff_GCevt_fly, baseline=bsl_s, epoch_len=event_dur_s, y_lim=GC_lim, whichBeh='air_evt',filename=date+'-'+genotype+'-'+fly, filepath=outDirEventsSumFly)
	

	p_value_list=[]
	for ROI_i, air_meanGCs in enumerate(Air_meanGC_fly):
		co2_meanGCs=CO2_meanGC_fly[ROI_i]

		p_value=math_utils.bootstrapped_twoSamplesComparison(co2_meanGCs, air_meanGCs, fold=10, resample_size=30, stats='Mann-Whitney')
		
		p_value_list.append(p_value)

	print('Gal4_labels', Gal4_labels)
	print('p_value_list', p_value_list)

	print('shape Air_meanGC_fly+CO2_meanGC_fly', np.shape(CO2_meanGC_fly))
	print('np.nanmin(general_utils.flatten_list(Air_meanGC_fly+CO2_meanGC_fly)', np.nanmin(general_utils.flatten_list(Air_meanGC_fly+CO2_meanGC_fly)))
	


	labels=['CO2', 'Air']
	y_lim=[np.nanmin(general_utils.flatten_list(Air_meanGC_fly+CO2_meanGC_fly)), np.nanmax(general_utils.flatten_list(Air_meanGC_fly+CO2_meanGC_fly))]
	print('y_lim', y_lim)
	plot_utils.plot_group_bar_w_scatterPoints(Gal4_labels, CO2_meanGC_fly, Air_meanGC_fly, y_lim, p_value_list, labels, outDirEventsSumFly, date+'-'+genotype+'-'+fly+'_CO2vsAir_dFF')




















