import numpy as np
import scipy.signal
import matplotlib
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import sys
import pandas as pd 
import os
import pickle
from multiprocessing import Pool
from itertools import repeat


import utils.EventDetection_utils as EventDetection_utils
import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.plot_setting as plot_setting
import utils.list_twoP_exp as list_twoP_exp
import utils.list_behavior as list_behavior
import utils.math_utils as math_utils




experiments=list_twoP_exp.SS36112_CO2puff_BW_analysis




# event_max_dur=EventDetection_utils.event_max_dur
# event_min_dur=EventDetection_utils.event_min_dur
event_max_dur=2.5
event_min_dur=0.27
bsl_dur_s=EventDetection_utils.bsl_s






def count_ROIs_from_folder(exp_lists_current_fly):

	for date, genotype, fly, recrd_num in exp_lists_current_fly:

		Gal4=genotype.split('-')[0]

		flyDir = NAS_AN_Proj_Dir +'03_general_2P_exp/'+ Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'
		dataDir = flyDir+genotype+'-'+fly+'-'+recrd_num + '/'
		pathForDic = dataDir+'/output/'
		outDirGCevt = pathForDic + 'GCevt_based_JposBehBallAnalysis/'

		folder_content=os.listdir(outDirGCevt)
		print('folder_content', folder_content)

		ROI_folder_list=[]
		for content in folder_content:
			if content[:4]=='ROI#':
				ROI_folder_list.append(content)


		ROI_count=len(ROI_folder_list)

		print('ROI_folder_list', ROI_folder_list,  ROI_count, 'ROIs found!')

		break


	return ROI_count



def make_structure_as_modelStructure(ori_list, exempl_list):

	if len(ori_list)!=len(exempl_list):

		anticipate_list=[]
		for i,v in enumerate(exempl_list):
			anticipate_list.append([])

		return anticipate_list

	else:
		return ori_list









def add_NaNtail_to_each_Evt(Evt_list):

	Evt_len_list=[]
	for evt in Evt_list:
		# print('np.shape(evt', np.shape(evt))
		Evt_len_list.append(np.shape(evt)[0])

	max_EvtLen=max(Evt_len_list)

	# print('max_EvtLen', max_EvtLen)

	EvtNaNtail_list=[]
	for evt in Evt_list:
		evt_NaNtail=math_utils.add_NaN_tail(evt, max_EvtLen)
		#print('len evt_NaNtail', len(evt_NaNtail))
		EvtNaNtail_list.append(evt_NaNtail)

	return EvtNaNtail_list



def mp_worker_for_CI_mean_trace(idx, dataset, confidence, least_realNum_amount, behFreq):

	dataset=np.asarray(dataset)
	# print('shape dataset', np.shape(dataset))
	# print('idx', idx)
	# print('shape dataset', np.shape(dataset))
	# print('least_realNum_amount', least_realNum_amount)
	# print('len dataset', len(dataset))

	if behFreq==0:
		behFreq=1

	data=np.array(dataset[:, idx])
	#print('shape data', np.shape(data))
	

	non_nan_counts=data.size - np.count_nonzero(np.isnan(data))

	if non_nan_counts > least_realNum_amount:

		nonnan_data_list=data[np.logical_not(np.isnan(data))] 

		(mean, down_CI, up_CI) = math_utils.compute_CI_and_mean(nonnan_data_list, confidence=confidence)

		return mean, down_CI, up_CI

	else:

		return np.nan, np.nan, np.nan




def compute_CI_and_mean_trace_w_BehfreqCorrec(dataset, confidence=0.95, least_realNum_amount=4, behFreq=1):




	idx_range=[i for i in range(0,np.shape(dataset)[1])]
	# print('colums_range', colums_range)

	p=Pool()
	mean_downCI_upCI = p.starmap(mp_worker_for_CI_mean_trace, zip(idx_range, repeat(dataset), repeat(confidence), repeat(least_realNum_amount), repeat(behFreq)))
	#mean_trace, down_err_trace, up_err_trace = p.starmap(worker_for_CI_mean_trace, args_for_pool)

	p.close()
	p.join()
	del p	

	#print('shape mean_downCI_upCI', np.shape(mean_downCI_upCI))

	mean_trace=np.asarray(mean_downCI_upCI)[:,0]
	down_err_trace=np.asarray(mean_downCI_upCI)[:,1]
	up_err_trace=np.asarray(mean_downCI_upCI)[:,2]



	return mean_trace, down_err_trace, up_err_trace


