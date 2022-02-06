import pandas as pd
import pickle as pickle
import sys
import os
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from skimage import io

import utils.list_inputFiles as list_inputFiles
import utils.general_utils as general_utils
import utils.list_behavior as list_behavior
import utils.plot_utils as plot_utils
import utils.plot_setting as plot_setting



leg_order_Victor = list_behavior.leg_order_Victor

leg_order_ori = list_behavior.leg_order_Florian

joint_order = list_behavior.joint_order
joint_order_rev = list_behavior.joint_order_rev



def import_jointPos_beh_dic(jointPos_beh_dic):

	if os.path.exists(jointPos_beh_dic):
		DicData = pickle.load(open( jointPos_beh_dic, "rb" ))

	return DicData





def convert_jointBasedDic_to_frameBased_pos3dDic(jointPos3d_jointBased_dic):

	## This structure of the dictionary is for plotting. The order of legs and joints is determined by the order list.

	jointPos3d_frameBased_dic={}
	for frame_ID, j in enumerate(jointPos3d_jointBased_dic['RH_leg Claw x']):

		Alllegs_pos3d_per_frame=[]

		for leg_idx, leg in enumerate(leg_order_ori):
			Alllegs_pos3d_per_frame.append([])
			x=[]
			y=[]
			z=[]
			for joint in joint_order_rev: 

				jointID=leg+' '+joint
				
				x.append(jointPos3d_jointBased_dic[jointID+' '+'x'][frame_ID])
				y.append(jointPos3d_jointBased_dic[jointID+' '+'y'][frame_ID])
				z.append(jointPos3d_jointBased_dic[jointID+' '+'z'][frame_ID])
				
			Alllegs_pos3d_per_frame[leg_idx].append(x)
			Alllegs_pos3d_per_frame[leg_idx].append(y)
			Alllegs_pos3d_per_frame[leg_idx].append(z)

		#print('shape Alllegs_pos3d_per_frame', np.shape(Alllegs_pos3d_per_frame)) 

		jointPos3d_frameBased_dic.update({'frame'+str(frame_ID): Alllegs_pos3d_per_frame})



	return jointPos3d_frameBased_dic



def convert_frameBasedDic_to_list(jointPos3d_frameBased_dic):


	jointPos3d_frameBased_list=[]
	for key, values in jointPos3d_frameBased_dic.items():
		# print(key)
		# print('shape jointPos3d_frameBased_dic[key]', np.shape(jointPos3d_frameBased_dic[key]))
		jointPos3d_frameBased_list.append(jointPos3d_frameBased_dic[key])


	#print(np.shape(jointPos3d_frameBased_list))


	return jointPos3d_frameBased_list



	



