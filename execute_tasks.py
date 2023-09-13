import os.path
import subprocess
import platform
import pyautogui

os_name = ''


# Open Opera with specific URL
def open_page(url):
    opera_path = "/Applications/Opera.app/Contents/MacOS/Opera"
    subprocess.run([opera_path, url])


# Open Mac Applicatons
def open_app(app):
    pyautogui.hotkey("command", "l")
    pyautogui.sleep(1)
    pyautogui.typewrite(app)
    pyautogui.sleep(2)
    pyautogui.press('enter')


# Checking and printing OS type
def check_os():
    global os_name
    os_name = platform.system()
    print(os_name)