import sys
import nrrd
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
import csv
import scipy


import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.sync_utils as sync_utils
import utils.math_utils as math_utils


import utils.list_innervation_MCFO as list_innervation_MCFO
import utils.list_innervation_MCFO as list_innervation_MCFO




VNC_neurites_filelist=list_innervation_MCFO.VNC_neurites_filelist
brain_neurites_filelist=list_innervation_MCFO.distal_neurites_filelist




##---manual assign the innervarted area for those no single neuron MCFO data based on full expression images---##
Visual_check_line_brain={}
Visual_check_line_brain.update({'R85A11':['GNG', 'AVLP', 'PVLP']})
Visual_check_line_brain.update({'SS42008':[]})
Visual_check_line_brain.update({'SS40619':[]})
Visual_check_line_brain.update({'SS29893':['catch as SS34574']})
Visual_check_line_brain.update({'SS29621':[]})
# Visual_check_line_brain.update({'SS28596':['GNG', 'IPS']})
Visual_check_line_brain.update({'SS51038':[]})
Visual_check_line_brain.update({'R70H06':['catch as SS42740']}) 
Visual_check_line_brain.update({'SS41605':['GNG']})
Visual_check_line_brain.update({'SS31219':['GNG']})
Visual_check_line_brain.update({'MAN':['GNG','FLA']}) 
Visual_check_line_brain.update({'SS36118':[]}) 
Visual_check_line_brain.update({'SS40489':['GNG', 'AVLP']})
Visual_check_line_brain.update({'SS45363':[]})
Visual_check_line_brain.update({'SS45605':['AVLP']})
Visual_check_line_brain.update({'SS52147':[]})
Visual_check_line_brain.update({'R36G04':['GNG']})
Visual_check_line_brain.update({'R30A08':['GNG']})
Visual_check_line_brain.update({'R39G01':['GNG']})
Visual_check_line_brain.update({'R69H10':[]})
Visual_check_line_brain.update({'R87H02':['GNG','FLA','SMP']})


Visual_check_line_VNC={}
Visual_check_line_VNC.update({'SS46233':['Prothoracic neuromere', 'Mesothoracic neuromere', 'Metathoracic neuromere']})
Visual_check_line_VNC.update({'R85A11':[]})
Visual_check_line_VNC.update({'SS42008':['Prothoracic neuromere', 'Mesothoracic neuromere', 'Metathoracic neuromere', 'Lower tectulum']})
Visual_check_line_VNC.update({'SS40619':[]})
Visual_check_line_VNC.update({'SS29893':['catch as SS34574']})
Visual_check_line_VNC.update({'SS29621':[]})
# Visual_check_line_VNC.update({'SS28596':['Neck tectulum']})
Visual_check_line_VNC.update({'SS51038':[]})
Visual_check_line_VNC.update({'R70H06':['catch as SS42740']}) 
Visual_check_line_VNC.update({'SS41605':['catch as SS44270']})
Visual_check_line_VNC.update({'SS31219':['Prothoracic neuromere', 'Mesothoracic neuromere', 'Metathoracic neuromere']}) #each neuron per leg neuromere
Visual_check_line_VNC.update({'MAN':['Metathoracic neuromere', 'Lower tectulum', 'Intermediate tectulum', 'Abdominal ganglion', 'Accessory mesothoracic neuromere']}) 
Visual_check_line_VNC.update({'SS36118':[]}) 
Visual_check_line_VNC.update({'SS40489':['Prothoracic neuromere', 'Mesothoracic neuromere', 'Metathoracic neuromere']}) #each neuron per leg neuromere
Visual_check_line_VNC.update({'SS45363':[]})
Visual_check_line_VNC.update({'SS45605':['Prothoracic neuromere', 'Mesothoracic neuromere', 'Metathoracic neuromere', 'Accessory mesothoracic neuromere', 'Abdominal ganglion']}) 
Visual_check_line_VNC.update({'SS52147':[]})
Visual_check_line_VNC.update({'R36G04':['Prothoracic neuromere', 'Mesothoracic neuromere', 'Metathoracic neuromere']})
Visual_check_line_VNC.update({'R30A08':['Prothoracic neuromere', 'Mesothoracic neuromere', 'Metathoracic neuromere']})
Visual_check_line_VNC.update({'R39G01':['Prothoracic neuromere', 'Mesothoracic neuromere', 'Metathoracic neuromere', 'Lower tectulum', 'Intermediate tectulum']})
Visual_check_line_VNC.update({'R69H10':[]})
Visual_check_line_VNC.update({'R87H02':['Lower tectulum', 'Abdominal ganglion', 'Haltere tectulum']})


