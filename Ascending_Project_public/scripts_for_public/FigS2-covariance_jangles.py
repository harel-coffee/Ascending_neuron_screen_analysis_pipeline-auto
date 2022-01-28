import sys
from skimage import io
import os, os.path
import math
import h5py
import time
import numpy as np
import pandas as pd
import pickle
import more_itertools as mit
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import pandas as pd


import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.list_twoP_exp as list_twoP_exp
import utils.sync_utils as sync_utils
import utils.math_utils as math_utils
import utils.list_behavior as list_behavior




experiments=list_twoP_exp.TwoP_recordings_sparseLine_list


# experiments=[


# # ('20181230', 'R36G04-tdTomGC6fopt', 'fly1', '001'), # done manually #event_min_dur=0.27, norm_thrsld=-0.2, raw_change_thrsld=8
# # ('20181230', 'R36G04-tdTomGC6fopt', 'fly1', '002'), # done manually # event_min_dur=1
# # ('20181230', 'R36G04-tdTomGC6fopt', 'fly1', '003'), # done manually # event_min_dur=1
# # ('20181230', 'R36G04-tdTomGC6fopt', 'fly1', '004'), # done manually # event_min_dur=1
# # ('20181230', 'R36G04-tdTomGC6fopt', 'fly1', '005'), # done manually # event_min_dur=1
# # ('20181230', 'R36G04-tdTomGC6fopt', 'fly1', '006'), # done manually # event_min_dur=1


# # ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '001'),#axoid
# # ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '002'),#axoid
# ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '003'),#axoid
# ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '004'),#axoid
# # ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '005'),#axoid
# # ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '006'),#axoid
# # ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '007'),#axoid
# # ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '008'),#axoid

# # ('20190318', 'SS29621-tdTomGC6fopt', 'fly1', '001'),#axoid
# # ('20190318', 'SS29621-tdTomGC6fopt', 'fly1', '002'),#axoid
# # ('20190318', 'SS29621-tdTomGC6fopt', 'fly1', '003'),#axoid #raw_change_thrsld=10
# # ('20190318', 'SS29621-tdTomGC6fopt', 'fly1', '004'),#axoid
# # ('20190318', 'SS29621-tdTomGC6fopt', 'fly1', '005'),#axoid
# # ('20190318', 'SS29621-tdTomGC6fopt', 'fly1', '006'),#axoid
# ('20190318', 'SS29621-tdTomGC6fopt', 'fly1', '007'),#axoid
# # ('20190318', 'SS29621-tdTomGC6fopt', 'fly1', '008'),#axoid
# # ('20190318', 'SS29621-tdTomGC6fopt', 'fly1', '009'),#axoid

# # ('20190619', 'SS41605-tdTomGC6fopt', 'fly3', '001'),#axoid
# # ('20190619', 'SS41605-tdTomGC6fopt', 'fly3', '002'),#axoid
# # ('20190619', 'SS41605-tdTomGC6fopt', 'fly3', '003'),#axoid
# # ('20190619', 'SS41605-tdTomGC6fopt', 'fly3', '004'),#diff_thrsld=0.2, event_min_dur=0.2, norm_thrsld=0.20, norm_change_thrsld=0.3, raw_change_thrsld=15, outlier_thrsld=1.1
# # ('20190619', 'SS41605-tdTomGC6fopt', 'fly3', '005'),#axoid #raw_change_thrsld=10
# # ('20190619', 'SS41605-tdTomGC6fopt', 'fly3', '006'),#axoid #raw_change_thrsld=10


# # ('20190701', 'SS42008-tdTomGC6fopt', 'fly4', '001'),#axoid
# # ('20190701', 'SS42008-tdTomGC6fopt', 'fly4', '002'),#axoid
# # ('20190701', 'SS42008-tdTomGC6fopt', 'fly4', '003'),#axoid
# # ('20190701', 'SS42008-tdTomGC6fopt', 'fly4', '004'),#axoid #raw_change_thrsld=13
# # ('20190701', 'SS42008-tdTomGC6fopt', 'fly4', '005'),#axoid #o utlier_thrsld=0.5, diff_thrsld=0.2, event_max_dur=2, event_min_dur=0.5, norm_thrsld=0.20, norm_change_thrsld=0.2, raw_change_thrsld=10, desiredRange_startIdx=0, desiredRange_endIdx=-1
# # ('20190701', 'SS42008-tdTomGC6fopt', 'fly4', '006'),#axoid


