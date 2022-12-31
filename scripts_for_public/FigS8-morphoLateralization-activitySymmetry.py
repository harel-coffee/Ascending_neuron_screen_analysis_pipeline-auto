import time
import numpy as np
import pandas as pd
import pickle
import more_itertools as mit
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import pandas as pd
from itertools import combinations
from scipy import stats
# from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm
import scipy.stats
import os
import sys
from skimage import io


import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.list_twoP_exp as list_twoP_exp
import utils.list_innervation_MCFO as list_innervation_MCFO
import utils.sync_utils as sync_utils
import utils.math_utils as math_utils






assign_ROI_for_comparison={}
# assign_ROI_for_comparison.update({'SS29579':[0,1,2,3,4,5]})
assign_ROI_for_comparison.update({'SS29579':[0,1,2,3]})
assign_ROI_for_comparison.update({'SS49172':[0,1,2]})
assign_ROI_for_comparison.update({'SS31480':[0,2]})

assign_ROI_for_comparison.update({'SS34574':[0,1]})
assign_ROI_for_comparison.update({'SS29893':[2,3]})
assign_ROI_for_comparison.update({'SS51046':[0,1]})

assign_ROI_for_comparison.update({'SS42740':[0,1]})
assign_ROI_for_comparison.update({'R70H06':[0,1]})

assign_ROI_for_comparison.update({'SS25469':[0,1]})

# assign_ROI_for_comparison.update({'SS27485':[0,1,2,3]})
assign_ROI_for_comparison.update({'SS27485':[0,2]})
assign_ROI_for_comparison.update({'SS36131':[0,1]})
assign_ROI_for_comparison.update({'SS38624':[0,1,2,3]})
assign_ROI_for_comparison.update({'SS38592':[0,1,2,5]})
assign_ROI_for_comparison.update({'SS41822':[0,1]})
assign_ROI_for_comparison.update({'SS43652':[0,2,3,4]})

assign_ROI_for_comparison.update({'SS31232':[0,1]})
assign_ROI_for_comparison.update({'SS30303':[0,1]})
assign_ROI_for_comparison.update({'SS25451':[2,4]})

assign_ROI_for_comparison.update({'SS42749':[0,1]})
assign_ROI_for_comparison.update({'SS44270':[0,1]})
assign_ROI_for_comparison.update({'SS41605':[0,1]})

assign_ROI_for_comparison.update({'SS36112':[0,1]})
assign_ROI_for_comparison.update({'SS41806':[0,1]})
assign_ROI_for_comparison.update({'SS51029':[0,1,2,3]})

assign_ROI_for_comparison.update({'SS31456':[0,1]})
assign_ROI_for_comparison.update({'SS38631':[0,1]})
assign_ROI_for_comparison.update({'SS51017':[0,1]})
assign_ROI_for_comparison.update({'SS51021':[0,1]})

assign_ROI_for_comparison.update({'SS29633':[0,1,2]})
assign_ROI_for_comparison.update({'SS41815':[0,1]})
assign_ROI_for_comparison.update({'SS40134':[0,1]})



manual_ROI_order=[
'SS25451',
'SS30303',
'SS31232',
'R70H06',
'SS42740',
'SS38624',
'SS41605',
'SS41822',
'SS41806',
'SS29579',
'SS43652',
'SS44270',
'SS38592',
'SS38631',
'SS40134',
'SS41815',
'SS51017',
'SS51029',
'SS49172',
'SS51046',
'SS29893',
'SS34574',
'SS31456',
'SS29633',
'SS36112',
'SS36131',
'SS25469',
'SS27485',
'SS31480',
'SS42749',
'SS51021',
]

experiments=list_twoP_exp.TwoP_recordings_sparseLine_list

VNC_neurites_filelist=list_innervation_MCFO.VNC_neurites_filelist


mcfo_Gal4name_list=[]
for traced_file_dir in VNC_neurites_filelist:

	if len(traced_file_dir)>9:
		Gal4_name = traced_file_dir.split('/')[7][4:]
	else:
		Gal4_name=traced_file_dir
	mcfo_Gal4name_list.append(Gal4_name)

print('mcfo_Gal4name_list', mcfo_Gal4name_list)



