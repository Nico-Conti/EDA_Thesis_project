import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data = pd.read_csv('C:\\Users\\HP\\OneDrive\\Desktop\\Visual studio\\Python Workspace ecg\\csv_folder\\peak_MCU_vs_Neuro.csv', header=None)

# BIOZ_PHASIC
biozphasic_conductance_values = [value.split(':')[1] for value in data.values[0] if 'BIOZ_PHASIC:' in value]
biozphasic_conductance_signal = np.array([float(value) for value in biozphasic_conductance_values])

# BIOZ_PEAK
biozpeak_conductance_values = [value.split(':')[1] for value in data.values[0] if 'BIOZ_PEAK:' in value]
biozpeak_conductance_signal = np.array([float(value) for value in biozpeak_conductance_values])

# BIOZ_ONSET
biozonset_conductance_values = [value.split(':')[1] for value in data.values[0] if 'BIOZ_ONSET:' in value]
biozonset_conductance_signal = np.array([float(value) for value in biozonset_conductance_values])

# BIOZ_SCR_risetime
biozrisetime_conductance_values = [value.split(':')[1] for value in data.values[0] if 'BIOZ_SCR_RISE_TIME:' in value]
biozrisetime_conductance_signal = np.array([float(value) for value in biozrisetime_conductance_values])

for signal in biozrisetime_conductance_signal:
    if signal != 0:
        print(signal)

sampling_rate = 32  # Samples per second
total_samples = len(biozphasic_conductance_signal)
time_axis = np.arange(total_samples) / sampling_rate

peak_mask = biozpeak_conductance_signal != 0
peak_mask_shifted = np.zeros_like(peak_mask, dtype=bool)
if peak_mask[0] == True:
    peak_mask[0] = False
peak_mask_shifted[:-1] = peak_mask[1:]

onset_mask = biozonset_conductance_signal != 0
onset_mask_shifted = np.zeros_like(onset_mask, dtype=bool)
if onset_mask[0] == True:
    onset_mask[0] = False
onset_mask_shifted[:-1] = onset_mask[1:]

# Initialize a shifted onset mask
shifted_onset_mask = np.zeros_like(onset_mask, dtype=bool)

# Loop through each index of biozrisetime_conductance_signal
for i, shift_value in enumerate(biozrisetime_conductance_signal.astype(float)):
    # Shift the onset at index i by shift_value * 32 to the left
    shifted_index = max(i - int(shift_value), 0)
    shifted_onset_mask[shifted_index] = onset_mask[i]

print(shifted_onset_mask)


print("Length of time_axis:", len(time_axis))
print("Length of biozpeak_conductance_signal:", len(biozpeak_conductance_signal))
print("Length of peak_mask_shifted:", len(peak_mask_shifted))

# Plotting SCR

plt.plot(time_axis, biozphasic_conductance_signal, label='SCR', color='orange')
plt.plot(time_axis[peak_mask_shifted], biozpeak_conductance_signal[peak_mask], linestyle='', marker='o', color='red', label='Peaks')
plt.plot(time_axis[shifted_onset_mask], biozonset_conductance_signal[onset_mask], linestyle='', marker='o', color='blue', label='Onsets')

plt.title('Phasic component SCR')
plt.xlabel('Time (seconds)')
plt.legend()
plt.grid(True)
plt.show()

bsignals, binfo = nk.eda_peaks(biozphasic_conductance_signal, sampling_rate=32, method='neurokit', amplitude_min=0.25)

peaks_indices = np.where(bsignals.SCR_Peaks == 1)[0]  # Get the indices where peaks occur
onsets_indices = np.where(bsignals.SCR_Onsets == 1)[0]  # Get the indices where peaks occur

plt.plot(time_axis, biozphasic_conductance_signal, label='SCR', color='orange')
plt.plot(time_axis[peaks_indices], biozphasic_conductance_signal[peaks_indices], linestyle='', marker='o', color='red', label='Peaks')
plt.plot(time_axis[onsets_indices], biozphasic_conductance_signal[onsets_indices], linestyle='', marker='o', color='blue', label='Peaks')
plt.legend()
plt.grid(True)
plt.show()





