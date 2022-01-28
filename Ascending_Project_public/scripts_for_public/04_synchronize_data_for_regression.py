import os.path

import pandas as pd
import numpy as np

import utils2p
import flydf

import utils_Florian as utils



if not os.path.isdir(utils.output_dir):
    raise RuntimeError(f"Output directory {utils.output_dir} does not exist. It is specified in utils.py and created by 00_trials_for_paper.py.")

trials_for_paper = pd.read_pickle(os.path.join(utils.output_dir, "trials_for_paper.pkl"))
beh_df = pd.read_pickle(os.path.join(utils.output_dir, "df_behaviour_prediction.pkl"))

print('trials_for_paper', trials_for_paper)
# trials_for_paper=trials_for_paper[(trials_for_paper['Genotype']=='SS25451-tdTomGC6fopt')]
# print('trials_for_paper', trials_for_paper)


skip_existing = False
update = False
files_without_PER = ""

gain_0_x = round(1 / 1.45, 2)
gain_0_y = round(1 / 1.41, 2)
gain_1_x = round(1 / 1.40, 2)
gain_1_y = round(1 / 1.36, 2)

error_stream = ""

os.makedirs(os.path.join(utils.output_dir, "glm_input_files"), exist_ok=True)


for genotype_df in flydf.split_into_genotype_dfs(trials_for_paper):


    genotype = genotype_df["Genotype"].iloc[0]

    # remove the UAS tdtTomGC6fopt part
    genotype = genotype.split("-")[0]
    output_file = os.path.join(utils.output_dir, f"glm_input_files/{genotype}.csv")

    if skip_existing and os.path.isfile(output_file):
        print("skipped because file exists")
        continue
    if update:
        total_df = pd.read_csv(output_file)
    else:
        total_df = pd.DataFrame()

    for index, row in genotype_df.iterrows():
        date = row["Date"]
        genotype = row["Genotype"]
        fly = row["Fly"]
        trial = row["Trial"]
        exp = (date, genotype, fly, trial)
        print(exp)

        # sys.exit(0)

        if update:
            sub_df = total_df[((total_df["Date"] == date) & 
                               (total_df["Genotype"] == genotype) &
                               (total_df["Fly"] == fly) &
                               (total_df["Trial"] == trial)
                              )]
            if sub_df.shape[0] > 0:
                continue

        try:
            co2_line, cam_line, opt_flow_line, frame_counter = utils.get_processed_sync_lines(*exp)

            frames_with_behaviour_images = np.arange(np.min(frame_counter), np.max(frame_counter) + 1)

            length = np.max(cam_line) + 1

            experiment_df = pd.DataFrame()

            dir_beh = utils.beh_dir(*exp)

            frame_times = utils.get_frame_times(cam_line, *exp)
            frame_times_2p = utils.get_frame_times(frame_counter, *exp)

            co2_onset, co2 = utils.co2_regressors(cam_line, co2_line)

            trial_df = flydf.get_trial_df(beh_df, genotype, date, fly, trial).copy()
            behaviour_column = trial_df["Behaviour"].values

            behaviour_regressor_names = []
            behaviour_regressors = []
            for beh in np.unique(behaviour_column):
                if beh == "":
                    continue
                regressor = (behaviour_column == beh)
                behaviour_regressors.append(regressor)
                behaviour_regressor_names.append(beh)

            angle_regressor_names = []
            angle_regressors = []
            for angle_col in utils.angle_columns:
                angle_values = trial_df[angle_col].values
                angle_regressor_names.append("Angle " + angle_col)
                angle_regressors.append(angle_values)

            try:
                PER_event_regressor, PER_length_regressor = utils.get_PER_regressors(cam_line, cam_line, *exp)
            except FileNotFoundError:
                files_without_PER += str(exp) + "\n"
                PER_event_regressor, PER_length_regressor = 0, 0

            for roi_idx, roi in enumerate(utils.get_rois(*exp)):
                    
                for processing in ["raw", ]:
                        df = pd.DataFrame()

                        df["Genotype"]              = [genotype,    ] * length
                        df["Fly"]                   = [fly,         ] * length
                        df["Trial"]                 = [trial,       ] * length
                        df["Date"]                  = [date,        ] * length
                        df["ROI"]                   = [roi_idx,     ] * length
                        df["dFF_processing"]        = [processing,  ] * length
                        df["Regressor_processing"]  = ["raw",       ] * length
                        df["Frame_times"] = frame_times
                        df["Behaviour"] = behaviour_column
                        
                        trace = utils.get_trace(*exp, roi=roi, processing=processing)
                        df["dFF"] = np.interp(frame_times, frame_times_2p, trace[frames_with_behaviour_images])

                        df["CO2_onset"] = co2_onset
                        df["CO2"] = co2

                        df["Pitch"] = trial_df["Pitch"].values
                        df["Roll"] = trial_df["Roll"].values
                        df["Yaw"] = trial_df["Yaw"].values

                        for name, regressor in zip(behaviour_regressor_names, behaviour_regressors):
                            df[name] = regressor

                        for name, regressor in zip(angle_regressor_names, angle_regressors):
                            df[name] = regressor

                        df["PER_event"] = PER_event_regressor
                        df["PER_length"] = PER_length_regressor

                        # Skip first frame to remove faulty optical flow values
                        df = df[8:]

                        experiment_df = experiment_df.append(df, ignore_index=True)
            total_df = total_df.append(experiment_df, ignore_index=True)
        except Exception as err:
            error_stream += f"{exp[0]} {exp[1]} {exp[2]} {exp[3]} \n"
            error_stream += f"{err}"
            error_stream += "\n\n\n"
            print(err)
            raise(err)

    if len(total_df) > 0:
        total_df.to_csv(output_file)

with open(os.path.join(utils.output_dir, "error_stream.txt"), "w") as f:
    f.write(error_stream)

with open(os.path.join(utils.output_dir, "files_without_PER.txt"), "w") as f:
    f.write(files_without_PER)
