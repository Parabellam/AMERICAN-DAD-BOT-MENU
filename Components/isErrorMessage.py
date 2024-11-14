import pyautogui
pyautogui.useImageNotFoundException(False)
import sys
from pathlib import Path
import concurrent.futures
from time import sleep

ERRORS_PATH = "Images/Errors"
WINDOW_PATH = "Images/BlueStacks"

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path
from Components.GetHomeScreen import main_get_home
from Components.JoinMap import open_main_map
from Components.MananaMimosa.ValidateOpenEvent import open_event
from Components.MananaMimosa.ValidateOpenEvent import validate_open_event
from TelegramLogs import custom_print

wifi_error_imgs = load_images_from_path(ERRORS_PATH, "wifi_error_")
wifi_error_button_imgs = load_images_from_path(ERRORS_PATH, "wifi_error_button_")
casa_vulnerable_imgs = load_images_from_path(ERRORS_PATH, "casa_vulnerable_")
atacando_casa_reload_button_imgs = load_images_from_path(ERRORS_PATH, "atacando_casa_reload_button_")
another_sessions_imgs = load_images_from_path(ERRORS_PATH, "another_sessions_button_")
afk_imgs = load_images_from_path(ERRORS_PATH, "afk_button_")
BS_window_imgs = load_images_from_path(WINDOW_PATH, "BS_window_")
open_app_imgs = load_images_from_path(WINDOW_PATH, "open_app_")
wait_app_imgs = load_images_from_path(WINDOW_PATH, "wait_app_")

resolve_afk_error_region = (527, 435, 266, 113)
resolve_another_sessions_error_region = (544, 432, 240, 113)
resolve_atacando_casa_error_region = (530, 526, 283, 132)
resolve_casa_vulnerable_error_region = (431, 375, 533, 264)
resolve_wifi_error_region = (431, 375, 533, 264)
BS_window_imgs_region = (706, 38, 442, 197)
open_app_imgs_region = (817, 176, 292, 173)
CONFIDENCE_LEVEL = 0.9

def open_event_flow():
    open_main_map()
    open_event()
    validate_open_event()
    custom_print("Se abrío todo correctamente", False)
    return True

def wait_app():
    count = 0
    failCount = 0
    custom_print("Haciendo wait_app", False)
    sleep(60)
    while count < 20 and failCount < 50:
        for _, image_path in wait_app_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
            if location:
                count = 0
                failCount += 1
                sleep(10)
                if(failCount >= 50):
                    custom_print("Error al cargar el juego nuevamente.", False)
                    # close_app() esto puede generar bucle infinito
            else:
                count += 1
                sleep(0.3)
                if(count >= 20):
                    custom_print("Haciendo main_get_home asdf", False)
                    sleep(7)
                    main_get_home()
                    return
    custom_print("Last return wait_app", False)
    return

def open_app():
    count = 0
    sleep(3)
    while count < 20:
        for _, image_path in open_app_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
            count += 1
            if location:
                sleep(4)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                wait_app()
                return True
    custom_print("No se ha encontrado la app", False)
    return False

def close_app():
    custom_print("Haciendo close_app", False)
    count = 0
    while count < 20:
        for _, image_path in BS_window_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL, region=BS_window_imgs_region)
            count += 1
            if location:
                sleep(3)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                open_app()
                open_event_flow()
                return True
    custom_print("No se ha encontrado cerrar ventana", False)
    return False

def locate_and_click(image_path, region):
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL, region=region)
        if location:
            custom_print("Se ha localizado un error", False)
            pyautogui.click(1346, 701)
            close_app()
            return True
    except Exception as e:
        custom_print(f"Error al localizar la imagen: {str(e)}", False)
    return False

def locate_and_click_2(image_path):
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
        if location:
            center_x, center_y = pyautogui.center(location)
            pyautogui.click(center_x, center_y)
            return True
    except Exception as e:
        custom_print(f"_2 Error al localizar la imagen: {str(e)}", False)
    return False

def resolve_wifi_error():
    for image_path in wifi_error_button_imgs.values():
        if locate_and_click(image_path, resolve_wifi_error_region):
            custom_print("resolve_wifi_error", False)
            main_get_home()
            return True
    return False

def resolve_casa_vulnerable_error():
    for image_path in casa_vulnerable_imgs.values():
        locate_and_click_2(image_path, resolve_casa_vulnerable_error_region)
    return False

def resolve_atacando_casa_error():
    for image_path in atacando_casa_reload_button_imgs.values():
        if locate_and_click(image_path, resolve_atacando_casa_error_region):
            custom_print("resolve_atacando_casa_error", False)
            main_get_home()
            return True
    return False

def resolve_another_sessions_error():
    for image_path in another_sessions_imgs.values():
        if locate_and_click(image_path, resolve_another_sessions_error_region):
            custom_print("resolve_another_sessions_error", False)
            main_get_home()
            return True
    return False

def resolve_afk_error():
    for image_path in afk_imgs.values():
        if locate_and_click(image_path, resolve_afk_error_region):
            custom_print("resolve_afk_error", False)
            main_get_home()
            return True
    return False

error_images_functions = [
    (wifi_error_imgs, resolve_wifi_error, resolve_wifi_error_region),
    (casa_vulnerable_imgs, resolve_casa_vulnerable_error, resolve_casa_vulnerable_error_region),
    (atacando_casa_reload_button_imgs, resolve_atacando_casa_error, resolve_atacando_casa_error_region),
    (another_sessions_imgs, resolve_another_sessions_error, resolve_another_sessions_error_region),
    (afk_imgs, resolve_afk_error, resolve_afk_error_region),
]

def locate_and_resolve(images, resolve_function, region):
    try:
        for image_path in images.values():
            custom_print("Before locate_and_click", False)
            if locate_and_click(image_path, region):
                custom_print("After locate_and_click", False)
                return resolve_function()
            custom_print("After locate_and_resolve loop", False)
    except Exception as e:
        custom_print(f"Error en locate_and_resolve: {str(e)}", False)
    return False

def main_are_there_errors():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(locate_and_resolve, images, resolve_function, region) for images, resolve_function, region in error_images_functions]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result:
                    custom_print("TERMINA main_are_there_errors en True", False)
                    return True
            except Exception as e:
                custom_print(f"Excepción en el hilo: {str(e)}", False)
                # Manejo de la excepción si es necesario
    custom_print("TERMINA main_are_there_errors en False", False)
    return False