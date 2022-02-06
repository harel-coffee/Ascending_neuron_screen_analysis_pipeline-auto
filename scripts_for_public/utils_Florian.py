import os.path
import pickle
import sys

import pandas as pd
import numpy as np
from tqdm import tqdm
import behavelet

import utils2p
import utils2p.synchronization
import flydf

root_dir=os.path.abspath("../..")+'/'
# print(root_dir)
# root_dir="/mnt/data/CLC/"


annotation_dir=root_dir+"Ascending_neuron_screen_analysis_pipeline/01_behavior_annotation_for_behavior_classifier/"
output_dir = root_dir+"Ascending_neuron_screen_analysis_pipeline/output/Fig2_S4-GLM_jangles_legs_beh_DFF/"

position_columns = [
    "LF_leg Coxa x",
    "LF_leg Coxa y",
    "LF_leg Coxa z",
    "LF_leg Femur x",
    "LF_leg Femur y",
    "LF_leg Femur z",
    "LF_leg Tibia x",
    "LF_leg Tibia y",
    "LF_leg Tibia z",
    "LF_leg Tarsus x",
    "LF_leg Tarsus y",
    "LF_leg Tarsus z",
    "LF_leg Claw x",
    "LF_leg Claw y",
    "LF_leg Claw z",
    "LM_leg Coxa x",
    "LM_leg Coxa y",
    "LM_leg Coxa z",
    "LM_leg Femur x",
    "LM_leg Femur y",
    "LM_leg Femur z",
    "LM_leg Tibia x",
    "LM_leg Tibia y",
    "LM_leg Tibia z",
    "LM_leg Tarsus x",
    "LM_leg Tarsus y",
    "LM_leg Tarsus z",
    "LM_leg Claw x",
    "LM_leg Claw y",
    "LM_leg Claw z",
    "LH_leg Coxa x",
    "LH_leg Coxa y",
    "LH_leg Coxa z",
    "LH_leg Femur x",
    "LH_leg Femur y",
    "LH_leg Femur z",
    "LH_leg Tibia x",
    "LH_leg Tibia y",
    "LH_leg Tibia z",
    "LH_leg Tarsus x",
    "LH_leg Tarsus y",
    "LH_leg Tarsus z",
    "LH_leg Claw x",
    "LH_leg Claw y",
    "LH_leg Claw z",
    "RF_leg Coxa x",
    "RF_leg Coxa y",
    "RF_leg Coxa z",
    "RF_leg Femur x",
    "RF_leg Femur y",
    "RF_leg Femur z",
    "RF_leg Tibia x",
    "RF_leg Tibia y",
    "RF_leg Tibia z",
    "RF_leg Tarsus x",
    "RF_leg Tarsus y",
    "RF_leg Tarsus z",
    "RF_leg Claw x",
    "RF_leg Claw y",
    "RF_leg Claw z",
    "RM_leg Coxa x",
    "RM_leg Coxa y",
    "RM_leg Coxa z",
    "RM_leg Femur x",
    "RM_leg Femur y",
    "RM_leg Femur z",
    "RM_leg Tibia x",
    "RM_leg Tibia y",
    "RM_leg Tibia z",
    "RM_leg Tarsus x",
    "RM_leg Tarsus y",
    "RM_leg Tarsus z",
    "RM_leg Claw x",
    "RM_leg Claw y",
    "RM_leg Claw z",
    "RH_leg Coxa x",
    "RH_leg Coxa y",
    "RH_leg Coxa z",
    "RH_leg Femur x",
    "RH_leg Femur y",
    "RH_leg Femur z",
    "RH_leg Tibia x",
    "RH_leg Tibia y",
    "RH_leg Tibia z",
    "RH_leg Tarsus x",
    "RH_leg Tarsus y",
    "RH_leg Tarsus z",
    "RH_leg Claw x",
    "RH_leg Claw y",
    "RH_leg Claw z",
]

angle_columns = [
    "LF_leg yaw",
    "LF_leg pitch",
    "LF_leg roll",
    "LF_leg th_fe",
    "LF_leg th_ti",
    "LF_leg roll_tr",
    "LF_leg th_ta",
    "LM_leg yaw",
    "LM_leg pitch",
    "LM_leg roll",
    "LM_leg th_fe",
    "LM_leg th_ti",
    "LM_leg roll_tr",
    "LM_leg th_ta",
    "LH_leg yaw",
    "LH_leg pitch",
    "LH_leg roll",
    "LH_leg th_fe",
    "LH_leg th_ti",
    "LH_leg roll_tr",
    "LH_leg th_ta",
    "RF_leg yaw",
    "RF_leg pitch",
    "RF_leg roll",
    "RF_leg th_fe",
    "RF_leg th_ti",
    "RF_leg roll_tr",
    "RF_leg th_ta",
    "RM_leg yaw",
    "RM_leg pitch",
    "RM_leg roll",
    "RM_leg th_fe",
    "RM_leg th_ti",
    "RM_leg roll_tr",
    "RM_leg th_ta",
    "RH_leg yaw",
    "RH_leg pitch",
    "RH_leg roll",
    "RH_leg th_fe",
    "RH_leg th_ti",
    "RH_leg roll_tr",
    "RH_leg th_ta",
]


