# Events/MananaMimosaEvent/MananaMimosaEvent.py
import os
import sys
from pathlib import Path
import time
import pyautogui
pyautogui.FAILSAFE = False
import numpy as np
import cv2

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components._GlobalOpenValidateJoin import open_validate_join
from Components.FindActividadSospechosa import isActividadSospechosa
from Components.LoadImages import load_images_from_path
from Components.ReloadGame import reload_game_another_session
from ManageJSON.ManageJSONFile import get_value_from_json

from Events.MananaMimosaEvent.ConfirmAndFight import confirm_and_fight
from Components.CloseButton import close_button
from Components.CheckRogerBarPosition import check_roger_bar_position
from Components.GetHomeScreen import main_get_home_screen
from Components.isThereFamiliaLandiaWar import main_is_there_familialandia_war
from Components.MananaMimosa.ValidateOpenEvent import validate_open_event
from Components.MananaMimosa.ValidateOpenEvent import open_event
from Components.MananaMimosa.IsEventRunning import isEventRuning

from Components.isErrorMessage import main_are_there_errors

MANANAMIMOSAEVENT_PATH = "Images/MananaMimosaEvent"
MANANAMIMOSAEVENT_FIGHT_PATH = "Images/MananaMimosaEvent/Fight"
HAPPINESS_PATH = "Images/Happiness"
GLOBAL_PATH = "Images/Global"
HOME_PATH = "Images/Home"
ANOTHER_SESSION_BUTTON_PATH = "Images/Errors"


MananaMimosa_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "MananaMimosaEvent_")
useFood_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "useFood_")
LeaveEvent_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "LeaveEvent_")
useTickets_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "useTickets_")
participar_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "participar_")
loading_game_imgs = load_images_from_path(GLOBAL_PATH, "loading_game_")
isOut_imgs = load_images_from_path(GLOBAL_PATH, "isOut_")
home_imgs = load_images_from_path(HOME_PATH, "home_")
another_session_button_imgs = load_images_from_path(ANOTHER_SESSION_BUTTON_PATH, "another_session_button_")
no_recursos_imgs = load_images_from_path(ANOTHER_SESSION_BUTTON_PATH, "no_rsc_")
finish_event_imgs = load_images_from_path(MANANAMIMOSAEVENT_FIGHT_PATH, "FinishEvent_")

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
lastBattleFood = [0, 1, 2, 3]
lBFoodPosition = 0
SHORT_SLEEP = 1
CONFIDENCE_LEVEL = 0.9
CONFIDENCE_LEVEL_TWO = 0.95

def preprocess_image(img):
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    kernel = np.ones((1, 1), np.uint8)
    img_dilated = cv2.dilate(thresh, kernel, iterations=1)
    img_eroded = cv2.erode(img_dilated, kernel, iterations=1)
    return img_eroded

def find_number_food(reader):
    time.sleep(2)
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = 353, 141, 466, 166
    img = pyautogui.screenshot(region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))
    
    processed_img = preprocess_image(img)
    
    result = reader.readtext(processed_img, allowlist='0123456789')
    
    numbers = [text[1] for text in result if text[1].isdigit()]
    return numbers

def use_tickets_option():
    pyautogui.click(484, 252)
    return True

def use_food_option():
    pyautogui.click(259, 254)
    return True


def participar_button():
    for _ in range(20):
        for _, image_path in participar_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                time.sleep(SHORT_SLEEP)
                return True
    print("No se logró encontrar participar_button")
    return False


def isLoadingGame():
    time.sleep(10)
    count = 0
    failCount = 0
    while count < 25 and failCount < 200:
        for _, image_path in loading_game_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
            if location:
                time.sleep(10)
                failCount += 1
            else:
                count += 1
    if (count > 23):
        return True
    if (failCount > 198):
        return False


def isOut():
    for _ in range(20):
        for _, image_path in isOut_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
    return False


def validate_screen():
    isOutResp = isOut()
    if(isOutResp == True):
        pyautogui.click(909, 94)
    else:
        print("NO hemos conseguido entrar al juego o ya estamos dentro del juego")


def leaveEventButton():
    count = 0
    while count < 20:
        for _, image_path in LeaveEvent_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
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
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            count += 1
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
    return False


def areThereFoodAlert():
    count = 0
    while count < 20:
        for _, image_path in no_recursos_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
            count += 1
            if location:
                return False
    return True


def reload_game():
    reload_game_another_session()

def close_event_button():
    found = False
    count = 0
    while not found and count < 50:
        for _, image_path in finish_event_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            count += 1
            if location:
                time.sleep(SHORT_SLEEP)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                found=True
                time.sleep(4)
                return found
            else:
                time.sleep(5)
    return found

def get_current_food(resp_reader):
    for _ in range(3):
        current_food_list = find_number_food(resp_reader)
        if current_food_list:
            return int(current_food_list[0])
    return 0

def handle_errors_and_validate():
    if main_are_there_errors():
        open_validate_join(True)
        open_event()
        validate_open_event()
        return True
    return False


