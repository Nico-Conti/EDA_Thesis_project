import serial
import array
import time

ser = serial.Serial('COM10', 115200)

size = 4
f = open('MCU_processing.txt', 'wb')
f.truncate(0)
inizio = input("Press Enter to start...")

# Discard initial data for a settling time of 1 second
settling_time = 1
start_time = time.time()
data_counter = 0

while time.time() - start_time < settling_time:
    ser.read(ser.inWaiting())  # Read and discard data

ser.write(b'=')
start_time = time.time()
try:
    while True:
        received_data = ser.read(size)
        
        if not received_data: 
            break
        

        f.write(received_data)
        
        # Increment the data counter
        data_counter += len(received_data)

        # Print data count every second
        if time.time() - start_time >= 1:
            print(f"Data sent in the last second: {data_counter} bytes")
            data_counter = 0
            start_time = time.time()

except KeyboardInterrupt:
    print("Exit")
except serial.SerialException as e:
    print(f"Serial error: {e}")
finally:
    f.close()
    ser.close()
    print("End")
