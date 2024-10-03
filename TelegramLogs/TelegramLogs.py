import os
import requests
import tkinter as tk
import sys
import threading
import queue
from requests.exceptions import ConnectionError, Timeout
from time import sleep

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

log_queue = queue.Queue()

MAX_RETRIES = 100
RETRY_DELAY = 5

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            break
        except (ConnectionError, Timeout) as e:
            retries += 1
            custom_print(f"Error de conexión: {e}. Reintentando ({retries}/{MAX_RETRIES})...", send_to_telegram = False)
            if retries < MAX_RETRIES:
                sleep(RETRY_DELAY * retries)
            else:
                custom_print("No se pudo enviar el mensaje después de varios intentos.", send_to_telegram = False)
        except Exception as e:
            custom_print(f"Error inesperado: {e}", send_to_telegram = False)
            break


def telegram_worker():
    while True:
        message = log_queue.get()
        if message is None:
            break
        send_telegram_message(message)
        log_queue.task_done()


threading.Thread(target=telegram_worker, daemon=True).start()


def enqueue_telegram_message(message):
    log_queue.put(message)


def custom_print(message, send_to_telegram=True):
    # Imprime el mensaje en la consola estándar
    sys.__stdout__.write(message + '\n')
    
    # Si send_to_telegram es True, encola el mensaje para enviar a Telegram
    if send_to_telegram:
        enqueue_telegram_message(message)

# Modifica la clase TelegramConsoleRedirector
class TelegramConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""

    def write(self, message):
        try:
            # Escribe en el widget de texto de Tkinter
            if self.text_widget.winfo_exists():
                self.text_widget.insert(tk.END, message)
                self.text_widget.see(tk.END)
            
            # También imprime en la consola estándar
            sys.__stdout__.write(message)
        except Exception as e:
            sys.__stdout__.write(f"Error al escribir en el widget de texto: {e}\n")

    def flush(self):
        pass

def create_telegram_console(root):
    console_frame = tk.Frame(root, bg='black')
    console_frame.pack(fill=tk.BOTH, expand=True)
    console_text = tk.Text(console_frame, bg='black', fg='white', wrap='word')
    console_text.pack(fill=tk.BOTH, expand=True)
    sys.stdout = TelegramConsoleRedirector(console_text)
    return console_text
