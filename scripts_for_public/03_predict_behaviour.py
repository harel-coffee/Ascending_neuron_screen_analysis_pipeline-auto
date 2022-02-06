import os
import pickle

import pandas as pd
import numpy as np

import flydf
import utils_Florian as utils



if not os.path.isdir(utils.output_dir):
    raise RuntimeError(f"Output directory {utils.output_dir} does not exist. It is specified in utils.py and created by 00_trials_for_paper.py.")

df = pd.read_pickle(os.path.join(utils.output_dir, "df_behaviour_classification_features.pkl"))


with open(os.path.join(utils.output_dir, "behaviour_classifier.pkl"), "rb") as f:
    clf = pickle.load(f)
with open(os.path.join(utils.output_dir, "label_encoder.pkl"), "rb") as f:
    le = pickle.load(f)
with open(os.path.join(utils.output_dir, "entropy_threshold.txt"), "r") as f:
    entropy_threshold = float(f.read())

wavelet_column_names = [col for col in df.columns if "Coeff" in col]
feature_columns = ["Rest metric front", "Rest metric mid", "Rest metric hind", "Pitch", "Roll", "Yaw"] + wavelet_column_names + utils.angle_columns

X_all = df[feature_columns].values
y_pred = clf.predict(X_all)
proba = clf.predict_proba(X_all)
logproba = np.log(proba)
logproba[np.where(proba == 0)] = 0
entropy = np.sum(-proba * logproba, axis=1)
prediction = le.inverse_transform(y_pred)
df["Raw_behaviour"] = prediction
df["Entropy"] = entropy
df = df[["Date", "Genotype", "Fly", "Trial", "Frame", "Raw_behaviour", "Entropy", "Pitch", "Roll", "Yaw"] + utils.angle_columns]

df["Entropy_thresh_behaviour"] = df["Raw_behaviour"]
entropy_mask = (df["Entropy"] > entropy_threshold).values
df["Filtered_behaviour"] = ""

for i, trial_mask in enumerate(flydf.get_trial_masks(df)):
    print(i)
    filtered_entropy_mask = utils.epoch_length_filter(entropy_mask, 10)
    df.loc[filtered_entropy_mask, "Entropy_thresh_behaviour"] = ""
    trial_df = df.loc[trial_mask, :]
    filtered_behaviours = np.full(trial_df.shape[0], "", dtype=np.object)
    for beh in trial_df["Entropy_thresh_behaviour"].unique():
        if beh == "":
            continue
        regressor = (trial_df["Entropy_thresh_behaviour"] == beh).values
        regressor = utils.epoch_length_filter(regressor, 18)
        filtered_behaviours[regressor] = beh
    df.loc[trial_mask, "Filtered_behaviour"] = filtered_behaviours

thresh_pitch = 0.0038
thresh_roll = 0.0038
thresh_yaw = 0.014

df["ball_moving"] = ( (np.absolute(df["Pitch"].values) > thresh_pitch)
                    | (np.absolute(df["Roll" ].values) > thresh_roll)
                    | (np.absolute(df["Yaw"  ].values) > thresh_yaw))

print('df["ball_moving"]', df["ball_moving"])


non_walk_rest_beh = ~df["Filtered_behaviour"].isin(["abdominal_grooming", "antennal_grooming", "hindleg_grooming", "foreleg_grooming", "eye_grooming", "pushing"])


print('non_walk_rest_beh', non_walk_rest_beh)




df["backward_walking"] = ( (df["Pitch"].values < -1.5*thresh_pitch) & df["ball_moving"])
print('df["backward_walking"]', df["backward_walking"])

df["forward_walking"] = ( (df["Pitch"].values > thresh_pitch) & df["ball_moving"])
print('df["forward_walking"]', df["forward_walking"])



rest = utils.hysteresis_filter((~df["ball_moving"] & non_walk_rest_beh).values, n=15)
walking = utils.hysteresis_filter((df["ball_moving"] & non_walk_rest_beh).values, n=15)
forward_walking = utils.hysteresis_filter((df["forward_walking"] & non_walk_rest_beh).values, n=15)
backward_walking = utils.hysteresis_filter((df["backward_walking"] & non_walk_rest_beh).values, n=15)


# print('walking', walking)
# print('forward_walking', forward_walking)
# print('backward_walking', backward_walking)

df["Behaviour"] = df["Filtered_behaviour"]
df.loc[rest, "Behaviour"] = "rest"
df.loc[walking, "Behaviour"] = "walking"
df.loc[forward_walking, "Behaviour"] = "forward_walking"
df.loc[backward_walking, "Behaviour"] = "backward_walking"

# print(df)
# print(list(df))

# options = ['MAN-tdTomGC6fopt']
# col_list=["Genotype", "rest", "forward_walking", "backward_walking", "antennal_grooming", "eye_grooming", "foreleg_grooming", "hindleg_grooming", "abdominal_grooming", "PER_event", "pushing", "CO2"]
# col_list=["Genotype", "rest"]

# dataframe_Gal4 = df[col_list]
# dataframe_Gal4 = dataframe_Gal4[dataframe_Gal4['Genotype'] == 'MAN-tdTomGC6fopt']
# print(dataframe_Gal4)

df.to_pickle(os.path.join(utils.output_dir, "df_behaviour_prediction.pkl"))

print(df)










