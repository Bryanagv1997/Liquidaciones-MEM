from ftp import xm

# Conexion con usuario y carpeta del agente 

user1 = xm('1017243061', 'Bwcn"1IL"Z{cSd|1', 'SFEC')
user1.set_periodo(2024,10)  # Establece el periodo antes de conectar
user1.archivo='dspcttos' # Archivo necesario para el despacho de contratos del comercializador
user1.version='tx2' # Version del archivo durante el mes
user1.conexion_comercia()
user1.archivo='cliq' # Archivo donde se encuentra el PEP.
user1.conexion_publico() #Conexion con el sitio publico del ASIC
user1.desconexion()