import serial
import array
import time

ser = serial.Serial('COM10', 115200)
size = 4
size_receive = 4 * 5
receive_file = open('MCU_test.txt', 'wb')
receive_file.truncate(0)
transmit_file = open('super_test.txt', 'rb')

inizio = input("Press Enter to start...")

# Discard initial data for a settling time of 1 second
settling_time = 1
start_time = time.time()
data_counter = 0


start_time = time.time()
try:
    while True:
        send_data = transmit_file.read(size)
        ser.write(send_data)
        if not send_data:
            break  # Exit the loop if the file is fully read
        

        received_data = ser.read(size_receive)
        # print(f"Sent: {send_data}, Received: {received_data}")
        
        if not received_data: 
            break

        receive_file.write(received_data)
        
        # Increment the data counter
        data_counter += len(received_data)

        # Print data count every second
        if time.time() - start_time >= 1:
            print(f"Data sent from MCU in the last second: {data_counter} bytes")
            data_counter = 0
            start_time = time.time()

except KeyboardInterrupt:
    print("Exit")
except serial.SerialException as e:
    print(f"Serial error: {e}")
finally:
    receive_file.close()
    ser.close()
    print("End")
