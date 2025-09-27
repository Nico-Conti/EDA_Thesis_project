import cvxEDA
import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk

# file_path = os.path.join('txt', 'serial.txt')
data = np.fromfile('wrist_person_4_E.txt', dtype="int32").reshape(-1, 2)

# Extracting columns from the data
column1 = data[:, 0]
column2 = data[:, 1]

v_ref = 1
y = []
for sample in column1:
    y.append(1 / ((sample * v_ref) / ((2 ** 19) * 10 * (110 * (10**-9)))))

# Convert y to a NumPy array
y = np.array(y)

yn = (y - y.mean()) / y.std()
Fs = 32.
[r, p, t, l, d, e, obj] = cvxEDA.cvxEDA(yn, 1./Fs)

tm = np.arange(1., len(y)+1.) / Fs

# bsignals, binfo = nk.eda_process(y, 32, method="neurokit",method_phasic="highpass", amplitude_min=0.4)

# plt.plot(tm, bsignals.EDA_Phasic * 1000000, label='SCR_highpass')

plt.plot(tm, yn, label='yn')
plt.plot(tm, r, label='r')
plt.plot(tm, p, label='p')
plt.plot(tm, t, label='t')
plt.legend()
plt.show()