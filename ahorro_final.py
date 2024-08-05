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
            if os.path.exists("usuarios.json") and os.stat("usuarios.json").st_size > 0:
                with open(f"usuarios.json", "r") as archivo:
                    usuarios = json.load(archivo)
            else:
                usuarios = {}

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
        
        if os.path.exists("usuarios.json") and os.stat("usuarios.json").st_size > 0:
            with open(f"usuarios.json", "r") as archivo:
                usuarios = json.load(archivo)
        else:
            usuarios = {}

        if usuario in usuarios and usuarios[usuario] == contrasena:
            usuario_actual = usuario
            cargar_datos()
            messagebox.showinfo("Info", f"Bienvenidx {usuario_actual}")
            ventana_login.destroy()
            mostrar_menu_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    ttk.Button(frame, text="Iniciar Sesión", command=verificar_usuario).pack(pady=10)

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
            messagebox.showinfo("Info", f"Bienvenidx {usuario_actual}")
            ventana_login.destroy()
            mostrar_menu_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    ttk.Button(frame, text="Iniciar Sesión", command=verificar_usuario).pack(pady=10)

# Función para configurar el saldo inicial
def configurar_saldo_inicial():
    ventana_saldo = tk.Toplevel(root)
    ventana_saldo.title("Introduzca el Saldo Inicial")
    
    frame = ttk.Frame(ventana_saldo, padding="10")
    frame.pack(fill="both", expand=True)
    
    ttk.Label(frame, text="Saldo Inicial").pack(pady=5)
    saldo_entry = ttk.Entry(frame)
    saldo_entry.pack(pady=5)
    

def editar_saldo():
    ventana_saldo = tk.Toplevel(root)
    ventana_saldo.title("Editar Saldo")

    frame = ttk.Frame(ventana_saldo, padding="10")
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Saldo Actual").pack(pady=5)
    saldo_entry = ttk.Entry(frame)
    saldo_entry.insert(0, saldo_actual)  # Mostrar el saldo actual en el entry
    saldo_entry.pack(pady=5)

    def guardar_saldo():
        try:
            global saldo_actual
            saldo_actual = float(saldo_entry.get())
            messagebox.showinfo("Info", "Saldo actualizado con éxito")
            ventana_saldo.destroy()
            guardar_datos()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un número válido")

    ttk.Button(frame, text="Guardar", command=guardar_saldo).pack(pady=10)

# Función para mostrar el menú principal
def mostrar_menu_principal():
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    ttk.Label(main_frame, text="Gestor de Dinero y Gastos", font=("Cambria", 16)).pack(pady=10)
    ttk.Button(main_frame, text="Registrar Gasto", command=registrar_gasto).pack(pady=10)
    ttk.Button(main_frame, text="Eliminar Gasto", command=eliminar_gasto).pack(pady=10)
    ttk.Button(main_frame, text="Ver Saldo", command=ver_saldo).pack(pady=10)
    ttk.Button(main_frame, text="Ver Gastos", command=ver_gastos).pack(pady=10)
    ttk.Button(main_frame, text="Calendario de Gastos", command=ver_calendario).pack(pady=10)
    ttk.Button(main_frame, text="Gráfico de Categorías", command=mostrar_grafico_categorias).pack(pady=10)
    ttk.Button(main_frame, text="Resetear Presupuesto", command=resetear_presupuesto).pack(pady=10)
    ttk.Button(main_frame, text="Configurar Presupuesto", command=configurar_presupuesto).pack(pady=10)
    ttk.Button(main_frame, text="Generar Reporte", command=generar_reporte).pack(pady=10)
    ttk.Button(main_frame, text="Editar Saldo", command=editar_saldo).pack(pady=10)
    # Solo mostrar "Configurar Presupuesto" si ha pasado un mes desde la fecha de inicio
    if datetime.now() >= fecha_inicio + timedelta(days=30):
        ttk.Button(main_frame, text="Configurar Presupuesto", command=configurar_presupuesto).pack(pady=10)

