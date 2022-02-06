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
import itertools

import utils.EventDetection_utils as EventDetection_utils
import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.list_twoP_exp as list_twoP_exp
import utils.list_behavior as list_behavior
import utils.math_utils as math_utils



# experiments=list_twoP_exp.SS29579_SS51046_DFFevt_based_anlysis

experiments=[

('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '001', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '002', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '003', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '004', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '005', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '006', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '007', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '008', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video
('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '009', {'kinx_factor':0.4,  'raw_thrsld':0.4, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}), # no video



# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '001', {'kinx_factor':0.4,  'raw_thrsld':1, 'grad_raw_thrsld':0.5, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '002', {'kinx_factor':0.4,  'raw_thrsld':0.7, 'grad_raw_thrsld':0.5, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),   
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '003', {'kinx_factor':0.2,  'raw_thrsld':1.5, 'grad_raw_thrsld':0.3, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),    
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '004', {'kinx_factor':0.2,  'raw_thrsld':1.4, 'grad_raw_thrsld':0.3, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '005', {'kinx_factor':0.4,  'raw_thrsld':0.7, 'grad_raw_thrsld':0.5, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '006', {'kinx_factor':0.4,  'raw_thrsld':0.7, 'grad_raw_thrsld':0.5, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '007', {'kinx_factor':0.2,  'raw_thrsld':0.55, 'grad_raw_thrsld':0.2, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '008', {'kinx_factor':0.4,  'raw_thrsld':0.7, 'grad_raw_thrsld':0.5, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '009', {'kinx_factor':0.4,  'raw_thrsld':0.7, 'grad_raw_thrsld':0.5, 'diff_window':0.3, 'evt_shortest_dur':0.5, 'evt_longest_dur':2}),     



]


bsl_dur_s=EventDetection_utils.bsl_s





def count_ROIs_from_folder(exp_lists_current_fly):

	for date, genotype, fly, recrd_num, evtDetc_params in exp_lists_current_fly:

		Gal4=genotype.split('-')[0]

		#dataDir = '/Users/clc/Documents/EPFL/NeLy/Data/ANproj/20180824/SS25451-tdTomGC6fopt-fly1/SS25451-tdTomGC6fopt-fly1-007'
		flyDir = NAS_AN_Proj_Dir + '03_general_2P_exp/' +Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'
		dataDir = flyDir+genotype+'-'+fly+'-'+recrd_num + '/'
		pathForDic = dataDir+'/output/'
		outDirGCevt = NAS_AN_Proj_Dir + 'output/Fig6c_7e-DFF_event_corresponding_ballRot/dFF_evt_results/'+Gal4+'/'+date+'-'+genotype+'-'+fly+'-'+recrd_num+'/'

		folder_content=os.listdir(outDirGCevt)
		print('folder_content', folder_content)

		

		ROI_folder_list=[]
		for content in folder_content:
			if content[:4]=='ROI_':
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






def retrieve_Jpos_dic(Jpos_related_dic):

	J_Pos_retrv={}
	for leg in list_behavior.leg_order:
		for joint in list_behavior.joint_order:
			for coord in list_behavior.list_xyz:
				J_pos_ID=leg+' '+joint+' '+coord
				J_Pos_retrv.update({J_pos_ID:Jpos_related_dic[J_pos_ID]})

	return J_Pos_retrv




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

	
	# print('Computing event mean and CI ...')

	# args_for_pool=[]
	# for j in range(0,np.shape(dataset)[1]):
		
	# 	args_for_pool.append([j, dataset, confidence, least_realNum_amount])




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

	for date, genotype, fly, recrd_num , evt_detect_params in exp_lists_per_fly:

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




def downsampling_jpos_evt_dic(Jpos_evt_jointBased_dic):


	Jpos_evt_jointBased_dic_DS={}
	for jointID, evt_list in Jpos_evt_jointBased_dic.items():

		evt_list_DS=[]
		for evt in evt_list:
			evt_DS=general_utils.downsampling_trace(evt, int(samplingFreq/beh_photo_fps))
			evt_list_DS.append(evt_DS)

		Jpos_evt_jointBased_dic_DS.update({jointID:evt_list_DS})


	return Jpos_evt_jointBased_dic_DS



def flatten_evt_for_jpos_evt_dic(Jpos_evt_jointBased_dic):


	Jpos_evt_jointBased_dic_flatten={}
	for jointID, evt_list in Jpos_evt_jointBased_dic.items():
		#print('shape evt_list', np.shape(evt_list))
		flatten_evt_list=[]
		for evt in evt_list:
			flatten_evt_list.extend(evt)
		#print('shape evt_lst_concat', np.shape(evt_lst_concat))
		Jpos_evt_jointBased_dic_flatten.update({jointID:flatten_evt_list})

	return Jpos_evt_jointBased_dic_flatten







##main##

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_Dir


experiments_group_per_fly=general_utils.group_expList_per_fly(experiments)

print('experiments_group_per_fly', experiments_group_per_fly)

count_evt_fly=[]



beh_photo_fps=30

least_realNum_amount=3


for exp_lists_per_fly in experiments_group_per_fly:

	print('Processing ', exp_lists_per_fly ,'....')

	## All events
	GC_evt_set_fly=[]
	time_evt_fly=[]



	velForw_evt_fly=[]
	velSide_evt_fly=[]
	velTurn_evt_fly=[]



	## dominat event list
	GC_dmnt_evt_set_fly=[]
	time_dmnt_evt_fly=[]



	velForw_dmnt_evt_fly=[]
	velSide_dmnt_evt_fly=[]
	velTurn_dmnt_evt_fly=[]




	ROI_amount=count_ROIs_from_folder(exp_lists_per_fly)
	model_list_struc=[]
	for i in range(0,ROI_amount):
		model_list_struc.append([])

	GC_evt_set_fly=make_structure_as_modelStructure(GC_evt_set_fly, model_list_struc)
	time_evt_fly=make_structure_as_modelStructure(time_evt_fly, model_list_struc)

	velForw_evt_fly=make_structure_as_modelStructure(velForw_evt_fly, model_list_struc)
	velSide_evt_fly=make_structure_as_modelStructure(velSide_evt_fly, model_list_struc)
	velTurn_evt_fly=make_structure_as_modelStructure(velTurn_evt_fly, model_list_struc)

	print('shape GC_evt_set_fly', np.shape(GC_evt_set_fly))



	GC_dmnt_evt_set_fly=make_structure_as_modelStructure(GC_dmnt_evt_set_fly, model_list_struc)
	time_dmnt_evt_fly=make_structure_as_modelStructure(time_dmnt_evt_fly, model_list_struc)
	
	velForw_dmnt_evt_fly=make_structure_as_modelStructure(velForw_dmnt_evt_fly, model_list_struc)
	velSide_dmnt_evt_fly=make_structure_as_modelStructure(velSide_dmnt_evt_fly, model_list_struc)
	velTurn_dmnt_evt_fly=make_structure_as_modelStructure(velTurn_dmnt_evt_fly, model_list_struc)



	#Process each recording
	for date, genotype, fly, recrd_num, evt_detect_params in exp_lists_per_fly:

		Gal4=genotype.split('-')[0]

		#dataDir = '/Users/clc/Documents/EPFL/NeLy/Data/ANproj/20180824/SS25451-tdTomGC6fopt-fly1/SS25451-tdTomGC6fopt-fly1-007'
		flyDir = NAS_AN_Proj_Dir + '03_general_2P_exp/' +Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'
		dataDir = flyDir+genotype+'-'+fly+'-'+recrd_num + '/'
		pathForDic = dataDir+'/output/'

		print('dataDir', dataDir)

		outDirGCevt = NAS_AN_Proj_Dir + 'output/Fig6c_7e-DFF_event_corresponding_ballRot/dFF_evt_results/'+Gal4+'/'+date+'-'+genotype+'-'+fly+'-'+recrd_num+'/'
		if not os.path.exists(outDirGCevt):
			os.makedirs(outDirGCevt)

		outDirGCevt_plot = NAS_AN_Proj_Dir + 'output/Fig6c_7e-DFF_event_corresponding_ballRot/plots/'+Gal4+'/'
		if not os.path.exists(outDirGCevt_plot):
			os.makedirs(outDirGCevt_plot)


		for ROI_i in range(0, ROI_amount):


			print('\nProcessing in ROI event\n')

			outDirGCevt_ROI = outDirGCevt+ 'ROI_'+str(ROI_i)+'/'
			if not os.path.exists(outDirGCevt_ROI):
				os.makedirs(outDirGCevt_ROI)

			print('Reading', 'GCevt_ROI#'+str(ROI_i)+'_dic.pkl', '...')



			if os.path.exists(outDirGCevt_ROI+'ROI#'+str(ROI_i)+'_GCevt_dic.pkl'):
				evt_dic=EventDetection_utils.read_evt_dic(outDirGCevt_ROI, 'ROI#'+str(ROI_i)+'_GCevt_dic.pkl')
			else:
				print('No GCevt_dic.pkl exists mainly due to no GC event is detected ...')
				continue


			evt_startIdx_list=evt_dic['evt_startIdx_list']
			evt_endIdx_list=evt_dic['evt_endIdx_list']
			samplingFreq=evt_dic['samplingFreq']

			GC_evt_set_list=evt_dic['GC_evt_set_list']

			time_evt_list=evt_dic['time_evt_list']


			velForw_evt_list=evt_dic['velForw_evt_list']
			velSide_evt_list=evt_dic['velSide_evt_list']
			velTurn_evt_list=evt_dic['velTurn_evt_list']

			print(len(GC_evt_set_list[ROI_i]), 'GC event found')



			print('shape GC_evt_set_list', np.shape(GC_evt_set_list))
			for i, GC_evts in enumerate(GC_evt_set_list):
				if len(GC_evt_set_fly[ROI_i])!=ROI_amount:
					GC_evt_set_fly[ROI_i].append([])
				GC_evt_set_fly[ROI_i][i].extend(GC_evt_set_list[i])
			time_evt_fly[ROI_i].extend(time_evt_list)

			velForw_evt_fly[ROI_i].extend(velForw_evt_list)
			velSide_evt_fly[ROI_i].extend(velSide_evt_list)
			velTurn_evt_fly[ROI_i].extend(velTurn_evt_list)

			print('shape GC_evt_set_fly[ROI_i]', np.shape(GC_evt_set_fly[ROI_i]))

			GC_for_plot=[
			GC_evt_set_fly[ROI_i][0][0],
			GC_evt_set_fly[ROI_i][1][0]
			]
			

			## Dominant event
			if not os.path.exists(outDirGCevt_ROI+'/ROI#'+str(ROI_i)+'_dmnt_GCevt_dic.pkl'):
				print('There is no dominant GC event found in this ROI.\nPass to next ROI ...')
			else:

				print('\nProcessing in dominant event\n')

				dmnt_evt_dic=EventDetection_utils.read_evt_dic(outDirGCevt_ROI, 'ROI#'+str(ROI_i)+'_dmnt_GCevt_dic.pkl')
				dmnt_evt_startIdx_list=dmnt_evt_dic['dmnt_evt_startIdx_list']
				dmnt_evt_endIdx_list=dmnt_evt_dic['dmnt_evt_endIdx_list']

				GC_dmnt_evt_set_list=dmnt_evt_dic['GC_dmnt_evt_set_list']
				time_dmnt_evt_list=dmnt_evt_dic['time_dmnt_evt_list']



				velForw_dmnt_evt_list=dmnt_evt_dic['velForw_dmnt_evt_list']
				velSide_dmnt_evt_list=dmnt_evt_dic['velSide_dmnt_evt_list']
				velTurn_dmnt_evt_list=dmnt_evt_dic['velTurn_dmnt_evt_list']


				print(len(GC_dmnt_evt_set_list[0]), 'dominant GC event found')



				for i, GC_evts in enumerate(GC_dmnt_evt_set_list):
					if len(GC_dmnt_evt_set_fly[ROI_i])!=ROI_amount:
						GC_dmnt_evt_set_fly[ROI_i].append([])
					GC_dmnt_evt_set_fly[ROI_i][i].extend(GC_dmnt_evt_set_list[i])			
				time_dmnt_evt_fly[ROI_i].extend(time_dmnt_evt_list)
				velForw_dmnt_evt_fly[ROI_i].extend(velForw_dmnt_evt_list)
				velSide_dmnt_evt_fly[ROI_i].extend(velSide_dmnt_evt_list)
				velTurn_dmnt_evt_fly[ROI_i].extend(velTurn_dmnt_evt_list)






	## Plotting event per fly
	for date, genotype, fly, recrd_num, evt_detect_params in exp_lists_per_fly:

		

		Gal4=genotype.split('-')[0]

		flyDir = NAS_AN_Proj_Dir + Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly
		


		outDirGCevtSumFly = outDirGCevt_plot + 'Summary/'
		if not os.path.exists(outDirGCevtSumFly):
			os.makedirs(outDirGCevtSumFly)

		GC_evt_set_NaNtail_fly=[]
		GC_dmntevt_set_NaNtail_fly=[]

		

		for ROI_i in range(0, ROI_amount):



			print('\nProcessing in fly pool events', date, genotype, fly, 'ROI#', ROI_i ,'\n')

			outDirGCevtSumFly_ROI = outDirGCevtSumFly
			if not os.path.exists(outDirGCevtSumFly_ROI):
				os.makedirs(outDirGCevtSumFly_ROI)	

			print(len(GC_evt_set_fly[ROI_i][0]), 'pool GC event found')

			print('shape GC_evt_set_fly', np.shape(GC_evt_set_fly))



			GC_evt_set_NaNtail_fly.append([])
			for i in range(0, len(GC_evt_set_fly[ROI_i])):
				GC_evt_set_NaNtail_fly[ROI_i].append([])
				GC_evtNaNtail_fly=add_NaNtail_to_each_Evt(GC_evt_set_fly[ROI_i][i])
				print('shape GC_evtNaNtail_fly', np.shape(GC_evtNaNtail_fly))
				GC_evt_set_NaNtail_fly[ROI_i][i].extend(GC_evtNaNtail_fly)
			time_evtNaNtail_fly=add_NaNtail_to_each_Evt(time_evt_fly[ROI_i])
			velForw_evtNaNtail_fly=add_NaNtail_to_each_Evt(velForw_evt_fly[ROI_i])
			velSide_evtNaNtail_fly=add_NaNtail_to_each_Evt(velSide_evt_fly[ROI_i])
			velTurn_evtNaNtail_fly=add_NaNtail_to_each_Evt(velTurn_evt_fly[ROI_i])

		# plot_utils.Plot_traces(GC_evtNaNtail_fly, outDirGCevtSumFly_ROI, 'ROI#'+str(ROI_i)+'_GCevt_fly_overlay.png', subtitle_list=[str(len(GC_evtNaNtail_fly))+' GC event fly overlay'], plot_mode='overlay')

			print('Computing mean and CI for pool GC events ...')
			GC_mean_fly, GC_downCI_fly, GC_upCI_fly=[],[],[]
			for i in range(0, len(GC_evt_set_NaNtail_fly[ROI_i])):
				GC_evtNaNtail_fly=GC_evt_set_NaNtail_fly[ROI_i][i]
				GC_mean_fly.append([])
				GC_downCI_fly.append([])
				GC_upCI_fly.append([])
				GC_mean, GC_down_CI, GC_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(GC_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
				GC_mean_fly[i].extend(GC_mean)
				GC_downCI_fly[i].extend(GC_down_CI)
				GC_upCI_fly[i].extend(GC_up_CI)				
	
			velForw_mean_fly, velForw_down_CI_fly, velForw_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(velForw_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			velSide_mean_fly, velSide_down_CI_fly, velSide_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(velSide_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
			velTurn_mean_fly, velTurn_down_CI_fly, velTurn_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(velTurn_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)


			CI_null_fly=[0]*len(velForw_down_CI_fly)
	
			print(len(GC_evt_set_fly[ROI_i]), 'pool GC event found')



			bsl_s=EventDetection_utils.bsl_s
			len_sort_time_evt_fly=sorted(time_evt_fly[ROI_i], key=len)
			time_boundary=[0-bsl_s, len_sort_time_evt_fly[-1][-1]-len_sort_time_evt_fly[-1][0]-bsl_s]



			plot_utils.Plot_GCEvt_avg_err(time_boundary, \
                     GC_mean_fly, GC_downCI_fly, GC_upCI_fly,\
                     velForw_mean_fly, velForw_down_CI_fly, velForw_up_CI_fly,\
                     velSide_mean_fly, velSide_down_CI_fly, velSide_up_CI_fly,\
                     velTurn_mean_fly, velTurn_down_CI_fly, velTurn_up_CI_fly,\
                     target_ROI=ROI_i, filename='ROI#'+str(ROI_i)+'_DFFevt_based_sumBeh_ballrota', savedir=outDirGCevtSumFly_ROI)			


			


			## Dominant event
			

			if len(GC_dmnt_evt_set_fly[ROI_i])==0:
				print('There is no dominant GC event found in this ROI.\nPass to next ROI ...')
				GC_dmntevt_set_NaNtail_fly.append([])
			

			else:

				print('\nProcessing in fly pool dominant event', date, genotype, fly, 'ROI#', ROI_i, '\n')

				print(len(GC_dmnt_evt_set_fly[ROI_i][0]), 'dominant GC event found')

				print('ROI_i', ROI_i)

				GC_dmntevt_set_NaNtail_fly.append([])

				
				for i in range(0, len(GC_dmnt_evt_set_fly[ROI_i])):
					print(i)
					GC_dmntevt_set_NaNtail_fly[ROI_i].append([])
					GC_dmntevtNaNtail_fly=add_NaNtail_to_each_Evt(GC_dmnt_evt_set_fly[ROI_i][i])
					GC_dmntevt_set_NaNtail_fly[ROI_i][i].extend(GC_dmntevtNaNtail_fly)
				time_dmntevtNaNtail_fly=add_NaNtail_to_each_Evt(time_dmnt_evt_fly[ROI_i])
				velForw_dmnt_evtNaNtail_fly=add_NaNtail_to_each_Evt(velForw_dmnt_evt_fly[ROI_i])
				velSide_dmnt_evtNaNtail_fly=add_NaNtail_to_each_Evt(velSide_dmnt_evt_fly[ROI_i])
				velTurn_dmnt_evtNaNtail_fly=add_NaNtail_to_each_Evt(velTurn_dmnt_evt_fly[ROI_i])


				# plot_utils.Plot_traces(GC_dmnt_evtNaNtail_fly, outDirGCevtSumFly_ROI, 'ROI#'+str(ROI_i)+'_dmnt_GCevt_fly_overlay.png', subtitle_list=[str(len(GC_dmnt_evtNaNtail_fly))+' Dominant GC event fly overlay'], plot_mode='overlay')


				print('Computing mean and CI for pool dominant GC events ...')
				GC_dmnt_mean_fly, GC_dmnt_down_CI_fly, GC_dmnt_up_CI_fly=[],[],[]
				for i in range(0, len(GC_dmntevt_set_NaNtail_fly[ROI_i])):
					GC_dmntevtNaNtail_fly=GC_dmntevt_set_NaNtail_fly[ROI_i][i]
					GC_dmnt_mean_fly.append([])
					GC_dmnt_down_CI_fly.append([])
					GC_dmnt_up_CI_fly.append([])
					GC_mean, GC_down_CI, GC_up_CI = compute_CI_and_mean_trace_w_BehfreqCorrec(GC_dmntevtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
					GC_dmnt_mean_fly[i].extend(GC_mean)
					GC_dmnt_down_CI_fly[i].extend(GC_down_CI)
					GC_dmnt_up_CI_fly[i].extend(GC_up_CI)	

				velForw_dmnt_mean_fly, velForw_dmnt_down_CI_fly, velForw_dmnt_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(velForw_dmnt_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
				velSide_dmnt_mean_fly, velSide_dmnt_down_CI_fly, velSide_dmnt_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(velSide_dmnt_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)
				velTurn_dmnt_mean_fly, velTurn_dmnt_down_CI_fly, velTurn_dmnt_up_CI_fly = compute_CI_and_mean_trace_w_BehfreqCorrec(velTurn_dmnt_evtNaNtail_fly, confidence=0.95, least_realNum_amount=least_realNum_amount)


				CI_dmnt_null_fly=[0]*len(velForw_dmnt_down_CI_fly)



				bsl_s=EventDetection_utils.bsl_s
				len_sort_time_dmntevt_fly=sorted(time_dmnt_evt_fly[ROI_i], key=len)
				time_boundary_dmnt=[0-bsl_s, len_sort_time_dmntevt_fly[-1][-1]-len_sort_time_dmntevt_fly[-1][0]-bsl_s]


				# plot_utils.Plot_traces(GC_dmnt_mean_fly, outDirGCevtSumFly_ROI, 'GC_dmnt_mean.pdf', subtitle_list=['GC_dmnt']*len(GC_mean_fly), plot_mode='row_by_row')


				plot_utils.Plot_GCEvt_avg_err(time_boundary_dmnt, \
	                     GC_dmnt_mean_fly, GC_dmnt_down_CI_fly, GC_dmnt_up_CI_fly,\
	                     velForw_dmnt_mean_fly, velForw_dmnt_down_CI_fly, velForw_dmnt_up_CI_fly,\
	                     velSide_dmnt_mean_fly, velSide_dmnt_down_CI_fly, velSide_dmnt_up_CI_fly,\
	                     velTurn_dmnt_mean_fly, velTurn_dmnt_down_CI_fly, velTurn_dmnt_up_CI_fly,\
	                     target_ROI=ROI_i, filename='ROI#'+str(ROI_i)+'_dmntDFFevt_based_sumBeh_ballrota', savedir=outDirGCevtSumFly_ROI)
	                     	

		## This break is to jump to next fly after the current fly's data already goes through once
		break










