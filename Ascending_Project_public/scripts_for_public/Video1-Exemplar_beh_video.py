import sys
import os
import cv2
from skimage import io
from multiprocessing import Pool
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
plt.switch_backend('agg')
import numpy as np

import video_utils.sync_utils as sync_utils 
import video_utils.plot_setting as plot_setting
import video_utils.plot_utils as plot_utils
import video_utils.general_utils as general_utils 
import video_utils.plot_jpos3d_utils as plot_jpos3d_utils 


import video_utils.list_behavior as list_behavior
leg_order=list_behavior.leg_order_Florian
print('leg_order', leg_order)
leg_order_plot=list_behavior.leg_order_Victor
leg_order_plot    =['RH_leg', 'LH_leg', 'RM_leg', 'LM_leg', 'RF_leg', 'LF_leg']
leg_order_plot_num=[ 0,         1,        2,        3,        4,        5.    ]
print('leg_order_plot', leg_order_plot)






def trim_jangle_frameBased_list(jangle_frameBased_list, start_idx, end_idx):

	trimmed_jangle_frameBased_list=[]
	for i, jangle in enumerate(jangle_frameBased_list):
		print('shape jangle', np.shape(jangle))
		trimmed_jangle_frameBased_list.append(jangle[start_idx:end_idx])



	return trimmed_jangle_frameBased_list


def make_pool_iter(vid_len_per_source, total_start_idx):

	iter_list=[]
	for i in range(0, vid_len_per_source):
		
		iter_list.append((i, total_start_idx))
		total_start_idx+=1

	return iter_list, total_start_idx



def wrap_args_func(args):

	return exemp_beh_video_frame(*args)


