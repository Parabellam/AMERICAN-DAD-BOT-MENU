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

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components._GlobalOpenValidateJoin import open_validate_join
from ManageJSON.ManageJSONFile import get_value_from_json

from Events.MananaMimosaEvent.ConfirmAndFight import confirm_and_fight

MANANAMIMOSAEVENT_PATH = "Images/MananaMimosaEvent"

MananaMimosa_imgs = {
    "img1": os.path.join(MANANAMIMOSAEVENT_PATH, "MananaMimosaEvent_1.png"),
    "img2": os.path.join(MANANAMIMOSAEVENT_PATH, "MananaMimosaEvent_2.png"),
    "img3": os.path.join(MANANAMIMOSAEVENT_PATH, "MananaMimosaEvent_3.png"),
    "img4": os.path.join(MANANAMIMOSAEVENT_PATH, "MananaMimosaEvent_4.png"),
    "img5": os.path.join(MANANAMIMOSAEVENT_PATH, "MananaMimosaEvent_5.png"),
}

Cake_imgs = {
    "img1": os.path.join(MANANAMIMOSAEVENT_PATH, "cake_1.png"),
    "img2": os.path.join(MANANAMIMOSAEVENT_PATH, "cake_2.png"),
    "img3": os.path.join(MANANAMIMOSAEVENT_PATH, "cake_3.png"),
}

EventNoRunning_imgs = {
    "img1": os.path.join(MANANAMIMOSAEVENT_PATH, "EventNoRunning_1.png"),
    "img2": os.path.join(MANANAMIMOSAEVENT_PATH, "EventNoRunning_2.png"),
    "img3": os.path.join(MANANAMIMOSAEVENT_PATH, "EventNoRunning_2.png"),
}

useFood_imgs = {
    "img1": os.path.join(MANANAMIMOSAEVENT_PATH, "useFood_1.png"),
    "img2": os.path.join(MANANAMIMOSAEVENT_PATH, "useFood_2.png"),
    "img3": os.path.join(MANANAMIMOSAEVENT_PATH, "useFood_3.png"),
    "img4": os.path.join(MANANAMIMOSAEVENT_PATH, "useFood_4.png"),
}

useTickets_imgs = {
    "img1": os.path.join(MANANAMIMOSAEVENT_PATH, "useTickets_1.png"),
    "img2": os.path.join(MANANAMIMOSAEVENT_PATH, "useTickets_2.png"),
    "img3": os.path.join(MANANAMIMOSAEVENT_PATH, "useTickets_3.png"),
    "img4": os.path.join(MANANAMIMOSAEVENT_PATH, "useTickets_4.png"),
}

participar_imgs = {
    "img1": os.path.join(MANANAMIMOSAEVENT_PATH, "participar_1.png"),
    "img2": os.path.join(MANANAMIMOSAEVENT_PATH, "participar_2.png"),
    "img3": os.path.join(MANANAMIMOSAEVENT_PATH, "participar_3.png"),
}

max_attempts = 10

def open_event():
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in MananaMimosa_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
    return False

def isEventRuning():
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


def findCake():
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in Cake_imgs.items():
            locationCake = pyautogui.locateOnScreen(image_path, confidence=0.9)
            print(count)
            count += 1
            if locationCake:
                found = True
                return locationCake
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
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in useTickets_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return found
    return found

def use_food_option():
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in useFood_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return found
    return found


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


def function_join_mananamimosa():
    resp1=open_validate_join()
    if(resp1.get("state")==True):
        resp2 = open_event()
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
            while True:
                if msvcrt.kbhit():
                    if msvcrt.getch().decode('utf-8').lower() == 'q':
                        print("Interrupción por usuario. Terminando...")
                        break

                current_food_list = find_number_food(resp1.get("reader"))
                current_food = int(current_food_list[0])  # Convierte el primer elemento de la lista a entero

                max_food = get_value_from_json("q6w5f4weg54er584")

                # Asegúrate de que max_food sea un entero
                if isinstance(max_food, list) and len(max_food) == 1:
                    max_food = int(max_food[0])
                elif isinstance(max_food, str):
                    max_food = int(max_food)

                average = max_food * 0.5
                print("Comida actual: ", current_food, "| Capacidad máxima: ", max_food)
                if current_food > average:
                    print("Tu comida actual SÍ supera el 50 por ciento de capacidad, USANDO COMIDA para el torneo.")
                    respA = use_food_option()
                    time.sleep(2)
                else:
                    print("Tu comida actual NO supera el 50 por ciento de capacidad, USANDO TICKETS para el torneo.")
                    respB = use_tickets_option()
                    time.sleep(2)

                if respA == True or respB == True:
                    isParticipantPressed = participar_button()
                    if isParticipantPressed == True:
                        isFightDone = confirm_and_fight(resp1.get("reader"))
                        print("Esperando 5 segundos...")
                        time.sleep(5)
                    else:
                        print("No hemos podido encontrar el botón de participar.")
                else:
                    print("No se ha encontrado el botón para ingresar al evento.")
    else:
        return print("No se ha conseguido abrir el evento.")