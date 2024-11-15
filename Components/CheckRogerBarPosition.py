import pyautogui
pyautogui.useImageNotFoundException(False)

from Components.LoadImages import load_images_from_path
from TelegramLogs import custom_print

HOME_PATH = "Images/Home"

muro_izquierdo_imgs = load_images_from_path(HOME_PATH, "muro_izquierdo_")
muro_izquierdo_region = (43, 293, 309, 392)

def check_roger_bar_position():
    count = 0
    while count < 20:
        for _, image_path in muro_izquierdo_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.9, region=muro_izquierdo_region)
            count += 1
            if location:
                return True
    custom_print("No se logró detectar la posición en el bar de Roger", False)
    return False