def exemp_beh_video_frame(currentVidIdx, video_frame_idx):

	currentTracePntIdx=currentVidIdx*50
	
	currentBeh=video_beh_labels[currentVidIdx]
	
	print('Exemplar video total frames =', len(video_beh_labels), ', Current_frame # =', currentVidIdx, 'current beh=', currentBeh)



	Behlabels_origin=[18, 0]
	Behlabels_xy_span=[int(730*3), 50]

	Cam0_origin=[0,Behlabels_origin[1]+Behlabels_xy_span[1]]
	Cam0_xy_span=[730,365]

	Cam6_origin=[Cam0_origin[0]+Cam0_xy_span[0], Cam0_origin[1]]
	Cam6_xy_span=[730,365]

	Cam5_origin=[Cam6_origin[0]+Cam6_xy_span[0], Cam0_origin[1]]
	Cam5_xy_span=[730,365]

	Cam1_origin=[Cam0_origin[0], Cam0_origin[1]+Cam0_xy_span[1]]
	Cam1_xy_span=[730,365]

	Cam2_origin=[Cam1_origin[0]+Cam1_xy_span[0], Cam1_origin[1]]
	Cam2_xy_span=[730,365]

	Cam3_origin=[Cam2_origin[0]+Cam2_xy_span[0], Cam1_origin[1]]
	Cam3_xy_span=[730,365]

	pose3d_origin=[Cam0_origin[0], Cam1_origin[1]+Cam1_xy_span[1]+50]
	pose3d_xy_span=[1095, 1045]

	trace_spacer_xy_span=[0,25]

	AP_origin=[int(730*3/2)+190, pose3d_origin[1]+trace_spacer_xy_span[1]]
	AP_xy_span=[900, 219-trace_spacer_xy_span[1]]

	ML_origin=[int(730*3/2)+190, AP_origin[1]+AP_xy_span[1]+trace_spacer_xy_span[1]]
	ML_xy_span=[900, 219-trace_spacer_xy_span[1]]

	Yaw_origin=[int(730*3/2)+190, ML_origin[1]+ML_xy_span[1]+trace_spacer_xy_span[1]]
	Yaw_xy_span=[900, 219-trace_spacer_xy_span[1]]

	PE_origin=[int(730*3/2)+190, Yaw_origin[1]+Yaw_xy_span[1]+trace_spacer_xy_span[1]]
	PE_xy_span=[900, 219-trace_spacer_xy_span[1]]

	co2_origin=[int(730*3/2)+190, PE_origin[1]+PE_xy_span[1]+trace_spacer_xy_span[1]]
	co2_xy_span=[900, 219-trace_spacer_xy_span[1]]


	fig_span = [co2_origin[0]+co2_xy_span[0], co2_origin[1]+co2_xy_span[1]]


	Frame_y=7.7 #inch 858
	Frame_x=9 #inch 2173

	fig = plt.figure(facecolor='k', figsize=(Frame_x, Frame_y), dpi=300, constrained_layout=True)
	fig.subplots_adjust(left=0.0435, right = 0.974, top = 0.945, bottom = 0.0458, wspace = 1000, hspace = 1000)
	normA = matplotlib.colors.Normalize(vmin=0.0,vmax=255.0)

	axBehlabels = plt.subplot2grid((fig_span[1],fig_span[0]),(Behlabels_origin[1], Behlabels_origin[0]),rowspan=Behlabels_xy_span[1],colspan=Behlabels_xy_span[0])
	axBehlabels.spines['bottom'].set_visible(False)
	axBehlabels.spines['top'].set_visible(False)
	axBehlabels.spines['right'].set_visible(False)
	axBehlabels.spines['left'].set_visible(False)
	axBehlabels.get_xaxis().set_visible(False)
	axBehlabels.get_yaxis().set_visible(False)

	non_beh_alpha=0.2


	alpha_r=non_beh_alpha
	alpha_fw=non_beh_alpha
	alpha_bw=non_beh_alpha
	alpha_eg=non_beh_alpha
	alpha_ag=non_beh_alpha
	alpha_flg=non_beh_alpha
	alpha_hlg=non_beh_alpha
	alpha_abdg=non_beh_alpha
	alpha_push=non_beh_alpha
	alpha_per=non_beh_alpha
	alpha_CO2=non_beh_alpha

	fw_font_color='k'
	flg_font_color='k'

	if currentBeh=='r':
		alpha_r=1
	elif currentBeh=='fw':
		alpha_fw=1
		fw_font_color='w'
	elif currentBeh=='bw':
		alpha_bw=1
	elif currentBeh=='eg':
		alpha_eg=1
	elif currentBeh=='ag':
		alpha_ag=1
	elif currentBeh=='flg':
		alpha_flg=1
		flg_font_color='w'
	elif currentBeh=='hlg':
		alpha_hlg=1
	elif currentBeh=='abdg':
		alpha_abdg=1
	elif currentBeh=='push':
		alpha_push=1
	elif currentBeh=='per':
		alpha_per=1
	elif currentBeh=='CO2':
		alpha_CO2=1

	beh_box_fontsize=6

	Rest=plt.text(0.006, 0.39, 'Resting', transform=axBehlabels.transAxes, color='k',size=beh_box_fontsize, alpha=1, fontweight='bold')
	Rest.set_bbox(dict(facecolor=plot_setting.rest_color, edgecolor='none', alpha=alpha_r))
	F_walk=plt.text(0.0628,0.39, 'Forward walking', transform=axBehlabels.transAxes, color=fw_font_color,size=beh_box_fontsize, alpha=1, fontweight='bold')
	F_walk.set_bbox(dict(facecolor=plot_setting.FW_color, edgecolor='none', alpha=alpha_fw))
	B_walk=plt.text(0.170,0.39, 'Backward walking', transform=axBehlabels.transAxes, color='k',size=beh_box_fontsize, alpha=1, fontweight='bold')
	B_walk.set_bbox(dict(facecolor=plot_setting.BW_color, edgecolor='none', alpha=alpha_bw))
	E_groom=plt.text(0.2865,0.39, 'Eye grooming', transform=axBehlabels.transAxes, color='k',size=beh_box_fontsize, alpha=1, fontweight='bold')
	E_groom.set_bbox(dict(facecolor=plot_setting.E_groom_color, edgecolor='none', alpha=alpha_eg))
	A_groom=plt.text(0.3783,0.39, 'Antennal grooming', transform=axBehlabels.transAxes, color='k',size=beh_box_fontsize, alpha=1, fontweight='bold')
	A_groom.set_bbox(dict(facecolor=plot_setting.A_groom_color, edgecolor='none', alpha=alpha_ag))
	FL_groom=plt.text(0.501,0.39, 'Foreleg rubbing', transform=axBehlabels.transAxes, color=flg_font_color,size=beh_box_fontsize, alpha=1, fontweight='bold')
	FL_groom.set_bbox(dict(facecolor=plot_setting.FL_groom_color, edgecolor='none', alpha=alpha_flg))
	HL_groom=plt.text(0.605,0.39, 'Hindleg rubbing', transform=axBehlabels.transAxes, color='k',size=beh_box_fontsize, alpha=1, fontweight='bold')
	HL_groom.set_bbox(dict(facecolor=plot_setting.HL_groom_color, edgecolor='none', alpha=alpha_hlg))
	Abd_groom=plt.text(0.7097,0.39, 'Abdomen grooming', transform=axBehlabels.transAxes, color='k',size=beh_box_fontsize, alpha=1, fontweight='bold')
	Abd_groom.set_bbox(dict(facecolor=plot_setting.Abd_groom_color, edgecolor='none', alpha=alpha_abdg))
	Push=plt.text(0.8345,0.39, 'Pushing', transform=axBehlabels.transAxes, color='k',size=beh_box_fontsize, alpha=1, fontweight='bold')
	Push.set_bbox(dict(facecolor=plot_setting.Push_color, edgecolor='none', alpha=alpha_push))
	PER=plt.text(0.8936,0.39, 'PE', transform=axBehlabels.transAxes, color='k',size=beh_box_fontsize, alpha=1, fontweight='bold')
	PER.set_bbox(dict(facecolor=plot_setting.PER_color, edgecolor='none', alpha=alpha_per))		
	Puff=plt.text(0.9217,0.39, 'Puff', transform=axBehlabels.transAxes, color='k',size=beh_box_fontsize, alpha=1, fontweight='bold')
	Puff.set_bbox(dict(facecolor='w', edgecolor='none', alpha=alpha_CO2))		


	Cam0_img=video_frames_Cam0[currentVidIdx]
	axCam0 = plt.subplot2grid((fig_span[1],fig_span[0]),(Cam0_origin[1], Cam0_origin[0]),rowspan=Cam0_xy_span[1],colspan=Cam0_xy_span[0])
	axCam0.spines['bottom'].set_visible(False)
	axCam0.spines['top'].set_visible(False)
	axCam0.spines['right'].set_visible(False)
	axCam0.spines['left'].set_visible(False)
	axCam0.get_xaxis().set_visible(False)
	axCam0.get_yaxis().set_visible(False)
	#axCam0.set_axis_off()
	axCam0.imshow(Cam0_img, origin='upper',norm=normA, aspect = 'equal')

	Cam6_img=video_frames_Cam6[currentVidIdx]
	axCam6 = plt.subplot2grid((fig_span[1],fig_span[0]),(Cam6_origin[1], Cam6_origin[0]),rowspan=Cam6_xy_span[1],colspan=Cam6_xy_span[0])
	axCam6.spines['bottom'].set_visible(False)
	axCam6.spines['top'].set_visible(False)
	axCam6.spines['right'].set_visible(False)
	axCam6.spines['left'].set_visible(False)
	axCam6.get_xaxis().set_visible(False)
	axCam6.get_yaxis().set_visible(False)
	#axCam6.set_axis_off()
	axCam6.imshow(Cam6_img, origin='upper',norm=normA, aspect = 'equal')

	Cam5_img=video_frames_Cam5[currentVidIdx]
	axCam5 = plt.subplot2grid((fig_span[1],fig_span[0]),(Cam5_origin[1], Cam5_origin[0]),rowspan=Cam5_xy_span[1],colspan=Cam5_xy_span[0])
	axCam5.spines['bottom'].set_visible(False)
	axCam5.spines['top'].set_visible(False)
	axCam5.spines['right'].set_visible(False)
	axCam5.spines['left'].set_visible(False)
	axCam5.get_xaxis().set_visible(False)
	axCam5.get_yaxis().set_visible(False)
	#axConfImg.set_axis_off()
	axCam5.imshow(Cam5_img, origin='upper',norm=normA, aspect = 'equal')

	Cam1_img=video_frames_Cam1[currentVidIdx]
	axCam1 = plt.subplot2grid((fig_span[1],fig_span[0]),(Cam1_origin[1], Cam1_origin[0]),rowspan=Cam1_xy_span[1],colspan=Cam1_xy_span[0])
	axCam1.spines['bottom'].set_visible(False)
	axCam1.spines['top'].set_visible(False)
	axCam1.spines['right'].set_visible(False)
	axCam1.spines['left'].set_visible(False)
	axCam1.get_xaxis().set_visible(False)
	axCam1.get_yaxis().set_visible(False)
	#axCam1.set_axis_off()
	axCam1.imshow(Cam1_img, origin='upper',norm=normA, aspect = 'equal')

	Cam2_img=video_frames_Cam2[currentVidIdx]
	axCam2 = plt.subplot2grid((fig_span[1],fig_span[0]),(Cam2_origin[1], Cam2_origin[0]),rowspan=Cam2_xy_span[1],colspan=Cam2_xy_span[0])
	axCam2.spines['bottom'].set_visible(False)
	axCam2.spines['top'].set_visible(False)
	axCam2.spines['right'].set_visible(False)
	axCam2.spines['left'].set_visible(False)
	axCam2.get_xaxis().set_visible(False)
	axCam2.get_yaxis().set_visible(False)
	#axCam2.set_axis_off()
	axCam2.imshow(Cam2_img, origin='upper',norm=normA, aspect = 'equal')

	Cam3_img=video_frames_Cam3[currentVidIdx]
	axCam3 = plt.subplot2grid((fig_span[1],fig_span[0]),(Cam3_origin[1], Cam3_origin[0]),rowspan=Cam3_xy_span[1],colspan=Cam3_xy_span[0])
	axCam3.spines['bottom'].set_visible(False)
	axCam3.spines['top'].set_visible(False)
	axCam3.spines['right'].set_visible(False)
	axCam3.spines['left'].set_visible(False)
	axCam3.get_xaxis().set_visible(False)
	axCam3.get_yaxis().set_visible(False)
	#axCam3.set_axis_off()
	axCam3.imshow(Cam3_img, origin='upper',norm=normA, aspect = 'equal')	


	axis_color=plot_setting.axis_color_blackBack
	font_color=plot_setting.font_color_blackBack
	axhline_color=plot_setting.axhline_color_blackBack
	data_ylabel_position=[plot_setting.data_ylabel_position[0]+0.05, plot_setting.data_ylabel_position[1]]
	fontsize=8



	ax_3d = plt.subplot2grid((fig_span[1],fig_span[0]),(pose3d_origin[1], pose3d_origin[0]),rowspan=pose3d_xy_span[1],colspan=pose3d_xy_span[0], projection='3d')
	ax_3d.set_xlabel('x mm')
	ax_3d.set_ylabel('y mm')
	ax_3d.set_zlabel('z mm')

	
	lim_x = (-2, 2)
	lim_y = (-2, 2)
	lim_z = (-2, 1)

	ax_3d.set_xlim(lim_x)
	ax_3d.set_ylim(lim_y)
	ax_3d.set_zlim(lim_z)

	ax_3d.grid(False)
	ax_3d.view_init(45, -45)

	# ax_3d.plot(x, y, z, '-', color=leg_color, alpha=1)	

	# plot_jpos3d_utils.plot_overlaplegs_from_pos3d(Jpos_dmntevt_frameBased_evt_DS_flatten_list, outDirGCevt_ROI, 'ROI#'+str(ROI_i)+'_dmnt_GCevt_Pose3d.png', plotting_order='leg',leg_order=leg_order_ori, plane='')


	# for frame_order_idx, frame_order_item in enumerate(Jpos_DicData_frameBased_list):

	# 	print('shape frame_order_item', np.shape(frame_order_item))

	# print('len Jpos_DicData_frameBased_list', len(Jpos_DicData_frameBased_list))

	frame_order_item=Jpos_DicData_frameBased_list[currentVidIdx]
	# Current leg order = ['LF_leg', 'LM_leg', 'LH_leg', 'RF_leg', 'RM_leg', 'RH_leg']
	# Desired leg order = ['RH_leg', 'RM_leg', 'RF_leg', 'LH_leg', 'LM_leg', 'LF_leg']
	corrspd_desiredNum_to_curr_legOrder=[5,4,3,2,1,0]
	zipped_num_frameBased_jpos=zip(corrspd_desiredNum_to_curr_legOrder, frame_order_item)
	sorted_zipped_num_frameBased_jpos=sorted(zipped_num_frameBased_jpos)
	sorted_frame_order_item = [element for _, element in sorted_zipped_num_frameBased_jpos]
	ref_leg_order=leg_order_plot


	for leg_order_idx, leg_order_item in enumerate(frame_order_item):

		#print('second_order_idx', second_order_idx)

		# print('shape leg_order_item', np.shape(leg_order_item))

		corresponding_ori_legIdx=corrspd_desiredNum_to_curr_legOrder[leg_order_idx]
		Leg_ID = leg_order[corresponding_ori_legIdx]
		# print('Leg_ID',Leg_ID)
		leg_color=plot_setting.leg_colors[Leg_ID]
		x=frame_order_item[corresponding_ori_legIdx][0]
		y=frame_order_item[corresponding_ori_legIdx][1]
		z=frame_order_item[corresponding_ori_legIdx][2]

		# print(currentVidIdx, leg_order_idx, x,y,z)
		
		ax_3d.plot(x, y, z, '-', color=leg_color, linewidth=3, alpha=1)	

	pane_color=(0.3, 0.3, 0.3)
	label_3d_color='w'
	ax_3d.w_xaxis.pane.set_color(pane_color);
	ax_3d.w_yaxis.pane.set_color(pane_color);
	ax_3d.w_zaxis.pane.set_color(pane_color);
	ax_3d.set_xlabel(u'\u27F5 Posterior       Anterior \u27F6', color=label_3d_color, size=fontsize, fontweight='bold', labelpad=-10)
	ax_3d.set_ylabel(u'\u27F5 Right              Left \u27F6', color=label_3d_color, size=fontsize, fontweight='bold', labelpad=-10)
	ax_3d.set_zlabel(u'\u27F5 Dorsal     Ventral \u27F6', color=label_3d_color, size=fontsize, fontweight='bold', labelpad=-10)
	# ax_3d.tick_params(axis='x', colors=pane_color, labelsize=fontsize, pad=-3)  # only affects
	# ax_3d.tick_params(axis='y', colors=pane_color, labelsize=fontsize, pad=-3)  # only affects
	# ax_3d.tick_params(axis='z', colors=pane_color, labelsize=fontsize, pad=-3)  # only affects
	ax_3d.set_xticks([lim_x[0], np.mean((lim_x[0], 0)), 0, np.mean((lim_x[1], 0)), lim_x[1]])
	ax_3d.set_yticks([lim_y[0], np.mean((lim_y[0], 0)), 0, np.mean((lim_y[1], 0)), lim_y[1]])
	ax_3d.set_zticks([lim_z[0], np.mean((lim_z[0], 0)), 0, lim_z[1]])

	ax_3d.xaxis.set_ticklabels([])
	ax_3d.yaxis.set_ticklabels([])
	ax_3d.zaxis.set_ticklabels([])
	for line in ax_3d.xaxis.get_ticklines():
	    line.set_visible(False)
	for line in ax_3d.yaxis.get_ticklines():
	    line.set_visible(False)
	for line in ax_3d.zaxis.get_ticklines():
	    line.set_visible(False)

	ax_3d.zaxis._axinfo['juggled'] = (1, 2, 0)




	xaxis=np.asarray(timeSec_trim)-timeSec_trim[0]



	axAP = plt.subplot2grid((fig_span[1],fig_span[0]),(AP_origin[1], AP_origin[0]),rowspan=AP_xy_span[1],colspan=AP_xy_span[0])
	axAP.plot(xaxis, velForw_trim, label = 'Yaw', color=plot_setting.AP_color,linewidth=plot_setting.data_trace_width)
	axAP.axhline(0, linestyle='dashed',color=axhline_color,linewidth=plot_setting.axhline_width)
	axAP.plot(xaxis[int(currentVidIdx*ratio_smpRate_trace_photos)], velForw_trim[int(currentVidIdx*ratio_smpRate_trace_photos)], marker = 'o', markersize = plot_setting.timedot_size, color=plot_setting.timedot_edgecolor, markeredgewidth=plot_setting.timedot_edgewidth, markerfacecolor=plot_setting.timedot_edgecolor, markeredgecolor=plot_setting.timedot_edgecolor, linewidth=0)		
	#axAP.yaxis.set_major_locator(ticker.MaxNLocator(nbins=tick_nbins, min_n_ticks=2, integer=True))
	axAP.yaxis.set_major_locator(ticker.FixedLocator(AP_tick_range))
	axAP.set_xlim(0,xaxis[-1])
	axAP.set_ylim(min_AP,max_AP)
	axAP.spines['bottom'].set_visible(False)
	axAP.spines['top'].set_visible(False)
	axAP.spines['right'].set_visible(False)
	axAP.spines['left'].set_color(axis_color)
	axAP.get_xaxis().set_visible(False)
	axAP.get_xaxis().tick_bottom()
	axAP.get_yaxis().tick_left()
	axAP.get_yaxis().set_label_coords(data_ylabel_position[0],data_ylabel_position[1])
	axAP.set_yticks([0, AP_tick_range[1]])
	axAP.tick_params(axis='both', colors=axis_color,top=False, right=False, labelsize=fontsize, length=2)
	axAP.set_ylabel(r'$\rm{V}_\mathrm{forward}$'+'\n'+r'$\rm{(mm. s}^\mathrm{-1}$'+')',size=fontsize, fontweight='bold', color=font_color, rotation=0, fontname='Arial', va='center')

	axML = plt.subplot2grid((fig_span[1],fig_span[0]),(ML_origin[1], ML_origin[0]),rowspan=ML_xy_span[1],colspan=ML_xy_span[0])
	axML.plot(xaxis, velSide_trim, label = 'ML', color=plot_setting.ML_color,linewidth=plot_setting.data_trace_width)
	axML.axhline(0, linestyle='dashed',color=axhline_color,linewidth=plot_setting.axhline_width)
	axML.plot(xaxis[int(currentVidIdx*ratio_smpRate_trace_photos)], velSide_trim[int(currentVidIdx*ratio_smpRate_trace_photos)], marker = 'o', markersize = plot_setting.timedot_size, color=plot_setting.timedot_edgecolor, markeredgewidth=plot_setting.timedot_edgewidth, markerfacecolor=plot_setting.timedot_edgecolor, markeredgecolor=plot_setting.timedot_edgecolor, linewidth=0)	
	#axML.yaxis.set_major_locator(ticker.MaxNLocator(nbins=tick_nbins, min_n_ticks=2, integer=True))
	axML.yaxis.set_major_locator(ticker.FixedLocator(ML_tick_range))
	axML.set_xlim(0,xaxis[-1])
	axML.set_ylim(min_ML,max_ML)
	axML.spines['bottom'].set_visible(False)
	axML.spines['top'].set_visible(False)
	axML.spines['right'].set_visible(False)
	axML.spines['left'].set_color(axis_color)
	axML.get_xaxis().set_visible(False)
	axML.get_xaxis().tick_bottom()
	axML.get_yaxis().tick_left()
	axML.get_yaxis().set_label_coords(data_ylabel_position[0],data_ylabel_position[1])
	axML.set_yticks([ML_tick_range[0], 0, ML_tick_range[1]])
	axML.tick_params(axis='both', colors=axis_color,top=False, right=False, labelsize=fontsize, length=2)
	axML.set_ylabel(r'$\rm{V}_\mathrm{side}$'+'\n'+r'$\rm{(mm. s}^\mathrm{-1}$'+')',size=fontsize, color=font_color, fontweight='bold', rotation=0, fontname='Arial', va='center')


	axYaw = plt.subplot2grid((fig_span[1],fig_span[0]),(Yaw_origin[1], Yaw_origin[0]),rowspan=Yaw_xy_span[1],colspan=Yaw_xy_span[0])
	axYaw.plot(xaxis, velTurn_trim, label = 'Yaw', color=plot_setting.Yaw_color,linewidth=plot_setting.data_trace_width)
	axYaw.axhline(0, linestyle='dashed',color=axhline_color, linewidth=plot_setting.axhline_width)
	axYaw.plot(xaxis[int(currentVidIdx*ratio_smpRate_trace_photos)], velTurn_trim[int(currentVidIdx*ratio_smpRate_trace_photos)], marker = 'o', markersize = plot_setting.timedot_size, color=plot_setting.timedot_edgecolor, markeredgewidth=plot_setting.timedot_edgewidth, markerfacecolor=plot_setting.timedot_edgecolor, markeredgecolor=plot_setting.timedot_edgecolor, linewidth=0)		
	#axYaw.yaxis.set_major_locator(ticker.MaxNLocator(nbins=tick_nbins, min_n_ticks=2, integer=True))
	axYaw.yaxis.set_major_locator(ticker.FixedLocator(Yaw_tick_range))
	axYaw.set_xlim(0,xaxis[-1])
	axYaw.set_ylim(min_Yaw,max_Yaw)
	axYaw.spines['bottom'].set_visible(False)
	axYaw.spines['top'].set_visible(False)
	axYaw.spines['right'].set_visible(False)
	axYaw.spines['left'].set_color(axis_color)
	axYaw.get_xaxis().set_visible(False)
	axYaw.get_xaxis().tick_bottom()
	axYaw.get_yaxis().tick_left()
	axYaw.get_yaxis().set_label_coords(data_ylabel_position[0],data_ylabel_position[1])
	axYaw.set_yticks([Yaw_tick_range[0], 0, Yaw_tick_range[1]])
	axYaw.tick_params(axis='both', colors=axis_color,top=False, right=False, labelsize=fontsize, length=2)
	axYaw.set_ylabel(r'$\rm{V}_\mathrm{turn}$'+'\n'+r'$\rm{(deg. s}^\mathrm{-1}$'+')',size=fontsize, color=font_color, fontweight='bold', rotation=0, fontname='Arial', va='center')


	axPER = plt.subplot2grid((fig_span[1],fig_span[0]),(PE_origin[1], PE_origin[0]),rowspan=PE_xy_span[1],colspan=PE_xy_span[0])
	axPER.plot(xaxis, PE_len_trim, label = 'PE', color=plot_setting.PER_color,linewidth=plot_setting.data_trace_width)
	axPER.plot(xaxis[int(currentVidIdx*ratio_smpRate_trace_photos)], PE_len_trim[int(currentVidIdx*ratio_smpRate_trace_photos)], marker = 'o', markersize = plot_setting.timedot_size, color=plot_setting.timedot_edgecolor, markeredgewidth=plot_setting.timedot_edgewidth, markerfacecolor=plot_setting.timedot_edgecolor, markeredgecolor=plot_setting.timedot_edgecolor, linewidth=0)	
	## for including NaN tail to be plotted
	axPER.plot(xaxis[-1], 0, color='k',linewidth=1, alpha=0) 
	axPER.axhline(0, linestyle='dashed',color=axhline_color,linewidth=plot_setting.axhline_width)
	axPER.yaxis.set_major_locator(ticker.FixedLocator(PE_tick_range))
	axPER.set_xlim(0,xaxis[-1])
	axPER.set_ylim(min_PER_len,max_PER_len)
	axPER.spines['bottom'].set_visible(False)
	axPER.spines['top'].set_visible(False)
	axPER.spines['right'].set_visible(False)
	axPER.spines['left'].set_color(axis_color)
	axPER.get_xaxis().set_visible(False)
	axPER.get_xaxis().tick_bottom()
	axPER.get_yaxis().tick_left()
	axPER.get_yaxis().set_label_coords(data_ylabel_position[0],data_ylabel_position[1])
	axPER.set_yticks([0, PE_tick_range[1]])
	axPER.tick_params(axis='both', colors=axis_color,top=False, right=False,labelsize=fontsize, length=2)
	axPER.set_ylabel('PE length \n(px)',size=fontsize, color=font_color, fontweight='bold', rotation=0, fontname='Arial', va='center')

	tick_nbins=1
	axCO2 = plt.subplot2grid((fig_span[1],fig_span[0]),(co2_origin[1], co2_origin[0]),rowspan=co2_xy_span[1],colspan=co2_xy_span[0])
	axCO2.plot(xaxis, CO2puff_trim, label = 'CO2', color=axis_color,linewidth=plot_setting.data_trace_width)
	axCO2.plot(xaxis[int(currentVidIdx*ratio_smpRate_trace_photos)], CO2puff_trim[int(currentVidIdx*ratio_smpRate_trace_photos)], marker = 'o', markersize = plot_setting.timedot_size, color=plot_setting.timedot_edgecolor, markeredgewidth=plot_setting.timedot_edgewidth, markerfacecolor=plot_setting.timedot_edgecolor, markeredgecolor=plot_setting.timedot_edgecolor, linewidth=0)	
	axCO2.yaxis.set_major_locator(ticker.FixedLocator([0, 1]))
	axCO2.set_xlim(0, xaxis[-1])
	axCO2.set_ylim(-0.1, 1.1)
	axCO2.spines['left'].set_visible(True)
	axCO2.spines['bottom'].set_visible(True)
	axCO2.spines['top'].set_visible(False)
	axCO2.spines['right'].set_visible(False)
	axCO2.spines['left'].set_color(axis_color)
	axCO2.spines['bottom'].set_color(axis_color)
	axCO2.get_xaxis().set_visible(True)
	axCO2.get_yaxis().set_visible(True)
	axCO2.get_xaxis().tick_bottom()
	axCO2.get_yaxis().tick_left()
	axCO2.get_yaxis().set_label_coords(data_ylabel_position[0],data_ylabel_position[1])
	axCO2.tick_params(axis='both', colors=axis_color,top=False, right=False,labelsize=fontsize, length=2)
	axCO2.set_ylabel(r'$\rm{CO}_\mathrm{2}$' +' puff',size=fontsize, color=font_color, fontweight='bold', rotation=0, fontname='Arial', va='center')
	axCO2.set_xlabel('Time (s)',size=fontsize, fontweight='bold', color=font_color, fontname='Arial')

	
	plt.savefig(str(output_video_dir + 'VidFrame' + "%05d" % video_frame_idx + '.jpg'), facecolor=fig.get_facecolor(), edgecolor='none', transparent=True)
	plt.close(fig)



	return 








