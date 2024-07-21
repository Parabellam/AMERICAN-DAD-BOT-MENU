import pyautogui
import sys
from pathlib import Path
import concurrent.futures

ERRORS_PATH = "Images/Errors"

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path

wifi_error_imgs = load_images_from_path(ERRORS_PATH, "wifi_error_")
wifi_error_button_imgs = load_images_from_path(ERRORS_PATH, "wifi_error_button_")
casa_vulnerable_imgs = load_images_from_path(ERRORS_PATH, "casa_vulnerable_")
atacando_casa_reload_button_imgs = load_images_from_path(ERRORS_PATH, "atacando_casa_reload_button_")
another_sessions_imgs = load_images_from_path(ERRORS_PATH, "another_sessions_button_")
afk_imgs = load_images_from_path(ERRORS_PATH, "afk_button_")

left = 248
top = 100
right = 1122
bottom = 642

width = right - left
height = bottom - top

region = (left, top, width, height)


def resolve_wifi_error():
    for _, image_path in wifi_error_button_imgs.items():
        location = pyautogui.locateOnScreen(
            image_path, confidence=0.95, region=region)
        if location:
            center_x, center_y = pyautogui.center(location)
            pyautogui.click(center_x, center_y)
            return True
    return False


def resolve_casa_vulnerable_error():
    for _, image_path in casa_vulnerable_imgs.items():
        location = pyautogui.locateOnScreen(
            image_path, confidence=0.95, region=region)
        if location:
            center_x, center_y = pyautogui.center(location)
            pyautogui.click(center_x, center_y)
            return True
    return False


def resolve_atacando_casa_error():
    for _, image_path in atacando_casa_reload_button_imgs.items():
        location = pyautogui.locateOnScreen(
            image_path, confidence=0.95, region=region)
        if location:
            center_x, center_y = pyautogui.center(location)
            pyautogui.click(center_x, center_y)
            return True
    return False


def resolve_another_sessions_error():
    for _, image_path in another_sessions_imgs.items():
        location = pyautogui.locateOnScreen(
            image_path, confidence=0.95, region=region)
        if location:
            center_x, center_y = pyautogui.center(location)
            pyautogui.click(center_x, center_y)
            return True
    return False


def resolve_afk_error():
    for _, image_path in afk_imgs.items():
        location = pyautogui.locateOnScreen(
            image_path, confidence=0.95, region=region)
        if location:
            center_x, center_y = pyautogui.center(location)
            pyautogui.click(center_x, center_y)
            return True
    return False


error_images_functions = [
    (wifi_error_imgs, resolve_wifi_error),
    (casa_vulnerable_imgs, resolve_casa_vulnerable_error),
    (atacando_casa_reload_button_imgs, resolve_atacando_casa_error),
    (another_sessions_imgs, resolve_another_sessions_error),
    (afk_imgs, resolve_afk_error),
]


def locate_and_resolve(images, resolve_function):
    for _ in range(10):
        for _, image_path in images.items():
            location = pyautogui.locateOnScreen(
                image_path, confidence=0.95, region=region)
            if location:
                resolve_function()
                print("BIEN 2")
                return True
    print("NADA 2")
    return False


def main_are_there_errors():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_error = {executor.submit(locate_and_resolve, images, resolve_function): (
            images, resolve_function) for images, resolve_function in error_images_functions}
        for future in concurrent.futures.as_completed(future_to_error):
            if future.result():
                print("BIEN 1")
                return True
    print("NADA 1")
    return False

main_are_there_errors()