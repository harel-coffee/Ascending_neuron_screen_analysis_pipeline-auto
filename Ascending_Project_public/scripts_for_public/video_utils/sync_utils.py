import os
import sys
import numpy as np
import math
from multiprocessing import Process
import matplotlib.pyplot as plt
from skimage import io
from itertools import groupby 
import more_itertools as mit
import pickle
import h5py

from utils import plot_setting






def open_GC_beh_sync_DicData(pathDic, filename):

    print('Opening',  filename ,'...')

    if os.path.exists(pathDic+'/'+filename):

        Beh_Jpos_GC_DicData = pickle.load(open( pathDic+'/'+filename, "rb" ))


        return Beh_Jpos_GC_DicData

    else:

        print('data not found...')
        sys.exit(0)

        return


def readH5File(FilePath):

    myFile = h5py.File(FilePath,'r')
    FrameCounter = myFile['CI']['Frame Counter'][:].squeeze()
    
    print('FrameCounter[-1]', FrameCounter[-1])

    return FrameCounter


def check_and_determine_numframe(Framecounter, RGBstack):

    numframe_temp=(Framecounter[-1])/(len(RGBstack))

    if numframe_temp.is_integer():
        numframe=numframe_temp
        print('numFrame=', numframe)
    else:

        print('framecounters does not match the 2Pimg numbers, it is not dividible')

    return numframe


def getXAxisAndRatio(timeSec,startVidIdx,stopVidIdx):
    #This function returns the x axis min and max values and the ratio of the number of points in the global time list to the number of points in the behavior time list.

    Ratio_HDseriestoCam=float(len(timeSec))/float(stopVidIdx-startVidIdx)

    return Ratio_HDseriestoCam



def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx], idx


def trim_period(trace, timeSec, startTime=0, endTime=150):

    # print('len trace', len(trace))

    crop_startTime, crop_startIdx = find_nearest(timeSec, startTime)


    if startTime == 0:
        crop_startTime, crop_startIdx = find_nearest(timeSec, timeSec[0])
        crop_startIdx=0
    else:
        crop_startTime, crop_startIdx = find_nearest(timeSec, startTime)   

    if endTime == -1:
        crop_stopTime, crop_stopIdx = find_nearest(timeSec, timeSec[-1])
        crop_stopIdx=-1
    else:
        crop_stopTime, crop_stopIdx = find_nearest(timeSec, endTime)

    print('crop_startTime', crop_startTime, 'crop_startIdx', crop_startIdx)
    print('crop_stopTime', crop_stopTime, 'crop_stopIdx', crop_stopIdx)


    trace_crop = trace[crop_startIdx:crop_stopIdx]



    return trace_crop



def grouping_consecutivePoints_into_evt(idx_beh):

    print()
    idx_beh_evt=[]
    for evt in mit.consecutive_groups(idx_beh):
        #type(evt) is map, once it is converted into list, it become an empty array
        #print(list(evt))
        idx_beh_evt.append(list(evt))    

    return idx_beh_evt



def convert_idx_to_timepoint(idx_beh_evt, timesec):

    timesec_beh_evt=[]
    for a in range(0,len(idx_beh_evt)):
        timesec_beh_evt.append([])
        for b in range(0, len(idx_beh_evt[a])):
            timesec_beh_evt[a].append(timesec[idx_beh_evt[a][b]])
    print()

    return timesec_beh_evt



