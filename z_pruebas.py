import json
import os

# Ruta del archivo JSON
inventory_file = 'inventory.json'

# Cargar inventario desde el archivo JSON
def cargar_inventario():
    if os.path.exists(inventory_file):
        with open(inventory_file, 'r') as file:
            return json.load(file)
    else:
        return {}

# Guardar inventario en el archivo JSON
def guardar_inventario(inventario):
    with open(inventory_file, 'w') as file:
        json.dump(inventario, file, indent=4)

# Añadir producto
def añadir_producto(inventario):
    nombre = input("Ingrese el nombre del producto: ")
    cantidad = int(input("Ingrese la cantidad disponible: "))
    precio = float(input("Ingrese el precio unitario: "))
    
    inventario[nombre] = {'cantidad': cantidad, 'precio': precio}
    print(f"Producto '{nombre}' añadido.")

# Actualizar producto
def actualizar_producto(inventario):
    nombre = input("Ingrese el nombre del producto a actualizar: ")
    if nombre in inventario:
        cantidad = int(input("Ingrese la nueva cantidad disponible: "))
        precio = float(input("Ingrese el nuevo precio unitario: "))
        
        inventario[nombre]['cantidad'] = cantidad
        inventario[nombre]['precio'] = precio
        print(f"Producto '{nombre}' actualizado.")
    else:
        print("Producto no encontrado.")

# Eliminar producto
def eliminar_producto(inventario):
    nombre = input("Ingrese el nombre del producto a eliminar: ")
    if nombre in inventario:
        del inventario[nombre]
        print(f"Producto '{nombre}' eliminado.")
    else:
        print("Producto no encontrado.")

# Mostrar inventario
def mostrar_inventario(inventario):
    if not inventario:
        print("El inventario está vacío.")
    else:
        print("Productos en inventario:")
        for nombre, detalles in inventario.items():
            print(f"Nombre: {nombre}, Cantidad: {detalles['cantidad']}, Precio: {detalles['precio']}")

# Menú principal
def menu():
    inventario = cargar_inventario()
    
    while True:
        print("\nSeleccione una opción:")
        print("1. Añadir un nuevo producto")
        print("2. Actualizar un producto existente")
        print("3. Eliminar un producto")
        print("4. Mostrar todos los productos")
        print("5. Salir")
        
        opción = input("Ingrese su opción (1-5): ")
        
        if opción == '1':
            añadir_producto(inventario)
        elif opción == '2':
            actualizar_producto(inventario)
        elif opción == '3':
            eliminar_producto(inventario)
        elif opción == '4':
            mostrar_inventario(inventario)
        elif opción == '5':
            guardar_inventario(inventario)
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

# Ejecutar el programa
menu()