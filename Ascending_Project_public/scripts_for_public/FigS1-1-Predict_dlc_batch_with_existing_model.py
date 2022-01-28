"""
Must do:
source activate DLC-CPU first!!!!
"""

print('\n FigS1-1 executing ... \n')


import sys
import os
import deeplabcut

# import utils.general_utils as general_utils


root=os.path.abspath("../../")+'/'
print(root)

NAS_Dir=root
NAS_AN_Proj_Dir=root+'Ascending_Project_public/'
AN_Proj_Dir = NAS_AN_Proj_Dir


path_model_config_file=NAS_AN_Proj_Dir+'DLC_model_for_labelling_proboscis/config.yaml'





# # For refining and re-training the network:
# deeplabcut.extract_outlier_frames(path_model_config_file,videofile_path)
# deeplabcut.refine_labels(path_model_config_file)
# deeplabcut.merge_datasets(path_model_config_file)
# deeplabcut.create_training_dataset(path_model_config_file)
# deeplabcut.train_network(path_model_config_file, displayiters=500, saveiters=1000, maxiters=11000)
# deeplabcut.evaluate_network(path_model_config_file, plotting=True)
# sys.exit(0)


video_cam=6


experiments=[
('20190412', 'SS31232-tdTomGC6fopt', 'fly3', '002'),
]


# For making prediction on video
for date, genotype, fly, recrd_num in experiments:

	Gal4=genotype.split('-')[0]
	fly_beh=fly[0].upper()+fly[1:]


	foroutDirtemp=AN_Proj_Dir+'00_behavior_data_preprocess/PE_regressors/'+Gal4+'/2P/'+date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+recrd_num
	outputDir = foroutDirtemp+'/output/'

	PER_h5_Dir= outputDir + 'PER/camera_6/'
	videoname = date[2:]+'_'+genotype+'-'+fly+'-'+recrd_num+'_camera_'+str(video_cam)

	video_path=PER_h5_Dir+videoname+'.mp4'


	dlc_h5_file=videoname+'DLC_resnet50_PERMar18shuffle1_10000.h5'

	path=[video_path]


	if not os.path.exists(PER_h5_Dir+dlc_h5_file):

		print('\nDLC process in ', (date, genotype, fly, recrd_num),'\n')

		deeplabcut.analyze_videos(path_model_config_file, path,  save_as_csv=True, videotype='.mp4')
		# deeplabcut.create_labeled_video(path_model_config_file, path, draw_skeleton=True, videotype='mp4')
		# deeplabcut.plot_trajectories(path_model_config_file, path)
			


	else: 
		print('DLC_resnet50_PERMar18shuffle1_10000.h5 already exists')