# # ('20190704', 'SS42749-tdTomGC6fopt', 'fly1', '001'),#axoid
# # ('20190704', 'SS42749-tdTomGC6fopt', 'fly1', '002'),
# # ('20190704', 'SS42749-tdTomGC6fopt', 'fly1', '003'),#axoid
# # ('20190704', 'SS42749-tdTomGC6fopt', 'fly1', '005'),#axoid
# # ('20190704', 'SS42749-tdTomGC6fopt', 'fly1', '006'),#axoid
# # ('20190704', 'SS42749-tdTomGC6fopt', 'fly1', '007'),#axoid
# # ('20190704', 'SS42749-tdTomGC6fopt', 'fly1', '008'),#axoid

# # ('20191001', 'SS49172-tdTomGC6fopt', 'fly1', '001'),
# # ('20191001', 'SS49172-tdTomGC6fopt', 'fly1', '002'),
# # ('20191001', 'SS49172-tdTomGC6fopt', 'fly1', '003'),
# # ('20191001', 'SS49172-tdTomGC6fopt', 'fly1', '004'),
# # ('20191001', 'SS49172-tdTomGC6fopt', 'fly1', '005'),
# # ('20191001', 'SS49172-tdTomGC6fopt', 'fly1', '006'),
# # ('20191001', 'SS49172-tdTomGC6fopt', 'fly1', '007'),
# # ('20191001', 'SS49172-tdTomGC6fopt', 'fly1', '008'),


# # ('20190610', 'SS40489-tdTomGC6fopt', 'fly3', '002'), # diff_thrsld=0.03, event_min_dur=0.27, norm_thrsld=0.27, norm_change_thrsld=0.2, raw_change_thrsld=7
# # ('20190610', 'SS40489-tdTomGC6fopt', 'fly3', '003'), # diff_thrsld=0.03, event_min_dur=0.27, norm_thrsld=0.27, norm_change_thrsld=0.2, raw_change_thrsld=7
# # ('20190610', 'SS40489-tdTomGC6fopt', 'fly3', '004'), # diff_thrsld=0.03, event_min_dur=0.27, norm_thrsld=0.27, norm_change_thrsld=0.2, raw_change_thrsld=7
# # ('20190610', 'SS40489-tdTomGC6fopt', 'fly3', '005'), # diff_thrsld=0.03, event_min_dur=0.27, norm_thrsld=0.27, norm_change_thrsld=0.2, raw_change_thrsld=7


# # ('20190719', 'SS45605-tdTomGC6fopt', 'fly1', '002'),
# # ('20190719', 'SS45605-tdTomGC6fopt', 'fly1', '003'),
# # ('20190719', 'SS45605-tdTomGC6fopt', 'fly1', '004'),
# # ('20190719', 'SS45605-tdTomGC6fopt', 'fly1', '006'),



# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '001'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '002'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '003'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '007'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '008'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '009'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '010'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '011'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '012'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '013'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '014'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '015'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '016'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '017'),#axoid
# # ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '018'),#axoid


