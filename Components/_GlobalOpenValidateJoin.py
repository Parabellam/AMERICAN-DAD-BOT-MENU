import easyocr
import sys
from pathlib import Path
import time

reader = None

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from Components.ValidateScreen import detect_screen
from Components.OpenWindow import open_bluestacks_window
from Components.JoinMap import open_main_map

def preload_easyocr():
    print("Cargando easyOCR (Detección de imagen)")
    time.sleep(2)
    global reader
    reader = easyocr.Reader(['en'], gpu=False)

def open_validate_join():
    preload_easyocr()
    print("Carga terminada")
    resp1 = open_bluestacks_window()
    time.sleep(2)
    if(resp1):
        resp2 = detect_screen()
    else:
        return "Error al abrir Bluestacks"

    if(resp2.get("state")=="outMainMap"):
        resp3 = open_main_map(resp2.get("location"))
        if(resp3):
            return {"state":True, "reader":reader}
        else:
            return "Error al abrir el mapa principal"
    if(resp2.get("state")=="inMainMap"):
        return {"state":True, "reader":reader}
    else:
        return "Por favor ubicar el juego en las pantallas recomendadas por la aplicación."