"""
--------------------------------
|          Audiophile          |
--------------------------------
- Build software to play an MP3 file with a GUI that looks like a traditional MP3 player
- Interface for listing the available MP3 files
- Interface to show details of the current file like Name, Artist, time currently played
- pygame is a library that lets python play audio files

MP3 Functionality:
# DONE: Play hardcoded MP3 on Play button press
# DONE: Implement play/pause toggle functionality
# DONE: When a track finishes, go to the next track
# DONE: Implement Next/Previous song on button press
# TODO: Input path to Music Library folder
# TODO: Clicking on song in Music Library in-app display plays the song

Interface Functionality:
# TODO: Show current progress of track on scrubber and time
# DONE: Show MP3 title
# TODO: Show MP3 artist
# TODO: Display Songs in Music Library
# TODO: Beautify UI overall

Test commit from new laptop
"""

import os
import time
import PySimpleGUI as sg
import pygame
from mutagen.mp3 import MP3

PLAY_PAUSE_LABEL = "Play / Pause"
PREV_TRACK_LABEL = "Prev"
NEXT_TRACK_LABEL = "Next"
CLOSE_WINDOW_LABEL = "Close"

SLEEP_AFTER_BUTTON_CLICK = 0.2              # Time to sleep after button press for better UX
RESTART_TRACK_TIME_THRESHOLD_SECONDS = 2    # When hitting "Prev", if past this restart song

NEXT = pygame.USEREVENT + 1

# Globals
playing = False             # Are we currently playing anything
currentSongPlayed = False   # Has the current song been played yet
musicFiles = []             # The mp3 files in Music Library
fileIndex = 0               # The index of the current file in Music Library selected
trackStartedTime = 0        # The time we started the currently playing track in seconds

# -----------------------------------------------------------------------


def generate_GUI_window():
    """
    Generate a PySimpleGUI window for the Audiophile player
    :return: the PySimpleGUI window we created
    """
    sg.theme('BrownBlue')  # Add color theme
    # All the stuff in the window
    layout = [
        [sg.Text("Welcome to Audiophile...")],
        [sg.Text("")],
        [sg.Text("Playing:                                             ", key="_TRACK_TITLE_")],
        [sg.Button(PREV_TRACK_LABEL), sg.Button(PLAY_PAUSE_LABEL), sg.Button(NEXT_TRACK_LABEL)],
        [sg.Text("")],
        [sg.Button(CLOSE_WINDOW_LABEL)]
    ]
    return sg.Window('Audiophile', layout)


def get_all_mp3_files_in_library():
    """
    Get all mp3 files within the "MusicLibrary/" directory
    :return: a list of all mp3 files in the directory
    """
    path = "./MusicLibrary/"
    files = []
    for r, d, f, in os.walk(path):
        for file in f:
            if '.mp3' in file:
                files.append(os.path.join(r, file))
    return files


def get_mp3_sample_rate(mp3file):
    """
    Helper function to get the sample rate of a given mp3 file
    :param mp3file: path to the mp3 file to get the sample rate of
    :return: the sample rate of mp3file
    """
    f = MP3(mp3file)
    return int(f.info.sample_rate)


def get_track_name(mp3file):
    """
    Get the track name of the mp3file
    :param mp3file:
    :return: the track name of the file
    """
    splits = (mp3file.rsplit('/', 1))
    splits.reverse()
    trackName = splits[0]
    return trackName


def handle_play_pause_button_action():
    """
    Handle when the play/pause button is pressed
    """
    global playing
    global currentSongPlayed
    global trackStartedTime

    playing = not playing
    if playing:  # start playback of current selected song
        if currentSongPlayed:  # Has the current song been played yet (do we play or unpause)
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.play()
            currentSongPlayed = True
            trackStartedTime = time.time()
    else:
        pygame.mixer.music.pause()

def handle_previous_button_action():
    """
    Handle when the previous button is pressed
    """
    global fileIndex
    global currentSongPlayed

    if currentSongPlayed:
        elapsed = time.time() - trackStartedTime
        if elapsed <= RESTART_TRACK_TIME_THRESHOLD_SECONDS:
            if fileIndex == 0:
                fileIndex = len(musicFiles) - 1
            else:
                fileIndex -= 1
            load_new_track(musicFiles[fileIndex])
        else:
            pygame.mixer.music.rewind() # Start the current song over
            currentSongPlayed = False
    else: # The currently selected song hasn't even started playing, go to the previous song
        if fileIndex == 0:
            fileIndex = len(musicFiles) - 1
        else:
            fileIndex -= 1
        load_new_track(musicFiles[fileIndex], playing)


def handle_next_button_action():
    """
    Handle when the next button is pressed
    """
    global fileIndex

    if fileIndex == len(musicFiles) - 1:
        fileIndex = 0
    else:
        fileIndex += 1
    load_new_track(musicFiles[fileIndex], playing)


def load_new_track(mp3file, play_song=True):
    """
    Start playing a new given mp3file
    :param mp3file: the new file to play
    :param play_song: whether we should play the song when loaded
    """
    global currentSongPlayed
    global trackStartedTime

    pygame.mixer.quit()  # Quit so we can reset the frequency to the new sample rate of the track
    pygame.mixer.init(frequency=get_mp3_sample_rate(mp3file))
    pygame.mixer.music.load(mp3file)
    if play_song:
        pygame.mixer.music.play()
        currentSongPlayed = True
        trackStartedTime = time.time()
    else:
        currentSongPlayed = False


def main():
    """
    Main functionality of the Audiophile player
    Contains the loop to continuously get updates from the window
    """
    global musicFiles

    musicFiles = get_all_mp3_files_in_library()
    mp3file = musicFiles[fileIndex]  # Start by getting the first file in the directory
    pygame.mixer.init(frequency=get_mp3_sample_rate(mp3file))
    pygame.mixer.music.load(mp3file)

    window = generate_GUI_window() # Create the window
    window.BringToFront()

    # Event loop for window updating
    while True:
        event, values = window.read(timeout=1) # timeout=1 means this loop will run once a second
        if event in (None, CLOSE_WINDOW_LABEL): # if the user closes the window or clicks Close
            break

        elif event == PLAY_PAUSE_LABEL: # Play/Pause button pressed
            time.sleep(SLEEP_AFTER_BUTTON_CLICK) # UX Sleep
            handle_play_pause_button_action()
            window.find_element("_TRACK_TITLE_").Update("Playing: {}".format(
                get_track_name(musicFiles[fileIndex])))

        elif event == PREV_TRACK_LABEL: # Previous button pressed
            time.sleep(SLEEP_AFTER_BUTTON_CLICK) # UX Sleep
            handle_previous_button_action()
            window.find_element("_TRACK_TITLE_").Update("Playing: {}".format(
                get_track_name(musicFiles[fileIndex])))

        elif event == NEXT_TRACK_LABEL: # Next button pressed
            time.sleep(SLEEP_AFTER_BUTTON_CLICK) # UX Sleep
            handle_next_button_action()
            window.find_element("_TRACK_TITLE_").Update("Playing: {}".format(
                get_track_name(musicFiles[fileIndex])))

        # Check to see if the current song that was playing has ended, if so play the next song
        if not pygame.mixer.music.get_busy() and currentSongPlayed and playing:
            time.sleep(2)
            handle_next_button_action()
            window.find_element("_TRACK_TITLE_").Update("Playing: {}".format(
                get_track_name(musicFiles[fileIndex])))


    pygame.mixer.quit()
    window.close() # actually close the window


# -----------------------------------------------------------------------


if __name__ == "__main__":
    main()
