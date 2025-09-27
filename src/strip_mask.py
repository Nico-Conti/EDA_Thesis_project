import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
import os

# file_path = os.path.join('txt', 'serial.txt')
data = np.fromfile('finger_person_5_T.txt', dtype="int32").reshape(-1, 2)
# Extracting columns from the data
column1 = data[:, 0]

column1.tofile('super_test.txt')
