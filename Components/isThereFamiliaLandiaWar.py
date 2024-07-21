import pyautogui
import sys
from pathlib import Path

GUERRA_FAMILIALANDIA_PATH = "Images/GuerraFamilialandia"

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path

is_there_familialamdia_war_imgs = load_images_from_path(GUERRA_FAMILIALANDIA_PATH, "is_there_familialandia_war_")

left = 166
top = 590
width = 335 - 166
height = 717 - 590
region = (left, top, width, height)


def main_is_there_familialandia_war():
    count = 0
    while count < 20:
        for _, image_path in is_there_familialamdia_war_imgs.items():
            location = pyautogui.locateOnScreen(
                image_path, region=region, confidence=0.95)
            count += 1
            if location:
                return True
    return False
