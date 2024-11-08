import pandas as pd

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('procesos.csv')

# Mostrar las primeras 5 filas
print(df.head())


round_robin = 3
grado_multiprogramacion = 5
rendimiento_sistema = 0

particiones = [
    {"id_particion": "Sistema operativo", 
    "direccion_comienzo": 0, 
    "tamano_particion": 100000, 
    "id_proceso_asignado": None, 
    "fragmentacion_interna": None},
    {"id_particion": "Trabajos grandes", 
    "direccion_comienzo": 100001, 
    "tamano_particion": 250000, 
    "id_proceso_asignado": None, 
    "fragmentacion_interna": None},
    {"id_particion": "Trabajos medianos", 
    "direccion_comienzo": 350001, 
    "tamano_particion": 150000, 
    "id_proceso_asignado": None, 
    "fragmentacion_interna": None},
    {"id_particion": "Trabajos peque�os", 
    "direccion_comienzo": 500001, 
    "tamano_particion": 50000, 
    "id_proceso_asignado": None, 
    "fragmentacion_interna": None},
]

procesos_terminados = [] #id_proceso, tiempo_retorno, tiempo_espera
procesador = []
cola_listos = []

