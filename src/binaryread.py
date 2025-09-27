import struct
import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt

# Read the binary data from the CSV file as a single string
with open('binary.csv', 'rb') as file:  # 'rb' mode for reading bytes
    binary_data = file.read()

# Interpret bytes as 32-bit signed integers
int_count = len(binary_data) // 4  # Assuming each integer is represented by 4 bytes
bioz_voltage_signal = struct.unpack(f'{int_count}i', binary_data)

bioz_conductance_signal = []
for sample in bioz_voltage_signal:
    bioz_conductance_signal.append(1/((sample * 1)/ ((2 ** 19) * 10 * (110 * (10**-9)))))
    
# Assuming the sampling rate of 128 Sa/s
sampling_rate = 128

# Process the EDA signal using NeuroKit2
bsignals, binfo = nk.eda_process(bioz_conductance_signal, sampling_rate, method="neurokit")

# Plot EDA signal
nk.eda_plot(bsignals, binfo)
plt.show()