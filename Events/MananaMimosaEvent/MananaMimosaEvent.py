# Events/MananaMimosaEvent/MananaMimosaEvent.py
import os
import sys
from pathlib import Path
import time
import pyautogui
pyautogui.FAILSAFE = False
import numpy as np
import cv2
import msvcrt
import random
from glob import glob

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components._GlobalOpenValidateJoin import open_validate_join
from Components.FindActividadSospechosa import isActividadSospechosa
from Components.RandomActivities import find_random_activity
from ManageJSON.ManageJSONFile import get_value_from_json

from Events.MananaMimosaEvent.ConfirmAndFight import confirm_and_fight
from Events.RickySpanishIslandEvent.RickySpanishIslandEvent import chatEvent

MANANAMIMOSAEVENT_PATH = "Images/MananaMimosaEvent"
HAPPINESS_PATH = "Images/Happiness"
GLOBAL_PATH = "Images/Global"
HOME_PATH = "Images/Home"

def load_images_from_path(path, prefix, suffix=".png"):
    return {
        f"img{index+1}": file
        for index, file in enumerate(glob(os.path.join(path, f"{prefix}*{suffix}")))
    }

MananaMimosa_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "MananaMimosaEvent_")
EventNoRunning_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "EventNoRunning_")
useFood_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "useFood_")
LeaveEvent_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "LeaveEvent_")
useTickets_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "useTickets_")
participar_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "participar_")
loading_game_imgs = load_images_from_path(GLOBAL_PATH, "loading_game_")
isOut_imgs = load_images_from_path(GLOBAL_PATH, "isOut_")
home_imgs = load_images_from_path(HOME_PATH, "home_")

happiness_imgs = {
    "img1": os.path.join(HAPPINESS_PATH, "1.png"),
    "img2": os.path.join(HAPPINESS_PATH, "2.png"),
    "img3": os.path.join(HAPPINESS_PATH, "3.png"),
    "img4": os.path.join(HAPPINESS_PATH, "4.png"),
    "img5": os.path.join(HAPPINESS_PATH, "5.png"),
    "img6": os.path.join(HAPPINESS_PATH, "6.png"),
    "img7": os.path.join(HAPPINESS_PATH, "7.png"),
    "img8": os.path.join(HAPPINESS_PATH, "8.png"),
}

max_attempts = 10

def open_event():
    time.sleep(1)
    pyautogui.click(1096, 180)
    return True

def isEventRuning():
    time.sleep(2)
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in EventNoRunning_imgs.items():
            locationNoRunning = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if locationNoRunning:
                found = True
                return "No running"
        # if(found==False):
        #     for _, image_path in EventRunning_imgs.items():
        #         locationRunning = pyautogui.locateOnScreen(image_path, confidence=0.95)
        #         count += 1
        #         if locationRunning:
        #             found = True
        #             return "Running"
    return False


def preprocess_image(img):
    # Convertir a escala de grises
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    
    # Aplicar umbralización para mejorar el contraste
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Opcional: Aplicar dilatación y erosión para mejorar la forma de los dígitos
    kernel = np.ones((1, 1), np.uint8)
    img_dilated = cv2.dilate(thresh, kernel, iterations=1)
    img_eroded = cv2.erode(img_dilated, kernel, iterations=1)
    return img_eroded

def find_number_food(reader):
    time.sleep(3)
    # Definir y capturar la región de interés
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = 353, 141, 466, 166
    img = pyautogui.screenshot(region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))
    
    # Preprocesar la imagen
    processed_img = preprocess_image(img)
    
    # Guardar la imagen procesada para inspección (opcional)
    cv2.imwrite('processed_image.png', processed_img)
    
    # Usar EasyOCR para extraer texto
    result = reader.readtext(processed_img, allowlist='0123456789')
    
    # Extraer y imprimir los resultados
    numbers = [text[1] for text in result if text[1].isdigit()]
    return numbers

def use_tickets_option():
    pyautogui.click(484, 252)
    return True

def use_food_option():
    pyautogui.click(259, 254)
    return True


def participar_button():
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in participar_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                time.sleep(1)
                return found
    return found


def validate_open_event():
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in EventNoRunning_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            found = True
            if location:
                return found
    return found


def isLoadingGame():
    time.sleep(10)
    count = 0
    failCount = 0
    while count < 25 and failCount < 200:
        for _, image_path in loading_game_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.9)
            if location:
                time.sleep(10)
                failCount += 1
            else:
                count += 1
    if (count > 23):
        return True
    if (failCount > 198):
        return False


def get_happiness():
    count = 0
    while count < 20:
        for _, image_path in happiness_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)


