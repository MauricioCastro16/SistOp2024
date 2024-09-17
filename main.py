

class cpu:
	def __init__()

class proceso:
	def __init__(Tr,Ta,Ti,Tam)
		self.tr = Tr
		self.ta = Ta
		self.ti = Ti
		self.tam = Tam

class memoria:
	def __init__()
		self.listaParticiones = []
		par1 = particion("Sistema Operativo",0,99999)
		listaParticiones.append(par1)
		par2 = particion("Trabajos Grandes",100000,249999)
		listaParticiones.append(par2)
		par3 = particion("Trabajos Mediano",350000,149999)
		listaParticiones.append(par3)
		par4 = particion("Trabajos Pequeños",500000,49999)
		listaParticiones.append(par4)

#(Id de partición, dirección de comienzo de partición, tamaño de la partición, id de proceso asignado a la partición, fragmentación interna
class particion:
	def __init__(idM,dirInit,tam):
		self.idM = idM
		self.dirInit = dirInit
		self.tam = tam
		self.proceso = None
		self.fragmInt = None
	
	def asignarProceso(proceso):
		self.proceso = proceso
		self.fragmInt = self.tam - proceso.tam

	def liberarProceso():
		self.proceso = None

	def estaLibre():
		return (self.proceso == None)

if __name__ = __main__:
	
	