def make_new_pair_ID_list(old_id_list):

	# print('old_id_list', old_id_list)

	new_id_list=[]
	for i, roi_pair_id in enumerate(old_id_list):
		pair_roi=roi_pair_id.split(' ')[0]+' '+roi_pair_id.split(' ')[1]+'\n'+'-'+'\n'+roi_pair_id.split(' ')[2]
		# print('pair_roi', pair_roi)
		new_id_list.append(pair_roi)

	return new_id_list






def sorting_roiID_correspondingMat_based_on_an_order(roi_id_list, corrspd_list, base_of_order_list, rename_ID_into_ROI=True):

	print('roi_id_list', roi_id_list)


	if rename_ID_into_ROI==True:
		ressembled_name_for_baseOrder_list=[]
		for i, id_name in enumerate(base_of_order_list):
			ressembled_name=id_name.split(' ')[0]+'-ROI#'+id_name.split(' ')[1]
			ressembled_name_for_baseOrder_list.append(ressembled_name)
	else:
		ressembled_name_for_baseOrder_list=base_of_order_list




	numbers_for_old_order=[]
	for i, id_name in enumerate(roi_id_list):
		id_name_Gal4=id_name.split(' ')[0]
		print(id_name_Gal4)
		if id_name_Gal4 in ressembled_name_for_baseOrder_list:
			numbers_for_old_order.append(ressembled_name_for_baseOrder_list.index(id_name_Gal4))
		else:
			print(id_name_Gal4, 'not in ressembled_name_for_baseOrder_list')
			print('Please recheck if base order list has all the ID of roi_id_list!!')
			sys.exit(0)

	# print('numbers_for_old_order', numbers_for_old_order)

	# print('len roi_id_list', len(roi_id_list))
	# print('len numbers_for_old_order', len(numbers_for_old_order))
	

	zipped_id_lists = zip(numbers_for_old_order, roi_id_list)
	# print('zipped_id_lists', zipped_id_lists)
	sorted_zipped_id_lists = sorted(zipped_id_lists)
	sorted_new_roi_id_list = [element for _, element in sorted_zipped_id_lists]
	# print('sorted_zipped_id_lists', sorted_zipped_id_lists)


	zipped_corrspd_lists = zip(numbers_for_old_order, corrspd_list)
	sorted_zipped_corrspd_lists = sorted(zipped_corrspd_lists)
	sorted_new_corrspd_list = [element for _, element in sorted_zipped_corrspd_lists]

	# print('sorted_new_roi_id_list', sorted_new_roi_id_list)


	return sorted_new_roi_id_list, sorted_new_corrspd_list



def activity_symmetricity_check_betwn_ROIpair(trace_set, ROI_pair):

	trace1=trace_set[ROI_pair[0]]
	trace2=trace_set[ROI_pair[1]]

	trace1=math_utils.norm_to_max(trace_set[ROI_pair[0]], percentile_th_to_norm=100)
	trace2=math_utils.norm_to_max(trace_set[ROI_pair[1]], percentile_th_to_norm=100)


	slope_ss, intercept_ss, Corr_coef_ss, p_value_ss, _ = math_utils.linear_regress(trace1,trace2)
	Corr_coef_ss_pear=scipy.stats.pearsonr(trace1, trace2)


	model = sm.OLS(trace2, trace1).fit()
	model_summary = model.summary()
	r2_sm=model.rsquared
	p_value_sm=model.pvalues[0]
	slope_sm=model.params[0]

	predictions = model.predict(trace1) 
	r2_sk=r2_score(trace2, predictions)
 
	r2=r2_sm
	p_value=p_value_sm
	slope=slope_sm
	Corr_coef=Corr_coef_ss
	

	print('r2_sm', r2_sm)
	print('r2_sk', r2_sk)

	print('Corr_coef_ss_pear', Corr_coef_ss_pear)
	print('Corr_coef_ss', Corr_coef_ss)


	print('slope', slope)
	print('intercept_ss', intercept_ss)
	print('Corr_coef', Corr_coef)
	print('p_value', p_value)




	return r2, slope, Corr_coef, p_value


