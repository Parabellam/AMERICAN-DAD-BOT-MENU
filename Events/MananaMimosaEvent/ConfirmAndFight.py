import copy
import cv2
import numpy as np
import time
import os
import pyautogui
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

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.OpenCloseChat import closeChat, thereAreMessages
from Events.ChatRewards.getChatRewards import getButtons

from Components.LoadImages import load_images_from_path
from Components.isErrorMessage import main_are_there_errors

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
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            if location:
                time.sleep(4)
                failCount += 1
            else:
                count += 1
    if (count > 8):
        return True
    if (failCount > 38):
        print("El torneo no ha logrado comenzar con éxito.")
        return False


def open_info_players():
    time.sleep(1.5)
    found = False
    count = 0
    while not found and count < 15:
        for _, image_path in SelectPlayer_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            count += 1
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                time.sleep(0.5)
                return found
            else:
                time.sleep(SHORT_SLEEP)
    return found


def preprocess_image_for_position(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    return thresh


def preprocess_image_for_power(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((1, 1), np.uint8)
    img_dilated = cv2.dilate(thresh, kernel, iterations=1)
    img_eroded = cv2.erode(img_dilated, kernel, iterations=1)

    return img_eroded


def capture_and_read_text(region, reader, allowlist, pos):
    img = pyautogui.screenshot(region=region)
    if pos == 1:
        processed_img = preprocess_image_for_position(
            cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
    else:
        processed_img = preprocess_image_for_power(
            cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    result = reader.readtext(processed_img, allowlist=allowlist)
    if pos == 1:
        for text in result:
            if text[1]:
                digits = ''.join(filter(str.isdigit, text[1]))
                if digits:
                    number = int(digits)
                    return number
    for text in result:
        if text[1].isdigit():
            number = int(text[1])
            return number
    return None


def find_position(reader):
    position = capture_and_read_text(
        position_region, reader, allowlist='Pposición: 0123456789', pos=1)
    if position == None:
        return 15
    return position

def find_power(reader):
    power = capture_and_read_text(
        power_region, reader, allowlist='0123456789', pos=0)
    if power == None:
        return 50000000
    return power

def find_state():
    found = False
    count = 0
    while not found and count < 5:
        for _, image_path in PlayerUnderMe_imgs.items():
            location = pyautogui.locateOnScreen(image_path, region=(state_region), confidence=CONFIDENCE_LEVEL_TWO)
            count += 1
            if location:
                found = True
                return "bot"
    count = 0
    while not found and count < 5:
        for _, image_path in PlayerOverMe_imgs.items():
            location = pyautogui.locateOnScreen(image_path, region=(state_region), confidence=CONFIDENCE_LEVEL_TWO)
            count += 1
            if location:
                found = True
                return "top"
    count = 0
    while not found and count < 5:
        for _, image_path in DisablePlayer_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
            count += 1
            if location:
                found = True
                return "disableForAttack"
    print("No se ha conseguido encontrar el estado")
    time.sleep(SHORT_SLEEP)
    return "disableForAttack"


def mapear_info_player(reader):
    position = 0
    power = 99999999
    state = "disableForAttack"
    with concurrent.futures.ThreadPoolExecutor() as executor:
        state_future = executor.submit(find_state)
        position_future = executor.submit(find_position, reader)
        power_future = executor.submit(find_power, reader)
        state = state_future.result()
        position = position_future.result()
        power = power_future.result()

    return position, power, state


def skip_player():
    pyautogui.click(778, 611)


def loading():
    count = 0
    failCount = 0
    while count < max_attempts and failCount < 30:
        for _, image_path in JoiningFight_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            if location:
                time.sleep(2)
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
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            count += 1
            time.sleep(2)
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                time.sleep(2)
                return found
    return found


def start_round(isThereRewards):
    errorCount = 0
    found = False
    count = 0
    firstTime = True
    while not found:
        for _, image_path in SelectOpponent_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
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
                    time.sleep(SHORT_SLEEP)
                    if (count > 200):
                        print(f"No se ha encontrado el texto Seleccionar al siguiente oponente. Error count hasta 50: {errorCount}")
                        time.sleep(5)
                        errorCount += 5
                        if(errorCount > 50):
                            print("Tienes 1 minuto para entrar al juego.")
                            time.sleep(30)
                            print("Tienes 30 segundos para entrar al juego.")
                            time.sleep(25)
                            print("Tienes 5 segundos para entrar al juego.")
                            time.sleep(5)
                            return "Error"
    time.sleep(2)
    return found


def wait_next_round():
    count = 0
    failCount = 0
    while count < max_attempts and failCount < 20:
        for _, image_path in WaitTournament_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            if location:
                time.sleep(5)
                failCount += 1
            else:
                count += 1


def attack():
    pyautogui.click(1012, 610)
    isLoad = loading()
    if (isLoad == True):
        time.sleep(4)
        isPressedLeaveFight = find_leave_fight_button()
        if (isPressedLeaveFight):
            wait_next_round()
        else:
            print("No se ha encontrado el botón de salir de pelea.")
    else:
        print("La pelea no se ha logrado comenzar con éxito.")
    return True


def round_1(reader):
    found = False
    # Buscar el jugador con menos poder
    min_power = float('inf')
    min_power_position = None

    for player in info_players:
        if player["power"] < min_power:
            min_power = player["power"]
            min_power_position = player["position"]

    # Comparar la posición actual con la posición del jugador con menos poder
    while found == False:
        time.sleep(SHORT_SLEEP)
        current_position = find_position(reader)
        if current_position != min_power_position:
            skip_player()
        else:
            found = True
    if (found):
        isDone = attack()
    if isDone:
        return True
    else:
        print("No se encontró el botón de ataque")


def round_2(reader):
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
            if player["reward"] != "disableForAttack" and player["position"] > min_power_position_top:
                min_power_top = player["power"]
                min_power_position_top = player["position"]

    # Buscar jugador de ataque por encima de mí
    if (min_power_position_top != None):
        while found == False:
            time.sleep(SHORT_SLEEP)
            current_position = find_position(reader)
            if current_position != min_power_position_top:
                skip_player()
            else:
                found = True
                break
    else:
        while found == False:
            time.sleep(SHORT_SLEEP)
            current_position = find_position(reader)
            if current_position != min_power_position_bot:
                skip_player()
            else:
                found = True
                break
    isDone = attack()
    if isDone:
        return True
    else:
        print("No se encontró el botón de ataque")


def round_4(reader):
    resp = round_3(reader)
    if (resp == True):
        return resp
    else:
        return False


def round_5(reader):
    resp = round_3(reader)
    if (resp == True):
        return resp
    else:
        return False


def leave_tournament():
    while True:
        for _, image_path in FinishEvent_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            if location:
                miss_click()
                time.sleep(SHORT_SLEEP)
                miss_click()
                time.sleep(SHORT_SLEEP)
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
            else:
                time.sleep(1.5)


def mapeo(reader):
    count = 0
    while True:
        count += 1
        unmapped_count = sum(
            1 for player in info_players if not player["isMaped"])
        if unmapped_count == 1:
            break
        
        if(count > 13):
            if main_are_there_errors():
                return "Error"
        time.sleep(0.5)
        position, power, state = mapear_info_player(reader)
        if position <= 15 and (state == "bot" or state == "top" or state == "disableForAttack"):
            info_players[position - 1]["power"] = power
            info_players[position - 1]["reward"] = state
            info_players[position - 1]["isMaped"] = True
        else:
            continue
        skip_player()
    # Asigna valores cualquiera al item no mapeado (Mi pos)
    for player in info_players:
        if not player["isMaped"]:
            player["power"] = 99999999
            player["reward"] = "No"
            break


def validate_open_info_players():
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in isInfoPlayersOpen_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            count += 1
            found = True
            if location:
                return found
    return found

def miss_click():
    pyautogui.click(165, 194)
    time.sleep(0.5)
    pyautogui.click(165, 194)


def am_i_out():
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in EventNoRunning_imgs.items():
            time.sleep(2)
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
            count += 1
            found = True
            if location:
                return found
    return found


def start_tournament_flow(reader, isThereRewards):
    isStartRound = False
    while True:
        isOpen = open_info_players()
        if main_are_there_errors():
            print("Conectate, tienes 10 minutos para completar el evento 1")
            time.sleep(600)
            return "Error"
        validate = validate_open_info_players()
        if isOpen and validate:
            break
    if isOpen == True and validate:
        mapResp = mapeo(reader)
        if(mapResp=="Error"):
            print("Conectate, tienes 10 minutos para completar el evento 2")
            time.sleep(600)
            return "Error"
        respR1 = round_1(reader)
        if main_are_there_errors():
            print("Conectate, tienes 10 minutos para completar el evento 3")
            time.sleep(600)
            return "Error"
        if (respR1 == True or print("No hay respR1")):
            isReset = reset_info_players()
            if (isReset == True):
                isStartRound = start_round(isThereRewards)
                if (isStartRound == True):
                    isStartRound = False
                    miss_click()
                    isOpen = open_info_players()
                    if main_are_there_errors():
                        print("Conectate, tienes 10 minutos para completar el evento 4")
                        time.sleep(600)
                        return "Error"
                    if (isOpen == True):
                        mapResp = mapeo(reader)
                        if(mapResp=="Error"):
                            print("Conectate, tienes 10 minutos para completar el evento 5")
                            time.sleep(600)
                            return "Error"
                        respR2 = round_2(reader)
                        if (respR2 == True or print("No hay respR2")):
                            isReset = reset_info_players()
                            if (isReset == True):
                                isStartRound = start_round(isThereRewards)
                                if (isStartRound == True):
                                    isStartRound = False
                                    miss_click()
                                    isOpen = open_info_players()
                                    if main_are_there_errors():
                                        print("Conectate, tienes 10 minutos para completar el evento 6")
                                        time.sleep(600)
                                        return "Error"
                                    if (isOpen == True):
                                        mapResp = mapeo(reader)
                                        if(mapResp=="Error"):
                                            print("Conectate, tienes 10 minutos para completar el evento 7")
                                            time.sleep(600)
                                            return "Error"
                                        respR3 = round_3(reader)
                                        if (respR3 == True or print("No hay respR3")):
                                            isReset = reset_info_players()
                                            if (isReset == True):
                                                isStartRound = start_round(isThereRewards)
                                                if (isStartRound == True):
                                                    isStartRound = False
                                                    miss_click()
                                                    isOpen = open_info_players()
                                                    if main_are_there_errors():
                                                        print("Conectate, tienes 7 minutos para completar el evento 8")
                                                        time.sleep(420)
                                                        return "Error"
                                                    if (isOpen == True):
                                                        mapResp = mapeo(reader)
                                                        if(mapResp=="Error"):
                                                            print("Conectate, tienes 7 minutos para completar el evento 9")
                                                            time.sleep(420)
                                                            return "Error"
                                                        respR4 = round_4(
                                                            reader)
                                                        if (respR4 == True or print("No hay respR4")):
                                                            isReset = reset_info_players()
                                                            if (isReset == True):
                                                                isStartRound = start_round(False)
                                                                if (isStartRound == True):
                                                                    isStartRound = False
                                                                    miss_click()
                                                                    isOpen = open_info_players()
                                                                    if main_are_there_errors():
                                                                        print("Conectate, tienes 5 minutos para completar el evento 10")
                                                                        time.sleep(300)
                                                                        return "Error"
                                                                    if (isOpen == True):
                                                                        mapResp = mapeo(reader)
                                                                        if(mapResp=="Error"):
                                                                            print("Conectate, tienes 5 minutos para completar el evento 11")
                                                                            time.sleep(300)
                                                                            return "Error"
                                                                        respR5 = round_5(
                                                                            reader)
                                                                        if (respR5 == True or print("No hay respR5")):
                                                                            isReset = reset_info_players()
                                                                            if (isReset == True):
                                                                                if main_are_there_errors():
                                                                                    print("Conectate, tienes 3 minutos para completar el evento 12")
                                                                                    time.sleep(180)
                                                                                    return "Error"
                                                                                isLeaving = leave_tournament()
                                                                                amIOut = am_i_out()
                                                                                if(amIOut==False):
                                                                                    isLeaving = leave_tournament()
                                                                                if (isLeaving == True and amIOut == True):
                                                                                    return True
                                                                                else:
                                                                                    print("No se logró validar el menu del evento")
                                                                                    print(amIOut)
                                                                        else:
                                                                            print(
                                                                                "Error al terminar el round 5.")
                                                                elif(isStartRound == "Error"):
                                                                    print("isStartRound 4")
                                                                    return isStartRound
                                                        else:
                                                            print(
                                                                "Error al terminar el round 4.")
                                                elif(isStartRound == "Error"):
                                                    print("isStartRound 3")
                                                    return isStartRound
                                        else:
                                            print(
                                                "Error al terminar el round 3.")
                                elif(isStartRound == "Error"):
                                    print("isStartRound 2")
                                    return isStartRound
                        else:
                            print("Error al terminar el round 2.")
                elif(isStartRound == "Error"):
                    print("isStartRound 1")
                    return isStartRound
        else:
            print("Error al terminar el round 1.")
    else:
        print("No se logró abrir el menú de información de jugador.")
    print("Error fatal")
    return False


ConfirmJoinTournament_imgs = {
        "img1": os.path.join(MANANAMIMOSAEVENT_PATH, "ConfirmJoinTournament_1.png"),
        "img2": os.path.join(MANANAMIMOSAEVENT_PATH, "ConfirmJoinTournament_2.png"),
}

def confirm_and_fight(reader, isThereRewards):
    reset_info_players()
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in ConfirmJoinTournament_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL_TWO)
            count += 1
            if location:
                time.sleep(0.2)
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
            else:
                time.sleep(SHORT_SLEEP)
                pyautogui.click(997, 647)
    if main_are_there_errors():
        print("5")
        return False
    if (found == True):
        isStart = wait_match()
        if (isStart == True):
            tournamentResp = start_tournament_flow(reader, isThereRewards)
            if (tournamentResp == True or tournamentResp == "Error"):
                return tournamentResp
            else:
                print("El torneo NO se ha completado correctamente.")
                return False
        else:
            print("No se encontro match")
            return False
    else:
        print("No se encontró el botón para confirmar batalla")
        return False
