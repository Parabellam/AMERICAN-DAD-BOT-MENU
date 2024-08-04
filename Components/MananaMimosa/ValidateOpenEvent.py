import sys
from pathlib import Path
import time
import pyautogui
pyautogui.FAILSAFE = False

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path

MANANAMIMOSAEVENT_PATH = "Images/MananaMimosaEvent"

EventNoRunning_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "EventNoRunning_")
EventRunning_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "EventRunning_")

def validate_open_event():
    found = False
    count = 0
    time.sleep(2)
    while not found and count < 10:
        for _, image_path in EventNoRunning_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            found = True
            if location:
                return found
    print("Falló event no running e intentará buscar EventRunning")
    found = False
    count = 0
    while not found and count < 10:
        for _, image_path2 in EventRunning_imgs.items():
            location2 = pyautogui.locateOnScreen(image_path2, confidence=0.95)
            count += 1
            found = True
            if location2:
                return "Event running"
    return found


def open_event():
    time.sleep(1)
    pyautogui.click(1096, 180)
    return True