def plot_overlaplegs_from_pos3d(joint_pos3d_frameBased_list, save_dir, filename, bsl=0.3, fps=30, leg_order=['RH_leg','LH_leg','RM_leg','LM_leg','RF_leg','LF_leg'], plane='xz', plotting_order='frame'):

	## plotting_order: the order for plotting, either 'frame' or 'leg'. If leg order, front leg will be the top and the hind leg will be the bottom.

	print('shape joint_pos3d_frameBased_list', np.shape(joint_pos3d_frameBased_list))

	if plotting_order=='frame':
		first_order_list=joint_pos3d_frameBased_list

	elif plotting_order=='leg':
		#convert to joint based structure, meaning each joint contains pos3d of all frames as a 6*n list.
		print('shape joint_pos3d_frameBased_list', np.shape(joint_pos3d_frameBased_list))
		joint_pos3d_jointBased_list=np.transpose(joint_pos3d_frameBased_list, (1,0,2,3))
		print('shape joint_pos3d_jointBased_list', np.shape(joint_pos3d_jointBased_list))
		if plane=='xz left':
			first_order_list=[]
			first_order_list.append(joint_pos3d_jointBased_list[leg_order_ori.index(leg_order[0])])
			first_order_list.append(joint_pos3d_jointBased_list[leg_order_ori.index(leg_order[1])])
			first_order_list.append(joint_pos3d_jointBased_list[leg_order_ori.index(leg_order[2])])
			# print(leg_order[0],leg_order_ori.index(leg_order[0]))
			# print(leg_order[1],leg_order_ori.index(leg_order[1]))
			# print(leg_order[2],leg_order_ori.index(leg_order[2]))
		elif plane=='xz right':
			first_order_list=[]
			first_order_list.append(joint_pos3d_jointBased_list[leg_order_ori.index(leg_order[0])])
			first_order_list.append(joint_pos3d_jointBased_list[leg_order_ori.index(leg_order[1])])
			first_order_list.append(joint_pos3d_jointBased_list[leg_order_ori.index(leg_order[2])])
			# print(leg_order[0],leg_order_ori.index(leg_order[0]))
			# print(leg_order[1],leg_order_ori.index(leg_order[1]))
			# print(leg_order[2],leg_order_ori.index(leg_order[2]))
		else:
			first_order_list=joint_pos3d_jointBased_list



	frame_begin=990
	#frame_end=len(joint_pos3d_frameBased_list)
	frame_end=1000


	fig_3d = plt.figure()

	if plane is not '':
		print('Plot', plane, 'plane')
	else:
		print('Plot 3D')
	
	lim_x = (-2.5,2.5)
	lim_y = (-2.7,2.7)
	lim_z = (-2,1.5)

	ax_3d = fig_3d.add_subplot(111, projection='3d')
	ax_3d.set_xlabel('x mm')
	ax_3d.set_ylabel('y mm')
	ax_3d.set_zlabel('z mm')

	ax_3d.set_xlim(lim_x)
	ax_3d.set_ylim(lim_y)
	ax_3d.set_zlim(lim_z)

	ax_3d.grid(True)
	ax_3d.view_init(40, -45)

	if not plane=='':
		if plane=='xy':
			view_2d = plt.figure(figsize=(10,8))
		elif plane=='xz left':
			lim_x = (-2.5,2.5)
			view_2d = plt.figure(figsize=(10,4))
		elif plane=='xz right':	
			lim_x = (2.5,-2.5)		
			view_2d = plt.figure(figsize=(10,4))
		elif plane=='yz':
			view_2d = plt.figure(figsize=(10,4))

		ax_2d = view_2d.add_subplot(111)
		ax_2d.set_xlabel(plane[0])
		ax_2d.set_ylabel(plane[1])
		ax_2d.grid(True)

	# for frame_idx, j_pos_per_leg in enumerate(joint_pos3d_frameBased_list):
	for first_order_idx, first_order_item in enumerate(first_order_list):

		#print('shape first_order_item', np.shape(first_order_item))

		for second_order_idx, second_order_item in enumerate(first_order_item):

			#print('second_order_idx', second_order_idx)

			#print('shape second_order_item', np.shape(second_order_item))

			if plotting_order=='frame':
				Leg_ID = leg_order[second_order_idx]
				leg_color=plot_setting.leg_colors[Leg_ID]
			elif plotting_order=='leg':
				Leg_ID = leg_order[first_order_idx]
				#print(first_order_idx, Leg_ID)
				leg_color=plot_setting.leg_colors[Leg_ID]				

			x=second_order_item[0]
			y=second_order_item[1]
			z=second_order_item[2]

			print(x,y,z)



			if plane == 'xy':
				ax_2d.set_xlim(lim_x)
				ax_2d.set_ylim(lim_y)
				ax_2d.plot(x, y, '-', color = leg_color)

			elif plane == 'xz left':
				ax_2d.set_xlim(lim_x)
				ax_2d.set_ylim(lim_z)
				ax_2d.plot(x, z, '-', color =leg_color)

			elif plane == 'xz right':
				ax_2d.set_xlim(lim_x)
				ax_2d.set_ylim(lim_z)
				ax_2d.plot(x, z, '-', color =leg_color)

			elif plane == 'yz':
				ax_2d.set_xlim(lim_y)
				ax_2d.set_ylim(lim_z)
				ax_2d.plot(y, z, '-', color = leg_color)

			else:
				ax_3d.plot(x, y, z, '-', color=leg_color, alpha=1)				



	if plane is not '':
		view_2d.savefig(save_dir+filename)
		view_2d.clf()
		plt.close(view_2d)

	else:
		fig_3d.savefig(save_dir+filename)
		#fig_3d.savefig(save_dir+'pose3d'+str(frame_idx)+'.png')
		fig_3d.clf()
		plt.close(fig_3d)



	return



