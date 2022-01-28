import os.path
import pickle

import numpy as np
from sklearn.experimental import enable_hist_gradient_boosting
import sklearn.preprocessing
import sklearn.model_selection
import sklearn.ensemble
import pandas as pd
import imblearn.over_sampling

import flydf
from flydf.core import _fix_dtypes

import utils_Florian as utils


if not os.path.isdir(utils.output_dir):
    raise RuntimeError(f"Output directory {utils.output_dir} does not exist. It is specified in utils.py and created by 00_trials_for_paper.py.")

df = pd.read_pickle(os.path.join(utils.output_dir, "df_joint_pos_joint_angles_opt_flow.pkl"))
for pos_col in utils.position_columns:
    del df[pos_col]

df = _fix_dtypes(df)
df[utils.angle_columns] = df[utils.angle_columns].apply(pd.to_numeric, downcast='float')

print("Computing wavelet coefficients")
df = utils.add_wavelet(df, utils.angle_columns)
wavelet_column_names = [col for col in df.columns if "Coeff" in col]
df[wavelet_column_names] = df[wavelet_column_names].apply(pd.to_numeric, downcast='float')

front_angle_columns = [col for col in utils.angle_columns if "F" in col]
hind_angle_columns = [col for col in utils.angle_columns if "H" in col]
mid_angle_columns = [col for col in utils.angle_columns if "M" in col]

print("Computing custom metrics")
print("Front")
df = utils.add_rest_metric(df, front_angle_columns, "front")
print("Hind")
df = utils.add_rest_metric(df, hind_angle_columns, "hind")
print("Mid")
df = utils.add_rest_metric(df, mid_angle_columns, "mid")
cols = ["Rest metric front", "Rest metric mid", "Rest metric hind", ]
df[cols] = df[cols].apply(pd.to_numeric, downcast='float')


df.to_pickle(os.path.join(utils.output_dir, "df_behaviour_classification_features.pkl"))
df = pd.read_pickle(os.path.join(utils.output_dir, "df_behaviour_classification_features.pkl"))
df = _fix_dtypes(df)

annotations_df = pd.read_csv(os.path.join(utils.annotation_dir, "behaviour_annotations.csv"), index_col=0)
annotations_df = _fix_dtypes(annotations_df)

trials_with_annotations = annotations_df[["Date", "Genotype", "Fly", "Trial"]].drop_duplicates()
df = df.merge(trials_with_annotations, how="inner", on=["Date", "Genotype", "Fly", "Trial"], validate="many_to_one")

# Add annotations
df = pd.merge(
   df,
   annotations_df,
   on=["Genotype", "Date", "Fly", "Trial", "Frame"],
   how="outer",
)
df["Annotation"] = df["Annotation"].replace(["undefined",], np.nan)
df["Annotation"] = df["Annotation"].astype("category")

# Some annotated data is not present in all_ascending_behaviour_data_no_rescale.pkl
df = df.dropna(axis="index", how="any", subset=utils.angle_columns)
df = df[pd.notnull(df["Annotation"])]

wavelet_column_names = [col for col in df.columns if "Coeff" in col]

feature_columns = ["Rest metric front", "Rest metric mid", "Rest metric hind", "Pitch", "Roll", "Yaw"] + wavelet_column_names + utils.angle_columns

annotated_df = df.dropna(subset=["Annotation",], axis="index")
X = annotated_df[feature_columns].values
annotations = annotated_df["Annotation"].values
le = sklearn.preprocessing.LabelEncoder()
le.fit(annotations)
y = le.transform(annotations)
smote = imblearn.over_sampling.SMOTE()
# X_smote, y_smote= smote.fit_sample(X, y)
X_smote, y_smote= smote.fit_resample(X, y)
clf = sklearn.ensemble.HistGradientBoostingClassifier()
clf = clf.fit(X_smote, y_smote)
with open(os.path.join(utils.output_dir, "behaviour_classifier.pkl"), "wb") as f:
    pickle.dump(clf, f)
with open(os.path.join(utils.output_dir, "label_encoder.pkl"), "wb") as f:
    pickle.dump(le, f)


##################
# Cross-validation
##################

print("Cross-validation for model evaluation")

annotated_df = flydf.add_epoch_column(annotated_df, extra_column="Annotation")
epoch_indices = annotated_df["Epoch index"].unique()
epoch_annotations = []
for epoch_index in epoch_indices:
    annotations = annotated_df.loc[annotated_df["Epoch index"] == epoch_index, "Annotation"]
    annotation = annotations.unique()
    assert annotation.shape[0] == 1
    annotation = annotation[0]
    epoch_annotations.append(annotation)

cv_results = pd.DataFrame()

rskf = sklearn.model_selection.RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=0)
for i, (train_epoch_indices, test_epoch_indices) in enumerate(rskf.split(epoch_indices, epoch_annotations)):
    print(f"Fold {i + 1}/30")
    X_train = X[annotated_df["Epoch index"].isin(train_epoch_indices)]
    X_test = X[annotated_df["Epoch index"].isin(test_epoch_indices)]
    y_train = y[annotated_df["Epoch index"].isin(train_epoch_indices)]
    y_test = y[annotated_df["Epoch index"].isin(test_epoch_indices)]
    smote = imblearn.over_sampling.SMOTE()
    # X_train, y_train = smote.fit_sample(X_train, y_train)
    X_train, y_train = smote.fit_resample(X_train, y_train)
    clf = sklearn.ensemble.HistGradientBoostingClassifier()
    clf = clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    proba = clf.predict_proba(X_test)
    logproba = np.log(proba)
    logproba[np.where(proba == 0)] = 0
    entropy = np.sum(-proba * logproba, axis=1)
    behaviours = le.inverse_transform(y_test)
    predictions = le.inverse_transform(y_pred)
    dates = annotated_df.loc[annotated_df["Epoch index"].isin(test_epoch_indices), "Date"]
    genotypes = annotated_df.loc[annotated_df["Epoch index"].isin(test_epoch_indices), "Genotype"]
    flies = annotated_df.loc[annotated_df["Epoch index"].isin(test_epoch_indices), "Fly"]
    trials = annotated_df.loc[annotated_df["Epoch index"].isin(test_epoch_indices), "Trial"]
    frames = annotated_df.loc[annotated_df["Epoch index"].isin(test_epoch_indices), "Frame"]
    current_test_fold_results = pd.DataFrame({"Date": dates, "Genotype": genotypes, "Fly": flies, "Trial": trials, "Frame": frames, "Behaviour": behaviours, "Prediction": predictions, "Entropy": entropy})
    cv_results = cv_results.append(current_test_fold_results, ignore_index=True)

entropy_threshold = cv_results.loc[cv_results["Behaviour"] == cv_results["Prediction"], "Entropy"].quantile(0.995)
print("Entropy threshold", entropy_threshold)
with open(os.path.join(utils.output_dir, "entropy_threshold.txt"), "w") as f:
    f.write(str(entropy_threshold))

cv_results.to_csv(os.path.join(utils.output_dir, "behaviour_classification_cv_results.csv"))
