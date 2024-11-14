import copy
import cv2
import numpy as np
from time import sleep
import os
import pyautogui
pyautogui.useImageNotFoundException(False)
pyautogui.FAILSAFE = False
from pathlib import Path
import sys
import concurrent.futures

MANANAMIMOSAEVENT_PATH = "Images/MananaMimosaEvent"
MANANAMIMOSAEVENTFIGHT_PATH = "Images/MananaMimosaEvent/Fight"
OPENCLOSECHAT_PATH = "Images/Chat"
GETBUTTONSCHAT_PATH = "Images/Chat/getButtonEvents"
max_attempts = 10
CONFIDENCE_LEVEL = 0.9
CONFIDENCE_LEVEL_TWO = 0.95
SHORT_SLEEP = 1
SHORT_SHORT_SLEEP = 0.5
random_count = 0
SelectPlayer_region = (196, 238, 948, 343)
DisablePlayer_region = (208, 563, 222, 99)
LeaveFightButton_region = (531, 611, 257, 110)
SelectOpponent_region = (885, 29, 372, 60)
WaitTournament_region = (931, 29, 267, 65)
FinishEvent_region = (1037, 123, 252, 119)
isInfoPlayersOpen_region = (210, 91, 921, 577)
ConfirmJoinTournament_region = (879, 592, 237, 110)

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.OpenCloseChat import closeChat, thereAreMessages
from Events.ChatRewards.getChatRewards import getButtons
from TelegramLogs import custom_print

from Components.LoadImages import load_images_from_path
from Components.isErrorMessage import main_are_there_errors
from Components.FindActividadSospechosa import isActividadSospechosa
from Components.GetHomeScreen import main_get_home
from Components.RandomActivities import mainGetHappiness
from Components._GlobalOpenValidateJoin import open_validate_join
from Components.isThereFamiliaLandiaWar import main_is_there_familialandia_war
from Components.MananaMimosa.ValidateOpenEvent import validate_open_event
from Components.MananaMimosa.ValidateOpenEvent import open_event
from Components.FamiliaLandiaFlow import main_familialandia_flow
from Components.GetMails import main_get_mails
from Components.WhereAmI import main_where_am_i

LoadingTournament_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "LoadingTournament_")
isInfoPlayersOpen_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "isInfoPlayersOpen_")
ArrowRight_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "ArrowRight_")
FightButton_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "FightButton_")
Fighting_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "Fighting_")
FinishEvent_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "FinishEvent_")
JoiningFight_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "JoiningFight_")
LeaveFightButton_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "LeaveFightButton_")
LeavingFight_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "LeavingFight_")
SelectOpponent_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "SelectOpponent_")
SelectPlayer_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "SelectPlayer_")
WaitTournament_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "WaitTournament_")
PlayerOverMe_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "PlayerOverMe_")
PlayerUnderMe_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "PlayerUnderMe_")
DisablePlayer_imgs = load_images_from_path(MANANAMIMOSAEVENTFIGHT_PATH, "DisablePlayer_")
Join_Chat_imgs = load_images_from_path(OPENCLOSECHAT_PATH, "join_chat_")
get_button_imgs = load_images_from_path(GETBUTTONSCHAT_PATH, "get_button_")
leave_button_imgs = load_images_from_path(OPENCLOSECHAT_PATH, "leave_chat_")
EventNoRunning_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "EventNoRunning_")
EventRunning_imgs = load_images_from_path(MANANAMIMOSAEVENT_PATH, "EventRunning_")

initial_state = [
    {"position": i, "power": 0, "reward": "bot", "isMaped": False}
    for i in range(1, 16)
]

info_players = copy.deepcopy(initial_state)


def reset_info_players():
    global info_players
    info_players = copy.deepcopy(initial_state)
    return True

position_region = (973, 518, 1105 - 973, 556 - 518)
power_region = (698, 331, 900 - 698, 366 - 331)
state_region = (209, 564, 440 - 209, 657 - 564)

