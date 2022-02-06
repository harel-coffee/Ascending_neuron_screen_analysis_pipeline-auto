import numpy as np
import os
import sys
import pickle
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from skimage import io
import scipy


import utils.general_utils as general_utils
import utils.plot_utils as plot_utils
import utils.math_utils as math_utils
import utils.sync_utils as sync_utils
import utils.EventDetection_utils as EventDetection_utils
import utils.list_twoP_exp as list_twoP_exp










def organize_x_labels_for_plot(dictionary_allGal4):

	labels=[]
	for key, value in dictionary_allGal4.items():
		ROI_counts= len(value)
		for i in range(0, len(ROI_counts)):
			cur_lab=key+'-ROI_'+str(i)
			labels.append(cur_lab)

	return labels



def organize_GC_datapoint_per_ROI_for_plot(dictionary_allGal4):

	GCdatapoints_per_ROI=[]
	for key, value in dictionary_allGal4.items():
		ROI_counts= len(value)
		for i in range(0, len(ROI_counts)):
			GCdatapoints_per_ROI.append(value[i])

	return GCdatapoints_per_ROI





def decide_y_lim(list_datapoint):

	# print('list_datapoint', list_datapoint)

	# print('shape list_datapoint', np.shape(list_datapoint))


	flatten_list = general_utils.flatten_list(list_datapoint)
	fflatten_list = general_utils.flatten_list(flatten_list)

	# print('fflatten_list', fflatten_list)
	# print('shape fflatten_list', np.shape(fflatten_list))

	max_val=np.nanmax(fflatten_list)
	min_val=np.nanmin(fflatten_list)

	y_lim=[min_val, max_val]

	print('y_lim', y_lim)

	return y_lim



### main ####

NAS_Dir=general_utils.NAS_Dir
NAS_AN_Proj_Dir=general_utils.NAS_AN_Proj_public_Dir

off_ball_active_lines_ONBALL=list_twoP_exp.off_ball_active_lines_ONBALL
off_ball_active_lines_OFFBALL=list_twoP_exp.off_ball_active_lines_OFFBALL


### analyzing OFF-BALL recordings ####


cutting_head_s=0.7


meanGC_per_OFFBALLmovingEpoch_offballActiveGal4={}
meanGC_per_OFFBALLrestingEpoch_offballActiveGal4={} 


experiments_group_per_fly=general_utils.group_expList_per_fly(off_ball_active_lines_OFFBALL)