def find_maxGC_perROI(exp_lists_per_fly):

	print('Finding amximum GC among all recordings per fly')

	GC_set_per_fly=[]

	for date, genotype, fly, recrd_num in exp_lists_per_fly:

		Gal4=genotype.split('-')[0]

		#dataDir = '/Users/clc/Documents/EPFL/NeLy/Data/ANproj/20180824/SS25451-tdTomGC6fopt-fly1/SS25451-tdTomGC6fopt-fly1-007'
		flyDir = NAS_AN_Proj_Dir + Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'
		dataDir = NAS_AN_Proj_Dir + Gal4 +'/2P/' + date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num + '/'
		pathForDic = dataDir+'/output/'

		Beh_Jpos_GC_DicData=general_utils.open_Beh_Jpos_GC_DicData(pathForDic)

		GC_set = Beh_Jpos_GC_DicData['GCset']

		for ROI_i, GC_trace in enumerate(GC_set):
			if len(GC_set_per_fly)!=len(GC_set):
				GC_set_per_fly.append([])


		print('len GC_set_per_fly', len(GC_set_per_fly))

		for ROI_i, GC_trace in enumerate(GC_set):
			GC_set_per_fly[ROI_i].extend(GC_trace)

	maxGC_per_fly=[]
	for ROI_i, GC_trace in enumerate(GC_set_per_fly):
		max_GC=max(GC_trace)
		maxGC_per_fly.append(max_GC)

	print('maxGC_per_fly', maxGC_per_fly)


	return maxGC_per_fly







def save_GCevt_fly_dic(save_dir, filename):


	print('Saving GCevent-based.dic')

	GCevt_dic_fly={}


	GCevt_dic_fly.update({'samplingFreq':samplingFreq})

	GCevt_dic_fly.update({'GC_evt_fly':GC_evt_fly})
	GCevt_dic_fly.update({'time_evt_fly':time_evt_fly})

	GCevt_dic_fly.update({'rest_evt_fly':rest_evt_fly})
	GCevt_dic_fly.update({'walk_evt_fly':walk_evt_fly})

	GCevt_dic_fly.update({'eye_groom_evt_fly':eye_groom_evt_fly})
	GCevt_dic_fly.update({'foreleg_groom_evt_fly':foreleg_groom_evt_fly})
	GCevt_dic_fly.update({'antennae_groom_evt_list':antennae_groom_evt_list})

	GCevt_dic_fly.update({'hindleg_groom_evt_list':hindleg_groom_evt_list})
	GCevt_dic_fly.update({'Abd_groom_evt_list':Abd_groom_evt_list})

	GCevt_dic_fly.update({'PER_evt_list':PER_evt_list})

	GCevt_dic_fly.update({'F_groom_evt_list':F_groom_evt_list})
	GCevt_dic_fly.update({'H_groom_evt_list':H_groom_evt_list})

	GCevt_dic_fly.update({'CO2puff_evt_list':CO2puff_evt_list})

	GCevt_dic_fly.update({'velForw_evt_list':velForw_evt_list})
	GCevt_dic_fly.update({'velSide_evt_list':velSide_evt_list})
	GCevt_dic_fly.update({'velTurn_evt_list':velTurn_evt_list})

	for item, value in J_Pos_evt.items():
		GCevt_dic_fly.update({item:value})



	pickle.dump( GCevt_dic, open( save_dir + filename, "wb" ) ) 



	return



def save_GCevt_fly_dic(save_dir, filename):


	print('Saving GCevent-based.dic')

	GCevt_dic_fly={}



	GCevt_dic_fly.update({'samplingFreq':samplingFreq})

	GCevt_dic_fly.update({'GC_evt_fly':GC_evt_fly})
	GCevt_dic_fly.update({'time_evt_fly':time_evt_fly})

	GCevt_dic_fly.update({'rest_evt_fly':rest_evt_fly})
	GCevt_dic_fly.update({'walk_evt_fly':walk_evt_fly})

	GCevt_dic_fly.update({'eye_groom_evt_fly':eye_groom_evt_fly})
	GCevt_dic_fly.update({'foreleg_groom_evt_fly':foreleg_groom_evt_fly})
	GCevt_dic_fly.update({'antennae_groom_evt_list':antennae_groom_evt_list})

	GCevt_dic_fly.update({'hindleg_groom_evt_fly':hindleg_groom_evt_list})
	GCevt_dic_fly.update({'Abd_groom_evt_fly':Abd_groom_evt_list})

	GCevt_dic_fly.update({'PER_evt_fly':PER_evt_list})

	GCevt_dic_fly.update({'F_groom_evt_fly':F_groom_evt_list})
	GCevt_dic_fly.update({'H_groom_evt_fly':H_groom_evt_list})

	GCevt_dic_fly.update({'CO2_evt_fly':CO2puff_evt_list})
	
	GCevt_dic_fly.update({'velForw_evt_fly':velForw_evt_list})
	GCevt_dic_fly.update({'velSide_evt_fly':velSide_evt_list})
	GCevt_dic_fly.update({'velTurn_evt_fly':velTurn_evt_list})

	GCevt_dic_fly.update({'JposEvt_fly':JposEvt_fly})




	pickle.dump( GCevt_dic, open( save_dir + filename, "wb" ) ) 



	return



