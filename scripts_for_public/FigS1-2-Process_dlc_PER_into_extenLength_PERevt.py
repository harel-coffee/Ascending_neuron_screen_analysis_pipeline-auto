import pandas as pd 
import glob
import os
import h5py
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
plt.switch_backend('agg')
import math
import scipy.signal
import statsmodels.api as sm
import pickle
from scipy.fftpack import rfft, irfft, fftfreq


import utils.general_utils as general_utils







experiments=[
('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '002', {'diff_thrsld':0.03, 'event_max_dur':2, 'event_min_dur':0.3, 'norm_thrsld':0.27, 'norm_change_thrsld':0.2, 'raw_change_thrsld':7}), ## example for supp figure
]




# desiredRange_list=[[750, 1160]]
desiredRange_list=[[0, -1]]




def read_latest_h5(PER_h5_Dir):

	list_of_filenames = glob.glob(PER_h5_Dir+'*.h5')
	print('list_of_filenames', list_of_filenames)

	File_create_time=[]
	for f in list_of_filenames:
		## Mac: stat.st_birthtime
		## Linux: No easy way to get creation time as in Mac, so we settle for modified time where the content is last modified: stat.st_mtime
		ctime=os.stat(f).st_mtime
		File_create_time.append(ctime)
	print('File_create_time', File_create_time)

	index_max=np.argmax(File_create_time)
	latest_h5_filename = list_of_filenames[index_max]
	print('latest_h5_filename', latest_h5_filename)

	latest_h5_file = h5py.File(latest_h5_filename,'r')




	return latest_h5_file


def extract_coord(h5File):

	table=h5File['df_with_missing']['table'][:]


	table_list=table


	Pbsc0_x=[]
	Pbsc0_y=[]
	Pbsc1_x=[]
	Pbsc1_y=[]
	for i in range(0,len(table_list)):
		Pbsc0_x.append(table_list[i][1][0])
		Pbsc0_y.append(table_list[i][1][1])
		Pbsc1_x.append(table_list[i][1][3])
		Pbsc1_y.append(table_list[i][1][4])



	



	return Pbsc0_x, Pbsc0_y, Pbsc1_x, Pbsc1_y



def fix_point(pt_x_series, pt_y_series):

	fix_pt_x = np.mean(pt_x_series)
	fix_pt_y = np.mean(pt_y_series)

	# print('fix_pt_x', fix_pt_x)
	# print('fix_pt_y', fix_pt_y)

	return fix_pt_x, fix_pt_y


def find_origin_position(pt_x_series, pt_y_series):

	template_x_series=[1]*len(pt_x_series)
	template_y_series=[1]*len(pt_y_series)

	#print('pt_y_series', pt_y_series)

	#norm_x_series ,_ ,_ = normalize_trace(pt_x_series, frame_window=100, mode='btwn_0and1')
	norm_y_series ,_ ,_ = normalize_trace(pt_y_series, frame_window=10, mode='btwn_0and1')

	# print('len(norm_y_series)', len(norm_y_series))
	# print('norm_y_series', norm_y_series)
	# print('max norm_y_series', max(norm_y_series))
	# print('min norm_y_series', min(norm_y_series))




	for i, val in enumerate(norm_y_series):
		if val>0.25:
			template_x_series[i]=np.nan
			template_y_series[i]=np.nan


	baseline_x=np.multiply(pt_x_series, template_x_series)
	baseline_y=np.multiply(pt_y_series, template_y_series)

	# print('baseline_x', baseline_x)
	# print('baseline_y', baseline_y)

	major_pt_x=np.nanmean(baseline_x)
	major_pt_y=np.nanmean(baseline_y)

	# print('major_pt_x', major_pt_x)
	# print('major_pt_y', major_pt_y)




	return major_pt_x, major_pt_y



def calc_length(pt0_x, pt0_y, pt1_x, pt1_y):

	return math.sqrt( ((pt0_x-pt1_x)**2)+((pt0_y-pt1_y)**2) )


def smooth_trace(trace, frame_window=9):

	window = np.ones(frame_window)/frame_window
	trace_smooth = np.convolve(trace, window, mode='same')
	trace_smooth[0] = trace[0]
	trace_smooth[-1] = trace[-1]

	return trace_smooth


def savgol_filter(trace, frame_window=9, polyorder=3):

	trace_hat = scipy.signal.savgol_filter(trace, frame_window, polyorder)

	return trace_hat


def butter_lowpass_filter(data, cutOff, fs, order=3):

    nyq = 0.5 * fs
    normalCutoff = cutOff / nyq
    b, a = scipy.signal.butter(order, normalCutoff, btype='low', analog = True)
    y = scipy.signal.filtfilt(b, a, data)
    return y


def median_filter(trace, frame_window=9):

	return scipy.signal.medfilt(trace,kernel_size=frame_window)


def FitSARIMAXModel(x,pcutoff=10,alpha=0.1,ARdegree=3,MAdegree=1,nforecast = 0, disp=False):
    # Seasonal Autoregressive Integrated Moving-Average with eXogenous regressors (SARIMAX)
    # see http://www.statsmodels.org/stable/statespace.html#seasonal-autoregressive-integrated-moving-average-with-exogenous-regressors-sarimax
    Y=x.copy()
    Y=np.asarray(Y)
    #Y[p<pcutoff]=np.nan # Set uncertain estimates to nan (modeled as missing data)
    if np.sum(np.isfinite(Y))>10:

        # SARIMAX implemetnation has better prediction models than simple ARIMAX (however we do not use the seasonal etc. parameters!)
        mod = sm.tsa.statespace.SARIMAX(Y.flatten(), order=(ARdegree,0,MAdegree),seasonal_order=(0, 0, 0, 0),simple_differencing=True)
        #Autoregressive Moving Average ARMA(p,q) Model
        #mod = sm.tsa.ARIMA(Y, order=(ARdegree,0,MAdegree)) #order=(ARdegree,0,MAdegree)
        try:
            res = mod.fit(disp=disp)
        except ValueError: #https://groups.google.com/forum/#!topic/pystatsmodels/S_Fo53F25Rk (let's update to statsmodels 0.10.0 soon...)
            startvalues=np.array([convertparms2start(pn) for pn in mod.param_names])
            res= mod.fit(start_params=startvalues,disp=disp)
        except np.linalg.LinAlgError:
            # The process is not stationary, but the default SARIMAX model tries to solve for such a distribution...
            # Relaxing those constraints should do the job.
            mod = sm.tsa.statespace.SARIMAX(Y.flatten(), order=(ARdegree, 0, MAdegree),
                                            seasonal_order=(0, 0, 0, 0), simple_differencing=True,
                                            enforce_stationarity=False, enforce_invertibility=False,
                                            use_exact_diffuse=False)
            res = mod.fit(disp=disp)

        predict = res.get_prediction(end=mod.nobs + nforecast-1)
        predict.predicted_mean[0]=Y[0]

        return predict.predicted_mean,predict.conf_int(alpha=alpha)

    else:
        return np.nan*np.zeros(len(Y)),np.nan*np.zeros((len(Y),2))


def fft_filter(trace, lf=2.5,hf=1.5, filename='fft_space.png'):

	fps=30
	start_time=0
	end_time=int(len(trace)/fps)
	time=np.linspace(start_time,end_time,len(trace))
	trace_copy=trace.copy()
	signal=np.asarray(trace_copy)

	

	W = fftfreq(signal.size, d=time[1]-time[0])
	f_signal = rfft(signal)
	f_signal[(W<0.1)] = 0

	# print('W',W)
	# print('len W', len(W))

	# If our original signal time was in seconds, this is now in Hz    
	band_f_signal = f_signal.copy()
	band_f_signal[(W<hf)] = 0
	band_f_signal[(W>lf)] = 0
	band_signal = irfft(band_f_signal)

	high_f_signal = f_signal.copy()
	high_f_signal[(W<7)] = 0
	high_f_signal[(W>15)] = 0
	high_signal = irfft(high_f_signal)

	low_f_signal = f_signal.copy()
	low_f_signal[(W<0)] = 0
	low_f_signal[(W>0.6)] = 0
	low_signal = irfft(low_f_signal)

	# Substract raw signal from low and high signals
	#Sub_raw_signal=signal-high_signal-low_signal
	Sub_raw_signal=signal-high_signal


	return Sub_raw_signal


def filtered_traces(trace, filtermode='median', **kwargs):

	trace_copy=trace.copy()


	if filtermode == 'running_window':
		trace_filt=smooth_trace(trace_copy, frame_window=3)

	elif filtermode == 'median':
		trace_filt=median_filter(trace_copy, frame_window=9)

	elif filtermode=='savgol_filter':
		trace_filt=savgol_filter(trace_copy, frame_window=13, polyorder=2)

	elif filtermode=='sarimax':
		trace_filt, CI=FitSARIMAXModel(trace_copy)

	elif filtermode=='butter_lowpass':
		trace_filt = butter_lowpass_filter(trace_copy, cutOff=0.03, fs=30, order=2) # cutoff frequency in rad/s; sampling frequency in rad/s; order of filter
	
	elif filtermode=='fft_filter':
		trace_filt=fft_filter(trace_copy, lf=7,hf=-0.01, filename='fft_space.png')

	return trace_filt
	


def normalize_trace(trace, frame_window=100, mode=None):


	if mode == 'btwn_0and1':

		max_val=max(trace)

		#print('max_val', max_val)

		smth_trace=smooth_trace(trace,frame_window)
		#print('smth_trace', smth_trace)
		#print('min smth_trace', min(smth_trace))
		#print('max smth_trace', max(smth_trace))


		#baseline = np.nanmin(smth_trace[int((1/7)*len(trace)):int((6/7)*len(trace))])


		temp_trace=[1]*len(trace)
		mean_trace = np.nanmean(smth_trace) 
		for i, val in enumerate(trace):
			if val>1.3*mean_trace:
				temp_trace[i]=np.nan
		
		baseline=np.nanmean(np.multiply(trace, temp_trace))



		
		#print('baseline', baseline)

		range_trace=max_val-baseline
		#print('range_trace', range_trace)
		
		# plt.plot(smth_trace)
		# plt.show()
		# plt.pause(3)
		# plt.clf()

		#print('min(np.asarray(trace)-baseline)' , min(np.asarray(trace)-baseline))
		norm_0and1_trace=(np.asarray(trace)-baseline)/range_trace

		# norm_0and1_trace=[]
		# for val in trace:
		# 	norm_val=(val-baseline)/range_trace
		# 	norm_0and1_trace.append(norm_val)

		return norm_0and1_trace, range_trace, baseline


	elif mode == 'fold_of_baseline':

		smth_trace=smooth_trace(trace,frame_window)
		if len(trace)>5000:
			baseline = min(smth_trace[int((1/7)*len(trace)):int((6/7)*len(trace))])
		else:
			baseline = min(smth_trace) 


		norm_trace = (np.asarray(trace)-baseline)/baseline



		return norm_trace



	


def find_nearest(ori_array, ori_value, condition=None, height_cond=None):
    

	array = np.asarray(ori_array)
	# print('array', array)
	# print('len array', len(array))

	if condition==None:
		idx = (np.abs(ori_array - ori_value)).argmin()

		return ori_array[idx]

	elif condition=='over_max':

		#print('ori_array', ori_array)

		array, range_trace, baseline=normalize_trace(ori_array,frame_window=1, mode='btwn_0and1')
		value=(ori_value-baseline)/range_trace

		if len(array)<10:
			
			print('Skip detecting end point of this event! It is too short!')
			return ori_array[1]

		else:

			peak_idx_array, _ = scipy.signal.find_peaks(array, height=0.5)
			if len(peak_idx_array)==0:
				max_idx=array.argmax()
			else:
				max_idx=peak_idx_array[0]

			# print('max_idx', max_idx)
			# print('array', array)
			# print('len array', len(array))
			#print('array[max_idx:-1]', array[max_idx:-1])

			# if the array is too short, then skip



			Similarity_with_value = 1 - np.abs(array[max_idx:-1] - value) 
			similarity_to_startVal=0.8
			local_max_idx, _ = scipy.signal.find_peaks(Similarity_with_value, height=similarity_to_startVal)

			similarity_grid=sorted(np.arange(0.5, 0.9, step=0.05), reverse = True)
			#print('similarity_grid',similarity_grid)

			for i, similarity in enumerate(similarity_grid):
				local_max_idx, _ = scipy.signal.find_peaks(Similarity_with_value, height=similarity)
				# print('similarity',similarity,'local_max_idx',local_max_idx)
				if len(local_max_idx)==0:
					if i==len(similarity_grid)-1:
						#print('	no local maximum found ... ')
						#print('	Instead looking for closet value  ... ')
						#print('similarity', similarity)
						#print('Similarity_with_value', Similarity_with_value)
						Similarity_with_value_thres=np.asarray(list(Similarity_with_value).copy())
						Similarity_with_value_thres[(np.asarray(Similarity_with_value)<similarity)]=0

						if np.sum(Similarity_with_value_thres)==0:
							if max_idx==len(array)-1:
								# print('	max_idx')
								idx=max_idx
							else:
								# print('	all values < threshold...')
								# print('	take last value as the end of the event...')
								idx_temp=len(Similarity_with_value_thres)-1
								idx=max_idx+idx_temp
								# print('idx_temp',idx_temp)

						else:
							idx_temp=Similarity_with_value_thres.argmax()
							idx=max_idx+idx_temp 
							# print('idx_temp',idx_temp)

							# plt.title('similarity ='+str(similarity)+' frame# ='+str(idx))
							# plt.plot(Similarity_with_value_thres)
							# plt.plot(idx_temp, Similarity_with_value_thres[idx_temp], 'ro')
							# plt.savefig(outputPERplotdir+'local_evt_no_local_max.png')
							# plt.clf()


					else:
						continue

				else:
					idx=max_idx+local_max_idx[0]


					# plt.title('similarity ='+str(similarity)+' frame# ='+str(idx))
					# plt.plot(0-max_idx,value,'x')
					# plt.plot(array[max_idx:-1],'r') 
					# plt.plot(np.abs(array[max_idx:-1] - value),'g')
					# plt.plot(Similarity_with_value,'b')
					# plt.plot(local_max_idx, Similarity_with_value[local_max_idx], "x")
					# plt.plot(idx-max_idx, array[idx], "v")

					# plt.savefig(outputPERplotdir+'local_evt.png')
					# plt.clf()

					break			

			##Normalize y-value with x-value for detecting distance between start point and end point
			# scaling_factor_for_fair_dist_cal=int(len(array[max_idx:-1])/max(array[max_idx:-1]))
			# slope_list=[]
			# dist_list=[]
			# for i, val in enumerate(array[max_idx:-1]):
			# 	dist=calc_length(0, value*scaling_factor_for_fair_dist_cal, max_idx+i, array[max_idx+i]*scaling_factor_for_fair_dist_cal)
			# 	dist_list.append(dist)
			# 	slope=np.abs((array[max_idx+i]-value)/(max_idx+i-0))
			# 	slope_list.append(slope)
			
			# print('len slope_list', len(slope_list))
			# print('len dist_list', len(dist_list))

			# min_slope_idx=np.asarray(slope_list).argmin()
			# min_dist_idx=np.asarray(dist_list).argmin()
			# print('min_slope_idx', min_slope_idx)
			# print('min_dist_idx', min_dist_idx)
			# idx=min_dist_idx


			return ori_array[idx]




def detect_kinx(trace, peaks_idx, mode='forward', srch_range=0.4, no_after_these_idx=None, height_cond=None):

	print(mode+' detecting ...')

	thrsld_facotor=0.2 # % of peak as event starting threshold
	data_samplerate=30



	evt_kinx_idx_series=[]




	for i, peak_idx in enumerate(peaks_idx):

		ajst_thrsld = trace[peak_idx]*thrsld_facotor

		if mode=='forward':
			
			if int(peak_idx-data_samplerate*srch_range)>0:
				nearest_value=find_nearest(trace[int(peak_idx-data_samplerate*srch_range):int(peak_idx)], ajst_thrsld)
			elif int(peak_idx-data_samplerate*srch_range)<=0:
				nearest_value=find_nearest(trace[0:int(peak_idx)], ajst_thrsld)

			nearest_value_idx = np.where(trace == nearest_value)
		# print('ddata_series searching range:', int(peak_idx-data_samplerate*srch_range), int(peak_idx))
		# print('nearest_value_idx', nearest_value_idx)

		elif mode=='backward':

			height_cond_val=height_cond[i]*0.7

			# Not touch trace end
			
			if int(peak_idx+data_samplerate*srch_range)<len(trace)-1:
				#print('Evt# '+str(i)+' at frame# '+str(peak_idx)+': '+'backward not touch trace end')
				
				# Not last start idx
				if i+1<len(no_after_these_idx):
					# print('Not last start idx')
					# Not touch next start idx
					if int(peak_idx+data_samplerate*srch_range)<no_after_these_idx[i+1]:
						#print('Evt# '+str(i)+' at frame# '+str(peak_idx)+': '+'Not touch next start idx')
						nearest_value=find_nearest(trace[int(peak_idx):int(peak_idx+data_samplerate*srch_range)], trace[peak_idx], condition='over_max', height_cond=height_cond_val)
						#print('int(peak_idx', int(peak_idx), 'int(peak_idx+data_samplerate*srch_range)',int(peak_idx+data_samplerate*srch_range))
					#Touch next start idx
					else:
						# print('touch next start idx')
						# print('i',i)
						# print('peak_idx', peak_idx)
						# print('peaks_idx', peaks_idx)
						# print('no_after_these_idx', no_after_these_idx)
						# print('no_after_these_idx[i+1]', no_after_these_idx[i+1])
						nearest_value=find_nearest(trace[int(peak_idx):no_after_these_idx[i+1]], trace[peak_idx], condition='over_max', height_cond=height_cond_val)
				
				# Last start idx
				else:		
					#print('Evt# '+str(i)+' at frame# '+str(peak_idx)+': '+'Last start idx')		
					nearest_value=find_nearest(trace[int(peak_idx):int(peak_idx+data_samplerate*srch_range)], trace[peak_idx], condition='over_max', height_cond=height_cond_val)

			# Touch trace end
			else:
				#print('Evt# '+str(i)+' at frame# '+str(peak_idx)+': '+'backward touch trace end')
				if i+1<len(no_after_these_idx):
					#print('Evt# '+str(i)+' at frame# '+str(peak_idx)+': '+'Not last start idx')
					# Not touch next start idx
					if int(peak_idx+data_samplerate*srch_range)<no_after_these_idx[i+1]:
						#print('Evt# '+str(i)+' at frame# '+str(peak_idx)+': '+'Not touch next start idx')
						nearest_value=find_nearest(trace[int(peak_idx):-1], trace[peak_idx], condition='over_max', height_cond=height_cond_val)
					#Touch next start idx
					else:
						#print('Evt# '+str(i)+' at frame# '+str(peak_idx)+': '+'touch next start idx')
						nearest_value=find_nearest(trace[int(peak_idx):no_after_these_idx[i+1]], trace[peak_idx], condition='over_max', height_cond=height_cond_val)
				
				# Last start idx
				else:		
					#print('Evt# '+str(i)+' at frame# '+str(peak_idx)+': '+'Last start idx')		
					nearest_value=find_nearest(trace[int(peak_idx):-1], trace[peak_idx], condition='over_max', height_cond=height_cond_val)

			# print('nearest_value', nearest_value)

			nearest_value_idx = np.where(trace == nearest_value)
			if len(nearest_value_idx[0])==0:
				nearest_value_idx=[[int(peak_idx+data_samplerate*srch_range), len(trace)]]


		# print('nearest_value_idx', nearest_value_idx)
		evt_kinx_idx_series.append(nearest_value_idx[0][0])
		evt_kinx_idx_series.sort()


	return evt_kinx_idx_series



def diff_trace(trace, samplerate=1, diff_window_s=0.2 ):

	intvl_dif=int(samplerate*diff_window_s)
	ddata_series=[]
	for i in range(0,len(trace)-intvl_dif):
		ddatapoint = trace[i+intvl_dif]-trace[i]
		ddata_series.append(ddatapoint) 

    
	# put 0 to the place where there is no derivative
	for i in range(0,len(trace)-len(ddata_series)):
		ddata_series.append(0)   

	return ddata_series



def detect_PER_event(norm_trace, raw_trace):

	print('Detecting events...')

	fps=30
	
	# diff_thrsld=0.03

	# event_min_dur=0.27
	# # event_min_dur=1
	
	# norm_thrsld=0.15
	# #norm_thrsld=-0.2
	# norm_change_thrsld=0.2
	# raw_change_thrsld=10
	# # raw_change_thrsld=8

	evt_min_dur=int(event_min_dur*fps)


	#grad_trace = np.gradient(trace,0.25)
	grad_trace = diff_trace(norm_trace, samplerate=fps, diff_window_s=0.1)
	grad_trace = filtered_traces(grad_trace, filtermode='running_window')



	peaks_idx_rawTrace, _ = scipy.signal.find_peaks(norm_trace, height = norm_thrsld, distance=25)
	peaks_idx_gradTrace, _ = scipy.signal.find_peaks(grad_trace, height = diff_thrsld, distance=25)
	#peaks_idx_gradTrace_cwt = scipy.signal.find_peaks_cwt(grad_trace, np.arange(1,20), max_distances=np.arange(1, 30)*2)
	#print('peaks_idx', peaks_idx)
	

	peaks_of_rawTrace_on_rawTrace = np.array(norm_trace)[peaks_idx_rawTrace]

	peaks_of_gradTrace_on_rawTrace = np.array(norm_trace)[peaks_idx_gradTrace]
	peaks_of_gradTrace_on_gradTrace = np.array(grad_trace)[peaks_idx_gradTrace]

	# peaks_idx_gradTrace_cwt_on_rawTrace = np.array(trace)[peaks_idx_gradTrace_cwt]
	# peaks_idx_gradTrace_cwt_on_gradTrace = np.array(grad_trace)[peaks_idx_gradTrace_cwt]

	## Find start kinx of event
	kinx_idx_rawTrace=detect_kinx(grad_trace, peaks_idx_gradTrace, mode='forward', srch_range=0.4)
	## clean repeated idx
	kinx_idx_rawTrace=sorted(list(set(kinx_idx_rawTrace)))
	# print('kinx_idx_rawTrace', kinx_idx_rawTrace)
	
	# Backward find nearest point of kinx as for the end of the event
	end_idx_rawTrace=detect_kinx(norm_trace, kinx_idx_rawTrace, mode='backward', srch_range=event_max_dur, no_after_these_idx=kinx_idx_rawTrace, height_cond=peaks_of_gradTrace_on_rawTrace)

	# print('kinx_idx_rawTrace', kinx_idx_rawTrace)
	# print('len kinx_idx_rawTrace', len(kinx_idx_rawTrace))

	# print('end_idx_rawTrace', end_idx_rawTrace)
	# print('len end_idx_rawTrace', len(end_idx_rawTrace))	

	startIdx_rawTrace, endIdx_rawTrace=clean_FalsePositive_detection(kinx_idx_rawTrace, end_idx_rawTrace, norm_trace, mode='remove_short_period', threshold=evt_min_dur)
	startIdx_rawTrace, endIdx_rawTrace=clean_FalsePositive_detection(startIdx_rawTrace, endIdx_rawTrace, norm_trace, mode='remove_small_value',threshold=norm_thrsld)
	startIdx_rawTrace, endIdx_rawTrace=clean_FalsePositive_detection(startIdx_rawTrace, endIdx_rawTrace, norm_trace, mode='remove_small_change',threshold=norm_change_thrsld)
	startIdx_rawTrace, endIdx_rawTrace=clean_FalsePositive_detection(startIdx_rawTrace, endIdx_rawTrace, raw_trace, mode='remove_small_change',threshold=raw_change_thrsld)

	start_idx_rawTrace_on_rawTrace = np.array(norm_trace)[startIdx_rawTrace]
	start_idx_rawTrace_on_gradTrace = np.array(grad_trace)[startIdx_rawTrace]	
	end_idx_rawTrace_on_rawTrace = np.array(norm_trace)[endIdx_rawTrace]

	evt_bin_trace=[0]*len(norm_trace)
	for i, evt_startIdx in enumerate(startIdx_rawTrace):
		evt_endIdx=endIdx_rawTrace[i]
		for j in range(evt_startIdx, evt_endIdx+1):
			evt_bin_trace[j]=1




	print('==Plot preview of PER event detection==')
	fig=plt.figure(facecolor='black', figsize=(25, 10), dpi=200)
	
	plt.subplot(411)
	plt.title('raw PER_trace')
	plt.plot(raw_trace, color='k', linewidth=1)
	#plt.plot(trace_med, color='r', linewidth=1)
	#plt.plot(peaks_idx_rawTrace, peaks_of_rawTrace_on_rawTrace, marker='x', color='r',linestyle = 'None')
	#plt.plot(peaks_idx_gradTrace, peaks_of_gradTrace_on_rawTrace, marker='o', color='g',linestyle = 'None')
	plt.plot(startIdx_rawTrace, start_idx_rawTrace_on_rawTrace, marker='^', color='b',linestyle = 'None')
	plt.plot(endIdx_rawTrace, end_idx_rawTrace_on_rawTrace, marker='v', color='r',linestyle = 'None')
	for i, evt_startIdx in enumerate(startIdx_rawTrace):
		evt_endIdx=endIdx_rawTrace[i]
		plt.axvspan(evt_startIdx, evt_endIdx, color='k', alpha=0.25, linewidth=0)

	
	plt.subplot(412)
	plt.title('norm PER_trace')
	plt.plot(norm_trace, color='k', linewidth=1)
	#plt.plot(trace_med, color='r', linewidth=1)
	#plt.plot(peaks_idx_rawTrace, peaks_of_rawTrace_on_rawTrace, marker='x', color='r',linestyle = 'None')
	#plt.plot(peaks_idx_gradTrace, peaks_of_gradTrace_on_rawTrace, marker='o', color='g',linestyle = 'None')
	plt.plot(startIdx_rawTrace, start_idx_rawTrace_on_rawTrace, marker='^', color='b',linestyle = 'None')
	plt.plot(endIdx_rawTrace, end_idx_rawTrace_on_rawTrace, marker='v', color='r',linestyle = 'None')
	for i, evt_startIdx in enumerate(startIdx_rawTrace):
		evt_endIdx=endIdx_rawTrace[i]
		plt.axvspan(evt_startIdx, evt_endIdx, color='k', alpha=0.25, linewidth=0)
	
	plt.subplot(413)
	plt.title('grad_PER_trace')
	plt.plot(grad_trace, color='k',linewidth=1)
	plt.plot(peaks_idx_gradTrace, peaks_of_gradTrace_on_gradTrace, marker='o', color='g',linestyle = 'None')
	plt.plot(startIdx_rawTrace, start_idx_rawTrace_on_gradTrace, marker='^', color='b',linestyle = 'None')
	for i, evt_startIdx in enumerate(startIdx_rawTrace):
		evt_endIdx=endIdx_rawTrace[i]
		plt.axvspan(evt_startIdx, evt_endIdx, color='k', alpha=0.25, linewidth=0)
	

	plt.subplot(414)
	plt.title('Binary PER event trace')
	plt.plot(evt_bin_trace, color='k',linewidth=1)

	
	plt.tight_layout()
	plt.savefig(outputPERplotdir+'PER_event.png')
	plt.savefig(outputPERplotdir+'PER_event.pdf')
	plt.clf()
	plt.close(fig)




	return evt_bin_trace, startIdx_rawTrace, endIdx_rawTrace


def clean_FalsePositive_detection(startIdx_series, stopIdx_series, ref_trace, mode='remove_small', threshold=0.5):

	if mode=='remove_small_change':

		new_startIdx_series=[]
		new_stopIdx_series=[]
		for i, evt_startIdx in enumerate(startIdx_series):
			evt_endIdx=stopIdx_series[i]

			startVal=ref_trace[evt_startIdx]
			pealVal=max(ref_trace[evt_startIdx:evt_endIdx])


			if (pealVal-startVal)>threshold:
				new_startIdx_series.append(evt_startIdx)
				new_stopIdx_series.append(evt_endIdx)


	elif mode=='remove_small_value':

		new_startIdx_series=[]
		new_stopIdx_series=[]
		for i, evt_startIdx in enumerate(startIdx_series):
			evt_endIdx=stopIdx_series[i]

			pealVal=max(ref_trace[evt_startIdx:evt_endIdx])
			if pealVal>threshold:
				new_startIdx_series.append(evt_startIdx)
				new_stopIdx_series.append(evt_endIdx)		


	elif mode=='remove_short_period':
		new_startIdx_series=[]
		new_stopIdx_series=[]		
		for i, evt_startIdx in enumerate(startIdx_series):
			evt_endIdx=stopIdx_series[i]

			if (evt_endIdx-evt_startIdx)>threshold:
				new_startIdx_series.append(evt_startIdx)
				new_stopIdx_series.append(evt_endIdx)

	return new_startIdx_series, new_stopIdx_series



def cutting_outlier_in_trace(trace, outlier_thrsld=0.4, keep_side='lower'):

	raw_thrld=np.nanmax(trace)*outlier_thrsld

	thresh_trace=[]

	if keep_side=='lower':
		for i, v in enumerate(trace):
			if v<raw_thrld:
				thresh_trace.append(v)
			else:
				thresh_trace.append(0)

	elif keep_side=='higher':
		for i, v in enumerate(trace):
			if v>raw_thrld:
				thresh_trace.append(v)
			else:
				thresh_trace.append(0)

	return thresh_trace



def keep_desired_range_of_trace(trace, desireRanges=[[0,-1]]):

	trace_desired_range=[0]*len(trace)

	for i, range_list in enumerate(desireRanges):
	
		trace_desired_range[range_list[0]:range_list[1]]=trace[range_list[0]:range_list[1]]


	# for i, v in enumerate(trace):
	# 	if i > startIdx and i < endIdx:
	# 		trace_desired_range[i]=v
	# 	else:
	# 		continue


	return trace_desired_range






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


def save_PER_dic(filename='PER_camera_6.p'):


	dicData={}

	# Proboscis original coordinate
	dicData.update({'pbsc0_X':origin_med_pbsc1_X})
	dicData.update({'pbsc0_Y':origin_med_pbsc1_Y})
	
	dicData.update({'pbsc1_X':pbsc1_X})
	dicData.update({'pbsc1_Y':pbsc1_Y})

	# Proboscis fix coordinate of Pbsc0
	dicData.update({'fix_pbsc0_X':fix_pbsc0_X})
	dicData.update({'fix_pbsc0_Y':fix_pbsc0_Y})

	# Proboscis filtered coordinate of Pbsc0
	dicData.update({'smth_pbsc1_X':smth_pbsc1_X})
	dicData.update({'smth_pbsc1_Y':smth_pbsc1_Y})	

	dicData.update({'med_pbsc1_X':med_pbsc1_X})
	dicData.update({'med_pbsc1_Y':med_pbsc1_Y})	

	dicData.update({'savgl_pbsc1_X':savgl_pbsc1_X})
	dicData.update({'savgl_pbsc1_Y':savgl_pbsc1_Y})	

	dicData.update({'sarimax_pbsc1_X':sarimax_pbsc1_X})
	dicData.update({'sarimax_pbsc1_Y':sarimax_pbsc1_Y})

	# raw PER extension length
	dicData.update({'PER_exten_len':PER_exten_len})
	dicData.update({'smth_PER_exten_len':smth_PER_exten_len})		
	dicData.update({'med_PER_exten_len':med_PER_exten_len})
	dicData.update({'savgl_PER_exten_len':savgl_PER_exten_len})
	dicData.update({'sarimax_PER_exten_len':sarimax_PER_exten_len})	
	dicData.update({'fft_PER_exten_len':fft_PER_exten_len})	


	# PER extension normalized between 0 and 1
	dicData.update({'norm_range_PER_exten_len':norm_range_PER_exten_len})
	dicData.update({'norm_range_smth_PER_exten_len':norm_range_smth_PER_exten_len})		
	dicData.update({'norm_range_med_PER_exten_len':norm_range_med_PER_exten_len})
	dicData.update({'norm_range_savgl_PER_exten_len':norm_range_savgl_PER_exten_len})
	dicData.update({'norm_range_sarimax_PER_exten_len':norm_range_sarimax_PER_exten_len})
	dicData.update({'norm_range_fft_PER_exten_len':norm_range_fft_PER_exten_len})

	# PER extension (fold of baseline)
	dicData.update({'norm_baseFold_PER_exten_len':norm_baseFold_PER_exten_len})
	dicData.update({'norm_baseFold_smth_PER_exten_len':norm_baseFold_smth_PER_exten_len})		
	dicData.update({'norm_baseFold_med_PER_exten_len':norm_baseFold_med_PER_exten_len})
	dicData.update({'norm_baseFold_savgl_PER_exten_len':norm_baseFold_savgl_PER_exten_len})
	dicData.update({'norm_baseFold_sarimax_PER_exten_len':norm_baseFold_sarimax_PER_exten_len})
	dicData.update({'norm_baseFold_fft_PER_exten_len':norm_baseFold_fft_PER_exten_len})



	# PER events evt_bin_trace, evt_startIdx_list, evt_endIdx_list
	dicData.update({'evt_bin_trace':evt_bin_trace})
	dicData.update({'evt_startIdx_list':evt_startIdx_list})		
	dicData.update({'evt_endIdx_list':evt_endIdx_list})



	pickle.dump( dicData, open( outputPERdir + filename, "wb" ) ) 


	return




## Main ##

print('\n FigS1-2 executing ... \n')


NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_public_Dir

AN_Proj_Dir = NAS_AN_Proj_Dir


for date, genotype, fly, recrd_num, evt_detct_params in experiments:


	diff_thrsld=evt_detct_params['diff_thrsld']
	event_max_dur=evt_detct_params['event_max_dur']
	event_min_dur=evt_detct_params['event_min_dur']
	norm_thrsld=evt_detct_params['norm_thrsld']
	norm_change_thrsld=evt_detct_params['norm_change_thrsld']
	raw_change_thrsld=evt_detct_params['raw_change_thrsld']


	Gal4=genotype.split('-')[0]

	foroutDirtemp=AN_Proj_Dir+'00_behavior_data_preprocess/PE_regressors/'+Gal4+'/2P/'+date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num

	outputDir = foroutDirtemp+'/output/'

	PER_h5_Dir= outputDir + 'PER/camera_6/'
	print('PER_h5_Dir', PER_h5_Dir)

	

	outputPERdir = outputDir+'PER/camera_6/'

	if not os.path.exists(outputPERdir):
		os.makedirs(outputPERdir)

	outputPERplotdir = AN_Proj_Dir+'output/FigS1-exemplar_PEevt_detection/'

	if not os.path.exists(outputPERplotdir):
		os.makedirs(outputPERplotdir)



	dlc_h5_file = read_latest_h5(PER_h5_Dir)
	pbsc0_X, pbsc0_Y, pbsc1_X, pbsc1_Y = extract_coord(dlc_h5_file)
	# print('len pbsc0_X', len(pbsc0_X))

	fix_pbsc0_X, fix_pbsc0_Y = fix_point(pbsc0_X, pbsc0_Y)
	# print('fix_pbsc0_X', fix_pbsc0_X)
	# print('fix_pbsc0_Y', fix_pbsc0_Y)




	smth_pbsc1_X=filtered_traces(pbsc1_X, filtermode='running_window')
	smth_pbsc1_Y=filtered_traces(pbsc1_Y, filtermode='running_window')

	med_pbsc1_X=filtered_traces(pbsc1_X, filtermode='median')
	med_pbsc1_Y=filtered_traces(pbsc1_Y, filtermode='median')

	savgl_pbsc1_X=filtered_traces(pbsc1_X, filtermode='savgol_filter')
	savgl_pbsc1_Y=filtered_traces(pbsc1_Y, filtermode='savgol_filter')

	sarimax_pbsc1_X=filtered_traces(pbsc1_X, filtermode='sarimax')
	sarimax_pbsc1_Y=filtered_traces(pbsc1_Y, filtermode='sarimax')

	butter_pbsc1_X=filtered_traces(pbsc1_X, filtermode='butter_lowpass')
	butter_pbsc1_Y=filtered_traces(pbsc1_Y, filtermode='butter_lowpass')

	fft_pbsc1_X=filtered_traces(pbsc1_X, filtermode='fft_filter')
	fft_pbsc1_Y=filtered_traces(pbsc1_Y, filtermode='fft_filter')


	origin_pbsc1_X, origin_pbsc1_Y=find_origin_position(pbsc1_X, pbsc1_Y)
	origin_smth_pbsc1_X, origin_smth_pbsc1_Y=find_origin_position(smth_pbsc1_X, smth_pbsc1_Y)
	origin_med_pbsc1_X, origin_med_pbsc1_Y=find_origin_position(med_pbsc1_X, med_pbsc1_Y)
	origin_savgl_pbsc1_X, origin_savgl_pbsc1_Y=find_origin_position(savgl_pbsc1_X, savgl_pbsc1_Y)
	origin_sarimax_pbsc1_X, origin_sarimax_pbsc1_Y=find_origin_position(sarimax_pbsc1_X, sarimax_pbsc1_Y)
	origin_butter_pbsc1_X, origin_butter_pbsc1_Y=find_origin_position(butter_pbsc1_X, butter_pbsc1_Y)
	origin_fft_pbsc1_X, origin_fft_pbsc1_Y=find_origin_position(fft_pbsc1_X, fft_pbsc1_Y)


	# print('origin_pbsc1_X', origin_pbsc1_X)
	# print('origin_pbsc1_Y', origin_pbsc1_Y)


	PER_exten_len=[]
	for i in range(0, len(pbsc1_X)):
		dist=calc_length(origin_pbsc1_X, origin_pbsc1_Y, pbsc1_X[i], pbsc1_Y[i])
		PER_exten_len.append(dist)

	smth_PER_exten_len=[]
	for i in range(0, len(pbsc1_X)):
		dist=calc_length(origin_smth_pbsc1_X, origin_smth_pbsc1_Y, smth_pbsc1_X[i], smth_pbsc1_Y[i])
		smth_PER_exten_len.append(dist)

	med_PER_exten_len=[]
	for i in range(0, len(pbsc1_X)):
		dist=calc_length(origin_med_pbsc1_X, origin_med_pbsc1_Y, med_pbsc1_X[i], med_pbsc1_Y[i])
		med_PER_exten_len.append(dist)

	savgl_PER_exten_len=[]
	for i in range(0, len(pbsc1_X)):
		dist=calc_length(origin_savgl_pbsc1_X, origin_savgl_pbsc1_Y, savgl_pbsc1_X[i], savgl_pbsc1_Y[i])
		savgl_PER_exten_len.append(dist)
	
	sarimax_PER_exten_len=[]
	for i in range(0, len(pbsc1_X)):
		dist=calc_length(origin_sarimax_pbsc1_X, origin_sarimax_pbsc1_Y, sarimax_pbsc1_X[i], sarimax_pbsc1_Y[i])
		sarimax_PER_exten_len.append(dist)

	butter_PER_exten_len=[]
	for i in range(0, len(pbsc1_X)):
		dist=calc_length(origin_butter_pbsc1_X, origin_butter_pbsc1_Y, butter_pbsc1_X[i], butter_pbsc1_Y[i])
		butter_PER_exten_len.append(dist)

	fft_PER_exten_len=[]
	for i in range(0, len(pbsc1_X)):
		dist=calc_length(origin_fft_pbsc1_X, origin_fft_pbsc1_Y, fft_pbsc1_X[i], fft_pbsc1_Y[i])
		fft_PER_exten_len.append(dist)



	# med_PER_exten_len=cutting_outlier_in_trace(med_PER_exten_len, outlier_thrsld=outlier_thrsld, keep_side='lower')



	# normalize entension length to baseline as baseline at 1 and fold of length

	norm_baseFold_PER_exten_len = normalize_trace(PER_exten_len, frame_window=300, mode='fold_of_baseline')
	norm_baseFold_smth_PER_exten_len = normalize_trace(smth_PER_exten_len, frame_window=300, mode='fold_of_baseline')
	norm_baseFold_med_PER_exten_len = normalize_trace(med_PER_exten_len, frame_window=300, mode='fold_of_baseline')
	norm_baseFold_savgl_PER_exten_len = normalize_trace(savgl_PER_exten_len, frame_window=300, mode='fold_of_baseline')
	norm_baseFold_sarimax_PER_exten_len = normalize_trace(sarimax_PER_exten_len, frame_window=300, mode='fold_of_baseline')
	norm_baseFold_fft_PER_exten_len = normalize_trace(fft_PER_exten_len, frame_window=300, mode='fold_of_baseline')


	

	norm_range_PER_exten_len ,_ ,_ = normalize_trace(PER_exten_len, frame_window=300, mode='btwn_0and1')
	norm_range_smth_PER_exten_len ,_ ,_ = normalize_trace(smth_PER_exten_len, frame_window=300, mode='btwn_0and1')
	norm_range_med_PER_exten_len ,_ ,_ = normalize_trace(med_PER_exten_len, frame_window=300, mode='btwn_0and1')
	norm_range_savgl_PER_exten_len ,_ ,_ = normalize_trace(savgl_PER_exten_len, frame_window=300, mode='btwn_0and1')
	norm_range_sarimax_PER_exten_len ,_ ,_ = normalize_trace(sarimax_PER_exten_len, frame_window=300, mode='btwn_0and1')
	norm_range_fft_PER_exten_len ,_ ,_ = normalize_trace(fft_PER_exten_len, frame_window=300, mode='btwn_0and1')


	## The median filtered trace is the final decision to continue to following anaylsis since it denoise well and doesn't distort the signal too much
	norm_range_med_PER_exten_len_keep=keep_desired_range_of_trace(norm_range_med_PER_exten_len,  desireRanges=desiredRange_list)


	evt_bin_trace, evt_startIdx_list, evt_endIdx_list = detect_PER_event(norm_range_med_PER_exten_len_keep, med_PER_exten_len)


	for i, startidx in enumerate(evt_startIdx_list):
		endIdx=evt_endIdx_list[i]
		if endIdx<startidx:
			print('Evt_Start_Idx#'+str(startidx)+' has conflict with Evt_end_Idx#'+str(endIdx) + '... Please check again...')
			sys.exit(0)


	print('len med_PER_exten_len', len(med_PER_exten_len))
	print('len evt_bin_trace', len(evt_bin_trace))


	save_PER_dic(filename='PER_labels_camera_6.p')




if not os.path.exists(outputPERplotdir+'reminder.txt'):
	print('Writing reminder.txt')
	reminder_file = open(outputPERplotdir+"reminder.txt","a")
	reminder_file.write('You can find the numerical PER labels-- "PER_labels_camera_6.p" in the corresponding folder in 00_behavior_data_preprocess/PE_regressors/ .')
	reminder_file.close()







