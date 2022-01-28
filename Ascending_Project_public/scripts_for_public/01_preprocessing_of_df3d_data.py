import os
import glob
import pickle
import json
import itertools

import numpy as np
import pandas as pd



import deepfly.signal_util
import deepfly.core
from deepfly.cv_util import triangulate_linear
from deepfly.procrustes import procrustes_seperate

import df3dPostProcessing


import utils2p
import flydf

import utils_Florian


if not os.path.isdir(utils_Florian.output_dir):
    raise RuntimeError(f"Output directory {utils_Florian.output_dir} does not exist. It is specified in utils_Florian.py and created by 00_trials_for_paper.py.")

update = False
output_file = os.path.join(utils_Florian.output_dir, "df_joint_pos_joint_angles_opt_flow.pkl")

def triangulate(camNet, cam_id_list,img_id, j_id):
    cam_list_iter = list()
    points2d_iter = list()
    for cam in [camNet.cam_list[cam_idx] for cam_idx in cam_id_list]:
        cam_list_iter.append(cam)
        points2d_iter.append(cam[img_id, j_id, :])
    return triangulate_linear(cam_list_iter, points2d_iter)

gain_0_x = round(1 / 1.45, 2)
gain_0_y = round(1 / 1.41, 2)
gain_1_x = round(1 / 1.40, 2)
gain_1_y = round(1 / 1.36, 2)

folders_without_df3d = ""
df3d_outliers = {}

if update:
    data = pd.read_pickle(output_file)
else:
    data = pd.DataFrame(columns=["Genotype", "Date", "Fly", "Trial", "Frame"])

error_stream = ""

