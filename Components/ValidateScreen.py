import os
import pyautogui
pyautogui.FAILSAFE = False

MAP_BUTTON_PATH = "Images/MapButton"
MAP_SCREEN_PATH = "Images/MapScreen"

map_imgs = {
    "img1": os.path.join(MAP_BUTTON_PATH, "map1.png"),
    "img2": os.path.join(MAP_BUTTON_PATH, "map2.png"),
    "img3": os.path.join(MAP_BUTTON_PATH, "map3.png"),
    "img4": os.path.join(MAP_BUTTON_PATH, "map4.png"),
    "img5": os.path.join(MAP_BUTTON_PATH, "map5.png"),
}

map_screen_imgs = {
    "img1": os.path.join(MAP_SCREEN_PATH, "map_screen_1.png"),
    "img2": os.path.join(MAP_SCREEN_PATH, "map_screen_2.png"),
    "img3": os.path.join(MAP_SCREEN_PATH, "map_screen_3.png"),
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
