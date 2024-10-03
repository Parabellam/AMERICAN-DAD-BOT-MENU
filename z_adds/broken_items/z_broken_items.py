import pyautogui
pyautogui.useImageNotFoundException(False)
from glob import glob
import os
from time import sleep
from PIL import Image
from pynput import keyboard

# Variables globales para controlar el estado del script
is_paused = False
is_running = True

def load_images_from_path(path, prefix, suffix=".png"):
    # Cargar y convertir imágenes a escala de grises
    images = {}
    for index, file in enumerate(glob(os.path.join(path, f"{prefix}*{suffix}"))):
        img = Image.open(file).convert('L')  # Convertir a escala de grises
        images[f"img{index+1}"] = img
    return images

IMGS_PATH = "z_adds/broken_items/no_selected"

no_selected_imgs = load_images_from_path(IMGS_PATH, "a_")
region = (159, 150, 1126, 563)
pyautogui_region = (region[0], region[1], region[2] - region[0], region[3] - region[1])
last_try = True
resp = True

def select_item():
    global last_try
    failCount = 0
    scroll = False
    while failCount < 50:
        for _, image in no_selected_imgs.items():
            # Guardar la imagen en escala de grises temporalmente
            image.save('temp_image.png')
            location = pyautogui.locateOnScreen('temp_image.png', confidence=0.7, region=pyautogui_region, grayscale=False)
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                sleep(0.5)
                last_try = True
                os.remove('temp_image.png')  # Eliminar la imagen temporal
                return True
            else:
                failCount += 1
                if failCount >= 49 and last_try and not scroll:
                    last_try = False
                    scroll = True
                    pyautogui.mouseDown(x=642, y=530)
                    pyautogui.move(0, -290, duration=0.7)
                    pyautogui.mouseUp()
                    sleep(0.2)
                    os.remove('temp_image.png')  # Eliminar la imagen temporal
                    return True
        os.remove('temp_image.png')  # Eliminar la imagen temporal
    return False

def on_press(key):
    global is_paused, is_running
    try:
        if key.char == 'p':
            # Pausar o reanudar el script
            is_paused = not is_paused
            print("Pausado" if is_paused else "Reanudado")
        elif key.char == '|':
            # Detener el script
            is_running = False
            print("Script detenido")
            return False  # Detiene el listener de teclas
    except AttributeError:
        pass

def main():
    global resp
    while is_running:
        while is_paused:
            sleep(0.1)  # Esperar mientras está en pausa
        if is_running:
            resp = select_item()
        else:
            break

# Listener de teclado en segundo plano
listener = keyboard.Listener(on_press=on_press)
listener.start()

main()
listener.join()  # Esperar a que el listener termine antes de salir del script