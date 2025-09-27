import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
import os

def process_trigger(file_path2):
    data = np.fromfile(file_path2, dtype="int32").reshape(-1, 2)
    trigger = data[:, 1]
    return trigger  # Modify to return necessary processed data

def process_data(file_path):
    data = np.fromfile(file_path, dtype="float32").reshape(-1, 5)
    bioz = data[:, 0]
    filtered = data[:, 1]
    tonic = data[:, 2]
    phasic = data[:, 3]
    peak = data[:, 4]
    
    sampling_rate = 32  
    total_samples = len(bioz)


    # Conversion for the first column
    v_ref = 1
    bioz_conductance_signal = []

    # for sample in column1:
    #     bioz_conductance_signal.append(sample)

    # bioz_conductance_signal = np.array(bioz_conductance_signal)
    # bioz_conductance_signal = (bioz_conductance_signal - bioz_conductance_signal.mean()) / bioz_conductance_signal.std()

    # bsignals, binfo = nk.eda_process(bioz_conductance_signal, 32, method="neurokit",method_phasic="highpass", amplitude_min=0.35)

    time_axis = np.arange(total_samples) / sampling_rate

    return bioz, filtered, tonic, phasic, peak, time_axis  # Modify to return necessary processed data



# List of file paths
position = 'MCU_finger'
file_paths = [
    position + '_person_1.txt',
    position + '_person_2_L.txt',
    position + '_person_3_P.txt',
    position + '_person_4_E.txt',
    position + '_person_5_T.txt'
]

# List of file paths for trigger
position2 = 'finger'
file_paths2 = [
    position2 + '_person_1.txt',
    position2 + '_person_2_L.txt',
    position2 + '_person_3_P.txt',
    position2 + '_person_4_E.txt',
    position2 + '_person_5_T.txt'
]

# Create lists to store processed data
all_bioz = []
all_filtered = []
all_tonic = []
all_phasic = []
all_peak = []
time_axes = []

all_trigger = []

# Process each file and store the processed data
for file_path in file_paths:
    bioz, filtered, tonic, phasic, peak, time = process_data(file_path)
    all_bioz.append(bioz)
    all_filtered.append(filtered)
    all_tonic.append(tonic)
    all_phasic.append(phasic)
    all_peak.append(peak)
    time_axes.append(time)

for file_path in file_paths2:
    trigger = process_trigger(file_path)
    all_trigger.append(trigger)

# Plotting
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6))

for i in range(len(file_paths)):
    time_axis = time_axes[i]
    bioz = all_bioz[i]
    filtered = all_filtered[i]
    tonic = all_tonic[i]
    phasic = all_phasic[i]
    peak = all_peak[i]
    trigger = all_trigger[i]

    peak_mask = peak != 0
    peak_mask_shifted = np.zeros_like(peak_mask, dtype=bool)
    if peak_mask[0] == True:
        peak_mask[0] = False
    peak_mask_shifted[:-1] = peak_mask[1:]

    # Plotting SCL
    ax1.plot(time_axis, tonic, label=f'SCL {i}', alpha=0.7)

    # Plotting SCR
    peaks_indices = np.where(peak_mask == 1)[0]
    # ax2.plot(time_axis, bsignals.EDA_Phasic, label=f'SCR {i}', alpha=0.7)
    ax2.plot(time_axis[peak_mask_shifted], peak[peak_mask],linestyle='', marker='o', label=f'Peaks {i}', alpha=0.7)

    # Plotting Trigger
    ax3.plot(time_axis, trigger, alpha=0.7)

# Setting titles for each subplot
ax1.set_title('SCL '+ position)
ax2.set_title('Peaks SCR '+ position)
ax3.set_title('Trigger')

# Adding legends
ax1.legend()
ax2.legend()
plt.tight_layout()
plt.legend()
plt.show()

