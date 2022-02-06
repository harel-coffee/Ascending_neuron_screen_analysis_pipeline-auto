import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import sys
from itertools import groupby 
from multiprocessing import Pool
import os
import pickle
from pandas import DataFrame
import pandas as pd
import csv

import utils.general_utils as general_utils
import utils.sync_utils as sync_utils
import utils.plot_setting as plot_setting
import utils.plot_utils as plot_utils
import utils.math_utils as math_utils
# import utils.List_deepfly3d_preprocess as List_deepfly3d_preprocess
import utils.list_twoP_exp as list_twoP_exp



experiments = list_twoP_exp.TwoP_recordings_sparseLine_list


experiments_group_per_fly=general_utils.group_expList_per_fly(experiments)







# Innervation_per_Gal4=Qt_Innervation_per_Gal4
# Innervation_per_Gal4=Bin_Innervation_per_Gal4
# Innervation_per_Gal4=mannual_Innervation_per_Gal4
# Innervation_per_Gal4=unIdf_Innervation_per_Gal4

# with open(JRC_MCFO_outDir+'/Distal_neurite_for_matrix.csv', 'w', encoding='UTF8', newline='') as f:
# with open(JRC_MCFO_outDir+'/Distal_neurite_bin_for_matrix.csv', 'w', encoding='UTF8', newline='') as f:
# with open(JRC_MCFO_outDir+'/Distal_neurite_mannual_for_matrix.csv', 'w', encoding='UTF8', newline='') as f:
# with open(JRC_MCFO_outDir+'/Distal_neurite_unIdf_for_matrix.csv', 'w', encoding='UTF8', newline='') as f:


# with open(JRC_MCFO_outDir+'/vnc_neurite_for_matrix.csv', 'w', encoding='UTF8', newline='') as f:
# with open(JRC_MCFO_outDir+'/vnc_neurite_bin_for_matrix.csv', 'w', encoding='UTF8', newline='') as f:
# with open(JRC_MCFO_outDir+'/vnc_neurite_mannual_for_matrix.csv', 'w', encoding='UTF8', newline='') as f:
# with open(JRC_MCFO_outDir+'/vnc_neurite_unIdf_for_matrix.csv', 'w', encoding='UTF8', newline='') as f:


# with open(JRC_MCFO_outDir+'/T1T2T3_neurite_for_matrix.csv', 'w', encoding='UTF8', newline='') as f:
# with open(JRC_MCFO_outDir+'/T1T2T3_neurite_bin_for_matrix.csv', 'w', encoding='UTF8', newline='') as f:
# with open(JRC_MCFO_outDir+'/T1T2T3_neurite_mannual_for_matrix.csv', 'w', encoding='UTF8', newline='') as f:
# with open(JRC_MCFO_outDir+'/T1T2T3_neurite_unIdf_for_matrix.csv', 'w', encoding='UTF8', newline='') as f:




def calculate_Other_value(list_value_brain_innerv, list_brain_area, datatype):

	print('datatype', datatype)
	print('list_value_brain_innerv', list_value_brain_innerv)
	print('len list_value_brain_innerv', len(list_value_brain_innerv))
	print('list_brain_area', list_brain_area)
	print('len list_brain_area', len(list_brain_area))



	other_val=0
	if datatype=='Distal_neurite':
		for i, val in enumerate(list_value_brain_innerv):
			if list_brain_area[i]!='GNG' and list_brain_area[i]!='AVLP':
				if list_value_brain_innerv[i]>0.5:
					print('list_brain_area[i]', list_brain_area[i])
					other_val+=list_value_brain_innerv[i]
				elif list_value_brain_innerv[i]==0.5:
					other_val=0.5
					break


	elif datatype=='Distal_neurite_mannual':
		for i, val in enumerate(list_value_brain_innerv):
			#print(list_brain_area[i], list_value_brain_innerv[i])
			if list_brain_area[i]!='GNG' and list_brain_area[i]!='AVLP':
				if list_value_brain_innerv[i]>=0.5:
					other_val=1
					break
				else:
					other_val=0

	elif datatype=='Distal_neurite_unIdf':
		for i, val in enumerate(list_value_brain_innerv):
			if list_brain_area[i]!='GNG' and list_brain_area[i]!='AVLP':
				if list_value_brain_innerv[i]>=0.5:
					other_val=1
					break
				else:
					other_val=0






	return other_val




list_data_type = [
'all_distal_neurite',
'all_distal_neurite_mannual',
'all_distal_neurite_unIdf',


'Distal_neurite',
'Distal_neurite_mannual',
'Distal_neurite_unIdf',

'vnc_neurite',
'vnc_neurite_mannual',
'vnc_neurite_unIdf',

'T1T2T3_neurite',
'T1T2T3_neurite_mannual',
'T1T2T3_neurite_unIdf',
]


