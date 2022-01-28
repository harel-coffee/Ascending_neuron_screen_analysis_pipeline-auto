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

# Representative_TwoP_recordings_sparseLine_list=[



# ('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '001'), # no video
# ('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '002'),
# ('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '003'),
# ('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '004'),
# ('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '005'),
# ('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '006'),


# ('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '001'), # no video
# ('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '002'), # no video
# ('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '003'), # no video
# ('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '004'),
# ('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '005'),
# ('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '006'),
# ('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '007'),
# ('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '008'),
# ('20190517', 'SS36112-tdTomGC6fopt', 'fly1', '009'),

# ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '001'), 
# ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '002'), 
# ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '003'),
# ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '004'),
# ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '005'),
# ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '006'),
# ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '007'),
# ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '008'),


# ('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '001'),
# ('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '002'),
# ('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '004'),
# ('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '005'),
# ('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '006'), 
# ('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '007'),
# ('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '008'),
# ('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '009'),
# ('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '010'),
# ('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '011'),
# ('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '012'),
# ('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '013'),

# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '001'), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '002'), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '003'), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '004'), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '005'), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '006'), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '007'), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '008'), # no video
# ('20190221', 'SS29579-tdTomGC6fopt', 'fly1', '009'), # no video


# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '001'),
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '002'),
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '003'),
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '004'),
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '005'),
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '006'),
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '007'),
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '008'),
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '009'),


# ('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '001'),
# ('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '002'),
# ('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '003'),
# ('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '004'),
# ('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '005'), # no video
# ('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '006'), # no video


# ]

 

experiments=TwoP_recordings_sparseLine_list






def sorting_roiID_correspondingMat_based_on_an_order(roi_id_list, corrspd_list, base_of_order_list):



	# if len(roi_id_list)!=len(base_of_order_list):
	# 	print('ROI numbers does not match. Reordering ROI IDs cannot be done ...')
	# 	sys.exit(0)

	ressembled_name_for_baseOrder_list=[]
	for i, id_name in enumerate(base_of_order_list):
		ressembled_name=id_name.split(' ')[0]+'-ROI#'+id_name.split(' ')[1]
		ressembled_name_for_baseOrder_list.append(ressembled_name)


	sorted_new_roi_id_list=[]
	sorted_new_corrspd_list=[]


	numbers_for_old_order=[]
	for i, id_name in enumerate(roi_id_list):
		if id_name in roi_id_list:
			numbers_for_old_order.append(ressembled_name_for_baseOrder_list.index(id_name))

	# print('numbers_for_old_order', numbers_for_old_order)


	zipped_id_lists = zip(numbers_for_old_order, roi_id_list)
	sorted_zipped_id_lists = sorted(zipped_id_lists)
	sorted_new_roi_id_list = [element for _, element in sorted_zipped_id_lists]
	# print('sorted_new_roi_id_list', sorted_new_roi_id_list)


	zipped_corrspd_lists = zip(numbers_for_old_order, corrspd_list)
	sorted_zipped_corrspd_lists = sorted(zipped_corrspd_lists)
	sorted_new_corrspd_list = [element for _, element in sorted_zipped_corrspd_lists]


	return sorted_new_roi_id_list, sorted_new_corrspd_list





def mask_out_dFF_based_on_p_value(dFF_list_ori, ref_mat):



	dFF_list = [x[:] for x in dFF_list_ori]
	mask_list = [y[:] for y in ref_mat]

	# min_dff=np.nanmin(dFF_list_ori)


	# print('type dFF_list_ori', type(dFF_list_ori))
	# print('type dFF_list_ori[0]', type(dFF_list_ori[0]))
	# print('type dFF_list_ori[0][0]', type(dFF_list_ori[0][0]))

	if len(ref_mat)==0:
		print('base_mat is not given. The refrent matrix for masking is obligatory...')
		sys.exit(0)

	for roi_i, p_values_per_roi in enumerate(ref_mat):
		for beh_i, p_value in enumerate(p_values_per_roi):
			if p_value>0.05 or np.isnan(p_value):
				dFF_list[roi_i][beh_i]=0


	for roi_i, p_values_per_roi in enumerate(ref_mat):
		for beh_i, p_value in enumerate(p_values_per_roi):
			if p_value>0.05 or np.isnan(p_value):
				mask_list[roi_i][beh_i]=1
			else:
				mask_list[roi_i][beh_i]=np.nan


	return dFF_list, mask_list



def mask_out_dFF_based_on_normality(dFF_list_ori, normality_array):


	dFF_list = [x[:] for x in dFF_list_ori]
	mask_list = [y[:] for y in ref_mat]





	if len(ref_mat)==0:
		print('base_mat is not given. The refrent matrix for masking is obligatory...')
		sys.exit(0)

	for roi_i, p_values_per_roi in enumerate(normality_array):
		for beh_i, p_value in enumerate(p_values_per_roi):
			if p_value>0.05 or np.isnan(p_value):
				dFF_list[roi_i][beh_i]=0


	for roi_i, p_values_per_roi in enumerate(ref_mat):
		for beh_i, p_value in enumerate(p_values_per_roi):
			if p_value>0.05 or np.isnan(p_value):
				mask_list[roi_i][beh_i]=1
			else:
				mask_list[roi_i][beh_i]=np.nan




	return



