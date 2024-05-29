# Solo cobrar fichas del chat
import time
import pyautogui
import os


CHAT_PATH = "Images/Chat"
RICKYSPANISH_PATH = "Images/RickySpanishIslandEvent"

is_chat_open_imgs = {
    "img1": os.path.join(CHAT_PATH, "is_chat_open_1.png"),
    "img2": os.path.join(CHAT_PATH, "is_chat_open_2.png"),
    "img3": os.path.join(CHAT_PATH, "is_chat_open_3.png"),
}

get_button_imgs = {
    "img1": os.path.join(RICKYSPANISH_PATH, "get_button_1.png"),
    "img2": os.path.join(RICKYSPANISH_PATH, "get_button_2.png"),
}

ficha_imgs = {
    "img1": os.path.join(RICKYSPANISH_PATH, "ficha_1.png"),
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
        end_time = time.time() + 180
        while time.time() < end_time:
            get_fichas()
            close_ficha_img()
            time.sleep(1)
        return True
    return False