##main##

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_Dir



dataAnalysisType=[
('CO2evt_long_dic'),
('CO2evt_short_dic'),
('BWwoCO2evt_dic'),
('BWwCO2evt_dic'),
]


for datatype in dataAnalysisType:


	experiments_group_per_fly=general_utils.group_expList_per_fly(experiments)

	print('experiments_group_per_fly', experiments_group_per_fly)

	count_evt_fly=[]



	beh_photo_fps=30

	least_realNum_amount=3



	if datatype=='CO2evt_long_dic':
		inputfilename='CO2evt_long_dic.pkl'
		outputfilename='CO2evt_long_based_BallRot_fly'

	elif datatype=='CO2evt_short_dic':
		inputfilename='CO2evt_short_dic.pkl'
		outputfilename='CO2evt_short_based_BallRot_fly'

	elif datatype=='BWwoCO2evt_dic':
		inputfilename='BWwoCO2evt_dic.pkl'
		outputfilename='BWwoCO2evt_based_BallRot_fly'

	elif datatype=='BWwCO2evt_dic':
		inputfilename='BWwCO2evt_dic.pkl'
		outputfilename='BWwCO2evt_based_BallRot_fly'



	for exp_lists_per_fly in experiments_group_per_fly:

		print('Processing ', exp_lists_per_fly ,'....')

		## All events
		GC_evt_fly=[]
		time_evt_fly=[]

		rest_evt_fly=[]
		f_walk_evt_fly=[]
		b_walk_evt_fly=[]

		eye_groom_evt_fly=[]
		antennae_groom_evt_fly=[]
		foreleg_groom_evt_fly=[]

		hindleg_groom_evt_fly=[]
		Abd_groom_evt_fly=[]

		PER_evt_fly=[]

		F_groom_evt_fly=[]
		H_groom_evt_fly=[]

		CO2_evt_fly=[]
		BW_beyong_CO2puff_evt_fly=[]

		velForw_evt_fly=[]
		velSide_evt_fly=[]
		velTurn_evt_fly=[]




		# maxGC_per_fly_list=find_maxGC_perROI(exp_lists_per_fly)





		#Process each recording
		for date, genotype, fly, recrd_num in exp_lists_per_fly:

			Gal4=genotype.split('-')[0]

			#dataDir = '/Users/clc/Documents/EPFL/NeLy/Data/ANproj/20180824/SS25451-tdTomGC6fopt-fly1/SS25451-tdTomGC6fopt-fly1-007'
			flyDir = NAS_AN_Proj_Dir +'03_general_2P_exp/'+ Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'
			dataDir = flyDir+genotype+'-'+fly+'-'+recrd_num + '/'
			pathForDic = dataDir+'/output/'

			print('dataDir', dataDir)

			# inputfilename='CO2evt_all_dic.pkl'
			# outputfilename='CO2evt_all_based_relativeBehFreq_fly'

			# inputfilename='CO2evt_short_dic.pkl'
			# outputfilename='CO2evt_short_based_relativeBehFreq_fly'

			# inputfilename='CO2evt_long_dic.pkl'
			# outputfilename='CO2evt_long_based_relativeBehFreq_fly'

			# inputfilename='CO2_BW_BWwoCO2evt_dic.pkl'
			# outputfilename='BWevt_beyong_CO2puff_based_relativeBehFreq_fly'

			# inputfilename='BWevt_dic.pkl'
			# outputfilename='BWevt_based_relativeBehFreq_fly'


			outDirCO2evt = NAS_AN_Proj_Dir + 'output/FigS5-CO2puff_BW_analysis_SS36112/' +Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num + '/output/CO2evt_based_BehBallAnalysis/'
			if os.path.exists(outDirCO2evt+inputfilename):
				evt_dic=EventDetection_utils.read_evt_dic(outDirCO2evt, inputfilename)

			else:
				print('No CO2evt_dic.pkl exists mainly due to no CO2 event is detected ...')
				continue
		

			evt_startIdx_list=evt_dic['evt_startIdx_list']
			evt_endIdx_list=evt_dic['evt_endIdx_list']
			samplingFreq=evt_dic['samplingFreq']

			GC_evt_set_list=evt_dic['GC_evt_set_list']
			
			time_evt_list=evt_dic['time_evt_list']

			rest_evt_list=evt_dic['rest_evt_list']
			f_walk_evt_list=evt_dic['f_walk_evt_list']
			b_walk_evt_list=evt_dic['b_walk_evt_list']

			eye_groom_evt_list=evt_dic['eye_groom_evt_list']
			antennae_groom_evt_list=evt_dic['antennae_groom_evt_list']
			foreleg_groom_evt_list=evt_dic['foreleg_groom_evt_list']
			print('shape foreleg_groom_evt_list', np.shape(foreleg_groom_evt_list))

			hindleg_groom_evt_list=evt_dic['hindleg_groom_evt_list']
			Abd_groom_evt_list=evt_dic['Abd_groom_evt_list']
			
			PER_evt_list=evt_dic['PER_evt_list']

			F_groom_evt_list=evt_dic['F_groom_evt_list']
			H_groom_evt_list=evt_dic['H_groom_evt_list']

			CO2puff_evt_list=evt_dic['CO2puff_evt_list']
			BW_beyong_CO2puff_evt_list=evt_dic['BW_beyong_CO2puff_evt_list']


			velForw_evt_list=evt_dic['velForw_evt_list']
			velSide_evt_list=evt_dic['velSide_evt_list']
			velTurn_evt_list=evt_dic['velTurn_evt_list']



			print(len(GC_evt_set_list), 'GC event found')

			model_list_struc=[]
			for i in range(0,len(GC_evt_set_list)):
				model_list_struc.append([])

			GC_evt_fly=make_structure_as_modelStructure(GC_evt_fly, model_list_struc)
			print('shape GC_evt_fly', len(GC_evt_fly))
			# time_evt_fly=make_structure_as_modelStructure(time_evt_fly, model_list_struc)
			# rest_evt_fly=make_structure_as_modelStructure(rest_evt_fly, model_list_struc)
			# walk_evt_fly=make_structure_as_modelStructure(walk_evt_fly, model_list_struc)
			# eye_groom_evt_fly=make_structure_as_modelStructure(eye_groom_evt_fly, model_list_struc)
			# antennae_groom_evt_fly=make_structure_as_modelStructure(antennae_groom_evt_fly, model_list_struc)
			# foreleg_groom_evt_fly=make_structure_as_modelStructure(foreleg_groom_evt_fly, model_list_struc)
			# hindleg_groom_evt_fly=make_structure_as_modelStructure(hindleg_groom_evt_fly, model_list_struc)
			# Abd_groom_evt_fly=make_structure_as_modelStructure(Abd_groom_evt_fly, model_list_struc)
			# PER_evt_fly=make_structure_as_modelStructure(PER_evt_fly, model_list_struc)
			# F_groom_evt_fly=make_structure_as_modelStructure(F_groom_evt_fly, model_list_struc)
			# H_groom_evt_fly=make_structure_as_modelStructure(H_groom_evt_fly, model_list_struc)
			# CO2_evt_fly=make_structure_as_modelStructure(CO2_evt_fly, model_list_struc)
			# velForw_evt_fly=make_structure_as_modelStructure(velForw_evt_fly, model_list_struc)
			# velSide_evt_fly=make_structure_as_modelStructure(velSide_evt_fly, model_list_struc)
			# velTurn_evt_fly=make_structure_as_modelStructure(velTurn_evt_fly, model_list_struc)




			## Pool events of all recordings per fly
			for ROI_i in range(0,len(GC_evt_set_list)):
				GC_evt_fly[ROI_i].extend(GC_evt_set_list[ROI_i])
			time_evt_fly.extend(time_evt_list)
			rest_evt_fly.extend(rest_evt_list)
			f_walk_evt_fly.extend(f_walk_evt_list)
			b_walk_evt_fly.extend(b_walk_evt_list)
			eye_groom_evt_fly.extend(eye_groom_evt_list)
			antennae_groom_evt_fly.extend(antennae_groom_evt_list)
			foreleg_groom_evt_fly.extend(foreleg_groom_evt_list)
			hindleg_groom_evt_fly.extend(hindleg_groom_evt_list)
			Abd_groom_evt_fly.extend(Abd_groom_evt_list)
			PER_evt_fly.extend(PER_evt_list)
			F_groom_evt_fly.extend(F_groom_evt_list)
			H_groom_evt_fly.extend(H_groom_evt_list)
			CO2_evt_fly.extend(CO2puff_evt_list)
			BW_beyong_CO2puff_evt_fly.extend(BW_beyong_CO2puff_evt_list)

			velForw_evt_fly.extend(velForw_evt_list)
			velSide_evt_fly.extend(velSide_evt_list)
			velTurn_evt_fly.extend(velTurn_evt_list)


			# ## For preparing the plot of each recording
			# GC_evt_set_NaNtail_list=[]
			# for i in range(0, len(GC_evt_set_list)):
			# 	GC_evt_set_NaNtail_list.append([])
			# 	GC_evtNaNtail=add_NaNtail_to_each_Evt(GC_evt_set_list[i])
			# 	GC_evt_set_NaNtail_list[i].extend(GC_evtNaNtail)
			# time_evtNaNtail_list=add_NaNtail_to_each_Evt(time_evt_list)
			# rest_evtNaNtail_list=add_NaNtail_to_each_Evt(rest_evt_list)
			# walk_evtNaNtail_list=add_NaNtail_to_each_Evt(walk_evt_list)
			# eye_groom_evtNaNtail_list=add_NaNtail_to_each_Evt(eye_groom_evt_list)
			# antennae_groom_evtNaNtail_list=add_NaNtail_to_each_Evt(antennae_groom_evt_list)
			# foreleg_groom_evtNaNtail_list=add_NaNtail_to_each_Evt(foreleg_groom_evt_list)
			# hindleg_groom_evtNaNtail_list=add_NaNtail_to_each_Evt(hindleg_groom_evt_list)
			# Abd_groom_evtNaNtail_list=add_NaNtail_to_each_Evt(Abd_groom_evt_list)
			# PER_evtNaNtail_list=add_NaNtail_to_each_Evt(PER_evt_list)
			# F_groom_evtNaNtail_list=add_NaNtail_to_each_Evt(F_groom_evt_list)
			# H_groom_evtNaNtail_list=add_NaNtail_to_each_Evt(H_groom_evt_list)
			# CO2puff_evtNaNtail_list=add_NaNtail_to_each_Evt(CO2puff_evt_list)
			# velForw_evtNaNtail_list=add_NaNtail_to_each_Evt(velForw_evt_list)
			# velSide_evtNaNtail_list=add_NaNtail_to_each_Evt(velSide_evt_list)
			# velTurn_evtNaNtail_list=add_NaNtail_to_each_Evt(velTurn_evt_list)

			# print('shape GC_evt_set_NaNtail_list', np.shape(GC_evt_set_NaNtail_list))
			# print('shape CO2puff_evtNaNtail_list', np.shape(CO2puff_evtNaNtail_list))

			
			# print('Computing mean and CI for CO2 events ...')
			# GC_mean_set, GC_downCI_Set, GC_upCI_set=[],[],[]
			# for i in range(0, len(GC_evt_set_NaNtail_list)):
			# 	GC_evtNaNtail_list=GC_evt_set_NaNtail_list[i]
			# 	GC_mean_set.append([])
			# 	GC_downCI_Set.append([])
			# 	GC_upCI_set.append([])
			# 	GC_mean, GC_down_CI, GC_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(GC_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# 	GC_mean_set[i].extend(GC_mean)
			# 	GC_downCI_Set[i].extend(GC_down_CI)
			# 	GC_upCI_set[i].extend(GC_up_CI)
			# rest_mean, rest_down_CI, rest_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(rest_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount, behFreq=1)
			# walk_mean, walk_down_CI, walk_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(walk_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount, behFreq=1)
			# eye_groom_mean, eye_groom_down_CI, eye_groom_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(eye_groom_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount, behFreq=1)
			# antennae_groom_mean, antennae_groom_down_CI, antennae_groom_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(antennae_groom_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount, behFreq=1)
			# foreleg_groom_mean, foreleg_groom_down_CI, foreleg_groom_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(foreleg_groom_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount, behFreq=1) 		
			# hindleg_groom_mean, hindleg_groom_down_CI, hindleg_groom_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(hindleg_groom_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount, behFreq=1)
			# Abd_groom_mean, Abd_groom_down_CI, Abd_groom_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(Abd_groom_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount, behFreq=1)
			# PER_mean, PER_down_CI, PER_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(PER_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount, behFreq=1)
			# F_groom_mean, F_groom_down_CI, F_groom_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(F_groom_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount, behFreq=1)
			# H_groom_mean, H_groom_down_CI, H_groom_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(H_groom_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount, behFreq=1)
			# CO2puff_mean, CO2puff_down_CI, CO2puff_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(CO2puff_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount, behFreq=1)
			# velForw_mean, velForw_down_CI, velForw_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(velForw_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# velSide_mean, velSide_down_CI, velSide_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(velSide_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# velTurn_mean, velTurn_down_CI, velTurn_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(velTurn_evtNaNtail_list, confidence=0.95, least_realNum_amount=least_realNum_amount)

			# print('shape CO2puff_mean', np.shape(CO2puff_mean))
			# print('shape CO2puff_down_CI', np.shape(CO2puff_down_CI))
			# print('shape GC_mean_set', np.shape(GC_mean_set))
			# CO2_Evt_beh_trace_plot=[GC_mean_set[0], rest_mean, walk_mean, eye_groom_mean, antennae_groom_mean, foreleg_groom_mean, hindleg_groom_mean, Abd_groom_mean, PER_mean, CO2puff_mean, velForw_mean, velSide_mean, velTurn_mean]
			# CO2_Evt_beh_subtitle=['GC_mean_set[0]', 'rest_mean', 'walk_mean', 'eye_groom_mean', 'antennae_groom_mean', 'foreleg_groom_mean', 'hindleg_groom_mean', 'Abd_groom_mean', 'PER_mean', 'CO2puff_mean', 'velForw_mean', 'velSide_mean', 'velTurn_mean']
			# plot_utils.Plot_traces(CO2_Evt_beh_trace_plot, outDirCO2evt, 'CO2evt_Beh.png', subtitle_list=CO2_Evt_beh_subtitle, plot_mode='row_by_row')


			

			# len_sort_time_evt_list=sorted(time_evt_list, key=len)
			# time_boundary=[0, len_sort_time_evt_list[-1][-1]-len_sort_time_evt_list[-1][0]]

			# print('time_boundary', time_boundary)
			

			# plot_utils.Plot_CO2Evt_avg_err(time_boundary, \
	  #                GC_mean_set, GC_downCI_Set, GC_upCI_set,\
	  #                rest_mean, rest_down_CI, rest_up_CI,\
	  #                walk_mean, walk_down_CI, walk_up_CI,\
	  #                eye_groom_mean, eye_groom_down_CI, eye_groom_up_CI,\
	  #                antennae_groom_mean, antennae_groom_down_CI, antennae_groom_up_CI,\
	  #                foreleg_groom_mean, foreleg_groom_down_CI, foreleg_groom_up_CI,\
	  #                hindleg_groom_mean, hindleg_groom_down_CI, hindleg_groom_up_CI,\
	  #                Abd_groom_mean, Abd_groom_down_CI, Abd_groom_up_CI,\
	  #                PER_mean, PER_down_CI, PER_up_CI,\
	  #                CO2puff_mean, CO2puff_down_CI, CO2puff_up_CI,\
	  #                velForw_mean, velForw_down_CI, velForw_up_CI,\
	  #                velSide_mean, velSide_down_CI, velSide_up_CI,\
	  #                velTurn_mean, velTurn_down_CI, velTurn_up_CI,\
	  #                'CO2evt_based_relativeBehFreq.png', outDirCO2evt)





		## Plotting event per fly
		for date, genotype, fly, recrd_num in exp_lists_per_fly:

			Gal4=genotype.split('-')[0]


			outDirCO2evtSumFly = NAS_AN_Proj_Dir + 'output/FigS5-CO2puff_BW_analysis_SS36112/plots/'
			if not os.path.exists(outDirCO2evtSumFly):
				os.makedirs(outDirCO2evtSumFly)

			
			print('\nProcessing in fly pool event', date, genotype, fly, '\n')


			GC_evt_set_NaNtail_fly=[]
			for i in range(0, len(GC_evt_fly)):
				GC_evt_set_NaNtail_fly.append([])
				GC_evtNaNtail_fly=add_NaNtail_to_each_Evt(GC_evt_fly[i])
				GC_evt_set_NaNtail_fly[i].extend(GC_evtNaNtail_fly)
			time_evtNaNtail_fly=add_NaNtail_to_each_Evt(time_evt_fly)
			rest_evtNaNtail_fly=add_NaNtail_to_each_Evt(rest_evt_fly)
			f_walk_evtNaNtail_fly=add_NaNtail_to_each_Evt(f_walk_evt_fly)
			b_walk_evtNaNtail_fly=add_NaNtail_to_each_Evt(b_walk_evt_fly)
			eye_groom_evtNaNtail_fly=add_NaNtail_to_each_Evt(eye_groom_evt_fly)
			antennae_groom_evtNaNtail_fly=add_NaNtail_to_each_Evt(antennae_groom_evt_fly)
			foreleg_groom_evtNaNtail_fly=add_NaNtail_to_each_Evt(foreleg_groom_evt_fly)
			hindleg_groom_evtNaNtail_fly=add_NaNtail_to_each_Evt(hindleg_groom_evt_fly)
			Abd_groom_evtNaNtail_fly=add_NaNtail_to_each_Evt(Abd_groom_evt_fly)
			PER_evtNaNtail_fly=add_NaNtail_to_each_Evt(PER_evt_fly)
			F_groom_evtNaNtail_fly=add_NaNtail_to_each_Evt(F_groom_evt_fly)
			H_groom_evtNaNtail_fly=add_NaNtail_to_each_Evt(H_groom_evt_fly)
			CO2puff_evtNaNtail_fly=add_NaNtail_to_each_Evt(CO2_evt_fly)
			BW_beyong_CO2puff_evtNaNtail_fly=add_NaNtail_to_each_Evt(BW_beyong_CO2puff_evt_fly)

			velForw_evtNaNtail_fly=add_NaNtail_to_each_Evt(velForw_evt_fly)
			velSide_evtNaNtail_fly=add_NaNtail_to_each_Evt(velSide_evt_fly)
			velTurn_evtNaNtail_fly=add_NaNtail_to_each_Evt(velTurn_evt_fly)



			print('Computing mean and CI for pool GC events ...')
			GC_mean_fly, GC_downCI_fly, GC_upCI_fly=[],[],[]
			for i in range(0, len(GC_evt_set_NaNtail_fly)):
				GC_evtNaNtail_fly=GC_evt_set_NaNtail_fly[i]
				GC_mean_fly.append([])
				GC_downCI_fly.append([])
				GC_upCI_fly.append([])
				GC_mean, GC_down_CI, GC_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(GC_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
				GC_mean_fly[i].extend(GC_mean)
				GC_downCI_fly[i].extend(GC_down_CI)
				GC_upCI_fly[i].extend(GC_up_CI)
			# rest_mean_fly, rest_down_CI_fly, rest_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(rest_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# walk_mean_fly, walk_down_CI_fly, walk_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(walk_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# eye_groom_mean_fly, eye_groom_down_CI_fly, eye_groom_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(eye_groom_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# antennae_groom_mean_fly, antennae_groom_down_CI_fly, antennae_groom_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(antennae_groom_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# foreleg_groom_mean_fly, foreleg_groom_down_CI_fly, foreleg_groom_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(foreleg_groom_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# hindleg_groom_mean_fly, hindleg_groom_down_CI_fly, hindleg_groom_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(hindleg_groom_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# Abd_groom_mean_fly, Abd_groom_down_CI_fly, Abd_groom_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(Abd_groom_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# PER_mean_fly, PER_down_CI_fly, PER_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(PER_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# F_groom_mean_fly, F_groom_down_CI_fly, F_groom_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(F_groom_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# H_groom_mean_fly, H_groom_down_CI_fly, H_groom_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(H_groom_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			# CO2puff_mean_fly, CO2puff_down_CI_fly, CO2puff_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(CO2puff_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			velForw_mean_fly, velForw_down_CI_fly, velForw_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(velForw_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			velSide_mean_fly, velSide_down_CI_fly, velSide_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(velSide_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			velTurn_mean_fly, velTurn_down_CI_fly, velTurn_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(velTurn_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)


			sum_rest_fly=np.nansum(rest_evtNaNtail_fly,axis=0)
			sum_f_walk_fly=np.nansum(f_walk_evtNaNtail_fly,axis=0)
			sum_b_walk_fly=np.nansum(b_walk_evtNaNtail_fly,axis=0)
			sum_E_groom_fly=np.nansum(eye_groom_evtNaNtail_fly,axis=0)
			sum_A_groom_fly=np.nansum(antennae_groom_evtNaNtail_fly,axis=0)
			sum_FL_groom_fly=np.nansum(foreleg_groom_evtNaNtail_fly,axis=0)
			sum_HL_groom_fly=np.nansum(hindleg_groom_evtNaNtail_fly,axis=0)
			sum_Abd_groom_fly=np.nansum(Abd_groom_evtNaNtail_fly,axis=0)
			sum_PER_fly=np.nansum(PER_evtNaNtail_fly,axis=0)
			sum_F_groom_fly=np.nansum(F_groom_evtNaNtail_fly,axis=0)
			sum_H_groom_fly=np.nansum(H_groom_evtNaNtail_fly,axis=0)
			sum_CO2puff_fly=np.nansum(CO2puff_evtNaNtail_fly,axis=0)
			sum_BW_beyong_CO2puff_fly=np.nansum(BW_beyong_CO2puff_evtNaNtail_fly,axis=0)

			CI_null=[0]*len(sum_rest_fly)




			# GC_Evt_beh_trace_fly_plot=[GC_mean_fly[0], rest_mean_fly, walk_mean_fly, F_groom_mean_fly, H_groom_mean_fly, PER_mean_fly, CO2puff_mean_fly, velForw_mean_fly, velSide_mean_fly, velTurn_mean_fly]
			# GC_Evt_beh_fly_subtitle=['GC_mean_fly[0]', 'rest_mean_fly', 'walk_mean_fly', 'F_groom_mean_fly', 'H_groom_mean_fly', 'PER_mean_fly', 'CO2puff_mean_fly', 'velForw_mean_fly', 'velSide_mean_fly', 'velTurn_mean_fly']
			# plot_utils.Plot_traces(GC_Evt_beh_trace_fly_plot, outDirCO2evtSumFly, 'CO2evt_Beh.png', subtitle_list=GC_Evt_beh_fly_subtitle, plot_mode='row_by_row')

			bsl_s=EventDetection_utils.bsl_s
			len_sort_time_evt_fly=sorted(time_evt_fly, key=len)
			time_boundary_fly=[0-bsl_s, len_sort_time_evt_fly[-1][-1]-len_sort_time_evt_fly[-1][0]-bsl_s]

			print('time_boundary_fly', time_boundary_fly)
			



			sum_mainBeh_fly=sum_CO2puff_fly
			sum_viceBeh_fly=sum_b_walk_fly
			mainColor=plot_setting.CO2puff_color
			viceColor=plot_setting.BW_color
			mainlabel='CO2 puff'
			vicelabel='BW'

			# sum_mainBeh_fly=sum_BW_beyong_CO2puff_fly
			# sum_viceBeh_fly=sum_CO2puff_fly
			# mainColor=plot_setting.BW_color
			# viceColor=plot_setting.CO2puff_color
			# mainlabel='BW'
			# vicelabel='CO2 puff'

			# sum_mainBeh_fly=sum_BW_beyong_CO2puff_fly
			plot_utils.Plot_BWevt_avg_err(time_boundary_fly, \
					 sum_mainBeh_fly, CI_null, CI_null,\
					 sum_viceBeh_fly, CI_null, CI_null,
	                 GC_mean_fly, GC_downCI_fly, GC_upCI_fly,\
	                 sum_rest_fly, CI_null, CI_null,\
	                 sum_f_walk_fly, CI_null, CI_null,\
	                 sum_b_walk_fly, CI_null, CI_null,\
	                 sum_E_groom_fly, CI_null, CI_null,\
	                 sum_A_groom_fly, CI_null, CI_null,\
	                 sum_FL_groom_fly, CI_null, CI_null,\
	                 sum_HL_groom_fly, CI_null, CI_null,\
	                 sum_Abd_groom_fly, CI_null, CI_null,\
	                 sum_PER_fly, CI_null, CI_null,\
	                 sum_CO2puff_fly, CI_null, CI_null,\
	                 sum_BW_beyong_CO2puff_fly, CI_null, CI_null,\
	                 velForw_mean_fly, velForw_down_CI_fly, velForw_up_CI_fly,\
	                 velSide_mean_fly, velSide_down_CI_fly, velSide_up_CI_fly,\
	                 velTurn_mean_fly, velTurn_down_CI_fly, velTurn_up_CI_fly,\
	                 mainColor=mainColor, mainlabel=mainlabel, viceColor=viceColor, vicelabel=vicelabel, \
	                 filename=outputfilename, savedir=outDirCO2evtSumFly,\
				 )







			## This break is to jump to next fly after the current fly's data already goes through once
			break










