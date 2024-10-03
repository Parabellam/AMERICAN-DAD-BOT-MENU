from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed:
        print(f'Coordenadas del clic: ({x}, {y})')

# Crear un listener para el mouse
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