def plot_scatter(data1, data2, x_y_name=['x', 'y'], datapoint_labels=[], savedir=None, filename=None):

	slope_ss, intercept_ss, Corr_coef_ss, p_value_ss, _ = math_utils.linear_regress(data1,data2)



	data1_intcp = sm.add_constant(data1)
	model = sm.OLS(data2, data1_intcp).fit()
	model_summary = model.summary()
	r2_sm=model.rsquared
	slope_sm=model.params[0]
	p_value_sm=model.pvalues[0]


	predictions = model.predict(data1_intcp) 
	r2_sk=r2_score(data2, predictions)

	print('model_summary', model_summary)
	print('model.params', model.params)
	print('model.pvalues', model.pvalues)
	print('p_value_ss', p_value_ss)
	print('slope_ss', slope_ss)


	r2=r2_sm
	slope=slope_sm
	p_value=p_value_sm
	slope=slope_sm
	intercept=intercept_ss
	Corr_coef=Corr_coef_ss



	print('r2_sm', r2_sm)
	print('r2_sk', r2_sk)

	print('slope', slope)
	print('intercept', intercept)
	print('Corr_coef', Corr_coef)
	print('p_value', p_value)

	interested_ROI_to_label=[
	'SS29579',
	'SS34574',
	'SS51046',
	'SS25469',
	'SS42740',
	'SS27485',
	'SS31232',
	'SS36112',

	# 'SS51021',
	# 'SS42749',
	# 'SS41822',
	# # 'SS38592',
	# 'SS36131',
	# 'SS29633',
	
	]




	fig = plt.figure(facecolor='white', figsize=(5,5), dpi=300)
	fig.suptitle(filename, color='k')
	fig.subplots_adjust(wspace = 0.01, hspace=0.01, left=0.17, right = 0.83, bottom = 0.17 , top = 0.83)
	plt.scatter(data1, data2, s=7, facecolors='none', edgecolors='gray')
	plt.plot(data1, predictions, color='k')
	plt.text(int(np.nanmin(data1)), int(0.80*max(data2)), 'Slope = '+str(round(slope, 2))+'\nR^2 = '+str(round(r2, 2))+'\nP value = '+str(round(p_value, 2)))
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.xlabel(x_y_name[0])
	plt.ylabel(x_y_name[1])
	for i, txt in enumerate(datapoint_labels):
		if txt[:-4] in interested_ROI_to_label:
		    plt.annotate(txt, (data1[i], data2[i]))
		    plt.scatter(data1[i], data2[i], s=7, facecolors='r', edgecolors='r')

	plt.savefig(savedir+filename+'.pdf')
	plt.savefig(savedir+filename+'.png')
	plt.clf()
	plt.close(fig)





	return





##main##

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_Dir




JRC_MCFO_dir=NAS_AN_Proj_Dir + '04_mcfo_traced_singleAN_exp/'
VNC_dir= JRC_MCFO_dir+'VNC/'


T1_R_vnc_name='T1_R_VNC.nrrd'
T2_R_vnc_name='T2_R_VNC.nrrd'
T3_R_vnc_name='T3_R_VNC.nrrd'
T1_L_vnc_name='T1_L_VNC.nrrd'
T2_L_vnc_name='T2_L_VNC.nrrd'
T3_L_vnc_name='T3_L_VNC.nrrd'
T1_R_vnc_mask = general_utils.read_nrrd(VNC_dir, T1_R_vnc_name)
T2_R_vnc_mask = general_utils.read_nrrd(VNC_dir, T2_R_vnc_name)
T3_R_vnc_mask = general_utils.read_nrrd(VNC_dir, T3_R_vnc_name)
T1_L_vnc_mask = general_utils.read_nrrd(VNC_dir, T1_L_vnc_name)
T2_L_vnc_mask = general_utils.read_nrrd(VNC_dir, T2_L_vnc_name)
T3_L_vnc_mask = general_utils.read_nrrd(VNC_dir, T3_L_vnc_name)

T1_R_vnc_mask=np.transpose(T1_R_vnc_mask, (2,1,0))	
T2_R_vnc_mask=np.transpose(T2_R_vnc_mask, (2,1,0))	
T3_R_vnc_mask=np.transpose(T3_R_vnc_mask, (2,1,0))	
T1_L_vnc_mask=np.transpose(T1_L_vnc_mask, (2,1,0))	
T2_L_vnc_mask=np.transpose(T2_L_vnc_mask, (2,1,0))	
T3_L_vnc_mask=np.transpose(T3_L_vnc_mask, (2,1,0))	

