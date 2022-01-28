import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys



def find_nearest_nice_integer_of_postive_number(number):

	if np.floor(number/10) > 0:
		nearest_nice_integer=int(np.floor(number/10)*10)
	else:
		nearest_nice_integer=int(np.floor(number))

	return nearest_nice_integer


def calc_scale_bar_um_to_px(pixelSize=0.5, scale_bar_length_um=10):

	scale_bar_px=scale_bar_length_um/pixelSize

	# print('scale_bar_length_um', scale_bar_length_um)
	# print('scale_bar_px', scale_bar_px)

	return scale_bar_px



def Plot_traces(series_set=None, savepath=None):

	if series_set==None:
		print('No data series to plot ...')
		pass

	else:
		print('Plotting '+savepath)

		keys_series_set=list(series_set.keys())
		values_series_set=list(series_set.values())

		fig=plt.figure(facecolor='black', figsize=(25, 10), dpi=200)
		for i in range(0, len(series_set)):
			plt.subplot(int(str(len(series_set))+'1'+str(i+1)))
			plt.plot(values_series_set[i], linewidth=1)
			plt.title(keys_series_set[i])
		plt.tight_layout()
		plt.savefig(savepath)
		plt.clf()
		plt.close(fig)


	return



def find_aligned_pos_of_panelLabel(ref_xy_span=[2,2], target_xy_span=[1,1], ref_position=0.9, direction='vertical'):

	# This dunction looks is for finding the position of text labels that put the text in the same place of panels with different size. 
	# It is aiming for the text alignment across different panels. 
	# ref_panel_span should be smaller than target_panel_span. Better use the smallest panel as the ref_panel_span. 



	if direction == 'vertical':

		ref_h = ref_xy_span[1]
		targ_h = target_xy_span[1]

		if targ_h>ref_h:

			ratio_h=targ_h/ref_h

			target_position=ref_position/ratio_h

		else:
			print('Target panel span should > Reference panel span.')
			sys.exit(0)


	elif direction == 'horizontal':

		ref_w = ref_xy_span[0]
		targ_w = target_xy_span[0]

		if targ_w>ref_w:

			ratio_w=targ_w/ref_w

			target_position=ref_position/ratio_w

		else:
			print('Target panel span should > Reference panel span.')
			sys.exit(0)

	#print('target_position', target_position)

	return target_position












