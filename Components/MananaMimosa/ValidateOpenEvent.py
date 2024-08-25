import sys
from pathlib import Path
from time import sleep
import pyautogui
pyautogui.FAILSAFE = False

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path
from Components.isErrorMessage import main_are_there_errors

MANANAMIMOSAEVENT_PATH = "Images/MananaMimosaEvent"
MANANAMIMOSAEVENTFIGHT_PATH = "Images/MananaMimosaEvent/Fight"

CONFIDENCE_LEVEL_TWO = 0.95
FinishEvent_region = (1037, 123, 252, 119)

EventNoRunning_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "EventNoRunning_")
EventRunning_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "EventRunning_")
FinishEvent_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "FinishEvent_")

def miss_click():
    pyautogui.click(165, 194)
    sleep(0.5)
    pyautogui.click(165, 194)

def is_finish_event():
    for _, image_path in FinishEvent_imgs.items():
        location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO, region=FinishEvent_region)
        if main_are_there_errors():
                return "Error"
        if location:
            miss_click()
            sleep(1)
            miss_click()
            center_x, center_y = pyautogui.center(location)
            pyautogui.click(center_x, center_y)
            return True
        else:
            sleep(1.5)
    return False

def validate_open_event():
    found = False
    count = 0
    sleep(2)
    while not found and count < 10:
        for _, image_path in EventNoRunning_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            count += 1
            found = True
            if location:
                return found
    print("Falló event no running e intentará buscar EventRunning")
    found = False
    count = 0
    while not found and count < 10:
        for _, image_path2 in EventRunning_imgs.items():
            location2 = pyautogui.locateOnScreen(image_path2, confidence=CONFIDENCE_LEVEL_TWO)
            count += 1
            found = True
            if location2:
                resp = is_finish_event()
                if(resp==False):
                    print("Esperando 90 1")
                    sleep(30)
                    resp = is_finish_event()
                    if(resp==False):
                        sleep(30)
                        resp = is_finish_event()
                        if(resp==False):
                            sleep(30)
                            resp = is_finish_event()
                            if(resp==False):
                                print("Esperando 300 1")
                                sleep(300)
                                resp = is_finish_event()
                return True
    print("Error fatal 2")
    return found


def open_event():
    print("Haciendo open_event:")
    sleep(1)
    pyautogui.click(1096, 180)
    return True