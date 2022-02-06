import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import matplotlib
plt.switch_backend('agg')
import sys
import pandas as pd 
import os
import pickle
from multiprocessing import Pool
from itertools import repeat




import utils.EventDetection_utils as EventDetection_utils
import utils.general_utils as general_utils
import utils.sync_utils as sync_utils
import utils.plot_utils as plot_utils
import utils.list_twoP_exp as list_twoP_exp
import utils.list_behavior as list_behavior
import utils.math_utils as math_utils





experiments=list_twoP_exp.SS36112_CO2puff_BW_analysis







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
		Evt_len_list.append(len(evt))

	max_EvtLen=max(Evt_len_list)

	# print('max_EvtLen', max_EvtLen)

	EvtNaNtail_list=[]
	for evt in Evt_list:
		evt_NaNtail=general_utils.add_NaN_tail(evt, max_EvtLen)
		#print('len evt_NaNtail', len(evt_NaNtail))
		EvtNaNtail_list.append(evt_NaNtail)

	return EvtNaNtail_list






def worker_for_CI_mean_trace(idx, dataset, confidence, least_realNum_amount):

	dataset=np.asarray(dataset)
	# print('idx', idx)
	# print('shape dataset', np.shape(dataset))
	# print('least_realNum_amount', least_realNum_amount)
	# print('len dataset', len(dataset))
	data=dataset[:, idx]
	

	non_nan_counts=data.size - np.count_nonzero(np.isnan(data))

	if non_nan_counts > least_realNum_amount:

		nonnan_data_list=data[np.logical_not(np.isnan(data))] 

		(mean, down_CI, up_CI) = math_utils.compute_CI_and_mean(nonnan_data_list, confidence=confidence)

		return mean, down_CI, up_CI

	else:

		return np.nan, np.nan, np.nan




def compute_CI_and_mean_trace(dataset, confidence=0.95, least_realNum_amount=4):

	
	print('Computing event mean amd CI ...')

	# args_for_pool=[]
	# for j in range(0,np.shape(dataset)[1]):
		
	# 	args_for_pool.append([j, dataset, confidence, least_realNum_amount])




	idx_range=[i for i in range(0,np.shape(dataset)[1])]
	# print('colums_range', colums_range)

	p=Pool()
	mean_downCI_upCI = p.starmap(worker_for_CI_mean_trace, zip(idx_range, repeat(dataset), repeat(confidence), repeat(least_realNum_amount)))
	#mean_trace, down_err_trace, up_err_trace = p.starmap(worker_for_CI_mean_trace, args_for_pool)

	p.close()
	p.join()
	del p	

	mean_trace=np.asarray(mean_downCI_upCI)[:,0]
	down_err_trace=np.asarray(mean_downCI_upCI)[:,1]
	up_err_trace=np.asarray(mean_downCI_upCI)[:,2]


	# print('compute mean and confidence interval...')
	# mean_trace=[]
	# down_err_trace=[]
	# up_err_trace=[]

	# dataset=np.asarray(dataset)
	# # print('np.shape(dataset)', np.shape(dataset))
	# # print('dataset[:, 0]', dataset[:,2])

	# for j in range(0,np.shape(dataset)[1]):

	# 	data=dataset[:, j]

	# 	non_nan_counts=data.size - np.count_nonzero(np.isnan(data))

	# 	print('idx', j, 'non_nan_counts', non_nan_counts)

	# 	#if np.count_nonzero(~np.isnan(dataset[:, j]))>=least_realNum_amount:
	# 	if non_nan_counts > least_realNum_amount:

	# 		print('Computing CI and mean')

	# 		nonnan_data_list=data[np.logical_not(np.isnan(data))] 

	# 		mean, down_CI, up_CI = math_utils.compute_CI_and_mean(nonnan_data_list, confidence=confidence)
	# 		print('mean', mean)

	# 		mean_trace.append(mean)
	# 		down_err_trace.append(down_CI)
	# 		up_err_trace.append(up_CI)

	# 	else:
	# 		print('< leat number for computing mean and CI. Appending NaN')
	# 		mean_trace.append(np.nan)
	# 		down_err_trace.append(np.nan)
	# 		up_err_trace.append(np.nan)
    

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

		Beh_Jpos_GC_DicData=general_utils.open_Beh_Jpos_GC_DicData(pathForDic, 'SyncDic_7CamBeh20210507_WalkRest_by_ball_GC-RES.p')

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




