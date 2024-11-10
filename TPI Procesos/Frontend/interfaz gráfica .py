import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk
import pygame
import pandas as pd

# Inicializar pygame para manejar audio
pygame.mixer.init()

# Función para reproducir música
def reproducir_musica():
    pygame.mixer.music.load('Frontend/musica.mp3')  # Asegúrate de que la música esté en el mismo directorio
    pygame.mixer.music.play(-1)  # Reproduce en bucle infinito (-1)

# Variables globales
musica_activa = True
archivo_csv = None
tree = None
pestanaProcesos = False

def toggle_musica():
    global musica_activa
    if musica_activa:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    musica_activa = not musica_activa

# Función para cargar un archivo CSV en memoria
def cargar_csv():
    global archivo_csv, tree
    archivo_csv = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if archivo_csv:
        df = pd.read_csv(archivo_csv)  # Cargar el archivo CSV en un DataFrame de pandas
        etiqueta_csv.config(text=f"Archivo cargado: {archivo_csv.split('/')[-1]}")  # Mostrar el nombre del archivo en la etiqueta
        agregarboton_procesos()
        mostrar_csv(df)

# Función para mostrar el contenido del CSV en un Treeview con scrollbar
def mostrar_csv(df):
    global tree  # Asegurarnos de usar la variable global
    # Crear un frame para contener el Treeview y el scrollbar en tab1
    frame_tabla = ttk.Frame(tab1)
    frame_tabla.pack(expand=True, fill="x", pady=10)

    # Crear un canvas para agregar desplazamiento
    canvas = tk.Canvas(frame_tabla)
    canvas.pack(side=tk.RIGHT, fill="x", expand=True)

    # Crear un scrollbar para el canvas
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Configurar el canvas para usar el scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

    # Crear un frame dentro del canvas para contener el Treeview
    frame_canvas = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_canvas, anchor="nw")

    # Configurar el Treeview
    tree = ttk.Treeview(frame_canvas)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    # Configurar encabezados y anchos
    for col in df.columns:
        tree.heading(col, text=col)
        ancho_ventana = ventana.winfo_height()
        tree.column(col, width= int(ancho_ventana / 2), anchor="center")

    # Agregar filas
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

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


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("MirandOS")

# Establecer tamaño de la ventana completa
ventana.state('zoomed')  # Hace que la ventana se abra maximizada

tamaño_ventana = [ventana.winfo_height(), ventana.winfo_width()]
# Función para obtener el tamaño de la ventana y ajustar la imagen
def ajustar_imagen(event=None):
    ancho_ventana = ventana.winfo_width()

    # Calcular el 20% del ancho de la ventana
    nuevo_ancho = int(ancho_ventana * 0.4)
    
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

# Función para actualizar la altura y el ancho de las columnas del Treeview al redimensionar la ventana
def ajustar_dimensiones_treeview(event):
    global tree  # Asegurarnos de usar la variable global
    if tree is not None:  # Verificar que tree esté definido
        # Ajustar altura del Treeview
        altura_ventana = ventana.winfo_height()
        tree_height = int(altura_ventana * 0.2)
        tree.config(height=tree_height)
        
        # Ajustar ancho de las columnas del Treeview
        ancho_ventana = ventana.winfo_width()
        num_columnas = len(tree["columns"])
        ancho_columna = int(ancho_ventana / num_columnas)  # Dividir el ancho entre el número de columnas
        
        for col in tree["columns"]:
            tree.column(col, width=ancho_columna, anchor="center")  # Ajustar el ancho de cada columna


def ajustar(event):
    global tamaño_ventana  # Asegurarnos de usar la variable global
    if [ventana.winfo_height(), ventana.winfo_width()] != tamaño_ventana:
        ajustar_imagen(event)
        ajustar_dimensiones_treeview(event)

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

# Funciones para cambiar de pestaña
def cambiar_a_pestana_1():
    notebook.select(tab1)

def agregarboton_procesos():
    global pestanaProcesos  # Asegurarnos de usar la variable global
    if not (pestanaProcesos):
        boton2 = ttk.Button(control_frame, text="Procesos", command=cambiar_a_pestana_2)
        boton2.pack(side=tk.LEFT, expand=True, fill="x")
        pestanaProcesos = True

def cambiar_a_pestana_2():
    notebook.select(tab2)

def agregarboton_memoria():
    boton3 = ttk.Button(control_frame, text="Memoria", command=cambiar_a_pestana_3)
    boton3.pack(side=tk.LEFT, expand=True, fill="x")

def cambiar_a_pestana_3():
    notebook.select(tab3)

def agregarboton_stats():
    boton4 = ttk.Button(control_frame, text="Estadísticas", command=cambiar_a_pestana_4)
    boton4.pack(side=tk.LEFT, expand=True, fill="x")

def cambiar_a_pestana_4():
    notebook.select(tab4)

# Crear botones para cambiar entre las pestañas
boton1 = ttk.Button(control_frame, text="Inicio", command=cambiar_a_pestana_1)
boton1.pack(side=tk.LEFT, expand=True, fill="x")

# Empaquetar el Notebook para que llene toda la ventana
notebook.pack(expand=True, fill="both")

# Añadir imagen a la pestaña 1
imagen_original = Image.open("Frontend/logotipo.png")

# Asociar el evento de redimensionamiento de la ventana a la función de ajuste de altura
ventana.bind("<Configure>", ajustar)

# Crear un widget Label que contenga la imagen
label_imagen = tk.Label(tab1)
label_imagen.pack(pady=10, padx=20, anchor=tk.N, expand=False)

label2 = tk.Label(tab2, text="Contenido de la Pestaña 2", font=("Arial", 14))
label2.pack(pady=20, expand=True, fill="both")

label3 = tk.Label(tab3, text="Contenido de la Pestaña 3", font=("Arial", 14))
label3.pack(pady=20, expand=True, fill="both")

label4 = tk.Label(tab4, text="Contenido de la Pestaña 4", font=("Arial", 14))
label4.pack(pady=20, expand=True, fill="both")

# Cargar la imagen para el botón
imagen_boton = Image.open("Frontend/boton_musica.png")  # Asegúrate de que la imagen esté en el directorio
imagen_boton = imagen_boton.resize((50, 50), Image.LANCZOS)  # Redimensionar la imagen si es necesario
imagen_boton_tk = ImageTk.PhotoImage(imagen_boton)

# Botón para activar/desactivar la música usando una imagen
boton_musica = ttk.Button(ventana, image=imagen_boton_tk, command=toggle_musica)
boton_musica.image = imagen_boton_tk  # Guardar referencia para evitar que la imagen sea recolectada
boton_musica.pack(side=tk.BOTTOM, anchor=tk.SE, padx=20, pady=20)

# Etiqueta para mostrar el estado del archivo CSV cargado
etiqueta_csv = tk.Label(tab1, text="Ningún archivo CSV cargado", font=("Arial", 12))
etiqueta_csv.pack(side=tk.TOP, pady=10)

# Botón para cargar el archivo CSV
boton_cargar_csv = ttk.Button(tab1, text="Cargar CSV", command=cargar_csv)
boton_cargar_csv.pack(side=tk.TOP, pady=10)

# Ajustar la imagen al iniciar la ventana
ventana.after(100, ajustar_imagen)  # Llama a la función ajustar_imagen después de 100 ms

# Reproducir música al iniciar la ventana
reproducir_musica()

# Ejecutar la ventana principal
ventana.mainloop()