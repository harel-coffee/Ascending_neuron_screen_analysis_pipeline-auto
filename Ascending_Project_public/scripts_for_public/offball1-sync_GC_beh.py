import numpy as np
import os
import sys
import pickle
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from skimage import io

import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.math_utils as math_utils
import utils.sync_utils as sync_utils
import utils.EventDetection_utils as EventDetection_utils
import utils.list_twoP_exp as list_twoP_exp






def Save_syncDic(dicDir, filename='sync.p'):

	frameCntr=np.asarray(FctrOk)
	GCset=np.asarray(GC_set_DD)

	Beh_GC_sync={}
	Beh_GC_sync.update({'frameCntr':frameCntr})
	Beh_GC_sync.update({'EdgeCam_Stair':EdgeCam_Stair_DD})
	Beh_GC_sync.update({'risingEdgeCam':risingEdgeCam})
	Beh_GC_sync.update({'timeSec':timeSec})


	Beh_GC_sync.update({'rest':norm_Beh_bin_restDD})
	Beh_GC_sync.update({'move':norm_Beh_bin_moveDD})
	Beh_GC_sync.update({'CO2puff':norm_CO2puffDD})

	Beh_GC_sync.update({'Etho_Idx_Dic':EthoIdxDic})
	Beh_GC_sync.update({'Etho_Timesec_Dic':EthoTimeDic})


	Beh_GC_sync.update({'GCset':GCset})	

	Beh_GC_sync.update({'startVidIdx':startCamIdx})
	Beh_GC_sync.update({'stopVidIdx':stopCamIdx})


	GC_beh=[
	GCset[0][1000:],
	norm_Beh_bin_restDD[1000:],
	norm_Beh_bin_moveDD[1000:],
	norm_CO2puffDD[1000:],
	]

	print('Plotting offball_beh_GC_rows.png')
	plot_utils.Plot_traces(GC_beh, dicDir, 'offball_beh_GC_rows.pdf', subtitle_list=['ROI_0', 'rest', 'move', 'co2'], plot_mode='row_by_row', xaxis_series=timeSec[1000:])

	print('Saving', filename, '.dic for', date, genotype, fly, recrd_num )
	pickle.dump( Beh_GC_sync, open( dicDir+'/'+filename, "wb" ) ) 


	print('Saved as', filename,  '!')

	return






off_ball_active_lines_ONBALL=list_twoP_exp.off_ball_active_lines_ONBALL
off_ball_active_lines_OFFBALL=list_twoP_exp.off_ball_active_lines_OFFBALL


experiments=off_ball_active_lines_ONBALL+off_ball_active_lines_OFFBALL



NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_Dir


