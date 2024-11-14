import pyautogui
pyautogui.useImageNotFoundException(False)
import sys
from pathlib import Path
from time import sleep

GUERRA_FAMILIALANDIA_PATH = "Images/GuerraFamilialandia"
GUERRA_FAMILIALANDIA_SPOTS_PATH = "Images/GuerraFamilialandia/spots"

max_count = 5

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.LoadImages import load_images_from_path

am_i_inside_imgs = load_images_from_path(GUERRA_FAMILIALANDIA_PATH, "verify_map_spots_")
spots_imgs = load_images_from_path(GUERRA_FAMILIALANDIA_SPOTS_PATH, "a_")
cant_deploy__imgs = load_images_from_path(GUERRA_FAMILIALANDIA_PATH, "cant_deploy_")
deploy_button_imgs = load_images_from_path(GUERRA_FAMILIALANDIA_PATH, "deploy_team_button_")
add_roger_imgs = load_images_from_path(GUERRA_FAMILIALANDIA_PATH, "add_roger_")
deploy_in_map_button_imgs = load_images_from_path(GUERRA_FAMILIALANDIA_PATH, "deploy_in_map_")

original_imgs = spots_imgs

def verify_inside():
    count = 0
    sleep(1)
    while count < max_count:
        for _, image_path in am_i_inside_imgs.items():
            location = pyautogui.locateOnScreen(
                image_path, confidence=0.95)
            count += 1
            if location:
                return True
    return False

def can_i_deploy_in_this_spot():
    count = 0
    while count < max_count:
        for _, image_path in cant_deploy__imgs.items():
            location = pyautogui.locateOnScreen(
                image_path, confidence=0.95)
            count += 1
            if location:
                return False
    return True

def open_spot():
    global spots_imgs  # Para modificar el diccionario global
    count = 0
    while count < max_count:
        for key, image_path in list(spots_imgs.items()):  # Iterar sobre una lista de ítems
            location = pyautogui.locateOnScreen(image_path, confidence=0.9)
            count += 1
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                sleep(1)
                resp = can_i_deploy_in_this_spot()
                if resp:
                    print("Se puede desplegar...")
                    sleep(1)
                    return True
                else:
                    print(f"No puedes desplegar en este spot: {key}. Descartando imagen.")
                    # Eliminar imagen del diccionario
                    del spots_imgs[key]
                    return "Cant"
    print("No se encontró ningún punto de despliegue. Revisar.")
    return False

def deploy_team():
    count = 0
    scroll = 0
    print("Buscando botón de desplegar equipo")
    sleep(2)
    while count < max_count:
        for _, image_path in deploy_button_imgs.items():
            location = pyautogui.locateOnScreen(
                image_path, confidence=0.85)
            count += 1
            if location:
                print("Se ha encontrado Botón Desplegar Equipo")
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                sleep(2)
                return True
            elif(scroll <= 2):
                scroll += 1
                sleep(1)
                pyautogui.mouseDown(1031, 500)
                sleep(0.5)
                pyautogui.moveTo(1030, 128, duration=2)
                sleep(1)
                pyautogui.mouseUp()
                sleep(0.5)
    print("NO se ha encontrado Botón Desplegar Equipo")
    return False

def deploy_in_map_button():
    count = 0
    while count < max_count:
        for _, image_path in deploy_in_map_button_imgs.items():
            location = pyautogui.locateOnScreen(
                image_path, confidence=0.9)
            count += 1
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                sleep(1)
                return True
    return False

def move_carroussel():
    sleep(1)
    pyautogui.mouseDown(850, 336)
    sleep(0.7)
    pyautogui.moveTo(297, 336, duration=2)
    sleep(0.5)
    pyautogui.mouseUp()
    sleep(2)
    return

def add_roger():
    count = 0
    move_carroussel()
    while count < max_count:
        for _, image_path in add_roger_imgs.items():
            location = pyautogui.locateOnScreen(
                image_path, confidence=0.9)
            count += 1
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.mouseDown(317, 468)
                sleep(0.7)
                pyautogui.moveTo(center_x, center_y, duration=2.5)
                sleep(1)
                pyautogui.mouseUp()
                sleep(1)
            elif count == 5:
                resp = deploy_in_map_button()
                if(resp==True):
                    return True
    resp = deploy_in_map_button()
    if(resp==True):
        return True
    return False

def main_familialandia_flow():
    global spots_imgs
    resp = verify_inside()
    if(resp==True):
        finding_spot = True
        spots_imgs = original_imgs
        while finding_spot==True:
            resp = open_spot()
            if(resp=="Cant"):
                pyautogui.press('esc')
            else:
                finding_spot==False
                sleep(1)
                break
        print("Antes de")
        if(resp==True):
            print("Despues de ")
            resp = deploy_team()
            if(resp==True):
                resp = add_roger()
                if(resp==True):
                    print("Ahora estamos participando en la guerra.")
                    return True
            else:
                return False
        else:
            return False
    else:
        print("No mapa de guerra")
        return False