def add_missing_cols_rows_to_posthocDf(missing_name_list, assigned_val_for_missing_name, original_name_list, posthoc_results_df):

	print('missing_name_list', missing_name_list)
	# print('original_name_list', original_name_list)
	# print('posthoc_results_df', posthoc_results_df)
	# print('type posthoc_results_df', type(posthoc_results_df))


	val_col_temp = [assigned_val_for_missing_name]*len(original_name_list)
	# print('val_col_temp', val_col_temp)

	# print('posthoc_results_df.columns\n', posthoc_results_df.columns)
	# print('posthoc_results_df.index\n', posthoc_results_df.index)

	new_posthoc_results_df = pd.DataFrame(columns = original_name_list)
	for col in posthoc_results_df.columns:
		# print(col)
		for beh in posthoc_results_df.index:
			# print('beh', beh)
			idx_beh=original_name_list.index(beh)
			# print('idx_beh', idx_beh)

			val_col_temp[idx_beh]=posthoc_results_df[col][beh]

		new_posthoc_results_df[col]=val_col_temp
		val_col_temp = [assigned_val_for_missing_name]*len(original_name_list)

	for col in missing_name_list:
		idx_col=original_name_list.index(col)
		val_col_temp[idx_col]=float(1)
		# print('val_col_temp',val_col_temp)
		new_posthoc_results_df[col]=val_col_temp
		val_col_temp = [assigned_val_for_missing_name]*len(original_name_list)

	new_posthoc_results_df=new_posthoc_results_df.set_axis(original_name_list, axis='index')

	# val_diagonal=posthoc_results_df['Bsl']['Bsl']
	# print('val_diagonal', val_diagonal)
	# for col in new_posthoc_results_df.columns:
	# 	new_posthoc_results_df.loc[col,col]=val_diagonal


	# print('new_posthoc_results_df\n', new_posthoc_results_df)
	# print('type new_posthoc_results_df', type(new_posthoc_results_df))


	return new_posthoc_results_df



def trim_smthRow_of_list(list2d, startIdx=0, endIdx=-1, fps=1500, smth_window_s=0):
    trim_2dlist=[]
    for row in list2d:
        #print('len row', len(row))
        if startIdx<len(row)-1:
            trim_row=row[startIdx:endIdx]
            # trim_row= sync_utils.smooth_data(trim_row, windowlen=int(fps*smth_window_s))
            #print('len trim_row', len(trim_row))
            trim_2dlist.append(trim_row)

    return trim_2dlist


def overlap_btwn_two_list(short_list, long_list):

	common_element_list=np.intersect1d(short_list, long_list)

	# common_element_list=list(set(short_list).intersection(long_list))
	overlap_perc=len(common_element_list)/len(short_list)

	# print('overlap_perc', overlap_perc)

	return overlap_perc



def deciding_bsl_evt_list_from_beh_evt_lists(all_beh_meanlist_list, name_list):

	datafreq=1500

	# for choosing the evt set with lowest mean and enough (>30) event numbers as the basline events

	beh_mean_list=[]
	freq_beh_list=[]
	for beh_i, meanlist_list in enumerate(all_beh_meanlist_list):
		# print('meanlist_list', meanlist_list)
		freq_beh_list.append(len(meanlist_list))
		if len(meanlist_list)>50: #50
			# print('meanlist_list', meanlist_list)
			# print('shape meanlist_list', np.shape(meanlist_list))
			# meanlist_beh = math_utils.compute_mean_with_diffrerent_row_length(meanlist_list)
			mean_beh=np.nanmean(meanlist_list)
			# median_beh = np.nanmedian(meanlist)
			# print('mean_beh', mean_beh)
			beh_mean_list.append(mean_beh)
		else:
			beh_mean_list.append(np.nan)



	# print('name_list', name_list)
	# print('freq_beh_list', freq_beh_list)
	# print('beh_mean_list', beh_mean_list)

	idx_min_mean = beh_mean_list.index(np.nanmin(beh_mean_list))

	bsl_meanlist_list = all_beh_meanlist_list[idx_min_mean]
	# print( 'bsl_meanlist_list',bsl_meanlist_list)
	# print('shape bsl_meanlist_list', np.shape(bsl_meanlist_list))
	bsl_mean_1dlist=[np.nanmean(x) for x in bsl_meanlist_list]
	# print('shape bsl_mean_1dlist', np.shape(bsl_mean_1dlist))
	bsl_mean=np.nanmean(bsl_mean_1dlist)


	print('baseline beh event is ', name_list[idx_min_mean])


	return bsl_mean_1dlist, bsl_mean



