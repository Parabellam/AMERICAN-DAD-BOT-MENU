from time import sleep
import pyautogui
pyautogui.useImageNotFoundException(False)
pyautogui.FAILSAFE = False

OPENCLOSECHAT_PATH = "Images/Chat/getButtonEvents"

from Components.LoadImages import load_images_from_path

get_reward_button_imgs = load_images_from_path(OPENCLOSECHAT_PATH, "get_button_")

def getButtons():
    found = False
    count = 0
    sleep(1)
    while not found and count < 10:
        for _, image_path in get_reward_button_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.85)
            count += 1
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                sleep(3)
                pyautogui.click(365, 687)
                sleep(1)