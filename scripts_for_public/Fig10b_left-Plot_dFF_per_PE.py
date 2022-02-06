import sys
import pickle
#import sys
import os
import re
import numpy as np
import random
from PIL import Image
Image.Image.tostring = Image.Image.tobytes
import matplotlib.pyplot as plt
import matplotlib
from skimage import io
from multiprocessing import Pool
import math
import scipy.stats
import time
from matplotlib import colors as mcolors
from itertools import groupby 
from itertools import chain


import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.list_twoP_exp as list_twoP_exp
import utils.sync_utils as sync_utils
import utils.math_utils as math_utils
import utils.EventDetection_utils as EventDetection_utils


experiments = list_twoP_exp.PE_dynamic_exp_list






def group_expList(list_exp, sort_by='fly'):


	list_exp.sort() 
	#print('list_exp', list_exp)
	#print('shape list_exp', np.shape(list_exp))

	if sort_by=='fly':
		exp_list = [list(i) for j, i in groupby(list_exp, lambda x: x[0]+x[1]+x[2])] 
	elif sort_by=='genotype':
		exp_list = [list(i) for j, i in groupby(list_exp, lambda x: x[1])] 

	#print('exp_list', exp_list)
	#print('shape exp_list', np.shape(exp_list))


    
	return exp_list




def open_GC_beh_PER_sync_DicData(pathForDic, startFrame, endFrame):


    if os.path.exists(pathForDic+'/DicDataForMovie_GC_PER_trim_camera6_'+str(startFrame)+'f-'+str(endFrame)+'f-RES.p'):
        
        DicData = pickle.load(open( pathForDic+'/DicDataForMovie_GC_PER_trim_camera6_'+str(startFrame)+'f-'+str(endFrame)+'f-RES.p', 'rb' ))
        
        frameCntr = DicData['frameCntr']
        GCset = DicData['GCset']

        CO2puff = DicData['CO2puff']
        Rest = DicData['rest']
        Walk = DicData['walk']
        Groom = DicData['groom']

        Etho_Idx_Dic = DicData['Etho_Idx_Dic']
        Etho_Timesec_Dic = DicData['Etho_Timesec_Dic']
        Etho_Colorcode_Dic = DicData['Etho_Colorcode_Dic']
        
        timeSec = DicData['timeSec']
        velForw_mm = DicData['velForw']
        velSide_mm = DicData['velSide']
        velTurn_deg = DicData['velTurn']

        PER_bin_trace = DicData['PER_bin_trace']
        PER_extLen = DicData['PER_extLen']
        PER_norm_baseFold_extenLen = DicData['PER_norm_baseFold_extenLen']

        startVidIdx = DicData['startVidIdx']
        stopVidIdx = DicData['stopVidIdx']


    else:
        print(pathForDic)
        print ("DicDataForMovie_GC_PER_trim_camera6.p not found - Data not analysed yet")
        sys.exit(0)

    return frameCntr, GCset, Rest, Walk, Groom, \
            Etho_Idx_Dic, Etho_Timesec_Dic, Etho_Colorcode_Dic, \
            CO2puff, timeSec, velForw_mm, velSide_mm, velTurn_deg, \
            PER_bin_trace, PER_extLen, PER_norm_baseFold_extenLen, \
            startVidIdx, stopVidIdx





def find_corresponding_evt_from_groupIdxs(groupIdxs, TargetTraceSet):

    

    if len(groupIdxs)>0:
  


        TargetsetEvt=[]
        for i in range(0,len(TargetTraceSet)):
            TargetsetEvt.append([])
            for j in range(0,len(groupIdxs)):    

                TargetsetEvt[i].append(TargetTraceSet[i][groupIdxs[j][0]:groupIdxs[j][-1]+1])


    else:
        TargetsetEvt=[]               
        for i in range(0,len(TargetTraceSet)):
            TargetsetEvt.append([])
            for j in range(0,len(groupIdxs)):           
                TargetsetEvt[i].append(np.nan)





    return TargetsetEvt



def find_interIdx(groupidxs):

	inter_groupIdx=[]
	for i, group_idx in enumerate(groupidxs):
		if i<len(groupidxs)-1:
			# print('groupidxs[i][-1]', groupidxs[i][-1])
			# print('groupidxs[i+1][0]', groupidxs[i+1][0])
			inter_groupIdx.append([])
			inter_groupIdx[i].append(groupidxs[i][-1])
			inter_groupIdx[i].append(groupidxs[i+1][0])



	return inter_groupIdx