def save_GCevt_dic(save_dir, filename):

	

	GCevt_dic={}
	GCevt_dic.update({'evt_bin_trace':evt_bin_trace})
	GCevt_dic.update({'evt_startIdx_list':evt_startIdx_list})
	GCevt_dic.update({'evt_endIdx_list':evt_endIdx_list})

	GCevt_dic.update({'samplingFreq':samplingFreq})
	GCevt_dic.update({'bsl_s':bsl_s})

	GCevt_dic.update({'GC_evt_set_list':GC_evt_set_list})
	GCevt_dic.update({'time_evt_list':time_evt_list})

	GCevt_dic.update({'rest_evt_list':rest_evt_list})
	GCevt_dic.update({'f_walk_evt_list':f_walk_evt_list})
	GCevt_dic.update({'b_walk_evt_list':b_walk_evt_list})

	GCevt_dic.update({'eye_groom_evt_list':eye_groom_evt_list})
	GCevt_dic.update({'antennae_groom_evt_list':antennae_groom_evt_list})
	GCevt_dic.update({'foreleg_groom_evt_list':foreleg_groom_evt_list})

	GCevt_dic.update({'hindleg_groom_evt_list':hindleg_groom_evt_list})
	GCevt_dic.update({'Abd_groom_evt_list':Abd_groom_evt_list})

	GCevt_dic.update({'PER_evt_list':PER_evt_list})

	GCevt_dic.update({'F_groom_evt_list':F_groom_evt_list})
	GCevt_dic.update({'H_groom_evt_list':H_groom_evt_list})

	GCevt_dic.update({'CO2puff_evt_list':CO2puff_evt_list})
	GCevt_dic.update({'BW_beyong_CO2puff_evt_list':BW_beyong_CO2puff_evt_list})

	GCevt_dic.update({'velForw_evt_list':velForw_evt_list})
	GCevt_dic.update({'velSide_evt_list':velSide_evt_list})
	GCevt_dic.update({'velTurn_evt_list':velTurn_evt_list})


	# for item, value in J_Pos_evt.items():
	# 	GCevt_dic.update({item:value})



	pickle.dump( GCevt_dic, open( save_dir + filename, "wb" ) ) 

	print('Saving '+filename+' done!')



	return




##main##

