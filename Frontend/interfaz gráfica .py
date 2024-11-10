import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, PhotoImage, messagebox
from PIL import Image, ImageTk
import pygame
import pandas as pd

# Inicializar pygame para manejar audio
pygame.mixer.init()

# Variables globales
musica_activa = True
archivo_csv = None
tree = None
pestanaProcesos = False
frame_tabla = None
boton_agregar_fila = None

#Clases a utilizar
class Procesos:
    def __init__(self, tr, ta, ti, tam_b):
        self.tr = tr
        self.ta = ta
        self.ti = ti
        self.tam_b = tam_b
    def __str__(self):
        return f"Proceso(TR={self.tr}, TA={self.ta}, TI={self.ti}, TAM(B)={self.tam_b})"


# Función para reproducir música
def reproducir_musica():
    pygame.mixer.music.load('Frontend/musica.mp3')  # Asegúrate de que la música esté en el mismo directorio
    pygame.mixer.music.play(-1)  # Reproduce en bucle infinito (-1)
# Función para activar y desactivar la música
def toggle_musica():
    global musica_activa
    if musica_activa:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    musica_activa = not musica_activa
# Función para cargar un archivo CSV en memoria
def cargar_csv():
    global archivo_csv, tree, frame_tabla
    archivo_csv = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if archivo_csv:
        df = pd.read_csv(archivo_csv)  # Cargar el archivo CSV en un DataFrame de pandas
        etiqueta_csv.config(text=f"Archivo cargado: {archivo_csv.split('/')[-1]}")  # Mostrar el nombre del archivo en la etiqueta
        if frame_tabla is not None:
            frame_tabla.destroy()
        if boton_agregar_fila is not None:
            boton_agregar_fila.destroy()
        mostrar_csv(df)
# Función para cargar un CSV con solo las etiquetas de columna
def cargar_csv_vacio():
    global tree, frame_tabla
    # Crear DataFrame vacío con las columnas deseadas
    columnas = ["TR", "TA", "TI", "TAM(B)"]
    df = pd.DataFrame(columns=columnas)
    etiqueta_csv.config(text=f"Archivo creado")
    # Limpiar el contenido actual de la tabla, si existe
    if frame_tabla is not None:
        frame_tabla.destroy()
    if boton_agregar_fila is not None:
        boton_agregar_fila.destroy()
    # Mostrar el DataFrame vacío en la tabla
    mostrar_csv(df)
# Añadir una entrada en la tabla de procesos
def add_row():
    # Solicitar datos para cada columna y verificar que no se cancelen
    while True:
        ta = simpledialog.askinteger("Entrada", "Ingrese TA:", parent = notebook)
        if ta is None:
            return  # Salir si se cancela

        ti = simpledialog.askinteger("Entrada", "Ingrese TI:", parent = notebook)
        if ti is None:
            return  # Salir si se cancela

        tam_b = simpledialog.askinteger("Entrada", "Ingrese TAM(B):", parent = notebook)
        if tam_b is None:
            return  # Salir si se cancela
        
        index = len(tree.get_children()) + 1
        # Insertar la fila si todos los datos son válidos
        tree.insert("", "end", values=[index, ta, ti, tam_b, "[X]"])
        break  # Salir del bucle si todo se ingresó correctamente
# Borrar una entrada de la tabla de procesos
def delete_row(event):
    # Obtener la fila seleccionada
    selected_item = tree.selection()
    if selected_item:
        # Verificar si el clic fue en la columna de la casilla "[X]" (última columna)
        col = tree.identify_column(event.x)  # Obtiene la columna bajo el clic
        if col == "#5":  # La columna con el índice 5 es la última, ajusta si es necesario
            tree.delete(selected_item)  # Eliminar la fila
            # Actualizar los índices de las filas restantes
            for idx, item in enumerate(tree.get_children()):
                tree.item(item, values=[idx+1] + list(tree.item(item, "values")[1:]))
