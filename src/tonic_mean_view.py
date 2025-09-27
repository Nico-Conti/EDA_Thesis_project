import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data = pd.read_csv('C:\\Users\\HP\\OneDrive\\Desktop\\Visual studio\\Python Workspace ecg\\csv_folder\\capture.csv', header=None)


bioztonic_conductance_values = [value.split(':')[1] for value in data.values[0] if 'BIOZ_TONIC:' in value]
bioztonic_conductance_signal = [float(value) for value in bioztonic_conductance_values]

bioztonicmean_conductance_values = [value.split(':')[1] for value in data.values[0] if 'BIOZ_TONIC_MEAN:' in value]
bioztonicmean_conductance_signal = [float(value) for value in bioztonicmean_conductance_values]


sampling_rate = 32  # Samples per second
total_samples = len(bioztonic_conductance_signal)
time_axis = np.arange(total_samples) / sampling_rate


# nk.ecg_plot(signals, info)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5))  # Create subplots with 3 rows and 1 column

# Raw and cleaned subplot
ax1.plot(time_axis, bioztonic_conductance_signal, color='green', label='Raw')
ax1.set_title('Tonic')
ax1.set_xlabel('Time')
ax1.set_ylabel('Conductance')
ax1.legend()
ax1.grid(True)

# Tonic subplot
ax2.plot(time_axis, bioztonicmean_conductance_signal, color='red')
ax2.set_title('Mean tonic')
ax2.set_xlabel('Time')
ax2.set_ylabel('Conductance')
ax2.grid(True)


plt.tight_layout()  # Adjust layout for better spacing
plt.show()




