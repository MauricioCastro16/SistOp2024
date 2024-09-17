import pandas as pd

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('procesos.csv')

# Mostrar las primeras 5 filas
print(df.head())

#ASDF


round_robin = 3
grado_multiprogramacion = 5
rendimiento_sistema = 0

particiones = [
    {"id_particion": "Sistema operativo", 
    "direccion_comienzo": 0, 
    "tamaño_particion": 100000, 
    "id_proceso_asignado": None, 
    "fragmentacion_interna": None},
    {"id_particion": "Trabajos grandes", 
    "direccion_comienzo": 100001, 
    "tamaño_particion": 250000, 
    "id_proceso_asignado": None, 
    "fragmentacion_interna": None},
    {"id_particion": "Trabajos medianos", 
    "direccion_comienzo": 350001, 
    "tamaño_particion": 150000, 
    "id_proceso_asignado": None, 
    "fragmentacion_interna": None},
    {"id_particion": "Trabajos pequeños", 
    "direccion_comienzo": 500001, 
    "tamaño_particion": 50000, 
    "id_proceso_asignado": None, 
    "fragmentacion_interna": None},
]

procesos_terminados = [] #id_proceso, tiempo_retorno, tiempo_espera
procesador = []
cola_listos = []