def function_join_mananamimosa(isThereRewards, isNightMode, isSaveMode):
    global lastBattleFood, lBFoodPosition
    resp1=open_validate_join()
    if(resp1.get("state")=="True"):
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
            battlesCount = 0
            repeat = True
            while True:
                battlesCount += 1
                respActividadSospechosa = isActividadSospechosa()
                if(respActividadSospechosa == True):
                    time.sleep(160)
                    reload_game()
                    open_event()
                    validate_open_event()
                if handle_errors_and_validate():
                    continue
                current_food = get_current_food(resp1.get("reader"))
                lastBattleFood[lBFoodPosition] = current_food
                if handle_errors_and_validate():
                    continue
                if all(x == lastBattleFood[0] for x in lastBattleFood):
                    print("La comida no está aumentando, resolviendo incidencia.")
                    close_button()
                    time.sleep(SHORT_SLEEP)
                    pyautogui.press('esc')
                    time.sleep(SHORT_SLEEP)
                    close_button()
                    if handle_errors_and_validate():
                        continue
                    barResp = check_roger_bar_position()
                    if barResp == False:
                        return
                    pyautogui.doubleClick(652, 474)
                    time.sleep(SHORT_SLEEP)
                    pyautogui.doubleClick(601, 467)
                    time.sleep(SHORT_SLEEP)
                    pyautogui.doubleClick(580, 470)
                    main_get_home_screen()
                    respCloseButton = close_button()
                    if respCloseButton == True:
                        time.sleep(SHORT_SLEEP)
                    main_are_there_errors()
                    open_validate_join()
                    open_event()
                    validate_open_event()
                elif (battlesCount > 6 and isNightMode == False):
                    main_get_home_screen()
                    main_are_there_errors()
                    reso = main_is_there_familialandia_war()
                    if(reso==True):
                        print("Guerra de Familialandia, Ingresa al juego. 2 Minutos.")
                        time.sleep(2)
                        print("Guerra de Familialandia, Ingresa al juego. 2 Minutos.")
                        time.sleep(2)
                        print("Guerra de Familialandia, Ingresa al juego. 2 Minutos.")
                        time.sleep(116)
                        reload_game()
                    main_are_there_errors()
                    open_validate_join(True)
                    open_event()
                    validate_open_event()
                    battlesCount = 0

                max_food = get_value_from_json("q6w5f4weg54er584")

                if isinstance(max_food, list) and len(max_food) == 1:
                    max_food = int(max_food[0])
                elif isinstance(max_food, str):
                    max_food = int(max_food)

                average = max_food * 0.5
                respA = False
                respB = False
                if(isSaveMode and current_food < 60000):
                    time.sleep(3600)
                    if main_are_there_errors():
                        open_validate_join(True)
                        open_event()
                        validateEvent = validate_open_event()
                        if(validateEvent == "Event running"):
                            close_event_button()
                if current_food > average or isSaveMode:
                    respA = use_food_option()
                    time.sleep(1.1)
                else:
                    respB = use_tickets_option()
                    time.sleep(1.1)
                if handle_errors_and_validate():
                    continue
                if respA == True or respB == True:
                    isParticipantPressed = participar_button()
                    if isParticipantPressed == True:
                        respAreThereFood = areThereFoodAlert()
                        if(respAreThereFood==False and repeat==True):
                            close_button()
                            time.sleep(SHORT_SLEEP)
                            pyautogui.press('esc')
                            time.sleep(SHORT_SLEEP)
                            pyautogui.press('esc')
                            time.sleep(SHORT_SLEEP)
                            close_button()
                            if handle_errors_and_validate():
                                continue
                            barResp = check_roger_bar_position()
                            if barResp == False:
                                return
                            pyautogui.doubleClick(652, 474)
                            time.sleep(SHORT_SLEEP)
                            pyautogui.doubleClick(601, 467)
                            time.sleep(SHORT_SLEEP)
                            pyautogui.doubleClick(580, 470)
                            main_get_home_screen()
                            respCloseButton = close_button()
                            if respCloseButton == True:
                                time.sleep(SHORT_SLEEP)
                            main_are_there_errors()
                            open_validate_join()
                            open_event()
                            validate_open_event()
                            repeat = False
                            continue
                        elif(repeat==False):
                            respAreThereFood = areThereFoodAlert()
                            if(respAreThereFood==False):
                                time.sleep(1800)
                                if main_are_there_errors():
                                    open_validate_join(True)
                                    open_event()
                                    validateEvent = validate_open_event()
                                    if(validateEvent == "Event running"):
                                        close_event_button()
                                    use_food_option()
                                    time.sleep(1.1)
                                    participar_button()
                        isFightDone = confirm_and_fight(resp1.get("reader"), isThereRewards)
                        repeat = True
                        if isFightDone == False or isFightDone == "Error":
                            main_are_there_errors()
                            time.sleep(10)
                            reload_game()
                            main_get_home_screen()
                            open_validate_join(True)
                            open_event()
                            validate_open_event()
                        restart += 1
                        if lBFoodPosition == 3:
                            lBFoodPosition = 0
                            lastBattleFood = [0, 1, 2, 3]
                        else:
                            lBFoodPosition += 1
                    else:
                        print("No hemos podido encontrar el botón de participar.")
                else:
                    print("No se ha encontrado el botón para ingresar al evento.")
    else:
        return print("No se ha conseguido abrir el evento.")