def wait_match():
    count = 0
    failCount = 0
    while count < max_attempts and failCount < 40:
        for _, image_path in LoadingTournament_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
            if location:
                sleep(6)
                failCount += 1
            else:
                count += 1
    if (count > 8):
        count = 0
        failCount = 0
        while count < max_attempts:
            for _, image_path in EventRunning_imgs.items():
                location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
                if location:
                    custom_print("El torneo ha comenzado...", False)
                    return True
                else:
                    custom_print("El torneo ha comenzado pero no se encontró EventRunning_imgs", False)
                    return False
    if (failCount > 38):
        custom_print("El torneo no ha logrado comenzar con éxito.", False)
        return False


def open_info_players():
    sleep(1.5)
    found = False
    count = 0
    while not found and count < 15:
        for _, image_path in SelectPlayer_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO, region=SelectPlayer_region)
            count += 1
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                sleep(SHORT_SHORT_SLEEP)
                return found
            else:
                sleep(SHORT_SLEEP)
    return found


def preprocess_image(img, pos):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if pos == 1:
        _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    else:
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((1, 1), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    return thresh

def capture_and_read_text(region, reader, allowlist, pos):
    img = pyautogui.screenshot(region=region)
    processed_img = preprocess_image(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR), pos)
    result = reader.readtext(processed_img, allowlist=allowlist)
    
    for text in result:
        if pos == 1:
            digits = ''.join(filter(str.isdigit, text[1]))
            if digits:
                return int(digits)
        elif text[1].isdigit():
            return int(text[1])
    return None

def find_position(reader):
    position = capture_and_read_text(
        position_region, reader, allowlist='Posición: 0123456789', pos=1)
    return position if position is not None else 15

def find_power(reader):
    power = capture_and_read_text(
        power_region, reader, allowlist='0123456789', pos=0)
    return power if power is not None and power > 10000 else 80000000

def find_state():
    attempts = 5
    for _ in range(attempts):
        for img_dict in [PlayerUnderMe_imgs, PlayerOverMe_imgs, DisablePlayer_imgs]:
            for _, image_path in img_dict.items():
                location = pyautogui.locateOnScreen(image_path, region=state_region, confidence=CONFIDENCE_LEVEL_TWO)
                if location:
                    return "bot" if img_dict == PlayerUnderMe_imgs else "top" if img_dict == PlayerOverMe_imgs else "disableForAttack"
    
    custom_print("No se ha conseguido encontrar el estado", False)
    sleep(2)
    if main_are_there_errors() or not validate_open_info_players():
        custom_print("Retornando errror en find_state", False)
        return "Error"
    else:
        custom_print("xxx 11", False)
    return "disableForAttack"

def mapear_info_player(reader):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        state_future = executor.submit(find_state)
        if state_future == "Error":
            return "Error"
        position_future = executor.submit(find_position, reader)
        power_future = executor.submit(find_power, reader)
        return position_future.result(), power_future.result(), state_future.result()


def skip_player():
    pyautogui.click(778, 611)


def loading():
    count = 0
    failCount = 0
    while count < max_attempts and failCount < 30:
        for _, image_path in JoiningFight_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            if location:
                sleep(2)
                failCount += 1
            else:
                count += 1
    if (count > 8):
        return True
    if (failCount > 28):
        return False


def find_leave_fight_button():
    found = False
    count = 0
    while not found and count < 30:
        for _, image_path in LeaveFightButton_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO, region=LeaveFightButton_region)
            count += 1
            sleep(2)
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                sleep(2)
                return found
    return found


def start_round(isThereRewards):
    errorCount = 0
    found = False
    count = 0
    firstTime = True
    while not found:
        for _, image_path in SelectOpponent_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL, region=SelectOpponent_region)
            count += 1
            if location:
                found = True
                return found
            else:
                if(isThereRewards and firstTime and thereAreMessages()):
                    firstTime = False
                    getButtons()
                    chatResp = closeChat()
                    if(chatResp == False):
                        pyautogui.click(736, 314)
                else:
                    sleep(SHORT_SLEEP)
                    if (count > 200):
                        custom_print(f"No se ha encontrado el texto Seleccionar al siguiente oponente. Error count hasta 50: {errorCount}")
                        sleep(10)
                        errorCount += 10
                        if(errorCount > 50):
                            custom_print("Tienes 1 minuto para entrar al juego.")
                            sleep(60)
                            if main_are_there_errors():
                                return "Error"
                            else:
                                custom_print("xxx 22", False)
                            return "Error"
    sleep(2)
    return found


