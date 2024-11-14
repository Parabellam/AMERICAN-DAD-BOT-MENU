import pyautogui
pyautogui.useImageNotFoundException(False)
from time import sleep
import sys
from pathlib import Path

HOME_PATH = "Images/Home"
GLOBAL_PATH = "Images/Global"

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path
from Components.FindActividadSospechosa import isActividadSospechosa
from TelegramLogs import custom_print

leave_home_msg_imgs = load_images_from_path(HOME_PATH, "leave_home_msg_")
leave_home_msg_region = (368, 187, 598, 378)
close_button_imgs = load_images_from_path(GLOBAL_PATH, "close_button_")

def validate_home(images, confidence):
    for _, image_path in images.items():
        location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=leave_home_msg_region)
        if location:
            pyautogui.press('esc')
            return True
    return False

def close_any_window():
    count = 0
    while count < 7:
        for _, image_path in close_button_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.9)
            count += 1
            if location:
                sleep(1)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return

def main_get_home():
    isActividadSospechosa()
    sleep(2)
    
    close_any_window()
    
    for _ in range(30):
        pyautogui.press('esc')
        sleep(2)
        if validate_home(leave_home_msg_imgs, confidence=0.9):
            return True
    isActividadSospechosa()
    pyautogui.click(77, 49)
    pyautogui.press('esc')
    pyautogui.click(77, 49)
    pyautogui.press('esc')
    
    close_any_window()
    
    for _ in range(10):
        pyautogui.press('esc')
        sleep(2)
        if validate_home(leave_home_msg_imgs, confidence=0.9):
            return True
    custom_print("Imagen no encontrada después de 10 intentos más.", False)
    return False