def exp_generator_paper_trials(path):
    df = pd.read_pickle(path)
    for i, row in df.iterrows():
        date = str(row["Date"])
        genotype = row["Genotype"]
        fly = f"fly{row['Fly']}"
        trial = f"{row['Trial']:03}"
        yield (date, genotype, fly, trial)


def exp_generator_annotations(path):
    df = pd.read_csv(path)
    df = df[["Date", "Genotype", "Fly", "Trial"]]
    df = df.drop_duplicates()
    for i, row in df.iterrows():
        date = str(row["Date"])
        genotype = row["Genotype"]
        fly = f"fly{row['Fly']}"
        trial = f"{row['Trial']:03}"

        yield (date, genotype, fly, trial)


def beh_dir(date, genotype, fly, trial):
    return root_dir+f"Ascending_neuron_screen_analysis_pipeline/00_behavior_data_preprocess/df3dResults_ballRot_captureMeta/{date - 20000000}_{genotype}/Fly{fly}/CO2xzGG/behData_{trial:03d}/"


def sync_dir(date, genotype, fly, trial):
    Gal4=genotype.split('-')[0]
    return root_dir+f"Ascending_neuron_screen_analysis_pipeline/03_general_2P_exp/{Gal4}/2P/{date}/{genotype}-fly{fly}/{genotype}-fly{fly}-sync-{trial:03d}"


def dir_2p(date, genotype, fly, trial):
    Gal4=genotype.split('-')[0]
    return root_dir+f"Ascending_neuron_screen_analysis_pipeline/03_general_2P_exp/{Gal4}/2P/{date}/{genotype}-fly{fly}/{genotype}-fly{fly}-{trial:03d}"


def clc_output_dir(date, genotype, fly, trial):
    return root_dir+f"Ascending_neuron_screen_analysis_pipeline/03_general_2P_exp/{genotype.split('-')[0]}/2P/{date}/{genotype}-fly{fly}/{genotype}-fly{fly}-{trial:03d}/output"


def get_processed_sync_lines(date, genotype, fly, trial):
    Gal4=genotype.split('-')[0]
    dir_beh = beh_dir(date, genotype, fly, trial)
    dir_sync = sync_dir(date, genotype, fly, trial)
    dir2p = dir_2p(date, genotype, fly, trial)
    h5_path = utils2p.find_sync_file(dir_sync)
    co2_line, cam_line, opt_flow_line, frame_counter, capture_on = utils2p.synchronization.get_lines_from_h5_file(h5_path, ["CO2_Stim", "Basler", "OpFlow", "Frame Counter", "Capture On"])
    try:
        capture_json = utils2p.find_seven_camera_metadata_file(dir_beh)
    except FileNotFoundError:
        capture_json = None
    metadata_2p = utils2p.find_metadata_file(dir2p)
    metadata = utils2p.Metadata(metadata_2p)

    cam_line = utils2p.synchronization.process_cam_line(cam_line, capture_json)

    opt_flow_line = utils2p.synchronization.process_optical_flow_line(opt_flow_line)

    n_flyback_frames = metadata.get_n_flyback_frames()
    n_steps = metadata.get_n_z()
    frame_counter = utils2p.synchronization.process_frame_counter(frame_counter, steps_per_frame=n_flyback_frames + n_steps)

    co2_line = utils2p.synchronization.process_stimulus_line(co2_line)

    mask = np.logical_and(capture_on, frame_counter >= 0)
    mask = np.logical_and(mask, cam_line >= 0)

    co2_line, cam_line, opt_flow_line, frame_counter = utils2p.synchronization.crop_lines(mask, [co2_line, cam_line, opt_flow_line, frame_counter])

    optical_flow_path = utils2p.find_optical_flow_file(dir_beh)
    optical_flow = utils2p.load_optical_flow(optical_flow_path, 0, 0, 0, 0)

    # Ensure all optical flow data was saved and remove frames with missing data
    mask = (opt_flow_line < len(optical_flow["time_stamps"]))
    co2_line, cam_line, opt_flow_line, frame_counter = utils2p.synchronization.crop_lines(mask, [co2_line, cam_line, opt_flow_line, frame_counter])

    return co2_line, cam_line, opt_flow_line, frame_counter


