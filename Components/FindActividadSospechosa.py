import os
import pyautogui

ACTIVIDAD_SOSPECHOSA_PATH = "Images/Errors"

actividad_sospechosa_imgs = {
    "img1": os.path.join(ACTIVIDAD_SOSPECHOSA_PATH, "actividad_sospechosa_1.png"),
}


def isActividadSospechosa():
    count = 0
    while count < 25:
        for _, image_path in actividad_sospechosa_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.9)
            count += 1
            if location:
                print("Se ha detectado una actividad sospechosa.")
                return True
    return False
