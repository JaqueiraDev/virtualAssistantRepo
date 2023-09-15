import os.path
import subprocess
import platform
import pyautogui

os_name = ''


# Open Opera with specific URL
def open_page(url):
    opera_path = "/Applications/Opera.app/Contents/MacOS/Opera"
    subprocess.run([opera_path, url])


def open_app(app):  # Open Mac Applications
    pyautogui.hotkey("command", "l")
    pyautogui.sleep(1)
    pyautogui.typewrite(app)
    pyautogui.sleep(2)
    pyautogui.press('enter')
    if app == "spotify":
        play_song_spotify()


def check_os():  # Checking and printing OS type
    global os_name
    os_name = platform.system()
    print(os_name)


def play_song_spotify():  # Play a song on Spotify
    print(" ")
