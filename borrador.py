import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt
import os

# Variables globales para almacenar saldo y gastos
saldo_actual = 0.0
gastos = []
fecha_inicio = datetime.now()
usuario_actual = None

# Función para guardar los datos del usuario en un archivo JSON
def guardar_datos():
    if usuario_actual is None:
        return

    datos = {
        "saldo_actual": saldo_actual,
        "gastos": [
            {
                "descripcion": gasto["descripcion"],
                "costo": gasto["costo"],
                "fecha": gasto["fecha"].strftime("%Y-%m-%d %H:%M:%S"),
                "categoria": gasto["categoria"]
            } for gasto in gastos
        ]
    }
    with open(f"datos_{usuario_actual}.json", "w") as archivo:
        json.dump(datos, archivo)

# Función para cargar los datos del usuario desde un archivo JSON
def cargar_datos():
    global saldo_actual, gastos
    if usuario_actual is None:
        return

    try:
        with open(f"datos_{usuario_actual}.json", "r") as archivo:
            datos = json.load(archivo)
            saldo_actual = datos["saldo_actual"]
            gastos = [
                {
                    "descripcion": gasto["descripcion"],
                    "costo": gasto["costo"],
                    "fecha": datetime.strptime(gasto["fecha"], "%Y-%m-%d %H:%M:%S"),
                    "categoria": gasto["categoria"]
                } for gasto in datos["gastos"]
            ]
    except FileNotFoundError:
        pass

# Función para registrar un nuevo usuario
def registrar_usuario():
    ventana_registro = tk.Toplevel(root)
    ventana_registro.title("Registrar Usuario")

    frame = ttk.Frame(ventana_registro, padding="10")
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Nombre de Usuario").pack(pady=5)
    usuario_entry = ttk.Entry(frame)
    usuario_entry.pack(pady=5)

    ttk.Label(frame, text="Contraseña").pack(pady=5)
    contrasena_entry = ttk.Entry(frame, show="*")
    contrasena_entry.pack(pady=5)

    def guardar_usuario():
        usuario = usuario_entry.get()
        contrasena = contrasena_entry.get()
        if usuario and contrasena:
            with open(f"usuarios.json", "r") as archivo:
                usuarios = json.load(archivo)
            if usuario in usuarios:
                messagebox.showerror("Error", "El usuario ya existe.")
            else:
                usuarios[usuario] = contrasena
                with open(f"usuarios.json", "w") as archivo:
                    json.dump(usuarios, archivo)
                messagebox.showinfo("Info", "Usuario registrado con éxito")
                ventana_registro.destroy()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    ttk.Button(frame, text="Registrar", command=guardar_usuario).pack(pady=10)

# Función para iniciar sesión
def iniciar_sesion():
    ventana_login = tk.Toplevel(root)
    ventana_login.title("Iniciar Sesión")

    frame = ttk.Frame(ventana_login, padding="10")
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Nombre de Usuario").pack(pady=5)
    usuario_entry = ttk.Entry(frame)
    usuario_entry.pack(pady=5)

    ttk.Label(frame, text="Contraseña").pack(pady=5)
    contrasena_entry = ttk.Entry(frame, show="*")
    contrasena_entry.pack(pady=5)

    def verificar_usuario():
        global usuario_actual
        usuario = usuario_entry.get()
        contrasena = contrasena_entry.get()
        with open(f"usuarios.json", "r") as archivo:
            usuarios = json.load(archivo)
        if usuario in usuarios and usuarios[usuario] == contrasena:
            usuario_actual = usuario
            cargar_datos()
            messagebox.showinfo("Info", f"Bienvenido {usuario_actual}")
            ventana_login.destroy()
            mostrar_menu_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    ttk.Button(frame, text="Iniciar Sesión", command=verificar_usuario).pack(pady=10)

# Inicializa la ventana principal de Tkinter
root = tk.Tk()
root.title("Gestor de Dinero y Gastos")
root.geometry("800x900")

# Verificar si el archivo de usuarios existe, si no, crear uno
if not os.path.exists("usuarios.json"):
    with open("usuarios.json", "w") as archivo:
        json.dump({}, archivo)

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc", font=("Cambria", 10), foreground="black")
style.configure("TLabel", padding=6, background="black", font=("Cambria", 12), foreground="white")
style.configure("TFrame", background="black")

# Crear frame principal
main_frame = ttk.Frame(root, padding="20", style="TFrame")

# Mostrar pantalla de inicio de sesión
def mostrar_pantalla_inicio():
    for widget in main_frame.winfo_children():
        widget.destroy()

    ttk.Label(main_frame, text="Gestor de Dinero y Gastos", font=("Cambria", 16)).pack(pady=10)
    ttk.Button(main_frame, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)
    ttk.Button(main_frame, text="Registrar Usuario", command=registrar_usuario).pack(pady=10)

mostrar_pantalla_inicio()

main_frame.pack(fill="both", expand=True)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