# # ('20180822', 'SS25451-tdTomGC6fopt', 'fly4', '002'), #event_min_dur=4
# # ('20180822', 'SS25451-tdTomGC6fopt', 'fly4', '009'),
# # ('20180822', 'SS25451-tdTomGC6fopt', 'fly4', '010'), 
# # ('20180822', 'SS25451-tdTomGC6fopt', 'fly4', '011'),
# # ('20180822', 'SS25451-tdTomGC6fopt', 'fly4', '012'), # outlier_thrsld=0.15, diff_thrsld=0.005, norm_thrsld=0.005, norm_change_thrsld=0.01, raw_change_thrsld=1, startIdx=4680, endIdx=5470
# # ('20180822', 'SS25451-tdTomGC6fopt', 'fly4', '013'),
# # ('20180822', 'SS25451-tdTomGC6fopt', 'fly4', '014'), # outlier_thrsld=0.15, diff_thrsld=0.005, norm_thrsld=0.005, norm_change_thrsld=0.01, raw_change_thrsld=1, startIdx=750, endIdx=1160
# # ('20180822', 'SS25451-tdTomGC6fopt', 'fly4', '015'), # outlier_thrsld=0.15, diff_thrsld=0.005, norm_thrsld=0.005, norm_change_thrsld=0.01, raw_change_thrsld=1, startIdx=3200, endIdx=3526
# # ('20180822', 'SS25451-tdTomGC6fopt', 'fly4', '017'), # diff_thrsld=0.1, event_min_dur=0.5, norm_thrsld=0.25, norm_change_thrsld=0.06, raw_change_thrsld=5


# ]


def save_dic_per_trial(dic_per_trial, save_dir, filename):

	pickle.dump( dic_per_trial, open( save_dir + filename, "wb" ) ) 

	return

def find_leg_corrspd_angleIDs(jangleID_list, leg_order):

	jangleIDs_groupby_leg=[]

	for i, legID in enumerate(leg_order):

		jangleIDs_groupby_leg.append([])

		for j, jangleID in enumerate(jangleID_list):

			jangleID_leg=jangleID.split('.')[1]

			if jangleID_leg==legID:
				jangleIDs_groupby_leg[i].append(jangleID)

	return jangleIDs_groupby_leg


def calcul_mean_corrCoef_wholeDic_to_matrix(corrCoef_wholeDic, level='joint_angle'):

	

	if level=='joint_angle':
		
		corrCoef_jangle_mat=[]

		i=0
		for j_id_master, corr_each_slavePool in corrCoef_wholeDic.items():
			corrCoef_jangle_mat.append([])
			# print('shape corrCoef_wholeDic[j_id_master]', np.shape(corrCoef_wholeDic[j_id_master]))
			# print('corrCoef_wholeDic[j_id_master]', corrCoef_wholeDic[j_id_master])
			# print('corr_each_slavePool', corr_each_slavePool)

			for j_id_slave, corr_slave in enumerate(corr_each_slavePool):
				mean_corr_slave=np.mean(corr_slave)
				corrCoef_jangle_mat[i].append(mean_corr_slave)

			i+=1

		print('shape corrCoef_jangle_mat', np.shape(corrCoef_jangle_mat))
		# print('corrCoef_jangle_mat', corrCoef_jangle_mat)

		return corrCoef_jangle_mat


	elif level=='leg':

		print()

		corrCoef_whole_mat=[]

		for jangleID, corrCoefs in corrCoef_wholeDic.items():
			# print(jangleID)
			corrCoef_whole_mat.append( np.asarray(corrCoefs))
		corrCoef_whole_mat=np.asarray(corrCoef_whole_mat)


		jangles_sum=7
		corrCoef_leg_mat=[]
		for i in range(0, len(leg_list)):
			corrCoef_leg_mat.append([])
			for j in range(0, len(leg_list)):
				# print('shape corrCoef_whole_mat[0+i*jangles_sum:6+i*jangles_sum, 0+j*jangles_sum:6+j*jangles_sum]', np.shape(corrCoef_whole_mat[0+i*jangles_sum:6+i*jangles_sum, 0+j*jangles_sum:6+j*jangles_sum]))
				mean_leg_corrCoef=np.nanmean(corrCoef_whole_mat[0+i*jangles_sum:6+i*jangles_sum, 0+j*jangles_sum:6+j*jangles_sum])

				corrCoef_leg_mat[i].append(mean_leg_corrCoef)

		print('corrCoef_leg_mat', corrCoef_leg_mat)
		print('shape corrCoef_leg_mat', np.shape(corrCoef_leg_mat))





		return corrCoef_leg_mat











####  MAIN #########

NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_Dir


experiments_group_per_fly=general_utils.group_expList_per_fly(experiments)


jangleID_list=list_behavior.jangles_order_Florian
behavior_list=list_behavior.behaviors