def wait_next_round():
    count = 0
    failCount = 0
    while count < max_attempts and failCount < 20:
        for _, image_path in WaitTournament_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO, region=WaitTournament_region)
            if location:
                sleep(5)
                failCount += 1
            else:
                count += 1


def attack():
    pyautogui.click(1012, 610)
    isLoad = loading()
    if (isLoad == True):
        sleep(4)
        isPressedLeaveFight = find_leave_fight_button()
        if (isPressedLeaveFight):
            wait_next_round()
        else:
            custom_print("No se ha encontrado el botón de salir de pelea.", False)
    else:
        custom_print("La pelea no se ha logrado comenzar con éxito.", False)
    return True


def round_1(reader):
    custom_print("Hace ronda 1", False)
    found = False
    # Buscar el jugador con menos poder
    min_power = float('inf')
    min_power_position = None

    for player in info_players:
        if player["power"] < min_power:
            min_power = player["power"]
            min_power_position = player["position"]
    count = 0
    # Comparar la posición actual con la posición del jugador con menos poder
    while found == False:
        sleep(SHORT_SLEEP)
        current_position = find_position(reader)
        if current_position != min_power_position:
            skip_player()
            count += 1
            if(count > 30):
                custom_print("AA 11.", False)
                if main_are_there_errors():
                    return "Error"
                else:
                    custom_print("xxx 33", False)
        else:
            found = True
    if (found):
        isDone = attack()
    if isDone:
        return True
    else:
        custom_print("No se encontró el botón de ataque", False)


def round_2(reader):
    custom_print("Hace ronda 2", False)
    resp = round_3(reader)
    if (resp == True):
        return resp
    else:
        return False


def round_3(reader):
    found = False
    min_power_top = float('inf')
    min_power_position_top = None
    min_power_bot = float('inf')
    min_power_position_bot = None

    for player in info_players:
        if player["reward"] == "top" and player["power"] < min_power_top:
            min_power_top = player["power"]
            min_power_position_top = player["position"]

    if min_power_position_top is None:
        for player in info_players:
            if player["reward"] == "bot" and player["power"] < min_power_bot:
                min_power_bot = player["power"]
                min_power_position_bot = player["position"]

    if(min_power_top == 1 or min_power_bot == 1):
        for player in info_players:
            if player["reward"] != "disableForAttack" and player["position"] is not None and player["position"] > min_power_position_top:
                min_power_top = player["power"]
                min_power_position_top = player["position"]
    count = 0
    # Buscar jugador de ataque por encima de mí
    if (min_power_position_top != None):
        while found == False:
            sleep(SHORT_SLEEP)
            current_position = find_position(reader)
            if current_position != min_power_position_top:
                skip_player()
                count += 1
                if(count > 30):
                    custom_print("AA 22.", False)
                    if main_are_there_errors():
                        return "Error"
                    else:
                        custom_print("xxx 44", False)
                    if(count > 40):
                        custom_print("Pasa count 40....", False)
                        return "Error"
            else:
                found = True
                break
    else:
        while found == False:
            sleep(SHORT_SLEEP)
            current_position = find_position(reader)
            if current_position != min_power_position_bot:
                skip_player()
                count += 1
                if(count > 30):
                    custom_print("AA 33.", False)
                    if main_are_there_errors():
                        return "Error"
            else:
                found = True
                break
    isDone = attack()
    if isDone:
        return True
    else:
        custom_print("No se encontró el botón de ataque", False)


def round_4(reader):
    custom_print("Hace ronda 4", False)
    resp = round_3(reader)
    if (resp == True):
        return resp
    else:
        return False


def round_5(reader):
    custom_print("Hace ronda 5", False)
    resp = round_3(reader)
    if (resp == True):
        return resp
    else:
        return False


