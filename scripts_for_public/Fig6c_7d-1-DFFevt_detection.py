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
import utils.plot_utils as plot_utils
import utils.list_twoP_exp as list_twoP_exp
import utils.list_behavior as list_behavior
import utils.math_utils as math_utils



experiments=list_twoP_exp.SS29579_SS51046_DFFevt_based_anlysis


# experiments=[

# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '001', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '002', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '003', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '004', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '005', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '006', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '007', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '008', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '009', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video



# # ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '001', {'kinx_factor':0.4,  'raw_thrsld':1, 'grad_raw_thrsld':0.5, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     
# # ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '002', {'kinx_factor':0.4,  'raw_thrsld':0.7, 'grad_raw_thrsld':0.5, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),   
# # ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '003', {'kinx_factor':0.2,  'raw_thrsld':1.5, 'grad_raw_thrsld':0.3, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),    
# # ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '004', {'kinx_factor':0.2,  'raw_thrsld':1.4, 'grad_raw_thrsld':0.3, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     
# # ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '005', {'kinx_factor':0.4,  'raw_thrsld':0.7, 'grad_raw_thrsld':0.5, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     
# # ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '006', {'kinx_factor':0.4,  'raw_thrsld':0.7, 'grad_raw_thrsld':0.5, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     
# # ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '007', {'kinx_factor':0.2,  'raw_thrsld':0.55, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     
# # ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '008', {'kinx_factor':0.4,  'raw_thrsld':0.7, 'grad_raw_thrsld':0.5, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     
# # ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '009', {'kinx_factor':0.4,  'raw_thrsld':0.7, 'grad_raw_thrsld':0.5, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     



# ]









##Assgining dFF difference for detecting dominant dFF events
dmnt_difference_thrsld=0.2






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


	return mean_trace, down_err_trace, up_err_trace


def find_maxGC_perROI(exp_lists_per_fly):

	print('Finding maximum GC among all recordings per fly')

	GC_set_per_fly=[]

	for date, genotype, fly, recrd_num, _ in exp_lists_per_fly:

		Gal4=genotype.split('-')[0]

		#dataDir = '/Users/clc/Documents/EPFL/NeLy/Data/ANproj/20180824/SS25451-tdTomGC6fopt-fly1/SS25451-tdTomGC6fopt-fly1-007'
		flyDir = NAS_AN_Proj_Dir + '03_general_2P_exp/' +Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'
		dataDir = flyDir+genotype+'-'+fly+'-'+recrd_num + '/'
		pathForDic = dataDir+'/output/'

		Beh_Jpos_GC_DicData=general_utils.open_Beh_Jpos_GC_DicData(pathForDic, 'SyncDic_7CamBeh_BW_20210619_GC-RES.p')

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

	print('Saving GCevent-based.dic')

	GCevt_dic={}
	GCevt_dic.update({'evt_bin_trace':evt_bin_trace})
	GCevt_dic.update({'evt_startIdx_list':evt_startIdx_list})
	GCevt_dic.update({'evt_endIdx_list':evt_endIdx_list})

	GCevt_dic.update({'samplingFreq':samplingFreq})
	GCevt_dic.update({'bsl_s':bsl_s})

	GCevt_dic.update({'GC_evt_set_list':GC_evt_set_list})
	GCevt_dic.update({'time_evt_list':time_evt_list})

	GCevt_dic.update({'rest_evt_list':rest_evt_list})
	GCevt_dic.update({'walk_evt_list':walk_evt_list})

	GCevt_dic.update({'eye_groom_evt_list':eye_groom_evt_list})
	GCevt_dic.update({'antennae_groom_evt_list':antennae_groom_evt_list})
	GCevt_dic.update({'foreleg_groom_evt_list':foreleg_groom_evt_list})

	GCevt_dic.update({'hindleg_groom_evt_list':hindleg_groom_evt_list})
	GCevt_dic.update({'Abd_groom_evt_list':Abd_groom_evt_list})

	GCevt_dic.update({'PER_evt_list':PER_evt_list})

	GCevt_dic.update({'F_groom_evt_list':F_groom_evt_list})
	GCevt_dic.update({'H_groom_evt_list':H_groom_evt_list})

	GCevt_dic.update({'CO2puff_evt_list':CO2puff_evt_list})

	GCevt_dic.update({'velForw_evt_list':velForw_evt_list})
	GCevt_dic.update({'velSide_evt_list':velSide_evt_list})
	GCevt_dic.update({'velTurn_evt_list':velTurn_evt_list})





	pickle.dump( GCevt_dic, open( save_dir + filename, "wb" ) ) 



	return



