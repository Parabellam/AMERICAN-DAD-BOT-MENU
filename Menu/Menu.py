import tkinter as tk
import sys
from pathlib import Path
# import threading

sys.path.append(str(Path(__file__).resolve().parent.parent / 'Events' / 'MananaMimosaEvent'))
sys.path.append(str(Path(__file__).resolve().parent.parent / 'ToolTip'))
sys.path.append(str(Path(__file__).resolve().parent.parent / 'ManageJSON'))
sys.path.append(str(Path(__file__).resolve().parent.parent / 'TelegramLogs'))

from MananaMimosaEvent import function_join_mananamimosa
from ToolTip import ToolTip 
from ManageJSONFile import save_to_json, get_value_from_json
from TelegramLogs import create_telegram_console
from TelegramLogs import custom_print

# Variable global para la señal de interrupción
# stop_event = threading.Event()

def main_window():
    root = tk.Tk()
    root.title("Interfaz de Botones")
    root.geometry("500x600")
    return root

def format_number(entry):
    value = entry.get().replace('.', '')
    if value.isdigit():
        formatted_value = "{:,}".format(int(value)).replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, formatted_value)

def add_food_capacity_input(frame):
    label = tk.Label(frame, text="Capacidad de almacen de comida:", font=('Helvetica', 9))
    label.grid(row=1, column=1, padx=10, pady=10, sticky='e')
    entry = tk.Entry(frame, width=15, font=('Helvetica', 12))
    entry.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    entry.bind("<KeyRelease>", lambda event: (check_food_capacity(entry, buttons), format_number(entry)))
    return entry

def add_checkbox(frame):
    checkbox_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(frame, text="¿Hay recompensas en el chat?", variable=checkbox_var, font=('Helvetica', 9))
    checkbox.grid(row=2, column=1, columnspan=2, pady=10)
    return checkbox_var

def add_night_checkbox(frame):
    night_checkbox_var = tk.BooleanVar()
    night_checkbox = tk.Checkbutton(frame, text="Modo noche (Solo llamados de actividad sospechosa)", variable=night_checkbox_var, font=('Helvetica', 9))
    night_checkbox.grid(row=3, column=0, columnspan=2, pady=10)
    return night_checkbox_var

def add_save_checkbox(frame):
    save_checkbox_var = tk.BooleanVar()
    save_checkbox = tk.Checkbutton(frame, text="Modo save tickets (Solo llamados de actividad sospechosa)", variable=save_checkbox_var, font=('Helvetica', 9))
    save_checkbox.grid(row=4, column=0, columnspan=2, pady=10)
    return save_checkbox_var

def add_family_war_checkbox(frame):
    family_war_checkbox_var = tk.BooleanVar()
    family_war_checkbox = tk.Checkbutton(frame, text="Family war", variable=family_war_checkbox_var, font=('Helvetica', 9))
    family_war_checkbox.grid(row=5, column=0, columnspan=2, pady=10)
    return family_war_checkbox_var

def action_buttons(frame, isThereRewards, isNightMode, isSaveMode, checkFamilyWar):
    button1 = tk.Button(frame, text="Mañana Mimosa", command=lambda: function_join_mananamimosa(isThereRewards.get(), isNightMode.get(), isSaveMode.get(), checkFamilyWar.get()), width=20, height=2, bg='lightgrey', fg='black', font=('Helvetica', 12, 'bold'), state='disabled')
    button1.grid(row=6, column=0, padx=10, pady=10)
    ToolTip(button1, "Para este evento se consumirá la comida si esta es mayor al 50% de tu capacidad. Por el contrario, usará los tickets hasta acabarlos y finalizará. Próximamente se podrá configurar este 50% mencionado.", width=300)
    
    return [button1]

# def function_wrapper(isThereRewards, isNightMode, isSaveMode, checkFamilyWar):
#     # Asegúrate de que function_join_mananamimosa revise stop_event periódicamente.
#     function_join_mananamimosa(isThereRewards, isNightMode, isSaveMode, checkFamilyWar, stop_event)

def finish():
    custom_print("Cerrando")
    # stop_event.set()  # Envía la señal de detenerse a todos los hilos
    root.destroy()

def close_app_button(frame):
    start_button = tk.Button(frame, text="Cerrar", command=finish, width=20, height=2, bg='lightcoral', fg='white', font=('Helvetica', 12, 'bold'))
    start_button.grid(row=8, column=0, columnspan=2, pady=20)

def check_food_capacity(entry, buttons):
    capacity = entry.get().replace('.', '').strip()
    if capacity.isdigit() and int(capacity) > 0:
        for button in buttons:
            button.config(state='normal', bg='lightblue')
        save_to_json("q6w5f4weg54er584", capacity)
    else:
        for button in buttons:
            button.config(state='disabled', bg='lightgrey')


root = main_window()
frame = tk.Frame(root)
frame.pack(pady=20)
food_capacity_entry = add_food_capacity_input(frame)
isThereRewards = add_checkbox(frame)
isNightMode = add_night_checkbox(frame)
isSaveMode = add_save_checkbox(frame)
checkFamilyWar = add_family_war_checkbox(frame)
buttons = action_buttons(frame, isThereRewards, isNightMode, isSaveMode, checkFamilyWar)

stored_value = get_value_from_json("q6w5f4weg54er584")
if stored_value:
    food_capacity_entry.insert(0, stored_value)
    check_food_capacity(food_capacity_entry, buttons)
else:
    custom_print("No se ha podido obtener el máximo de comida almacenada")
    check_food_capacity(food_capacity_entry, buttons)

close_app_button(frame)
console_text = create_telegram_console(root)

# Cerrar la aplicación después de 4 horas (4 horas * 60 minutos * 60 segundos * 1000 milisegundos)
# root.after(4 * 60 * 60 * 1000, finish)

custom_print("Aplicación iniciada")
root.mainloop()