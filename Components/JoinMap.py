import pyautogui
pyautogui.FAILSAFE = False


def open_main_map(location):
    center_x, center_y = pyautogui.center(location)
    pyautogui.click(center_x, center_y)
    return True
