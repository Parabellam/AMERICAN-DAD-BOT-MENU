import pyautogui
from time import sleep
import sys
from pathlib import Path

HOME_PATH = "Images/Home"

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path
from Components.FindActividadSospechosa import isActividadSospechosa

leave_home_msg_imgs = load_images_from_path(HOME_PATH, "leave_home_msg_")
leave_home_msg_region = (368, 187, 598, 378)

def validate_home(images, confidence):
    for _, image_path in images.items():
        location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=leave_home_msg_region)
        if location:
            print("Home encontrada XXXXXXXXX, terminando el bucle.")
            pyautogui.press('esc')
            return True
    return False

def main_get_home():
    isActividadSospechosa()
    sleep(2)
    for _ in range(30):
        pyautogui.press('esc')
        sleep(1.5)
        if validate_home(leave_home_msg_imgs, confidence=0.9):
            print("Home encontrada, terminando el bucle.")
            return True
    isActividadSospechosa()
    print("Imagen no encontrada después de 30 intentos.")
    return False