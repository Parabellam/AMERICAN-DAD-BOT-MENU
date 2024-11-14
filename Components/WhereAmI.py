import pyautogui
from time import sleep
from Components.LoadImages import load_images_from_path

pyautogui.useImageNotFoundException(False)

MM_PATH = "Images\MananaMimosaEvent"
MM_FINISH_PATH = "Images\MananaMimosaEvent\Fight"
MAP_PATH = "Images\Home"  # Si veo home button es porque estoy en el mapa
HOME_PATH = "Images\MapButton"  # Si veo map button es porque estoy en casa

button_go_map_imgs = load_images_from_path(HOME_PATH, "map_btn_")
button_go_home_imgs = load_images_from_path(MAP_PATH, "home_")
event_no_running_imgs = load_images_from_path(MM_PATH, "EventNoRunning_")
event_finish_imgs = load_images_from_path(MM_FINISH_PATH, "FinishEvent_")

BS_window_imgs_region = (706, 38, 442, 197)
open_app_imgs_region = (817, 176, 292, 173)
CONFIDENCE_LEVEL = 0.9
MAX_COUNT = 10

def check_images(images_dict, return_str):
    for attempt in range(MAX_COUNT):
        for _, image_path in images_dict.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
            if location:
                return return_str
        sleep(0.5)  # Espera un breve periodo antes del siguiente intento
    return False

def checks():
    checks_to_perform = [
        (event_no_running_imgs, "at_outside_event"),
        (event_finish_imgs, "at_inside_event"),
        (button_go_home_imgs, "at_map"),
        (button_go_map_imgs, "at_home"),
    ]
    
    for images, state in checks_to_perform:
        result = check_images(images, state)
        if result:
            return result
    return False

def main_where_am_i():
    return checks()