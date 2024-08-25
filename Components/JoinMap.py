import pyautogui
pyautogui.FAILSAFE = False
from time import sleep


def open_main_map():
    sleep(2)
    pyautogui.click(129, 659)
    print("Se ha hecho click en el mapa")
    sleep(2)
    return True