def prep_eachBehEvts_for_stat(name_list, eachBeh_evts_set, bsl_evts_list, bsl_data_1dlist, min_evt_num=3, bsl_s=1, cutting_head_s=0.7, data_freq=1500):

	print('preparing the data for statistics ...')

	# print('len bsl_data_1dlist', len(bsl_data_1dlist))
	# print('len bsl_evts_list', len(bsl_evts_list))

	evt_count_list=[]
	for i, beh_GCevt in enumerate(eachBeh_evts_set):
		evt_count=len(beh_GCevt)
		evt_count_list.append(evt_count)
	print('evt_count_list', evt_count_list)
	mean_evt_count=int(np.nanmean(evt_count_list))

	# resample_bsl_datapoints=np.random.choice(bsl_data_1dlist, size=len(1*bsl_evts_list))
	resample_bsl_datapoints=np.random.choice(bsl_data_1dlist, size=mean_evt_count) #100, 110, 125, 150, 200 are tried so far
	# print('len resample_bsl_datapoints', len(resample_bsl_datapoints))
	bsl_mean_list=math_utils.compute_mean_with_diffrerent_row_length(bsl_evts_list, samplerate=data_freq, cutting_head_s=cutting_head_s)
	bsl_mean=np.nanmean(bsl_mean_list)
	# print('bsl_mean', bsl_mean)

	all_beh_meanlist_list=[]
	all_beh_mean=[]
	all_beh_evtCount=[]
	non_overlapBsl_perc_list=[]



	


	for i, beh_GCevt in enumerate(eachBeh_evts_set):

		print('-',name_list[i], 'has', len(beh_GCevt), 'events')

		all_beh_evtCount.append(len(beh_GCevt))

		if len(beh_GCevt)>min_evt_num:
			GCevt_fly_wo_bsl = trim_smthRow_of_list(beh_GCevt, startIdx=int(data_freq*(bsl_s)))
			print('len GCevt_fly_wo_bsl', len(GCevt_fly_wo_bsl))
			# print(name_list[i], 'shape GCevt_fly_wo_bsl', np.shape(GCevt_fly_wo_bsl))
			evtmean_list=math_utils.compute_mean_with_diffrerent_row_length(GCevt_fly_wo_bsl, samplerate=data_freq, cutting_head_s=cutting_head_s)
			print('len evtmean_list', len(evtmean_list))
			# print('evtmean_list', evtmean_list)

			# resample_beh_datapoints=np.random.choice(general_utils.flatten_list(GCevt_fly_wo_bsl), size=len(1*beh_GCevt))
			# resample_beh_datapoints=np.random.choice(general_utils.flatten_list(GCevt_fly_wo_bsl), size=100) 
			# print('resample_beh_datapoints', resample_beh_datapoints)

			## ------------------------------------------------------------------
			## choose the mean of each epoch or resampled datapoint from every epochs in the same length of epoch numbers
			## 1.
			beh_data_for_stats=evtmean_list	
			## 2.
			# beh_data_for_stats=resample_beh_datapoints
			## ------------------------------------------------------------------

	
			# print(name_list[i], 'shape beh_data_for_stats', np.shape(beh_data_for_stats))

			if len(beh_data_for_stats)>min_evt_num:
				mean_evt=np.nanmean(beh_data_for_stats)-bsl_mean
				# print(name_list[i], 'mean_evt', mean_evt)
				f_GCevt_fly_wo_bsl=general_utils.flatten_list(GCevt_fly_wo_bsl)
				overlap_bsl_perc=overlap_btwn_two_list(f_GCevt_fly_wo_bsl, bsl_data_1dlist)
				print(name_list[i], 'overlap_bsl_perc', overlap_bsl_perc)
				if overlap_bsl_perc>0.9:
					mean_evt=0
					beh_data_for_stats=bsl_mean_list			
			else:
				mean_evt=0
				beh_data_for_stats=[np.nan]	
				overlap_bsl_perc=1.1
		else:
			mean_evt=0
			beh_data_for_stats=[np.nan]	
			overlap_bsl_perc=1.1

		all_beh_meanlist_list.append(beh_data_for_stats)
		all_beh_mean.append(mean_evt)
		non_overlapBsl_perc_list.append(1-overlap_bsl_perc)

		# print('all_beh_mean', all_beh_mean)


	return all_beh_meanlist_list, all_beh_mean, non_overlapBsl_perc_list, resample_bsl_datapoints






