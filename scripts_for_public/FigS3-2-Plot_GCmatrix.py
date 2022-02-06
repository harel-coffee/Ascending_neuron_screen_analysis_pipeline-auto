import sys
import pickle
import pandas as pd
import numpy as np
import csv


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


def replace_p_value_with_starisk(p_value_list):

	new_p_val_list=[]

	for n, neuron_p_val in enumerate(p_value_list):
		new_p_val_list.append([])
		for b, p_val in enumerate(neuron_p_val):

			if p_val<=0.001:
				p_star='***'
			elif p_val<=0.01:
				p_star='**'
			elif p_val<=0.05:
				p_star='*'
			elif p_val>0.05:
				p_star='n.s'
			else:
				# p_star=np.nan
				p_star='< 10 events'

			new_p_val_list[n].append(p_star)


	return new_p_val_list


def output_p_value_csv(reordered_ROI_ID_list, y_list_allBeh, p_value_list, savedir, title):


	print('reordered_ROI_ID_list', reordered_ROI_ID_list)
	print('y_list_allBeh', y_list_allBeh, np.shape(y_list_allBeh))
	print('p_value_list', p_value_list, np.shape(p_value_list))


	p_value_list_T=np.transpose(p_value_list)
	print('p_value_list_T', p_value_list_T, np.shape(p_value_list_T))

	header = ['regressor']
	header.extend(reordered_ROI_ID_list)

	data=[]
	for i, beh in enumerate(y_list_allBeh):
		print(i)
		data.append([])
		data[i].append(beh)
		data[i].extend(p_value_list_T[i])


	with open(savedir+title+'.csv', 'w', encoding='UTF8') as f:
		writer = csv.writer(f)
		writer.writerow(header)
		writer.writerows(data)


	return



##--------main----------##

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_public_Dir
workstation_dir=general_utils.workstation_dir




DFF_mat_dir=NAS_AN_Proj_Dir + 'output/FigS3-DFF_mat/'

dFF_for_matPlot_DicData=general_utils.open_Beh_Jpos_GC_DicData(DFF_mat_dir, 'data_for_dFF_matrix_dic.p')

manual_ROI_order_csv=pd.read_csv(NAS_AN_Proj_Dir+'scripts_for_public/utils/row_order_manual.csv')
manual_ROI_order= manual_ROI_order_csv['x'].tolist()

ROI_ID_list=dFF_for_matPlot_DicData['reordered_ROI_ID_list']
y_list_allBeh=dFF_for_matPlot_DicData['y_list_allBeh']

p_value_list=dFF_for_matPlot_DicData['reordered_p_value_list']
normality_list=dFF_for_matPlot_DicData['reordered_normality_list']
masked_mean_dFF_01_list=dFF_for_matPlot_DicData['reordered_masked_mean_dFF_01_list']



combined_mask=make_mask_based_on_p_value_and_normality(p_value_list, normality_list)

print('shape combined_mask', np.shape(combined_mask))




DFF_mat_plot_dir=NAS_AN_Proj_Dir + '/output/FigS3-DFF_mat/plots/'

reordered_ROI_ID_list, reordered_masked_mean_dFF_01_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_ID_list, masked_mean_dFF_01_list, manual_ROI_order)
reordered_ROI_ID_list, reordered_combined_mask=sorting_roiID_correspondingMat_based_on_an_order(ROI_ID_list, combined_mask, manual_ROI_order)




plot_utils.plot_overlay_matrix(reordered_ROI_ID_list, y_list_allBeh, reordered_masked_mean_dFF_01_list, reordered_combined_mask, hatch=False, colorbar_bas='BuPu', savedir=DFF_mat_plot_dir, title='mean_dFF01_masked_by_pvalue')

star_p_value_list=replace_p_value_with_starisk(p_value_list)


output_p_value_csv(reordered_ROI_ID_list, y_list_allBeh, star_p_value_list, savedir=DFF_mat_plot_dir, title='p_value')

# plot_utils.plot_matrix(reordered_ROI_ID_list, y_list_allBeh, p_value_list, savedir=DFF_mat_plot_dir, title='p_value', PlotMethod='p_value', Gal4_x_list_reformat=True, cmap='Greens')
# plot_utils.plot_matrix(reordered_ROI_ID_list, y_list_allBeh, bin_p_value_mask, savedir=DFF_mat_plot_dir, title='p_value_bin_mask', PlotMethod='other', cmap='gray', hatch='/', Gal4_x_list_reformat=True, hatchcolor='lightgrey')