def leave_tournament():
    count = 0
    while True and count < 75:
        count += 1
        for _, image_path in FinishEvent_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO, region=FinishEvent_region)
            if main_are_there_errors():
                custom_print("AA 44.", False)
                return "Error"
            else:
                custom_print("xxx 444", False)
            if location:
                miss_click()
                sleep(SHORT_SLEEP)
                miss_click()
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
            else:
                sleep(1.5)
    custom_print("Error leave tournament 1", False)
    return False


def mapeo(reader):
    count = 0
    while True:
        count += 1
        unmapped_count = sum(
            1 for player in info_players if not player["isMaped"])
        if unmapped_count == 1:
            break
        
        if(count > 14):
            custom_print("AA 55.", False)
            if main_are_there_errors():
                return "Error"
        sleep(0.8)
        position, power, state = mapear_info_player(reader)
        if state == "Error":
            return "Error"
        if position <= 15 and (state == "bot" or state == "top" or state == "disableForAttack"):
            info_players[position - 1]["power"] = power
            info_players[position - 1]["reward"] = state
            info_players[position - 1]["isMaped"] = True
        else:
            continue
        skip_player()
    # Asigna valores cualquiera al item no mapeado (Mi pos)
    # custom_print(info_players)
    for player in info_players:
        if not player["isMaped"]:
            player["power"] = 99999999
            player["reward"] = "No"
            break


def validate_open_info_players():
    count = 0
    while count < max_attempts:
        for _, image_path in isInfoPlayersOpen_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO, region=isInfoPlayersOpen_region)
            count += 1
            if location:
                return True
    return False

def miss_click():
    pyautogui.click(165, 194)
    sleep(SHORT_SHORT_SLEEP)
    pyautogui.click(165, 194)


def am_i_out():
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in EventNoRunning_imgs.items():
            sleep(2)
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
            count += 1
            found = True
            if location:
                return True
            else:
                sleep(0.5)
    return found