nrrd_T1T2T3_R_mask_stacks=[
T1_R_vnc_mask,
T2_R_vnc_mask,
T3_R_vnc_mask
]

nrrd_T1T2T3_L_mask_stacks=[
T1_L_vnc_mask,
T2_L_vnc_mask,
T3_L_vnc_mask
]




Visual_check_line_T1T2T3={}
Visual_check_line_T1T2T3.update({'SS46233':['T1', 'T2', 'T3']})
Visual_check_line_T1T2T3.update({'R85A11':[]})
Visual_check_line_T1T2T3.update({'SS42008':['T1', 'T2', 'T3']})
Visual_check_line_T1T2T3.update({'SS40619':[]})
# Visual_check_line_T1T2T3.update({'SS29893':['catch as SS34574']})
Visual_check_line_T1T2T3.update({'SS29621':[]})
Visual_check_line_T1T2T3.update({'SS28596':['T1']})
Visual_check_line_T1T2T3.update({'SS51038':[]})
# Visual_check_line_T1T2T3.update({'R70H06':['catch as SS42740']}) 
# Visual_check_line_T1T2T3.update({'SS41605':['catch as SS44270']})
Visual_check_line_T1T2T3.update({'SS31219':['T1', 'T2', 'T3']}) #each neuron per leg neuromere
Visual_check_line_T1T2T3.update({'MAN':['T2', 'T3']}) 
Visual_check_line_T1T2T3.update({'SS36118':[]}) 
Visual_check_line_T1T2T3.update({'SS40489':['T1', 'T2', 'T3']}) #each neuron per leg neuromere
Visual_check_line_T1T2T3.update({'SS45363':[]})
Visual_check_line_T1T2T3.update({'SS45605':['T1', 'T2', 'T3']}) 
Visual_check_line_T1T2T3.update({'SS52147':[]})
Visual_check_line_T1T2T3.update({'R36G04':['T1', 'T2', 'T3']})
Visual_check_line_T1T2T3.update({'R30A08':['T1', 'T2', 'T3']})
Visual_check_line_T1T2T3.update({'R39G01':['T1', 'T2', 'T3']})
Visual_check_line_T1T2T3.update({'R69H10':[]})
Visual_check_line_T1T2T3.update({'R87H02':['T3']})


Visual_check_T1T2T3_list=[]
for i, v in Visual_check_line_T1T2T3.items():
	Visual_check_T1T2T3_list.append(i)




ROI_id_list=[]
lateralization_value_allROI=[]
r2_symm_list_allROI=[]
slope_symm_list_allROI=[]
Corr_coef_symm_list_allROI=[]
p_value_symm_list_allROI=[]
unilateralized_ratio_list_allROI=[]
bilateralized_ratio_list_allROI=[]

experiments_group_per_fly=general_utils.group_expList_per_fly(experiments)
# print('experiments_group_per_fly', experiments_group_per_fly)

