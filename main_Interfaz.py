from ftp import xm

# Conexion con usuario y carpeta del agente 

user1 = xm('###', '###', '###')
user1.set_periodo(2020,1)  # Establece el periodo antes de conectar
user1.archivo='###'
user1.version='###'
user1.conexion_comercia()