jangleID_beh_list=jangleID_list+behavior_list

jangleID_list_NMF=list_behavior.jangles_order_NeuroMechFly
jangleIDNMF_beh_list=jangleID_list_NMF+behavior_list
# leg_list=list_behavior.leg_order_Florian
print('shape jangleID_list', np.shape(jangleID_list))
# print('shape leg_list', np.shape(leg_list))
# print('leg_list', leg_list)
# jangleIDs_groupby_leg=find_leg_corrspd_angleIDs(jangleID_list, leg_list)
# print('shape jangleIDs_groupby_leg', np.shape(jangleIDs_groupby_leg))

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_Dir


output_sum_jangle_dir=NAS_AN_Proj_Dir+'output/FigS2-jangle_beh_covariance/'
if not os.path.exists(output_sum_jangle_dir):
	os.mkdir(output_sum_jangle_dir)

df_beh_jangle = pd.read_pickle(NAS_AN_Proj_Dir+'output/Fig2_S4-GLM_jangles_legs_beh_DFF/df_behaviour_prediction.pkl')


# for key, value in df_beh_jangle.items():
# 	print(key)
# print('df_beh_jangle[Filtered_behaviour]', df_beh_jangle['Filtered_behaviour'])
# sys.exit(0)


jangles_beh_dic_whole={}
for i, jangleID_beh in enumerate(jangleID_beh_list):
	jangles_beh_dic_whole.update({jangleID_beh:[]})
	print('jangleID_beh', jangleID_beh)

corrCoef_jangles_beh_dic_whole={}

y_list=jangleID_list
x_list=y_list
corrCoef_whole=[]



for exp_lists_per_fly in experiments_group_per_fly:
	print('Processing per fly for ... ', exp_lists_per_fly )

	for TwoP_date, TwoP_genotype, TwoP_fly, TwoP_recrd_num in exp_lists_per_fly:

		Gal4=TwoP_genotype.split('-')[0]

		TwoP_date_num=int(TwoP_date)
		trial=int(TwoP_recrd_num)
		Fly_num=int(TwoP_fly[-1])



		# sys.exit(0)



		for i, jangleID_master in enumerate(jangleID_list):

			# print('jangleID_master', jangleID_master)

			jangleID_master_in_df=jangleID_master.split('.')[1]+' '+jangleID_master.split('.')[2]
			jangle_master=df_beh_jangle[(df_beh_jangle["Genotype"] == TwoP_genotype) & (df_beh_jangle["Fly"] == Fly_num) & (df_beh_jangle["Date"] == TwoP_date_num) & (df_beh_jangle["Trial"] == trial)][jangleID_master_in_df].tolist()

			jangles_beh_dic_whole[jangleID_master].extend(jangle_master)



		Beh_preds_ori=df_beh_jangle[(df_beh_jangle["Genotype"] == TwoP_genotype) & (df_beh_jangle["Fly"] == Fly_num) & (df_beh_jangle["Date"] == TwoP_date_num) & (df_beh_jangle["Trial"] == trial)]["Behaviour"].tolist()

		for beh in behavior_list[:9]:
			Beh_bin = sync_utils.convert_behList_to_binarizedList(Beh_preds_ori, beh)
			jangles_beh_dic_whole[beh].extend(Beh_bin)
		# Beh_bin_FW = sync_utils.convert_behList_to_binarizedList(Beh_preds_ori, 'forward_walking')
		# Beh_bin_BW = sync_utils.convert_behList_to_binarizedList(Beh_preds_ori, 'backward_walking')
		# Beh_bin_push = sync_utils.convert_behList_to_binarizedList(Beh_preds_ori, 'pushing')
		# Beh_bin_rest = sync_utils.convert_behList_to_binarizedList(Beh_preds_ori, 'rest')
		# Beh_bin_E_groom = sync_utils.convert_behList_to_binarizedList(Beh_preds_ori, 'eye_grooming')
		# Beh_bin_A_groom = sync_utils.convert_behList_to_binarizedList(Beh_preds_ori, 'antennal_grooming')
		# Beh_bin_FL_groom = sync_utils.convert_behList_to_binarizedList(Beh_preds_ori, 'foreleg_grooming')
		# Beh_bin_HL_groom = sync_utils.convert_behList_to_binarizedList(Beh_preds_ori, 'hindleg_grooming')
		# Beh_bin_Abd_groom = sync_utils.convert_behList_to_binarizedList(Beh_preds_ori, 'abdominal_grooming')
				
		exp = (int(TwoP_date), TwoP_genotype, int(TwoP_fly[-1]), int(TwoP_recrd_num))
		print(exp)
		co2_line, cam_line, opt_flow_line, frame_counter = sync_utils.get_processed_sync_lines_Florian(*exp)
		co2_onset, Beh_bin_co2 = sync_utils.co2_regressors_Florian(cam_line, co2_line)
		jangles_beh_dic_whole['CO2_puff'].extend(Beh_bin_co2)

		Beh_bin_PER, PER_length_regressor = sync_utils.get_PER_regressors_Florian(cam_line, cam_line, *exp)
		print('len Beh_bin_PER', len(Beh_bin_PER))
		jangles_beh_dic_whole['proboscis_extension'].extend(Beh_bin_PER)






