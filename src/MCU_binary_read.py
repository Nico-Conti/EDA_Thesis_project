import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
import os

# file_path = os.path.join('txt', 'serial.txt')
data = np.fromfile('MCU_test.txt', dtype="float32").reshape(-1, 5)
# print(data.shape)

# print(data)


# Extracting columns from the data
bioz_conductance_signal = data[:, 0]
bioz_filtered_signal = data[:, 1]
bioz_tonic_signal = data[:, 2]
bioz_phasic_signal = data[:, 3]
bioz_peak_signal = data[:, 4]

sampling_rate = 32  # Samples per second
total_samples = len(bioz_conductance_signal)
print(len(bioz_conductance_signal))
print(len(bioz_peak_signal))



# bioz_conductance_signal = np.array(bioz_conductance_signal)
# bioz_conductance_signal = (bioz_conductance_signal - bioz_conductance_signal.mean()) / bioz_conductance_signal.std()

#Time axis
time_axis = np.arange(total_samples) / sampling_rate
peak_mask = bioz_peak_signal != 0
peak_mask_shifted = np.zeros_like(peak_mask, dtype=bool)
if peak_mask[0] == True:
    peak_mask[0] = False
peak_mask_shifted[:-1] = peak_mask[1:]
    
    
# print(peak_mask)

# print(bioz_peak_signal[peak_mask])
# print(total_samples)
# print(time_axis)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 5))  # Create subplots with 3 rows and 1 column

# Raw and cleaned subplot
ax1.plot(time_axis, bioz_conductance_signal, color='green', label='Raw')
ax1.plot(time_axis, bioz_filtered_signal, color='purple', label='Cleaned')
ax1.set_title('Raw and Cleaned Signals')
ax1.set_xlabel('Time')
ax1.set_ylabel('Conductance')
ax1.legend()
ax1.grid(True)

# Phasic subplot
ax2.plot(time_axis, bioz_phasic_signal, color='red')
ax2.plot(time_axis[peak_mask_shifted], bioz_peak_signal[peak_mask], marker='o',linestyle='',color='blue', )
ax2.set_title('Phasic Signal')
ax2.set_xlabel('Time')

ax2.set_ylabel('Conductance')
ax2.grid(True)

# Tonic subplot
ax3.plot(time_axis, bioz_tonic_signal, color='blue')
ax3.set_title('Tonic Signal')
ax3.set_xlabel('Time')
ax3.set_ylabel('Conductance')
ax3.grid(True)
plt.tight_layout(h_pad=0.01)  # Adjust layout for better vertical spacing
signals, info = nk.eda_process(bioz_conductance_signal, 32, amplitude_min = 0.25)
nk.eda_plot(signals, info)


plt.show()