bsl_s=EventDetection_utils.bsl_s
tail_s=EventDetection_utils.tail_s
event_max_dur=2.5
event_min_dur=0.27


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


	for exp_lists_per_fly in experiments_group_per_fly:
		
		print('Processing ', exp_lists_per_fly ,'....')


		#maxGC_per_fly_list=find_maxGC_perROI(exp_lists_per_fly)

		
		for date, genotype, fly, recrd_num in exp_lists_per_fly:

			Gal4=genotype.split('-')[0]

			flyDir = NAS_AN_Proj_Dir +'03_general_2P_exp/'+ Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'
			dataDir = flyDir+genotype+'-'+fly+'-'+recrd_num + '/'
			pathForDic = dataDir+'/output/'

			print('dataDir', dataDir)

			outDirCO2evt = NAS_AN_Proj_Dir + 'output/FigS5-CO2puff_BW_analysis_SS36112/' +Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num + '/output/CO2evt_based_BehBallAnalysis/'
			if not os.path.exists(outDirCO2evt):
				os.makedirs(outDirCO2evt)

			# Beh_Jpos_GC_DicData=general_utils.open_Beh_Jpos_GC_DicData(pathForDic, 'SyncDic_7CamBeh20210507_WalkRest_by_ball_GC-RES.p')
			Beh_Jpos_GC_DicData=general_utils.open_Beh_Jpos_GC_DicData(pathForDic, 'SyncDic_7CamBeh_BW_20210619_GC-RES.p')


			GC_set = Beh_Jpos_GC_DicData['GCset']
			timeSec = Beh_Jpos_GC_DicData['timeSec']

			rest = Beh_Jpos_GC_DicData['rest']
			f_walk = Beh_Jpos_GC_DicData['forward_walk']
			b_walk = Beh_Jpos_GC_DicData['backward_walk']

			eye_groom = Beh_Jpos_GC_DicData['eye_groom']
			antennae_groom = Beh_Jpos_GC_DicData['antennae_groom']
			foreleg_groom = Beh_Jpos_GC_DicData['foreleg_groom']

			hindleg_groom = Beh_Jpos_GC_DicData['hindleg_groom']
			Abd_groom = Beh_Jpos_GC_DicData['Abd_groom']

			PER = Beh_Jpos_GC_DicData['PER']

			F_groom = Beh_Jpos_GC_DicData['F_groom']
			H_groom = Beh_Jpos_GC_DicData['H_groom']

			CO2puff = Beh_Jpos_GC_DicData['CO2puff']

			velForw = Beh_Jpos_GC_DicData['velForw']
			velSide = Beh_Jpos_GC_DicData['velSide']
			velTurn = Beh_Jpos_GC_DicData['velTurn']


			samplingFreq=int(len(timeSec)/timeSec[-1])

			print('len timeSec', len(timeSec))
			print('samplingFreq', samplingFreq)

			BW_beyong_CO2puff=sync_utils.make_new_bin_trace_excluding_otherBeh(b_walk, excld_beh_bin_trace=CO2puff, timeSec=timeSec)


			# evt_bin_trace, evt_startIdx_list, evt_endIdx_list = EventDetection_utils.detect_event(CO2puff, outDirCO2evt, 'CO2evt_all.png', fps=samplingFreq, kinx_factor=1, evt_shortest_dur=0.2, evt_longest_dur=10, raw_thrsld=0.001, diff_thrsld=0.001, diff_window=0.001, select_specific_dur_evt=True)
			
			if datatype=='CO2evt_long_dic':
				dic_filename='CO2evt_long_dic'
				evt_bin_trace, evt_startIdx_list, evt_endIdx_list = EventDetection_utils.detect_event(CO2puff, outDirCO2evt,  'CO2evt_long.png', Plot=True, fps=samplingFreq, kinx_factor=1, evt_shortest_dur=1, evt_longest_dur=10, raw_thrsld=0.001, diff_thrsld=0.001, diff_window=0.001, select_specific_dur_evt=True)
			elif datatype=='CO2evt_short_dic':
				dic_filename='CO2evt_short_dic'
				evt_bin_trace, evt_startIdx_list, evt_endIdx_list = EventDetection_utils.detect_event(CO2puff, outDirCO2evt,  'CO2evt_short.png', Plot=True, fps=samplingFreq, kinx_factor=1, evt_shortest_dur=0.2, evt_longest_dur=3, raw_thrsld=0.001, diff_thrsld=0.001, diff_window=0.001, select_specific_dur_evt=True)
			elif datatype=='BWwoCO2evt_dic':
				dic_filename='BWwoCO2evt_dic'
				evt_bin_trace, evt_startIdx_list, evt_endIdx_list = EventDetection_utils.detect_event(BW_beyong_CO2puff, outDirCO2evt,  'BWwoCO2evt.png', Plot=True, fps=samplingFreq, kinx_factor=1, evt_shortest_dur=0.2, evt_longest_dur=4, raw_thrsld=0.001, diff_thrsld=0.001, diff_window=0.001, select_specific_dur_evt=True)
			elif datatype=='BWwCO2evt_dic':
				dic_filename='BWwCO2evt_dic'
				evt_bin_trace, evt_startIdx_list, evt_endIdx_list = EventDetection_utils.detect_event(b_walk, outDirCO2evt,  'BWwCO2evt.png', Plot=True, fps=samplingFreq, kinx_factor=1, evt_shortest_dur=0.2, evt_longest_dur=4, raw_thrsld=0.001, diff_thrsld=0.001, diff_window=0.001, select_specific_dur_evt=True)

			


			if len(evt_startIdx_list)!=0:

				GC_evt_set_list=[]
				for i, GC_trace in enumerate(GC_set):
					GC_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, GC_trace, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
					GC_evt_set_list.append(GC_evt_list)
				time_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, timeSec, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				rest_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, rest, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				f_walk_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, f_walk, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				b_walk_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, b_walk, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				eye_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, eye_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				foreleg_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, foreleg_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				antennae_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, antennae_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				hindleg_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, hindleg_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				Abd_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, Abd_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				PER_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, PER, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				F_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, F_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				H_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, H_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				CO2puff_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, CO2puff, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				BW_beyong_CO2puff_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, BW_beyong_CO2puff, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)

				velForw_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, velForw, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				velSide_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, velSide, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)
				velTurn_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, velTurn, fps=samplingFreq, bsl_s=bsl_s, tail_s=tail_s)

				
				

				# CO2evt_trace_subtitle=['0', '1', '2', '3', '4', '5']
				# plot_utils.Plot_traces(CO2puff_evt_list, outDirCO2evt, 'CO2evts_trace.png', subtitle_list=CO2evt_trace_subtitle, plot_mode='row_by_row')
				

				print('\n', len(evt_startIdx_list), 'events are detected\n', 'saving into _evt_dic.pkl', 'Baseline duration is set to', bsl_s,'s')
				# save_GCevt_dic(outDirCO2evt, 'CO2evt_all_dic.pkl')
				# save_GCevt_dic(outDirCO2evt, 'CO2evt_long_dic.pkl')
				# save_GCevt_dic(outDirCO2evt, 'CO2evt_short_dic.pkl')
				# save_GCevt_dic(outDirCO2evt, 'CO2_BW_BWwoCO2evt_dic.pkl')
				# save_GCevt_dic(outDirCO2evt, 'BWevt_dic.pkl')
				save_GCevt_dic(outDirCO2evt, dic_filename+'.pkl')


			else:
				print('\n', len(evt_startIdx_list), 'events are detected\n', 'no _evt_dic.pkl is saved...')
				
				# if os.path.exists(outDirCO2evt+'CO2evt_all_dic.pkl'):
				# 	os.remove(outDirCO2evt+'CO2evt_all_dic.pkl')
				# if os.path.exists(outDirCO2evt+'CO2evt_long_dic.pkl'):
				# 	os.remove(outDirCO2evt+'CO2evt_long_dic.pkl')
				# if os.path.exists(outDirCO2evt+'CO2evt_short_dic.pkl'):
				# 	os.remove(outDirCO2evt+'CO2evt_short_dic.pkl')
				# if os.path.exists(outDirCO2evt+'CO2_BW_BWwoCO2evt_dic.pkl'):
				# 	os.remove(outDirCO2evt+'CO2_BW_BWwoCO2evt_dic.pkl')
				# if os.path.exists(outDirCO2evt+'BWevt_dic.pkl'):
				# 	os.remove(outDirCO2evt+'BWevt_dic.pkl')
				if os.path.exists(outDirCO2evt+dic_filename+'.pkl'):
					os.remove(outDirCO2evt+dic_filename+'.pkl')







