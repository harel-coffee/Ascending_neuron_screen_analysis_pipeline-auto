import os
import sys
import numpy as np
import pandas as pd
import math
from multiprocessing import Process
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.switch_backend('agg')
from matplotlib import ticker 
from skimage import io
from itertools import groupby 
from PIL import Image
Image.Image.tostring = Image.Image.tobytes
import cv2
import shutil


import video_utils.list_inputFiles as list_inputFiles
import video_utils.plot_setting as plot_setting
import video_utils.sync_utils as sync_utils
import video_utils.plot_utils as plot_utils
import utils2p 


trace_intvl=150


experiments=list_inputFiles.suppfig_experiments

# experiments=[
# ('20181230', 'R36G04-tdTomGC6fopt', 'fly1', '003', 380, 5,5+trace_intvl, 'cc512_001', '20181117', 'R36G04-GFP', '1'),  
# ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '006', 31, 0,0+trace_intvl, 'cc512_006', '20190416', 'SS25469-smFP', '2'), 
# ('20190318', 'SS29621-tdTomGC6fopt', 'fly1', '006', 654, 80,80+trace_intvl, 'cc512_000', '20190425', 'SS29621-smFP', '1'),  
# ('20190619', 'SS41605-tdTomGC6fopt', 'fly3', '003', 288, 90,90+trace_intvl, 'cc512_004', '20190821', 'SS41605-smFP', '5'),  
# ('20190701', 'SS42008-tdTomGC6fopt', 'fly4', '003', 397, 0,0+trace_intvl, 'cc512_002', '20190604', 'SS42008-smFP', '3'), 
# ('20190704', 'SS42749-tdTomGC6fopt', 'fly1', '002', 112, 80,80+trace_intvl, 'cc512_002', '20190805', 'SS42749-smFP', '3'),  
# ('20191001', 'SS49172-tdTomGC6fopt', 'fly1', '001', 441 ,80,80+trace_intvl, 'cc512_001', '20190805', 'SS49172-smFP', '2'),  
# ('20190610', 'SS40489-tdTomGC6fopt', 'fly3', '004', 983, 50,90+trace_intvl, 'cc512_001', 'redo', 'redo', '1'), #trim based on selected time (s), period = 150 s # missed file
# ('20190719', 'SS45605-tdTomGC6fopt', 'fly1', '003', 303, 30,30+trace_intvl, 'cc512_001', '20190830', 'SS45605-smFP', '4'), 
# ('20190723', 'SS45363-tdTomGC6fopt', 'fly1', '013', 355, 20,20+trace_intvl, 'cc512_003', '20190611', 'SS45363-smFP', '2'),  
# ('20180822', 'SS25451-tdTomGC6fopt', 'fly4', '012', 379, 55,55+trace_intvl, 'cc512_000', '20190406', 'SS25451-smFP', '1'),  

# ]


# experiments=[
# ('20190311', 'SS27485-tdTomGC6fopt', 'fly2', '004', 646, 10,10+trace_intvl, 'cc512_001', '20190416', 'SS27485-smFP', '3'),  
# ('20190220', 'SS25469-tdTomGC6fopt', 'fly1', '006', 31, 0,0+trace_intvl, 'cc512_006', '20190416', 'SS25469-smFP', '2'), 

# ]



def check_file_existence(exp_list, exp_type='confocal'):

	for TwoP_date, TwoP_genotype, TwoP_fly, TwoP_recrd_num, start_s, end_s, CC_fluorcn_num, conf_date, conf_genotype, conf_fly in exp_list:
		
		Gal4=TwoP_genotype.split('-')[0]
		dataDir = AN_Proj_Dir + Gal4 +'/2P/' + TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '/'

		if exp_type=='confocal':
			# ConfocalImg_dir = AN_Proj_Dir + Gal4 + '/Confocal/Registered/'
			ConfocalImg_dir = AN_Proj_Dir + Gal4 + '/Confocal/Best_image/'
			BrainImgDir = ConfocalImg_dir + conf_date + '-' + conf_fly + '-' + conf_genotype + '-brain.tif'
			VNCImgDir = ConfocalImg_dir + conf_date + '-' + conf_fly + '-' + conf_genotype + '-VNC.tif'
			
			if not os.path.exists(BrainImgDir):
				print(BrainImgDir, "doesn't exist.")
			if not os.path.exists(VNCImgDir):
				print(VNCImgDir, "doesn't exist.")

		elif exp_type=='cc512':
			CCfluoImgDir = AN_Proj_Dir + Gal4 +'/2P/' + TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-'+CC_fluorcn_num + '/2Pimg/AVG_warped_RGB.tif'
			if not os.path.exists(CCfluoImgDir):
				print(CCfluoImgDir, "doesn't exist.")

		elif exp_type=='TwoP':
			pathForRGB =dataDir +'/2Pimg/'
			if not os.path.exists(pathForRGB+'RGB.tif'):
				print('RGB.tif', "doesn't exist.")

		elif exp_type=='sync':
			pathDic=dataDir+'output/'
			if not os.path.exists(pathDic+'/SyncDic_7CamBeh_BW_20210619_GC-RES.p'):
				print('RGB.tif', "doesn't exist.")


	return



def find_max_ROIs(exp_list):

	ROI_eachGal4=[]

	for TwoP_date, TwoP_genotype, TwoP_fly, TwoP_recrd_num, TwoP_frame, start_s, end_s, CC_fluorcn_num, conf_date, conf_genotype, conf_fly in exp_list:

		Gal4=TwoP_genotype.split('-')[0]
		ThorsyncDir_inNas = NAS_Dir+'2photonData/CLC/'+TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-sync-'+TwoP_recrd_num
		Thorsync_CC_Dir_inNAS = NAS_Dir+'2photonData/CLC/'+TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-sync-'+CC_fluorcn_num
		dataDir = AN_Proj_Dir + Gal4 +'/2P/' + TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '/'
		pathDic=dataDir+'output/'

		Beh_Jpos_GC_DicData = sync_utils.open_GC_beh_sync_DicData(pathDic, filename='SyncDic_7CamBeh_BW_20210619_GC-RES.p')
		GC_set = Beh_Jpos_GC_DicData['GCset']

		ROI_eachGal4.append(len(GC_set))



	max_ROI_counts = max(ROI_eachGal4)


	return max_ROI_counts



def Stitch_frame_as_same_ratio_of_RefImg(targetimg, RefImg=np.zeros((512,683,3), np.uint8)):

	ideal_xy_ratio = np.shape(RefImg)[1]/np.shape(RefImg)[0]
	print('ideal_xy_ratio', ideal_xy_ratio)

	desire_x = np.shape(targetimg)[0]*ideal_xy_ratio
	desire_y = np.shape(targetimg)[0]


	stitch_x = int((desire_x-np.shape(targetimg)[1])/2)
	stitch_y = int(desire_y)

	print('stitch_x', stitch_x, 'stitch_y', stitch_y)

	stitch_Img = np.zeros((stitch_y,stitch_x,3), np.uint8)

	desiredImg_temp = cv2.hconcat([stitch_Img, targetimg])
	desiredImg = cv2.hconcat([desiredImg_temp, stitch_Img])



	return desiredImg



def overlay_small_img_to_big_img(small_img, big_img):

	small_img_w=np.shape(small_img)[1]
	small_img_h=np.shape(small_img)[0]

	print('small_img_w', small_img_w)
	print('small_img_h', small_img_h)

	big_img_w=np.shape(big_img)[1]
	big_img_h=np.shape(big_img)[0]

	print('big_img_w', big_img_w)
	print('big_img_h', big_img_h)

	x_offset=int((big_img_w-small_img_w)/2)
	y_offset=int((big_img_h-small_img_h)/2)

	big_img[y_offset:y_offset+small_img_h, x_offset:x_offset+small_img_w]=small_img


	return big_img






