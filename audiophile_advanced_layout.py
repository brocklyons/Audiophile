import PySimpleGUI as sg

DEFAULT_TRACKS = [  "Salt Shaker",
                    "Roller Mobster",
                    "Unstoppable",
                    "bad guy"
                 ]

TRACKS = DEFAULT_TRACKS

def main():
    sg.theme('BrownBlue') # Add color theme

    prevButton = [[sg.Button("<<")]]
    playButton = [[sg.Button("▶")]]
    nextButton = [[sg.Button(">>")]]

    # All the stuff in the window
    layout = [  [sg.Text("Welcome to Audiophile...")],
                [sg.Text("")],
                [sg.Text("Add a song to your track list"), sg.InputText(do_not_clear=False)],
                [sg.Button('OK'), sg.Button('Exit')],
                [sg.Text("")],
                #[sg.Button('Prev'), sg.Button('Play/Pause'), sg.Button('Next')],
                [
                    sg.Column(prevButton, element_justification="right", size=(100, 30)),
                    sg.Column(playButton, element_justification="center", size=(100, 30)),
                    sg.Column(nextButton, element_justification="left", size=(100, 30))
                ],
                [sg.Listbox(values=TRACKS, key='_TRACK_LIST_', size=(30, 6))]
             ]

    # Create the window
    window = sg.Window('Audiophile', layout)

    # Event loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, "Cancel"): # if the user closes the window or clicks cancel
            break
        if event == "OK" and values[0] is not None and values[0] != "":
            TRACKS.append(values[0])
            window.find_element('_TRACK_LIST_').Update(values=TRACKS)

    window.close() # actually close the window



if __name__ == "__main__":
    main()