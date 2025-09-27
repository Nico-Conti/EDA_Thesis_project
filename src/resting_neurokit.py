import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
import os

def process_data(file_path):
    data = np.fromfile(file_path, dtype="int32").reshape(-1, 2)
    # Extracting columns from the data
    column1 = data[:, 0][:5760]  # Select the first 5760 values
    column2 = data[:, 1][:5760]  # Select the first 5760 values

    sampling_rate = 32  
    total_samples = len(column1)


    # Conversion for the first column
    v_ref = 1
    bioz_conductance_signal = []
    extracted_features = []

    for sample in column1:
        bioz_conductance_signal.append(1 / ((sample * v_ref) / ((2 ** 19) * 10 * (110 * (10**-9)))))

    bioz_conductance_signal = np.array(bioz_conductance_signal)
    # bioz_conductance_signal = (bioz_conductance_signal - bioz_conductance_signal.mean()) / bioz_conductance_signal.std()

    bsignals, binfo = nk.eda_process(bioz_conductance_signal, 32, method="neurokit",method_phasic="highpass", amplitude_min=0.5)

    time_axis = np.arange(total_samples) / sampling_rate

    std_rise_time = np.std(binfo["SCR_RiseTime"])
    mean_rise_time = np.mean(binfo["SCR_RiseTime"])
    # print("Standard Deviation of Phasic (SCR) Rise Time Stressed:", std_rise_time)
    # print("Mean of Phasic (SCR) Rise Time Stressed:", mean_rise_time)

    # Append features and labels for resting periods
    extracted_features.append(mean_rise_time)
    average_extracted_features = np.mean(extracted_features)
    print(average_extracted_features)

    return bioz_conductance_signal, bsignals, column2, time_axis  # Modify to return necessary processed data

    

# List of file paths
position = 'finger'
position_2 = 'hand'

file_paths = [
    position + '_person_1.txt',
    position + '_person_2_L.txt',
    position + '_person_3_P.txt',
    position + '_person_4_E.txt',
    position + '_person_5_T.txt',
    position_2 + '_person_1.txt',
    position_2 + '_person_2_L.txt',
    position_2 + '_person_3_P.txt',
    position_2 + '_person_4_E.txt',
    position_2 + '_person_5_T.txt',

]

# Create lists to store processed data
bioz_conductance_signals = []
bsignals_list = []
column2_list = []
time_axes = []

# Process each file and store the processed data
for file_path in file_paths:
    bioz_signal, bsignal, col2, time = process_data(file_path)
    bioz_conductance_signals.append(bioz_signal)
    bsignals_list.append(bsignal)
    column2_list.append(col2)
    time_axes.append(time)

# Plotting
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6))

for i in range(len(file_paths)):
    time_axis = time_axes[i]
    bsignals = bsignals_list[i]
    column2 = column2_list[i]

    # Plotting SCL
    ax1.plot(time_axis, bsignals.EDA_Tonic, label=f'SCL {i}', alpha=0.7)

    # Plotting SCR
    peaks_indices = np.where(bsignals.SCR_Peaks == 1)[0]
    # ax2.plot(time_axis, bsignals.EDA_Phasic, label=f'SCR {i}', alpha=0.7)
    ax2.plot(time_axis[peaks_indices], bsignals.EDA_Phasic[peaks_indices], linestyle='', marker='o', label=f'Peaks {i}', alpha=0.7)

    # Plotting Trigger
    ax3.plot(time_axis, column2, alpha=0.7)

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


