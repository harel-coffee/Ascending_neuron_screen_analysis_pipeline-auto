import sys
import pickle
import pandas as pd
import numpy as np



import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
# import utils.plot_setting as plot_setting
# import utils.math_utils as math_utils
# import utils.sync_utils as sync_utils






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



def make_mask_based_on_p_value_and_normality(p_value_mat, normality_arr):

	mask_list = [y[:] for y in p_value_mat]


	if len(p_value_mat)==0:
		print('base_mat is not given. The refrent matrix for masking is obligatory...')
		sys.exit(0)



	# for roi_i, normality_per_roi in enumerate(normality_arr):
	# 	if normality_per_roi==True:
	# 		for beh_i, mask_val in enumerate(p_value_mat[roi_i]):
	# 			mask_list[roi_i][beh_i]=1
	# 	else:
	# 		for beh_i, mask_val in enumerate(p_value_mat[roi_i]):
	# 			mask_list[roi_i][beh_i]=np.nan


	for roi_i, pvalues_per_roi in enumerate(p_value_mat):
		for beh_i, p_value in enumerate(pvalues_per_roi):
			if p_value>0.05 or np.isnan(p_value) or normality_arr[roi_i]==True:
				mask_list[roi_i][beh_i]=1
			else:
				mask_list[roi_i][beh_i]=np.nan




	return mask_list



##--------main----------##

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_public_Dir
workstation_dir=general_utils.workstation_dir



DFF_mat_dir=NAS_AN_Proj_Dir + '/output/FigS3-DFF_mat/plots/'

dFF_for_matPlot_DicData=general_utils.open_Beh_Jpos_GC_DicData(DFF_mat_dir, 'data_for_dFF_matrix_dic.p')

manual_ROI_order_csv=pd.read_csv(workstation_dir+'from_florian/Ascending_analysis/output/row_order_manual.csv')
manual_ROI_order= manual_ROI_order_csv['x'].tolist()

ROI_ID_list=dFF_for_matPlot_DicData['reordered_ROI_ID_list']
y_list_allBeh=dFF_for_matPlot_DicData['y_list_allBeh']

p_value_list=dFF_for_matPlot_DicData['reordered_p_value_list']
normality_list=dFF_for_matPlot_DicData['reordered_normality_list']
masked_mean_dFF_01_list=dFF_for_matPlot_DicData['reordered_masked_mean_dFF_01_list']



combined_mask=make_mask_based_on_p_value_and_normality(p_value_list, normality_list)

print('shape combined_mask', np.shape(combined_mask))






reordered_ROI_ID_list, reordered_masked_mean_dFF_01_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_ID_list, masked_mean_dFF_01_list, manual_ROI_order)
reordered_ROI_ID_list, reordered_combined_mask=sorting_roiID_correspondingMat_based_on_an_order(ROI_ID_list, combined_mask, manual_ROI_order)


# plot_utils.plot_matrix(reordered_ROI_ID_list, y_list_allBeh, reordered_masked_mean_dFF_01_list, savedir=DFF_mat_dir, title='mean_dFF_01_masked_by_p', PlotMethod='dFF_01_w_negative', Gal4_x_list_reformat=True, cmap='BuPu')


plot_utils.plot_overlay_matrix(reordered_ROI_ID_list, y_list_allBeh, reordered_masked_mean_dFF_01_list, reordered_combined_mask, hatch=False, colorbar_bas='BuPu', savedir=DFF_mat_dir, title='mean_dFF01_masked_by_pvalue')







