import pyautogui
import keyboard
import threading
import time

# Variable para controlar el estado del clic automático
clicking = False

# Función que realiza clics automáticos cada 0.5 segundos
def auto_clicker():
    while True:
        if clicking:
            pyautogui.click()
            time.sleep(0.3)
        else:
            time.sleep(0.1)

# Función que inicia o detiene el clic automático al presionar 'P'
def toggle_clicking():
    global clicking
    clicking = not clicking

# Función para salir del programa al presionar '|'
def exit_program():
    print("Saliendo del programa...")
    exit(0)

# Vinculación de teclas
keyboard.add_hotkey('p', toggle_clicking)
keyboard.add_hotkey('|', exit_program)

# Hilo para el clic automático
click_thread = threading.Thread(target=auto_clicker)
click_thread.daemon = True
click_thread.start()

print("Presiona 'P' para iniciar/detener el clic automático.")
print("Presiona '|' para cerrar el programa.")

# Mantén el programa corriendo
keyboard.wait()