def start_tournament_flow(reader, isThereRewards, checkFamilyWar):
    custom_print("start_tournament_flow", False)
    isStartRound = False
    global random_count
    prevent = 0
    while True:
        prevent += 1 # Usar este prevente para controlar el bucle xxx 223 despues de identificarlo bien
        isOpen = open_info_players()
        if main_are_there_errors():
            resp = main_where_am_i()
            if(resp != False):
                return "Error"
            custom_print("Conectate, tienes 10 minutos para completar el evento 1")
            sleep(600)
            return "Error"
        else:
            custom_print("xxx 223", False)
        sleep(1)
        validate = validate_open_info_players()
        if isOpen and validate:
            custom_print("xxx 223 break 1", False)
            break
    if isOpen == True and validate:
        mapResp = mapeo(reader)
        if(mapResp=="Error"):
            resp = main_where_am_i()
            if(resp != False):
                return "Error"
            custom_print("Conectate, tienes 10 minutos para completar el evento 2")
            sleep(600)
            return "Error"
        respR1 = round_1(reader)
        if main_are_there_errors():
            resp = main_where_am_i()
            if(resp != False):
                return "Error"
            custom_print("Conectate, tienes 10 minutos para completar el evento 3")
            sleep(600)
            return "Error"
        if (respR1 == True or custom_print("No hay respR1", False)):
            isReset = reset_info_players()
            if (isReset == True):
                isStartRound = start_round(isThereRewards)
                if (isStartRound == True):
                    isStartRound = False
                    miss_click()
                    isOpen = open_info_players()
                    if main_are_there_errors():
                        resp = main_where_am_i()
                        if(resp != False):
                            return "Error"
                        custom_print("Conectate, tienes 10 minutos para completar el evento 4")
                        sleep(600)
                        return "Error"
                    if (isOpen == True):
                        mapResp = mapeo(reader)
                        if(mapResp=="Error"):
                            resp = main_where_am_i()
                            if(resp != False):
                                return "Error"
                            custom_print("Conectate, tienes 10 minutos para completar el evento 5")
                            sleep(600)
                            return "Error"
                        respR2 = round_2(reader)
                        if (respR2 == True or custom_print("No hay respR2", False)):
                            isReset = reset_info_players()
                            if (isReset == True):
                                isStartRound = start_round(isThereRewards)
                                if (isStartRound == True):
                                    isStartRound = False
                                    miss_click()
                                    isOpen = open_info_players()
                                    if main_are_there_errors():
                                        resp = main_where_am_i()
                                        if(resp != False):
                                            return "Error"
                                        custom_print("Conectate, tienes 9 minutos para completar el evento 6")
                                        sleep(540)
                                        return "Error"
                                    if (isOpen == True):
                                        mapResp = mapeo(reader)
                                        if(mapResp=="Error"):
                                            resp = main_where_am_i()
                                            if(resp != False):
                                                return "Error"
                                            custom_print("Conectate, tienes 9 minutos para completar el evento 7")
                                            sleep(540)
                                            return "Error"
                                        custom_print("Hace ronda 3", False)
                                        respR3 = round_3(reader)
                                        if (respR3 == True or custom_print("No hay respR3", False)):
                                            isReset = reset_info_players()
                                            if (isReset == True):
                                                isStartRound = start_round(isThereRewards)
                                                if (isStartRound == True):
                                                    isStartRound = False
                                                    miss_click()
                                                    isOpen = open_info_players()
                                                    if main_are_there_errors():
                                                        resp = main_where_am_i()
                                                        if(resp != False):
                                                            return "Error"
                                                        custom_print("Conectate, tienes 7 minutos para completar el evento 8")
                                                        sleep(420)
                                                        return "Error"
                                                    if (isOpen == True):
                                                        mapResp = mapeo(reader)
                                                        if(mapResp=="Error"):
                                                            resp = main_where_am_i()
                                                            if(resp != False):
                                                                return "Error"
                                                            custom_print("Conectate, tienes 7 minutos para completar el evento 9")
                                                            sleep(420)
                                                            return "Error"
                                                        respR4 = round_4(
                                                            reader)
                                                        if (respR4 == True or custom_print("No hay respR4", False)):
                                                            isReset = reset_info_players()
                                                            if (isReset == True):
                                                                isStartRound = start_round(False)
                                                                if (isStartRound == True):
                                                                    isStartRound = False
                                                                    miss_click()
                                                                    isOpen = open_info_players()
                                                                    if main_are_there_errors():
                                                                        resp = main_where_am_i()
                                                                        if(resp != False):
                                                                            return "Error"
                                                                        custom_print("Conectate, tienes 5 minutos para completar el evento 10")
                                                                        sleep(300)
                                                                        return "Error"
                                                                    if (isOpen == True):
                                                                        mapResp = mapeo(reader)
                                                                        if(mapResp=="Error"):
                                                                            resp = main_where_am_i()
                                                                            if(resp != False):
                                                                                return "Error"
                                                                            custom_print("Conectate, tienes 5 minutos para completar el evento 11")
                                                                            sleep(300)
                                                                            return "Error"
                                                                        respR5 = round_5(
                                                                            reader)
                                                                        if (respR5 == True or custom_print("No hay respR5", False)):
                                                                            isReset = reset_info_players()
                                                                            if (isReset == True):
                                                                                if main_are_there_errors():
                                                                                    resp = main_where_am_i()
                                                                                    if(resp != False):
                                                                                        return "Error"
                                                                                    custom_print("Conectate, tienes 3 minutos para completar el evento 12")
                                                                                    sleep(180)
                                                                                    return "Error"
                                                                                respHome = main_get_home()
                                                                                if(respHome == True):
                                                                                    mainGetHappiness()
                                                                                    if(checkFamilyWar == True):
                                                                                        warResp = main_is_there_familialandia_war(True)
                                                                                        if(warResp==True):
                                                                                            print("Hay guerra, uniéndose...")
                                                                                            main_familialandia_flow()
                                                                                    if random_count % 2 == 0:
                                                                                        main_get_mails()
                                                                                    random_count += 1
                                                                                    main_get_home()
                                                                                    open_validate_join(True)
                                                                                    open_event()
                                                                                    validate_open_event()
                                                                                isLeaving = leave_tournament()
                                                                                amIOut = am_i_out()
                                                                                if(amIOut==False):
                                                                                    isLeaving = leave_tournament()
                                                                                if (isLeaving == True and amIOut == True):
                                                                                    return True
                                                                                else:
                                                                                    custom_print("No se logró validar el menu del evento", False)
                                                                                    respActividadSospechosa = isActividadSospechosa()
                                                                                    if(respActividadSospechosa == True):
                                                                                        sleep(160)
                                                                                        custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA 13")
                                                                                    else:
                                                                                        if main_are_there_errors():
                                                                                            resp = main_where_am_i()
                                                                                            if(resp != False):
                                                                                                return "Error"
                                                                                            custom_print("Conectate, tienes 10 minutos para completar el evento 16")
                                                                                            sleep(600)
                                                                            else:
                                                                                custom_print("FT 7", False)
                                                                        else:
                                                                            custom_print(
                                                                                "Error al terminar el round 5.", False)
                                                                            respActividadSospechosa = isActividadSospechosa()
                                                                            if(respActividadSospechosa == True):
                                                                                sleep(160)
                                                                                custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA 12")
                                                                            else:
                                                                                if main_are_there_errors():
                                                                                    resp = main_where_am_i()
                                                                                    if(resp != False):
                                                                                        return "Error"
                                                                                    custom_print("Conectate, tienes 10 minutos para completar el evento 15")
                                                                                    sleep(600)
                                                                elif(isStartRound == "Error"):
                                                                    custom_print("isStartRound 4", False)
                                                                    respActividadSospechosa = isActividadSospechosa()
                                                                    if(respActividadSospechosa == True):
                                                                        sleep(160)
                                                                        custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA 11")
                                                                    else:
                                                                        if main_are_there_errors():
                                                                            resp = main_where_am_i()
                                                                            if(resp != False):
                                                                                return "Error"
                                                                            custom_print("Conectate, tienes 10 minutos para completar el evento 14")
                                                                            sleep(600)
                                                                    return isStartRound
                                                                else:
                                                                    custom_print("FT 6", False)
                                                            else:
                                                                custom_print("FT 5", False)
                                                        else:
                                                            custom_print(
                                                                "Error al terminar el round 4.", False)
                                                            respActividadSospechosa = isActividadSospechosa()
                                                            if(respActividadSospechosa == True):
                                                                sleep(160)
                                                                custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA 10")
                                                            else:
                                                                if main_are_there_errors():
                                                                    resp = main_where_am_i()
                                                                    if(resp != False):
                                                                        return "Error"
                                                                    custom_print("Conectate, tienes 10 minutos para completar el evento 13")
                                                                    sleep(600)
                                                    else:
                                                        custom_print("FT 4", False)
                                                elif(isStartRound == "Error"):
                                                    custom_print("isStartRound 3", False)
                                                    respActividadSospechosa = isActividadSospechosa()
                                                    if(respActividadSospechosa == True):
                                                        sleep(160)
                                                        custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA 9")
                                                    else:
                                                        if main_are_there_errors():
                                                            resp = main_where_am_i()
                                                            if(resp != False):
                                                                return "Error"
                                                            custom_print("Conectate, tienes 10 minutos para completar el evento 12")
                                                            sleep(600)
                                                    return isStartRound
                                                else:
                                                    custom_print("FT 3", False)
                                            else:
                                                custom_print("FT 2", False)
                                        else:
                                            custom_print(
                                                "Error al terminar el round 3.", False)
                                            respActividadSospechosa = isActividadSospechosa()
                                            if(respActividadSospechosa == True):
                                                sleep(160)
                                                custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA 8")
                                            else:
                                                if main_are_there_errors():
                                                    resp = main_where_am_i()
                                                    if(resp != False):
                                                        return "Error"
                                                    custom_print("Conectate, tienes 10 minutos para completar el evento 11")
                                                    sleep(600)
                                    else:
                                        custom_print("FT 1", False)
                                elif(isStartRound == "Error"):
                                    custom_print("isStartRound 2", False)
                                    respActividadSospechosa = isActividadSospechosa()
                                    if(respActividadSospechosa == True):
                                        sleep(160)
                                        custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA 7")
                                    else:
                                        if main_are_there_errors():
                                            resp = main_where_am_i()
                                            if(resp != False):
                                                return "Error"
                                            custom_print("Conectate, tienes 10 minutos para completar el evento 10")
                                            sleep(600)
                                    return isStartRound
                                else:
                                    custom_print("isStartRound 2", False)
                            else:
                                custom_print("Error reset_info_players 1", False)
                        else:
                            custom_print("Error al terminar el round 2.", False)
                            respActividadSospechosa = isActividadSospechosa()
                            if(respActividadSospechosa == True):
                                sleep(160)
                                custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA 6")
                            else:
                                if main_are_there_errors():
                                    resp = main_where_am_i()
                                    if(resp != False):
                                        return "Error"
                                    custom_print("Conectate, tienes 10 minutos para completar el evento 9")
                                    sleep(600)
                elif(isStartRound == "Error"):
                    custom_print("isStartRound 1", False)
                    respActividadSospechosa = isActividadSospechosa()
                    if(respActividadSospechosa == True):
                        sleep(160)
                        custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA 5")
                    else:
                        if main_are_there_errors():
                            resp = main_where_am_i()
                            if(resp != False):
                                return "Error"
                            custom_print("Conectate, tienes 9 minutos para completar el evento 8")
                            sleep(540)
                    return isStartRound
                else:
                    custom_print("Error isStartRound", False)
            else:
                custom_print("Error reset_info_players 1", False)
        else:
            custom_print("Error al terminar el round 1.", False)
    else:
        custom_print("No se logró abrir el menú de información de jugador.", False)
        respActividadSospechosa = isActividadSospechosa()
        if(respActividadSospechosa == True):
            sleep(160)
            custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA 4")
        else:
            if main_are_there_errors():
                resp = main_where_am_i()
                if(resp != False):
                    return False
                custom_print("Conectate, tienes 10 minutos para completar el evento 77")
                sleep(600)
    custom_print("Error fatal", False)
    return False


