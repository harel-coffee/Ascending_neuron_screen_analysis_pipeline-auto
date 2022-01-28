import sys
import pandas as pd
import numpy as np
import os
from itertools import groupby


import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.plot_setting as plot_setting
import utils.math_utils as math_utils
import utils.sync_utils as sync_utils
import utils.list_twoP_exp as list_twoP_exp
import utils.list_behavior as list_behavior




def sorting_roiID_correspondingMat_based_on_an_order(roi_id_list, corrspd_list, base_of_order_list, rename_ID_into_ROI=True):



	# if len(roi_id_list)!=len(base_of_order_list):
	# 	print('ROI numbers does not match. Reordering ROI IDs cannot be done ...')
	# 	sys.exit(0)

	if rename_ID_into_ROI==True:
		ressembled_name_for_baseOrder_list=[]
		for i, id_name in enumerate(base_of_order_list):
			ressembled_name=id_name.split(' ')[0]+'-ROI#'+id_name.split(' ')[1]
			ressembled_name_for_baseOrder_list.append(ressembled_name)
	else:
		ressembled_name_for_baseOrder_list=base_of_order_list

	# print(ressembled_name_for_baseOrder_list)


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


def make_IDorder_for_turn(ori_genotpye_roi_list, root_roi_order_list):

	# print('ori_genotpye_roi_list', ori_genotpye_roi_list)
	# print('root_roi_order_list', root_roi_order_list)


	group_ori_genotype_roi_list=[list(i) for j, i in groupby(ori_genotpye_roi_list, lambda x: x[:-4])] 
	# print('group_ori_genotype_roi_list', group_ori_genotype_roi_list)

	root_gal4_list=[i[:-2] for i in root_roi_order_list]
	# print('root_gal4_list', root_gal4_list)

	new_genotype_roi_order_list=[]
	idx_list_in_root=[]
	for i, group_ori_genotype_roi in enumerate(group_ori_genotype_roi_list):
		# print('group_ori_genotype_roi', group_ori_genotype_roi)
		ref_for_sort=group_ori_genotype_roi[0][:-4]+' 0'
		# print(ref_for_sort)
		idx_ref_in_root=root_roi_order_list.index(ref_for_sort)
		# print(idx_ref_in_root)
		idx_list_in_root.append(idx_ref_in_root)



	zipped_id_lists = zip(idx_list_in_root, group_ori_genotype_roi_list)
	sorted_zipped_id_lists = sorted(zipped_id_lists)
	sorted_new_roi_id_list = [element for _, element in sorted_zipped_id_lists]

	sorted_new_roi_id_list=general_utils.flatten_list(sorted_new_roi_id_list)

	# print('sorted_new_roi_id_list', sorted_new_roi_id_list)


	return sorted_new_roi_id_list


def make_new_pair_ID_list(old_id_list):

	# print('old_id_list', old_id_list)

	new_id_list=[]
	for i, roi_pair_id in enumerate(old_id_list):
		pair_roi=roi_pair_id.split(' ')[0]+' '+roi_pair_id.split(' ')[1]+'\n'+'-'+'\n'+roi_pair_id.split(' ')[2]
		# print('pair_roi', pair_roi)
		new_id_list.append(pair_roi)

	return new_id_list


def convert_p_value_to_stars(p_value_list):

	star_list=[]
	for i, p in enumerate(p_value_list):

		if p>=0.05:
			star_list.append(['n.s.'])
		elif p>=0.01:
			star_list.append(['*'])
		elif p>=0.001:
			star_list.append(['**'])
		elif p<0.001:
			star_list.append(['***'])

	return star_list



##-----------------------main--------------------------------##


NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_Dir
workstation_dir=general_utils.workstation_dir




manual_ROI_order_csv=pd.read_csv(NAS_AN_Proj_Dir+'scripts_for_public/utils/row_order_manual.csv')
manual_ROI_order= manual_ROI_order_csv['x'].tolist()



turn_df=pd.read_csv(NAS_AN_Proj_Dir+'output/Fig7a_7c-turning/all_results_turning.csv')


florian_glm_dir= NAS_AN_Proj_Dir+'output/Fig7a_7c-turning/plots/' 
if not os.path.exists(florian_glm_dir):
	os.makedirs(florian_glm_dir)




##---------------Process turning df---------------##

