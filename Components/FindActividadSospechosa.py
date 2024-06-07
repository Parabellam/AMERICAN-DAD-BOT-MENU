import os
import pyautogui
import pygame
import time

ACTIVIDAD_SOSPECHOSA_PATH = "Images/Errors"

actividad_sospechosa_imgs = {
    "img1": os.path.join(ACTIVIDAD_SOSPECHOSA_PATH, "actividad_sospechosa_1.png"),
}


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
                print("Se ha detectado una actividad sospechosa.")
                for _ in range(5):
                    play_alert_sound()
                    time.sleep(10)
                return True
    return False