def save_GC_dominantEvt_dic(save_dir, filename):

	print('Saving GC_dmntEvt_dic.')

	GC_dmntEvt_dic={}
	GC_dmntEvt_dic.update({'dmnt_evt_startIdx_list':dmnt_evt_startIdx_list})
	GC_dmntEvt_dic.update({'dmnt_evt_endIdx_list':dmnt_evt_endIdx_list})

	GC_dmntEvt_dic.update({'samplingFreq':samplingFreq})
	GC_dmntEvt_dic.update({'bsl_s':bsl_s})

	GC_dmntEvt_dic.update({'GC_dmnt_evt_set_list':GC_dmnt_evt_set_list})
	GC_dmntEvt_dic.update({'time_dmnt_evt_list':time_dmnt_evt_list})

	GC_dmntEvt_dic.update({'rest_dmnt_evt_list':rest_dmnt_evt_list})
	GC_dmntEvt_dic.update({'walk_dmnt_evt_list':walk_dmnt_evt_list})

	GC_dmntEvt_dic.update({'eye_groom_dmnt_evt_list':eye_groom_dmnt_evt_list})
	GC_dmntEvt_dic.update({'antennae_groom_dmnt_evt_list':antennae_groom_dmnt_evt_list})
	GC_dmntEvt_dic.update({'foreleg_groom_dmnt_evt_list':foreleg_groom_dmnt_evt_list})

	GC_dmntEvt_dic.update({'hindleg_groom_dmnt_evt_list':hindleg_groom_dmnt_evt_list})
	GC_dmntEvt_dic.update({'Abd_groom_dmnt_evt_list':Abd_groom_dmnt_evt_list})

	GC_dmntEvt_dic.update({'PER_dmnt_evt_list':PER_dmnt_evt_list})

	GC_dmntEvt_dic.update({'F_groom_dmnt_evt_list':F_groom_dmnt_evt_list})
	GC_dmntEvt_dic.update({'H_groom_dmnt_evt_list':H_groom_dmnt_evt_list})

	GC_dmntEvt_dic.update({'CO2puff_dmnt_evt_list':CO2puff_dmnt_evt_list})	


	GC_dmntEvt_dic.update({'velForw_dmnt_evt_list':velForw_dmnt_evt_list})
	GC_dmntEvt_dic.update({'velSide_dmnt_evt_list':velSide_dmnt_evt_list})
	GC_dmntEvt_dic.update({'velTurn_dmnt_evt_list':velTurn_dmnt_evt_list})






	pickle.dump( GC_dmntEvt_dic, open( save_dir + filename, "wb" ) ) 



	return



##main##

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_Dir

bsl_s=EventDetection_utils.bsl_s



experiments_group_per_fly=general_utils.group_expList_per_fly(experiments)

print('experiments_group_per_fly', experiments_group_per_fly)

count_evt_fly=[]