for exp_lists_per_fly in experiments_group_per_fly:


	for date, genotype, fly, recrd_num in exp_lists_per_fly:	

		print(date, genotype, fly, recrd_num)

		if not date+'-'+genotype+'-'+fly in meanGC_per_OFFBALLmovingEpoch_offballActiveGal4:
			meanGC_per_OFFBALLmovingEpoch_offballActiveGal4.update({date+'-'+genotype+'-'+fly:[]})
			meanGC_per_OFFBALLrestingEpoch_offballActiveGal4.update({date+'-'+genotype+'-'+fly:[]})


		Gal4=genotype.split('-')[0]
		fly_beh=fly[0].upper()+fly[1:]

		outDir_AN_recrd=NAS_AN_Proj_Dir+'05_offBall_onBall_2P_exp/'+Gal4+'/2P/'+date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num+'/output/'
		outDir_hangedfly=outDir_AN_recrd+'offBall_onBall_exp/'
		if not os.path.exists(outDir_hangedfly):
			os.makedirs(outDir_hangedfly)
		print('outDir_hangedfly', outDir_hangedfly)


		plot_outDir_hangedfly=NAS_AN_Proj_Dir+'output/FigS7-offballActive_ANs/plots/'
		if not os.path.exists(plot_outDir_hangedfly):
			os.makedirs(plot_outDir_hangedfly)


		offball_beh_GC_dic = general_utils.read_jointPos3d_Beh(outDir_hangedfly, 'offball_sync_Beh_GC_20220901.p')

		GC_set = offball_beh_GC_dic['GCset']
		timeSec = offball_beh_GC_dic['timeSec']

		rest = offball_beh_GC_dic['rest']
		move = offball_beh_GC_dic['move']

		CO2puff = offball_beh_GC_dic['CO2puff']

		Etho_Timesec_Dic = offball_beh_GC_dic['Etho_Timesec_Dic']
		Etho_Idx_Dic = offball_beh_GC_dic['Etho_Idx_Dic']

		datasamplerate=len(timeSec)/timeSec[-1]
		print('datasamplerate', datasamplerate)

		if (date, genotype, fly, recrd_num)==('20190604', 'SS38631-tdTomGC6fopt', 'fly2', '002') or (date, genotype, fly, recrd_num)==('20190904', 'SS51017-tdTomGC6fopt', 'fly3', '002'):
			plot_utils.Plot_whole_trace_off_ball(GC_set, CO2puff, timeSec, Etho_Timesec_Dic, date+'-'+genotype+'-'+fly+'-'+recrd_num+'_whole_trace_off_ball', filepath=plot_outDir_hangedfly)



		# bool_rest_trace=np.array(rest)>0.tolist()
		# bool_move_trace=np.array(move)>0.tolist()


		if len(meanGC_per_OFFBALLmovingEpoch_offballActiveGal4[date+'-'+genotype+'-'+fly])!=len(GC_set):
			for i in range(0, len(GC_set)):
				meanGC_per_OFFBALLmovingEpoch_offballActiveGal4[date+'-'+genotype+'-'+fly].append([])

		if len(meanGC_per_OFFBALLrestingEpoch_offballActiveGal4[date+'-'+genotype+'-'+fly])!=len(GC_set):
			for i in range(0, len(GC_set)):
				meanGC_per_OFFBALLrestingEpoch_offballActiveGal4[date+'-'+genotype+'-'+fly].append([])

		# for key, value in Etho_Idx_Dic.items():
		# 	print('key', key)
		# 	# print('value', value)
		# 	print('shape value', np.shape(value))

		# print('shape GC_set', np.shape(GC_set))


		GCsetEvt_move, _ = general_utils.find_corresponding_evt_from_groupIdxs(Etho_Idx_Dic, 'move_evt', GC_set, baseline=0, fps=datasamplerate)
		GCsetEvt_rest, _ = general_utils.find_corresponding_evt_from_groupIdxs(Etho_Idx_Dic, 'rest_evt', GC_set, baseline=0, fps=datasamplerate)

		# print('shape GCsetEvt_move', np.shape(GCsetEvt_move))
		# print('shape GCsetEvt_rest', np.shape(GCsetEvt_rest))

		# print('GCsetEvt_move', GCsetEvt_move)
		# print('GCsetEvt_rest', GCsetEvt_rest)

		mean_GCsetEvt_move=[]
		for ROI_i, GCevts in enumerate(GCsetEvt_move):
			mean_GCevts = math_utils.compute_mean_with_diffrerent_row_length(GCevts, samplerate=datasamplerate, cutting_head_s=cutting_head_s)
			mean_GCsetEvt_move.append(mean_GCevts)


		mean_GCsetEvt_rest=[]
		for ROI_i, GCevts in enumerate(GCsetEvt_rest):
			mean_GCevts = math_utils.compute_mean_with_diffrerent_row_length(GCevts, samplerate=datasamplerate, cutting_head_s=cutting_head_s)
			mean_GCsetEvt_rest.append(mean_GCevts)

		# print('mean_GCsetEvt_move', mean_GCsetEvt_move)
		# print('mean_GCsetEvt_rest', mean_GCsetEvt_rest)
		# print('shape mean_GCsetEvt_move', np.shape(mean_GCsetEvt_move))
		# print('shape mean_GCsetEvt_rest',np.shape(mean_GCsetEvt_rest))

		for i in range(0, len(GC_set)):
			meanGC_per_OFFBALLmovingEpoch_offballActiveGal4[date+'-'+genotype+'-'+fly][i].extend(mean_GCsetEvt_move[i])
			meanGC_per_OFFBALLrestingEpoch_offballActiveGal4[date+'-'+genotype+'-'+fly][i].extend(mean_GCsetEvt_rest[i])