def add_nan_to_make_same_length_event(target_trace, ref_trace):


    if len(target_trace)<len(ref_trace):
        #print('len(target_trace)', len(target_trace))
        nan_tail= [np.nan]*int(len(ref_trace)-len(target_trace))
        #print('len(nan_tail)', len(nan_tail))
        #nan_tail= [0]*int(len(timesec_beh_evt[-1])-len(GCsetEvt[i][j]))
        target_trace_nantail=np.append(target_trace,nan_tail)

    else:
    	target_trace_nantail=target_trace[0:len(ref_trace)]
        


    return target_trace_nantail


def xy_exchange(input_mat):

	new_length= max([len(array) for array in input_mat])

	# print('new_length', new_length)

	output_mat=[]


	for i in range(0, new_length):
		output_mat.append([])

	for i, ls_empty in enumerate(output_mat):
		for j, ls in enumerate(input_mat):
			if i<len(ls):
				ls_empty.append(ls[i])
			else:
				#ls_empty.append(None)
				continue


	return output_mat


def restructure_into_evtOrder(list_rcrdOrder):

	evts_count_list=[]
	for i, evts in enumerate(list_rcrdOrder):
		evts_count_list.append(len(evts))
	len_list_evtOrder=max(evts_count_list)

	list_evtOrder=[]
	for i in range(0,len_list_evtOrder):
		list_evtOrder.append([])
		for j, evts in enumerate(list_rcrdOrder):
			if i<len(evts):
				list_evtOrder[i].append(evts[i])
	
	
	return list_evtOrder