def anova_w_dataset(all_beh_meanlist_list, beh_name_list):

	print('ANOVA ...')

	# print('all_beh_meanlist_list', all_beh_meanlist_list)

	new_all_beh_meanlist_list_for_anova=[]
	new_beh_name_list_for_anova=[]
	missing_beh_meanlist_list=[]
	missing_beh_name_list=[]
	for i, meanlist in enumerate(all_beh_meanlist_list):
		print('len(meanlist)', len(meanlist))
		if len(meanlist)>1:
			new_all_beh_meanlist_list_for_anova.append(meanlist)
			new_beh_name_list_for_anova.append(beh_name_list[i])
		else:
			missing_beh_meanlist_list.append(meanlist)
			missing_beh_name_list.append(beh_name_list[i])

			bsl_mean_list=all_beh_meanlist_list[beh_name_list.index('Bsl')]
			new_all_beh_meanlist_list_for_anova.append(bsl_mean_list)
			new_beh_name_list_for_anova.append(beh_name_list[i])






	count_nanlist=sum(map(lambda x : x==[np.nan], missing_beh_meanlist_list))

	print('')

	if count_nanlist==len(all_beh_meanlist_list)-1:

		p_value_ANOVA=1
		print('p_value_ANOVA', p_value_ANOVA)

		row = [1.0]*len(beh_name_list)
		# print('row\n', row)

		null_mat=[row]*len(beh_name_list)
		# print('null_mat\n', null_mat)

		posthoc_results_anova=pd.DataFrame(null_mat)
		posthoc_results_anova=posthoc_results_anova.set_axis(beh_name_list, axis='columns')
		posthoc_results_anova=posthoc_results_anova.set_axis(beh_name_list, axis='index')



	else:

		ANOVA_value, p_value_ANOVA=scipy.stats.f_oneway(\
			*new_all_beh_meanlist_list_for_anova
			)
		print('p_value_ANOVA', p_value_ANOVA)
		#print('new_all_beh_meanlist_list_for_anova', new_all_beh_meanlist_list_for_anova)

		if p_value_ANOVA<0.05:

			print('len new_all_beh_meanlist_list_for_anova', len(new_all_beh_meanlist_list_for_anova))
			print('len new_beh_name_list_for_anova', len(new_beh_name_list_for_anova))
			print('new_beh_name_list_for_anova', new_beh_name_list_for_anova)
 

			posthoc_results_tukey=scikit_posthocs.posthoc_tukey(np.array(new_all_beh_meanlist_list_for_anova))
			# posthoc_results_scheffe=scikit_posthocs.posthoc_scheffe(np.array(new_all_beh_meanlist_list_for_anova))
			# posthoc_results_ttest=scikit_posthocs.posthoc_ttest(np.array(new_all_beh_meanlist_list_for_anova))
			# posthoc_results_tamhane=scikit_posthocs.posthoc_tamhane(np.array(new_all_beh_meanlist_list_for_anova))

			posthoc_results_anova=posthoc_results_tukey
			posthoc_results_anova=posthoc_results_anova.set_axis(new_beh_name_list_for_anova, axis='columns')
			posthoc_results_anova=posthoc_results_anova.set_axis(new_beh_name_list_for_anova, axis='index')

			posthoc_results_anova=add_missing_cols_rows_to_posthocDf(missing_beh_name_list, np.nan, beh_name_list, posthoc_results_anova)

			print('posthoc_results_tukey\n', posthoc_results_tukey)
			# print('posthoc_results_scheffe\n', posthoc_results_scheffe)
			# print('posthoc_results_ttest\n', posthoc_results_ttest)
			# print('posthoc_results_tamhane\n', posthoc_results_tamhane)
			# print('type posthoc_results_tamhane', type(posthoc_results_tamhane))
			print('posthoc_results_anova\n', posthoc_results_anova)

		else:
			row = [1.0]*len(beh_name_list)
			# print('row\n', row)

			null_mat=[row]*len(beh_name_list)
			# print('null_mat\n', null_mat)

			posthoc_results_anova=pd.DataFrame(null_mat)
			posthoc_results_anova=posthoc_results_anova.set_axis(beh_name_list, axis='columns')
			posthoc_results_anova=posthoc_results_anova.set_axis(beh_name_list, axis='index')

	print('posthoc_results_anova\n', posthoc_results_anova)



	return posthoc_results_anova, p_value_ANOVA




def save_data_for_dFF_matrix(filename='data_for_dFF_matrix_dic.p'):

	data_for_dFF_mat_dic={}

	data_for_dFF_mat_dic.update({'y_list_allBeh':y_list_allBeh})
	data_for_dFF_mat_dic.update({'reordered_ROI_ID_list':reordered_ROI_ID_list})
	data_for_dFF_mat_dic.update({'reordered_mean_dFF_list':reordered_mean_dFF_list})
	data_for_dFF_mat_dic.update({'reordered_mean_dFF_01_list':reordered_mean_dFF_01_list})
	data_for_dFF_mat_dic.update({'reordered_masked_mean_dFF_list':reordered_masked_mean_dFF_list})
	data_for_dFF_mat_dic.update({'reordered_masked_mean_dFF_01_list':reordered_masked_mean_dFF_01_list})
	data_for_dFF_mat_dic.update({'reordered_p_value_list':reordered_p_value_list})
	data_for_dFF_mat_dic.update({'bin_p_value_mask':bin_p_value_mask})
	data_for_dFF_mat_dic.update({'reordered_nonoverlap_list':reordered_nonoverlap_list})
	data_for_dFF_mat_dic.update({'reordered_normality_list':reordered_normality_list})
	data_for_dFF_mat_dic.update({'reordered_std_list':reordered_std_list})


	pickle.dump( data_for_dFF_mat_dic, open( DFF_mat_dir+'/'+filename, "wb" ) )



	return