ConfirmJoinTournament_imgs = {
        "img1": os.path.join(MANANAMIMOSAEVENT_PATH, "ConfirmJoinTournament_1.png"),
        "img2": os.path.join(MANANAMIMOSAEVENT_PATH, "ConfirmJoinTournament_2.png"),
}

def confirm_and_fight(reader, isThereRewards, checkFamilyWar):
    custom_print("confirm_and_fight", False)
    reset_info_players()
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in ConfirmJoinTournament_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO, region=ConfirmJoinTournament_region)
            count += 1
            if location:
                sleep(0.2)
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
            else:
                sleep(SHORT_SLEEP)
                pyautogui.click(997, 647)
    if main_are_there_errors():
        custom_print("AA 66.", False)
        return False
    if (found == True):
        isStart = wait_match()
        if (isStart == True):
            tournamentResp = start_tournament_flow(reader, isThereRewards, checkFamilyWar)
            if (tournamentResp == True or tournamentResp == "Error"):
                return tournamentResp
            else:
                custom_print("El torneo NO se ha completado correctamente.", False)
                respActividadSospechosa = isActividadSospechosa()
                if(respActividadSospechosa == True):
                    sleep(160)
                    custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA")
                else:
                    if main_are_there_errors():
                        resp = main_where_am_i()
                        if(resp != False):
                            return False
                        custom_print("Conectate, tienes 10 minutos para completar el evento 4")
                        sleep(600)
                return False
        else:
            custom_print("No se encontro match", False)
            respActividadSospechosa = isActividadSospechosa()
            if(respActividadSospechosa == True):
                sleep(160)
                custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA 2")
            else:
                if main_are_there_errors():
                    resp = main_where_am_i()
                    if(resp != False):
                        return False
                    custom_print("Conectate, tienes 10 minutos para completar el evento 5")
                    sleep(600)
            return False
    else:
        custom_print("No se encontró el botón para confirmar batalla", False)
        respActividadSospechosa = isActividadSospechosa()
        if(respActividadSospechosa == True):
            sleep(160)
            custom_print("ACTIVIDAD SOSPECHOSAAAAAAAA 3")
        else:
            if main_are_there_errors():
                resp = main_where_am_i()
                if(resp != False):
                    return False
                custom_print("Conectate, tienes 10 minutos para completar el evento 6")
                sleep(600)
        return False
