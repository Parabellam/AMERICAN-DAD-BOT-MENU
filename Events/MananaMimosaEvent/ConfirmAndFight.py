import copy
import json
import cv2
import numpy as np
import time
import os
import pyautogui
import random
pyautogui.FAILSAFE = False

MANANAMIMOSAEVENT_PATH = "Images/MananaMimosaEvent"
MANANAMIMOSAEVENTFIGHT_PATH = "Images/MananaMimosaEvent/Fight"
max_attempts = 10

LoadingTournament_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENT_PATH))
    if file.startswith("LoadingTournament_") and file.endswith(".png")
}

isInfoPlayersOpen_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("isInfoPlayersOpen_") and file.endswith(".png")
}

ArrowRight_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("ArrowRight_") and file.endswith(".png")
}

FightButton_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("FightButton_") and file.endswith(".png")
}

Fighting_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("Fighting_") and file.endswith(".png")
}

FinishEvent_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("FinishEvent_") and file.endswith(".png")
}

JoiningFight_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("JoiningFight_") and file.endswith(".png")
}

LeaveFightButton_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("LeaveFightButton_") and file.endswith(".png")
}

LeavingFight_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("LeavingFight_") and file.endswith(".png")
}

SelectOpponent_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("SelectOpponent_") and file.endswith(".png")
}

SelectPlayer_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("SelectPlayer_") and file.endswith(".png")
}

WaitTournament_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("WaitTournament_") and file.endswith(".png")
}

PlayerOverMe_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("PlayerOverMe_") and file.endswith(".png")
}

PlayerUnderMe_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("PlayerUnderMe_") and file.endswith(".png")
}

DisablePlayer_imgs = {
    f"img{index+1}": os.path.join(MANANAMIMOSAEVENTFIGHT_PATH, file)
    for index, file in enumerate(os.listdir(MANANAMIMOSAEVENTFIGHT_PATH))
    if file.startswith("DisablePlayer_") and file.endswith(".png")
}

initial_state = [{
    "position": 1,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 2,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 3,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 4,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 5,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 6,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 7,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 8,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 9,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 10,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 11,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 12,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 13,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 14,
    "power": 0,
    "reward": "bot",
    "isMaped": False
}, {
    "position": 15,
    "power": 0,
    "reward": "bot",
    "isMaped": False
},]


info_players = copy.deepcopy(initial_state)


def reset_info_players():
    global info_players
    info_players = copy.deepcopy(initial_state)
    time.sleep(1)
    return True


# Find position range
top_left_x_position, top_left_y_position = 973, 518
bottom_right_x_position, bottom_right_y_position = 1105, 556
# Find power range
top_left_x_power, top_left_y_power = 698, 331
bottom_right_x_power, bottom_right_y_power = 900, 366
# Find state range
top_left_x_state, top_left_y_state = 209, 564
bottom_right_x_state, bottom_right_y_state = 440, 657


def wait_match():
    count = 0
    failCount = 0
    while count < max_attempts and failCount < 40:
        for _, image_path in LoadingTournament_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            if location:
                time.sleep(random.uniform(4, 5))
                failCount += 1
            else:
                count += 1
    if (count > 8):
        return True
    if (failCount > 38):
        print("El torneo no ha logrado comenzar con éxito.")
        return False


def open_info_players():
    time.sleep(1)
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in SelectPlayer_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                time.sleep(random.uniform(4, 5))
                return found
    return found


def preprocess_image_for_position(img):
    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar un umbral fijo para separar el texto negro del fondo
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    return thresh


def preprocess_image_for_power(img):
    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar umbralización para mejorar el contraste
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Opcional: Aplicar dilatación y erosión para mejorar la forma de los dígitos
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

    # Guardar la imagen procesada para inspección (opcional)
    if pos == 1:
        cv2.imwrite('processed_image_position.png', processed_img)
    else:
        cv2.imwrite('processed_image_power.png', processed_img)

    result = reader.readtext(processed_img, allowlist=allowlist)
    if pos == 1:
        for text in result:
            if text[1]:
                # Extraer todos los dígitos de text[1]
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
    region = (top_left_x_position, top_left_y_position, bottom_right_x_position -
              top_left_x_position, bottom_right_y_position - top_left_y_position)
    position = capture_and_read_text(
        region, reader, allowlist='Pposición: 0123456789', pos=1)
    if position == None:
        return 15
    return position


def find_power(reader):
    region = (top_left_x_power, top_left_y_power, bottom_right_x_power -
              top_left_x_power, bottom_right_y_power - top_left_y_power)
    power = capture_and_read_text(
        region, reader, allowlist='0123456789', pos=0)
    if power == None:
        return 50000000
    return power