### analyze ON-BALL recording ###



meanGC_per_ONBALLmovingEpoch_offballActiveGal4={}
meanGC_per_ONBALLrestingEpoch_offballActiveGal4={} 

experiments_group_per_fly=general_utils.group_expList_per_fly(off_ball_active_lines_ONBALL)



for exp_lists_per_fly in experiments_group_per_fly:


	for date, genotype, fly, recrd_num in exp_lists_per_fly:	

		print(date, genotype, fly, recrd_num)

		if not date+'-'+genotype+'-'+fly in meanGC_per_ONBALLmovingEpoch_offballActiveGal4:
			meanGC_per_ONBALLmovingEpoch_offballActiveGal4.update({date+'-'+genotype+'-'+fly:[]})
			meanGC_per_ONBALLrestingEpoch_offballActiveGal4.update({date+'-'+genotype+'-'+fly:[]})


		Gal4=genotype.split('-')[0]
		fly_beh=fly[0].upper()+fly[1:]

		outDir_AN_recrd=NAS_AN_Proj_Dir+'05_offBall_onBall_2P_exp/'+Gal4+'/2P/'+date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num+'/output/'
		outDir_hangedfly=outDir_AN_recrd+'offBall_onBall_exp/'
		if not os.path.exists(outDir_hangedfly):
			os.makedirs(outDir_hangedfly)
		print('outDir_hangedfly', outDir_hangedfly)

	

		plot_outDir_hangedfly=NAS_AN_Proj_Dir+'output/FigS7-offballActive_ANs/plots/'
		if not os.path.exists(plot_outDir_hangedfly):
			os.makedirs(plot_outDir_hangedfly)



		if os.path.exists(outDir_hangedfly+'onBall_sync_Beh_GC.p'):
			offball_beh_GC_dic = general_utils.read_jointPos3d_Beh(outDir_hangedfly, 'onBall_sync_Beh_GC.p')
			GC_set = offball_beh_GC_dic['GCset']
			timeSec = offball_beh_GC_dic['timeSec']

			rest = offball_beh_GC_dic['rest']
			f_walk = offball_beh_GC_dic['forward_walk']
			b_walk = offball_beh_GC_dic['backward_walk']
			Push = offball_beh_GC_dic['Push']
			SixLeg_move = np.asarray(f_walk)+np.asarray(b_walk)+np.asarray(Push)


			CO2puff = offball_beh_GC_dic['CO2puff']

			Etho_Timesec_Dic = offball_beh_GC_dic['Etho_Timesec_Dic']
			Etho_Idx_Dic = offball_beh_GC_dic['Etho_Idx_Dic']

			datasamplerate=len(timeSec)/timeSec[-1]

			SixLeg_move_LP = math_utils.hysteresis_filter(SixLeg_move, n=int(datasamplerate*0.06))*1	
			idx_SixLeg_move_evt, timesec_SixLeg_move_evt=sync_utils.Calculate_idx_time_for_bin_beh_trace(SixLeg_move_LP, timeSec)

			Etho_Idx_Dic.update({'move_evt':idx_SixLeg_move_evt})
			Etho_Timesec_Dic.update({'move_evt':timesec_SixLeg_move_evt})

		else:
			print(outDir_hangedfly, 'onBall_sync_Beh_GC.p', 'is missing...')
			sys.exit(0)



		if (date, genotype, fly, recrd_num)==('20190604', 'SS38631-tdTomGC6fopt', 'fly2', '006') or (date, genotype, fly, recrd_num)==('20190904', 'SS51017-tdTomGC6fopt', 'fly3', '003'):
			plot_utils.Plot_whole_trace_off_ball(GC_set, CO2puff, timeSec, Etho_Timesec_Dic, date+'-'+genotype+'-'+fly+'-'+recrd_num+'_whole_trace_on_ball', filepath=plot_outDir_hangedfly)
		




		if len(meanGC_per_ONBALLmovingEpoch_offballActiveGal4[date+'-'+genotype+'-'+fly])!=len(GC_set):
			for i in range(0, len(GC_set)):
				meanGC_per_ONBALLmovingEpoch_offballActiveGal4[date+'-'+genotype+'-'+fly].append([])

		if len(meanGC_per_ONBALLrestingEpoch_offballActiveGal4[date+'-'+genotype+'-'+fly])!=len(GC_set):
			for i in range(0, len(GC_set)):
				meanGC_per_ONBALLrestingEpoch_offballActiveGal4[date+'-'+genotype+'-'+fly].append([])


		GCsetEvt_move, _ = general_utils.find_corresponding_evt_from_groupIdxs(Etho_Idx_Dic, 'move_evt', GC_set, baseline=0, fps=datasamplerate)
		GCsetEvt_rest, _ = general_utils.find_corresponding_evt_from_groupIdxs(Etho_Idx_Dic, 'rest_evt', GC_set, baseline=0, fps=datasamplerate)

		# print('shape GCsetEvt_move', np.shape(GCsetEvt_move))
		# print('shape GCsetEvt_rest', np.shape(GCsetEvt_rest))

		mean_GCsetEvt_move=[]
		for ROI_i, GCevts in enumerate(GCsetEvt_move):
			mean_GCevts = math_utils.compute_mean_with_diffrerent_row_length(GCevts, samplerate=datasamplerate, cutting_head_s=cutting_head_s)
			mean_GCsetEvt_move.append(mean_GCevts)


		mean_GCsetEvt_rest=[]
		for ROI_i, GCevts in enumerate(GCsetEvt_rest):
			mean_GCevts = math_utils.compute_mean_with_diffrerent_row_length(GCevts, samplerate=datasamplerate, cutting_head_s=cutting_head_s)
			mean_GCsetEvt_rest.append(mean_GCevts)

		# print('mean_GCsetEvt_move', mean_GCsetEvt_move)
		# print('mean_GCsetEvt_rest', mean_GCsetEvt_rest)

		for i in range(0, len(GC_set)):
			meanGC_per_ONBALLmovingEpoch_offballActiveGal4[date+'-'+genotype+'-'+fly][i].extend(mean_GCsetEvt_move[i])
			meanGC_per_ONBALLrestingEpoch_offballActiveGal4[date+'-'+genotype+'-'+fly][i].extend(mean_GCsetEvt_rest[i])





