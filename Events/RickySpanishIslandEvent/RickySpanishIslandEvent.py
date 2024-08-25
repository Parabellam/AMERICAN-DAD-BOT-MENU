# Solo cobrar fichas del chat
from time import sleep
from time import time
import pyautogui
import os


CHAT_PATH = "Images/Chat"
RICKYSPANISH_PATH = "Images/RickySpanishIslandEvent"

is_chat_open_imgs = {
    f"img{index+1}": os.path.join(CHAT_PATH, file)
    for index, file in enumerate(os.listdir(CHAT_PATH))
    if file.startswith("is_chat_open_") and file.endswith(".png")
}

get_button_imgs = {
    f"img{index+1}": os.path.join(RICKYSPANISH_PATH, file)
    for index, file in enumerate(os.listdir(RICKYSPANISH_PATH))
    if file.startswith("get_button_") and file.endswith(".png")
}

ficha_imgs = {
    f"img{index+1}": os.path.join(RICKYSPANISH_PATH, file)
    for index, file in enumerate(os.listdir(RICKYSPANISH_PATH))
    if file.startswith("ficha_") and file.endswith(".png")
}


def isChatOpen():
    found = False
    count = 0
    while not found and count < 10:
        for _, image_path in is_chat_open_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            found = True
            if location:
                return found
    return found


def get_fichas():
    found = False
    while not found:
        for _, image_path in get_button_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            found = True
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True


def close_ficha_img():
    found = False
    count = 0
    while not found and count < 10:
        for _, image_path in ficha_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            found = True
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return found
    return True


def chatEvent():
    pyautogui.click(98, 340)  # Abrir chat
    respIsChatOpen = isChatOpen()
    if (respIsChatOpen):
        end_time = time() + 180
        while time() < end_time:
            get_fichas()
            close_ficha_img()
            sleep(1)
        return True
    return False