def find_state():
    found = False
    count = 0
    while not found and count < 5:
        for _, image_path in PlayerUnderMe_imgs.items():
            location = pyautogui.locateOnScreen(image_path, region=(
                top_left_x_state, top_left_y_state, bottom_right_x_state - top_left_x_state, bottom_right_y_state - top_left_y_state), confidence=0.95)
            count += 1
            if location:
                found = True
                return "bot"
    count = 0
    while not found and count < 5:
        for _, image_path in PlayerOverMe_imgs.items():
            location = pyautogui.locateOnScreen(image_path, region=(
                top_left_x_state, top_left_y_state, bottom_right_x_state - top_left_x_state, bottom_right_y_state - top_left_y_state), confidence=0.95)
            count += 1
            if location:
                found = True
                return "top"
    count = 0
    while not found and count < 5:
        for _, image_path in DisablePlayer_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.9)
            count += 1
            if location:
                found = True
                return "disableForAttack"
    print("No se ha conseguido encontrar el estado")
    return "No"


def mapear_info_player(reader):
    position = 0
    power = 99999999
    state = "No"
    position = find_position(reader)
    power = find_power(reader)
    state = find_state()
    return position, power, state


def skip_player():
    pyautogui.click(778, 611)


def loading():
    count = 0
    failCount = 0
    while count < max_attempts and failCount < 30:
        for _, image_path in JoiningFight_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
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
    while not found and count < max_attempts:
        for _, image_path in LeaveFightButton_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            time.sleep(2)
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                time.sleep(2)
                return found
    return found


def start_round():
    found = False
    count = 0
    while not found:
        for _, image_path in SelectOpponent_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if location:
                found = True
                return found
            else:
                time.sleep(1)
                if (count > 200):
                    print(
                        "No se ha encontrado el texto Seleccionar al siguiente oponente.")
                    found = False
    time.sleep(2)
    return found


def wait_next_round():
    count = 0
    failCount = 0
    while count < max_attempts and failCount < 20:
        for _, image_path in WaitTournament_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            if location:
                time.sleep(random.uniform(7, 9))
                failCount += 1
            else:
                count += 1


def attack(round):
    pyautogui.click(1012, 610)
    time.sleep(1)
    isLoad = loading()
    if (isLoad == True):
        time.sleep(random.uniform(4, 5))
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
        time.sleep(1)
        current_position = find_position(reader)
        if current_position != min_power_position:
            skip_player()
            found = False
        else:
            found = True
    if (found):
        isDone = attack(1)
    if (isDone == True):
        return True
    else:
        print("No se encontró el botón de ataque")


def round_2(reader):
    found = False
    min_power = float('inf')
    min_power_position = None

    for player in info_players:
        if player["reward"] != "disableForAttack" and player["power"] < min_power:
            min_power = player["power"]
            min_power_position = player["position"]

    # Comparar la posición actual con la posición del jugador con menos poder
    while found == False:
        time.sleep(1)
        # Encontrar la posición actual
        current_position = find_position(reader)
        if current_position != min_power_position:
            skip_player()
        else:
            found = True
    isDone = attack(2)
    if (isDone == True):
        return True
    else:
        print("No se encontró el botón de ataque")


def round_3(reader, round):
    found = False
    min_power_top = float('inf')
    min_power_position_top = None
    min_power_bot = float('inf')
    min_power_position_bot = None

    for player in info_players:
        if player["reward"] == "top" and player["power"] < min_power_top:
            min_power_top = player["power"]
            min_power_position_top = player["position"]

    for player in info_players:
        if player["reward"] == "bot" and player["power"] < min_power_bot:
            min_power_bot = player["power"]
            min_power_position_bot = player["position"]

    count = 0
    # Buscar jugador de ataque por encima de mí
    if (min_power_position_top != None):
        while found == False:
            time.sleep(1)
            current_position = find_position(reader)
            if current_position != min_power_position_top:
                count += 1
                skip_player()
            else:
                found = True
    else:
        # Buscar jugador de ataque por debajo de mí
        while found == False:
            time.sleep(1)
            current_position = find_position(reader)
            if current_position != min_power_position_bot:
                count += 1
                skip_player()
            else:
                found = True
    isDone = attack(round)
    if (isDone == True):
        return True
    else:
        print("No se encontró el botón de ataque")


def round_4(reader):
    resp = round_3(reader, 4)
    if (resp == True):
        return resp
    else:
        return False


def round_5(reader):
    resp = round_3(reader, 5)
    if (resp == True):
        return resp
    else:
        return False


def leave_tournament():
    found = False
    while not found:
        for _, image_path in FinishEvent_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                time.sleep(1)
                return found


