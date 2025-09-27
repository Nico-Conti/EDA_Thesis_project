import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
import os

# file_path = os.path.join('txt', 'serial.txt')
data = np.fromfile('MCU_test.txt', dtype="float32").reshape(-1, 1)

# Extracting columns from the data
column1 = data[:, 0]


sampling_rate = 32  # Samples per second
total_samples = len(column1)


# Conversion for the first column
v_ref = 1
bioz_conductance_signal = []
for sample in column1:
    bioz_conductance_signal.append(sample)

bioz_conductance_signal = np.array(bioz_conductance_signal)
# bioz_conductance_signal = (bioz_conductance_signal - bioz_conductance_signal.mean()) / bioz_conductance_signal.std()

bsignals, binfo = nk.eda_process(bioz_conductance_signal, 32, method="neurokit",method_phasic="highpass", amplitude_min=0.25)


time_axis = np.arange(total_samples) / sampling_rate
print(total_samples)
print(time_axis)


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

# Plotting SCL
ax1.plot(time_axis, bsignals.EDA_Tonic, label='SCL', color='blue')
ax1.set_title('Tonic component SCL')
ax1.set_xlabel('Time (seconds)')
# ax1.set_ylabel('Siemens')
ax1.legend()
ax1.grid(True)

peaks_indices = np.where(bsignals.SCR_Peaks == 1)[0]  # Get the indices where peaks occur
onsets_indices = np.where(bsignals.SCR_Onsets == 1)[0]  # Get the indices where peaks occur
# Plotting SCR
ax2.plot(time_axis, bsignals.EDA_Phasic, label='SCR', color='orange')
ax2.plot(time_axis[peaks_indices], bsignals.EDA_Phasic[peaks_indices], linestyle='', marker='o', color='red', label='Peaks')
ax2.plot(time_axis[onsets_indices], bsignals.EDA_Phasic[onsets_indices], linestyle='', marker='o', color='blue', label='Peaks')
# for i in range(0, len(trigger_change_indices), 2):
#     start_idx = trigger_change_indices[i]
#     end_idx = trigger_change_indices[i + 1] if i + 1 < len(trigger_change_indices) else len(column2)

#     if trigger_mask[start_idx] == 1:
#         ax2.plot(time_axis[start_idx:end_idx], bsignals.EDA_Phasic[start_idx:end_idx], linewidth=2, color='green')
ax2.set_title('Phasic component SCR')
ax2.set_xlabel('Time (seconds)')
# ax2.set_ylabel('Siemens')
ax2.legend()
ax2.grid(True)


def on_xlims_change(ax):
    xlim = ax.get_xlim()
    ax1.set_xlim(xlim)

# Connecting the zoom event to the function
ax2.callbacks.connect('xlim_changed', on_xlims_change)

signals, info = nk.eda_process(bioz_conductance_signal, 32, amplitude_min = 0.25)
nk.eda_plot(signals, info)

plt.tight_layout()
plt.show()