def another_tasks():
    respChatEvent = chatEvent()
    if(respChatEvent):
        get_happiness()
    else:
        print("No se logró abrir el chat.")

def isOut():
    count = 0
    while count < 20:
        for _, image_path in isOut_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
    return False


def validate_screen():
    isOutResp = isOut()
    if(isOutResp == True):
        pyautogui.click(909, 94) # Entra al juego
    else:
        print("NO hemos conseguido entrar al juego o ya estamos dentro del juego")


def leaveEventButton():
    count = 0
    while count < 20:
        for _, image_path in LeaveEvent_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
    return False


def goHome():
    count = 0
    while count < 20:
        for _, image_path in home_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
    return False


def function_join_mananamimosa(root, isThereRewards):
    resp1=open_validate_join()
    if(resp1.get("state")==True):
        while True:
            resp2 = open_event()
            validate = validate_open_event()
            if validate==True:
                break
    else:
        return print(resp1)
    if(resp2):
        resp3 = isEventRuning()
        if(resp3=="Running"):
            print("Función de torneo en progreso no disponible.")
            return print("Por favor espera a que termine el torneo y ejecuta de nuevo este evento.")
        if(resp3==False):
            return print("No hemos conseguido detectar el menú principal del evento ni el torneo en progreso, inicia de nuevo el proceso.")
        else:
            restart = 1
            while True:
                respActividadSospechosa = isActividadSospechosa()
                if(respActividadSospechosa == True):
                    root.destroy()
                    return respActividadSospechosa
                if msvcrt.kbhit():
                    if msvcrt.getch().decode('utf-8').lower() == 'q':
                        print("Interrupción por usuario. Terminando...")
                        break

                current_food_list = find_number_food(resp1.get("reader"))
                if current_food_list:
                    current_food = int(current_food_list[0])
                else:
                    current_food_list = find_number_food(resp1.get("reader"))
                    if(current_food_list):
                        current_food = int(current_food_list[0])
                    else:
                        current_food = 0

                max_food = get_value_from_json("q6w5f4weg54er584")

                # Asegúrate de que max_food sea un entero
                if isinstance(max_food, list) and len(max_food) == 1:
                    max_food = int(max_food[0])
                elif isinstance(max_food, str):
                    max_food = int(max_food)

                average = max_food * 0.5
                respA = False
                respB = False
                if current_food > average:
                    # print("Tu comida actual SÍ supera el 50 por ciento de capacidad, USANDO COMIDA para el torneo.")
                    respA = use_food_option()
                    time.sleep(2)
                else:
                    # print("Tu comida actual NO supera el 50 por ciento de capacidad, USANDO TICKETS para el torneo.")
                    respB = use_tickets_option()
                    time.sleep(2)

                if respA == True or respB == True:
                    isParticipantPressed = participar_button()
                    if isParticipantPressed == True:
                        isFightDone = confirm_and_fight(resp1.get("reader"), isThereRewards)
                        time.sleep(5)
                        restart += 1
                        # random_value = random.choice([2, 3, 4])
                        # if restart % random_value == 0:
                        #     # isLeaveEvent = leaveEventButton()
                        #     # if(isLeaveEvent == True):
                        #     #     isHome = goHome()
                        #     #     if(isHome):
                        #     #         find_random_activity()
                        #     #     else:
                        #     #         print("No se ha encontrado el botón de casa")
                        #     # else:
                        #     #     print("No se ha logrado salir del evento")
                            
                            
                            
                            
                        #     pyautogui.click(1348, 704)
                        #     time.sleep(10)
                        #     pyautogui.click(909, 94) # Borrar todas las aplicaciones abiertas
                        #     time.sleep(120)
                        #     time.sleep(120)
                        #     time.sleep(120)
                        #     time.sleep(random.uniform(120, 240))
                        #     time.sleep(random.uniform(120, 240))
                        #     time.sleep(120)
                        #     time.sleep(120)
                        #     time.sleep(120)
                        #     pyautogui.click(950, 227) # Entra al juego
                        #     time.sleep(3)
                        #     pyautogui.click(950, 227) # Entra al juego
                        #     loadDone = isLoadingGame()
                        #     if(loadDone==True):
                        #         pyautogui.click(137, 657)
                        #         time.sleep(7)
                        #         pyautogui.click(1100, 186)
                        #         time.sleep(7)
                        #         # another_tasks()
                        #     else:
                        #         # validate_screen()
                        #         print("Error al cargar el juego")
                    else:
                        print("No hemos podido encontrar el botón de participar.")
                else:
                    print("No se ha encontrado el botón para ingresar al evento.")
    else:
        return print("No se ha conseguido abrir el evento.")