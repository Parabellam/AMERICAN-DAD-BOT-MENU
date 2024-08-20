import os
import requests
import tkinter as tk
import sys
import threading
import queue
from requests.exceptions import ConnectionError, Timeout
import time

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
            print(f"Error de conexión: {e}. Reintentando ({retries}/{MAX_RETRIES})...")
            if retries < MAX_RETRIES:
                time.sleep(RETRY_DELAY * retries)
            else:
                print("No se pudo enviar el mensaje después de varios intentos.")
        except Exception as e:
            print(f"Error inesperado: {e}")
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


class TelegramConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""

    def write(self, message):
        try:
            if self.text_widget.winfo_exists():
                self.text_widget.insert(tk.END, message)
                self.text_widget.see(tk.END)
                self.buffer += message
                if '\n' in self.buffer:
                    enqueue_telegram_message(self.buffer.strip())
                    self.buffer = ""
            else:
                sys.__stdout__.write("El widget de texto no existe\n")
        except Exception as e:
            sys.__stdout__.write(f"Error al escribir en el widget de texto: {e}\n")

    def flush(self):
        if self.buffer:
            enqueue_telegram_message(self.buffer.strip())
            self.buffer = ""


    def flush(self):
        if self.buffer:
            enqueue_telegram_message(self.buffer.strip())
            self.buffer = ""



def create_telegram_console(root):
    console_frame = tk.Frame(root, bg='black')
    console_frame.pack(fill=tk.BOTH, expand=True)
    console_text = tk.Text(console_frame, bg='black', fg='white', wrap='word')
    console_text.pack(fill=tk.BOTH, expand=True)
    sys.stdout = TelegramConsoleRedirector(console_text)
    return console_text
