import pandas as pd

df = pd.read_csv('procesos.csv')


particiones = [
    {"id_particion": "Sistema operativo", 
    "direccion_comienzo": 0, 
    "tama�o_particion": 100000, 
    "id_proceso_asignado": None, 
    "fragmentacion_interna": None},
    {"id_particion": "Trabajos grandes", 
    "direccion_comienzo": 100001, 
    "tama�o_particion": 250000, 
    "id_proceso_asignado": None, 
    "fragmentacion_interna": None},
    {"id_particion": "Trabajos medianos", 
    "direccion_comienzo": 350001, 
    "tama�o_particion": 150000, 
    "id_proceso_asignado": None, 
    "fragmentacion_interna": None},
    {"id_particion": "Trabajos peque�os", 
    "direccion_comienzo": 500001, 
    "tama�o_particion": 50000, 
    "id_proceso_asignado": None, 
    "fragmentacion_interna": None},
]