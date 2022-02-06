import os
import pickle

import pandas as pd
import numpy as np
import sklearn.preprocessing
import matplotlib
import utils_Florian as utils
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "sans-serif"
from matplotlib import pyplot as plt
plt.switch_backend('agg')


def rename_behaviours(x):
    x = pd.Series(x)
    return x.replace({"abdominal_grooming": "Abdominal grooming",
                      "antennal_grooming": "Antennal grooming",
                      "eye_grooming": "Eye grooming",
                      "foreleg_grooming": "Front leg grooming",
                      "forward_walking": "Walking",
                      "hindleg_grooming": "Rear leg grooming",
                      "pushing": "Pushing",
                      "rest": "Resting"}).values


print(utils.output_dir)

plot_output=utils.root_dir+'Ascending_neuron_screen_analysis_pipeline/output/FigS10-confusionMat_beh_classifier/plots/'
if not os.path.exists(plot_output):
    os.makedirs(plot_output)

with open(os.path.join(utils.output_dir, "label_encoder.pkl"), "rb") as f:
    le = pickle.load(f)

df = pd.read_csv(os.path.join(utils.output_dir, "behaviour_classification_cv_results.csv"))

le = le.fit(df["Behaviour"])
n_classes = len(le.classes_)
confusion_matrix = np.zeros((n_classes, n_classes + 1))
absolute_numbers = np.zeros((n_classes, n_classes + 1), dtype=np.int)
for i in range(n_classes):
    target_behaviour = le.inverse_transform([i])[0]
    total = np.sum(df["Behaviour"] == target_behaviour)
    for j in range(n_classes):
        probe_behaviour = le.inverse_transform([j])[0]
        n = np.sum((df["Behaviour"] == target_behaviour) & (df["Prediction"] == probe_behaviour))
        confusion_matrix[i, j] = n / total * 100
        absolute_numbers[i, j] = int(n)
    n = np.sum((df["Behaviour"] == target_behaviour) & (df["Prediction"] == ""))
    confusion_matrix[i, -1] = n / total * 100
    absolute_numbers[i, -1] = int(n)
fig, ax = plt.subplots()
ax.matshow(confusion_matrix, cmap=plt.cm.Blues)
for i in range(n_classes):
    total = np.sum(absolute_numbers[i, :])
    for j in range(n_classes + 1):
        ax.text(j, i, f"{confusion_matrix[i, j]:.2f}%\n({absolute_numbers[i, j]}/{total})",
                va="center",
                ha="center",
                fontsize=3)
ax.set_ylabel("True behaviour")
ax.set_xlabel("Predicted behaviour")
tick_positions_y = np.arange(n_classes)
tick_positions_x = np.arange(n_classes + 1)
tick_labels_y = le.inverse_transform(tick_positions_y)
tick_labels_x = list(tick_labels_y.copy())
tick_labels_x.append("not classified")
ax.set_yticks(tick_positions_y)
ax.set_yticklabels(tick_labels_y, fontsize=4, rotation=45)
ax.set_xticks(tick_positions_x)
ax.set_xticklabels(tick_labels_x, fontsize=4, rotation=45,)
plt.savefig(os.path.join(plot_output, "confusion_matrix.pdf"))
plt.close()

