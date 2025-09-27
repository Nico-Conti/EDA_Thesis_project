import numpy as np
import neurokit2 as nk
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import accuracy_score, precision_score, f1_score

# Initialize lists to store extracted features and corresponding labels
std_max_peak_stressed = []
std_amplitude_resting_mean = []
all_max_peak_stressed = []
all_mean_peak_stressed = []
all_max_peak_resting = []
all_mean_peak_resting = []
labels = []

# Define a list of filenames
file_names = ['finger_person_1.txt', 'finger_person_2_L.txt', 'finger_person_3_P.txt', 'finger_person_5_T.txt','hand_person_1.txt','hand_person_2_L.txt','hand_person_3_P.txt','hand_person_4_E.txt','wrist_person_4_E.txt', 'wrist_person_5_T.txt']

for file_name in file_names:
    data = np.fromfile(file_name, dtype="int32").reshape(-1, 2)

    # Splitting into resting and stressed periods
    resting_samples = 5760  # Assuming first 5760 samples are resting
    resting_data = data[:resting_samples]
    stressed_data = data[resting_samples:]

    # Extracting columns from the data for resting and stressed periods
    resting_column1 = resting_data[:, 0]
    resting_column2 = resting_data[:, 1]

    stressed_column1 = stressed_data[:, 0]
    stressed_column2 = stressed_data[:, 1]

    sampling_rate = 32  # Samples per second

    # Resting Period Processing
    bioz_conductance_signal_resting = np.array([(1 / ((sample * 1) / ((2 ** 19) * 10 * (110 * (10**-9))))) for sample in resting_column1])
    # bioz_conductance_signal_resting = (bioz_conductance_signal_resting - np.mean(bioz_conductance_signal_resting)) / np.std(bioz_conductance_signal_resting)

    bsignals_resting, binfo_resting = nk.eda_process(bioz_conductance_signal_resting, sampling_rate, method="neurokit", method_phasic="highpass", amplitude_min=0.25)
    std_amplitude_resting = np.std(binfo_resting["SCR_Amplitude"])
    mean_peaks_resting = np.min(binfo_resting["SCR_Amplitude"])
    max_peak_resting = np.max(binfo_resting["SCR_Amplitude"])
    # print("Standard Deviation of Phasic SCR_Amplitude Resting:", std_amplitude_resting)
    # print("Mean of Phasic SCR_Amplitude Resting:", mean_amplitude_resting)
    # Append features and labels for resting periods
    all_max_peak_resting.append(max_peak_resting)
    all_mean_peak_resting.append(mean_peaks_resting)

    # Stressed Period Amplitude
    bioz_conductance_signal_stressed = np.array([(1 / ((sample * 1) / ((2 ** 19) * 10 * (110 * (10**-9)))))  for sample in stressed_column1])
    # bioz_conductance_signal_stressed = (bioz_conductance_signal_stressed - np.mean(bioz_conductance_signal_stressed)) / np.std(bioz_conductance_signal_stressed)

    bsignals_stressed, binfo_stressed = nk.eda_process(bioz_conductance_signal_stressed, sampling_rate, method="neurokit", method_phasic="highpass", amplitude_min=0.25)

    std_amplitude_stressed = np.std(binfo_stressed["SCR_Amplitude"])
    mean_peaks_stressed = np.min(binfo_stressed["SCR_Amplitude"])
    max_peak_stressed = np.max(binfo_stressed["SCR_Amplitude"])
    # print("Standard Deviation of Phasic SCR_Amplitude Stressed:", std_amplitude_stressed)
    # print("Max peak Phasic SCR Stressed:", max_peak_stressed)
    all_max_peak_stressed.append(max_peak_stressed)
    all_mean_peak_stressed.append(mean_peaks_stressed)

# Calculate the mean of means and the mean of std
# print(np.mean(mean_amplitude_resting_mean))
# print(np.mean(std_amplitude_resting_mean))

# print(np.mean(mean_amplitude_stressed_mean))
# print(np.mean(std_amplitude_stressed_mean))

result_max_stressed = (np.mean(all_max_peak_stressed) + np.std(all_max_peak_stressed)) * 0.25
result_mean_stressed = (np.mean(all_mean_peak_stressed) + 2 * np.std(all_mean_peak_stressed))
result_max_resting = (np.mean(all_max_peak_resting) + 2 * np.std(all_max_peak_resting)) * 0.25
result_mean_resting = (np.mean(all_mean_peak_resting) + 3 * np.std(all_mean_peak_resting)) 
print("Treshold using max peak from each signal stressed:", result_max_stressed)
print("Treshold using mean peak from each signal stressed:", result_mean_stressed)
print("Treshold using max peak from each signal resting:", result_max_resting)
print("Treshold using mean peak from each signal resting:", result_mean_resting)