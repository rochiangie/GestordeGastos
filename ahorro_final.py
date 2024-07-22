import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt

# Variables globales para almacenar saldo y gastos
saldo_actual = 0.0
gastos = []
fecha_inicio = datetime.now()

# Función para guardar los datos en un archivo JSON
def guardar_datos():
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
    with open("datos.json", "w") as archivo:
        json.dump(datos, archivo)

# Función para cargar los datos desde un archivo JSON
def cargar_datos():
    global saldo_actual, gastos
    try:
        with open("datos.json", "r") as archivo:
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

# Botón para editar el saldo
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
    if not gastos:
        messagebox.showinfo("Info", "No hay gastos registrados para eliminar.")
        return
    
    ventana_eliminar = tk.Toplevel(root)
    ventana_eliminar.title("Eliminar Gasto")
    
    frame = ttk.Frame(ventana_eliminar, padding="10")
    frame.pack(fill="both", expand=True)
    
    ttk.Label(frame, text="Selecciona el gasto a eliminar:").pack(pady=10)
    
    gastos_descripcion = [f"{gasto['descripcion']} ({gasto['categoria']}) - ${gasto['costo']:.2f}" for gasto in gastos]
    gasto_combobox = ttk.Combobox(frame, values=gastos_descripcion)
    gasto_combobox.pack(pady=10)
    
    def confirmar_eliminar():
        seleccion = gasto_combobox.get()
        for gasto in gastos:
            if seleccion == f"{gasto['descripcion']} ({gasto['categoria']}) - ${gasto['costo']:.2f}":
                gastos.remove(gasto)
                global saldo_actual
                saldo_actual += gasto["costo"]  # Revertir el costo eliminado al saldo
                messagebox.showinfo("Info", "Gasto eliminado correctamente.")
                ventana_eliminar.destroy()
                guardar_datos()
                return
    
    ttk.Button(frame, text="Eliminar", command=confirmar_eliminar).pack(pady=10)

# Función para ver el saldo
def ver_saldo():
    messagebox.showinfo("Saldo Actual", f"Tu saldo actual es: ${saldo_actual:.2f}")

# Función para ver los gastos en una lista
def ver_gastos():
    ventana_gastos = tk.Toplevel(root)
    ventana_gastos.title("Gastos Registrados")
    
    frame = ttk.Frame(ventana_gastos, padding="10")
    frame.pack(fill="both", expand=True)
    
    for gasto in gastos:
        ttk.Label(frame, text=f"{gasto['fecha'].strftime('%d/%m/%Y')} - {gasto['descripcion']} ({gasto['categoria']}): ${gasto['costo']:.2f}").pack(pady=2)

