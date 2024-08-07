import sys
from pathlib import Path
import time
import pyautogui
pyautogui.FAILSAFE = False

ANOTHER_SESSION_BUTTON_PATH = "Images/Errors"
GLOBAL_PATH = "Images/Global"
HOME_PATH = "Images/Home"

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path
from Components._GlobalOpenValidateJoin import open_validate_join

another_session_button_imgs = load_images_from_path(ANOTHER_SESSION_BUTTON_PATH, "another_session_button_")
loading_game_imgs = load_images_from_path(GLOBAL_PATH, "loading_game_")
leave_home_msg_imgs = load_images_from_path(HOME_PATH, "leave_home_msg_")

def reload_game_another_session():
    count = 0
    while count < 20:
        for _, image_path in another_session_button_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                count = 21
                break
            elif count == 19:
                return False
    time.sleep(5)
    count = 0
    failCount = 0
    while count < 25 and failCount < 200:
        for _, image_path in loading_game_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.9)
            if location:
                time.sleep(8)
                failCount += 1
            else:
                count += 1
    if count > 24:
        time.sleep(10)
        count = 0
        while count == 0:
            pyautogui.press('esc')
            time.sleep(2.5)
            for _, image_path in leave_home_msg_imgs.items():
                location = pyautogui.locateOnScreen(image_path, confidence=0.9)
                if location:
                    pyautogui.press('esc')
                    count = 1
                    time.sleep(1.5)
                    break
        for _, image_path2 in leave_home_msg_imgs.items():
            location2 = pyautogui.locateOnScreen(image_path2, confidence=0.9)
            if location2:
                pyautogui.press('esc')
                count = 1
                time.sleep(1)
                break
        print("El juego logró cargar correctamente, validando pantalla.")
        time.sleep(2)
    elif failCount > 199:
        print("El juego NO logró cargar correctamente.")
        time.sleep(5)
        return False
    open_validate_join(True)
    return True