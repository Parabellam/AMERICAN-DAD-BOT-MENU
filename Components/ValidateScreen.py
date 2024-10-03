import os
import pyautogui
pyautogui.useImageNotFoundException(False)
pyautogui.FAILSAFE = False

MAP_BUTTON_PATH = "Images/MapButton"
MAP_SCREEN_PATH = "Images/MapScreen"

map_imgs = {
    f"img{index+1}": os.path.join(MAP_BUTTON_PATH, file)
    for index, file in enumerate(os.listdir(MAP_BUTTON_PATH))
    if file.startswith("map_btn_") and file.endswith(".png")
}
map_button_region = (20, 539, 238, 197)

map_screen_imgs = {
    f"img{index+1}": os.path.join(MAP_SCREEN_PATH, file)
    for index, file in enumerate(os.listdir(MAP_SCREEN_PATH))
    if file.startswith("map_screen_") and file.endswith(".png")
}

CONFIDENCE = 0.95
MAX_ATTEMPTS = 10


def isOutMainMap():
    found = False
    count = 0
    while not found and count < MAX_ATTEMPTS:
        for _, image_path in map_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE)
            count += 1
            if location:
                found = True
                return {"state": "outMainMap", "location": location}
    return {"state": False}


def isInMainMap():
    found = False
    count = 0
    while not found and count < MAX_ATTEMPTS:
        for _, image_path in map_screen_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE)
            count += 1
            if location:
                found = True
                return {"state": "inMainMap"}
    return {"state": False}


def detect_screen():
    resp = isOutMainMap()
    if (resp.get('state') == False):
        resp = isInMainMap()
    return resp
