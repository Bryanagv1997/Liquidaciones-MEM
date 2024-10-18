## Liquidación de despacho de contratos en el MEM

- Deberas descargar primero todos los archivos del respectivo mes que quieras despachar de tu generador o comercializador:
  * Ingresando tu ID_xm,Password_xm,Agent_Id.
  * Luego el año y mes de liquidación.
  * El archivo con el que vas a realizar la liquidación.
  * Versión de tu archivo.
  
```python
user1 = xm('Id_xm', 'Password_xm', 'Agente_Id')
user1.set_periodo(año, mes) 
user1.archivo='Archivo'
user1.version='versión'
user1.conexion_comercia()
user1.desconexion()
```