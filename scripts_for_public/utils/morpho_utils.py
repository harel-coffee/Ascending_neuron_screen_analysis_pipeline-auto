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








	