# Función para registrar un gasto
def registrar_gasto():
    ventana_gasto = tk.Toplevel(root)
    ventana_gasto.title("Registrar Gasto")
    
    frame = ttk.Frame(ventana_gasto, padding="10")
    frame.pack(fill="both", expand=True)
    
    ttk.Label(frame, text="Descripción").pack(pady=5)
    descripcion_entry = ttk.Entry(frame)
    descripcion_entry.pack(pady=5)
    
    ttk.Label(frame, text="Costo").pack(pady=5)
    costo_entry = ttk.Entry(frame)
    costo_entry.pack(pady=5)
    
    ttk.Label(frame, text="Fecha (dd/mm/yyyy)").pack(pady=5)
    fecha_entry = ttk.Entry(frame)
    fecha_entry.pack(pady=5)
    
    ttk.Label(frame, text="Categoría").pack(pady=5)
    categorias = ["Comida", "Camila", "Transporte", "Servicios", "Tarjetas", "Deudas", "Porro", "Compras"]
    categoria_combobox = ttk.Combobox(frame, values=categorias)
    categoria_combobox.pack(pady=5)
    
    def guardar_gasto():
        descripcion = descripcion_entry.get()
        try:
            costo = float(costo_entry.get())
            fecha = datetime.strptime(fecha_entry.get(), "%d/%m/%Y")
            categoria = categoria_combobox.get()
            global saldo_actual
            saldo_actual -= costo
            gastos.append({"descripcion": descripcion, "costo": costo, "fecha": fecha, "categoria": categoria})
            messagebox.showinfo("Info", "Gasto registrado con éxito")
            ventana_gasto.destroy()
            guardar_datos()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese datos válidos")
    
    ttk.Button(frame, text="Guardar", command=guardar_gasto).pack(pady=10)

# Función para eliminar un gasto
def eliminar_gasto():
    ventana_eliminar = tk.Toplevel(root)
    ventana_eliminar.title("Eliminar Gasto")
    
    frame = ttk.Frame(ventana_eliminar, padding="10")
    frame.pack(fill="both", expand=True)
    
    ttk.Label(frame, text="Seleccione el gasto a eliminar:").pack(pady=5)
    
    gasto_listbox = tk.Listbox(frame)
    gasto_listbox.pack(pady=5)
    
    for idx, gasto in enumerate(gastos):
        gasto_listbox.insert(idx, f"{gasto['fecha'].strftime('%d/%m/%Y')} - {gasto['descripcion']} - ${gasto['costo']}")
    
    def eliminar_seleccionado():
        try:
            seleccion = gasto_listbox.curselection()[0]
            gasto = gastos.pop(seleccion)
            global saldo_actual
            saldo_actual += gasto["costo"]
            messagebox.showinfo("Info", "Gasto eliminado con éxito")
            ventana_eliminar.destroy()
            guardar_datos()
        except IndexError:
            messagebox.showerror("Error", "Por favor, seleccione un gasto a eliminar")
    
    ttk.Button(frame, text="Eliminar", command=eliminar_seleccionado).pack(pady=10)

# Función para ver el saldo actual
def ver_saldo():
    messagebox.showinfo("Saldo Actual", f"Saldo actual: ${saldo_actual:.2f}")

# Función para ver todos los gastos
def ver_gastos():
    ventana_gastos = tk.Toplevel(root)
    ventana_gastos.title("Gastos Registrados")
    
    frame = ttk.Frame(ventana_gastos, padding="10")
    frame.pack(fill="both", expand=True)
    
    text_area = tk.Text(frame, wrap="word", width=50, height=15)
    text_area.pack(pady=5)
    
    for gasto in gastos:
        text_area.insert("end", f"{gasto['fecha'].strftime('%d/%m/%Y')} - {gasto['descripcion']} - ${gasto['costo']} - {gasto['categoria']}\n")
    
    text_area.config(state="disabled")

# Función para ver el calendario de gastos
def ver_calendario():
    ventana_calendario = tk.Toplevel(root)
    ventana_calendario.title("Calendario de Gastos")
    
    frame = ttk.Frame(ventana_calendario, padding="10")
    frame.pack(fill="both", expand=True)
    
    cal = Calendar(frame, selectmode="day")
    cal.pack(pady=5)
    
    def mostrar_gastos_dia():
        fecha_seleccionada = cal.selection_get()
        gastos_dia = [gasto for gasto in gastos if gasto["fecha"].date() == fecha_seleccionada]
        if gastos_dia:
            texto_gastos = "\n".join([f"{gasto['descripcion']} - ${gasto['costo']} - {gasto['categoria']}" for gasto in gastos_dia])
        else:
            texto_gastos = "No hay gastos registrados en esta fecha"
        messagebox.showinfo(f"Gastos del {fecha_seleccionada.strftime('%d/%m/%Y')}", texto_gastos)
    
    ttk.Button(frame, text="Ver Gastos del Día", command=mostrar_gastos_dia).pack(pady=10)