def optical_flow_regressors(frame_counter, opt_flow_line, optical_flow):
    pitch = utils2p.synchronization.reduce_during_2p_frame(frame_counter, optical_flow["vel_pitch"][opt_flow_line], np.mean)
    roll = utils2p.synchronization.reduce_during_2p_frame(frame_counter, optical_flow["vel_roll"][opt_flow_line], np.mean)
    yaw = utils2p.synchronization.reduce_during_2p_frame(frame_counter, optical_flow["vel_yaw"][opt_flow_line], np.mean)
    return pitch, roll, yaw


def add_rest_metric(df, columns, name):
    n = flydf.number_of_epochs(df)
    rest_metric_df = pd.DataFrame()
    for epoch_df in tqdm(flydf.split_into_epoch_dfs(df), total=n):
        pre_rest_metric = []
        post_rest_metric = []
        kernel = np.array([-49 / 20, 6, -15 / 2, 20 / 3, -15 / 4, 6 / 5, -1 / 6])
        inversion_factor = -1
        # Second derivative accuracy 7
        kernel = np.array([469/90, -223/10, 879/20, -949/18, 41, -201/10, 1019/180, -7/10])
        inversion_factor = 1
        for col in columns:
            pre_rest_metric_col = np.abs(np.convolve(epoch_df[col].values, kernel[::-1] * inversion_factor, mode="valid"))
            post_rest_metric_col = np.abs(np.convolve(epoch_df[col].values, kernel, mode="valid"))
            pre_rest_metric.append(pre_rest_metric_col)
            post_rest_metric.append(post_rest_metric_col)
        pre_rest_metric = np.max(np.array(pre_rest_metric), axis=0)
        post_rest_metric = np.max(np.array(post_rest_metric), axis=0)

        rest_metric = np.zeros(epoch_df.shape[0])
        len_kern = len(kernel)
        rest_metric[:len_kern] = post_rest_metric_col[:len_kern]
        rest_metric[-(len_kern - 1):] = pre_rest_metric_col[-(len_kern - 1):]
        rest_metric[(len_kern - 1) : -(len_kern - 1)] = np.minimum(pre_rest_metric[:-(len_kern - 1)], post_rest_metric[(len_kern - 1):])

        epoch_indices = epoch_df.index
        rest_metric_df = rest_metric_df.append(pd.DataFrame(
            data=rest_metric,
            columns=[f"Rest metric {name}"],
            index=epoch_indices,
        ))
    #df = df.combine_first(rest_metric_df)
    df = df.join(rest_metric_df)
    return df


def add_wavelet(df, columns):
    n = flydf.number_of_epochs(df)
    coeff_df = pd.DataFrame()
    for epoch_df in tqdm(flydf.split_into_epoch_dfs(df), total=n):
        X = epoch_df[columns].values
        freqs, power, X_coeff = behavelet.wavelet_transform(X, n_freqs=15, fsample=30., fmin=1., fmax=15., gpu=True)
        epoch_indices = epoch_df.index
        coeff_columns = [f"Coeff {col} {freq}Hz" for col in columns for freq in freqs]
        coeff_df = coeff_df.append(pd.DataFrame(
            data=X_coeff,
            columns=coeff_columns,
            index=epoch_indices,
        ))
        coeff_df = coeff_df.apply(pd.to_numeric, downcast="float")
    #df = df.combine_first(coeff_df)
    df = df.join(coeff_df)
    return df


def get_frame_times(frame_counter, date, genotype, fly, trial):
    dir_sync = sync_dir(date, genotype, fly, trial)
    sync_metadata_file = utils2p.find_sync_metadata_file(dir_sync)
    sync_metadata = utils2p.synchronization.SyncMetadata(sync_metadata_file)
    freq = sync_metadata.get_freq()
    times = utils2p.synchronization.get_times(len(frame_counter), freq=freq)
    indices = utils2p.synchronization.edges(frame_counter, size=(0, np.inf))
    if frame_counter[0] == 0:
        with_start_frame = np.zeros(len(indices[0]) + 1, dtype=np.int)
        with_start_frame[1:] = indices[0]
        indices = (with_start_frame,)
    frame_times = times[indices]
    return frame_times


def co2_regressors(frame_counter, co2_line):
    co2_onset = utils2p.synchronization.reduce_during_2p_frame(frame_counter, co2_line, lambda x: np.max(np.diff(x)))
    co2 = utils2p.synchronization.reduce_during_2p_frame(frame_counter, co2_line, np.mean)
    return co2_onset, co2