Visual_check_line_T1T2T3={}
Visual_check_line_T1T2T3.update({'SS46233':['T1', 'T2', 'T3']})
Visual_check_line_T1T2T3.update({'R85A11':[]})
Visual_check_line_T1T2T3.update({'SS42008':['T1', 'T2', 'T3']})
Visual_check_line_T1T2T3.update({'SS40619':[]})
Visual_check_line_T1T2T3.update({'SS29893':['catch as SS34574']})
Visual_check_line_T1T2T3.update({'SS29621':[]})
# Visual_check_line_T1T2T3.update({'SS28596':['T1']})
Visual_check_line_T1T2T3.update({'SS51038':[]})
Visual_check_line_T1T2T3.update({'R70H06':['catch as SS42740']}) 
Visual_check_line_T1T2T3.update({'SS41605':['catch as SS44270']})
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









Visual_check_brain_list=[]
for i, v in Visual_check_line_brain.items():
	Visual_check_brain_list.append(i)

Visual_check_vnc_list=[]
for i, v in Visual_check_line_VNC.items():
	Visual_check_vnc_list.append(i)


if len(Visual_check_brain_list)!=len(Visual_check_vnc_list):
	print('Length of visual check lines in the brain and in the VNC are different... check again!')
	# sys.exit(0)
else:
	print('Visual check list have same length. Good to go!')

print('len Visual_check_brain_list', len(Visual_check_brain_list))
print('Visual_check_brain_list', Visual_check_brain_list)
print('Visual_check_vnc_list', Visual_check_vnc_list)










def extract_brain_ROI_name_from_VFBcsv(csv_file_dir, csv_file):

	csv_df=pd.read_csv(csv_file_dir+csv_file)

	id_list=csv_df['id'].values.tolist()
	name_list=csv_df['name'].values.tolist()


	MB_sublobe=['aL', 'bL', "a\\'L", "b\\'L", 'gL']

	abbrv_name_list=[]
	for name in name_list:
		abbrv_name = name.split(' ')[0]
		if abbrv_name in MB_sublobe:
			if abbrv_name=='aL':
				abbrv_name = 'αL'
			elif abbrv_name=='bL':
				abbrv_name = 'βL'
			elif abbrv_name=="a\\'L":
				abbrv_name = "α'L"
			elif abbrv_name=="b\\'L":
				abbrv_name = "β'L"
			elif abbrv_name=='gL':
				abbrv_name = 'γL'

		abbrv_name_list.append(abbrv_name)


	# print('id_list', id_list)
	# print('abbrv_name_list', abbrv_name_list)


	return id_list, abbrv_name_list



def extract_vnc_ROI_name_from_VNCcsv(csv_file_dir, csv_file):

	csv_df=pd.read_csv(csv_file_dir+csv_file)

	id_list=csv_df['id'].values.tolist()
	name_list=csv_df['name'].values.tolist()


	MB_sublobe=['aL', 'bL', "a\\'L", "b\\'L", 'gL']



	# print('id_list', id_list)
	# print('name_list', name_list)


	return id_list, name_list



def find_zero_px_sum_neuropils(mask_name_list, intsct_px_list_all_Gal4):

	sum_intsct_px_list_all_Gal4=np.nansum(intsct_px_list_all_Gal4, axis=0)
	print('sum_intsct_px_list_all_Gal4', sum_intsct_px_list_all_Gal4)

	nonzero_idx = np.where(sum_intsct_px_list_all_Gal4!=0)[0]
	print('nonzero_idx', nonzero_idx)

	nonzero_mask_name=np.asarray(mask_name_list)[nonzero_idx]
	print('nonzero_mask_name', nonzero_mask_name)
	print('len nonzero_mask_name', len(nonzero_mask_name))

	nonzero_intsct_px_list_all_Gal4=[]
	for i, intsct_px_list in enumerate(intsct_px_list_all_Gal4):
		nonzero_intsct_px_list_all_Gal4.append(list(np.asarray(intsct_px_list)[nonzero_idx]))
	
	print('shapen nonzero_intsct_px_list_all_Gal4', np.shape(nonzero_intsct_px_list_all_Gal4))


	return nonzero_mask_name, nonzero_intsct_px_list_all_Gal4




