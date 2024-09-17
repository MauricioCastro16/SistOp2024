

class cpu:
	def __init__(self):
		self.memoria = memoria()
		self.procesoActivo = None
		self.quantum = 3
		self.colaListos = []
		self.tiempo = 0
	
	def ingresarProceso(self, proceso):
		if self.procesoActivo is None:
			self.procesoActivo = proceso
	
	def Procesar(self):
		self.tiempo += 1
		self.procesoActivo.tiempoEjecutado += 1
		self.quantum -= 1
		if self.procesoActivo.tiempoEjecutado == self.procesoActivo.tiempIrrupt:
			self.terminarProceso()
			return None
		if self.quantum == 0:
			self.quantum = 3
			auxproceso = self.procesoActivo
			self.terminarProceso()
			return auxproceso
	
	def terminarProceso(self):
		self.procesoActivo = None


class proceso:
	def __init__(self, idproc, tiempArrivo, tiempIrrupt, tamMem):
		self.idproc = idproc
		self.tiempArrivo = tiempArrivo
		self.tiempIrrupt = tiempIrrupt
		self.tamMem = tamMem
		self.tiempEjecutado = 0

class memoria:
	def __init__(self):
		self.listaParticiones = []
		par1 = particion("Sistema Operativo",0,99999)
		self.listaParticiones.append(par1)
		par2 = particion("Trabajos Grandes",100000,249999)
		self.listaParticiones.append(par2)
		par3 = particion("Trabajos Mediano",350000,149999)
		self.listaParticiones.append(par3)
		par4 = particion("Trabajos Pequenos",500000,49999)
		self.listaParticiones.append(par4)

#(Id de particion, direccion de comienzo de particion, tamano de la particion, id de proceso asignado a la particion, fragmentacion interna
class particion:
	def __init__(self,idM,dirInit,tam):
		self.idM = idM
		self.dirInit = dirInit
		self.tam = tam
		self.proceso = None
		self.fragmInt = None
	
	def asignarProceso(self, proceso):
		self.proceso = proceso
		self.fragmInt = self.tam - proceso.tam

	def liberarProceso(self):
		self.proceso = None

	def estaLibre(self):
		return (self.proceso == None)

if __name__ == "__main__":
	listaProcesos = []
	colaListos = []
	while True:
		cpu.ingresarProceso(colaListos[0])
		procesoEncolado = cpu.Procesar()
		colaListos.append(cpu.Procesar()) #CUIDADO NONE SI APPENDEA
	
	