def get_PER_regressors(frame_counter, cam_line, date, genotype, fly, trial):

    date=str(date)
    fly='fly'+str(fly)
    trial=f"{trial:03d}"
    Gal4=genotype.split('-')[0]
    # pickle_file = os.path.join(clc_output_dir(date, genotype, fly, trial), "PER/camera_6/PER_labels_camera_6.p")
    pickle_file = root_dir+"Ascending_neuron_screen_analysis_pipeline/00_behavior_data_preprocess/PE_regressors/"+Gal4+'/2P/'+date+'/'+genotype+'-'+fly+'/'+genotype+'-'+fly+'-'+trial+"/output/PER/camera_6/PER_labels_camera_6.p"


    with open(pickle_file, "rb") as f:
        PER = pickle.load(f)
    event = np.array(PER["evt_bin_trace"])
    length = np.array(PER["med_PER_exten_len"])

    event_regressor = utils2p.synchronization.reduce_during_2p_frame(frame_counter, event[cam_line], np.mean)
    length_regressor = utils2p.synchronization.reduce_during_2p_frame(frame_counter, length[cam_line], np.mean)
    return event_regressor, length_regressor


def get_rois(date, genotype, fly, trial):
    traces_dir = os.path.join(clc_output_dir(date, genotype, fly, trial), "GC6_auto/final/")
    dff_file = os.path.join(traces_dir, "DFF_dic.p")
    with open(dff_file, "rb") as f:
        dff = pickle.load(f)
    return sorted(list(dff.keys()))


def get_trace(date, genotype, fly, trial, roi, processing):
    traces_dir = os.path.join(clc_output_dir(date, genotype, fly, trial), "GC6_auto/final/")

    if processing == "raw":
        dff_file = os.path.join(traces_dir, "DFF_dic.p")
    elif processing == "denoised":
        dff_file = os.path.join(traces_dir, "DFF_dic_denoised.p")
    elif processing == "deconvolved":
        dff_file = os.path.join(traces_dir, "DFF_dic_deconvolved.p")
    elif processing == "absolute":
        dff_file = os.path.join(traces_dir, "GC_abs_dic.p")
    else:
        raise ValueError("processing can only be 'raw', 'denoised' or 'deconvolved'.")
    
    with open(dff_file, "rb") as f:
        dff_all_rois = pickle.load(f)

    dff = np.array(dff_all_rois[roi])

    dff = interpolate_for_nans(dff)

    return dff


def interpolate_for_nans(traces):
    """
    This function linearly interpolates nan values in the traces.

    Parameters
    ----------
    traces : numpy array
        Trace of values that contain nans.
        Second dimension is time. If 1D, first
        dimension is time.
    """
    if traces.ndim > 2 or traces.ndim == 0:
        raise ValueError("Parameter 'traces' must be a 1D or 2D numpy array.")
    if traces.ndim == 1:
        traces = np.expand_dims(traces, axis=0)

    mask_nan = np.isnan(traces)
    x = np.arange(traces.shape[1])
    for i in range(traces.shape[0]):
        if np.sum(mask_nan[i]) == 0 or np.sum(~mask_nan[i]) == 0:
            continue
        interp_locations = x[mask_nan[i]]
        value_locations = x[~mask_nan[i]]
        values = traces[i, ~mask_nan[i]]
        traces[i, mask_nan[i]] = np.interp(interp_locations, value_locations, values)
    return np.squeeze(traces)


def epoch_length_filter(regressor, cut_off):
    diff = np.diff(np.pad(regressor.astype(int), 1, "constant", constant_values=0))
    rising_edges = np.where(diff > 0)[0]
    falling_edges = np.where(diff < 0)[0]
    epoch_length = falling_edges - rising_edges
    
    discarded_epochs = (epoch_length < cut_off)
    
    discarded_rising_edges = rising_edges[discarded_epochs]
    discarded_falling_edges = falling_edges[discarded_epochs]

    filtered = regressor.copy()
    for start, stop in zip(discarded_rising_edges, discarded_falling_edges):
        filtered[start:stop] = 0
    
    return filtered


def hysteresis_filter(seq, n=5, n_false=None):
    """
    This function implements a hysteresis filter for boolean sequences.
    The state in the sequence only changes if n consecutive element are in a different state.

    Parameters
    ----------
    seq : 1D np.array of type boolean
        Sequence to be filtered.
    n : int, default=5
        Length of hysteresis memory.
    n_false : int, optional, default=None
        Length of hystresis memory applied for the false state.
        This means the state is going to change to false when it encounters
        n_false consecutive entries with value false.
        If None, the same value is used for true and false.

    Returns
    -------
    seq : 1D np.array of type boolean
        Filtered sequence.
    """
    if n_false is None:
        n_false = n
    seq = seq.astype(np.bool)
    state = seq[0]
    start_of_state = 0
    memory = 0

    current_n = n
    if state:
        current_n = n_false

    for i in range(len(seq)):
        if state != seq[i]:
            memory += 1
        elif memory < current_n:
            memory = 0
            continue
        if memory == current_n:
            seq[start_of_state : i - current_n + 1] = state
            start_of_state = i - current_n + 1
            state = not state
            if state:
                current_n = n_false
            else:
                current_n = n
            memory = 0
    seq[start_of_state:] = state
    return seq