def Supp_figure():



	ConfImg_origin=[0, 0]
	ConfImg_xy_span=[43,86]

	TwoPImg_origin=[ConfImg_origin[0]+ConfImg_xy_span[0], ConfImg_origin[1]]
	TwoPImg_xy_span=[57,43]

	CCfluoImg_origin=[TwoPImg_origin[0],TwoPImg_origin[1]+TwoPImg_xy_span[1]]
	CCfluoImg_xy_span=[57,43]

	print('ConfImg_origin', ConfImg_origin)
	print('TwoPImg_origin', TwoPImg_origin)
	print('CCfluoImg_origin', CCfluoImg_origin)



	trace_xy_span=[100-25, 8]



	Behlabels_origin=[ConfImg_origin[0], ConfImg_origin[1]+ConfImg_xy_span[1]]
	Behlabels_xy_span=[100,trace_xy_span[1]]



	PER_origin=[ConfImg_origin[0]+25, Behlabels_origin[1]+Behlabels_xy_span[1]]
	PER_xy_span=[trace_xy_span[0],trace_xy_span[1]]

	spacer_origin = [PER_origin[0], PER_origin[1]+PER_xy_span[1]]
	spacer_xy_span = [trace_xy_span[0], 1]

	CO2_origin=[PER_origin[0], PER_origin[1]+PER_xy_span[1]+spacer_xy_span[1]]
	CO2_xy_span=[trace_xy_span[0],trace_xy_span[1]]

	AP_origin=[CO2_origin[0], CO2_origin[1]+CO2_xy_span[1]+spacer_xy_span[1]]
	AP_xy_span=[trace_xy_span[0],trace_xy_span[1]]

	ML_origin=[CO2_origin[0], AP_origin[1]+AP_xy_span[1]+spacer_xy_span[1]]
	ML_xy_span=[trace_xy_span[0],trace_xy_span[1]]

	Yaw_origin=[CO2_origin[0], ML_origin[1]+ML_xy_span[1]+spacer_xy_span[1]]
	Yaw_xy_span=[trace_xy_span[0],trace_xy_span[1]]

	ROI_origin=[CO2_origin[0], Yaw_origin[1]+Yaw_xy_span[1]+spacer_xy_span[1]]
	ROI_xy_span=[trace_xy_span[0],trace_xy_span[1]]



	#fig_span = [Behlabels_xy_span[0], ROI_origin[1]+ROI_xy_span[1]*max_ROI_counts]
	fig_span = [Behlabels_xy_span[0], CO2_origin[1]+(ROI_xy_span[1]+spacer_xy_span[1])*(max_ROI_counts+4)]


	print('fig_span', fig_span)

	#sys.exit(0)




	A4_x=11.69 #inch
	A4_y=8.27 #inch

	Ref_Panellabel_pos=[0.01,0.92]
	axConfImg_label_y=plot_utils.find_aligned_pos_of_panelLabel(ref_xy_span=TwoPImg_xy_span, target_xy_span=ConfImg_xy_span, ref_position=1+Ref_Panellabel_pos[1], direction='vertical')
	
	print('axConfImg_label_y', axConfImg_label_y)

	Ref_Panel_scaleBar_pos=[0.03,0.05]

	axTwoPImg_scaleBar_x=plot_utils.find_aligned_pos_of_panelLabel(ref_xy_span=ConfImg_xy_span, target_xy_span=TwoPImg_xy_span, ref_position=Ref_Panel_scaleBar_pos[0], direction='horizontal')
	axTwoPImg_scaleBar_x_px=np.shape(TwoPImg)[1]*axTwoPImg_scaleBar_x
	axTwoPImg_scaleBar_y_px=np.shape(TwoPImg)[0]-np.shape(TwoPImg)[0]*Ref_Panel_scaleBar_pos[1]
	TwoPImg_scale_bar_len_px = plot_utils.calc_scale_bar_um_to_px(pixelSize=TwoP_pixelSizeUM, scale_bar_length_um=Desired_TwoP_scale_bar)

	axCCfluoImg_scaleBar_x=plot_utils.find_aligned_pos_of_panelLabel(ref_xy_span=ConfImg_xy_span, target_xy_span=TwoPImg_xy_span, ref_position=Ref_Panel_scaleBar_pos[0], direction='horizontal')
	axCCfluoImg_scaleBar_x_px=np.shape(CCfluoImg)[1]*axCCfluoImg_scaleBar_x
	axCCfluoImg_scaleBar_y_px=np.shape(CCfluoImg)[0]-np.shape(CCfluoImg)[0]*Ref_Panel_scaleBar_pos[1]
	CCfluoImg_scale_bar_len_px = plot_utils.calc_scale_bar_um_to_px(pixelSize=CCfluo_pixelSizeUM, scale_bar_length_um=Desired_TwoP_scale_bar)

	axConfImg_scaleBar_y=plot_utils.find_aligned_pos_of_panelLabel(ref_xy_span=TwoPImg_xy_span, target_xy_span=ConfImg_xy_span, ref_position=Ref_Panel_scaleBar_pos[1], direction='vertical')
	axConfImg_scaleBar_x_px = np.shape(BrainVNCImg)[1]*Ref_Panel_scaleBar_pos[0]
	axConfImg_scaleBar_y_px = np.shape(BrainVNCImg)[0]-np.shape(BrainVNCImg)[0]*axConfImg_scaleBar_y
	ConfImg_scale_bar_len_px = plot_utils.calc_scale_bar_um_to_px(pixelSize=ConfImg_pixelSizeUM, scale_bar_length_um=Desired_ConfImg_scale_bar)


	print('axTwoPImg_scaleBar_x_px', axTwoPImg_scaleBar_x_px)
	print('axTwoPImg_scaleBar_y_px', axTwoPImg_scaleBar_y_px)
	print('TwoPImg_scale_bar_len_px', TwoPImg_scale_bar_len_px)


	print('axCCfluoImg_scaleBar_x_px', axCCfluoImg_scaleBar_x_px)
	print('axCCfluoImg_scaleBar_y_px', axCCfluoImg_scaleBar_y_px)
	print('CCfluoImg_scale_bar_len_px', CCfluoImg_scale_bar_len_px)


	print('axConfImg_scaleBar_x_px', axConfImg_scaleBar_x_px)
	print('axConfImg_scaleBar_y_px', axConfImg_scaleBar_y_px)
	print('ConfImg_scale_bar_len_px', ConfImg_scale_bar_len_px)

	fluorophore_y_offset = 0.025
	axConfImg_fluorophore_y_offset = plot_utils.find_aligned_pos_of_panelLabel(ref_xy_span=TwoPImg_xy_span, target_xy_span=ConfImg_xy_span, ref_position=fluorophore_y_offset, direction='vertical')


	data_ylabel_position=plot_setting.data_ylabel_position

	matplotlib.rcParams['font.sans-serif'] = "Arial"
	matplotlib.rcParams['font.family'] = "sans-serif"

	xaxis = adjusted_timeSec_trim


	fig = plt.figure(facecolor='w', figsize=(A4_y, A4_x), dpi=600, constrained_layout=True)
	#fig.subplots_adjust(left=0.0617, right = 0.466, top = 0.9464, bottom = 0.478, wspace = 0, hspace = 1000) for 4 ROIs
	fig.subplots_adjust(left=0.0617, right = 0.466, top = 0.9464, bottom = 0.32, wspace = 0, hspace = 1000)
	normA = matplotlib.colors.Normalize(vmin=0.0,vmax=255.0)

	fig.suptitle(TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num, fontsize=8, fontname='Arial', x=0.26)

	axConfImg = plt.subplot2grid((fig_span[1],fig_span[0]),(ConfImg_origin[1], ConfImg_origin[0]),rowspan=ConfImg_xy_span[1],colspan=ConfImg_xy_span[0])
	axConfImg.spines['bottom'].set_visible(False)
	axConfImg.spines['top'].set_visible(False)
	axConfImg.spines['right'].set_visible(False)
	axConfImg.spines['left'].set_visible(False)
	axConfImg.get_xaxis().set_visible(False)
	axConfImg.get_yaxis().set_visible(False)
	#axConfImg.set_axis_off()
	axConfImg.imshow(BrainVNCImg, origin='upper',norm=normA, aspect = 'equal')
	axConfImg.plot([axConfImg_scaleBar_x_px, axConfImg_scaleBar_x_px+ConfImg_scale_bar_len_px], [axConfImg_scaleBar_y_px, axConfImg_scaleBar_y_px], color='w',linewidth=plot_setting.data_trace_width*2)
	PanelA=plt.text(Ref_Panellabel_pos[0],axConfImg_label_y, 'A', transform=axConfImg.transAxes, color='w',size=8, fontname='Arial', fontweight='bold')
	_40um=plt.text(Ref_Panellabel_pos[0],axConfImg_scaleBar_y+1.1*axConfImg_fluorophore_y_offset, '40 μm', transform=axConfImg.transAxes, color='w',size=6, fontname='Arial', fontweight='bold')
	smFP=plt.text(1-Ref_Panellabel_pos[0], axConfImg_scaleBar_y-axConfImg_fluorophore_y_offset, 'smFP\n', transform=axConfImg.transAxes, color='lime',size=6, fontname='Arial', fontweight='bold', ha='right', va='bottom')
	nc82=plt.text(1-Ref_Panellabel_pos[0], axConfImg_scaleBar_y-axConfImg_fluorophore_y_offset, '\nnc82', transform=axConfImg.transAxes, color='b',size=6, fontname='Arial', fontweight='bold', ha='right', va='bottom')


	axTwoPImg = plt.subplot2grid((fig_span[1],fig_span[0]),(TwoPImg_origin[1], TwoPImg_origin[0]),rowspan=TwoPImg_xy_span[1],colspan=TwoPImg_xy_span[0])
	axTwoPImg.spines['bottom'].set_visible(False)
	axTwoPImg.spines['top'].set_visible(False)
	axTwoPImg.spines['right'].set_visible(False)
	axTwoPImg.spines['left'].set_visible(False)
	axTwoPImg.get_xaxis().set_visible(False)
	axTwoPImg.get_yaxis().set_visible(False)
	#axTwoPImg.set_axis_off()
	axTwoPImg.imshow(TwoPImg, origin='upper',norm=normA, aspect = 'equal')
	axTwoPImg.plot([axTwoPImg_scaleBar_x_px, axTwoPImg_scaleBar_x_px+TwoPImg_scale_bar_len_px], [axTwoPImg_scaleBar_y_px, axTwoPImg_scaleBar_y_px], color='w',linewidth=plot_setting.data_trace_width*2)
	PanelB=plt.text(Ref_Panellabel_pos[0],Ref_Panellabel_pos[1], 'B', transform=axTwoPImg.transAxes, color='w',size=8, fontname='Arial', fontweight='bold')
	_5um=plt.text(Ref_Panellabel_pos[0], Ref_Panel_scaleBar_pos[1]+1.1*fluorophore_y_offset, '5 μm', transform=axTwoPImg.transAxes, color='w',size=6, fontname='Arial', fontweight='bold')
	OpGCaMP6f=plt.text(1-Ref_Panellabel_pos[0], Ref_Panel_scaleBar_pos[1]-fluorophore_y_offset, 'OpGCaMP6f\n', transform=axTwoPImg.transAxes, color='cyan',size=6, fontname='Arial', fontweight='bold', ha='right', va='bottom')
	tdtomato=plt.text(1-Ref_Panellabel_pos[0], Ref_Panel_scaleBar_pos[1]-fluorophore_y_offset, '\ntdtomato', transform=axTwoPImg.transAxes, color='r',size=6, fontname='Arial', fontweight='bold', ha='right', va='bottom')


	axCCfluoImg = plt.subplot2grid((fig_span[1],fig_span[0]),(CCfluoImg_origin[1], CCfluoImg_origin[0]),rowspan=CCfluoImg_xy_span[1],colspan=CCfluoImg_xy_span[0])
	axCCfluoImg.spines['bottom'].set_visible(False)
	axCCfluoImg.spines['top'].set_visible(False)
	axCCfluoImg.spines['right'].set_visible(False)
	axCCfluoImg.spines['left'].set_visible(False)
	axCCfluoImg.get_xaxis().set_visible(False)
	axCCfluoImg.get_yaxis().set_visible(False)
	#axCCfluoImg.set_axis_off()
	axCCfluoImg.imshow(CCfluoImg, origin='upper',norm=normA, aspect = 'equal')
	axCCfluoImg.plot([axCCfluoImg_scaleBar_x_px, axCCfluoImg_scaleBar_x_px+CCfluoImg_scale_bar_len_px], [axCCfluoImg_scaleBar_y_px, axCCfluoImg_scaleBar_y_px ], color='w',linewidth=plot_setting.data_trace_width*2)	
	PanelC=plt.text(Ref_Panellabel_pos[0],Ref_Panellabel_pos[1], 'C', transform=axCCfluoImg.transAxes, color='w',size=8, fontname='Arial', fontweight='bold')	
	_5um=plt.text(Ref_Panellabel_pos[0], Ref_Panel_scaleBar_pos[1]+1.1*fluorophore_y_offset, '5 μm', transform=axCCfluoImg.transAxes, color='w',size=6, fontname='Arial', fontweight='bold')
	Fluorescein=plt.text(1-Ref_Panellabel_pos[0], Ref_Panel_scaleBar_pos[1]-fluorophore_y_offset, 'Fluorescein\n', transform=axCCfluoImg.transAxes, color='cyan',size=6, fontname='Arial', fontweight='bold', ha='right', va='bottom')
	tdtomato=plt.text(1-Ref_Panellabel_pos[0], Ref_Panel_scaleBar_pos[1]-fluorophore_y_offset, '\ntdtomato', transform=axCCfluoImg.transAxes, color='r',size=6, fontname='Arial', fontweight='bold', ha='right', va='bottom')


	axBehlabels = plt.subplot2grid((fig_span[1],fig_span[0]),(Behlabels_origin[1], Behlabels_origin[0]),rowspan=Behlabels_xy_span[1],colspan=Behlabels_xy_span[0])
	axBehlabels.spines['bottom'].set_visible(False)
	axBehlabels.spines['top'].set_visible(False)
	axBehlabels.spines['right'].set_visible(False)
	axBehlabels.spines['left'].set_visible(False)
	axBehlabels.get_xaxis().set_visible(False)
	axBehlabels.get_yaxis().set_visible(False)

	PanelD=plt.text(Ref_Panellabel_pos[0], Ref_Panellabel_pos[1]-0.36,'D', transform=axBehlabels.transAxes, color='k',size=8, fontname='Arial', fontweight='bold')

	box_font_size=5


	F_Walk=plt.text(0.055,0.39, 'F.W.', transform=axBehlabels.transAxes, color='w', size=box_font_size, weight='bold')
	F_Walk.set_bbox(dict(facecolor=plot_setting.FW_color, edgecolor='none', alpha=0.7))

	B_Walk=plt.text(0.132,0.39, 'B.W.', transform=axBehlabels.transAxes, color='k',size=box_font_size, weight='bold')
	B_Walk.set_bbox(dict(facecolor=plot_setting.BW_color, edgecolor='none', alpha=0.5))

	push=plt.text(0.211,0.39, 'Push', transform=axBehlabels.transAxes, color='k',size=box_font_size, weight='bold')
	push.set_bbox(dict(facecolor=plot_setting.Push_color, edgecolor='none', alpha=0.5))

	Rest=plt.text(0.294,0.39, 'Rest', transform=axBehlabels.transAxes, color='k',size=box_font_size, weight='bold')
	Rest.set_bbox(dict(facecolor=plot_setting.rest_color, edgecolor='none', alpha=0.5))

	E_groom=plt.text(0.372,0.39, 'Eye groom', transform=axBehlabels.transAxes, color='k',size=box_font_size, weight='bold')
	E_groom.set_bbox(dict(facecolor=plot_setting.E_groom_color, edgecolor='none', alpha=0.5))

	A_groom=plt.text(0.512,0.39, 'Ant. groom', transform=axBehlabels.transAxes, color='k',size=box_font_size, weight='bold')
	A_groom.set_bbox(dict(facecolor=plot_setting.A_groom_color, edgecolor='none', alpha=0.5))

	FL_groom=plt.text(0.656,0.39, 'Fl. rub', transform=axBehlabels.transAxes, color='w',size=box_font_size, weight='bold')
	FL_groom.set_bbox(dict(facecolor=plot_setting.FL_groom_color, edgecolor='none', alpha=0.5))

	Abd_groom=plt.text(0.752,0.39, 'Abd. groom', transform=axBehlabels.transAxes, color='k',size=box_font_size, weight='bold')
	Abd_groom.set_bbox(dict(facecolor=plot_setting.Abd_groom_color, edgecolor='none', alpha=0.5))

	HL_groom=plt.text(0.901,0.39, 'Hl. rub', transform=axBehlabels.transAxes, color='k',size=box_font_size, weight='bold')
	HL_groom.set_bbox(dict(facecolor=plot_setting.HL_groom_color, edgecolor='none', alpha=0.5))

	PER=plt.text(1,0.39, 'PE', transform=axBehlabels.transAxes, color='k',size=box_font_size, weight='bold')
	PER.set_bbox(dict(facecolor=plot_setting.PER_color, edgecolor='none', alpha=0.5))
	

	

	axCO2 = plt.subplot2grid((fig_span[1],fig_span[0]),(CO2_origin[1], CO2_origin[0]),rowspan=CO2_xy_span[1],colspan=CO2_xy_span[0])
	axPER = plt.subplot2grid((fig_span[1],fig_span[0]),(PER_origin[1], PER_origin[0]),rowspan=PER_xy_span[1],colspan=PER_xy_span[0])
	axAP = plt.subplot2grid((fig_span[1],fig_span[0]),(AP_origin[1], AP_origin[0]),rowspan=AP_xy_span[1],colspan=AP_xy_span[0])
	axML = plt.subplot2grid((fig_span[1],fig_span[0]),(ML_origin[1], ML_origin[0]),rowspan=ML_xy_span[1],colspan=ML_xy_span[0])
	axYaw = plt.subplot2grid((fig_span[1],fig_span[0]),(AP_origin[1], AP_origin[0]),rowspan=Yaw_xy_span[1],colspan=Yaw_xy_span[0])
	ROI_origin_x_temp=ROI_origin[1]
	for i in range(0, len(GC_set_DD_trim)):
		axGC = 'axGC' + str(i)
		vars()[axGC] = plt.subplot2grid((fig_span[1],fig_span[0]),(ROI_origin_x_temp, ROI_origin[0]),rowspan=ROI_xy_span[1],colspan=ROI_xy_span[0])
		ROI_origin_x_temp+=ROI_xy_span[1]



	tick_nbins=1

	axPER = plt.subplot2grid((fig_span[1],fig_span[0]),(PER_origin[1], PER_origin[0]),rowspan=PER_xy_span[1],colspan=PER_xy_span[0])
	axPER.plot(xaxis, PER_exten_len_DD_trim, label = 'PER', color='k',linewidth=plot_setting.data_trace_width)
	axPER.yaxis.set_major_locator(ticker.MaxNLocator(nbins=tick_nbins, min_n_ticks=2, integer=True))
	axPER.set_xlim(0,time_dur)
	if max(PER_exten_len_DD_trim)<50:
		PER_max=50
	else:
		PER_max=max(PER_exten_len_DD_trim)
	axPER.set_ylim(min(PER_exten_len_DD_trim), PER_max)
	axPER.spines['bottom'].set_visible(False)
	axPER.spines['top'].set_visible(False)
	axPER.spines['right'].set_visible(False)
	axPER.spines['left'].set_color('black')
	axPER.get_xaxis().set_visible(False)
	axPER.get_xaxis().tick_bottom()
	axPER.get_yaxis().tick_left()
	axPER.get_yaxis().set_label_coords(data_ylabel_position[0],data_ylabel_position[1])
	axPER.tick_params(axis='both', colors='k',top=False, right=False,labelsize=6, length=2) 
	axPER.get_yaxis().set_label_coords(plot_setting.data_ylabel_position[0],plot_setting.data_ylabel_position[1])
	axPER.set_ylabel('PE length \n(px)',size=6, color='k', rotation=0, fontname='Arial', va='center')


	axCO2 = plt.subplot2grid((fig_span[1],fig_span[0]),(CO2_origin[1], CO2_origin[0]),rowspan=CO2_xy_span[1],colspan=CO2_xy_span[0])
	axCO2.plot(xaxis, CO2puff_DD_trim, label = 'CO2', color=plot_setting.CO2_color,linewidth=plot_setting.data_trace_width)
	axCO2.yaxis.set_major_locator(ticker.MaxNLocator(nbins=tick_nbins, min_n_ticks=2, integer=True))
	axCO2.set_xlim(0,time_dur)
	axCO2.set_ylim(0,1)
	axCO2.spines['bottom'].set_visible(False)
	axCO2.spines['top'].set_visible(False)
	axCO2.spines['right'].set_visible(False)
	axCO2.spines['left'].set_color('black')
	axCO2.get_xaxis().set_visible(False)
	axCO2.get_xaxis().tick_bottom()
	axCO2.get_yaxis().tick_left()
	axCO2.get_yaxis().set_label_coords(data_ylabel_position[0],data_ylabel_position[1])
	axCO2.tick_params(axis='both', colors='k',top=False, right=False,labelsize=6, length=2)
	axCO2.get_yaxis().set_label_coords(plot_setting.data_ylabel_position[0],plot_setting.data_ylabel_position[1])
	axCO2.set_ylabel(r'$\rm{CO}_\mathrm{2}$' +'\npuff',size=6, color='k', rotation=0, fontname='Arial', va='center')

	axAP = plt.subplot2grid((fig_span[1],fig_span[0]),(AP_origin[1], AP_origin[0]),rowspan=AP_xy_span[1],colspan=AP_xy_span[0])
	axAP.plot(xaxis, velForw_mm_trim, label = 'AP', color=plot_setting.AP_color,linewidth=plot_setting.data_trace_width)
	axAP.axhline(0, linestyle='dashed',color=plot_setting.axhline_color,linewidth=plot_setting.axhline_width)
	#axAP.yaxis.set_major_locator(ticker.MaxNLocator(nbins=tick_nbins, min_n_ticks=2, integer=True))
	axAP.yaxis.set_major_locator(ticker.FixedLocator(AP_tick_range))
	axAP.set_xlim(0,time_dur)
	axAP.set_ylim(min_AP,max_AP)
	axAP.spines['bottom'].set_visible(False)
	axAP.spines['top'].set_visible(False)
	axAP.spines['right'].set_visible(False)
	axAP.spines['left'].set_color('black')
	axAP.get_xaxis().set_visible(False)
	axAP.get_xaxis().tick_bottom()
	axAP.get_yaxis().tick_left()
	axAP.get_yaxis().set_label_coords(data_ylabel_position[0],data_ylabel_position[1])
	axAP.tick_params(axis='both', colors='k',top=False, right=False,labelsize=6, length=2)
	axAP.get_yaxis().set_label_coords(plot_setting.data_ylabel_position[0],plot_setting.data_ylabel_position[1])
	axAP.set_ylabel(r'$\rm{V}_\mathrm{forward}$'+'\n'+r'$\rm{(deg. s}^\mathrm{-1}$'+')',size=6, color='k', rotation=0, fontname='Arial', va='center')

	axML = plt.subplot2grid((fig_span[1],fig_span[0]),(ML_origin[1], ML_origin[0]),rowspan=ML_xy_span[1],colspan=ML_xy_span[0])
	axML.plot(xaxis, velSide_mm_trim, label = 'ML', color=plot_setting.ML_color,linewidth=plot_setting.data_trace_width)
	axML.axhline(0, linestyle='dashed',color=plot_setting.axhline_color,linewidth=plot_setting.axhline_width)
	#axML.yaxis.set_major_locator(ticker.MaxNLocator(nbins=tick_nbins, min_n_ticks=2, integer=True))
	axML.yaxis.set_major_locator(ticker.FixedLocator(ML_tick_range))
	axML.set_xlim(0,time_dur)
	axML.set_ylim(min_ML,max_ML)
	axML.spines['bottom'].set_visible(False)
	axML.spines['top'].set_visible(False)
	axML.spines['right'].set_visible(False)
	axML.spines['left'].set_color('black')
	axML.get_xaxis().set_visible(False)
	axML.get_xaxis().tick_bottom()
	axML.get_yaxis().tick_left()
	axML.get_yaxis().set_label_coords(data_ylabel_position[0],data_ylabel_position[1])
	axML.tick_params(axis='both', colors='k',top=False, right=False,labelsize=6, length=2)
	axML.get_yaxis().set_label_coords(plot_setting.data_ylabel_position[0],plot_setting.data_ylabel_position[1])
	axML.set_ylabel(r'$\rm{V}_\mathrm{side}$'+'\n'+r'$\rm{(deg. s}^\mathrm{-1}$'+')',size=6, color='k', rotation=0, fontname='Arial', va='center')

	axYaw = plt.subplot2grid((fig_span[1],fig_span[0]),(Yaw_origin[1], Yaw_origin[0]),rowspan=Yaw_xy_span[1],colspan=Yaw_xy_span[0])
	axYaw.plot(xaxis, velTurn_deg_trim, label = 'Yaw', color=plot_setting.Yaw_color,linewidth=plot_setting.data_trace_width)
	axYaw.axhline(0, linestyle='dashed',color=plot_setting.axhline_color,linewidth=plot_setting.axhline_width)
	#axYaw.yaxis.set_major_locator(ticker.MaxNLocator(nbins=tick_nbins, min_n_ticks=2, integer=True))
	axYaw.yaxis.set_major_locator(ticker.FixedLocator(Yaw_tick_range))
	axYaw.set_xlim(0,time_dur)
	axYaw.set_ylim(min_Yaw,max_Yaw)
	axYaw.spines['bottom'].set_visible(False)
	axYaw.spines['top'].set_visible(False)
	axYaw.spines['right'].set_visible(False)
	axYaw.spines['left'].set_color('black')
	axYaw.get_xaxis().set_visible(False)
	axYaw.get_xaxis().tick_bottom()
	axYaw.get_yaxis().tick_left()
	axYaw.get_yaxis().set_label_coords(data_ylabel_position[0],data_ylabel_position[1])
	axYaw.tick_params(axis='both', colors='k',top=False, right=False, labelsize=6, length=2)
	axYaw.get_yaxis().set_label_coords(plot_setting.data_ylabel_position[0],plot_setting.data_ylabel_position[1])
	axYaw.set_ylabel(r'$\rm{V}_\mathrm{turn}$'+'\n'+r'$\rm{(deg. s}^\mathrm{-1}$'+')',size=6, color='k', rotation=0, fontname='Arial', va='center')


	for i in range(0, len(GC_set_DD_trim)):

		axGC = 'axGC' + str(i)

		vars()[axGC] = plt.subplot2grid((fig_span[1],fig_span[0]),(ROI_origin[1], ROI_origin[0]),rowspan=ROI_xy_span[1],colspan=ROI_xy_span[0])
		
		vars()[axGC].plot(xaxis, GC_set_DD_trim[i][:], label = 'GC', color=plot_setting.GC_color,linewidth=plot_setting.data_trace_width)
		vars()[axGC].axhline(0, linestyle='dashed',color=plot_setting.axhline_color,linewidth=plot_setting.axhline_width)
		vars()[axGC].yaxis.set_major_locator(ticker.MaxNLocator(nbins=tick_nbins+1, min_n_ticks=2, integer=True))
		vars()[axGC].set_xlim(0,time_dur)
		vars()[axGC].set_ylim(min_GC,max_GC)
		vars()[axGC].spines['bottom'].set_visible(False)		
		vars()[axGC].spines['top'].set_visible(False)
		vars()[axGC].spines['right'].set_visible(False)
		vars()[axGC].spines['left'].set_color('black')
		vars()[axGC].get_xaxis().set_visible(False)
		vars()[axGC].get_xaxis().tick_bottom()
		vars()[axGC].get_yaxis().tick_left()
		vars()[axGC].get_yaxis().set_label_coords(data_ylabel_position[0],data_ylabel_position[1])
		vars()[axGC].tick_params(axis='both', colors='k',top=False, right=False,labelsize=6, length=2)
		vars()[axGC].get_yaxis().set_label_coords(plot_setting.data_ylabel_position[0],plot_setting.data_ylabel_position[1])
		vars()[axGC].set_ylabel('ROI '+str(i)+'\n'+r'$\Delta$'+'F/F (%)', size=6, color='k', rotation=0, fontname='Arial', va='center')

		if i == len(GC_set_DD_trim)-1:
			vars()[axGC].spines['bottom'].set_visible(True)
			vars()[axGC].spines['bottom'].set_color('black')
			vars()[axGC].get_xaxis().set_visible(True)
			vars()[axGC].tick_params(axis='x', colors='k',top='off',labelsize=6, length=2)
			vars()[axGC].set_xlabel('Time (s)',size=6, color='k', fontname='Arial')

		ROI_origin[1]+=ROI_xy_span[1]+spacer_xy_span[1]




	for key in EthoTimeDic_trim: 

		if key == 'rest_evt' or key=='forward_walk_evt' or key=='backward_walk_evt' or key=='eye_groom_evt' or key=='antennae_groom_evt' or key=='foreleg_groom_evt' or key=='hindleg_groom' or key=='Abdomen_groom_evt' or key=='push_evt':

			for a in range(0,len(EthoTimeDic_trim[key])):

				# print(key)
				# print(a)
				# print(EthoTimeDic_trim[key][a][0])
				# print(EthoTimeDic_trim[key][a][-1])

				alpha=0.5
				if key=='forward_walk_evt':
					alpha=0.7

				
				#axCO2.axvspan(EthoTimeDic_trim[key][a][0], EthoTimeDic_trim[key][a][-1], alpha=0.5, color=EthoColorCodeDic_trim[key], linewidth=0)
				axAP.axvspan(EthoTimeDic_trim[key][a][0], EthoTimeDic_trim[key][a][-1], alpha=alpha, color=EthoColorCodeDic_trim[key], linewidth=0)
				axML.axvspan(EthoTimeDic_trim[key][a][0], EthoTimeDic_trim[key][a][-1], alpha=alpha, color=EthoColorCodeDic_trim[key], linewidth=0)
				axYaw.axvspan(EthoTimeDic_trim[key][a][0], EthoTimeDic_trim[key][a][-1], alpha=alpha, color=EthoColorCodeDic_trim[key], linewidth=0)  

				for i in range(0, len(GC_set_DD_trim)):
					axGC = 'axGC' + str(i)
					vars()[axGC].axvspan(EthoTimeDic_trim[key][a][0], EthoTimeDic_trim[key][a][-1], alpha=alpha, color=EthoColorCodeDic_trim[key], linewidth=0)
		elif key=='PER_evt':
			for b in range(0,len(EthoTimeDic_trim[key])):
				axPER.axvspan(EthoTimeDic_trim[key][b][0], EthoTimeDic_trim[key][b][-1], alpha=alpha, color=EthoColorCodeDic_trim[key], linewidth=0)
				




	plt.savefig(str(outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '.png'), facecolor=fig.get_facecolor(), edgecolor='none', transparent=True)
	# plt.savefig(str(outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '_registered_not_resized.png'), facecolor=fig.get_facecolor(), edgecolor='none', transparent=True)
	# plt.savefig(str(outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '_registered_resized.png'), facecolor=fig.get_facecolor(), edgecolor='none', transparent=True)
	# plt.savefig(str(outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '_not_registered.png'), facecolor=fig.get_facecolor(), edgecolor='none', transparent=True)


	plt.savefig(str(outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '.pdf'), facecolor=fig.get_facecolor(), edgecolor='none', transparent=True)
	# plt.savefig(str(outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '.svg'), facecolor=fig.get_facecolor(), edgecolor='none', transparent=True) 
	
	plt.close(fig)




	print('Saving figure Done!!!')

	#todo: made another script to use local computer to copy the file from NAS. Do it as a .run file. 
	# os.system(str('cp ' + outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '.eps '+ outputFigureLocalDir))
	# os.system(str('cp ' + outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '.png '+ outputFigureLocalDir))
	# os.system(str('cp ' + outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '.svg '+ outputFigureLocalDir))





	return



