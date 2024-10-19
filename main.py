from ftp import xm

# Conexion con usuario y carpeta del agente 

user1 = xm('1017243061', 'Bwcn"1IL"Z{cSd|1', 'SFEC')
user1.set_periodo(2024,10)  # Establece el periodo antes de conectar
user1.archivo='dspcttos'
user1.version='tx2'
user1.conexion_comercia()
user1.to_excel()
user1.desconexion()