from time import sleep
import pyautogui
pyautogui.FAILSAFE = False

OPENCLOSECHAT_PATH = "Images/Chat"
GETBUTTONSCHAT_PATH = "Images/Chat/getButtonEvents"

from Components.LoadImages import load_images_from_path

leave_button_imgs = load_images_from_path(OPENCLOSECHAT_PATH, "leave_chat_")
Join_Chat_imgs = load_images_from_path(OPENCLOSECHAT_PATH, "join_chat_")

regionOpenChat = (59, 250, 103, 172)

def closeChat():
    found = False
    count = 0
    sleep(1)
    while not found and count < 10:
        for _, image_path in Join_Chat_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.85)
            count += 1
            if location:
                sleep(1)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                sleep(1)
                return True
    return False


def thereAreMessages():
    found = False
    count = 0
    while not found and count < 10:
        for _, image_path in Join_Chat_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95, region=regionOpenChat)
            count += 1
            sleep(0.5)
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                sleep(1)
                return found
    return found