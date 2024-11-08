#!/bin/bash
echo "Script de Python en ejecución..."

cd /home/penguinblack97/Liquidaciones || exit
echo "Directorio cambiado a /home/penguinblack97/Liquidaciones"

. ./venv/bin/activate || exit
echo "Entorno virtual activado"

python3 main.py || exit
echo "main.py ejecutado con éxito"

python3 trasladar.py || exit
echo "trasladar.py ejecutado con éxito"

deactivate
echo "Entorno virtual desactivado"

rm *.png
echo "Archivos PNG eliminados"
# Para verificar errores utilizar en ´crontab -e´ 0 8 * * * /home/penguinblack/Liquidaciones/run_python_.sh >> /home/penguinblack/salida.log 2>&1 