def sorted_oriExperimentList_based_on_an_order(ori_list, base_list):

	# print('base_list', base_list)

	new_ori_list=[]

	new_base_w_eachGal4_list=[]
	for i, roi_id in enumerate(base_list):
		new_base_w_eachGal4_list.append(roi_id.split(' ')[0])

	# print('new_base_w_eachGal4_list', new_base_w_eachGal4_list)


	## remove repeated element in the list
	new_base_w_eachGal4_list=list(dict.fromkeys(new_base_w_eachGal4_list))
	# print('new_base_w_eachGal4_list', new_base_w_eachGal4_list)
	# print('len new_base_w_eachGal4_list', len(new_base_w_eachGal4_list))

	# print('len ori_list', len(ori_list))


	## find the corresponding index in the base list
	idx_of_ori_gal4_in_baseList=[]
	for i, gal4_cnt in enumerate(ori_list):

		# print('gal4_cnt', gal4_cnt[1].split('-')[0])

		idx_in_baseList=new_base_w_eachGal4_list.index(gal4_cnt[1].split('-')[0])

		# print('idx_in_baseList', idx_in_baseList)
		idx_of_ori_gal4_in_baseList.append(idx_in_baseList)

	# print('idx_of_ori_gal4_in_baseList', idx_of_ori_gal4_in_baseList)


	##sort the corresponding index list and propagate to the original list
	zipped_lists = zip(idx_of_ori_gal4_in_baseList, ori_list)
	sorted_zipped_lists = sorted(zipped_lists)
	sorted_ori_list = [element for _, element in sorted_zipped_lists]

	print('sorted_ori_list', sorted_ori_list)



	return sorted_ori_list





