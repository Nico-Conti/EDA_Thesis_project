import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
import os

# file_path = os.path.join('txt', 'serial.txt')
data = np.fromfile('finger_person_4_E.txt', dtype="int32").reshape(-1, 2)
# print(data.shape)
# print(data)


# Extracting columns from the data
column1 = data[:, 0]
column2 = data[:, 1]



# trigger_mask = (column2 == 1)
# trigger_change_indices = np.where(np.diff(trigger_mask.astype(int)) != 0)[0] + 1


sampling_rate = 32  # Samples per second
total_samples = len(column1)


# Conversion for the first column
v_ref = 1
bioz_conductance_signal = []
for sample in column1:
    bioz_conductance_signal.append(1 / ((sample * v_ref) / ((2 ** 19) * 10 * (110 * (10**-9)))))

bioz_conductance_signal = np.array(bioz_conductance_signal)
bioz_conductance_signal = (bioz_conductance_signal - bioz_conductance_signal.mean()) / bioz_conductance_signal.std()

bsignals, binfo = nk.eda_process(bioz_conductance_signal, 32, method="neurokit",method_phasic="cvxeda", amplitude_min=0.25)
# cleaned = nk.eda_clean(bioz_conductance_signal, 32, method="neurokit")
# bsignals = nk.eda_phasic(bioz_conductance_signal, 32, method="cvxeda")
# find_peaks, info_peaks = nk.eda_peaks(bsignals.EDA_Phasic, 32, method="neurokit")
# print(find_peaks)

# Calculate the features
mean_tonic = np.mean(bsignals.EDA_Tonic)
max_tonic = np.max(bsignals.EDA_Tonic)
max_phasic = np.max(bsignals.EDA_Phasic)
std_onsets = np.std(binfo["SCR_Onsets"])  # Standard deviation of SCR rise times
std_rise_time = np.std(binfo["SCR_RiseTime"])  # Standard deviation of SCR rise times
mean_rise_time = np.mean(binfo["SCR_RiseTime"])  # Standard deviation of SCR rise times
num_peaks = np.sum(bsignals.SCR_Peaks)  # Number of SCR peaks

print(bsignals.SCR_RiseTime)
print(np.std(bsignals.SCR_RiseTime))
# print("Mean of Tonic (SCL):", mean_tonic)
# print("Max of Tonic (SCL):", max_tonic)
# print("Max of Phasic (SCR) Peaks:", max_phasic)
# print("Standard Deviation of Phasic (SCR) onsets:", std_onsets)
# print("Standard Deviation of Phasic (SCR) Rise Time:", std_rise_time)
# print("Mean of Phasic (SCR) Rise Time:", mean_rise_time)
# print("Number of Peaks in Phasic (SCR):", num_peaks)
#Time axis
time_axis = np.arange(total_samples) / sampling_rate
# print(total_samples)
# print(time_axis)


fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6))

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

# Plotting Trigger
ax3.plot(time_axis, column2, label='Trigger mask', color='green')
ax3.set_title('Trigger')
ax3.set_xlabel('Time (seconds)')
ax3.legend()
ax3.grid(True)

def on_xlims_change(ax):
    xlim = ax.get_xlim()
    ax3.set_xlim(xlim)
    ax1.set_xlim(xlim)

# Connecting the zoom event to the function
ax2.callbacks.connect('xlim_changed', on_xlims_change)

plt.tight_layout()
plt.show()