new_turn_df=turn_df.groupby(['Genotype_ROI','Regressor']).mean()
new_p_value_turn_df=turn_df.groupby(['Genotype_ROI','Regressor']).max()
print('new_turn_df\n', new_turn_df)
print('new_turn_df["Explained_variance"]["SS34574 0 1"][Roll"]\n', new_turn_df["Explained_variance"]["SS34574 0 1"]['Roll'])
print('new_turn_df["Explained_variance"]["SS34574 0 1"][Yaw"]\n', new_turn_df["Explained_variance"]["SS34574 0 1"]['Yaw'])
print('new_turn_df["p.value"]["SS34574 0 1"][Roll"]\n', new_p_value_turn_df["p.value"]["SS34574 0 1"]['Roll'])
print('new_turn_df["p.value"]["SS34574 0 1"][Yaw"]\n', new_p_value_turn_df["p.value"]["SS34574 0 1"]['Yaw'])




turn_id_list=[]
turn_roll_expalined_variance=[]
turn_yaw_expalined_variance=[]
turn_roll_yaw_expalined_variance=[]
turn_roll_p_value=[]
turn_yaw_p_value=[]


genotypes_roi_turn_list=turn_df["Genotype_ROI"].tolist()
genotypes_roi_turn_list= list(dict.fromkeys(genotypes_roi_turn_list))



for Genotype_ROI in genotypes_roi_turn_list:



	turn_id_list.append(Genotype_ROI)
	turn_roll_expalined_variance.append(new_turn_df["Explained_variance"][Genotype_ROI]["Roll"])
	turn_yaw_expalined_variance.append(new_turn_df["Explained_variance"][Genotype_ROI]["Yaw"])
	turn_roll_yaw_expalined_variance.append([new_turn_df["Explained_variance"][Genotype_ROI]["Roll"], new_turn_df["Explained_variance"][Genotype_ROI]["Yaw"]])
	turn_roll_p_value.append(new_p_value_turn_df["p.value"][Genotype_ROI]["Roll"])
	turn_yaw_p_value.append(new_p_value_turn_df["p.value"][Genotype_ROI]["Yaw"])


print('turn_id_list', turn_id_list)

sorted_turn_roi_id_list=make_IDorder_for_turn(turn_id_list, manual_ROI_order)


reordered_turn_ROI_ID_list, reordered_roll_uniq_r_sq_list=sorting_roiID_correspondingMat_based_on_an_order(turn_id_list, turn_roll_expalined_variance, sorted_turn_roi_id_list, rename_ID_into_ROI=False)
reordered_turn_ROI_ID_list, reordered_yaw_uniq_r_sq_list=sorting_roiID_correspondingMat_based_on_an_order(turn_id_list, turn_yaw_expalined_variance, sorted_turn_roi_id_list, rename_ID_into_ROI=False)
reordered_turn_ROI_ID_list, reordered_roll_yaw_uniq_r_sq_list=sorting_roiID_correspondingMat_based_on_an_order(turn_id_list, turn_roll_yaw_expalined_variance, sorted_turn_roi_id_list, rename_ID_into_ROI=False)

reordered_turn_ROI_ID_list, reordered_roll_p_value_list=sorting_roiID_correspondingMat_based_on_an_order(turn_id_list, turn_roll_p_value, sorted_turn_roi_id_list, rename_ID_into_ROI=False)
reordered_turn_ROI_ID_list, reordered_yaw_p_value_list=sorting_roiID_correspondingMat_based_on_an_order(turn_id_list, turn_yaw_p_value, sorted_turn_roi_id_list, rename_ID_into_ROI=False)



star_roll_list=general_utils.flatten_list(convert_p_value_to_stars(reordered_roll_p_value_list))
star_yaw_list=general_utils.flatten_list(convert_p_value_to_stars(reordered_yaw_p_value_list))
print('len star_roll_list', len(star_roll_list))


new_turn_ROI_ID_list=make_new_pair_ID_list(reordered_turn_ROI_ID_list)
print('new_turn_ROI_ID_list', new_turn_ROI_ID_list)


turn_output_dir=florian_glm_dir
# plot_utils.plot_matrix(new_turn_ROI_ID_list, ['Roll'], reordered_roll_uniq_r_sq_list, second_x_list=star_roll_list, roi_seperation_marker=' ', savedir=turn_output_dir, title='roll_unique_explained_variance', PlotMethod='other', cmap='BuPu')
# plot_utils.plot_matrix(new_turn_ROI_ID_list, ['Yaw'], reordered_yaw_uniq_r_sq_list, second_x_list=star_yaw_list, roi_seperation_marker=' ', savedir=turn_output_dir, title='yaw_unique_explained_variance', PlotMethod='other', cmap='BuPu')
plot_utils.plot_matrix(new_turn_ROI_ID_list, ['ROll', 'Yaw'], reordered_roll_yaw_uniq_r_sq_list, second_x_list=star_yaw_list, Gal4_x_list_reformat=True, roi_seperation_marker=' ', savedir=turn_output_dir, title='roll_yaw_unique_explained_variance', PlotMethod='other', cmap='BuPu')







