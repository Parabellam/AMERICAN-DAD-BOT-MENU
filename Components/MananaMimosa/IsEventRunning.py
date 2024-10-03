import sys
from pathlib import Path
from time import sleep
import pyautogui
pyautogui.useImageNotFoundException(False)
pyautogui.FAILSAFE = False

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path

MANANAMIMOSAEVENT_PATH = "Images/MananaMimosaEvent"

EventNoRunning_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "EventNoRunning_")

def isEventRuning():
    sleep(2)
    found = False
    count = 0
    while not found and count < 10:
        for _, image_path in EventNoRunning_imgs.items():
            locationNoRunning = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if locationNoRunning:
                found = True
                return "No running"
        # if(found==False):
        #     for _, image_path in EventRunning_imgs.items():
        #         locationRunning = pyautogui.locateOnScreen(image_path, confidence=0.95)
        #         count += 1
        #         if locationRunning:
        #             found = True
        #             return "Running"
    return False