def Package_beh_bin_trace_into_idx_time(\
        rest_trace, 
        FW_trace, 
        BW_trace, 
        EG_trace, 
        AG_trace, 
        FLG_trace, 
        HL_trace, 
        Abd_trace,  
        Push_trace, 
        PER_trace,
        timesec):

    print('len rest_trace', len(rest_trace))

    idx_rest=[]
    for i, val in enumerate(rest_trace):
        if val>0.5:
            idx_rest.append(i)

    idx_FW=[]
    for i, val in enumerate(FW_trace):
        if val>0.5:
            idx_FW.append(i)

    idx_BW=[]
    for i, val in enumerate(BW_trace):
        if val>0.5:
            idx_BW.append(i)

    idx_EG=[]
    for i, val in enumerate(EG_trace):
        if val>0.5:
            idx_EG.append(i)

    idx_AG=[]
    for i, val in enumerate(AG_trace):
        if val>0.5:
            idx_AG.append(i)

    idx_FLG=[]
    for i, val in enumerate(FLG_trace):
        if val>0.5:
            idx_FLG.append(i)

    idx_HL=[]
    for i, val in enumerate(HL_trace):
        if val>0.5:
            idx_HL.append(i)

    idx_Abd=[]
    for i, val in enumerate(Abd_trace):
        if val>0.5:
            idx_Abd.append(i)

    idx_Push=[]
    for i, val in enumerate(Push_trace):
        if val>0.5:
            idx_Push.append(i)

    idx_PER=[]
    for i, val in enumerate(PER_trace):
        if val>0.5:
            idx_PER.append(i)


    ##Package behavior binary trace into event index and time
    idx_rest_evt=grouping_consecutivePoints_into_evt(idx_rest)
    idx_FW_evt=grouping_consecutivePoints_into_evt(idx_FW)
    idx_BW_evt=grouping_consecutivePoints_into_evt(idx_BW)
    idx_EG_evt=grouping_consecutivePoints_into_evt(idx_EG)
    idx_AG_evt=grouping_consecutivePoints_into_evt(idx_AG)
    idx_FLG_evt=grouping_consecutivePoints_into_evt(idx_FLG)
    idx_HL_evt=grouping_consecutivePoints_into_evt(idx_HL)
    idx_Abd_evt=grouping_consecutivePoints_into_evt(idx_Abd)
    idx_Push_evt=grouping_consecutivePoints_into_evt(idx_Push)
    idx_PER_evt=grouping_consecutivePoints_into_evt(idx_PER)

    timesec_rest_evt=convert_idx_to_timepoint(idx_rest_evt, timesec)
    timesec_FW_evt=convert_idx_to_timepoint(idx_FW_evt, timesec)
    timesec_BW_evt=convert_idx_to_timepoint(idx_BW_evt, timesec)
    timesec_EG_evt=convert_idx_to_timepoint(idx_EG_evt, timesec)
    timesec_AG_evt=convert_idx_to_timepoint(idx_AG_evt, timesec)
    timesec_FLG_evt=convert_idx_to_timepoint(idx_FLG_evt, timesec)
    timesec_HL_evt=convert_idx_to_timepoint(idx_HL_evt, timesec)
    timesec_Abd_evt=convert_idx_to_timepoint(idx_Abd_evt, timesec)
    timesec_Push_evt=convert_idx_to_timepoint(idx_Push_evt, timesec)
    timesec_PER_evt=convert_idx_to_timepoint(idx_PER_evt, timesec)

    

    EthoIdxDic={}
    EthoTimeDic={}
    EthoColorCodeDic={}

    EthoIdxDic.update({'rest_evt':idx_rest_evt})
    EthoTimeDic.update({'rest_evt':timesec_rest_evt})
    EthoColorCodeDic.update({'rest_evt':plot_setting.rest_color})

    EthoIdxDic.update({'forward_walk_evt':idx_FW_evt})
    EthoTimeDic.update({'forward_walk_evt':timesec_FW_evt})
    EthoColorCodeDic.update({'forward_walk_evt':plot_setting.FW_color})

    EthoIdxDic.update({'backward_walk_evt':idx_BW_evt})
    EthoTimeDic.update({'backward_walk_evt':timesec_BW_evt})
    EthoColorCodeDic.update({'backward_walk_evt':plot_setting.BW_color})

    EthoIdxDic.update({'eye_groom_evt':idx_EG_evt})
    EthoTimeDic.update({'eye_groom_evt':timesec_EG_evt})
    EthoColorCodeDic.update({'eye_groom_evt':plot_setting.E_groom_color})

    EthoIdxDic.update({'antennae_groom_evt':idx_AG_evt})
    EthoTimeDic.update({'antennae_groom_evt':timesec_AG_evt})
    EthoColorCodeDic.update({'antennae_groom_evt':plot_setting.A_groom_color})

    EthoIdxDic.update({'foreleg_groom_evt':idx_FLG_evt})
    EthoTimeDic.update({'foreleg_groom_evt':timesec_FLG_evt})
    EthoColorCodeDic.update({'foreleg_groom_evt':plot_setting.FL_groom_color})

    EthoIdxDic.update({'hindleg_groom':idx_HL_evt})
    EthoTimeDic.update({'hindleg_groom':timesec_HL_evt})
    EthoColorCodeDic.update({'hindleg_groom':plot_setting.HL_groom_color})

    EthoIdxDic.update({'Abdomen_groom_evt':idx_Abd_evt})
    EthoTimeDic.update({'Abdomen_groom_evt':timesec_Abd_evt})
    EthoColorCodeDic.update({'Abdomen_groom_evt':plot_setting.Abd_groom_color})

    EthoIdxDic.update({'push_evt':idx_Push_evt})
    EthoTimeDic.update({'push_evt':timesec_Push_evt})
    EthoColorCodeDic.update({'push_evt':plot_setting.Push_color})

    EthoIdxDic.update({'PER_evt':idx_PER_evt})
    EthoTimeDic.update({'PER_evt':timesec_PER_evt})
    EthoColorCodeDic.update({'PER_evt':plot_setting.PER_color})




    return EthoIdxDic, EthoTimeDic, EthoColorCodeDic