for exp_lists_per_fly in experiments_group_per_fly:

	# print('exp_lists_per_fly', exp_lists_per_fly)

	gapFree_GC_fly=[]

	Gal4=exp_lists_per_fly[0][1].split('-')[0]
	print('Gal4', Gal4)

	if not Gal4 in Visual_check_T1T2T3_list:


		for date, genotype, fly, recrd_num in exp_lists_per_fly:

			
			fly_beh=fly[0].upper()+fly[1:]
			flyDir = NAS_AN_Proj_Dir +'03_general_2P_exp/'+ Gal4 +'/2P/'+ date+'/'+genotype+'-'+fly+'/'
			outDir_AN_recrd=flyDir+genotype+'-'+fly+'-'+recrd_num+'/output'


			outDirGC6_axoid = outDir_AN_recrd + '/GC6_auto/final/'

			GC_set_temp = general_utils.readGCfile(outDirGC6_axoid)
			if np.isnan(GC_set_temp).any():
				print('Replacing NaN with interpolaration')
				GC_set=sync_utils.replace_nan_with_interp(GC_set_temp)

			else:
				print('No NaN detected. Not replacing Na')
				GC_set=GC_set_temp

			GC_raw_datafreq=len(GC_set[0])/248 #s

			for i, GC_trace in enumerate(GC_set):
				if len(gapFree_GC_fly)!=len(GC_set):
					gapFree_GC_fly.append([])
				GC_trace=math_utils.smooth_data(GC_trace, windowlen=int(GC_raw_datafreq*0.7)) 
				# GC_trace=math_utils.norm_to_max(GC_trace, percentile_th_to_norm=100)
				gapFree_GC_fly[i].extend(GC_trace)



		target_ROIs=assign_ROI_for_comparison[Gal4]

		



		combinations_ROIs = list(combinations(target_ROIs, 2)) 

		if Gal4=='SS38592':
			combinations_ROIs=[(0,5),(1,5),(2,5)]
		if Gal4=='SS38624':
			combinations_ROIs=[(0,2),(0,3),(1,2),(1,3)]
		if Gal4=='SS43652':
			combinations_ROIs=[(0,3),(0,4),(2,3),(2,4)]
		if Gal4=='SS51029':
			combinations_ROIs=[(0,2),(0,3),(1,2),(1,3)]
		if Gal4=='SS49172':
			combinations_ROIs=[(0,1),(0,2)]
		if Gal4=='SS29579':
			combinations_ROIs=[(0,2),(0,3),(1,2),(1,3)]
			# combinations_ROIs=[(0,3)]

		print('combinations_ROIs', combinations_ROIs)


		for i, roi_pair in enumerate(combinations_ROIs):
			
			#the fitting value is also depndent on the portion of baseline datapoints. Better balance the activated vs baseline amount of datapoint.

			r2_symm, slope_symm, Corr_coef_symm, p_value_symm=activity_symmetricity_check_betwn_ROIpair(gapFree_GC_fly, roi_pair) 

			ROI_id_list.append(Gal4+' '+str(roi_pair[0])+' '+str(roi_pair[1]))		

			r2_symm_list_allROI.append(r2_symm)
			slope_symm_list_allROI.append(slope_symm)
			Corr_coef_symm_list_allROI.append(Corr_coef_symm)
			p_value_symm_list_allROI.append(p_value_symm)

	
		

		## Process analyzing lateralization of VNC innervation

		R_intsct_px_list=[]
		L_intsct_px_list=[]


		##Substitute redundant Gal4 line with those have available MCFO image
		if Gal4=='SS41605':
			Gal4='SS44270'
		if Gal4=='SS29893':
			Gal4='SS34574'
		if Gal4=='R70H06':
			Gal4='SS42740'

		Gal4_idx_in_mcfp_list=mcfo_Gal4name_list.index(Gal4)
		traced_file_dir=VNC_neurites_filelist[Gal4_idx_in_mcfp_list]

		traced_neurites_stack = np.asarray(io.imread(traced_file_dir))

		traced_neurites_stack[traced_neurites_stack>0]=1
		traced_neurite_px_count=np.count_nonzero(traced_neurites_stack>0)


		for i, vnc_r_mask in enumerate(nrrd_T1T2T3_R_mask_stacks):
			r_intrsct_stacks = traced_neurites_stack*vnc_r_mask
			r_intrsct_px_count = np.count_nonzero(r_intrsct_stacks>0)
			R_intsct_px_list.append(r_intrsct_px_count)

		for i, vnc_l_mask in enumerate(nrrd_T1T2T3_L_mask_stacks):
			l_intrsct_stacks = traced_neurites_stack*vnc_l_mask
			l_intrsct_px_count = np.count_nonzero(l_intrsct_stacks>0)
			L_intsct_px_list.append(l_intrsct_px_count)

		T1_diff_px_RL=abs(R_intsct_px_list[0]-L_intsct_px_list[0])
		T2_diff_px_RL=abs(R_intsct_px_list[1]-L_intsct_px_list[1])
		T3_diff_px_RL=abs(R_intsct_px_list[2]-L_intsct_px_list[2])

		unilateralized_ratio=(T1_diff_px_RL+T2_diff_px_RL+T3_diff_px_RL)/traced_neurite_px_count
		bilateralized_ratio=1-unilateralized_ratio


	else:
		continue



	# repeat appending the values till it match the amounts of ROI pairs in dFF data
	for i in range(0, len(combinations_ROIs)):
		unilateralized_ratio_list_allROI.append(unilateralized_ratio)
		bilateralized_ratio_list_allROI.append(bilateralized_ratio)