def convert_to_binary_mat(mat):

	print('type mat', type(mat))

	mat_cp=mat.copy()

	bin_mat=scipy.sign(mat_cp)

	print('bin_mat', bin_mat)


	return bin_mat


def make_mannual_full_mat(mat, reserved_val=0):

	##Keep value equal to reserved_val, those different val convert to 0

	print('shape mat', type(mat))

	mat_cp=mat.copy()
	mat_mannual=np.zeros(np.shape(mat_cp))


	mat_cp=np.asarray(mat_cp)
	print('mat_cp', mat_cp)

	manual_val_idxs=np.argwhere(mat_cp==reserved_val)

	print('manual_val_idxs', manual_val_idxs)

	for i, loc in enumerate(manual_val_idxs):
		mat_mannual[loc[0]][loc[1]]=1


	print('mat_mannual', mat_mannual)




	return mat_mannual
 



def make_unidentifiable_full_mat(mat, reserved_val=0):

	##Keep value equal to reserved_val, those different val convert to 0

	print('shape mat', type(mat))

	mat_cp=mat.copy()

	mat_cp=np.asarray(mat_cp)
	print('mat_cp', mat_cp)

	unIdf_idxs=np.isnan(mat_cp)

	print('unIdf_idxs', unIdf_idxs)


	mat_unIdf=1*unIdf_idxs


	print('mat_unIdf', mat_unIdf)

	return mat_unIdf



