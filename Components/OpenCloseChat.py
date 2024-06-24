import time
import pyautogui
pyautogui.FAILSAFE = False
from glob import glob
import os

OPENCLOSECHAT_PATH = "Images/Chat"
GETBUTTONSCHAT_PATH = "Images/Chat/getButtonEvents"

def load_images_from_path(path, prefix, suffix=".png"):
    return {
        f"img{index+1}": file
        for index, file in enumerate(glob(os.path.join(path, f"{prefix}*{suffix}")))
    }

leave_button_imgs = load_images_from_path(OPENCLOSECHAT_PATH, "leave_chat_")
Join_Chat_imgs = load_images_from_path(OPENCLOSECHAT_PATH, "join_chat_")

regionOpenChat = (59, 250, 103, 172)

def closeChat():
    found = False
    count = 0
    time.sleep(1)
    while not found and count < 10:
        for _, image_path in Join_Chat_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.85)
            count += 1
            if location:
                time.sleep(1)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                time.sleep(1)
                return True
    return False


def thereAreMessages():
    found = False
    count = 0
    while not found and count < 10:
        for _, image_path in Join_Chat_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95, region=regionOpenChat)
            count += 1
            time.sleep(0.5)
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                time.sleep(1)
                return found
    return found