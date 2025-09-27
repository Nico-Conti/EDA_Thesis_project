from biosppy.signals import ecg
from biosppy.plotting import plot_ecg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data = pd.read_csv('dati.csv', header=None)

ecg_values = [value.split(':')[1] for value in data.values[0] if 'ECG:' in value]
ecg_signal = [int(value) for value in ecg_values]

rtor_values = [value.split(':')[1] for value in data.values[0] if 'RTOR:'in value]
rtor_signal = [float(value) for value in rtor_values]

sampling_rate = 128  # Sa/s
time_values = [i / sampling_rate for i in range(len(ecg_signal))]

out = ecg.ecg(ecg_signal, sampling_rate, show=False)


# Using biosppy.plotting.plot_ecg to generate the plot
plot_ecg(ts=out["ts"], raw=ecg_signal, filtered=out["filtered"], rpeaks=out["rpeaks"], show=True, heart_rate_ts=out["heart_rate_ts"], heart_rate=out["heart_rate"], templates_ts=out["templates_ts"], templates= out["templates"])