def FindLastCamPhotoIdx(cameraPath):

    listFiles = os.listdir(cameraPath)
    print('len listFiles',  len(listFiles))

    if '.DS_Store' in listFiles:
        print('removing .DS_Store')
        listFiles.remove('.DS_Store')

    if 'Thumbs.db' in listFiles:
        print('removing Thumbs.db')
        listFiles.remove('Thumbs.db')

    if 'capture_metadata.json' in listFiles:
        print('removing .json from img list')
        listFiles.remove('capture_metadata.json')

    # print('listFiles',listFiles)
    # print('len listFiles',  len(listFiles))
    
    #print('len(listFiles)%cameraAmount',len(listFiles)%cameraAmount)

    #camera_2_img_3220.jpg

    camera_num=[0,1,2,3,4,5,6]

    camera_0_imgs=[]
    camera_1_imgs=[]
    camera_2_imgs=[]
    camera_3_imgs=[]
    camera_4_imgs=[]
    camera_5_imgs=[]
    camera_6_imgs=[]
    for f in listFiles:
        #print(f)
        if f.startswith('camera_0'):
            camera_0_imgs.append(f)
        elif f.startswith('camera_1'):
            camera_1_imgs.append(f)
        elif f.startswith('camera_2'):
            camera_2_imgs.append(f)
        elif f.startswith('camera_3'):
            camera_3_imgs.append(f)
        elif f.startswith('camera_4'):
            camera_4_imgs.append(f)
        elif f.startswith('camera_5'):
            camera_5_imgs.append(f)
        elif f.startswith('camera_6'):
            camera_6_imgs.append(f)

    photoCounts_each_cam=[0,0,0,0,0,0,0]
    if len(camera_0_imgs)!=0:
        photoCounts_each_cam[0]=len(camera_0_imgs)
    if len(camera_1_imgs)!=0:
        photoCounts_each_cam[1]=len(camera_1_imgs)
    if len(camera_2_imgs)!=0:
        photoCounts_each_cam[2]=len(camera_2_imgs)
    if len(camera_3_imgs)!=0:
        photoCounts_each_cam[3]=len(camera_3_imgs)
    if len(camera_4_imgs)!=0:
        photoCounts_each_cam[4]=len(camera_4_imgs)
    if len(camera_5_imgs)!=0:
        photoCounts_each_cam[5]=len(camera_5_imgs)
    if len(camera_6_imgs)!=0:
        photoCounts_each_cam[6]=len(camera_6_imgs)


    print('photoCounts_each_cam', photoCounts_each_cam)

    print('np.nonzero(photoCounts_each_cam)[0]', np.nonzero(photoCounts_each_cam)[0])

    active_cam=[]
    for i in np.nonzero(photoCounts_each_cam)[0]:
        active_cam.append(i)
    active_cam_counts=len(active_cam)
    print('active_cam_counts', active_cam_counts)

    beh_photo_sum=sum(photoCounts_each_cam)
    print('beh_photo_sum', beh_photo_sum)

    if beh_photo_sum%active_cam_counts==0:
        vidStopIdx=int(beh_photo_sum/active_cam_counts-1)
    else:
        print('Behavioral cameras have acquisition issue. Amounts of photos are different from at least one of the cameras...')
        sys.exit(0)


    print('vidStopIdx', vidStopIdx)


    return vidStopIdx







