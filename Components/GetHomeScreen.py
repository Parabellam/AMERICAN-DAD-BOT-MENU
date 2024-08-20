import pyautogui
import time
import sys
from pathlib import Path

GUERRA_FAMILIALANDIA_PATH = "Images/GuerraFamilialandia"
HOME_PATH = "Images/Home"

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path

leave_home_msg_imgs = load_images_from_path(HOME_PATH, "leave_home_msg_")

def get_home(times, delay=1):
    for _ in range(times):
        pyautogui.press('esc')
        time.sleep(delay)

def validate_home(images, confidence):
    for _, image_path in images.items():
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            return True
    return False

def main_get_home_screen():
    while True:
        get_home(5)
        if validate_home(leave_home_msg_imgs, 0.9):
            get_home(1, 1.5)
            break

    while validate_home(leave_home_msg_imgs, 0.95):
        get_home(1, 1)
    
    return True
