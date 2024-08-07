import time
import pyautogui
pyautogui.FAILSAFE = False
from glob import glob
import os

OPENCLOSECHAT_PATH = "Images/Chat"

from Components.LoadImages import load_images_from_path

Join_Chat_imgs = load_images_from_path(OPENCLOSECHAT_PATH, "join_chat_")

def getButtons():
    found = False
    count = 0
    time.sleep(1)
    while not found and count < 10:
        for _, image_path in Join_Chat_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.85)
            count += 1
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                time.sleep(3)