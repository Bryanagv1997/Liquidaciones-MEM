from ftp import xm
from ftp import liq
from datetime import datetime

# Obtener la fecha actual
hoy = datetime.now()

# Obtener el mes y el día
mes_actual = hoy.month
dia_hoy = hoy.day
año_actual = hoy.year

mes_actual = mes_actual if dia_hoy>5 else mes_actual-1
b,a = (año_actual,mes_actual) if mes_actual>1 else (año_actual-1,12)
# Conexion con usuario y carpeta del agente 
user1 = xm('ID_XM', 'psswd_XM', 'SFEC')
user1.set_periodo(b,a)  # Establece el periodo antes de conectar
user1.archivo='dspcttos' # Archivo necesario para el despacho de contratos del comercializador
user1.version='tx2' # Version del archivo durante el mes
user1.conexion_comercia()
user1.archivo='cliq' # Archivo donde se encuentra el PEP.
user1.conexion_publico() #Conexion con el sitio publico del ASIC
user1.desconexion()

liquidacion = liq('dspcttos','cliq')
compras,resultado = liquidacion.liquidacion()
liquidacion.imagen_liquidacion(compras,resultado,'Tabla_liquidacion.png')