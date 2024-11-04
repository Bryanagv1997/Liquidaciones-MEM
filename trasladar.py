import os
import shutil

def listar_archivos_png(directorio):
    # Lista para almacenar los archivos PNG
    archivos_png = []

    # Iterar sobre los archivos en el directorio
    for nombre in os.listdir(directorio):
        # Construir la ruta completa
        ruta_completa = os.path.join(directorio, nombre)
        
        # Verificar si es un archivo y si termina con .png
        if os.path.isfile(ruta_completa) and nombre.lower().endswith('.png'):
            archivos_png.append(ruta_completa)  # Agregar a la lista

    return archivos_png

def extraer_anio_mes(ruta_archivo):
    # Obtener el nombre del archivo
    nombre_archivo = os.path.basename(ruta_archivo)
    
    # Quitar la extensión del archivo
    nombre_sin_extension = nombre_archivo.split('.')[0]
    
    # Obtener las primeras dos partes separadas por '_'
    anio_mes = '_'.join(nombre_sin_extension.split('_')[:2])
    
    return anio_mes

# Especifica el directorio que deseas leer
directorio = os.getcwd() 
archivos_png = listar_archivos_png(directorio)

# Imprimir los archivos PNG encontrados
directorio_destino = directorio+'/liquidaciones' 
os.chdir(directorio_destino)


for archivo in archivos_png:
    directorio_creacion = extraer_anio_mes(archivo)
    print(directorio_creacion)
    try:
        os.mkdir(directorio_destino+"/"+directorio_creacion)
        print(f'Directorio "{directorio_destino+"/"+directorio_creacion}" creado exitosamente.')
        os.chdir(directorio_destino+"/"+directorio_creacion)
        shutil.copy(archivo,os.getcwd())
        print(f'Directorio "{directorio_destino+"/"+directorio_creacion}" creado exitosamente.')
    except FileExistsError:
        print(f'El directorio "{directorio_destino+"/"+directorio_creacion}" ya existe.')
        os.chdir(directorio_destino+"/"+directorio_creacion)
        print(f'Ahora estás en el directorio: {os.getcwd()}')
        shutil.copy(archivo,os.getcwd())
    except Exception as e:
        print(f'Error al crear el directorio: {e}')  