import easyocr
import sys
from pathlib import Path
from time import sleep

reader = None

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.ValidateScreen import detect_screen
from Components.OpenWindow import open_bluestacks_window
from Components.JoinMap import open_main_map
from Components.RestartGame import open_app
from TelegramLogs import custom_print

def preload_easyocr():
    sleep(1.5)
    global reader
    reader = easyocr.Reader(['en'], gpu=False)

def open_validate_join(isReloadGame = False):
    if(isReloadGame==False):
        preload_easyocr()
        resp1 = open_bluestacks_window()
        sleep(1.5)
    if(isReloadGame == True or resp1):
        resp2 = detect_screen()
    else:
        return {"state":"Error al abrir Bluestacks"}

    if(resp2.get("state")=="outMainMap"):
        resp3 = open_main_map()
        if(resp3):
            return {"state":"True", "reader":reader}
        else:
            return {"state":"Error al abrir el mapa principal"}
    if(resp2.get("state")=="inMainMap"):
        return {"state":"True", "reader":reader}
    else:
        resp = open_app()
        if resp:
            custom_print("Se ha organizado un error 11.", False)
            return {"state":"True", "reader":reader}
        custom_print("Por favor ubicar el juego:")
        return {"state":"Por favor ubicar el juego en las pantallas recomendadas por la aplicación."}