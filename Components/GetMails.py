import pyautogui
pyautogui.useImageNotFoundException(False)
import sys
from pathlib import Path
from time import sleep

MESSAGES_PATH = "Images/Messages"

max_count = 5

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path

mailButton_imgs = load_images_from_path(MESSAGES_PATH, "areThereMessages_")
isThereAMessage_imgs = load_images_from_path(MESSAGES_PATH, "isThereAMessage_")
getMessageReward_imgs = load_images_from_path(MESSAGES_PATH, "getMessageReward_")

def getMessageReward():
    count = 0
    while count < max_count:
        for _, image_path in getMessageReward_imgs.items():
            location = pyautogui.locateOnScreen(
                image_path, confidence=0.9)
            count += 1
            if location:
                sleep(1)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
    return False

def isThereAMessage():
    count = 0
    while count < max_count:
        for _, image_path in isThereAMessage_imgs.items():
            location = pyautogui.locateOnScreen(
                image_path, confidence=0.9)
            count += 1
            if location:
                sleep(1)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
    return False

def get_mail_button():
    count = 0
    while count < max_count:
        for _, image_path in mailButton_imgs.items():
            location = pyautogui.locateOnScreen(
                image_path, confidence=0.9)
            count += 1
            if location:
                sleep(1)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
    return False

def main_get_mails():
    get_mail_button()
    isThereAMessage()
    getMessageReward()
    return True