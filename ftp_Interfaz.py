from ftplib import FTP_TLS
import fnmatch
import os

class xm:
    def __init__(self, usuario, pwss, agente):
        self.ftp = FTP_TLS(timeout=10)
        self.usuario = usuario
        self.agente = agente
        self.ftp.connect(host='xmftps.xm.com.co', port=210)
        self.ftp.auth()
        self.ftp.prot_p()
        self.ftp.login(user=f'ISAMDNT\\{self.usuario}', passwd=pwss)
        print(f'Se inicializa en la ruta {self.ftp.pwd()}')

    @property
    def archivo(self):
        return self._archivo  # Usar un atributo privado para almacenar el valor

    @archivo.setter
    def archivo(self, archivo_info):
        self._archivo = archivo_info

    @property
    def version(self):
        return self._version  # Usar un atributo privado para almacenar el valor

    @version.setter
    def version(self, version_info):
        self._version = version_info

    def set_periodo(self, año, mes):
        self.periodo = f'{año}-{mes}'
    
    def directorio(self):
        directorio = self.archivo
        try:
            os.mkdir(directorio)
            print(f'Directorio "{directorio}" creado exitosamente.')
            os.chdir(self.archivo)
        except FileExistsError:
            print(f'El directorio "{directorio}" ya existe.')
            os.chdir(self.archivo)
            print(f'Ahora estás en el directorio: {os.getcwd()}')
            archivos = os.listdir()
            for archivo in archivos:
                os.remove(archivo)  # Borrar el archivo
                print(f'Archivo "{archivo}" borrado exitosamente.')
        except Exception as e:
            print(f'Error al crear el directorio: {e}')        
    
    def busqueda(self):
        lista=self.ftp.nlst()
        self.Files=fnmatch.filter(lista,self.archivo+'*'+self.version)
        if len(self.Files)>0:
            print(f'El archivo {self.archivo} existe en su version {self.version}')
            print(f'\nIniciando traslado de carpeta paa descarga....')
            self.directorio()
            print(f'\nEl directorio {self.archivo} ya esta limpio ....')
        else:
            print(f'El archivo {self.archivo} no existe en su version {self.version} o este archivo no existe en esta carpeta')

    def descarga(self):
        for archivo in self.Files:
            self.ftp.retrbinary(f'RETR {archivo}',open(archivo,'wb').write)
            print(f'Archivo "{archivo}" descargado exitosamente.')
        print(f'Se ha completado exitosamente la descarga.')

    def conexion_comercia(self):
        self.ftp.cwd(f'/INFORMACION_XM/USUARIOSK/{self.agente}/SIC/COMERCIA/{self.periodo}')
        print(f'Estoy en la ruta {self.ftp.pwd()}')
        self.busqueda()
        print(f'\n Iniciadno la descarga de archivos.')
        self.descarga()


    def conexion_finance(self):
        self.ftp.cwd(f'/INFORMACION_XM/USUARIOSK/{self.agente}/FINANCE/SIC/{self.periodo}')
        print(f'Estoy en la ruta {self.ftp.pwd()}') 
        self.busqueda()
        print(f'\n Iniciadno la descarga de archivos.')
        self.descarga()          

    def desconexion(self):
        self.ftp.quit()
