import sys
import pickle
import pandas as pd
import os
import numpy as np



import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.plot_setting as plot_setting
import utils.math_utils as math_utils
import utils.sync_utils as sync_utils

import utils.list_twoP_exp as list_twoP_exp
import utils.list_morpho as list_morpho




experiments=list_twoP_exp.TwoP_recordings_sparseLine_list









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




def main_plot(ROI_id_list, manual_ROI_order, interested_area_list, innerv_df, manual_innerv_df, unidf_innerv_df, colorbar_bas, savedir, filename):

	print('Processing in', filename, '...')

	# innerv_df['area']=innerv_df['area'].replace(0, np.nan)
	manual_innerv_df['area']=manual_innerv_df['area'].replace(0, np.nan)
	unidf_innerv_df['area']=unidf_innerv_df['area'].replace(0, np.nan)



	# print('manual_innerv_df\n', manual_innerv_df)


	innervation_list=[]
	innervation_manual_list=[]
	innervation_unIdf_list=[]

	for i, neuron_id in enumerate(ROI_id_list):
		# print('neuron_id', neuron_id)
		Gal4=neuron_id.split('-')[0]
		# print('Gal4', Gal4)
		ROI=neuron_id.split('-')[1][-1]
		# print('ROI', ROI)
		# print('type ROI', type(ROI))

		temp_real_innervation=[]
		temp_manual_innervation=[]
		temp_inIdf_innervation=[]
		for i, area in enumerate(interested_area_list):

			# print('area', area)

			temp_real_innervation.append(innerv_df[(innerv_df["Genotype"]==Gal4) & (innerv_df["ROI"]==int(ROI)) & (innerv_df["Regressor"]==area)]["area"].tolist()[0])
			temp_manual_innervation.append(manual_innerv_df[(manual_innerv_df["Genotype"]==Gal4) & (manual_innerv_df["ROI"]==int(ROI)) & (manual_innerv_df["Regressor"]==area)]["area"].tolist()[0])
			temp_inIdf_innervation.append(unidf_innerv_df[(unidf_innerv_df["Genotype"]==Gal4) & (unidf_innerv_df["ROI"]==int(ROI)) & (unidf_innerv_df["Regressor"]==area)]["area"].tolist()[0])


		innervation_list.append(temp_real_innervation)
		innervation_manual_list.append(temp_manual_innervation)
		innervation_unIdf_list.append(temp_inIdf_innervation)



		reordered_ROI_ID_list, reordered_innervation_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, innervation_list, manual_ROI_order)
		reordered_ROI_ID_list, reordered_innervation_manual_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, innervation_manual_list, manual_ROI_order)
		reordered_ROI_ID_list, reordered_innervation_unIdf_list=sorting_roiID_correspondingMat_based_on_an_order(ROI_id_list, innervation_unIdf_list, manual_ROI_order)


	plot_utils.plot_overlay_innerv_matrix(reordered_ROI_ID_list, interested_area_list, reordered_innervation_list, reordered_innervation_manual_list, reordered_innervation_unIdf_list, colorbar_bas='BuPu', savedir=savedir, title=filename)



	return 



##-------main-------##

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_public_Dir



JRC_MCFO_outDir=NAS_AN_Proj_Dir + 'output/Fig3_S4-single_AN_innervation_mat/'

manual_ROI_order_csv=pd.read_csv(NAS_AN_Proj_Dir+'scripts_for_public/utils/row_order_manual.csv')
manual_ROI_order= manual_ROI_order_csv['x'].tolist()

Innervation_brain_distalenurites=general_utils.open_Beh_Jpos_GC_DicData(JRC_MCFO_outDir, 'Innervation_px_count_visualCount_distalenurites.p')
Innervation_vnc=general_utils.open_Beh_Jpos_GC_DicData(JRC_MCFO_outDir, 'Innervation_px_count_visualCount_vnc.p')
Innervation_t1t2t3=general_utils.open_Beh_Jpos_GC_DicData(JRC_MCFO_outDir, 'Innervation_px_count_visualCount_T1T2T3.p')

all_brain_neuropil_list=Innervation_brain_distalenurites['all_Innervated_neuropil_list']
brain_neuropil_list=Innervation_brain_distalenurites['Innervated_neuropil_list']
print('all_brain_neuropil_list', all_brain_neuropil_list)
brain_neuropil_w_Other_list=brain_neuropil_list.tolist()+['Other']
print('brain_neuropil_w_Other_list', brain_neuropil_w_Other_list)
vnc_neuropil_list=Innervation_vnc['Innervated_neuropil_list']
t1t2t3_neuropil_list=Innervation_t1t2t3['Innervated_neuropil_list']

print('vnc_neuropil_list', vnc_neuropil_list)
print('t1t2t3_neuropil_list', t1t2t3_neuropil_list)



all_brain_innervation_df=pd.read_csv(JRC_MCFO_outDir+'all_distal_neurite_for_matrix.csv')
all_brain_innervation_manual_df=pd.read_csv(JRC_MCFO_outDir+'all_distal_neurite_mannual_for_matrix.csv')
all_brain_innervation_unIdf_df=pd.read_csv(JRC_MCFO_outDir+'all_distal_neurite_unIdf_for_matrix.csv')
all_brain_innervation_df['area'] = all_brain_innervation_df['area'].fillna(0)