for i, exp in enumerate(itertools.chain(utils_Florian.exp_generator_paper_trials(os.path.join(utils_Florian.output_dir, "trials_for_paper.pkl")),
                                        utils_Florian.exp_generator_annotations(os.path.join(utils_Florian.annotation_dir, "behaviour_annotations.csv")))):
    try:
        date = int(exp[0])
        genotype = exp[1]
        fly = int(exp[2][3:])
        trial = int(exp[3])
        exp = (date, genotype, fly, trial)
        
        directory = utils_Florian.beh_dir(*exp)

        print("\n" + directory + "\n" + len(directory) * "#")

        if flydf.get_trial_df(data, genotype, date, fly, trial).shape[0] != 0:
            print("Skipped because it already exists in df.")
            continue


        if os.path.isdir(os.path.join(directory, "images/df3d_corr/")):
            output_subfolder = "df3d_corr"
        else: 
            output_subfolder = "df3d_2"
        possible_pose_results = glob.glob(os.path.join(directory, f"images/{output_subfolder}/pose_result*.pkl"))
        change_times = [os.stat(path).st_mtime for path in possible_pose_results]
        try:
            most_recent_pose_result = possible_pose_results[np.argmax(change_times)]
        except ValueError:
            folders_without_df3d += (directory + "\n")
            print("Skipped because df3d output is missing.")
            continue
        
        if output_subfolder != "df3d_corr":
            # Fix outliers due to wrong 2D prediction of one camera
            image_dir = os.path.join(directory, "images")
            c = deepfly.core.Core(input_folder=image_dir,
                                  output_subfolder=output_subfolder,
                                  num_images_max=7500,
                                 )
  

            c.camNetAll.triangulate()

            # Find outliers (number of image and joint)
            outlier_img_ids = np.where(np.abs(c.camNetAll.points3d) > 5)[0]
            outlier_joint_ids = np.where(np.abs(c.camNetAll.points3d) > 5)[1]
            if len(outlier_img_ids) > 0:
                df3d_outliers[directory] = {"Image id": list(map(int, list(outlier_img_ids))), "Joint ids": list(map(int, list(outlier_joint_ids)))}

            # Fix outliers that were found
            for img_id, joint_id in zip(outlier_img_ids, outlier_joint_ids):
                reprojection_errors = list()
                points_using_2_cams = list()
                # Select cameras based on which side the joint is on
                all_cam_ids = [0, 1, 2] if joint_id < 19 else [4, 5, 6]
                # Try all possible combinations of 2 cameras
                for subset_cam_ids in itertools.combinations(all_cam_ids, 2):
                    points3d_using_2_cams = triangulate(c.camNetAll, subset_cam_ids, img_id, joint_id)
                    reprojection_error_function = lambda cam_id: c.camNetAll.cam_list[cam_id].project(points3d_using_2_cams) - c.camNetAll.cam_list[cam_id].points2d[img_id, joint_id]
                    reprojection_error = np.mean([reprojection_error_function(cam_id) for cam_id in subset_cam_ids])
                    reprojection_errors.append(reprojection_error)
                    points_using_2_cams.append(points3d_using_2_cams)
                # Replace 3D points with best estimation from 2 cameras only
                best_cam_tuple_index = np.argmin(reprojection_errors)
                c.camNetAll.points3d[img_id, joint_id] = points_using_2_cams[best_cam_tuple_index]

            points = procrustes_seperate(c.camNetAll.points3d)
        else:
            points = np.load(most_recent_pose_result, allow_pickle=True)["points3d"]

        
        # Filter data
        points_filtered = deepfly.signal_util.filter_batch(points, freq=30)

        pickle_data = np.load(most_recent_pose_result, allow_pickle=True)
        # pickle_data = pickle.load(open(most_recent_pose_result, 'rb'))
        # print(pickle_data)

        pickle_data["points3d"] = points_filtered
        filtered_pickle = most_recent_pose_result.replace(".pkl", "_filtered.pkl")
        try:
            with open(filtered_pickle, "wb") as f:
                pickle.dump(pickle_data, f)
            df3dPost = df3dPostProcessing.df3dPostProcess(filtered_pickle)
        finally:
            os.remove(filtered_pickle)

        #print(df3dPost)

        aligned = df3dPost.align_3d_data(rescale=False)
        points_filtered_aligned, aligned_columns = df3dPostProcessing.convert_to_df3d_output_format(aligned)
        points_filtered_aligned = points_filtered_aligned.reshape((points_filtered_aligned.shape[0], -1))
        aligned_columns = [f"{col} {axis}" for col in aligned_columns for axis in ["x", "y", "z"]]
   
        # Drop the antenna and stripes
        mask = ["antenna" not in col and "stripe" not in col for col in aligned_columns]
        points_filtered_aligned = points_filtered_aligned[:, mask]
        aligned_columns = list(itertools.compress(aligned_columns, mask))

        angles = df3dPost.calculate_leg_angles()
        angles, angle_columns = df3dPostProcessing.angles_as_list(angles)
        
        # Load optical flow data
        co2_line, cam_line, opt_flow_line, frame_counter = utils_Florian.get_processed_sync_lines(*exp)
        print('cam_line', cam_line)
        optical_flow_path = utils2p.find_optical_flow_file(directory)
        smoothing_kernel = np.ones(81) / 81
        optical_flow = utils2p.load_optical_flow(optical_flow_path, gain_0_x, gain_0_y, gain_1_x, gain_1_y, smoothing_kernel=smoothing_kernel)
        
        pitch, roll, yaw = utils_Florian.optical_flow_regressors(cam_line, opt_flow_line, optical_flow)
        pitch = pitch[:, np.newaxis]
        roll = roll[:, np.newaxis]
        yaw = yaw[:, np.newaxis]


        cam_frames = np.sort(np.unique(cam_line))
        print('cam_frames', cam_frames)
        columns = ["Frame", ] + aligned_columns + angle_columns + ["Pitch", "Roll", "Yaw", ]
        data_matrix = np.concatenate([cam_frames[:, np.newaxis],
                                      points_filtered_aligned[cam_frames],
                                      angles[cam_frames],
                                      pitch,
                                      roll,
                                      yaw
                                     ], axis=1)
        data = flydf.add_data(data, genotype, date, fly, trial, columns, data_matrix)
        
        
        data.to_pickle(output_file)
    
    except Exception as err:
        print()
        error_stream += directory + "\n"
        error_stream += f"{err}"
        error_stream += "\n\n\n"
        raise(err)


   
    finally:
        with open(os.path.join(utils_Florian.output_dir, "error_stream_01.txt"), "w") as f:
            f.write(error_stream)


with open(os.path.join(utils_Florian.output_dir, "folders_without_df3d.txt"), "w") as f:
    f.write(folders_without_df3d)
with open(os.path.join(utils_Florian.output_dir, "df3d_outliers.json"), "w") as f:
    json.dump(df3d_outliers, f, sort_keys=True, indent=4)