## main ##
NAS_Dir='/mnt/data/'
NAS_AN_Proj_Dir=NAS_Dir+'CLC/Ascending_Project/'


NAS_Dir='/mnt/data/'
local_Dir = '/Users/clc/Documents/EPFL/NeLy/Data/ANproj/'
local_AN_proj_Dir = local_Dir + 'Ascending_Project/'
NAS_AN_Proj_Dir = NAS_Dir+'CLC/Ascending_Project/'
workstation_dir='/mnt/internal_hdd/clc/'

AN_Proj_Dir = NAS_AN_Proj_Dir



manual_ROI_order_csv=pd.read_csv(workstation_dir+'from_florian/Ascending_analysis/output/row_order_manual.csv')
manual_ROI_order= manual_ROI_order_csv['x'].tolist()
# print('manual_ROI_order\n', manual_ROI_order)
# print('type manual_ROI_order', type(manual_ROI_order))


sorted_experiments=sorted_oriExperimentList_based_on_an_order(experiments, manual_ROI_order)





# check_file_existence(experiments, exp_type='confocal')
# check_file_existence(experiments, exp_type='cc512')
# check_file_existence(experiments, exp_type='TwoP')
# check_file_existence(experiments, exp_type='sync')




max_ROI_counts=find_max_ROIs(sorted_experiments)
print('max_ROI_counts', max_ROI_counts)
max_ROI_counts=10


