import pyautogui
from time import sleep

from Components.LoadImages import load_images_from_path

HAPPINESS_PATH = "Images/Happiness"

happiness_imgs = load_images_from_path(HAPPINESS_PATH, "h_")

def mainGetHappiness():
    count = 0
    while count < 3:
        count += 1
        for _, image_path in happiness_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.7)
            if location:
                sleep(0.5)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
    return True