# Función para mostrar el gráfico de categorías
def mostrar_grafico_categorias():
    categorias = {}
    for gasto in gastos:
        if gasto["categoria"] in categorias:
            categorias[gasto["categoria"]] += gasto["costo"]
        else:
            categorias[gasto["categoria"]] = gasto["costo"]
    
    if categorias:
        plt.figure(figsize=(10, 5))
        plt.pie(categorias.values(), labels=categorias.keys(), autopct="%1.1f%%", startangle=140)
        plt.title("Distribución de Gastos por Categoría")
        plt.show()
    else:
        messagebox.showinfo("Info", "No hay gastos registrados para generar el gráfico")

# Función para resetear el presupuesto
def resetear_presupuesto():
    global saldo_actual, gastos
    saldo_actual = 0.0
    gastos = []
    guardar_datos()
    messagebox.showinfo("Info", "Presupuesto reseteado con éxito")

# Función para configurar el presupuesto
def configurar_presupuesto():
    ventana_presupuesto = tk.Toplevel(root)
    ventana_presupuesto.title("Configurar Presupuesto")
    
    frame = ttk.Frame(ventana_presupuesto, padding="10")
    frame.pack(fill="both", expand=True)
    
    ttk.Label(frame, text="Ingrese el saldo inicial").pack(pady=5)
    saldo_entry = ttk.Entry(frame)
    saldo_entry.pack(pady=5)
    
    def guardar_presupuesto():
        try:
            global saldo_actual
            saldo_actual = float(saldo_entry.get())
            messagebox.showinfo("Info", "Presupuesto configurado con éxito")
            ventana_presupuesto.destroy()
            guardar_datos()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un número válido")
    
    ttk.Button(frame, text="Guardar", command=guardar_presupuesto).pack(pady=10)

# Función para generar un reporte de gastos
def generar_reporte():
    ventana_reporte = tk.Toplevel(root)
    ventana_reporte.title("Generar Reporte")
    
    frame = ttk.Frame(ventana_reporte, padding="10")
    frame.pack(fill="both", expand=True)
    
    ttk.Label(frame, text="Seleccione el rango de fechas para el reporte").pack(pady=5)
    
    ttk.Label(frame, text="Fecha de Inicio (dd/mm/yyyy)").pack(pady=5)
    fecha_inicio_entry = ttk.Entry(frame)
    fecha_inicio_entry.pack(pady=5)
    
    ttk.Label(frame, text="Fecha de Fin (dd/mm/yyyy)").pack(pady=5)
    fecha_fin_entry = ttk.Entry(frame)
    fecha_fin_entry.pack(pady=5)
    
    def generar():
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_entry.get(), "%d/%m/%Y")
            fecha_fin = datetime.strptime(fecha_fin_entry.get(), "%d/%m/%Y")
            gastos_reporte = [gasto for gasto in gastos if fecha_inicio <= gasto["fecha"] <= fecha_fin]
            if gastos_reporte:
                with open(f"reporte_{fecha_inicio.strftime('%Y%m%d')}_{fecha_fin.strftime('%Y%m%d')}.txt", "w") as archivo:
                    for gasto in gastos_reporte:
                        archivo.write(f"{gasto['fecha'].strftime('%d/%m/%Y')} - {gasto['descripcion']} - ${gasto['costo']} - {gasto['categoria']}\n")
                messagebox.showinfo("Info", "Reporte generado con éxito")
            else:
                messagebox.showinfo("Info", "No hay gastos registrados en el rango de fechas seleccionado")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese fechas válidas")
    
    ttk.Button(frame, text="Generar", command=generar).pack(pady=10)

# Función para mostrar la pantalla de inicio de sesión/registro
def mostrar_pantalla_inicio():
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    ttk.Label(main_frame, text="Bienvenidx", font=("Cambria", 16)).pack(pady=10)
    ttk.Button(main_frame, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)
    ttk.Button(main_frame, text="Registrar Usuario", command=registrar_usuario).pack(pady=10)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestor de Dinero y Gastos")
root.geometry("400x500")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

# Verificar si existe el archivo de usuarios, sino crearlo
if not os.path.exists("usuarios.json"):
    with open("usuarios.json", "w") as archivo:
        json.dump({}, archivo)

mostrar_pantalla_inicio()  # Mostrar la pantalla de inicio al iniciar la aplicación

root.mainloop()
