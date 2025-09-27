import PySimpleGUI as sg
import random

# Initialize score
score = 0

# Create initial layout
layout = [[sg.Button('here', key='-HERE-'), sg.Button('not here', key='-NOT_HERE-')],
     [sg.Text(f'Score: {score}', key='-SCORE-')]]

window = sg.Window('Game', layout)

correct_button = '-HERE-'

while True:
  event, values = window.read()

  # Check if any button was clicked
  if event in ('-HERE-', '-NOT_HERE-'):
      # Increase score if correct button was clicked
      if event == correct_button:
          score += 1
      # Reset score if incorrect button was clicked
      else:
          score = 0

      # Update score text
      window['-SCORE-'].update(f'Score: {score}')

      # Randomly swap the labels of the buttons
      if random.choice([True, False]):
          window['-HERE-'].update('not here')
          window['-NOT_HERE-'].update('here')
          correct_button = '-NOT_HERE-'
      else:
          window['-HERE-'].update('here')
          window['-NOT_HERE-'].update('not here')
          correct_button = '-HERE-'

  elif event == sg.WINDOW_CLOSED:
      break

window.close()