# print('File already exists. If you want to re-run, please comment this line in the script to proceed ...')
# sys.exit(0)


##main##

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_public_Dir




JRC_MCFO_outDir=NAS_AN_Proj_Dir + 'output/Fig3_S4-single_AN_innervation_mat/'





for datatype in list_data_type:
	print('datatype', datatype)
	if datatype=='all_distal_neurite' or datatype=='Distal_neurite' or datatype=='vnc_neurite' or datatype=='T1T2T3_neurite':

		if datatype[:10]=='all_distal':
			csv_input_name='Innervation_px_count_visualCount_distalenurites'		
		elif datatype[:6]=='Distal':
			csv_input_name='Innervation_px_count_visualCount_distalenurites'
		elif datatype[:3]=='vnc':
			csv_input_name='Innervation_px_count_visualCount_vnc'
		elif datatype[:6]=='T1T2T3':
			csv_input_name='Innervation_px_count_visualCount_T1T2T3'

		innervation_dic=pickle.load( open( JRC_MCFO_outDir+'/'+csv_input_name+'.p', "rb" ) )

		Gal4_list=innervation_dic['Gal4_list']

		if not datatype=='all_distal_neurite':
			Qt_Innervation_per_Gal4=innervation_dic['Innervation_per_Gal4']
			Innervated_neuropil_list=list(innervation_dic['Innervated_neuropil_list'])
			if datatype[:6]=='Distal':
				Innervated_neuropil_list.append('Other')
		else:
			Qt_Innervation_per_Gal4=innervation_dic['all_Innervation_per_Gal4']
			Innervated_neuropil_list=list(innervation_dic['all_Innervated_neuropil_list'])
			print('Innervated_neuropil_list', Innervated_neuropil_list)

		Innervation_per_Gal4=Qt_Innervation_per_Gal4
		# print('Innervation_per_Gal4', Innervation_per_Gal4)
		csv_output_filename= datatype+'_for_matrix.csv'


	elif datatype=='all_distal_neurite_mannual' or datatype=='Distal_neurite_mannual' or datatype=='vnc_neurite_mannual' or datatype=='T1T2T3_neurite_mannual':

		if datatype[:10]=='all_distal':
			csv_input_name='Innervation_px_count_visualCount_distalenurites'	
		elif datatype[:6]=='Distal':
			csv_input_name='Innervation_px_count_visualCount_distalenurites'
		elif datatype[:3]=='vnc':
			csv_input_name='Innervation_px_count_visualCount_vnc'
		elif datatype[:6]=='T1T2T3':
			csv_input_name='Innervation_px_count_visualCount_T1T2T3'


		innervation_dic=pickle.load( open( JRC_MCFO_outDir+'/'+csv_input_name+'.p', "rb" ) )

		Gal4_list=innervation_dic['Gal4_list']
		
		if not datatype=='all_distal_neurite_mannual':
			mannual_Innervation_per_Gal4=innervation_dic['Innervation_per_Gal4_mannual']
			Innervated_neuropil_list=list(innervation_dic['Innervated_neuropil_list'])
			if datatype[:6]=='Distal':
				Innervated_neuropil_list.append('Other')
		else:
			mannual_Innervation_per_Gal4=innervation_dic['all_Innervation_per_Gal4_mannual']
			Innervated_neuropil_list=list(innervation_dic['all_Innervated_neuropil_list'])
			print('Innervated_neuropil_list', Innervated_neuropil_list)

		Innervation_per_Gal4=mannual_Innervation_per_Gal4
		csv_output_filename= datatype+'_for_matrix.csv'


	elif datatype=='all_distal_neurite_unIdf' or datatype=='Distal_neurite_unIdf' or datatype=='vnc_neurite_unIdf' or datatype=='T1T2T3_neurite_unIdf':

		if datatype[:10]=='all_distal':
			csv_input_name='Innervation_px_count_visualCount_distalenurites'	
		elif datatype[:6]=='Distal':
			csv_input_name='Innervation_px_count_visualCount_distalenurites'
		elif datatype[:3]=='vnc':
			csv_input_name='Innervation_px_count_visualCount_vnc'
		elif datatype[:6]=='T1T2T3':
			csv_input_name='Innervation_px_count_visualCount_T1T2T3'

		innervation_dic=pickle.load( open( JRC_MCFO_outDir+'/'+csv_input_name+'.p', "rb" ) )

		Gal4_list=innervation_dic['Gal4_list']

		if not datatype=='all_distal_neurite_unIdf':
			unIdf_Innervation_per_Gal4=innervation_dic['Innervation_per_Gal4_unidenfiable']
			Innervated_neuropil_list=list(innervation_dic['Innervated_neuropil_list'])
			if datatype[:6]=='Distal':
				Innervated_neuropil_list.append('Other')

		else:
			unIdf_Innervation_per_Gal4=innervation_dic['all_Innervation_per_Gal4_unidenfiable']
			Innervated_neuropil_list=list(innervation_dic['all_Innervated_neuropil_list'])
			print('Innervated_neuropil_list', Innervated_neuropil_list)


		Innervation_per_Gal4=unIdf_Innervation_per_Gal4
		csv_output_filename= datatype+'_for_matrix.csv'


	print('csv_output_filename', csv_output_filename)



	csv_header=['Genotype', 'ROI', 'Regressor', 'area']



	with open(JRC_MCFO_outDir+'/'+csv_output_filename, 'w', encoding='UTF8', newline='') as f:


		writer = csv.writer(f)
		writer.writerow(csv_header)

		for exp_lists_per_fly in experiments_group_per_fly:
			for date, genotype, fly, recrd_num in exp_lists_per_fly:

				Gal4=genotype.split('-')[0]
				fly_beh=fly[0].upper()+fly[1:]

				outDir_AN_recrd=NAS_AN_Proj_Dir+'/03_general_2P_exp/'+Gal4+'/2P/'+date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num+'/output/'
				print('outDir_AN_recrd', outDir_AN_recrd)


				Beh_Jpos_GC_DicData=general_utils.open_Beh_Jpos_GC_DicData(outDir_AN_recrd, 'SyncDic_7CamBeh_BW_20210619_GC-RES.p')

				GC_set = Beh_Jpos_GC_DicData['GCset']
			
				ROI_count=len(GC_set)

				break

			Regressor_rows=[]
			for i in range(0,ROI_count):
				 Regressor_rows.extend(Innervated_neuropil_list)

			print('shape Regressor_rows', np.shape(Regressor_rows))
			print('Regressor_rows', Regressor_rows)

			print(np.where(np.asarray(Gal4_list)==Gal4))



			print('Gal4_list', Gal4_list)
			idx_current_Gal4=np.where(np.asarray(Gal4_list)==Gal4)[0][0]
			print('idx_current_Gal4', idx_current_Gal4)

			
			if datatype[:6]=='Distal':
				
				if datatype=='Distal_neurite':
					Other_value=calculate_Other_value(Innervation_per_Gal4[idx_current_Gal4], Innervated_neuropil_list, datatype)
				elif datatype=='Distal_neurite_mannual':
					Other_value=calculate_Other_value(Innervation_per_Gal4[idx_current_Gal4], Innervated_neuropil_list, datatype)				
				elif datatype=='Distal_neurite_unIdf':
					Other_value=calculate_Other_value(Innervation_per_Gal4[idx_current_Gal4], Innervated_neuropil_list, datatype)	

				print('Innervation_per_Gal4[idx_current_Gal4]', Innervation_per_Gal4[idx_current_Gal4])
				print('len Innervation_per_Gal4[idx_current_Gal4]', len(Innervation_per_Gal4[idx_current_Gal4]))
				print('type Innervation_per_Gal4[idx_current_Gal4]', type(Innervation_per_Gal4[idx_current_Gal4]))
				print('Other_value', Other_value)

				current_Gal4_innervation = list(Innervation_per_Gal4[idx_current_Gal4])+[Other_value]
				print('current_Gal4_innervation', current_Gal4_innervation)
				print('len current_Gal4_innervation', len(current_Gal4_innervation))
			
			else:
				current_Gal4_innervation = list(Innervation_per_Gal4[idx_current_Gal4])


			area_rows=[]
			for i in range(0,ROI_count):
				area_rows.extend(current_Gal4_innervation)
			# print('shape area_rows', np.shape(area_rows))
			# print('area_rows', area_rows)


			len_rows=len(Innervated_neuropil_list)

			Gal4_rows=[Gal4]*(ROI_count*len_rows)
			print('shape Gal4_rows', np.shape(Gal4_rows))
			print('Gal4_rows', Gal4_rows)

			ROI_rows=[]
			for i in range(0,ROI_count):
				ROI_rows.extend([i]*len_rows)
			print('shape ROI_rows', np.shape(ROI_rows))
			print('ROI_rows', ROI_rows)




			print('len_rows',len_rows)


			print('shape Regressor_rows', np.shape(Regressor_rows))
			print('shape area_rows', np.shape(area_rows))
			print('area_rows', area_rows)


			# print('Regressor_rows', Regressor_rows)



			csv_data=np.stack((Gal4_rows, ROI_rows, Regressor_rows, area_rows), axis=-1)

			
			
			writer.writerows(csv_data)
		





		
























