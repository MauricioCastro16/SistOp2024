

class cpu:
	def __init__(self):
		print("hello")

class proceso:
	def __init__(self, idproc, tiempArrivo, tiempIrrupt, tamMem):
		self.idproc = idproc
		self.tiempArrivo = tiempArrivo
		self.tiempIrrupt = tiempIrrupt
		self.tamMem = tamMem

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
	print("Hello world")
	
	