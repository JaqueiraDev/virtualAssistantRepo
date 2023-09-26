import os.path
import subprocess
import platform
import pyautogui
from selenium import webdriver as options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

os_name = ''
pyautogui.FAILSAFE = True
first_time = True


# Open Opera with specific URL
def open_page(url):
    opera_path = "/Applications/Opera.app/Contents/MacOS/Opera"
    subprocess.run([opera_path, url])


def search_on_google(search_text):
    navigator = options.Firefox()
    navigator.get('https://www.google.pt')
    navigator.maximize_window()  # Maximize browser window
    pyautogui.sleep(1)
    button_cookie_xpath = '//*[@id="L2AGLb"]'  # Xpath from cookie Accept button on Chrome
    button_cookie = navigator.find_element(By.XPATH, button_cookie_xpath)  # Create variable and find button
    button_cookie.click()  # Click the Accept button
    x_path = '//*[@id="APjFqb"]'
    pyautogui.sleep(2)
    navigator.find_element(By.XPATH, x_path).send_keys(search_text)
    pyautogui.sleep(2)
    pyautogui.press('enter')


def play_song_spotify(music_name):
    navigator = options.Firefox()
    navigator.get('https://www.spotify.com')
    navigator.maximize_window()
    pyautogui.sleep(2)
    button_cookie_xpath = '//*[@id="onetrust-accept-btn-handler"]'  # Xpath from cookie Accept button on Chrome
    button_cookie = navigator.find_element(By.XPATH, button_cookie_xpath)  # Create variable and find button
    button_cookie.click()


def open_app(app):  # Open Mac Applications
    global first_time
    if first_time:
        pyautogui.press('shift')  # Just to activate the Python before try to open an app
        pyautogui.sleep(3)
        first_time = False
    pyautogui.hotkey("command", "l")
    pyautogui.sleep(2)
    pyautogui.typewrite(app)
    pyautogui.sleep(2)
    pyautogui.press('enter')
    if app == "spotify":
        play_song_spotify()


def check_os():  # Checking and printing OS type
    global os_name
    os_name = platform.system()
    print(os_name)