for i, jangleID_beh_master in enumerate(jangleID_beh_list):
	
	jangle_beh_master=jangles_beh_dic_whole[jangleID_beh_master]
	print('jangleID_beh_master', jangleID_beh_master)
	print('len jangle_beh_master', len(jangle_beh_master))

	# print('len corrCoef_jangles_beh_dic_whole', len(corrCoef_jangles_beh_dic_whole))
	if len(corrCoef_jangles_beh_dic_whole)<len(jangleID_beh_list):
		corrCoef_jangles_beh_dic_whole.update({jangleID_beh_master:[]})


	for j, jangleID_beh_slave in enumerate(jangleID_beh_list):

		jangle_beh_slave=jangles_beh_dic_whole[jangleID_beh_slave]
		print('jangleID_beh_slave', jangleID_beh_slave)
		print('len jangle_beh_slave', len(jangle_beh_slave))

		_, _, Corr_coef, _, _ = math_utils.linear_regress(jangle_beh_master, jangle_beh_slave)

		corrCoef_jangles_beh_dic_whole[jangleID_beh_master].append(Corr_coef)

		# print('Corr_coef', Corr_coef)
		

	# print('corrCoef_jangles_beh_dic_whole[jangleID_master]', len(corrCoef_jangles_beh_dic_whole[jangleID_master]))






corrCoef_jangle_mat=calcul_mean_corrCoef_wholeDic_to_matrix(corrCoef_jangles_beh_dic_whole, level='joint_angle')
# corrCoef_leg_mat=calcul_mean_corrCoef_wholeDic_to_matrix(corrCoef_jangles_beh_dic_whole, level='leg')


corrCoef_whole_mat_dic={}
corrCoef_whole_mat_dic.update({'corrCoef_jangle_mat':corrCoef_jangle_mat})
# corrCoef_whole_mat_dic.update({'corrCoef_leg_mat':corrCoef_leg_mat})

pickle.dump( corrCoef_whole_mat_dic, open( output_sum_jangle_dir + 'corrCoef_whole_mat_dic', "wb" ) )


mat_max=1
mat_min=-1

# mat_max=np.nanmax(corrCoef_whole_mat)
# mat_min=np.nanmin(corrCoef_whole_mat)


plot_utils.plot_matrix(jangleIDNMF_beh_list, jangleIDNMF_beh_list, corrCoef_jangle_mat, set_max=mat_max, set_min=mat_min, figsize=(10,10), second_x_list=False, Gal4_x_list_reformat=False, savedir=output_sum_jangle_dir, title='joint_angle_corr_coef', PlotMethod='other', cmap='bwr_r')
# plot_utils.plot_matrix(leg_list, leg_list, corrCoef_leg_mat, set_max=mat_max, set_min=mat_min, figsize=(10,10), second_x_list=False, Gal4_x_list_reformat=False, savedir=output_sum_jangle_dir, title='leg_corr_coef', PlotMethod='other', cmap='bwr_r')











