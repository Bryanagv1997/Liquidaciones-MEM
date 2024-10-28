# !/bin/bash
# programa para correr main.py en el bash como ejecutable
# Se debe agregar el automatismo
# crontab -e
# 0 8 * * * RUTAABSOLUTA/run_python_.sh

# Borrar la imagen guardada
find Ruta_absoluta_Desde_Home -type f -name "*.png" -exec rm {} \;

# Cambiar al directorio correcto
cd Ruta_absoluta_Desde_Home || exit

# Activar el entorno virtual
# Entorno ruta para activarla
. ./venv/bin/activate || exit

# Ejecutar el script de Python
python3 main.py || exit
python3 trasladar.py || exit
# Desactivar el entorno virtual (opcional)
deactivate

