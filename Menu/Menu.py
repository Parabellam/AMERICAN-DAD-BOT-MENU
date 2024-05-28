import tkinter as tk
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent / 'Events' / 'MananaMimosaEvent'))
sys.path.append(str(Path(__file__).resolve().parent.parent / 'ToolTip'))
sys.path.append(str(Path(__file__).resolve().parent.parent / 'ManageJSON'))
sys.path.append(str(Path(__file__).resolve().parent.parent / 'TelegramLogs'))

from MananaMimosaEvent import function_join_mananamimosa
from ToolTip import ToolTip 
from ManageJSONFile import save_to_json, get_value_from_json
from TelegramLogs import create_telegram_console

def main_window():
    root = tk.Tk()
    root.title("Interfaz de Botones")
    root.geometry("500x600")
    return root

def add_description(frame):
    description = tk.Label(frame, text="Antes de elegir alguna función, su pantalla debe de estar ubicada en la casa o en el mapa principal del juego.",
                           wraplength=450, justify='center', font=('Helvetica', 12, 'italic'))
    description.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

def format_number(entry):
    value = entry.get().replace('.', '')
    if value.isdigit():
        formatted_value = "{:,}".format(int(value)).replace(',', '.')
        entry.delete(0, tk.END)
        entry.insert(0, formatted_value)

def add_food_capacity_input(frame):
    label = tk.Label(frame, text="Capacidad de almacen de comida:", font=('Helvetica', 9))
    label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    entry = tk.Entry(frame, width=15, font=('Helvetica', 12))
    entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    entry.bind("<KeyRelease>", lambda event: (check_food_capacity(entry, buttons), format_number(entry)))
    return entry

def action_buttons(frame):
    button1 = tk.Button(frame, text="Mañana Mimosa", command=function_join_mananamimosa, width=20, height=2, bg='lightgrey', fg='black', font=('Helvetica', 12, 'bold'), state='disabled')
    button1.grid(row=2, column=0, padx=10, pady=10)
    ToolTip(button1, "Para este evento se consumirá la comida si esta es mayor al 50% de tu capacidad. Por el contrario, usará los tickets hasta acabarlos y finalizará. Próximamente se podrá configurar este 50% mencionado.", width=300)
    
    button2 = tk.Button(frame, text="Guerra Familialandia", command=function_join_mananamimosa, width=20, height=2, bg='lightgrey', fg='black', font=('Helvetica', 12, 'bold'), state='disabled')
    button2.grid(row=2, column=1, padx=10, pady=10)
    
    button3 = tk.Button(frame, text="General", command=function_join_mananamimosa, width=20, height=2, bg='lightgrey', fg='black', font=('Helvetica', 12, 'bold'), state='disabled')
    button3.grid(row=3, column=0, padx=10, pady=10)
    ToolTip(button3, "Hacer todas las actividades diarias.", width=300)
    
    return [button1, button2, button3]

def finish():
    print("Cerrando")
    root.destroy()

def close_app_button(frame):
    start_button = tk.Button(frame, text="Cerrar", command=finish, width=20, height=2, bg='lightcoral', fg='white', font=('Helvetica', 12, 'bold'))
    start_button.grid(row=4, column=0, columnspan=2, pady=20)

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
add_description(frame)
food_capacity_entry = add_food_capacity_input(frame)
buttons = action_buttons(frame)

stored_value = get_value_from_json("q6w5f4weg54er584")
if stored_value:
    food_capacity_entry.insert(0, stored_value)
    check_food_capacity(food_capacity_entry, buttons)
else:
    print("No se ha podido obtener el máximo de comida almacenada")
    check_food_capacity(food_capacity_entry, buttons)

close_app_button(frame)
create_telegram_console(root)

root.mainloop()