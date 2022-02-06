import os
import pandas as pd
from flydf.core import _fix_dtypes
import utils_Florian

import utils.list_twoP_exp as list_twoP_exp
l = list_twoP_exp.df3d_processed_list



df = pd.DataFrame(data=l, columns=["Date", "Genotype", "Fly", "Trial"])
df["Date"] = df["Date"].apply(lambda x: int(x))
df["Fly"] = df["Fly"].apply(lambda x: int(x[3:]))
df["Trial"] = df["Trial"].apply(lambda x: int(x))
for col in df.columns:
    df[col] = df[col].astype("category")

os.makedirs(utils_Florian.output_dir, exist_ok=True)
output_file = os.path.join(utils_Florian.output_dir, "trials_for_paper.pkl")
df.to_pickle(output_file)