def export_summary_table(filename):

	sum_table_dic={}
	sum_table_dic.update({'Gal4_list': Gal4_list})
	sum_table_dic.update({'Innervated_neuropil_list': innvted_mask_name_list})
	sum_table_dic.update({'Innervation_per_Gal4': innvted_intesct_px_list_all_Gal4})
	sum_table_dic.update({'Innervation_per_Gal4_mannual': innvted_intesct_px_list_all_Gal4_mannual})
	sum_table_dic.update({'Innervation_per_Gal4_unidenfiable': innvted_intesct_px_list_all_Gal4_unidenfiable})
	sum_table_dic.update({'Bin_Innervation_per_Gal4': innvted_intesct_bin_list_all_Gal4})

	sum_table_dic.update({'all_Innervated_neuropil_list': mask_name_list})
	sum_table_dic.update({'all_Innervation_per_Gal4': intsct_px_list_all_Gal4})
	sum_table_dic.update({'all_Innervation_per_Gal4_mannual': intsct_px_list_all_Gal4_mannual})
	sum_table_dic.update({'all_Innervation_per_Gal4_unidenfiable': intsct_px_list_all_Gal4_unidenfiable})	

	print('Saving', filename)
	pickle.dump( sum_table_dic, open( JRC_MCFO_outDir+'/'+filename+'.p', "wb" ) ) 





	#print('innvted_mask_name_list', innvted_mask_name_list)
	csv_header=['Genotype']
	csv_header.extend(innvted_mask_name_list)
	print('csv_header', csv_header)

	csv_data=[]
	for i, Gal4 in enumerate(Gal4_list):
		data_row=[Gal4]
		data_row.extend(innvted_intesct_px_list_all_Gal4[i])
		csv_data.append(data_row)
	with open(JRC_MCFO_outDir+'/'+filename+'.csv', 'w', encoding='UTF8', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(csv_header)
		writer.writerows(csv_data)

	csv_data_mannual=[]
	for i, Gal4 in enumerate(Gal4_list):
		data_row=[Gal4]
		data_row.extend(innvted_intesct_px_list_all_Gal4_mannual[i])
		csv_data_mannual.append(data_row)
	with open(JRC_MCFO_outDir+'/'+filename+'_mannual.csv', 'w', encoding='UTF8', newline='') as f_m:
		writer = csv.writer(f_m)
		writer.writerow(csv_header)
		writer.writerows(csv_data_mannual)

	csv_data_unIdf=[]
	for i, Gal4 in enumerate(Gal4_list):
		data_row=[Gal4]
		data_row.extend(innvted_intesct_px_list_all_Gal4_unidenfiable[i])
		csv_data_unIdf.append(data_row)
	with open(JRC_MCFO_outDir+'/'+filename+'_unidenfiable.csv', 'w', encoding='UTF8', newline='') as f_unIdf:
		writer = csv.writer(f_unIdf)
		writer.writerow(csv_header)
		writer.writerows(csv_data_unIdf)


	return



## main ##


NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_public_Dir


JRC_MCFO_dir=NAS_AN_Proj_Dir + '04_mcfo_traced_singleAN_exp/MCFO/'
JRC_MCFO_outDir=NAS_AN_Proj_Dir + 'output/Fig3_S4-single_AN_innervation_mat/'
if not os.path.exists(JRC_MCFO_outDir):
	os.makedirs(JRC_MCFO_outDir)


VFB_dir= NAS_AN_Proj_Dir + '04_mcfo_traced_singleAN_exp/VFB/'
VNC_dir= NAS_AN_Proj_Dir + '04_mcfo_traced_singleAN_exp/VNC/'



for f in os.listdir(VFB_dir):
	if f.endswith('.csv'):
		VFB_csv=f

		break


for f in os.listdir(VNC_dir):
	if f.endswith('.csv'):
		VNC_csv=f

		break



print('VFB_csv', VFB_csv)
print('VNC_csv', VNC_csv)





brain_mask_id_raw_list, brain_mask_name_raw_list=extract_brain_ROI_name_from_VFBcsv(VFB_dir,VFB_csv)
vnc_mask_id_raw_list, vnc_mask_name_raw_list=extract_vnc_ROI_name_from_VNCcsv(VNC_dir,VNC_csv)

print('brain_mask_id_raw_list', brain_mask_id_raw_list)
print('brain_mask_name_raw_list', brain_mask_name_raw_list) 

print('vnc_mask_id_raw_list', vnc_mask_id_raw_list)
print('vnc_mask_name_raw_list', vnc_mask_name_raw_list) 


GNG_idx=np.where(np.asarray(brain_mask_name_raw_list)=='GNG')[0][0]
GNG_mask_id=brain_mask_id_raw_list[GNG_idx]


brain_mask_id_list=[]
brain_mask_id_raw_list.remove(GNG_mask_id)
brain_mask_id_list.extend(brain_mask_id_raw_list)
brain_mask_id_list.append(GNG_mask_id)


brain_mask_name_list=[]
brain_mask_name_raw_list.remove('GNG')
brain_mask_name_list.extend(brain_mask_name_raw_list)
brain_mask_name_list.append('GNG')


vnc_mask_id_list=vnc_mask_id_raw_list
vnc_mask_name_list=vnc_mask_name_raw_list


print('brain_mask_id_list', brain_mask_id_list)
print('brain_mask_name_list', brain_mask_name_list) 

print('vnc_mask_id_list', vnc_mask_id_list)
print('vnc_mask_name_list', vnc_mask_name_list) 





print('Importing mask image stacks ...')
nrrd_brain_mask_stacks=[]
for mask_id in brain_mask_id_list:
	nrrd_filename=mask_id+'_JRC2018uni20.nrrd'
	brain_region_mask = general_utils.read_nrrd(VFB_dir, nrrd_filename)
	brain_region_mask=np.transpose(brain_region_mask, (2,1,0))	

	nrrd_brain_mask_stacks.append(brain_region_mask)


nrrd_vnc_mask_stacks=[]
for mask_id in vnc_mask_id_list:
	nrrd_filename=mask_id+'.nrrd'
	vnc_region_mask = general_utils.read_nrrd(VNC_dir, nrrd_filename)
	vnc_region_mask=np.transpose(vnc_region_mask, (2,1,0))	

	nrrd_vnc_mask_stacks.append(vnc_region_mask)

	


T1_vnc_name='T1_VNC.nrrd'
T2_vnc_name='T2_VNC.nrrd'
T3_vnc_name='T3_VNC.nrrd'
T1_vnc_mask = general_utils.read_nrrd(VNC_dir, T1_vnc_name)
T2_vnc_mask = general_utils.read_nrrd(VNC_dir, T2_vnc_name)
T3_vnc_mask = general_utils.read_nrrd(VNC_dir, T3_vnc_name)

T1_vnc_mask=np.transpose(T1_vnc_mask, (2,1,0))	
T2_vnc_mask=np.transpose(T2_vnc_mask, (2,1,0))	
T3_vnc_mask=np.transpose(T3_vnc_mask, (2,1,0))	

nrrd_T1T2T3_mask_stacks=[
T1_vnc_mask,
T2_vnc_mask,
T3_vnc_mask
]

T1T2T3_mask_name_list=['T1', 'T2', 'T3']



print('shape nrrd_brain_mask_stacks', np.shape(nrrd_brain_mask_stacks))
print('shape nrrd_vnc_mask_stacks', np.shape(nrrd_vnc_mask_stacks))
print('shape nrrd_T1T2T3_mask_stacks', np.shape(nrrd_T1T2T3_mask_stacks))





# Gal4_list=[]
# for Ga4_file in traced_neurites_filelist:
# 	Gal4_name = Ga4_file.split('/')[7][4:]
# 	Gal4_list.append(Gal4_name)

# print('Gal4_list', Gal4_list)
# print('len Gal4_list', len(Gal4_list))



manual_given=0.5 #use non-interger because those innervated area are integer
unidentifiable=np.nan




data_types=[
(brain_neurites_filelist, 'Innervation_px_count_visualCount_distalenurites', 'brain', Visual_check_brain_list, Visual_check_line_brain),
(VNC_neurites_filelist, 'Innervation_px_count_visualCount_vnc', 'vnc', Visual_check_vnc_list, Visual_check_line_VNC),
(VNC_neurites_filelist, 'Innervation_px_count_visualCount_T1T2T3', 'T1T2T3', Visual_check_vnc_list, Visual_check_line_T1T2T3),

]



for traced_neurites_filelist, output_filename, nervous_system, Visual_check_list, Visual_check_line in data_types:


### !!! Choose whcih type of neurites and interested neuropils to analyze!!!!

# traced_neurites_filelist=brain_neurites_filelist
# #output_filename = 'Innervation_px_count_distalenurites'
# output_filename = 'Innervation_px_count_visualCount_distalenurites'
# nervous_system='brain'
# Visual_check_list=Visual_check_brain_list
# Visual_check_line=Visual_check_line_brain



# traced_neurites_filelist=VNC_neurites_filelist
# output_filename = 'Innervation_px_count_visualCount_vnc'
# nervous_system='vnc'
# Visual_check_list=Visual_check_vnc_list
# Visual_check_line=Visual_check_line_VNC


# traced_neurites_filelist=VNC_neurites_filelist
# output_filename = 'Innervation_px_count_visualCount_T1T2T3'
# nervous_system='T1T2T3'
# Visual_check_list=Visual_check_vnc_list
# Visual_check_line=Visual_check_line_T1T2T3

###################################################################






	if nervous_system=='brain':

		nrrd_mask_stacks=nrrd_brain_mask_stacks
		mask_name_list=brain_mask_name_list

		print('mask_name_list', mask_name_list)

	elif nervous_system=='vnc':

		nrrd_mask_stacks=nrrd_vnc_mask_stacks
		mask_name_list=vnc_mask_name_list


	elif nervous_system=='T1T2T3':

		nrrd_mask_stacks=nrrd_T1T2T3_mask_stacks
		mask_name_list=T1T2T3_mask_name_list






	Gal4_list=[]
	intsct_px_list_all_Gal4=[]



	for traced_file_dir in traced_neurites_filelist:

		if len(traced_file_dir)>9:
			Gal4_name = traced_file_dir.split('/')[7][4:]
		else:
			Gal4_name=traced_file_dir
		Gal4_list.append(Gal4_name)

		print('Gal4_name', Gal4_name)
		print('traced_file_dir', traced_file_dir)




		intsct_px_list=[]

		if not Gal4_name in Visual_check_list:


			traced_neurites_stack = io.imread(traced_file_dir)
			traced_neurites_stack = np.asarray(traced_neurites_stack)
			#print('shape traced_neurites_stack', np.shape(traced_neurites_stack))

			
			traced_neurites_stack[traced_neurites_stack>0]=1
			# print('traced_neurites_stack', traced_neurites_stack)

			# plt.imshow(traced_neurites_stack[100])
			# plt.savefig(JRC_MCFO_outDir+'test_frame_bin.tif')
			# plt.clf()


			for i, brain_region_mask in enumerate(nrrd_mask_stacks):

				print('mask_name_list', mask_name_list[i])


				intrsct_stacks = traced_neurites_stack*brain_region_mask
				#print('shape intrsct_stacks', np.shape(intrsct_stacks))

				intrsct_px_count = np.count_nonzero(intrsct_stacks>0)
				print('intrsct_px_count', intrsct_px_count)


				intsct_px_list.append(intrsct_px_count)


			print('intsct_px_list', intsct_px_list)
			intsct_px_list_all_Gal4.append(intsct_px_list)

		elif Gal4_name=='R70H06':
			if nervous_system=='brain':
				traced_neurites_stack = io.imread(NAS_AN_Proj_Dir+'/04_mcfo_traced_singleAN_exp/MCFO/JRC_SS42740/JRC_SS42740_20180907_21_C3_REG_UNISEX_20x_HR_m_VNC-V5-trace/JRC_SS42740_20180907_21_C3_REG_UNISEX_VNC_m_Brain-distalneuritesfilled.tif')
			elif nervous_system=='vnc' or nervous_system=='T1T2T3':
				traced_neurites_stack = io.imread(NAS_AN_Proj_Dir+'/04_mcfo_traced_singleAN_exp/MCFO/JRC_SS42740/JRC_SS42740_20180907_21_C3_REG_UNISEX_20x_HR_m_VNC-V5-trace/JRC_SS42740_20180907_21_C3_REG_UNISEX_VNC_m_VNC_filt.tif')

			traced_neurites_stack = np.asarray(traced_neurites_stack)
			traced_neurites_stack[traced_neurites_stack>0]=1

			for i, brain_region_mask in enumerate(nrrd_mask_stacks):

				#print('mask_name_list', mask_name_list[i])


				intrsct_stacks = traced_neurites_stack*brain_region_mask
				#print('shape intrsct_stacks', np.shape(intrsct_stacks))

				intrsct_px_count = np.count_nonzero(intrsct_stacks>0)
				#print('intrsct_px_count', intrsct_px_count)


				intsct_px_list.append(intrsct_px_count)


			print('intsct_px_list', intsct_px_list)
			intsct_px_list_all_Gal4.append(intsct_px_list)


		elif Gal4_name=='SS29893':
			if nervous_system=='brain':
				traced_neurites_stack = io.imread(NAS_AN_Proj_Dir+'/04_mcfo_traced_singleAN_exp/MCFO/JRC_SS34574/JRC_SS34574_20200904_20_F6_REG_UNISEX_VNC_m_VNC-FLAG/JRC_SS34574_20200904_20_F6_REG_UNISEX_VNC_m_Brain-distalneuritefilled.tif')
			elif nervous_system=='vnc' or nervous_system=='T1T2T3':
				traced_neurites_stack = io.imread(NAS_AN_Proj_Dir+'/04_mcfo_traced_singleAN_exp/MCFO/JRC_SS34574/JRC_SS34574_20200904_20_F6_REG_UNISEX_VNC_m_VNC-FLAG/JRC_SS34574_20200904_20_F6_REG_UNISEX_VNC_m_VNC-filt.tif')

			traced_neurites_stack = np.asarray(traced_neurites_stack)
			traced_neurites_stack[traced_neurites_stack>0]=1

			for i, brain_region_mask in enumerate(nrrd_mask_stacks):

				print('mask_name_list', mask_name_list[i])


				intrsct_stacks = traced_neurites_stack*brain_region_mask
				#print('shape intrsct_stacks', np.shape(intrsct_stacks))

				intrsct_px_count = np.count_nonzero(intrsct_stacks>0)
				print('intrsct_px_count', intrsct_px_count)


				intsct_px_list.append(intrsct_px_count)


			print('intsct_px_list', intsct_px_list)
			intsct_px_list_all_Gal4.append(intsct_px_list)


		elif Gal4_name=='SS41605':
			if nervous_system=='brain':
				traced_neurites_stack = io.imread(NAS_AN_Proj_Dir+'/04_mcfo_traced_singleAN_exp/MCFO/JRC_SS44270/JRC_SS44270_20180706_20_C4__REG_UNISEX_20x_HR_m_Brain/JRC_SS44270_20180706_20_C4__REG_UNISEX_20x_HR_m_Brain-distalneuritesfilled.tif')
			elif nervous_system=='vnc' or nervous_system=='T1T2T3':
				traced_neurites_stack = io.imread(NAS_AN_Proj_Dir+'/04_mcfo_traced_singleAN_exp/MCFO/JRC_SS44270/JRC_SS44270_20180706_20_C4__REG_UNISEX_20x_HR_m_Brain/JRC_SS44270_20180706_20_C4__REG_UNISEX_VNC_m_VNC-filled.tif')


			traced_neurites_stack = np.asarray(traced_neurites_stack)
			traced_neurites_stack[traced_neurites_stack>0]=1

			for i, brain_region_mask in enumerate(nrrd_mask_stacks):

				print('mask_name_list', mask_name_list[i])


				intrsct_stacks = traced_neurites_stack*brain_region_mask
				#print('shape intrsct_stacks', np.shape(intrsct_stacks))

				intrsct_px_count = np.count_nonzero(intrsct_stacks>0)
				print('intrsct_px_count', intrsct_px_count)


				intsct_px_list.append(intrsct_px_count)


			print('intsct_px_list', intsct_px_list)
			intsct_px_list_all_Gal4.append(intsct_px_list)


		else:


			mask_name_list=np.array(mask_name_list)

			visual_check_regions=Visual_check_line[Gal4_name]

			## manual given innervation
			if len(visual_check_regions)!=0:
				print('visual_check_regions', visual_check_regions)

				v_regions_idx = np.where(np.isin(mask_name_list,visual_check_regions))[0]

				print('v_regions_idx', v_regions_idx)
				print('mask_name_list[v_regions_idx]', mask_name_list[v_regions_idx])

				for i, brain_region_mask in enumerate(nrrd_mask_stacks):
					if i in v_regions_idx:
						# intsct_px_list.append(True)
						intsct_px_list.append(manual_given)
					else:
						intsct_px_list.append(0)

				intsct_px_list_all_Gal4.append(intsct_px_list)

			##Can't even give innervation = unidentifiable lines
			else:
				for i, brain_region_mask in enumerate(nrrd_mask_stacks):
					intsct_px_list.append(unidentifiable)
				intsct_px_list_all_Gal4.append(intsct_px_list)



	innvted_mask_name_list, innvted_intesct_px_list_all_Gal4=find_zero_px_sum_neuropils(mask_name_list, intsct_px_list_all_Gal4)
	print('innvted_intesct_px_list_all_Gal4', innvted_intesct_px_list_all_Gal4)

	innvted_intesct_bin_list_all_Gal4 = convert_to_binary_mat(innvted_intesct_px_list_all_Gal4)


	innvted_intesct_px_list_all_Gal4_mannual=make_mannual_full_mat(innvted_intesct_px_list_all_Gal4, reserved_val=manual_given)
	innvted_intesct_px_list_all_Gal4_unidenfiable=make_unidentifiable_full_mat(innvted_intesct_px_list_all_Gal4, reserved_val=unidentifiable)

	intsct_px_list_all_Gal4_mannual=make_mannual_full_mat(intsct_px_list_all_Gal4, reserved_val=manual_given)
	intsct_px_list_all_Gal4_unidenfiable=make_unidentifiable_full_mat(intsct_px_list_all_Gal4, reserved_val=unidentifiable)



	print('shape Gal4_list', np.shape(Gal4_list))
	print('shape innvted_mask_name_list', np.shape(innvted_mask_name_list))
	print('innvted_mask_name_list', innvted_mask_name_list)
	# print('shape intsct_px_list_all_Gal4', np.shape(intsct_px_list_all_Gal4))
	# print('intsct_px_list_all_Gal4[0]', intsct_px_list_all_Gal4[0])
	print('shape innvted_intesct_px_list_all_Gal4', np.shape(innvted_intesct_px_list_all_Gal4))
	print('shape innvted_intesct_bin_list_all_Gal4', np.shape(innvted_intesct_bin_list_all_Gal4))



	export_summary_table(output_filename)


	# ##Plot all neuropils
	# # plot_utils.plot_matrix(Gal4_list, mask_name_list, intsct_px_list_all_Gal4, savedir=JRC_MCFO_outDir, title=output_filename, PlotMethod='other', unit='px count', cmap='Blues')

	# #Plot neuropils with innervation only
	# plot_utils.plot_matrix(Gal4_list, innvted_mask_name_list, innvted_intesct_px_list_all_Gal4, savedir=JRC_MCFO_outDir, title='Nonzero_'+output_filename, PlotMethod='other', unit='px count', cmap='Blues')









		






