brain_innervation_df=pd.read_csv(JRC_MCFO_outDir+'Distal_neurite_for_matrix.csv')
brain_innervation_manual_df=pd.read_csv(JRC_MCFO_outDir+'Distal_neurite_mannual_for_matrix.csv')
brain_innervation_unIdf_df=pd.read_csv(JRC_MCFO_outDir+'Distal_neurite_unIdf_for_matrix.csv')
brain_innervation_df['area'] = brain_innervation_df['area'].fillna(0)


vnc_innervation_df=pd.read_csv(JRC_MCFO_outDir+'vnc_neurite_for_matrix.csv')
vnc_innervation_manual_df=pd.read_csv(JRC_MCFO_outDir+'vnc_neurite_mannual_for_matrix.csv')
vnc_innervation_unIdf_df=pd.read_csv(JRC_MCFO_outDir+'vnc_neurite_unIdf_for_matrix.csv')
vnc_innervation_df['area'] = vnc_innervation_df['area'].fillna(0)


t1t2t3_innervation_df=pd.read_csv(JRC_MCFO_outDir+'T1T2T3_neurite_for_matrix.csv')
t1t2t3_innervation_manual_df=pd.read_csv(JRC_MCFO_outDir+'T1T2T3_neurite_mannual_for_matrix.csv')
t1t2t3_innervation_unIdf_df=pd.read_csv(JRC_MCFO_outDir+'T1T2T3_neurite_unIdf_for_matrix.csv')
t1t2t3_innervation_df['area'] = t1t2t3_innervation_df['area'].fillna(0)
print('t1t2t3_innervation_unIdf_df\n', t1t2t3_innervation_unIdf_df)


print(brain_innervation_df[(brain_innervation_df['Genotype']=='SS27485') & (brain_innervation_df['ROI']==0) & (brain_innervation_df['Regressor']=='GNG')])
print(brain_innervation_df[(brain_innervation_df['Genotype']=='SS41806') & (brain_innervation_df['ROI']==0) & (brain_innervation_df['Regressor']=='GNG')])
print(brain_innervation_df[(brain_innervation_df['Genotype']=='SS36131') & (brain_innervation_df['ROI']==0) & (brain_innervation_df['Regressor']=='GNG')])
print(brain_innervation_df[(brain_innervation_df['Genotype']=='SS38592') & (brain_innervation_df['ROI']==0) & (brain_innervation_df['Regressor']=='GNG')])
print(brain_innervation_df[(brain_innervation_df['Genotype']=='SS38631') & (brain_innervation_df['ROI']==0) & (brain_innervation_df['Regressor']=='GNG')])
print(brain_innervation_df[(brain_innervation_df['Genotype']=='SS36118') & (brain_innervation_df['ROI']==0) & (brain_innervation_df['Regressor']=='AVLP')])


experiments_group_per_fly=general_utils.group_expList_per_fly(experiments)
# print('experiments_group_per_fly', experiments_group_per_fly)

## Making ROI ID list ##
ROI_id_list=[]
for exp_lists_per_fly in experiments_group_per_fly:
	for date, genotype, fly, recrd_num in exp_lists_per_fly:
		Gal4=genotype.split('-')[0]

		ROI_len=len(list(set(t1t2t3_innervation_df[(t1t2t3_innervation_df["Genotype"]==Gal4)]["ROI"].tolist())))

		temp_real_innervation=[]
		temp_manual_innervation=[]
		temp_inIdf_innervation=[]
		for roi_ID in range(ROI_len):
			ROI_id_list.append(Gal4+'-ROI#'+str(roi_ID))

		## all Gal4 just need one time to added the mean value, not correct go across all recordings in the list. So break!!!
		break

print('ROI_id_list', ROI_id_list)



all_brain_neuropil_list=list_morpho.all_brain_areas



innerv_summary_dir= NAS_AN_Proj_Dir+'output/Fig3_S4-single_AN_innervation_mat/plots/' 
if not os.path.exists(innerv_summary_dir):
	os.makedirs(innerv_summary_dir)

main_plot(ROI_id_list, manual_ROI_order, all_brain_neuropil_list, all_brain_innervation_df, all_brain_innervation_manual_df, all_brain_innervation_unIdf_df, colorbar_bas='BuPu', savedir=innerv_summary_dir, filename='all_brain_innervation_overlay')
main_plot(ROI_id_list, manual_ROI_order, brain_neuropil_list, brain_innervation_df, brain_innervation_manual_df, brain_innervation_unIdf_df, colorbar_bas='BuPu', savedir=innerv_summary_dir, filename='brain_innervation_overlay')
main_plot(ROI_id_list, manual_ROI_order, ['GNG','AVLP','Other'], brain_innervation_df, brain_innervation_manual_df, brain_innervation_unIdf_df, colorbar_bas='BuPu', savedir=innerv_summary_dir, filename='brain_innervation_shrinked_overlay')
main_plot(ROI_id_list, manual_ROI_order, vnc_neuropil_list, vnc_innervation_df, vnc_innervation_manual_df, vnc_innervation_unIdf_df, colorbar_bas='BuPu', savedir=innerv_summary_dir, filename='VNC_innervation_overlay')
main_plot(ROI_id_list, manual_ROI_order, t1t2t3_neuropil_list, t1t2t3_innervation_df, t1t2t3_innervation_manual_df, t1t2t3_innervation_unIdf_df, colorbar_bas='BuPu', savedir=innerv_summary_dir, filename='T1T2T3_innervation_overlay')





















