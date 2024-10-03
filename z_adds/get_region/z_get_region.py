from pynput import mouse
from PIL import ImageGrab
from time import sleep

# Lista para almacenar las coordenadas de los clics
clicks = []

def on_click(x, y, button, pressed):
    # Si se detecta un clic del botón izquierdo
    if pressed and button == mouse.Button.left:
        # Almacena las coordenadas del clic
        clicks.append((x, y))
        print(f"Clic detectado en: ({x}, {y})")
        
        # Si ya tenemos dos clics, calculamos la región y tomamos el screenshot
        if len(clicks) == 2:
            # Obtener las coordenadas de la región a partir de los clics
            top_left_x = min(clicks[0][0], clicks[1][0])
            top_left_y = min(clicks[0][1], clicks[1][1])
            bottom_right_x = max(clicks[0][0], clicks[1][0])
            bottom_right_y = max(clicks[0][1], clicks[1][1])

            # Imprimir coordenadas para verificación
            print(f"Coordenadas de clic: {clicks}")
            print(f"Región: ({top_left_x}, {top_left_y}, {bottom_right_x}, {bottom_right_y})")

            # Pausa para asegurarse de que la pantalla esté estabilizada
            sleep(0.5)

            # Tomar la captura de pantalla de la región
            screenshot = ImageGrab.grab(bbox=(top_left_x, top_left_y, bottom_right_x, bottom_right_y))
            
            # Guardar la imagen
            screenshot.save("captura_region.png")
            print("Captura de pantalla guardada como captura_region.png")

            # Detener el listener
            return False

# Listener del ratón
with mouse.Listener(on_click=on_click) as listener:
    print("Por favor, haga dos clics para seleccionar la región.")
    listener.join()