# Función para mostrar el contenido del CSV en un Treeview con scrollbar
def mostrar_csv(df):
    global tree  # Asegurarnos de usar la variable global
    global frame_tabla 
    global boton_agregar_fila
    # Crear un frame para contener el Treeview y el scrollbar en tab1

    boton_agregar_fila = ttk.Button(tab1, text="Agregar un nuevo proceso", command=add_row)
    boton_agregar_fila.pack(side=tk.TOP, pady=10)

    frame_tabla = ttk.Frame(tab1)
    frame_tabla.pack(expand=True, fill="x", pady=10)

    # Crear un canvas para agregar desplazamiento
    canvas = tk.Canvas(frame_tabla, height = 400)
    canvas.pack(side=tk.RIGHT, fill="x", expand=True)

    # Crear un scrollbar para el canvas
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.LEFT, fill="y")

    # Configurar el canvas para usar el scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

    # Crear un frame dentro del canvas para contener el Treeview
    frame_canvas = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_canvas, anchor="nw")

    # Configurar el Treeview
    tree = ttk.Treeview(frame_canvas)
    tree["columns"] = list(df.columns) + [""]
    tree["show"] = "headings"

    # Configurar encabezados y anchos
    for col in df.columns:
        tree.heading(col, text=col)
        ancho_ventana = ventana.winfo_height()
        tree.column(col, width= int(ancho_ventana / (5/2)), anchor="center")

    # Agregar filas
    for _, row in df.iterrows():
        tree.insert("", "end", values=[*row, "❌"])

    # Función para ajustar el área de desplazamiento del canvas
    def ajustar_scrollregion(event=None):
        canvas.config(scrollregion=canvas.bbox("all"))

    # Asociar la función de ajuste al evento de configuración del tree y el canvas
    frame_canvas.bind("<Configure>", ajustar_scrollregion)
    ventana.bind("<Configure>", ajustar_scrollregion)  # Ajusta el scroll al redimensionar la ventana

    # Limitar altura del Treeview al 20% de la ventana
    altura_ventana = ventana.winfo_height()
    tree_height = int(altura_ventana * 0.2)
    tree.config(height=tree_height)

    # Colocar el Treeview en el frame_canvas
    tree.pack(fill="x", expand=True)

    # Asociar evento de clic en el Treeview
    tree.bind("<ButtonRelease-1>", delete_row)
# Función para obtener el tamaño de la ventana y ajustar la imagen
def ajustar_imagen(event=None):
    if ventana.winfo_width()>10 and ventana.winfo_height()>10:
        ancho_ventana = ventana.winfo_width()

        # Calcular el 20% del ancho de la ventana
        nuevo_ancho = int(ancho_ventana * 0.2)
        
        # Mantener la relación de aspecto de la imagen
        proporcion = imagen_original.width / imagen_original.height
        nuevo_alto = int(nuevo_ancho / proporcion)
        
        # Redimensionar la imagen original
        imagen_redimensionada = imagen_original.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

        # Convertir la imagen redimensionada en un objeto PhotoImage compatible con Tkinter
        imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)

        # Actualizar la imagen en el label
        label_imagen.config(image=imagen_tk)
        label_imagen.image = imagen_tk  # Guardar una referencia para evitar que el garbage collector elimine la imagen
# Funciones para cambiar de pestaña
def cambiar_a_pestana_1():
    notebook.select(tab1)
def cambiar_a_pestana_2():
    notebook.select(tab2)
def cambiar_a_pestana_3():
    notebook.select(tab3)
def cambiar_a_pestana_4():
    notebook.select(tab4)
#Funciones para agregar las pestañas
def agregarboton_procesos():
    global pestanaProcesos  # Asegurarnos de usar la variable global
    if not (pestanaProcesos):
        boton2 = ttk.Button(control_frame, text="Procesos", command=cambiar_a_pestana_2)
        boton2.pack(side=tk.LEFT, expand=True, fill="x")
        pestanaProcesos = True
def agregarboton_memoria():
    boton3 = ttk.Button(control_frame, text="Memoria", command=cambiar_a_pestana_3)
    boton3.pack(side=tk.LEFT, expand=True, fill="x")