print('ROI_id_list', ROI_id_list)
new_ROI_id_list=make_new_pair_ID_list(ROI_id_list)
print('new_ROI_id_list', new_ROI_id_list)



GCsymm_morphoLterl_summary = NAS_AN_Proj_Dir + 'output/FigS8-morphoSymmetry-activitySymmetry/plots/'
if not os.path.exists(GCsymm_morphoLterl_summary):
	os.makedirs(GCsymm_morphoLterl_summary)


reordered_ROI_ID_list, reordered_Corr_coef_symm_list=sorting_roiID_correspondingMat_based_on_an_order(new_ROI_id_list, Corr_coef_symm_list_allROI, manual_ROI_order, rename_ID_into_ROI=False)
reordered_ROI_ID_list, reordered_bilateralized_ratio_list=sorting_roiID_correspondingMat_based_on_an_order(new_ROI_id_list, bilateralized_ratio_list_allROI, manual_ROI_order, rename_ID_into_ROI=False)




# plot_utils.plot_matrix(new_ROI_id_list, ['r-squared'], r2_symm_list_allROI, second_x_list=p_value_symm_list_allROI, roi_seperation_marker=' ', savedir=GCsymm_morphoLterl_summary, title='dFF_r2_betwn_ROIpair', PlotMethod='other', unit=' ', cmap='BuPu')
# plot_utils.plot_matrix(new_ROI_id_list, ['slope'], slope_symm_list_allROI, second_x_list=p_value_symm_list_allROI, roi_seperation_marker=' ', savedir=GCsymm_morphoLterl_summary, title='dFF_slope_betwn_ROIpair', PlotMethod='other', unit=' ', cmap='BuPu')
plot_utils.plot_matrix(reordered_ROI_ID_list, ['Corr. coef.'], reordered_Corr_coef_symm_list, second_x_list=p_value_symm_list_allROI, roi_seperation_marker=' ', savedir=GCsymm_morphoLterl_summary, title='dFF_corr_coef_betwn_ROIpair', Gal4_x_list_reformat=True, PlotMethod='other', unit=' ', cmap='BuPu')

# plot_utils.plot_matrix(new_ROI_id_list, ['Unilateralized_ratio'], unilateralized_ratio_list_allROI, roi_seperation_marker=' ',savedir=GCsymm_morphoLterl_summary, title='UnilateralizationIdx_all_Gal4', PlotMethod='other', unit=' ', cmap='BuPu')
plot_utils.plot_matrix(reordered_ROI_ID_list, ['bilateralization_ratio'], reordered_bilateralized_ratio_list, roi_seperation_marker=' ',savedir=GCsymm_morphoLterl_summary, title='BilateralizationIdx_all_Gal4', PlotMethod='other', Gal4_x_list_reformat=True, unit=' ', cmap='BuPu')




# plot_scatter(unilateralized_ratio_list_allROI, Corr_coef_symm_list_allROI, x_y_name=['Unilateralization ratio', 'Corr. coef.'], datapoint_labels=ROI_id_list, savedir=GCsymm_morphoLterl_summary, filename='morphoUnilatrl-GCsymmCorr')

plot_scatter(bilateralized_ratio_list_allROI, Corr_coef_symm_list_allROI, x_y_name=['bilateralization ratio', 'Corr. coef.'], datapoint_labels=ROI_id_list, savedir=GCsymm_morphoLterl_summary, filename='morphoBilatrl-GCsymmCorr' )
# plot_scatter(bilateralized_ratio_list_allROI, slope_symm_list_allROI, x_y_name=['bilateralization ratio', 'slope'], datapoint_labels=ROI_id_list, savedir=GCsymm_morphoLterl_summary, filename='morphoBilatrl-GCsymmSlope' )
# plot_scatter(bilateralized_ratio_list_allROI, r2_symm_list_allROI, x_y_name=['bilateralization ratio', 'r-squared'], datapoint_labels=ROI_id_list, savedir=GCsymm_morphoLterl_summary, filename='morphoBilatrl-GCsymmRsqured' )