def mapeo(reader):
    while True:
        # Verifica si todos los elementos menos uno están mapeados
        unmapped_count = sum(
            1 for player in info_players if not player["isMaped"])
        if unmapped_count == 1:
            break

        time.sleep(1)
        position, power, state = mapear_info_player(reader)
        if position <= 15:
            info_players[position - 1]["power"] = power
            info_players[position - 1]["reward"] = state
            info_players[position - 1]["isMaped"] = True
        skip_player()

    # Asigna los valores específicos al primer item no mapeado
    for player in info_players:
        if not player["isMaped"]:
            player["power"] = 99999999
            player["reward"] = "No"
            # Deja isMaped como False
            break

    # mapped_data_str = "\n".join(
    #     [json.dumps(player, indent=2) for player in info_players])
    # print("Datos mapeados: ", mapped_data_str)


def validate_open_info_players():
    found = False
    count = 0
    while not found and count < max_attempts:
        for _, image_path in isInfoPlayersOpen_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            found = True
            if location:
                return found
    return found

def miss_click():
    pyautogui.click(165, 194)
    time.sleep(0.5)
    pyautogui.click(165, 194)


def start_tournament_flow(reader):
    isStartRound = False
    while True:
        isOpen = open_info_players()
        validate = validate_open_info_players()
        if isOpen and validate:
            break
    if isOpen == True and validate:
        mapeo(reader)
        respR1 = round_1(reader)
        if (respR1 == True or print("No hay respR1")):
            isReset = reset_info_players()
            if (isReset == True or print("No hay isReset")):
                isStartRound = start_round()
                if (isStartRound == True or print("No hay isStartRound")):
                    isStartRound = False
                    miss_click()
                    isOpen = open_info_players()
                    if (isOpen == True or print("No hay isOpen")):
                        mapeo(reader)
                        respR2 = round_2(reader)
                        if (respR2 == True):
                            isReset = reset_info_players()
                            if (isReset == True or print("No hay isReset")):
                                isStartRound = start_round()
                                if (isStartRound == True or print("No hay isStartRound")):
                                    isStartRound = False
                                    miss_click()
                                    isOpen = open_info_players()
                                    if (isOpen == True or print("No hay isOpen")):
                                        mapeo(reader)
                                        respR3 = round_3(reader, 3)
                                        if (respR3 == True):
                                            isReset = reset_info_players()
                                            if (isReset == True or print("No hay isReset")):
                                                isStartRound = start_round()
                                                if (isStartRound == True or print("No hay isStartRound")):
                                                    isStartRound = False
                                                    miss_click()
                                                    isOpen = open_info_players()
                                                    if (isOpen == True or print("No hay isOpen")):
                                                        mapeo(reader)
                                                        respR4 = round_4(
                                                            reader)
                                                        if (respR4 == True):
                                                            isReset = reset_info_players()
                                                            if (isReset == True or print("No hay isReset")):
                                                                isStartRound = start_round()
                                                                if (isStartRound == True or print("No hay isStartRound")):
                                                                    isStartRound = False
                                                                    miss_click()
                                                                    isOpen = open_info_players()
                                                                    if (isOpen == True or print("No hay isOpen")):
                                                                        mapeo(
                                                                            reader)
                                                                        respR5 = round_5(
                                                                            reader)
                                                                        if (respR5 == True):
                                                                            isReset = reset_info_players()
                                                                            if (isReset == True or print("No hay isReset")):
                                                                                isLeaving = leave_tournament()
                                                                                if (isLeaving == True):
                                                                                    return True
                                                                        else:
                                                                            print(
                                                                                "Error al terminar el round 5.")
                                                        else:
                                                            print(
                                                                "Error al terminar el round 4.")
                                        else:
                                            print(
                                                "Error al terminar el round 3.")
                        else:
                            print("Error al terminar el round 2.")
        else:
            print("Error al terminar el round 1.")
    else:
        print("No se logró abrir el menú de información de jugador.")
    return False


def confirm_and_fight(reader):
    reset_info_players()
    ConfirmJoinTournament_imgs = {
        "img1": os.path.join(MANANAMIMOSAEVENT_PATH, "ConfirmJoinTournament_1.png"),
        "img2": os.path.join(MANANAMIMOSAEVENT_PATH, "ConfirmJoinTournament_2.png"),
    }
    found = False
    count = 0
    time.sleep(1)
    while not found and count < max_attempts:
        for _, image_path in ConfirmJoinTournament_imgs.items():
            location = pyautogui.locateOnScreen(image_path, confidence=0.95)
            count += 1
            if location:
                found = True
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
            else:
                time.sleep(1)
                pyautogui.click(997, 647)
    if (found == True):
        isStart = wait_match()
        if (isStart == True):
            tournamentResp = start_tournament_flow(reader)
            if (tournamentResp == True):
                return tournamentResp
            else:
                print("El torneo NO se ha completado correctamente.")
                return tournamentResp
        else:
            print("No se encontro match")
            return False
    else:
        print("No se encontró el botón para confirmar batalla")
        return False
    return
