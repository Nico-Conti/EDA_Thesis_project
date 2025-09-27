import serial
import array
import time 
import socket
import PySimpleGUI as sg
import threading
import random

ser = serial.Serial('COM10', 115200)
image_folder = "C:\\Users\\HP\\OneDrive\\Desktop\\Visual studio\\Python Workspace ecg\\foto\\"

size=4

score = 0
timer = 4
idx_c = random.randint(0, 3)
idx_w = random.randint(0, 3)
stop = 0
start_timer = 0
trigger_value = 0
n_test = 0

while idx_w == idx_c:
    idx_w = random.randint(0,3)

if random.choice([True, False]):
    correct_button = '-LEFT-'
    left_start = idx_c
    right_start = idx_w
else:
    correct_button = '-RIGHT-'
    left_start = idx_w
    right_start = idx_c



colours = ['red', 'yellow', 'blue', 'green']


layout_1 = [
    [sg.Text('Python GUIs for Humans', font=('Arial Bold', 16), size=(20, 1), justification='center')],
    [sg.Image(f'{image_folder}riposa.png', size=(300, 200), pad=(50, 20))]
]

layout_2 = [
    [
        sg.Text(f'Score: {score}',key='-SCORE-',font=('Helvetica', 15), size=(10, 1)), sg.Text(f'Time: {timer}',key='-TIMER-',font=('Helvetica', 15), size=(10, 1))
    ],
    [
        sg.Text(colours[idx_w], font=('Helvetica', 50), text_color=f'{colours[idx_c]}', justification='center', size=(30, 1), key = '-COLOUR-')
    ],
    [
        sg.Text('', font=('Helvetica', 50), text_color='red', justification='center', size=(30, 1))
    ],
    [   
        sg.Column([
            [sg.Button(f'{colours[left_start]}', size=(15, 2), key='-LEFT-'), sg.Button(f'{colours[right_start]}', size=(15, 2), key='-RIGHT-')]
        ], justification='center', element_justification='center',key='-BUTTONS-')
    ]
]

layout_3 = [
    [
        sg.Text(f'Score: {score}',key='-SCORE-',font=('Helvetica', 15), size=(10, 1)), sg.Text(f'Time: {timer}',key='-TIMER-',font=('Helvetica', 15), size=(10, 1))
    ],
    [
        sg.Text(colours[idx_w], font=('Helvetica', 50), text_color=f'{colours[idx_c]}', justification='center', size=(30, 1), key = '-COLOUR-')
    ],
    [
        sg.Text('', font=('Helvetica', 50), text_color='red', justification='center', size=(30, 1))
    ],
    [   
        sg.Column([
            [sg.Button(button_color='red', size=(15, 2), key='-LEFT_2-'), sg.Button(button_color='blue', size=(15, 2), key='-RIGHT_2-')]
        ], justification='center', element_justification='center',key='-BUTTONS_2-')
    ]
]

layout = [[sg.Column(layout_1, key='-COL1-', visible = True), sg.Column(layout_2, visible=False, key='-COL2-'), sg.Column(layout_3, visible=False, key='-COL3-')]]


window = sg.Window('HelloWorld', layout, size=(500,300), keep_on_top=True)


# loop waiting for connections (terminate with Ctrl-C)
f = open('finger_person_stroop_1.txt', 'wb')
f.truncate(0)
inizio = input("premi invio per iniziare")

# Discard initial data for a settling time of 1 second
settling_time = 1  
discard_start = time.time()
while time.time() - discard_start < settling_time:
    ser.read(ser.inWaiting())  # Read and discard data

ser.write(b'=')
start_time = time.time()

try:
    while True:
        event, values = window.read(timeout=0)
        receivedData = ser.read(size)

        if time.time() - start_time > 180 and stop == 0:
            # window = sg.Window('H', layout_2, size=(500, 200), keep_on_top=True)
            window['-COL1-'].update(visible=False)
            window['-COL2-'].update(visible=True)
            window['-COL3-'].update(visible=False)
            start_timer = time.time()
            stop = 1
            trigger_value = 1
            
        else:
            if timer > 0:  # Ensure timer is positive
                if time.time() - start_timer > 1:
                    start_timer = time.time()  # Reset timer
                    timer -= 1  # Decrement timer
                    window['-TIMER-'].update(f'Time: {timer}')  # Update timer display

                if event in ('-LEFT-', '-RIGHT-'):
                    timer = 3
                    window['-TIMER-'].update(f'Time: {timer}')  # Update timer display
                    if event == correct_button:
                        score += 1
                    else:
                        score = 0

                    idx_c = random.randint(0, 3)
                    idx_w = random.randint(0, 3)

                    while idx_w == idx_c:
                        idx_w = random.randint(0, 3)
                    

                    window['-COLOUR-'].update(colours[idx_w], text_color=f'{colours[idx_c]}',)
                    window['-SCORE-'].update(f'Score: {score}')

                    if random.choice([True, False]):
                        window['-LEFT-'].update(f'{colours[idx_w]}')
                        window['-RIGHT-'].update(f'{colours[idx_c]}')
                        correct_button = '-RIGHT-'
                    else:
                        window['-LEFT-'].update(f'{colours[idx_c]}')
                        window['-RIGHT-'].update(f'{colours[idx_w]}')
                        correct_button = '-LEFT-'
                    
        
                    # ... (rest of your previous code)
            if timer == 0:
                timer = 3
                window['-TIMER-'].update(f'Time: {timer}')  # Update timer display
                idx_c = random.randint(0, 3)
                idx_w = random.randint(0, 3)

                while idx_w == idx_c:
                    idx_w = random.randint(0, 3)
                

                window['-COLOUR-'].update(colours[idx_w], text_color=f'{colours[idx_c]}',)
                window['-SCORE-'].update(f'Score: {score}')

                if random.choice([True, False]):
                    window['-LEFT-'].update(f'{colours[idx_w]}')
                    window['-RIGHT-'].update(f'{colours[idx_c]}')
                    correct_button = '-RIGHT-'
                else:
                    window['-LEFT-'].update(f'{colours[idx_c]}')
                    window['-RIGHT-'].update(f'{colours[idx_w]}')
                    correct_button = '-LEFT-'
                
            
        if event == sg.WIN_CLOSED:
            break

        receivedDataByte = bytearray(8)
        receivedDataByte = bytearray(receivedData)
        receivedDataByte[4:] = bytearray(trigger_value.to_bytes(4,'little'))
        
        print(receivedDataByte)
        f.write(receivedDataByte)

    f.close()	
    ser.close(  )
except KeyboardInterrupt:
    print("exit")
finally:
    ser.close()
    print("end")
