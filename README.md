## Liquidación de despacho de contratos en el MEM

- Deberas descargar primero todos los archivos del respectivo mes que quieras despachar de tu generador o comercializador:
  * Ingresando tu ID_xm,Password_xm,Agent_Id.
  * Luego el año y mes de liquidación.
  * El archivo con el que vas a realizar la liquidación.
  * Versión de tu archivo.
  
```python
user1 = xm('ID_XM', 'psswd_XM', 'Codigo_SIC')
user1.set_periodo(2024,10)  # Establece el periodo antes de conectar
user1.archivo='dspcttos' # Archivo necesario para el despacho de contratos del comercializador
user1.version='tx2' # Version del archivo durante el mes
user1.conexion_comercia()
user1.archivo='cliq' # Archivo donde se encuentra el PEP.
user1.conexion_publico() #Conexion con el sitio publico del ASIC
user1.desconexion()

liquidacion = liq('dspcttos','cliq')
compras,resultado = liquidacion.liquidacion()
liquidacion.imagen_liquidacion(compras,resultado,'Tabla_liquidacion.png')
```