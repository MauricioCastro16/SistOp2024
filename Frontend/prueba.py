import time
cpu = None

#Clases a utilizar
class Procesos:
    def __init__(self, tr, ta, ti, tam_b):
        self.tr = tr
        self.ta = ta
        self.ti = ti
        self.tam_b = tam_b
        self.estado = "nuevo"
        self.tiempoEjecutado = 0
        self.particion_asignada = None
    def __str__(self):
        return f"Proceso(TR={self.tr}, TA={self.ta}, TI={self.ti}, TAM(B)={self.tam_b}, TiempoEj={self.tiempoEjecutado})"
    def nombreProceso(self):
        return f"Proceso {self.tr}"
    def asignar_particion(self, particion):
        self.particion_asignada = particion
    def obtener_particion(self):
        return self.particion_asignada
    
class Particiones:
    def __init__(self, tamano):
        self.tamano = tamano
        self.fragmentacion = 0
        self.proceso_asignado = None
    def __str__(self):
        return f"Partición(TAM={self.tamano}, FRAG={self.fragmentacion}, Proceso={self.proceso_asignado})"
    def setFragmentacion(self, fragmentacion):
        self.fragmentacion = fragmentacion
    def setProceso(self, proceso):
        self.proceso_asignado = proceso

particionGrande = Particiones(250000)
particionMediana = Particiones(150000)
particionChiquita = Particiones(50000)
Memoria = [particionChiquita, particionGrande, particionMediana]

#Listas
procesos_cargados = []
procesos_nuevos = []
procesos_listos = []
procesos_terminados = []
procesos_listos_y_en_suspension = []

proceso1 = Procesos(1, 0, 5, 15000)
proceso2 = Procesos(2, 0, 4, 20000)
proceso3 = Procesos(3, 0, 10, 150000)
proceso4 = Procesos(4, 0, 3, 5000)
proceso5 = Procesos(5, 0, 2, 3000)
proceso6 = Procesos(6, 2, 10, 70000)
proceso7 = Procesos(7, 4, 5, 25000)
proceso8 = Procesos(8, 6, 5, 10000)
procesos_cargados.extend([proceso1, proceso2, proceso3, proceso4, proceso5, proceso6, proceso7, proceso8])

t = 0
multiprogramacion = 5
quantum = 3
while not all(proceso.estado == "terminado" for proceso in procesos_cargados):
    for proceso in procesos_cargados: #Planificador a largo plazo
        if (proceso.ta == t):
            procesos_nuevos.append(proceso)
    i = 0
    while (len(procesos_nuevos) > 0) and (i <= (len(procesos_nuevos) - 1)):
        procesonuevo = procesos_nuevos[i]
        for particion in sorted(Memoria, key=lambda particion: particion.tamano, reverse=True):
            if particion.proceso_asignado is None and particion.tamano >= procesonuevo.tam_b:
                particion.proceso_asignado = procesonuevo
                procesos_nuevos.remove(procesonuevo)
                procesos_listos.append(procesonuevo)
                procesonuevo.estado = "listo"
                procesonuevo.asignar_particion(particion)
                multiprogramacion -= 1
                break
        if procesonuevo.estado != "listo" and multiprogramacion != 0:
            procesos_nuevos.remove(procesonuevo)
            procesos_listos_y_en_suspension.append(procesonuevo)
            procesonuevo.estado = "listo y suspendido"
            multiprogramacion -= 1
        if procesonuevo.estado == "nuevo":
            i += 1
    if (cpu is None) and (len(procesos_listos) != 0):
        cpu = procesos_listos.pop(0)
        cpu.estado = "ejecutando"
    print("Procesos nuevos:", [str(p) for p in procesos_nuevos])
    print("Procesos listos:", [str(p) for p in procesos_listos])
    print("Procesos listos y suspendidos:", [str(p) for p in procesos_listos_y_en_suspension])
    print("CPU:", cpu)
    for particion in Memoria:
        print(particion)
    t += 1
    print("-"*60)
    if cpu is not None: #Planificador a corto plazo
        cpu.tiempoEjecutado += 1
        if cpu.tiempoEjecutado == cpu.ti:
            cpu.estado = "terminado"
            procesos_terminados.append(cpu)
            particionDeMemoria = cpu.obtener_particion()
            particionDeMemoria.setProceso(None)
            cpu = None
            multiprogramacion += 1
        if (t)%quantum == 0 and cpu is not None: #Round Robin
            cpu.estado = "listo"
            procesos_listos.append(cpu)
            cpu = None
        if cpu is None:
            if len(procesos_listos)>0:
                cpu = procesos_listos.pop(0)
                cpu.estado = "ejecutando"
            if (len(procesos_listos) < (len(Memoria) - 1)):
                if len(procesos_listos_y_en_suspension)>0: #Planificador a mediano plazo
                    for procesolistoysusp in procesos_listos_y_en_suspension:
                        for particionMediano in sorted(Memoria, key=lambda particionMediano: particionMediano.tamano, reverse=True):
                            if particionMediano.proceso_asignado is None and particionMediano.tamano >= procesolistoysusp.tam_b:
                                particionMediano.proceso_asignado = procesolistoysusp
                                procesolistoysusp.estado = "listo"
                                procesolistoysusp.asignar_particion(particionMediano)
                                procesos_listos_y_en_suspension.remove(procesolistoysusp)
                                procesos_listos.append(procesolistoysusp)
                                break
    time.sleep(0.1)
    print("Procesos nuevos:", [str(p) for p in procesos_nuevos])
    print("Procesos listos:", [str(p) for p in procesos_listos])
    print("Procesos listos y suspendidos:", [str(p) for p in procesos_listos_y_en_suspension])
    print("CPU:", cpu)