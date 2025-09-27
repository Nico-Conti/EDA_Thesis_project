import serial
import array
import time 

# Create a socket
ser = serial.Serial('COM10', 115200)

# # Ensure that you can restart your server quickly when it terminates
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set the client socket's TCP "well-known port" number
well_known_port = 3333
size=4
#sock.bind(('', well_known_port))

# Set the number of clients waiting for connection that can be queued
# sock.listen(5)

# loop waiting for connections (terminate with Ctrl-C)
stop=1
f = open('serial.txt', 'wb')
f.truncate(0)
inizio = input("premi invio per iniziare")

time.sleep(1)
ser.write(b'=')

start_rest=0
end_rest=0
try:
    while 1:
        # newSocket, address = sock.accept(  )
        # print("Connected from", address)
        # loop serving the new client
        tic = time.perf_counter()
        start_mov = time.perf_counter()
        n=0
        start_rest = time.perf_counter()
        while(1):
            #number of byte received   
            receivedData = ser.read(size)
            toc= time.perf_counter()
            end_mov = time.perf_counter()
            end_rest = time.perf_counter()
            n=n+1
            if(toc-tic>1):
                tic = time.perf_counter()
                
                # print(n*size*8/1000)
                print(n)
                n=0

            if(end_mov-start_mov >=10 and stop==0):
                stop = 1
                print("stop")
                start_rest = time.perf_counter()
            if(stop==1 and end_rest-start_rest >=5):
                stop=0
                start_mov = time.perf_counter()
                print("contrai")

            #print(len(receivedData))
            if not receivedData: 
                break
            f.write(receivedData)
            # for x in receivedData:
            #     #print(f"{int.from_bytes(x, byteorder='big', signed=False)}\n")

            #     #print(f"{x},", end='')
            #     f.write(x)
            #data = array.array('H',receivedData)
            # for x in receivedData:
            #     #print(f"{int.from_bytes(x, byteorder='big', signed=False)}\n")

            #     #print(f"{x},", end='')
            #     f.write(f"{x};")
            # f.write(f"\n")
            #print()

            
            # Echo back the same data you just received
            #newSocket.send(receivedData)
        
        f.close()	
        ser.close(  )
        # print("Disconnected from", address)

except KeyboardInterrupt:
    print("Serial reading stopped by user")
    
finally:
    ser.close( )