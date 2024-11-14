import pyautogui
pyautogui.useImageNotFoundException(False)
from time import sleep

ERRORS_PATH = "Images/Errors"
WINDOW_PATH = "Images/BlueStacks"

from Components.LoadImages import load_images_from_path
from Components.GetHomeScreen import main_get_home
from TelegramLogs import custom_print

BS_window_imgs = load_images_from_path(WINDOW_PATH, "BS_window_")
open_app_imgs = load_images_from_path(WINDOW_PATH, "open_app_")
wait_app_imgs = load_images_from_path(WINDOW_PATH, "wait_app_")

BS_window_imgs_region = (706, 38, 442, 197)
open_app_imgs_region = (817, 176, 292, 173)
CONFIDENCE_LEVEL = 0.9

def wait_app():
    count = 0
    failCount = 0
    sleep(60)
    custom_print("Haciendo wait_app 222", False)
    while count < 20 and failCount < 50:
        for _, image_path in wait_app_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
            if location:
                count = 0
                failCount += 1
                sleep(10)
                if(failCount >= 50):
                    custom_print("Error al cargar el juego nuevamente. 222", False)
                    close_app()
            else:
                count += 1
                sleep(0.3)
                if(count >= 20):
                    custom_print("Haciendo main_get_home asdf 222", False)
                    sleep(7)
                    main_get_home()
                    return
    custom_print("Last return wait_app 222", False)
    return

def open_app():
    count = 0
    sleep(3)
    while count < 20:
        for _, image_path in open_app_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
            count += 1
            if location:
                sleep(3)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                wait_app()
                return True
    custom_print("No se ha encontrado la app 222", False)
    return False

def close_app():
    custom_print("Haciendo close_app 222", False)
    count = 0
    while count < 20:
        for _, image_path in BS_window_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL, region=BS_window_imgs_region)
            count += 1
            if location:
                sleep(1)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                open_app()
                return True
    custom_print("No se ha encontrado cerrar ventana 222", False)
    return False

def main_restart_game():
    pyautogui.click(1349, 705)
    close_app()