# Función para ver los gastos en un calendario
def ver_calendario():
    ventana_calendario = tk.Toplevel(root)
    ventana_calendario.title("Calendario de Gastos")
    
    frame = ttk.Frame(ventana_calendario, padding="10")
    frame.pack(fill="both", expand=True)
    
    cal = Calendar(frame, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    cal.pack(pady=20)
    
    gastos_fecha = tk.StringVar()
    ttk.Label(frame, textvariable=gastos_fecha, background="black", foreground="white").pack(pady=5)
    
    def mostrar_gastos(event):
        fecha_seleccionada = cal.selection_get()
        gastos_en_fecha = [gasto for gasto in gastos if gasto['fecha'].date() == fecha_seleccionada]
        texto_gastos = "\n".join([f"{gasto['descripcion']} ({gasto['categoria']}): ${gasto['costo']:.2f}" for gasto in gastos_en_fecha])
        gastos_fecha.set(texto_gastos)
    
    cal.bind("<<CalendarSelected>>", mostrar_gastos)

# Función para configurar el presupuesto
def configurar_presupuesto():
    ventana_presupuesto = tk.Toplevel(root)
    ventana_presupuesto.title("Configurar Presupuesto")
    
    frame = ttk.Frame(ventana_presupuesto, padding="10")
    frame.pack(fill="both", expand=True)
    
    ttk.Label(frame, text="Presupuesto").pack(pady=5)
    presupuesto_entry = ttk.Entry(frame)
    presupuesto_entry.pack(pady=5)
    
    def guardar_presupuesto():
        try:
            presupuesto = float(presupuesto_entry.get())
            global saldo_actual
            saldo_actual = presupuesto  # Configurar el saldo inicial con el presupuesto
            messagebox.showinfo("Info", "Presupuesto configurado con éxito")
            ventana_presupuesto.destroy()
            guardar_datos()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un número válido")
    
    ttk.Button(frame, text="Guardar", command=guardar_presupuesto).pack(pady=10)

# Función para resetear el presupuesto
def resetear_presupuesto():
    global saldo_actual
    saldo_actual = 0.0
    messagebox.showinfo("Info", "Presupuesto reseteado correctamente a $0.00")
    guardar_datos()

# Función para mostrar el gráfico tipo torta
def mostrar_grafico_categorias():
    if not gastos:
        messagebox.showinfo("Info", "No hay gastos registrados para mostrar en el gráfico.")
        return

    categorias = list(set([gasto["categoria"] for gasto in gastos]))
    total_por_categoria = [sum([gasto["costo"] for gasto in gastos if gasto["categoria"] == cat]) for cat in categorias]

    plt.figure(figsize=(8, 6))
    plt.pie(total_por_categoria, labels=categorias, autopct="%1.1f%%", startangle=140)
    plt.axis("equal")
    plt.title("Distribución de Gastos por Categorías")
    plt.show()

# Función para generar un reporte de gastos
def generar_reporte():
    with open("reporte_gastos.txt", "w") as archivo:
        archivo.write(f"Saldo inicial: ${saldo_actual:.2f}\n\n")
        archivo.write("Gastos registrados:\n\n")
        for gasto in gastos:
            archivo.write(f"Fecha: {gasto['fecha'].strftime('%d/%m/%Y')}\n")
            archivo.write(f"Descripción: {gasto['descripcion']}\n")
            archivo.write(f"Categoría: {gasto['categoria']}\n")
            archivo.write(f"Costo: ${gasto['costo']:.2f}\n\n")
        archivo.write(f"Saldo final: ${saldo_actual:.2f}")
    messagebox.showinfo("Info", "Reporte generado correctamente como 'reporte_gastos.txt'.")

# Función para configurar el fondo con una imagen
def configurar_fondo(root):
    # Carga la imagen de fondo
    ruta_imagen = "gastar.jpg"  # Coloca la ruta correcta de tu imagen
    imagen = Image.open(ruta_imagen)

    # Función para redimensionar la imagen según el tamaño de la ventana
    def redimensionar_imagen(event=None):
        # Obtén las dimensiones de la ventana
        width = root.winfo_width()
        height = root.winfo_height()

        # Redimensiona la imagen al tamaño de la ventana
        imagen_resized = imagen.resize((width, height), Image.LANCZOS)
        fondo_imagen = ImageTk.PhotoImage(imagen_resized)

        # Configura el canvas con la imagen de fondo
        canvas.create_image(0, 0, image=fondo_imagen, anchor="nw")
        canvas.image = fondo_imagen  # Guarda la referencia para evitar el garbage collection

    # Crea el canvas y coloca la imagen de fondo inicial
    canvas = tk.Canvas(root, width=root.winfo_width(), height=root.winfo_height())
    canvas.pack(fill="both", expand=True)
    redimensionar_imagen()

    # Configura el evento para redimensionar la imagen cuando la ventana cambie de tamaño
    root.bind("<Configure>", redimensionar_imagen)

# Inicializa la ventana principal de Tkinter
root = tk.Tk()
root.title("Gestor de Dinero y Gastos")
root.geometry("800x900")

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc", font=("Cambria", 10), foreground="black")
style.configure("TLabel", padding=6, background="black", font=("Cambria", 12), foreground="white")
style.configure("TFrame", background="black")

# Crear frame principal
main_frame = ttk.Frame(root, padding="20", style="TFrame")

# Configurar el fondo
configurar_fondo(root)

main_frame.pack(fill="both", expand=True)

# Botón para introducir el saldo inicial
#ttk.Button(main_frame, text="Configurar Saldo Inicial", command=configurar_saldo_inicial).pack(pady=20)

# Mostrar menú principal
mostrar_menu_principal()

# Cargar datos al iniciar la aplicación
cargar_datos()

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