# print('meanGC_per_OFFBALLmovingEpoch_offballActiveGal4.keys()', meanGC_per_OFFBALLmovingEpoch_offballActiveGal4.keys())
# print('meanGC_per_ONBALLmovingEpoch_offballActiveGal4.keys()', meanGC_per_ONBALLmovingEpoch_offballActiveGal4.keys())
# print('meanGC_per_OFFBALLrestingEpoch_offballActiveGal4.keys()', meanGC_per_OFFBALLrestingEpoch_offballActiveGal4.keys())
# print('meanGC_per_ONBALLrestingEpoch_offballActiveGal4.keys()', meanGC_per_ONBALLrestingEpoch_offballActiveGal4.keys())








## off-ball active Gal4 lines off-ball comparison (move vs rest) stats. ##
for fly_exp, GC_set in meanGC_per_OFFBALLrestingEpoch_offballActiveGal4.items():

	GC_OFFBALLresting_set = GC_set
	GC_ONBALLresting_set = meanGC_per_ONBALLrestingEpoch_offballActiveGal4[fly_exp]
	GC_OFFBALLmoving_set = meanGC_per_OFFBALLmovingEpoch_offballActiveGal4[fly_exp]
	GC_ONBALLmoving_set = meanGC_per_ONBALLmovingEpoch_offballActiveGal4[fly_exp]


	#list_datapoint=[GC_OFFBALLmoving_set, GC_ONBALLmoving_set, GC_OFFBALLresting_set, GC_ONBALLresting_set]
	list_datapoint=[GC_OFFBALLmoving_set, GC_OFFBALLresting_set, GC_ONBALLmoving_set,  GC_ONBALLresting_set]
	y_lim=decide_y_lim(list_datapoint)


	Gal4_labels=[]
	p_value_list=[]
	for ROI_i, GC_datapoint_OFFBALLresting in enumerate(GC_OFFBALLresting_set):

		GC_datapoint_OFFBALLmoving=GC_OFFBALLmoving_set[ROI_i]

		fold=10
		votes=[]
		for i in range(0,fold):
			gc_point_offballmove_sampled=np.random.choice(GC_datapoint_OFFBALLmoving, size=29)
			gc_point_offballrest_sampled=np.random.choice(GC_datapoint_OFFBALLresting, size=29)

			U_value, p_value = scipy.stats.mannwhitneyu(gc_point_offballmove_sampled, gc_point_offballrest_sampled)
			# t_value, p_value = scipy.stats.ttest_ind(GC_datapoint_OFFBALLmoving, GC_datapoint_OFFBALLresting)
			print('p_value', p_value)
			votes.append(p_value)


		Gal4_labels.append('ROI_'+str(ROI_i))
		count_p_lessthan_005=sum(map(lambda x : x<0.05, votes))
		print(count_p_lessthan_005, 'out of', fold, 'Mann-Whitney test are <0.05.')

		if count_p_lessthan_005<=len(votes)*0.6:
			print('-->GC datapoint is no different between MOVE and REST')
			p_value_list.append(1)
		else:
			print('-->GC datapoint is significant different between MOVE and REST')
			
			count_p_lessthan_0001=sum(map(lambda x : x<0.001, votes))
			count_p_lessthan_001=sum(map(lambda x : x<0.01, votes))-count_p_lessthan_0001
			count_p_lessthan_005=sum(map(lambda x : x<0.05, votes))-count_p_lessthan_0001-count_p_lessthan_001

			p_vote_list=[count_p_lessthan_005, count_p_lessthan_001, count_p_lessthan_0001]
			max_p_vote_idx=	p_vote_list.index(max(p_vote_list))	
			if max_p_vote_idx==0:
				p_value_list.append(0.04)	
			elif max_p_vote_idx==1:
				p_value_list.append(0.009)	
			elif max_p_vote_idx==2:
				p_value_list.append(0.0009)	




	filename=fly_exp+'-off-ball'
	NAS_AN_Proj_Dir
	savedir = NAS_AN_Proj_Dir+'output/FigS7-offballActive_ANs/plots/'
	if not os.path.exists(savedir):
		os.makedirs(savedir)
	labels=['rest', 'move']



	print('shape Gal4_labels', np.shape(Gal4_labels))
	print('shape GC_datapoint_OFFBALLmoving', np.shape(GC_datapoint_OFFBALLmoving))
	print('shape GC_datapoint_OFFBALLresting', np.shape(GC_datapoint_OFFBALLresting))


	plot_utils.plot_group_bar_w_scatterPoints(Gal4_labels, GC_OFFBALLresting_set, GC_OFFBALLmoving_set, y_lim, p_value_list, labels, savedir, filename,  exp_color='b')





