import serial
import matplotlib.pyplot as plt
from collections import deque

ecg_data = deque(maxlen=500)  # Initialize a deque to store the last 500 ECG data points
ser = serial.Serial(port='COM10', baudrate=115200)

plt.ion()  # Turn on interactive mode for continuous plotting

fig, ax = plt.subplots()
line, = ax.plot([])

while True:
    try:
        # Read a line and decode it to a string
        data = ser.readline().decode('utf-8').strip()

        # Split the data by ',' and check for 'BIOZ:' in each element
        values = [float(d.split('BIOZ:')[1]) for d in data.split(',') if 'BIOZ:' in d]

        for value in values:
            print(f"Received data: {value}")  # Print the received data value
            ecg_data.append(value)  # Append the received data value as a float to the deque

            line.set_xdata(range(len(ecg_data)))
            line.set_ydata(ecg_data)
            ax.relim()
            ax.autoscale_view()

            if len(ecg_data) < 200:
                ax.set_xlim(0, 200)
            else:
                ax.set_xlim(len(ecg_data) - 200, len(ecg_data))

            plt.draw()
            plt.pause(0.01)  # Adjust the pause duration as needed

    except KeyboardInterrupt:
        break

ser.close()  # Close the serial port when done