video_frames=[]

count=1


for TwoP_date, TwoP_genotype, TwoP_fly, TwoP_recrd_num, TwP_frame, start_s, end_s, CC_fluorcn_num, conf_date, conf_genotype, conf_fly in sorted_experiments:

	print(TwoP_date, TwoP_genotype, TwoP_fly, TwoP_recrd_num, TwP_frame, start_s, end_s, CC_fluorcn_num, conf_date, conf_genotype, conf_fly)


	Gal4=TwoP_genotype.split('-')[0]
	ThorsyncDir_inNas = NAS_Dir+'2photonData/CLC/'+TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-sync-'+TwoP_recrd_num + '/'
	Thorsync_CC_Dir_inNAS = NAS_Dir+'2photonData/CLC/'+TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-sync-'+CC_fluorcn_num + '/'

	TwoP_raw_Dir = NAS_Dir+'CLC/2photonData/CLC/'+TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '/'
	CCfluo_raw_Dir = NAS_Dir+'CLC/2photonData/CLC/'+TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-'+CC_fluorcn_num + '/'

	print('TwoP_raw_Dir', TwoP_raw_Dir)
	print('CCfluo_raw_Dir', CCfluo_raw_Dir)

	dataDir = AN_Proj_Dir + Gal4 +'/2P/' + TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '/'
	pathDic=dataDir+'output/'
	pathForRGB =dataDir +'/2Pimg/'
	pathForTwoPimgAxoID = pathDic +'ROI_auto/final/'

	# ConfocalImg_dir = AN_Proj_Dir + Gal4 + '/Confocal/Best_image/'
	ConfocalImg_dir = AN_Proj_Dir + Gal4 + '/Confocal/Registered/'

	# BrainImgDir = ConfocalImg_dir + conf_date + '-' + conf_fly + '-' + conf_genotype + '-brain.tif'
	# VNCImgDir = ConfocalImg_dir + conf_date + '-' + conf_fly + '-' + conf_genotype + '-VNC.tif'
	BrainImgDir = ConfocalImg_dir + conf_date + '-' + conf_fly + '-' + conf_genotype + '-brain.tif'
	VNCImgDir = ConfocalImg_dir + conf_date + '-' + conf_fly + '-' + conf_genotype + '-VNC.tif'
	VNCImg_resized_Dir = ConfocalImg_dir + conf_date + '-' + conf_fly + '-' + conf_genotype + '-VNC_RGB_resized.tif'



	CCfluoImgDir = AN_Proj_Dir + Gal4 +'/2P/' + TwoP_date+'/'+TwoP_genotype+'-'+TwoP_fly+'/'+TwoP_genotype+'-'+TwoP_fly+'-'+CC_fluorcn_num + '/2Pimg/AVG_warped_RGB.tif'

	outputFigureNasDir = NAS_AN_Proj_Dir+'_Summary/Figures/supp_figures/' +  TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '/'
	#outputFigureLocalDir = '/Users/clc/Documents/EPFL/NeLy/manuscript/2021_Ascending_neurons_screen/Figures/SuppFig/'
	outputFigureNasDir_each_recrd = pathDic + 'Events/'

	outputFigureNasDir=NAS_AN_Proj_Dir+'_Summary/Figures/supp_figures/'+Gal4+'/'

	if not os.path.exists(outputFigureNasDir):
		os.makedirs(outputFigureNasDir)

	output_Sum_FigureNasDir=NAS_AN_Proj_Dir+'_Summary/Figures/supp_figures/individual_Gal4_plot/'
	if not os.path.exists(output_Sum_FigureNasDir):
		os.makedirs(output_Sum_FigureNasDir)	

	

	
	if not os.path.exists(BrainImgDir):
		BrainImg=np.zeros((1023,1023,3), np.uint8)
		ConfImg_pixelSizeUM=np.inf
	else:
		BrainImg = io.imread(BrainImgDir)
		

	
	if not os.path.exists(VNCImgDir):
		VNCImg=np.zeros((1023,1023,3), np.uint8)
	else:
		VNCImg = io.imread(VNCImgDir)
		



	BrainImg_h=np.shape(BrainImg)[0]
	BrainImg_w=np.shape(BrainImg)[1]
	print('BrainImg_h', BrainImg_h)
	print('BrainImg_w', BrainImg_w)

	VNCImg = cv2.resize(VNCImg, (BrainImg_w, BrainImg_h),interpolation = cv2.INTER_AREA)

	VNCImg_h=np.shape(VNCImg)[0]
	VNCImg_w=np.shape(VNCImg)[1]
	print('VNCImg_h', VNCImg_h)
	print('VNCImg_w', VNCImg_w)

	BrainImg=BrainImg[147:147+760, int(BrainImg_w/2-760/2):int(BrainImg_w/2+760/2)]
	print('shape BrainImg', np.shape(BrainImg))
	BrainImg=Stitch_frame_as_same_ratio_of_RefImg(BrainImg, RefImg=np.zeros((760,760+52*2,3), np.uint8))

	VNCImg=VNCImg[9:9+970, int(VNCImg_w/2-760/2):int(VNCImg_w/2+760/2)]
	print('shape VNCImg', np.shape(VNCImg))
	VNCImg=Stitch_frame_as_same_ratio_of_RefImg(VNCImg, RefImg=np.zeros((970,760+52*2,3), np.uint8))

	ConfImg_pixelSizeUM = 0.521 #um



	#sys.exit(0)

	# VNC_resized_Img = io.imread(VNCImg_resized_Dir)
	# VNCImg_resized_h=np.shape(VNC_resized_Img)[0]
	# VNCImg_resized_w=np.shape(VNC_resized_Img)[1]
	# print('VNCImg_resized_h', VNCImg_resized_h)
	# print('VNCImg_resized_w', VNCImg_resized_w)
	# Brain_resized_Img = overlay_small_img_to_big_img(np.asarray(BrainImg).copy(), np.zeros((VNCImg_resized_h,VNCImg_resized_w,3), np.uint8))


	BrainVNCImg = cv2.vconcat([BrainImg, VNCImg])
	print('shape BrainVNCImg', np.shape(BrainVNCImg))	
	# BrainVNC_resized_Img = cv2.vconcat([Brain_resized_Img, VNC_resized_Img])
	# print('shape BrainVNC_resized_Img', np.shape(BrainVNC_resized_Img))	

	# BrainVNCImg=BrainVNC_resized_Img



	ideal_2Pframe_ratio=683/512

	if os.path.exists(pathForTwoPimgAxoID+'RGB_seg.tif'):
		RGB = io.imread(pathForTwoPimgAxoID+'RGB_seg.tif')
		TwoPImg = RGB[TwP_frame-1,:,:,:]
		if '{:.2f}'.format(np.shape(TwoPImg)[1]/np.shape(TwoPImg)[0]) != '{:.2f}'.format(ideal_2Pframe_ratio):
			print('stitching TwoP image')
			TwoPImg = Stitch_frame_as_same_ratio_of_RefImg(TwoPImg, RefImg=np.zeros((np.shape(TwoPImg)[0],int(np.shape(TwoPImg)[0]*ideal_2Pframe_ratio),3), np.uint8))
	else:
		TwoPImg=np.zeros((512,683,3), np.uint8)
	print('shape TwoPImg', np.shape(TwoPImg))


	if os.path.exists(CCfluoImgDir):
		CCfluoImg_original = io.imread(CCfluoImgDir)
		if '{:.2f}'.format(np.shape(CCfluoImg_original)[1]/np.shape(CCfluoImg_original)[0]) != '{:.2f}'.format(ideal_2Pframe_ratio):
			print('stitching CC image')
			CCfluoImg = Stitch_frame_as_same_ratio_of_RefImg(CCfluoImg_original, RefImg=np.zeros((np.shape(TwoPImg)[0],int(np.shape(TwoPImg)[0]*ideal_2Pframe_ratio),3), np.uint8))
	else:
		CCfluoImg=np.zeros((512,683,3), np.uint8)
	print('shape CCfluoImg', np.shape(CCfluoImg))
	

	if os.path.exists(TwoP_raw_Dir):
		TwoP_xml_metadata = utils2p.Metadata(TwoP_raw_Dir + 'Experiment.xml')
		TwoP_pixelSizeUM=float(TwoP_xml_metadata.get_metadata_value('LSM','pixelSizeUM'))
	else:
		print("TwoP_raw_Dir doesn't exists. TwoP_pixelSizeUM is forced to be 0.223 um")
		TwoP_pixelSizeUM = np.inf

	if os.path.exists(CCfluo_raw_Dir):
		CCfluo_xml_metadata = utils2p.Metadata(CCfluo_raw_Dir + 'Experiment.xml')
		CCfluo_pixelSizeUM=float(CCfluo_xml_metadata.get_metadata_value('LSM','pixelSizeUM'))
	else:
		print("CCfluo_raw_Dir doesn't exists. CCfluo_pixelSizeUM is forced to be 0.171 um")
		CCfluo_pixelSizeUM = np.inf
	
	
	

	print('TwoP_pixelSizeUM', TwoP_pixelSizeUM)
	print('CCfluo_pixelSizeUM', CCfluo_pixelSizeUM)
	print('ConfImg_pixelSizeUM', ConfImg_pixelSizeUM)

	Desired_TwoP_scale_bar = 5 #um
	Desired_ConfImg_scale_bar = 40 #um

	Desired_TwoP_scale_bar_px = Desired_TwoP_scale_bar/TwoP_pixelSizeUM
	Desired_ConfImg_scale_bar_px = Desired_ConfImg_scale_bar/ConfImg_pixelSizeUM


	# BrainVNCImg=plot_utils.draw_scale_bar(BrainVNCImg, ConfImg_pixelSizeUM, Desired_ConfImg_scale_bar, pos=[ScaleBar_pos_BrainVNCImg_h, ScaleBar_pos_BrainVNCImg_v])
	# TwoPImg=plot_utils.draw_scale_bar(TwoPImg, TwoP_pixelSizeUM, Desired_TwoP_scale_bar, pos=Ref_Panel_scaleBar_pos)
	# CCfluoImg=plot_utils.draw_scale_bar(CCfluoImg, CCfluo_pixelSizeUM, Desired_TwoP_scale_bar, pos=Ref_Panel_scaleBar_pos)

	# cv2.imshow('BrainVNCImg', BrainVNCImg)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()


	
	#TwoP_img_width_scale = plot_utils.find_widthScale_in_xml(ThorsyncDir_inNas)
	#CCfluoImg_width_scale = plot_utils.find_widthScale_in_xml(Thorsync_CC_Dir_inNAS)


	# frameCntr, EdgeCam_Stair, risingEdgeCam, GC_set, Rest_bin_trace, Walk_bin_trace, Groom_bin_trace, \
	# Etho_Idx_Dic, Etho_Timesec_Dic, Etho_Colorcode_Dic, coarse_beh,\
	# CO2puff, timeSec, velForw_mm, velSide_mm, velTurn_deg, \
	# startVidIdx, stopVidIdx \
	Beh_Jpos_GC_DicData = sync_utils.open_GC_beh_sync_DicData(pathDic, filename='SyncDic_7CamBeh_BW_20210619_GC-RES.p')


	GC_set = Beh_Jpos_GC_DicData['GCset']

	PER_exten_len = Beh_Jpos_GC_DicData['PER_exten_len']
	CO2puff = Beh_Jpos_GC_DicData['CO2puff']
	timeSec = Beh_Jpos_GC_DicData['timeSec']
	velForw_mm = Beh_Jpos_GC_DicData['velForw']
	velSide_mm = Beh_Jpos_GC_DicData['velSide']
	velTurn_deg = Beh_Jpos_GC_DicData['velTurn']
	Etho_Timesec_Dic = Beh_Jpos_GC_DicData['Etho_Timesec_Dic']
	Etho_Idx_Dic = Beh_Jpos_GC_DicData['Etho_Idx_Dic']

	PER_exten_len=Beh_Jpos_GC_DicData['PER_exten_len']

	bin_restDD=Beh_Jpos_GC_DicData['rest']
	bin_FWDD=Beh_Jpos_GC_DicData['forward_walk']
	bin_BWDD=Beh_Jpos_GC_DicData['backward_walk']
	bin_EGDD=Beh_Jpos_GC_DicData['eye_groom']
	bin_AGDD=Beh_Jpos_GC_DicData['antennae_groom']
	bin_FLGDD=Beh_Jpos_GC_DicData['foreleg_groom']
	bin_HLDD=Beh_Jpos_GC_DicData['hindleg_groom']
	bin_AbdDD=Beh_Jpos_GC_DicData['Abd_groom']
	bin_PERDD=Beh_Jpos_GC_DicData['PER']
	bin_PushDD=Beh_Jpos_GC_DicData['Push']


	if end_s>timeSec[-1]:
		end_s=int(timeSec[-1])


	GC_set_DD_trim=[]
	for GC_trace in GC_set:
		GC_trace_trim=sync_utils.trim_period(GC_trace, timeSec, start_s, end_s)
		GC_set_DD_trim.append(GC_trace_trim)

	timeSec_trim=sync_utils.trim_period(timeSec, timeSec, start_s, end_s)
	velForw_mm_trim=sync_utils.trim_period(velForw_mm, timeSec, start_s, end_s)
	velSide_mm_trim=sync_utils.trim_period(velSide_mm, timeSec, start_s, end_s)
	velTurn_deg_trim=sync_utils.trim_period(velTurn_deg, timeSec, start_s, end_s)

	CO2puff_DD_trim=sync_utils.trim_period(CO2puff, timeSec, start_s, end_s)
	PER_exten_len_DD_trim=sync_utils.trim_period(PER_exten_len, timeSec, start_s, end_s)

	restDD_trim=sync_utils.trim_period(bin_restDD, timeSec, start_s, end_s)
	FWDD_trim=sync_utils.trim_period(bin_FWDD, timeSec, start_s, end_s)
	BWDD_trim=sync_utils.trim_period(bin_BWDD, timeSec, start_s, end_s)
	EGDD_trim=sync_utils.trim_period(bin_EGDD, timeSec, start_s, end_s)
	AGDD_trim=sync_utils.trim_period(bin_AGDD, timeSec, start_s, end_s)
	FLGDD_trim=sync_utils.trim_period(bin_FLGDD, timeSec, start_s, end_s)
	HLDD_trim=sync_utils.trim_period(bin_HLDD, timeSec, start_s, end_s)
	AbdDD_trim=sync_utils.trim_period(bin_AbdDD, timeSec, start_s, end_s)
	PERDD_trim=sync_utils.trim_period(bin_PERDD, timeSec, start_s, end_s)
	PushDD_trim=sync_utils.trim_period(bin_PushDD, timeSec, start_s, end_s)

	time_dur = timeSec_trim[-1]-timeSec_trim[0]
	adjusted_timeSec_trim = np.linspace(0, time_dur, len(timeSec_trim))

	print('len adjusted_timeSec_trim', len(adjusted_timeSec_trim))
	print('len restDD_trim', len(restDD_trim))



	EthoIdxDic_trim, EthoTimeDic_trim, EthoColorCodeDic_trim=sync_utils.Package_beh_bin_trace_into_idx_time(\
		restDD_trim, 
		FWDD_trim, 
		BWDD_trim, 
		EGDD_trim, 
		AGDD_trim, 
		FLGDD_trim, 
		HLDD_trim, 
		AbdDD_trim, 
		PushDD_trim,
		PERDD_trim, 
		adjusted_timeSec_trim)




	if start_s<1:
		opflow_start=1000
	else:
		opflow_start=0

	max_AP=np.nanmax(velForw_mm_trim[opflow_start:-1])
	min_AP=np.nanmin(velForw_mm_trim[opflow_start:-1])
	if max_AP>25:
		max_AP=25

	if abs(max_AP)<abs(min_AP):
		max_AP=abs(min_AP)
	elif abs(min_AP)<abs(max_AP):
		min_AP = (-1)*max_AP
	elif min_AP>0:
		min_AP=0
	AP_tick = plot_utils.find_nearest_nice_integer_of_postive_number(max_AP)
	AP_tick_range=[-AP_tick, AP_tick]

	print('max_AP', max_AP)
	print('min_AP', min_AP)
	print('AP_tick_range', AP_tick_range)

	max_ML=np.nanmax(velSide_mm_trim[opflow_start:-1])
	min_ML=np.nanmin(velSide_mm_trim[opflow_start:-1])

	if max_ML>11:
		max_ML=11
	if abs(min_ML)>11:
		min_ML=-11

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

	max_Yaw=np.nanmax(velTurn_deg_trim[opflow_start:-1])
	min_Yaw=np.nanmin(velTurn_deg_trim[opflow_start:-1])

	if max_Yaw>720:
		max_Yaw=720
	if abs(min_Yaw)>720:
		min_Yaw=-720

	if abs(max_Yaw)<abs(min_Yaw):
		max_Yaw=abs(min_Yaw)
	elif abs(min_Yaw)<abs(max_Yaw):
		min_Yaw = (-1)*max_Yaw
	elif min_Yaw>0:
		min_Yaw=0
	Yaw_tick = plot_utils.find_nearest_nice_integer_of_postive_number(max_Yaw)
	Yaw_tick_range=[-Yaw_tick, Yaw_tick]
	print('max_Yaw', max_Yaw)
	print('min_Yaw', min_Yaw)
	print('Yaw_tick_range', Yaw_tick_range)

	max_GC = np.nanmax(np.asarray(GC_set_DD_trim).flatten())
	if max_GC<80:
		max_GC=80
	min_GC = np.nanmin(np.asarray(GC_set_DD_trim).flatten())
	GC_range=[min_GC, max_GC]





	# beh_traces_for_plot={
	# 'CO2puff':CO2puff, 
	# 'Rest_bin_trace':Rest_bin_trace,
	# 'Walk_bin_trace':Walk_bin_trace,
	# 'Groom_bin_trace':Groom_bin_trace,
	# }
	# plot_utils.Plot_traces(series_set=beh_traces_for_plot, savepath=outputFigureNasDir+'beh_bin_traces.png')


	# beh_traces_trim_for_plot={
	# 'CO2puff_DD_trim':CO2puff_DD_trim, 
	# 'norm_restDD_trim':norm_restDD_trim,
	# 'norm_walkDD_trim':norm_walkDD_trim,
	# 'norm_groomDD_trim':norm_groomDD_trim,
	# }
	# plot_utils.Plot_traces(series_set=beh_traces_trim_for_plot, savepath=outputFigureNasDir+'beh_bin_trim_traces.png')



	Supp_figure()
	

	img_Gal4=cv2.imread(outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '.png')
	# img_Gal4=cv2.imread(outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '_registered_resized.png')
	# img_Gal4=cv2.imread(outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '_registered_not_resized.png')
	# img_Gal4=cv2.imread(outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '_not_registered.png')
	
	img_Gal4_w=np.shape(img_Gal4)[1]
	img_Gal4_h=np.shape(img_Gal4)[0]
	# print('img_Gal4_w', img_Gal4_w)
	# print('img_Gal4_h', img_Gal4_h)
	img_Gal4=cv2.putText(img_Gal4, str(count), (int(0.05*img_Gal4_w),int(0.05*img_Gal4_h)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)
	img_Gal4_crop=img_Gal4[0:4466, 0:2650]
	# img_Gal4_crop=img_Gal4[0:2512, 0:1307]
	cv2.imwrite(outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '_cropped.png', img_Gal4_crop)
	img_Gal4_crop_w=np.shape(img_Gal4_crop)[1]
	img_Gal4_crop_h=np.shape(img_Gal4_crop)[0]

	video_frames.append(img_Gal4_crop)

	shutil.copy(outputFigureNasDir + TwoP_date+'-'+TwoP_genotype+'-'+TwoP_fly+'-'+TwoP_recrd_num + '_cropped.png', output_Sum_FigureNasDir)




	count+=1




fps=0.5
video = cv2.VideoWriter( output_Sum_FigureNasDir+'/All_Gal4.avi', cv2.VideoWriter_fourcc('M','J','P','G'), fps, (img_Gal4_crop_w,img_Gal4_crop_h))
# video = cv2.VideoWriter( NAS_AN_Proj_Dir+'_Summary/Figures/supp_figures/All_Gal4.avi', cv2.VideoWriter_fourcc('M','J','P','G'), fps, (img_Gal4_crop_w,img_Gal4_crop_h))
# video = cv2.VideoWriter( NAS_AN_Proj_Dir+'_Summary/Figures/supp_figures/All_Gal4+registered_not_resized.avi', cv2.VideoWriter_fourcc('M','J','P','G'), fps, (img_Gal4_w,img_Gal4_h))
# video = cv2.VideoWriter( NAS_AN_Proj_Dir+'_Summary/Figures/supp_figures/All_Gal4_registered_resized.avi', cv2.VideoWriter_fourcc('M','J','P','G'), fps, (img_Gal4_w,img_Gal4_h))
# video = cv2.VideoWriter( NAS_AN_Proj_Dir+'_Summary/Figures/supp_figures/All_Gal4_not_registered.avi', cv2.VideoWriter_fourcc('M','J','P','G'), fps, (img_Gal4_w,img_Gal4_h))

for frame in video_frames:
	video.write(frame)
video.release()
