##main##

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_public_Dir
workstation_dir=general_utils.workstation_dir



experiments_group_per_fly=general_utils.group_expList_per_fly(experiments)
print('experiments_group_per_fly', experiments_group_per_fly)







ROI_id_list=[] #[Gal4-neuron (1 x n)]
mean_dFF_list=[]
mean_dFF_01_list=[]
mean_dFF_norm_list=[]
mean_dFF_log_list=[]
p_value_list=[]
nonoverlap_list=[]
bsl_mean_eachFly_list=[]
bsl_mean_01_eachFly_list=[]

normality_list=[]
std_list=[]

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


manual_ROI_order_csv=pd.read_csv(NAS_AN_Proj_Dir+'scripts_for_public/utils/row_order_manual.csv')
manual_ROI_order= manual_ROI_order_csv['x'].tolist()
# print('manual_ROI_order\n', manual_ROI_order)
# print('type manual_ROI_order', type(manual_ROI_order))




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

	print('\n Find the max DFF per fly ... \n')

	GC_fly_preSum=[]
	for date, genotype, fly, recrd_num in exp_lists_per_fly:
		Gal4=genotype.split('-')[0]
		dataDir = NAS_AN_Proj_Dir +'03_general_2P_exp/'+Gal4 +'/2P/' + date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num + '/'
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


		dataDir = NAS_AN_Proj_Dir +'03_general_2P_exp/'+ Gal4 +'/2P/' + date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num + '/'
		pathForDic = dataDir+'/output/'

		print('dataDir', dataDir)



		Beh_Jpos_GC_DicData=general_utils.open_Beh_Jpos_GC_DicData(pathForDic, 'SyncDic_7CamBeh_BW_20210619_GC-RES.p')

		# for item, value in Beh_Jpos_GC_DicData['Etho_Idx_Dic'].items():
		# 	print(item)



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


		GC_gapfree=[]

		# AP_gapfree_fly.extend(velForw_mm[10000:])




	maxGC=np.nanmax(GC_gapfree_fly)
	minGC=np.nanmin(GC_gapfree_fly)

	# maxGC=sorted(GC_gapfree_fly)[int(len(GC_gapfree_fly)*0.99)]
	# minGC=sorted(GC_gapfree_fly)[int(len(GC_gapfree_fly)*0.01)]

	GC_lim=[minGC, maxGC]
	GC_lim=[minGC, 100]

	# maxAP=np.nanmax(AP_gapfree_fly)
	# minAP=np.nanmin(AP_gapfree_fly)
	# AP_lim=[minAP, maxAP]



	print('shape GC_all_fly_perROI', np.shape(GC_all_fly_perROI))
	print('shape GCnorm01_all_fly_perROI', np.shape(GCnorm01_all_fly_perROI))
	print('shape GC_gapfree_fly', np.shape(GC_gapfree_fly))

	



	##Handling the statistics comapring behavioral dFF vs baseline dFF
	for ROI_i, evts in enumerate(F_Walk_GCevt_fly):

		print('ROI_i', ROI_i)

		

		p_value_fold=[[] for i in range(11)] # 11 types of behavior in total
		# print('p_value_fold', p_value_fold)

		stats_posthoc_fold=6
		for fold in range(0,stats_posthoc_fold):

			beh_name_list=[
			'FW',
			'BW',
			'Push',
			'Rest',
			'EG',
			'AG',
			'FLG',
			'AbdG',
			'HLG',
			'PE',
			'CO2',
			# 'FG',
			# 'HG',
			]
			# print('len beh_name_list', len(beh_name_list))


			Beh_Evts_set_perROI=[
			F_Walk_GCevt_fly[ROI_i],
			B_Walk_GCevt_fly[ROI_i],
			Push_GCevt_fly[ROI_i],
			Rest_GCevt_fly[ROI_i],
			E_groom_GCevt_fly[ROI_i],
			A_groom_GCevt_fly[ROI_i],
			FL_groom_GCevt_fly[ROI_i],
			Abd_groom_GCevt_fly[ROI_i],
			HL_groom_GCevt_fly[ROI_i],
			PER_GCevt_fly[ROI_i],
			CO2puff_GCevt_fly[ROI_i],
			# F_groom_GCevt_fly[ROI_i],
			# H_groom_GCevt_fly[ROI_i],
			]

			# print('shape Beh_Evts_set_perROI', np.shape(Beh_Evts_set_perROI[0][0]))

			Beh_Norm01Evts_set_perROI=[
			F_Walk_GCevtNorm01_fly[ROI_i],
			B_Walk_GCevtNorm01_fly[ROI_i],
			Push_GCevtNorm01_fly[ROI_i],
			Rest_GCevtNorm01_fly[ROI_i],
			E_groom_GCevtNorm01_fly[ROI_i],
			A_groom_GCevtNorm01_fly[ROI_i],
			FL_groom_GCevtNorm01_fly[ROI_i],
			Abd_groom_GCevtNorm01_fly[ROI_i],
			HL_groom_GCevtNorm01_fly[ROI_i],
			PER_GCevtNorm01_fly[ROI_i],
			CO2puff_GCevtNorm01_fly[ROI_i],
			# F_groom_GCevtNorm01_fly[ROI_i],
			# H_groom_GCevtNorm01_fly[ROI_i],
			]

			# print('PER_GCevtNorm01_fly[0]', PER_GCevtNorm01_fly[0])
			# print('shape PER_GCevtNorm01_fly[0]', np.shape(PER_GCevtNorm01_fly[0]))




			_, bsl_evts, _=math_utils.find_baseline_of_trace01(GC_all_fly_perROI[ROI_i], GC_all_fly_perROI[ROI_i], samplerate=data_freq)
			bsl_datapoints_01, bsl_evts_01, normal=math_utils.find_baseline_of_trace01(GCnorm01_all_fly_perROI[ROI_i], GC_all_fly_perROI[ROI_i], samplerate=data_freq)


			## Handling the raw dFF baseline mean
			bsl_evtmean_list=math_utils.compute_mean_with_diffrerent_row_length(bsl_evts, samplerate=data_freq, cutting_head_s=1)
			bsl_mean_ROI=np.nanmean(bsl_evtmean_list)
			bsl_mean_eachFly_list.append([bsl_mean_ROI])


			cutting_head_s=0.7
			min_evt_num=10

			print('\n----',date, genotype, fly, recrd_num, 'ROI#', ROI_i, 'fold=', fold, '----\n')
			all_beh_meanlist_01_list, all_beh_mean_01, all_behdatapoint_nonoverlap_w_Bsl_01, resample_bsl_evtmean_01_list=prep_eachBehEvts_for_stat(\
				beh_name_list, Beh_Norm01Evts_set_perROI, bsl_evts_01, bsl_datapoints_01, min_evt_num=min_evt_num, bsl_s=bsl_s, cutting_head_s=cutting_head_s, data_freq=data_freq)
			
			
			## ---------------------------------------------------------------------------
			# ## Take thresholding baseline and its mean for statistics
			bsl_evtmean_01_list=resample_bsl_evtmean_01_list
			bsl_mean_01=np.nanmean(bsl_evtmean_01_list)
			bsl_mean_01_eachFly_list.append([bsl_mean_01])	
			# print('shape bsl_evtmean_01_list', np.shape(bsl_evtmean_01_list))
			# print('bsl_mean_01', bsl_mean_01)	

			all_beh_meanlist_01_list.append(bsl_evtmean_01_list)




			beh_name_list.append('Bsl')
			all_beh_meanlist_list=all_beh_meanlist_01_list

			# print('len beh_name_list', len(beh_name_list))
			# print('beh_name_list', beh_name_list)
			print('len all_beh_meanlist_list', len(all_beh_meanlist_list))
			for i, v in enumerate(all_beh_meanlist_list):
				print('len v', len(v))


			##--------------------ANOVA, Tukey posthoc-----------------------------------
			posthoc_results_anova, p_value_ANOVA=anova_w_dataset(all_beh_meanlist_list, beh_name_list)
			p_value_whole=p_value_ANOVA		
			stats_type='ANOVA'
			posthoc_results=posthoc_results_anova
			##-------------------------------------------------------


			print('posthoc_results\n', posthoc_results)
			# print('p value against bsl\n', posthoc_results['Bsl'])

			for i, name in enumerate(beh_name_list):
				if name!='Bsl':
					p_value_fold[i].append(posthoc_results['Bsl'][beh_name_list[i]])
			print('fold=',fold,'p-values:\n',posthoc_results['Bsl'])

		print('p_value_fold', p_value_fold)

		
		
		##reassign the p-value against baseline after voting from boostrapped datapoints
		for i, name in enumerate(beh_name_list):
			if name!='Bsl':
				votes=p_value_fold[i]
				count_p_lessthan_005_posthoc=sum(map(lambda x : x<0.05, votes))
				print('->', count_p_lessthan_005_posthoc, 'out of', len(votes), '<0.05')


				if count_p_lessthan_005_posthoc<=len(votes)*0.5 and not np.isnan(posthoc_results.loc['Bsl',name]):

					print('-->', name, 'is not significantly drifferent from baseline')

					posthoc_results.loc['Bsl',name]=1
					# print('posthoc_results["Bsl"][name]', posthoc_results['Bsl'][name])

				elif count_p_lessthan_005_posthoc>len(votes)*0.5 and not np.isnan(posthoc_results.loc['Bsl',name]):
					print('-->', name, 'is significantly drifferent from baseline')
					# print('posthoc_results["Bsl"][name]', posthoc_results['Bsl'][name])
					p_value_fold=np.asarray(p_value_fold)
					print('p_value_fold', p_value_fold)
					if np.median(p_value_fold[p_value_fold<0.05])<=0.001:
						assign_p=0.000999
					else:
						assign_p=np.median(p_value_fold[p_value_fold<0.05])
					posthoc_results.loc['Bsl',name]=np.median(assign_p)

				else:
					print('-->', name, 'p-value is', posthoc_results.loc['Bsl',name])

		# print('type posthoc_results\n', type(posthoc_results))
		print('after re-assign based on the vote of p-value < 0.05. posthoc_results\n', posthoc_results)


		all_beh_mean=[
		np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(F_Walk_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(B_Walk_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(Push_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(Rest_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(E_groom_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(A_groom_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(FL_groom_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(Abd_groom_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(HL_groom_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(PER_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(CO2puff_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		# np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(F_groom_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		# np.nanmean(math_utils.compute_mean_with_diffrerent_row_length(H_groom_GCevt_fly[ROI_i], samplerate=data_freq, cutting_head_s=1))-bsl_mean_ROI,
		]

		dFF_list_ROI=all_beh_mean
		dFF_01_list_ROI=all_beh_mean_01

		# dFF_list_ROI=[mean_F_Walk_evt, mean_B_Walk_evt, mean_Rest_evt, mean_E_groom_evt, mean_A_groom_evt, mean_FL_groom_evt, mean_HL_groom_evt, mean_Abd_groom_evt, mean_Push_evt, mean_PER_evt, mean_CO2puff_evt]
		#dFF_norm_list_ROI=[mean_norm_F_Walk_evt, mean_norm_B_Walk_evt, mean_norm_Rest_evt, mean_norm_E_groom_evt, mean_norm_A_groom_evt, mean_norm_FL_groom_evt, mean_norm_HL_groom_evt, mean_norm_Abd_groom_evt, mean_norm_Push_evt, mean_norm_PER_evt, mean_norm_CO2puff_evt]


		p_value_list_ROI=[]
		for i, name in enumerate(beh_name_list):
			if name!='Bsl':
				p_value_list_ROI.append(posthoc_results.loc['Bsl',name])

		

		# p_value_list_ROI =[
		# posthoc_results['Bsl']['FW'], 
		# posthoc_results['Bsl']['BW'], 
		# posthoc_results['Bsl']['Push'], 
		# posthoc_results['Bsl']['Rest'], 
		# posthoc_results['Bsl']['EG'], 
		# posthoc_results['Bsl']['AG'], 
		# posthoc_results['Bsl']['FLG'], 
		# posthoc_results['Bsl']['AbdG'], 
		# posthoc_results['Bsl']['HLG'], 
		# posthoc_results['Bsl']['PE'], 
		# posthoc_results['Bsl']['CO2']
		# ]
		print('p_value_list_ROI', p_value_list_ROI)




		mean_dFF_list.append(dFF_list_ROI)
		mean_dFF_01_list.append(dFF_01_list_ROI)
		p_value_list.append(p_value_list_ROI)
		nonoverlap_list.append(all_behdatapoint_nonoverlap_w_Bsl_01)
		#mean_dFF_norm_list.append(dFF_norm_list_ROI)

		normality_list.append(normal)
		std_list.append(np.std(general_utils.flatten_list(GC_all_fly_perROI[ROI_i])))


		F_walk_evtmean_list=all_beh_meanlist_01_list[0]
		B_walk_evtmean_list=all_beh_meanlist_01_list[1]
		Push_evtmean_list=all_beh_meanlist_01_list[2]
		Rest_evtmean_list=all_beh_meanlist_01_list[3]
		E_groom_evtmean_list=all_beh_meanlist_01_list[4]
		A_groom_evtmean_list=all_beh_meanlist_01_list[5]
		FL_groom_evtmean_list=all_beh_meanlist_01_list[6]
		Abd_groom_evtmean_list=all_beh_meanlist_01_list[7]
		HL_groom_evtmean_list=all_beh_meanlist_01_list[8]
		PER_evtmean_list=all_beh_meanlist_01_list[9]
		CO2puff_evtmean_list=all_beh_meanlist_01_list[10]


		
		dFF_list_ROI=[]
		dFF_norm_list_ROI=[]
		dFF_log_list_ROI=[]
		p_value_list_ROI=[]






reordered_ROI_ID_list, reordered_mean_dFF_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, mean_dFF_list, manual_ROI_order)
reordered_ROI_ID_list, reordered_mean_dFF_01_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, mean_dFF_01_list, manual_ROI_order)
reordered_ROI_ID_list, reordered_p_value_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, p_value_list, manual_ROI_order)
reordered_ROI_ID_list, reordered_nonoverlap_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, nonoverlap_list, manual_ROI_order)
reordered_ROI_ID_list, reordered_bslmean_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, bsl_mean_eachFly_list, manual_ROI_order)
reordered_ROI_ID_list, reordered_bslmean_01_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, bsl_mean_01_eachFly_list, manual_ROI_order)

reordered_ROI_ID_list, reordered_normality_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, normality_list, manual_ROI_order)
reordered_ROI_ID_list, reordered_std_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, std_list, manual_ROI_order)


reordered_masked_mean_dFF_list, bin_p_value_mask = mask_out_dFF_based_on_p_value(reordered_mean_dFF_list, ref_mat=reordered_p_value_list)
reordered_masked_mean_dFF_01_list, bin_p_value_mask = mask_out_dFF_based_on_p_value(reordered_mean_dFF_01_list, ref_mat=reordered_p_value_list)




y_list_allBeh=[
'F_Walk', 
'B_Walk', 
'Push', 
'Rest', 
'E_groom', 
'A_groom', 
'FL_rub', 
'Abd_groom', 
'HL_rub', 
'PE', 
'CO2puff'
]



DFF_mat_dir=NAS_AN_Proj_Dir + 'output/FigS3-DFF_mat/'
if not os.path.exists(DFF_mat_dir):
	os.makedirs(DFF_mat_dir)

save_data_for_dFF_matrix(filename='data_for_dFF_matrix_dic.p')
# save_data_for_dFF_matrix(filename='data_for_dFF_matrix_dic-BehEpochMean.p')


# plot_utils.plot_matrix(reordered_ROI_ID_list, y_list_allBeh, reordered_mean_dFF_list, savedir=DFF_mat_dir, title='mean_dFF', PlotMethod='other', Gal4_x_list_reformat=True, cmap='BuPu')
# plot_utils.plot_matrix(reordered_ROI_ID_list, y_list_allBeh, reordered_mean_dFF_01_list, savedir=DFF_mat_dir, title='mean_dFF_01', PlotMethod='dFF_01_w_negative', Gal4_x_list_reformat=True, cmap='BuPu')
# plot_utils.plot_matrix(reordered_ROI_ID_list, y_list_allBeh, reordered_masked_mean_dFF_list, savedir=DFF_mat_dir, title='mean_dFF_masked_by_p', PlotMethod='dFF_01_w_negative', Gal4_x_list_reformat=True, cmap='BuPu')
# plot_utils.plot_matrix(reordered_ROI_ID_list, y_list_allBeh, reordered_masked_mean_dFF_01_list, savedir=DFF_mat_dir, title='mean_dFF_01_masked_by_p', PlotMethod='dFF_01_w_negative', Gal4_x_list_reformat=True, cmap='BuPu')
# plot_utils.plot_matrix(reordered_ROI_ID_list, y_list_allBeh, reordered_p_value_list, savedir=DFF_mat_dir, title='p_value', PlotMethod='p_value', Gal4_x_list_reformat=True, cmap='Greens')
# plot_utils.plot_matrix(reordered_ROI_ID_list, y_list_allBeh, bin_p_value_mask, savedir=DFF_mat_dir, title='p_value_bin_mask', PlotMethod='other', cmap='gray', hatch='/', Gal4_x_list_reformat=True, hatchcolor='lightgrey')
# plot_utils.plot_matrix(reordered_ROI_ID_list, y_list_allBeh, reordered_nonoverlap_list, savedir=DFF_mat_dir, title='Non-overlap_against_bsl', PlotMethod='other', Gal4_x_list_reformat=True, cmap='Greens')

# plot_utils.plot_matrix(reordered_ROI_ID_list, ['STD'], reordered_std_list, savedir=DFF_mat_dir, title='std', PlotMethod='other', Gal4_x_list_reformat=True, cmap='gist_gray')
# plot_utils.plot_matrix(reordered_ROI_ID_list, ['Normality'], reordered_normality_list, savedir=DFF_mat_dir, title='normality', PlotMethod='other', Gal4_x_list_reformat=True, cmap='gist_gray')

# plot_utils.plot_overlay_matrix(reordered_ROI_ID_list, y_list_allBeh, reordered_masked_mean_dFF_list, bin_p_value_mask, savedir=DFF_mat_dir, title='mean_dFF_masked_by_p_w_mask', hatch=False, colorbar_bas='BuPu')
# plot_utils.plot_overlay_matrix(reordered_ROI_ID_list, y_list_allBeh, reordered_masked_mean_dFF_01_list, bin_p_value_mask, savedir=DFF_mat_dir, title='mean_dFF_01_masked_by_p_w_mask', hatch=False, colorbar_bas='BuPu')