def agregarboton_stats():
    boton4 = ttk.Button(control_frame, text="Estadísticas", command=cambiar_a_pestana_4)
    boton4.pack(side=tk.LEFT, expand=True, fill="x")

#Empezar a tratar los procesos
def empezar_procesos():
    agregarboton_procesos()
    for item in tree.get_children():
        valores = tree.item(item, 'values')
        tr = valores[0]; ta = valores[1]; ti = valores[2]; tam_b = valores[3]
        proceso = Procesos(tr, ta, ti, tam_b)
        print(proceso)


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("MirandOS")
ventana.geometry("1280x720")
# Establecer tamaño de la ventana completa
ventana.state('zoomed')  # Hace que la ventana se abra maximizada
tamaño_ventana = [ventana.winfo_height(), ventana.winfo_width()]
# Crear el widget Notebook para las pestañas
notebook = ttk.Notebook(ventana)
# Crear los frames (contenedores) para cada pestaña
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
# Añadir las pestañas al Notebook
notebook.add(tab1)
notebook.add(tab2)
notebook.add(tab3)
notebook.add(tab4)
# Crear un frame para los botones de control de pestañas
control_frame = ttk.Frame(notebook)
control_frame.pack(side=tk.TOP, fill="x")
# Crear botones para cambiar entre las pestañas
boton1 = ttk.Button(control_frame, text="Inicio", command=cambiar_a_pestana_1)
boton1.pack(side=tk.LEFT, expand=True, fill="x")
# Empaquetar el Notebook para que llene toda la ventana
notebook.pack(expand=True, fill="both")
# Añadir imagen a la pestaña 1
imagen_original = Image.open("Frontend/logotipo.png")
# Crear un widget Label que contenga la imagen
label_imagen = tk.Label(tab1)
label_imagen.pack(pady=10, padx=20, anchor=tk.N, expand=False)
# Cargar la imagen para el botón
imagen_boton = Image.open("Frontend/boton_musica.png")  # Asegúrate de que la imagen esté en el directorio
imagen_boton = imagen_boton.resize((20, 20), Image.LANCZOS)  # Redimensionar la imagen si es necesario
imagen_boton_tk = ImageTk.PhotoImage(imagen_boton)
# Botón para activar/desactivar la música usando una imagen
boton_musica = ttk.Button(ventana, image=imagen_boton_tk, command=toggle_musica)
boton_musica.image = imagen_boton_tk  # Guardar referencia para evitar que la imagen sea recolectada
boton_musica.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)
# Etiqueta para mostrar el estado del archivo CSV cargado
etiqueta_csv = tk.Label(tab1, text="Ningún archivo CSV cargado", font=("Arial", 12))
etiqueta_csv.pack(side=tk.TOP, pady=10)
# Crear un Frame para los botones
frame_botones = tk.Frame(tab1)
frame_botones.pack(pady=10)
# Botón para cargar el archivo CSV
boton_cargar_csv = ttk.Button(frame_botones, text="Cargar CSV", command=cargar_csv)
boton_cargar_csv.pack(side=tk.RIGHT, pady=10)
boton_cargar_csv_vacio = ttk.Button(frame_botones, text="CSV desde 0", command=cargar_csv_vacio)
boton_cargar_csv_vacio.pack(side=tk.LEFT, pady=10)
boton_empezar_proceso = ttk.Button(tab1, text="Empezar proceso", command = empezar_procesos)
boton_empezar_proceso.pack(side=tk.BOTTOM, pady=10)
# Ajustar la imagen al iniciar la ventana
ventana.after(500, ajustar_imagen)  # Llama a la función ajustar_imagen después de 100 ms
# Asociar el evento de redimensionamiento de la ventana a la función de ajuste de altura
ventana.bind("<Configure>", ajustar_imagen)
# Reproducir música al iniciar la ventana
reproducir_musica()
# Ejecutar la ventana principal
ventana.mainloop()