## off-ball active Gal4 lines on-ball comparison (move vs rest) stats. ##
for fly_exp, GC_set in meanGC_per_OFFBALLrestingEpoch_offballActiveGal4.items():

	GC_OFFBALLresting_set = GC_set
	GC_ONBALLresting_set = meanGC_per_ONBALLrestingEpoch_offballActiveGal4[fly_exp]
	GC_OFFBALLmoving_set = meanGC_per_OFFBALLmovingEpoch_offballActiveGal4[fly_exp]
	GC_ONBALLmoving_set = meanGC_per_ONBALLmovingEpoch_offballActiveGal4[fly_exp]


	#list_datapoint=[ GC_ONBALLmoving_set,  GC_ONBALLresting_set, GC_OFFBALLresting_set, GC_OFFBALLmoving_set]
	list_datapoint=[ GC_ONBALLmoving_set,  GC_ONBALLresting_set, GC_OFFBALLmoving_set, GC_OFFBALLresting_set]
	y_lim=decide_y_lim(list_datapoint)


	Gal4_labels=[]
	p_value_list=[]
	for ROI_i, GC_datapoint_ONBALLresting in enumerate(GC_ONBALLresting_set):

		GC_datapoint_ONBALLmoving=GC_ONBALLmoving_set[ROI_i]

		fold=10
		votes=[]
		for i in range(0,fold):
			gc_point_onballmove_sampled=np.random.choice(GC_datapoint_ONBALLmoving, size=29)
			gc_point_onballrest_sampled=np.random.choice(GC_datapoint_ONBALLresting, size=29)


			U_value, p_value = scipy.stats.mannwhitneyu(gc_point_onballmove_sampled, gc_point_onballrest_sampled)
			# t_value, p_value = scipy.stats.ttest_ind(GC_datapoint_ONBALLmoving, GC_datapoint_ONBALLresting)
			print('p_value', p_value)

			votes.append(p_value)

		Gal4_labels.append('ROI_'+str(ROI_i))
		count_p_lessthan_005=sum(map(lambda x : x<0.05, votes))
		print(count_p_lessthan_005, 'out of', fold, 'Mann-Whitney test are <0.05.')

		if count_p_lessthan_005<=len(votes)*0.6:
			print('-->GC datapoint is no different between MOVE and REST')
			p_value_list.append(1)
		else:
			print('-->GC datapoint is significant different between MOVE and REST')
			
			count_p_lessthan_0001=sum(map(lambda x : x<0.001, votes))
			count_p_lessthan_001=sum(map(lambda x : x<0.01, votes))-count_p_lessthan_0001
			count_p_lessthan_005=sum(map(lambda x : x<0.05, votes))-count_p_lessthan_0001-count_p_lessthan_001

			p_vote_list=[count_p_lessthan_005, count_p_lessthan_001, count_p_lessthan_0001]
			max_p_vote_idx=	p_vote_list.index(max(p_vote_list))	
			if max_p_vote_idx==0:
				p_value_list.append(0.04)	
			elif max_p_vote_idx==1:
				p_value_list.append(0.009)	
			elif max_p_vote_idx==2:
				p_value_list.append(0.0009)	



	filename=fly_exp+'-on-ball'
	savedir = NAS_AN_Proj_Dir+'output/FigS7-offballActive_ANs/plots/'
	if not os.path.exists(savedir):
		os.makedirs(savedir)
	labels=['rest', 'move']


	print('shape Gal4_labels', np.shape(Gal4_labels))
	print('shape GC_ONBALLmoving_set', np.shape(GC_ONBALLmoving_set))
	print('shape GC_ONBALLresting_set', np.shape(GC_ONBALLresting_set))


	plot_utils.plot_group_bar_w_scatterPoints(Gal4_labels, GC_ONBALLresting_set, GC_ONBALLmoving_set, y_lim, p_value_list, labels, savedir, filename, exp_color='b')





# Labels_for_offballActiveGal4=organize_x_labels_for_plot(meanGC_per_OFFBALLmovingEpcoch_offballActiveGal4)
# GCdatapoints_per_ROI_OFFBALLmoving_offballActiveGal4=organize_GC_datapoint_per_ROI_for_plot(meanGC_per_OFFBALLmovingEpcoch_offballActiveGal4)
# GCdatapoints_per_ROI_ONBALLmoving_offballActiveGal4=organize_GC_datapoint_per_ROI_for_plot(meanGC_per_ONBALLmovingEpcoch_offballActiveGal4)


# for fly, GC_values in meanGC_per_OFFBALLmovingEpcoch_offballActiveGal4.items():




# meanGC_per_OFFBALLmovingEpcoch_offballActiveGal4
# meanGC_per_ONBALLmovingEpcoch_offballActiveGal4

# meanGC_per_OFFBALLrestingEpcoch_offballActiveGal4
# meanGC_per_ONBALLrestingEpcoch_offballActiveGal4







































