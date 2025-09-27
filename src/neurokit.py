import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data = pd.read_csv('C:\\Users\\HP\\OneDrive\\Desktop\\Visual studio\\Python Workspace ecg\\csv_folder\\confronto_MCU_NEURO.csv', header=None)

v_ref = 1

# ecg_values = [value.split(':')[1] for value in data.values[0] if 'ECG:' in value] #Seperate ECG values
# ecg_signal = [int(value) for value in ecg_values]

# ecg_signal_converted = []
# for sample in ecg_signal:
#     ecg_signal_converted.append(sample/((2 ** 17) * 20))

# rtor_values = [value.split(':')[1] for value in data.values[0] if 'RTOR:'in value] #Seperate RTOR values
# rtor_signal = [float(value) for value in rtor_values]

bioz_conductance_values = [value.split(':')[1] for value in data.values[0] if 'BIOZ:' in value] #Seperate BIOZ values
bioz_conductance_signal = [float(value) for value in bioz_conductance_values]

biozfiltered_conductance_values = [value.split(':')[1] for value in data.values[0] if 'BIOZ_FILTERED:' in value] #Seperate BIOZ_FILTERED values
biozfiltered_conductance_signal = [float(value) for value in biozfiltered_conductance_values]

bioztonic_conductance_values = [value.split(':')[1] for value in data.values[0] if 'BIOZ_TONIC:' in value]
bioztonic_conductance_signal = [float(value) for value in bioztonic_conductance_values]

biozphasic_conductance_values = [value.split(':')[1] for value in data.values[0] if 'BIOZ_PHASIC:' in value] 
biozphasic_conductance_signal = [float(value) for value in biozphasic_conductance_values]

# bioz_conductance_signal = [value / 100000 for value in bioz_conductance_signal]
# biozfiltered_conductance_signal = [value / 100000 for value in biozfiltered_conductance_signal]
# bioztonic_conductance_signal = [value / 100000 for value in bioztonic_conductance_signal]
# biozphasic_conductance_signal = [value / 100000 for value in biozphasic_conductance_signal]

sampling_rate = 32  # Samples per second
total_samples = len(bioz_conductance_signal)
time_axis = np.arange(total_samples) / sampling_rate

# signals, info = nk.ecg_process(ecg_signal_converted, sampling_rate, method="neurokit")

# bsignals, binfo = nk.eda_process(bioz_conductance_signal, 32, method="neurokit")

# heart_rate = nk.ecg_rate(signals,128)
# heart_rate_sensor = [60 / rr for rr in rtor_signal]

# heart_rate_sensor = heart_rate_sensor[1:]


# timestamps = [pd.Timestamp('2023-11-09')]  # Start time
# for i in range(1, len(heart_rate_sensor)):
#     timestamps.append(timestamps[-1] + pd.Timedelta(seconds=heart_rate_sensor[i-1])/60)

# rr_time_index = pd.DatetimeIndex(timestamps)

# plt.plot(rr_time_index, heart_rate_sensor, label='Sensor RR Intervals')
# plt.plot(rr_time_index, heart_rate, label='NeuroKit Heart Rate')

# plt.xlabel('Time')
# plt.ylabel('Heart Rate (bpm) or RR intervals (s)')
# plt.title('Comparison of Heart Rate and RR Intervals Over Time')
# plt.legend()

# nk.ecg_plot(signals, info)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 5))  # Create subplots with 3 rows and 1 column

# Raw and cleaned subplot
ax1.plot(time_axis, bioz_conductance_signal, color='green', label='Raw')
ax1.plot(time_axis, biozfiltered_conductance_signal, color='purple', label='Cleaned')
ax1.set_title('Raw and Cleaned Signals')
ax1.set_xlabel('Time')
ax1.set_ylabel('Conductance')
ax1.legend()
ax1.grid(True)

# Tonic subplot
ax2.plot(time_axis, biozphasic_conductance_signal, color='red')
ax2.set_title('Phasic Signal')
ax2.set_xlabel('Time')
ax2.set_ylabel('Conductance')
ax2.grid(True)

# Phasic subplot
ax3.plot(time_axis, bioztonic_conductance_signal, color='blue')
ax3.set_title('Tonic Signal')
ax3.set_xlabel('Time')
ax3.set_ylabel('Conductance')
ax3.grid(True)

signals, info = nk.eda_process(bioz_conductance_signal, 32, amplitude_min = 0.1)
nk.eda_plot(signals, info)

plt.tight_layout()  # Adjust layout for better spacing
plt.show()