def compute_mean_CI_sem(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.nanmean(a, axis=0), scipy.stats.sem(a, axis=0, nan_policy='propagate')
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h, m-se, m+se






def count_flyNum_for_each_PER(ref_evt):


	counts_evt_per_order=[]
	for evt_order, evt_stacks in enumerate(ref_evt):
		counts_evt_per_order.append(len(evt_stacks))



	return counts_evt_per_order




def normalize_GCset_btwn_0_1(GC_set_ori):

	

	GC_set=GC_set_ori.copy()

	norm_GCset=[]

	for ROI_i, GC_trace in enumerate(GC_set):

		

		norm_GC_trace, _, _ = EventDetection_utils.normalize_trace(GC_trace, frame_window=int(1*dataFreq), mode='btwn_0and1')

		

		norm_GCset.append(norm_GC_trace)

	return norm_GCset







def Plot_avgDFF_per_evt(evts_set, n_num_each_evt, mode='SEM', savepath=None, filename=None):
	data_font_size=15
	data_ylabel_position=[-0.8,0.5]
	trace_width=2
	dataFreq=len(timeSec)/(timeSec[-1]-timeSec[0])

	ref_color='k'
	accompany_color='k'

	beh_photo_fps=30
	TwoP_frame_fps=1972/(timeSec[-1])


	pool_value_per_event_DS=[]	
	pool_mean_per_event=[]
	for ROI_i, ROI_evts in enumerate(evts_set): 
		pool_value_per_event_DS.append([])
		pool_mean_per_event.append([])
		for evt_i, ROI_evtStack in enumerate(ROI_evts):
			ROI_evtStack_DS=[]
			ROI_evtmeans=[]
			for evt in ROI_evtStack:

				evt_DS=general_utils.downsampling_trace(evt, int(dataFreq/TwoP_frame_fps))
				evt_mean=np.nanmean(evt)
				#print('shape evt_DS', np.shape(evt_DS))
				ROI_evtStack_DS.append(evt_DS)
				ROI_evtmeans.append(evt_mean)

			flatten_ROI_evtStack_DS=list(chain.from_iterable(ROI_evtStack_DS))
			#print('shape flatten_ROI_evtStack_DS', np.shape(flatten_ROI_evtStack_DS))
			pool_value_per_event_DS[ROI_i].append(flatten_ROI_evtStack_DS)
			pool_mean_per_event[ROI_i].append(ROI_evtmeans)
			


	inds = np.arange(1, len(n_num_each_evt) + 1)


	rows=len(pool_value_per_event_DS)+1
	fig = plt.figure(facecolor='white', figsize=(6, 15), dpi=170)
	fig.subplots_adjust(left=0.2, right = 0.95, wspace = 0.3, hspace = 0.6)


	ax_n_num=plt.subplot(rows,1,1)
	ax_n_num.plot(inds, n_num_each_evt, marker='o',  color='k', linewidth=1.5, markersize=3, zorder=3)

	ax_n_num.spines['top'].set_visible(False)
	ax_n_num.spines['right'].set_visible(False)
	ax_n_num.spines['bottom'].set_visible(True)
	ax_n_num.spines['left'].set_visible(True)
	ax_n_num.spines['bottom'].set_linewidth(trace_width)
	ax_n_num.spines['left'].set_linewidth(trace_width)
	ax_n_num.set_xlabel('PER#',size=data_font_size, color='k')
	ax_n_num.set_ylabel('Counts',size=data_font_size,color='k')	
	ax_n_num.tick_params(axis='both', colors='k',top=False,right=False,bottom=True,left=True,labelsize=data_font_size, width=trace_width)
	ax_n_num.set_xlim(0, 12)

	legend_bp=[]
	for i, data in enumerate(pool_mean_per_event):



		if i == 0:
			# marker='o'
			marker=''
			linestyle='-'
			color_roi='k'
			position=list(np.arange(1, 3*(len(data)),3))
		elif i==1:
			# marker='D'
			marker=''
			linestyle='--'
			color_roi='k'
			position=list(np.arange(1, 3*(len(data)),3)+1)

		ticks=np.arange(1, 3*(len(data)),3)+0.5
		



		ax_accompany = 'ax_accompany' + str(i)
		ax_accompany=plt.subplot(rows,1,2)

		mean_evts=[]
		downCI_evts=[]
		upCI_evts=[]
		downSEM_evts=[]
		upSEM_evts=[]
		for evt_i, evts_pool in enumerate(data):

			mean, downCI, upCI, downSEM, upSEM = compute_mean_CI_sem(evts_pool, confidence=0.95)

			mean_evts.append(mean)
			downCI_evts.append(downCI)
			upCI_evts.append(upCI)
			downSEM_evts.append(downSEM)
			upSEM_evts.append(upSEM)

		inds = np.arange(1, len(mean_evts) + 1)

		if mode=='SEM':
			ax_accompany.plot(inds, mean_evts, marker=marker, color=accompany_color, linestyle=linestyle, linewidth=1.5, markersize=6, zorder=3,label='ROI_'+str(i))
			ax_accompany.vlines(inds, downSEM_evts, upSEM_evts, color=accompany_color, linestyle='-', lw=1.5)
		elif mode=='CI':
			ax_accompany.plot(inds, mean_evts, marker=marker,  color=accompany_color, linestyle=linestyle, linewidth=1.5, markersize=6, zorder=3, label='ROI_'+str(i))
			ax_accompany.vlines(inds, downCI_evts, upCI_evts, color=accompany_color, linestyle='-', lw=1.5)	
		
		if mode =='box':
			color_box=color_roi
			bp=ax_accompany.boxplot(data, positions=position, notch=False)
			for box in bp['boxes']:
			    # change outline color
			    box.set( color=color_box, linewidth=1, linestyle=linestyle)
			    # # change fill color
			    # box.set( facecolor = 'w' )

			## change color and linewidth of the whiskers
			for whisker in bp['whiskers']:
			    whisker.set(color=color_box, linewidth=1, linestyle=linestyle)

			## change color and linewidth of the caps
			for cap in bp['caps']:
			    cap.set(color=color_box, linewidth=0, linestyle=linestyle)

			## change color and linewidth of the medians
			for median in bp['medians']:
			    median.set(color=color_box, linewidth=1, linestyle=linestyle)

			## change the style of fliers and their fill
			for flier in bp['fliers']:
			    flier.set(marker='o', color=color_box, alpha=0.5)

			legend_bp.append(bp["boxes"][0])

			
	
	if mode =='box':
		ax_accompany.set_xticks(ticks)
		ax_accompany.set_xticklabels([str(x) for x in list(np.arange(1,len(data)+1))])



	ax_accompany.spines['top'].set_visible(False)
	ax_accompany.spines['right'].set_visible(False)
	ax_accompany.spines['bottom'].set_visible(True)
	ax_accompany.spines['left'].set_visible(True)
	ax_accompany.spines['bottom'].set_linewidth(trace_width)
	ax_accompany.spines['left'].set_linewidth(trace_width)
	ax_accompany.set_xlabel('PER#',size=data_font_size, color='k')
	ax_accompany.set_ylabel(r'$\Delta$'+'F/F (%)',size=data_font_size,color='k')	
	ax_accompany.tick_params(axis='both', colors='k',top=False,right=False,bottom=True,left=True,labelsize=data_font_size, width=trace_width)
	ax_accompany.set_xlim(0, 3*11+0.5)
	ax_accompany.set_ylim(-0.52, 1.25)
	#ax_accompany.set_ylim(-0.2,1) #option for pllotting normalized trace
	ax_accompany.legend(legend_bp, ["ROI 0", "ROI 1"], loc='upper right')




	plt.savefig(savepath+filename+'.png' , facecolor=fig.get_facecolor(), edgecolor='none', transparent=True) #bbox_inches='tight',      
	plt.savefig(savepath+filename+'.pdf', facecolor=fig.get_facecolor(), edgecolor='none', transparent=True) #bbox_inches='tight', 

	plt.clf
	plt.close(fig)


	return








## main ##


NAS_Dir=general_utils.NAS_Dir


NAS_AN_Proj_public_Dir=general_utils.NAS_AN_Proj_public_Dir
AN_Proj_Dir = NAS_AN_Proj_public_Dir




experiments_group_per_genotype=group_expList(experiments, sort_by='genotype')
print('experiments_group_per_genotype', experiments_group_per_genotype)




for exp_list_per_genotype in experiments_group_per_genotype:
	Etho_time_genotype_Dic={}
	Etho_time_genotype_Dic['PER_evt']=[]

	PERbased_GCevt_genotype_in_recrdOrder=[]
	PERbased_PERevt_genotype_in_recrdOrder=[]

	interPER_GCevt_genotype_in_recrdOrder=[]
	interPER_PERev_genotype_in_recrdOrder=[]

	PERtrainbased_GCevt_genotype_in_recrdOrder=[]
	PERtrainbased_PERevt_genotype_in_recrdOrder=[]


	GC_gapfree_genotype=[]

	dataFreq_list=[]

	count_recrd=0




	experiments_group_per_fly=group_expList(exp_list_per_genotype, sort_by='fly')
	print('experiments_group_per_fly', experiments_group_per_fly)


	for exp_lists_per_fly in experiments_group_per_fly:
	    print('Processing per fly for ... ', exp_lists_per_fly )

	    Etho_time_fly_Dic={}
	    # Etho_time_fly_Dic['walk_evt']=[]
	    # Etho_time_fly_Dic['groom_evt']=[]
	    # Etho_time_fly_Dic['rest_evt']=[]
	    Etho_time_fly_Dic['PER_evt']=[]



	    PER_GCevt_fly=[]
	    GC_gapfree_fly=[]

	    maxGC_fly=0
	    minGC_fly=0

	    
	    # Process in single recording
	    for date, genotype, fly, recrd_num, startFrame, endFrame in exp_lists_per_fly:

	        Gal4=genotype.split('-')[0]

	        flyDir = AN_Proj_Dir +'07_SS31232-PE_exp/'+ Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'
	        dataDir = flyDir+genotype+'-'+fly+'-'+recrd_num + '/'
	        pathForDic = dataDir+'output/PER/camera_6/'




	        frameCntr, GC_set, Rest_bin_trace, Walk_bin_trace, Groom_bin_trace, \
	        Etho_Idx_Dic, Etho_Timesec_Dic, Etho_Colorcode_Dic, \
	        CO2puff, timeSec, velForw_mm, velSide_mm, velTurn_deg, \
	        PER_bin_trace, PER_extLen_px, PER_norm_baseFold_extenLen,\
	        startVidIdx, stopVidIdx = open_GC_beh_PER_sync_DicData(pathForDic, startFrame, endFrame)

	        count_recrd+=1
	        dataFreq=len(timeSec)/(timeSec[-1]-timeSec[0])

	        dataFreq_list.append(dataFreq)





	        norm_GC_set=normalize_GCset_btwn_0_1(GC_set)




	        GC_set=norm_GC_set


	        Etho_time_fly_Dic['PER_evt'].append(Etho_Timesec_Dic['PER_evt'])
	        Etho_time_genotype_Dic['PER_evt'].append(Etho_Timesec_Dic['PER_evt'])
	        # print("shape Etho_time_genotype_Dic['PER_evt']", np.shape(Etho_time_genotype_Dic['PER_evt']))

	        ## find GC and PER trace during PER events
	        idx_PER_evt = Etho_Idx_Dic['PER_evt']
	        PERbased_GC_evt_set=find_corresponding_evt_from_groupIdxs(idx_PER_evt, GC_set)
	        PERbased_PERlen_evt_set=find_corresponding_evt_from_groupIdxs(idx_PER_evt, [PER_extLen_px])

	        PERbased_GCevt_genotype_in_recrdOrder.append(PERbased_GC_evt_set)
	        PERbased_PERevt_genotype_in_recrdOrder.extend(PERbased_PERlen_evt_set)

	        ## find GC and PER trace during inter-PER events
	        idx_inter_PER_evt=find_interIdx(idx_PER_evt)
	        #print('idx_inter_PER_evt', idx_inter_PER_evt)
	        inter_PERbased_GC_evt_set=find_corresponding_evt_from_groupIdxs(idx_inter_PER_evt, GC_set)
	        inter_PERbased_PERlen_evt_set=find_corresponding_evt_from_groupIdxs(idx_inter_PER_evt, [PER_extLen_px])

	        interPER_GCevt_genotype_in_recrdOrder.append(inter_PERbased_GC_evt_set)
	        interPER_PERev_genotype_in_recrdOrder.extend(inter_PERbased_PERlen_evt_set)


	        PE_train_start_idx=Etho_Idx_Dic['PER_evt'][0][0]
	        PE_train_end_idx=Etho_Idx_Dic['PER_evt'][-1][-1]
	        idx_PER_train=[*range(PE_train_start_idx, PE_train_end_idx+1, 1)]


	        PERtrainbased_GC_evt_set=find_corresponding_evt_from_groupIdxs([idx_PER_train], GC_set)
	        PERtrainbased_PERlen_evt_set=find_corresponding_evt_from_groupIdxs([idx_PER_train], [PER_extLen_px])

	        PERtrainbased_GCevt_genotype_in_recrdOrder.append(PERtrainbased_GC_evt_set)
	        PERtrainbased_PERevt_genotype_in_recrdOrder.extend(PERtrainbased_PERlen_evt_set)

	       



	genotype_PER_summary=AN_Proj_Dir+'output/Fig10b_left-PE_dynamic/plots/'
	if not os.path.exists(genotype_PER_summary):
		os.makedirs(genotype_PER_summary)


	print('recording counts =', count_recrd)


	## transform into ROI-order GC event set

	PERbased_GCevt_genotype_in_ROIOrder=xy_exchange(PERbased_GCevt_genotype_in_recrdOrder)
	interPER_GCevt_genotype_in_ROIOrder=xy_exchange(interPER_GCevt_genotype_in_recrdOrder)


	PERbased_PERevt_genotype_in_evtOrder = restructure_into_evtOrder(PERbased_PERevt_genotype_in_recrdOrder)
	PERtrainbased_GCevt_genotype_in_ROIOrder=xy_exchange(PERtrainbased_GCevt_genotype_in_recrdOrder)


	


	PERbased_GCevt_genotype_in_ROIOrder_evtOrder=[]
	for i in range(0,len(PERbased_GCevt_genotype_in_ROIOrder)):
		PERbased_GCevt_genotype_in_evtOrder_per_ROI=restructure_into_evtOrder(PERbased_GCevt_genotype_in_ROIOrder[i])
		PERbased_GCevt_genotype_in_ROIOrder_evtOrder.append(PERbased_GCevt_genotype_in_evtOrder_per_ROI)
	
	interPER_GCevt_genotype_in_ROIOrder_evtOrder=[]
	for i in range(0,len(interPER_GCevt_genotype_in_ROIOrder)):
		interPER_GCevt_genotype_in_ROIOrder_per_ROI=restructure_into_evtOrder(interPER_GCevt_genotype_in_ROIOrder[i])
		interPER_GCevt_genotype_in_ROIOrder_evtOrder.append(interPER_GCevt_genotype_in_ROIOrder_per_ROI)

	PERtrainbased_GCevt_genotype_in_ROIOrder_rmPseudoEvtOrder=[]
	for ROI_i, ROI_evts in enumerate(PERtrainbased_GCevt_genotype_in_ROIOrder):
		PERtrainbased_GCevt_genotype_in_ROIOrder_rmPseudoEvtOrder.append([])
		for evt_i, evt in enumerate(ROI_evts):
			PERtrainbased_GCevt_genotype_in_ROIOrder_rmPseudoEvtOrder[ROI_i].extend(evt)







	sum_evts=0
	for i, trace in enumerate(PERbased_GCevt_genotype_in_ROIOrder_evtOrder[0]):
		#print(len(trace))
		sum_evts+=len(trace)
	print('sum_evts =', sum_evts)


	n_num_each_PER=count_flyNum_for_each_PER(PERbased_PERevt_genotype_in_evtOrder)
	# print('n_num_each_PER', n_num_each_PER)



	# print('dataFreq_list', dataFreq_list)
	dataFreq=np.mean(dataFreq_list)


	Plot_avgDFF_per_evt(PERbased_GCevt_genotype_in_ROIOrder_evtOrder, n_num_each_PER, mode='box', savepath=genotype_PER_summary, filename='normDFF_per_evt_Box')	