for exp_lists_per_fly in experiments_group_per_fly:
	
	print('Processing ', exp_lists_per_fly ,'....')


	maxGC_per_fly_list=find_maxGC_perROI(exp_lists_per_fly)

	
	for date, genotype, fly, recrd_num, evtDetc_params in exp_lists_per_fly:

		kinx_factor=evtDetc_params['kinx_factor']
		raw_thrsld=evtDetc_params['raw_thrsld']
		grad_raw_thrsld=evtDetc_params['grad_raw_thrsld']
		diff_window=evtDetc_params['diff_window']
		evt_shortest_dur=evtDetc_params['evt_shortest_dur']
		evt_longest_dur=evtDetc_params['evt_longest_dur']

		Gal4=genotype.split('-')[0]

		#dataDir = '/Users/clc/Documents/EPFL/NeLy/Data/ANproj/20180824/SS25451-tdTomGC6fopt-fly1/SS25451-tdTomGC6fopt-fly1-007'
		flyDir = NAS_AN_Proj_Dir + '03_general_2P_exp/' +Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'
		dataDir = flyDir+genotype+'-'+fly+'-'+recrd_num + '/'
		pathForDic = dataDir+'/output/'



		print('dataDir', dataDir)

		outDirGCevt = NAS_AN_Proj_Dir + 'output/Fig6c_7d-DFF_event_corresponding_ballRot/dFF_evt_results/'+Gal4+'/'+date+'-'+genotype+'-'+fly+'-'+recrd_num+'/'
		if not os.path.exists(outDirGCevt):
			os.makedirs(outDirGCevt)

		outDirGCevt_plot = NAS_AN_Proj_Dir + 'output/Fig6c_7d-DFF_event_corresponding_ballRot/plots/'+Gal4+'/'
		if not os.path.exists(outDirGCevt_plot):
			os.makedirs(outDirGCevt_plot)


		Beh_Jpos_GC_DicData=general_utils.open_Beh_Jpos_GC_DicData(pathForDic, 'SyncDic_7CamBeh_BW_20210619_GC-RES.p')



		GC_set = Beh_Jpos_GC_DicData['GCset']
		timeSec = Beh_Jpos_GC_DicData['timeSec']

		rest = Beh_Jpos_GC_DicData['rest']
		f_walk = Beh_Jpos_GC_DicData['forward_walk']
		b_walk = Beh_Jpos_GC_DicData['backward_walk']

		walk = np.asarray(f_walk)+np.asarray(b_walk)

		eye_groom = Beh_Jpos_GC_DicData['eye_groom']
		antennae_groom = Beh_Jpos_GC_DicData['antennae_groom']
		foreleg_groom = Beh_Jpos_GC_DicData['foreleg_groom']
		print('shape foreleg_groom', np.shape(foreleg_groom))

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



		for ROI_i, GC_trace in enumerate(GC_set):

			outDirGCevt_ROI = outDirGCevt + 'ROI_'+str(ROI_i)+'/'
			if not os.path.exists(outDirGCevt_ROI):
				os.makedirs(outDirGCevt_ROI)

			print('len GC_trace', len(GC_trace))

			smth_GC_trace=EventDetection_utils.filtered_traces(GC_trace, filtermode='running_window', frame_window=int(0.6*samplingFreq)) #0.1s

			
			norm_range_smth_GC_trace ,_ ,_ = EventDetection_utils.normalize_trace(smth_GC_trace, frame_window=int(10*samplingFreq), mode='btwn_0and1')
			#print('norm_range_smth_GC_trace', norm_range_smth_GC_trace)
			Norm_GC_for_plot_2dlist=[]
			Norm_GC_for_plot_2dlist.append(norm_range_smth_GC_trace)
			


			evt_bin_trace, evt_startIdx_list, evt_endIdx_list = EventDetection_utils.detect_event(norm_range_smth_GC_trace, outDirGCevt_plot,  date+'-'+genotype+'-'+fly+'-'+recrd_num+'-ROI_'+str(ROI_i)+'_GCevt.png', fps=samplingFreq, \
			kinx_factor=kinx_factor, evt_shortest_dur=evt_shortest_dur, evt_longest_dur=evt_longest_dur, raw_thrsld=raw_thrsld, diff_thrsld=grad_raw_thrsld, diff_window=diff_window)


			print('evt_startIdx_list', evt_startIdx_list)
			print('evt_endIdx_list', evt_endIdx_list)
			print('evt_endIdx_list-evt_startIdx_list', (np.asarray(evt_endIdx_list)-np.asarray(evt_startIdx_list))/samplingFreq)
			print('\n', len(evt_startIdx_list), 'events are detected\n')

			
			
			GC_evt_set_list=[]
			for i, GC_trace in enumerate(GC_set):
				GC_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, GC_trace, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
				GC_evt_set_list.append(GC_evt_list)
			time_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, timeSec, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			rest_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, rest, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			walk_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, walk, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			eye_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, eye_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			foreleg_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, foreleg_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			antennae_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, antennae_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			hindleg_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, hindleg_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			Abd_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, Abd_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			PER_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, PER, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			F_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, F_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			H_groom_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, H_groom, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			CO2puff_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, CO2puff, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			velForw_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, velForw, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			velSide_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, velSide, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			velTurn_evt_list=EventDetection_utils.find_parallel_evt(evt_startIdx_list, evt_endIdx_list, velTurn, fps=samplingFreq, bsl_s=bsl_s, tail_s=0)
			print('shape GC_evt_set_list', np.shape(GC_evt_set_list))



			
			save_GCevt_dic(outDirGCevt_ROI, 'ROI#'+str(ROI_i)+'_GCevt_dic.pkl')


			## Find dominant event to analyze asymmetrical activity
			dmnt_evt_startIdx_list, dmnt_evt_endIdx_list=EventDetection_utils.find_dominant_event(evt_startIdx_list, evt_endIdx_list, GC_set, outDirGCevt_plot, Gal4 + '-'+date+'-'+genotype+'-'+fly+'-'+recrd_num+'-ROI_'+str(ROI_i)+'_dmnt_GCevt.png', ref_ROI=ROI_i, difference_thrsld=dmnt_difference_thrsld, mode='Norm_trace_to_0_1')

			if len(dmnt_evt_startIdx_list)==0:
				print('No dominant event is found. All events are symmetrical.\nNo need for further analysis')
				continue
			
			else:
				GC_dmnt_evt_set_list=[]
				for i, GC_trace in enumerate(GC_set):
					GC_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, GC_trace, fps=samplingFreq, bsl_s=bsl_s)
					GC_dmnt_evt_set_list.append(GC_dmnt_evt_list)
				time_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, timeSec, fps=samplingFreq, bsl_s=bsl_s)
				rest_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, rest, fps=samplingFreq, bsl_s=bsl_s)
				walk_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, walk, fps=samplingFreq, bsl_s=bsl_s)
				eye_groom_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, eye_groom, fps=samplingFreq, bsl_s=bsl_s)
				foreleg_groom_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, foreleg_groom, fps=samplingFreq, bsl_s=bsl_s)
				antennae_groom_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, antennae_groom, fps=samplingFreq, bsl_s=bsl_s)
				hindleg_groom_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, hindleg_groom, fps=samplingFreq, bsl_s=bsl_s)
				Abd_groom_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, Abd_groom, fps=samplingFreq, bsl_s=bsl_s)
				PER_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, PER, fps=samplingFreq, bsl_s=bsl_s)
				F_groom_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, F_groom, fps=samplingFreq, bsl_s=bsl_s)
				H_groom_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, H_groom, fps=samplingFreq, bsl_s=bsl_s)
				CO2puff_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, CO2puff, fps=samplingFreq, bsl_s=bsl_s)
				velForw_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, velForw, fps=samplingFreq, bsl_s=bsl_s)
				velSide_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, velSide, fps=samplingFreq, bsl_s=bsl_s)
				velTurn_dmnt_evt_list=EventDetection_utils.find_parallel_evt(dmnt_evt_startIdx_list, dmnt_evt_endIdx_list, velTurn, fps=samplingFreq, bsl_s=bsl_s)	

				print('shape GC_dmnt_evt_set_list', np.shape(GC_dmnt_evt_set_list))
				print('shape time_dmnt_evt_list', np.shape(time_dmnt_evt_list))

				print('ROI_i', ROI_i)
				save_GC_dominantEvt_dic(outDirGCevt_ROI, 'ROI#'+str(ROI_i)+'_dmnt_GCevt_dic.pkl')

				


