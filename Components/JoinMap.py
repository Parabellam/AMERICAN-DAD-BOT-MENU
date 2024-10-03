import pyautogui
pyautogui.useImageNotFoundException(False)
pyautogui.FAILSAFE = False
from time import sleep


def open_main_map():
    sleep(2)
    pyautogui.click(129, 659)
    sleep(2)
    return True
