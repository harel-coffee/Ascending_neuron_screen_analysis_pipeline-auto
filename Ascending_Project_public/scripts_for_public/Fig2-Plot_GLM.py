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



NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_Dir





manual_ROI_order_csv=pd.read_csv(NAS_AN_Proj_Dir+'scripts_for_public/utils/row_order_manual.csv')
manual_ROI_order= manual_ROI_order_csv['x'].tolist()





florian_glm_dir= NAS_AN_Proj_Dir+'output/Fig2_S4-GLM_jangles_legs_beh_DFF/plots/' 
if not os.path.exists(florian_glm_dir):
	os.makedirs(florian_glm_dir)


glm_beh_dir=florian_glm_dir+'glm_beh/'
if not os.path.exists(glm_beh_dir):
	os.makedirs(glm_beh_dir)
lm_df=pd.read_csv(NAS_AN_Proj_Dir+'output/Fig2_S4-GLM_jangles_legs_beh_DFF/overview_beh/lm_results.csv')


glm_legPair_dir=florian_glm_dir+'glm_leg_pair/'
if not os.path.exists(glm_legPair_dir):
	os.makedirs(glm_legPair_dir)
lm_legPair_df=pd.read_csv(NAS_AN_Proj_Dir+'output/Fig2_S4-GLM_jangles_legs_beh_DFF/overview_leg_pairs/lm_results_angles_leg_pairs.csv')


glm_leg_dir=florian_glm_dir+'glm_leg/'
if not os.path.exists(glm_leg_dir):
	os.makedirs(glm_leg_dir)
lm_leg_df=pd.read_csv(NAS_AN_Proj_Dir+'output/Fig2_S4-GLM_jangles_legs_beh_DFF/overview_legs/lm_results_angles_legs.csv')


glm_janlges_dir=florian_glm_dir+'glm_jangle/'
if not os.path.exists(glm_janlges_dir):
	os.makedirs(glm_janlges_dir)
lm_jangles_df=pd.read_csv(NAS_AN_Proj_Dir+'output/Fig2_S4-GLM_jangles_legs_beh_DFF/overview_angles/lm_results_angles.csv')



##---------Process df of beh, leg pairs, leg, jangles---------##

experiments=list_twoP_exp.TwoP_recordings_sparseLine_list
experiments_group_per_fly=general_utils.group_expList_per_fly(experiments)
# print('experiments_group_per_fly', experiments_group_per_fly)


whole_set_df=[
(lm_df, 'beh'),
(lm_legPair_df, 'legPair'),
(lm_leg_df, 'leg'),
(lm_jangles_df, 'jangle'),
]



Beh_order=[
'forward_walking',
'backward_walking',
'pushing',
'rest',
'eye_grooming',
'antennal_grooming',
'foreleg_grooming',
'abdominal_grooming',
'hindleg_grooming',
'PER_event',
'CO2',
]

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

univsl_max_uniqR2=False
univsl_min_uniqR2=False
univsl_max_allR2=False
univsl_min_allR2=False





for df, df_tag in whole_set_df:

	


	new_df=df.groupby(['Genotype', 'ROI', 'Regressor']).mean()
	p_value_df=df.groupby(['Genotype', 'ROI', 'Regressor']).max()

	new_df["Unique_explained_variance"]=new_df["r.squared"] - new_df["r.sq.w.o.explained.variance"]

	new_df["All_explained_variance"]=new_df["r.sq.only.explained.variance"]



	if df_tag=='beh':
		variables_order=Beh_order
		y_list_variables=y_list_allBeh
		glm_dir=glm_beh_dir

	elif df_tag=='legPair':
		variables_order=list_behavior.leg_pairs_order
		y_list_variables=list_behavior.leg_pairs_order
		glm_dir=glm_legPair_dir

	elif df_tag=='leg':
		variables_order=list_behavior.legs_order
		y_list_variables=list_behavior.legs_order
		glm_dir=glm_leg_dir

	elif df_tag=='jangle':

		variables_order=list_behavior.jangles_order_Florian
		y_list_variables=list_behavior.jangles_order_NeuroMechFly
		glm_dir=glm_janlges_dir



	ROI_id_list=[]
	unique_explained_variance_list=[]
	all_explained_variacne_list=[]
	p_value_list=[]


	
	for exp_lists_per_fly in experiments_group_per_fly:
		# print('Processing per fly for ... ', exp_lists_per_fly )

		for date, genotype, fly, recrd_num in exp_lists_per_fly:

			Gal4=genotype.split('-')[0]

			ROI_len=len(list(set(df[(df["Genotype"]==Gal4)]["ROI"].tolist())))

			temp_unique_r_sq_list=[]
			temp_all_r_sq_list=[]
			for roi_ID in range(ROI_len):
				ROI_id_list.append(Gal4+'-ROI#'+str(roi_ID))

				for i, beh in enumerate(variables_order):
					temp_unique_r_sq_list.append(new_df["Unique_explained_variance"][Gal4][roi_ID][beh])
					temp_all_r_sq_list.append(new_df["All_explained_variance"][Gal4][roi_ID][beh])
				# print('shape temp_unique_r_sq_list', np.shape(temp_unique_r_sq_list))
				unique_explained_variance_list.append(temp_unique_r_sq_list)
				all_explained_variacne_list.append(temp_all_r_sq_list)
				p_value_list.append(max(p_value_df["F.p.value"][Gal4][roi_ID].tolist()))

				temp_unique_r_sq_list=[]
				temp_all_r_sq_list=[]


			## all Gal4 just need one time to added the mean value, not correct go across all recordings in the list. So break!!!
			break

	print('len ROI_id_list', len(ROI_id_list))
	print('shape ROI_id_list', np.shape(ROI_id_list))
	print('shape unique_explained_variance_list', np.shape(unique_explained_variance_list))

	star_list=convert_p_value_to_stars(p_value_list)
	print('len star_list', len(star_list))




	reordered_ROI_ID_list, reordered_uniq_r_sq_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, unique_explained_variance_list, manual_ROI_order)
	reordered_ROI_ID_list, reordered_all_r_sq_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, all_explained_variacne_list, manual_ROI_order)
	reordered_ROI_ID_list, reordered_star_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, star_list, manual_ROI_order)

	reordered_star_list=general_utils.flatten_list(reordered_star_list)


	if df_tag=='beh':
		print('setting universal max. and min.')
		univsl_max_uniqR2=np.nanmax(reordered_uniq_r_sq_list)
		univsl_min_uniqR2=np.nanmin(reordered_uniq_r_sq_list)
		univsl_max_allR2=np.nanmax(reordered_all_r_sq_list)
		univsl_min_allR2=np.nanmin(reordered_all_r_sq_list)	

	print('univsl_max_uniqR2, univsl_min_uniqR2', univsl_max_uniqR2, univsl_min_uniqR2)
	print('univsl_max_allR2, univsl_min_allR2', univsl_max_allR2, univsl_min_allR2)

	plot_utils.plot_matrix(reordered_ROI_ID_list, y_list_variables, reordered_uniq_r_sq_list, set_max=univsl_max_uniqR2, set_min=univsl_min_uniqR2, second_x_list=reordered_star_list, savedir=glm_dir, title='unqiue_explained_variance', PlotMethod='other', cmap='BuPu')