for date, genotype, fly, recrd_num in experiments:

	print(date, genotype, fly, recrd_num)


	Gal4=genotype.split('-')[0]
	fly_beh=fly[0].upper()+fly[1:]

	outDir_AN_recrd=NAS_AN_Proj_Dir+Gal4+'/2P/'+date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num+'/output/'

	outDir_hangedfly=outDir_AN_recrd+'hanged_fly_analysis/'
	if not os.path.exists(outDir_hangedfly):
		os.makedirs(outDir_hangedfly)

	print('outDir_hangedfly', outDir_hangedfly)


	ThorsyncDir_inNas = NAS_Dir+'CLC/2photonData/CLC/'+date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-sync-'+recrd_num
	pathH5File=ThorsyncDir_inNas+'/Episode001.h5'



	CamDir = NAS_Dir+'CLC/'+date[2:]+'_'+genotype+'/'+fly+'/'+'CO2xzGG/behData_'+recrd_num+'/images/'

	outDirGC6_axoid = outDir_AN_recrd + '/GC6_auto/final/'

	opflowFile = NAS_Dir+'CLC/'+date[2:]+'_'+genotype+'/'+fly_beh+'/'+'CO2xzGG/behData_'+recrd_num+'/OptFlowData/OptFlow.txt'  


	pathForRGB =NAS_AN_Proj_Dir+Gal4+'/2P/'+date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num+'/2Pimg/'
	RGB = io.imread(pathForRGB+'warped_RGB.tif')
	RGB=np.asarray(RGB)


	Cam, OpFlow, CO2puff, FrameCounter = general_utils.readH5File(pathH5File)
	print('FrameCounter[-1]',FrameCounter[-1])

	numFrame=sync_utils.check_and_determine_numframe(FrameCounter,RGB)

	GC_set_temp = general_utils.readGCfile(outDirGC6_axoid)
	if np.isnan(GC_set_temp).any():
		print('Replacing NaN with interpolaration')
		GC_set=sync_utils.replace_nan_with_interp(GC_set_temp)
		plot_utils.Plot_traces_by_rows(GC_set, len(GC_set)*['ROI_1'], outDirGC6_axoid, 'GC_interp.png')
		
	else:
		print('No NaN detected. Not replacing Na')
		GC_set=GC_set_temp


	offball_beh_dic = general_utils.read_jointPos3d_Beh(outDir_hangedfly, 'beh_rest_move_hangedFly.p')
	rest_bin_trace=offball_beh_dic['rest']
	move_bin_trace=offball_beh_dic['move']


	risingEdgeCam = sync_utils.risingEdge(7,Cam)
	risingEdgeOpflow = sync_utils.risingEdge(7,OpFlow)
	startFC, stopFC = sync_utils.startStopIdxFCtr(FrameCounter)

	#print ("len risingEdgeCam",len(risingEdgeCam))
	print('len(risingEdgeCam)',len(risingEdgeCam))

	FECam = sync_utils.fallingEdge(Cam)
	FEFCam = FECam[0]
	addDiff = []
	for m in range(len(risingEdgeCam)-1):
		addDiff.append(FEFCam[m]-risingEdgeCam[m])
	ZD2 = np.where(np.asarray(addDiff)==2)
	print ("ZD2",ZD2)
	risingEdgeCam = list(risingEdgeCam)
	for z in range(len(ZD2[0])-1,-1,-1):
		del(risingEdgeCam[ZD2[0][z]])
	risingEdgeCam = np.asarray(risingEdgeCam)
	print('shape risingEdgeCam', np.shape(risingEdgeCam))
	## Need to delete from the end otherwise the index in risingEdge are going to change and we won't delete the good values


	GC_set_US=sync_utils.upsampleGC(GC_set, FrameCounter, numFrame)

	Beh_bin_rest_US=sync_utils.upsampleBeh(rest_bin_trace, Cam, risingEdgeCam)
	Beh_bin_move_US=sync_utils.upsampleBeh(move_bin_trace, Cam, risingEdgeCam)

	risingEdgeCam_Stair_US = sync_utils.upsample_risingEdgeCam(risingEdgeCam, Cam)
	print('len risingEdgeCam_Stair_US', len(risingEdgeCam_Stair_US))
	print("shape GC_set_US",np.shape(GC_set_US))
	print("shape Beh_bin_rest_US",np.shape(Beh_bin_rest_US))

	op0XSensor, op0YSensor, op1XSensor, op1YSensor, timeOpt = sync_utils.OpenOpflowVector(opflowFile)
	op0XSensor, op0YSensor, op1XSensor, op1YSensor = sync_utils.manageCompleteSensors(op0XSensor, op0YSensor, op1XSensor, op1YSensor)
	op0XSensor, op0YSensor, op1XSensor, op1YSensor = sync_utils.manageTypeOpflow(op0XSensor, op0YSensor, op1XSensor, op1YSensor)

	DiffOpflowPoints, risingEdgeOpCropped = sync_utils.compareOpflowTSReal(risingEdgeOpflow,op0XSensor)
	DiffOpflowPoints = np.asarray(DiffOpflowPoints)
	Opflow0XUS, Opflow0YUS, Opflow1XUS, Opflow1YUS = sync_utils.upsampleOpflow(DiffOpflowPoints, op0XSensor,op0YSensor,op1XSensor,op1YSensor)



	startIdx, stopIdx, vidStopTime = sync_utils.findStartAndStopIdx(risingEdgeCam,risingEdgeOpCropped,startFC,stopFC)
	startCamIdx, stopCamIdx = sync_utils.findStartStopCamera(startIdx,stopIdx,risingEdgeCam)
	CroppedFCTR= sync_utils.CropFrameCtr(FrameCounter, startIdx,stopIdx)
	
	croppedGCsetUS=[]
	for i in range(0, len(GC_set_US)):
		croppedGCsetUS.append([])
		croppedGCsetUS[i] = sync_utils.CropFrameCtr(GC_set_US[i], startIdx, stopIdx)		

	CroppedCO2puff= sync_utils.CropFrameCtr(CO2puff, startIdx,stopIdx)
	CroppedEdgeCam_Stair= sync_utils.CropFrameCtr(risingEdgeCam_Stair_US, startIdx,stopIdx)
	CroppedBeh_bin_rest= sync_utils.CropFrameCtr(Beh_bin_rest_US, startIdx,stopIdx)
	CroppedBeh_bin_move= sync_utils.CropFrameCtr(Beh_bin_move_US, startIdx,stopIdx)

	FctrOk=sync_utils.downSampling(CroppedFCTR,vidStopTime)
	EdgeCam_Stair_DD=sync_utils.downSampling(CroppedEdgeCam_Stair,vidStopTime)

	timeSec = np.linspace(0,vidStopTime,len(FctrOk))

	GC_set_DD=[]
	for i, GC_trace in enumerate(croppedGCsetUS):
		GC_set_DD.append([])
		GC_set_DD[i]=sync_utils.downSampling(GC_trace,vidStopTime)

	CO2puffDD=sync_utils.downSampling(CroppedCO2puff,vidStopTime)
	Beh_bin_restDD=sync_utils.downSampling(CroppedBeh_bin_rest, vidStopTime)
	Beh_bin_moveDD=sync_utils.downSampling(CroppedBeh_bin_move, vidStopTime)



	norm_CO2puffDD = sync_utils.normalize_Data(CO2puffDD)
	norm_Beh_bin_restDD = sync_utils.normalize_Data(Beh_bin_restDD)
	norm_Beh_bin_moveDD = sync_utils.normalize_Data(Beh_bin_moveDD)

	data_freq_DD=len(norm_Beh_bin_restDD)/timeSec[-1]

	idx_CO2puff_evt, timesec_CO2puff_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(norm_CO2puffDD, timeSec)
	idx_rest_evt, timesec_rest_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(norm_Beh_bin_restDD, timeSec)
	idx_move_evt, timesec_move_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(norm_Beh_bin_moveDD, timeSec)


	EthoIdxDic={}
	EthoIdxDic.update({'rest_evt':idx_rest_evt})
	EthoIdxDic.update({'move_evt':idx_move_evt})
	EthoIdxDic.update({'CO2puff_evt':idx_CO2puff_evt})


	EthoTimeDic={}
	EthoTimeDic.update({'rest_evt':timesec_rest_evt})
	EthoTimeDic.update({'move_evt':timesec_move_evt})
	EthoTimeDic.update({'CO2puff_evt':timesec_CO2puff_evt})

	Save_syncDic(outDir_hangedfly, filename='offball_sync_Beh_GC_20220901.p')





