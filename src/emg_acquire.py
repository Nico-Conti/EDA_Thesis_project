import serial
import array
import time 
import socket
import PySimpleGUI as sg
import threading

# Create a socket
ser = serial.Serial('COM10', 115200)
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Ensure that you can restart your server quickly when it terminates
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set the client socket's TCP "well-known port" number
image_folder = "C:\\Users\\HP\\OneDrive\\Desktop\\Visual studio\\Python Workspace ecg\\foto\\"

well_known_port = 3333
size=4
#sock.bind(("127.0.0.1", 30000))
layout = [[sg.Text(text='Python GUIs for Humans',
   font=('Arial Bold', 16),
   size=20, expand_x=True,
   justification='center')],
   [sg.Image(f'{image_folder}riposa.png',
   expand_x=True, expand_y=True,key='image' )]
]

# Create the window
window = sg.Window('HelloWorld', layout, size=(715,350), keep_on_top=True)

# Set the number of clients waiting for connection that can be queued
#sock.listen(5)

# loop waiting for connections (terminate with Ctrl-C)
stop=2
f = open('test.txt', 'wb')
f.truncate(0)
inizio = input("premi invio per iniziare")

# Discard initial data for a settling time of 1 second
settling_time = 1  
start_time = time.time()
while time.time() - start_time < settling_time:
    ser.read(ser.inWaiting())  # Read and discard data

ser.write(b'=')

label = ['one', 'two', 'three']
tempo_riposo = 15
tempo_manovra = 3
tempo_inizio = 180

start_rest=0
end_rest=0
end =1
trigger_value = 0

mov_counter = 0

try:
    while 1:
        #newSocket, address = sock.accept(  )
        
        #print("Connected from", address)
        # loop serving the new client
        tic = time.perf_counter()
        start_mov = time.perf_counter()
        n=0
        start_rest =  time.perf_counter()
        start_begin =  time.perf_counter()
        s = 3
        while(end):
            event, values = window.read(timeout = 0)
            #number of byte received   
            receivedData = ser.read(size)
            toc= time.perf_counter()
            end_mov = time.perf_counter()
            end_rest = time.perf_counter()
            end_begin =  time.perf_counter()
            n=n+1
            if(toc-tic>1):
                tic = time.perf_counter()
                
                print(n)
                n=0

            #MANOVRA SESSION
            if(end_mov-start_mov >=tempo_manovra and stop==0):
                if(end_mov-start_mov >= tempo_manovra):
                    stop = 1
                    image = f'{image_folder}riposa.png'
                    window['image'].update(image)
                    trigger_value = 0
                    start_rest = time.perf_counter()

                    mov_counter += 1
                    if mov_counter == 6:
                        tempo_riposo = 30
                        mov_counter = 0
                    else:
                        tempo_riposo = 15
                    


            #REST SESSION
            if(stop==1 and end_rest-start_rest >=tempo_riposo-s):    
                if(stop==1 and end_rest-start_rest >=tempo_riposo):
                    stop=0
                    start_mov = time.perf_counter()
                    image = f'{image_folder}exhale.png'
                    window['image'].update(image)
                    #newSocket.sendall(label[i].to_bytes(2,'little'))
                    trigger_value = 1
                    s = 3
                else:
                    image = f'{image_folder}{label[s-1]}.png'
                    window['image'].update(image)
                    #window['image'].update(f'riposa.png')
                    #newSocket.sendall(b'\x00')
                    s -= 1

            #BEGIN SESSION
            if(end_begin-start_begin >=tempo_inizio-s and stop==2):
                if(end_begin-start_begin >= tempo_inizio):
                    stop = 0
                    image = f'{image_folder}exhale.png'
                    window['image'].update(image)
                    trigger_value = 1
                    start_mov = time.perf_counter()
                    s = 3
                else:
                    image = f'{image_folder}{label[s-1]}.png'
                    window['image'].update(image)
                    #window['image'].update(f'riposa.png')
                    #newSocket.sendall(b'\x00')
                    s -= 1
            
                    
            if event == sg.WIN_CLOSED:
                break
            #print(len(receivedData))
            if not receivedData: 
                break
            receivedDataByte = bytearray(8)
            receivedDataByte = bytearray(receivedData)
            receivedDataByte[4:] = bytearray(trigger_value.to_bytes(4,'little'))
            trigger_value = 0
            
            # print(receivedDataByte)
            f.write(receivedDataByte)
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
    print("exit")
finally:
    ser.close( )
    print("end")