resting_video_source = [( '20190703', 'SS42740-tdTomGC6fopt', 'fly2', '001', 26, 31, 'r')] #good

forward_walking_video_source = [('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '005', 55, 59, 'fw')] #good
backward_walking_video_source = [('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '005', 16, 17, 'bw')] #good

# L_turn_walking_video_source = [('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '005', 132, 134, 'L_trun')]
# R_turn_walking_video_source = [('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '005', 132, 134, 'R_turn')]

eye_grooming_video_source = [('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '005', 181, 183, 'eg')] #good 5422-5575
antennae_grooming_video_source = [('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '001', 69, 70, 'ag')] #good
foreleg_grooming_video_source = [('20190918', 'SS52147-tdTomGC6fopt', 'fly1', '009', 54, 56, 'flg')] #good

hindleg_grooming_video_source = [('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '001', 57, 60, 'hlg')] #good 1696-1800
Abdomen_grooming_video_source = [
# ('20190904', 'SS51017-tdTomGC6fopt', 'fly3', '001', 100, 105, 'abdg'),   #2990-3181 # deepfly3d tracking not good
# ('20190904', 'SS51017-tdTomGC6fopt', 'fly3', '001', 88, 91, 'abdg'),    # deepfly3d tracking not good
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '003', 33, 34.1, 'abdg'),  #good    
# ('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '003', 36, 37, 'abdg'),  #good   
('20191002', 'SS51046-tdTomGC6fopt', 'fly1', '004', 189.5, 193.5, 'abdg'), #good    
] 

pushing_video_source = [
('20190906', 'SS51029-tdTomGC6fopt', 'fly4', '005', 4, 11, 'push'), #good
('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '004', 206.5, 209.3, 'push'), #good #6176-6266
]

PER_during_resting_video_source = [('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '005', 220, 235, 'per')] #good
# PER_during_walking_video_source = [('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '005', 100, 110)] #good

CO2puff_video_source = [('20190703', 'SS42740-tdTomGC6fopt', 'fly2', '005', 9, 12, 'CO2')] #good also used for backward walking




## main ##
NAS_Dir='/mnt/data/'
NAS_AN_Proj_Dir=NAS_Dir+'CLC/Ascending_Project/'

NAS_AN_Proj_Dir = NAS_Dir+'CLC/Ascending_Project/'

AN_Proj_Dir = NAS_AN_Proj_Dir


experiments=resting_video_source+forward_walking_video_source+backward_walking_video_source+eye_grooming_video_source+antennae_grooming_video_source+foreleg_grooming_video_source+hindleg_grooming_video_source+Abdomen_grooming_video_source+pushing_video_source+PER_during_resting_video_source+CO2puff_video_source
# experiments=resting_video_source+forward_walking_video_source
# experiments=Abdomen_grooming_video_source
print('experiments', experiments)



AP_concat=[]
ML_concat=[]
Yaw_concat=[]
PE_concat=[]




print('Look for the bboundary of traces')
for TwoP_date, TwoP_genotype, TwoP_fly, TwoP_recrd_num, start_s, end_s, beh_label in experiments:
	Gal4=TwoP_genotype.split('-')[0]
	fly_beh=TwoP_fly[0].upper()+TwoP_fly[1:]
	dataDir = AN_Proj_Dir + Gal4 +'/2P/' + TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '/'
	pathDic=dataDir+'output/'
	Beh_GC_DicData = general_utils.open_Beh_Jpos_GC_DicData(pathDic, filename='SyncDic_7CamBeh_BW_20210619_GC-RES.p')

	timeSec = Beh_GC_DicData['timeSec']
	velForw_mm = Beh_GC_DicData['velForw']
	velSide_mm = Beh_GC_DicData['velSide']
	velTurn_deg = Beh_GC_DicData['velTurn']
	PER_exten_len = Beh_GC_DicData['PER_exten_len']

	velForw_trim=sync_utils.trim_period(velForw_mm, timeSec, startTime=start_s, endTime=end_s)
	velSide_trim=sync_utils.trim_period(velSide_mm, timeSec, startTime=start_s, endTime=end_s)
	velTurn_trim=sync_utils.trim_period(velTurn_deg, timeSec, startTime=start_s, endTime=end_s)
	PE_len_trim=sync_utils.trim_period(PER_exten_len, timeSec, startTime=start_s, endTime=end_s)


	AP_concat.extend(velForw_trim)
	ML_concat.extend(velSide_trim)
	Yaw_concat.extend(velTurn_deg)
	PE_concat.extend(PE_len_trim)

	



max_AP=np.nanmax(AP_concat)
min_AP=np.nanmin(AP_concat)

print('max_AP', max_AP)
print('min_AP', min_AP)



# if max_AP>30:
# 	max_AP=30

if abs(max_AP)<abs(min_AP):
	max_AP=abs(min_AP)
# elif abs(min_AP)<abs(max_AP):
# 	min_AP = (-1)*max_AP
elif min_AP>0:
	min_AP=0
AP_tick = plot_utils.find_nearest_nice_integer_of_postive_number(max_AP)
AP_tick_range=[-AP_tick, AP_tick]

print('max_AP', max_AP)
print('min_AP', min_AP)
print('AP_tick_range', AP_tick_range)

max_ML=np.nanmax(ML_concat)
min_ML=np.nanmin(ML_concat)

if max_ML>11:
	max_ML=11
if abs(min_ML)>11:
	min_ML=(-1)*11

if abs(max_ML)<abs(min_ML):
	max_ML=abs(min_ML)
elif abs(min_ML)<abs(max_ML):
	min_ML = (-1)*max_ML
elif min_ML>0:
	min_ML=0
ML_tick = plot_utils.find_nearest_nice_integer_of_postive_number(max_ML)
ML_tick_range=[-ML_tick, ML_tick]
print('max_ML', max_ML)
print('min_ML', min_ML)
print('ML_tick_range', ML_tick_range)

max_Yaw=np.nanmax(velTurn_deg)
min_Yaw=np.nanmin(velTurn_deg)

if max_Yaw>720:
	max_Yaw=720
if abs(min_Yaw)>720:
	min_Yaw=(-1)*720

if abs(max_Yaw)<abs(min_Yaw):
	max_Yaw=abs(min_Yaw)
elif abs(min_Yaw)<abs(max_Yaw):
	min_Yaw = (-1)*max_Yaw
elif min_Yaw>0:
	min_Yaw=0
Yaw_tick = plot_utils.find_nearest_nice_integer_of_postive_number(max_Yaw)
Yaw_tick_range=[-Yaw_tick, Yaw_tick]

	

max_PER_len=np.nanmax(PE_concat)
min_PER_len=np.nanmin(PE_concat)
if max_PER_len<100:
	max_PER_len=100
if min_PER_len>0:
	min_PER_len=0 
PER_len_tick_range=[min_PER_len, max_PER_len]
PE_tick = plot_utils.find_nearest_nice_integer_of_postive_number(max_PER_len)
PE_tick_range=[-PE_tick, PE_tick]

print('[min_PER_len, max_PER_len]', [min_PER_len, max_PER_len])
print('PE_tick_range', PE_tick_range)











video_frames_Cam0=[]
video_frames_Cam6=[]
video_frames_Cam5=[]
video_frames_Cam1=[]
video_frames_Cam2=[]
video_frames_Cam3=[]

video_beh_labels=[]



video_frame_idx=0




for TwoP_date, TwoP_genotype, TwoP_fly, TwoP_recrd_num, start_s, end_s, beh_label in experiments:

	print(TwoP_date, TwoP_genotype, TwoP_fly, TwoP_recrd_num, start_s, end_s, beh_label)



	Gal4=TwoP_genotype.split('-')[0]
	fly_beh=TwoP_fly[0].upper()+TwoP_fly[1:]
	dataDir = AN_Proj_Dir + Gal4 +'/2P/' + TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '/'
	pathDic=dataDir+'output/'
	jpos_ang_dir=pathDic+'joint_angles/'

	CamDir = NAS_Dir+'CLC/'+TwoP_date[2:]+'_'+TwoP_genotype+'/'+fly_beh+'/'+'CO2xzGG/behData_'+TwoP_recrd_num+'/images/'
	print('CamDir', CamDir)

	output_video_dir=NAS_AN_Proj_Dir+'_Summary/Figures/supp_figures/Exemplar_behavior_video/'
	if not os.path.exists(output_video_dir):
		os.makedirs(output_video_dir)	


	RealstopCamIdx = sync_utils.FindLastCamPhotoIdx(CamDir)
	Beh_GC_DicData = general_utils.open_Beh_Jpos_GC_DicData(pathDic, filename='SyncDic_7CamBeh_BW_20210619_GC-RES.p')
	Jpos_DicData_temp = general_utils.open_Beh_Jpos_GC_DicData(jpos_ang_dir, filename='joint_pose3d_beh_filtered_BW_20210619.pkl')


	timeSec = Beh_GC_DicData['timeSec']

	sample_freq=len(timeSec)/max(timeSec)

	frame_rate=RealstopCamIdx/max(timeSec)

	print('RealstopCamIdx', RealstopCamIdx)
	print('timeSec', timeSec)
	print('frame_rate', frame_rate)
	print('sample_freq', sample_freq)


	startVidIdx=int(start_s*frame_rate)
	stopVidIdx=int(end_s*frame_rate)
	print('startVidIdx', startVidIdx)
	print('stopVidIdx', stopVidIdx)

	

	Jpos_DicData={}
	for key, value in Jpos_DicData_temp.items():
		if key!='Behaviour' and key!='RH_FeTi':
			Jpos_DicData.update({key:value})
	# for key, value in Jpos_DicData.items():
	# 	print(key)


	Jpos_DicData_frameBased=plot_jpos3d_utils.convert_jointBasedDic_to_frameBased_pos3dDic(Jpos_DicData)
	Jpos_DicData_frameBased_list=plot_jpos3d_utils.convert_frameBasedDic_to_list(Jpos_DicData_frameBased)
	print('shape Jpos_DicData_frameBased_list', np.shape(Jpos_DicData_frameBased_list))

	Jpos_DicData_frameBased_list=Jpos_DicData_frameBased_list[startVidIdx:stopVidIdx]
	print('shape Jpos_DicData_frameBased_list', np.shape(Jpos_DicData_frameBased_list))


	

	velForw_mm = Beh_GC_DicData['velForw']
	velSide_mm = Beh_GC_DicData['velSide']
	velTurn_deg = Beh_GC_DicData['velTurn']
	PER_exten_len = Beh_GC_DicData['PER_exten_len']
	CO2puff = Beh_GC_DicData['CO2puff']

	sampleFreq_trace=len(velForw_mm)/max(timeSec)



	
	print('velForw_mm', velForw_mm)
	print('len velForw_mm', len(velForw_mm))
	print('len PER_exten_len', len(PER_exten_len))
	print('len timeSec', len(timeSec))



	velForw_trim=sync_utils.trim_period(velForw_mm, timeSec, startTime=start_s, endTime=end_s)
	velSide_trim=sync_utils.trim_period(velSide_mm, timeSec, startTime=start_s, endTime=end_s)
	velTurn_trim=sync_utils.trim_period(velTurn_deg, timeSec, startTime=start_s, endTime=end_s)
	PE_len_trim=sync_utils.trim_period(PER_exten_len, timeSec, startTime=start_s, endTime=end_s)
	CO2puff_trim=sync_utils.trim_period(CO2puff, timeSec, startTime=start_s, endTime=end_s)
	timeSec_trim=sync_utils.trim_period(timeSec, timeSec, startTime=start_s, endTime=end_s)


	print('velForw_trim', velForw_trim)
	print('len velForw_trim', len(velForw_trim))
	print('len PE_len_trim', len(PE_len_trim))
	print('len timeSec_trim', len(timeSec_trim))



	for VidIdx in range(startVidIdx, stopVidIdx):


		if os.path.exists(CamDir+'camera_0_img_'+str(VidIdx)+'.jpg'):
			Cam0_img = io.imread(CamDir+'camera_0_img_'+str(VidIdx)+'.jpg')
			Cam0_img = cv2.cvtColor(Cam0_img, cv2.COLOR_GRAY2BGR)
			video_frames_Cam0.append(Cam0_img)
		else:
			print("Cam0 video frame doesn't exist.")
			sys.exit(0)

		if os.path.exists(CamDir+'camera_6_img_'+str(VidIdx)+'.jpg'):
			Cam6_img = io.imread(CamDir+'camera_6_img_'+str(VidIdx)+'.jpg')
			Cam6_img = cv2.cvtColor(Cam6_img, cv2.COLOR_GRAY2BGR)
			video_frames_Cam6.append(Cam6_img)
		else:
			print("Cam6 video frame doesn't exist.")
			sys.exit(0)

		if os.path.exists(CamDir+'camera_5_img_'+str(VidIdx)+'.jpg'):
			Cam5_img = io.imread(CamDir+'camera_5_img_'+str(VidIdx)+'.jpg')
			Cam5_img = cv2.cvtColor(Cam5_img, cv2.COLOR_GRAY2BGR)
			video_frames_Cam5.append(Cam5_img)
		else:
			print("Cam5 video frame doesn't exist.")
			sys.exit(0)

		if os.path.exists(CamDir+'camera_1_img_'+str(VidIdx)+'.jpg'):	
			Cam1_img = io.imread(CamDir+'camera_1_img_'+str(VidIdx)+'.jpg')
			Cam1_img = cv2.cvtColor(Cam1_img, cv2.COLOR_GRAY2BGR)
			video_frames_Cam1.append(Cam1_img)
		else:
			print("Cam1 video frame doesn't exist.")
			sys.exit(0)

		if os.path.exists(CamDir+'camera_2_img_'+str(VidIdx)+'.jpg'):	
			Cam2_img = io.imread(CamDir+'camera_2_img_'+str(VidIdx)+'.jpg')
			Cam2_img = cv2.cvtColor(Cam2_img, cv2.COLOR_GRAY2BGR)
			video_frames_Cam2.append(Cam2_img)
		else:
			print("Cam2 video frame doesn't exist.")
			sys.exit(0)

		if os.path.exists(CamDir+'camera_3_img_'+str(VidIdx)+'.jpg'):	
			Cam3_img = io.imread(CamDir+'camera_3_img_'+str(VidIdx)+'.jpg')
			Cam3_img = cv2.cvtColor(Cam3_img, cv2.COLOR_GRAY2BGR)
			video_frames_Cam3.append(Cam3_img)
		else:
			print("Cam3 video frame doesn't exist.")
			sys.exit(0)


		video_beh_labels.append(beh_label)

	# print('video_beh_labels', video_beh_labels)
	print('len video_beh_labels', len(video_beh_labels))
	print('shape video_frames_Cam0', np.shape(video_frames_Cam0))

	ratio_smpRate_trace_photos=len(velForw_trim)/len(video_frames_Cam3)
	print('ratio_smpRate_trace_photos', ratio_smpRate_trace_photos)












	print('video_frame_idx', video_frame_idx)
	pool_iter_list, video_frame_endIdx=make_pool_iter(len(video_beh_labels), video_frame_idx)

	print('pool_iter_list', pool_iter_list)
	print('video_frame_endIdx', video_frame_endIdx)


	# for i, f_i in ((50,video_frame_idx), (100,video_frame_idx+1)):
	# # for i, f_i in pool_iter_list:
	# 	exemp_beh_video_frame(i, f_i)

	# sys.exit(0)



	pool = Pool() 
	# pool.map(exemp_beh_video_frame, range(0,len(video_frames_Cam0)))
	# pool.map(exemp_beh_video_frame, (50,100))
	# pool.map(wrap_args_func, [(50,video_frame_idx), (100,video_frame_idx+1)])
	pool.map(wrap_args_func, pool_iter_list)


	pool.close()
	pool.join()
	del pool

	

	video_frame_idx=video_frame_endIdx
	print('video_frame_idx', video_frame_idx)


	video_frames_Cam0=[]
	video_frames_Cam6=[]
	video_frames_Cam5=[]
	video_frames_Cam1=[]
	video_frames_Cam2=[]
	video_frames_Cam3=[]

	video_beh_labels=[]







#os.system('ls')
#digit5_number="%05d" %200
digit5_number="%05d" % 0
print('digit5_number', digit5_number)

os.chdir(output_video_dir)
#os.system('ffmpeg -y -r 30 -start_number '+digit5_number+' -i VidFrame%05d.jpg -vcodec libx264 -pix_fmt yuvj420p -crf 32 '+ TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num+'-'+str(start_s)+'s-'+str(end_s)+'s_GC_BehClass_30fps.mp4')
os.system('ffmpeg -y -r 30 -start_number '+digit5_number+' -i VidFrame%05d.jpg -vcodec libx264 -pix_fmt yuv420p -crf 32 '+ 'Exemplar_behavior_30fps.mp4')

os.system('rm *.jpg')

































