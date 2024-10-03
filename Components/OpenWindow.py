import pygetwindow as gw
from time import sleep

from TelegramLogs import custom_print

def open():
    try:
        windows = gw.getWindowsWithTitle('BlueStacks')
        if windows:
            bluestacks_window = windows[0]

            # Verificar si la ventana está minimizada
            if bluestacks_window.isMinimized:
                bluestacks_window.restore()

            # Activar la ventana
            bluestacks_window.activate()

            # Maximizar la ventana
            # Pequeña pausa para asegurarse de que la ventana se activa antes de maximizarla
            sleep(0.1)
            bluestacks_window.maximize()

            return True
        else:
            custom_print("La ventana de BlueStacks no se encontró.")
            return False

    except gw.PyGetWindowException as e:
        custom_print(f"Error al intentar manipular la ventana de BlueStacks: {e}")
        return False


def open_bluestacks_window():
    resp = open()
    return resp
