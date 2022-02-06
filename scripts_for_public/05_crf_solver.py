import os.path

from scipy.optimize import fsolve
import math
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

import utils_Florian as utils



def equations(p, t_peak, t_half):
    x, y = p
    return (0.5 * (math.exp(-x * t_peak) - math.exp(-y * t_peak)) - (math.exp(-x * t_half) - math.exp(-y * t_half)), -x * math.exp(-x * t_peak) + y * math.exp(-y * t_peak))


results = pd.DataFrame()

t_peaks = []
t_halfs = []
xs = []
ys = []
initial_conditions = ((12, 5),
                      (14, 4),
                      (14, 4),
                      (30, 1),
                      (30, 1),
                      (30, 1),
                      (30, 1),
                      (30, 1),
                      (30, 1),
                      (30, 1),
                      (30, 1),
                      (30, 1),
                      (30, 1),
                      (30, 1),
                      (30, 1),
                      (30, 1))
for alpha in range(1, 16):
    t_peak = 0.1415
    t_half = t_peak + 0.2 + alpha * 0.05
    print("Target: ", t_half)
    x, y =  fsolve(equations, initial_conditions[alpha], args=(t_peak, t_half))

    t_peaks.append(t_peak)
    t_halfs.append(t_half - t_peak)
    xs.append(x)
    ys.append(y)
    
    t = np.linspace(0, 2.0, 10000)
    crf = -np.exp(-x * t) + np.exp(-y * t)
    crf = crf / sum(crf)
    print("t peak", t[np.argmax(crf)])
    diff = crf - 0.5 * max(crf)
    diff[:np.argmax(crf)] = np.inf
    diff = np.abs(diff)
    half_idx = np.argmin(diff)
    print("t half", t[half_idx] - t[np.argmax(crf)])
    plt.plot(t, crf, label=str(t_half - t_peak))
    results = results.append(pd.DataFrame({"t_peak": [t_peak], "t_half": [t_half - t_peak], "a": [x], "b": [y]}))

results.to_csv(os.path.join(utils.output_dir, "crf_parameters.csv"))
