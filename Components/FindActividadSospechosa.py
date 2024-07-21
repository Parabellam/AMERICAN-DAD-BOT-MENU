import pyautogui
import pygame
import time
import sys
from pathlib import Path
pyautogui.FAILSAFE = False

ACTIVIDAD_SOSPECHOSA_PATH = "Images/Errors"

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path

actividad_sospechosa_imgs = load_images_from_path(ACTIVIDAD_SOSPECHOSA_PATH, "actividad_sospechosa_")

pygame.mixer.init()


def play_alert_sound():
    pygame.mixer.music.load("va_a_jugar_o_que.mp3")
    pygame.mixer.music.play()


def isActividadSospechosa():
    count = 0
    while count < 25:
        for _, image_path in actividad_sospechosa_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.9)
            count += 1
            if location:
                print("Se ha detectado una actividad sospechosa 1.")
                for _ in range(3):
                    play_alert_sound()
                    time.sleep(1)
                    print("Se ha detectado una actividad sospechosa 2.")
                    time.sleep(9)
                    print("Se ha detectado una actividad sospechosa 3.")
                    time.sleep(1)
                return True
    return False
