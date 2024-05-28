import easyocr
import cv2
import numpy as np
import pyautogui
import time
import keyboard
from pathlib import Path

# Find position range
top_left_x_position, top_left_y_position = 973, 518
bottom_right_x_position, bottom_right_y_position = 1105, 556

def preprocess_image_for_position(img):
    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar un umbral fijo para separar el texto negro del fondo
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    return thresh

def capture_and_read_text(region, reader, allowlist, pos):
    img = pyautogui.screenshot(region=region)
    processed_img = preprocess_image_for_position(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    # Guardar la imagen procesada para inspección (opcional)
    cv2.imwrite('processed_image_position.png', processed_img)

    result = reader.readtext(processed_img, allowlist=allowlist)
    print(result, " - Resultados de OCR.")
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
    region = (top_left_x_position, top_left_y_position, bottom_right_x_position - top_left_x_position, bottom_right_y_position - top_left_y_position)
    position = capture_and_read_text(region, reader, allowlist='Pposición: 0123456789', pos=1)
    if position is not None:
        print("Posición encontrada:", position)
    else:
        print("No se encontró la posición.")
    return position

def preload_easyocr():
    print("Cargando easyOCR (Detección de imagen)")
    time.sleep(2)
    reader = easyocr.Reader(['es'], gpu=False)
    return reader

if __name__ == "__main__":
    reader = preload_easyocr()
    print("Carga Lista... 5 segundos")
    time.sleep(5)

    # Escuchar la tecla "+"
    print("Presiona la tecla '+' para encontrar la posición.")
    while True:
        if keyboard.is_pressed('+'):
            find_position(reader)
            # Esperar un poco para evitar múltiples detecciones de una sola pulsación
            time.sleep(0.5)
