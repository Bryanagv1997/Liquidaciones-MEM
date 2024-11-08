from ftplib import FTP_TLS
import fnmatch
import os
import pandas as pd
import matplotlib.pyplot as plt

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
        self.año= año
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
        contador = 0
        for archivo in self.Files:
            self.ftp.retrbinary(f'RETR {archivo}',open(archivo,'wb').write)
            print(f'Archivo "{archivo}" descargado exitosamente.')
            contador +=1
        print(f'Se ha completado exitosamente la descarga.')
        self.to_excel()
        return contador
    
    def to_excel(self):
        data_base = pd.DataFrame()
        for file_name in self.Files:

            fecha_str =  file_name[len(self.archivo):-len('.'+self.version)]
            fecha = pd.to_datetime(str(self.año)+fecha_str,format='%Y%m%d')

            df = pd.read_table(file_name,sep=';',encoding='latin-1')
            df['fecha'] = fecha

            data_base = pd.concat((data_base,df))
        [os.remove(archivo) for archivo in self.Files] 
        data_base.to_excel(self.archivo+'_'+self.version+'.xlsx',index=False)
        os.chdir("..")

    def conexion_comercia(self):
        self.ftp.cwd(f'/INFORMACION_XM/USUARIOSK/{self.agente}/SIC/COMERCIA/{self.periodo}')
        print(f'Estoy en la ruta {self.ftp.pwd()}')
        self.busqueda()
        print(f'\n Iniciando la descarga de archivos.')
        dias=self.descarga()
        return dias


    def conexion_finance(self):
        self.ftp.cwd(f'/INFORMACION_XM/USUARIOSK/{self.agente}/FINANCE/SIC/{self.periodo}')
        print(f'Estoy en la ruta {self.ftp.pwd()}') 
        self.busqueda()
        print(f'\n Iniciando la descarga de archivos.')
        self.descarga()

    def conexion_publico(self):
        self.ftp.cwd(f'/INFORMACION_XM/PUBLICOK/SIC/COMERCIA/{self.periodo}')
        print(f'Estoy en la ruta {self.ftp.pwd()}') 
        self.busqueda()
        print(f'\n Iniciando la descarga de archivos.')
        self.descarga()                  

    def desconexion(self):
        self.ftp.quit()

class liq:

    def __init__(self,dspcctos,cliq):
        lista = [dspcctos,cliq]
        self.dataframes =[]
        for i in lista:
            os.chdir(i)
            archivos = os.listdir()
            for archivo in archivos:
                        self.dataframes.append(pd.read_excel(archivo))
            os.chdir('..')
        print('Lectura de los archivo dataframe finalizado')

    def liquidacion(self):
        df_dsp = self.dataframes[0].round(2)
        df = df_dsp.drop(['TIPO','TIPOMERC','TIPO ASIGNA'],axis=1)
        # Se crea lista de columnas pra seleccionar
        _desp = ['DESP_HORA {:02}'.format(i) for i in range(1,25)]
        _hora = ['TRF_HORA {:02}'.format(i) for i in range(1,25)]

        # Contratos de compra y venta
        Compras_Contratos = df[df['COMPRADOR'].isin(['SFEC'])]
        Ventas_Contratos = df[df['VENDEDOR'].isin(['SFEC'])]

        # Filtro para filtrar por el agente comercializador
        df_cliq = self.dataframes[1]
        cliq= df_cliq[df_cliq['AGENTE'].isin(['SFEC'])]
        # Bolsa
        ventas_bolsa_kWh = cliq['VENTAS BOLSA kwh'].sum()
        ventas_bolsa_COP = cliq['VENTAS BOLSA $'].sum()
        compras_bolsa_kWh = cliq['COMPRAS BOLSA kwh'].sum()
        compras_bolsa_COP = -cliq['COMPRAS BOLSA $'].sum()
        Compras_Contratos_kWh = Compras_Contratos.groupby(['CONTRATO','COMPRADOR','VENDEDOR'])[_desp].sum().sum(axis=1).reset_index(name='Total [kWh/mes]')
        Ventas_Contratos_kWh = Ventas_Contratos.groupby(['CONTRATO','COMPRADOR','VENDEDOR'])[_desp].sum().sum(axis=1).reset_index(name='Total [kWh/mes]')
        # Se calcula el despacho de los contratos
        Compras_Contratos_COP = Compras_Contratos.groupby(['CONTRATO','COMPRADOR','VENDEDOR']).apply(lambda x:(-x[_desp].values*x[_hora].values).sum()).reset_index(name='Total [COP]')
        Ventas_Contratos_COP = Ventas_Contratos.groupby(['CONTRATO','COMPRADOR','VENDEDOR']).apply(lambda x:(x[_desp].values*x[_hora].values).sum()).reset_index(name='Total [COP]')
        # Paso anterior no es necesario para el calculo pero si se quiere mostar tablas diferentes (compras y ventas) es un buen ejercicio
        Compras = pd.merge(Compras_Contratos_kWh,Compras_Contratos_COP,on=['CONTRATO','COMPRADOR','VENDEDOR'],how='inner')
        Ventas = pd.merge(Ventas_Contratos_kWh,Ventas_Contratos_COP,on=['CONTRATO','COMPRADOR','VENDEDOR'],how='inner')

        Compras_COP=Compras['Total [COP]'].sum()
        ventas_COP=Ventas['Total [COP]'].sum()

        Compras_kwh=Compras['Total [kWh/mes]'].sum()
        ventas_kwh=Ventas['Total [kWh/mes]'].sum()

        # Se realiza un consolidado completo de todos los contratos del comercializador
        totales = pd.DataFrame([['VENTAS BOLSA','','SFEC',ventas_bolsa_kWh,ventas_bolsa_COP],['VENTAS TOTALES','-','SFEC',ventas_kwh + ventas_bolsa_kWh,ventas_COP+ventas_bolsa_COP]],columns=Ventas.columns)
        resultado_contratos = pd.concat([Ventas,totales])
        totales = pd.DataFrame([['COMPRAS BOLSA','SFEC','-',compras_bolsa_kWh,compras_bolsa_COP],['COMPRAS TOTALES','SFEC','-',Compras_kwh + compras_bolsa_kWh,Compras_COP+compras_bolsa_COP]],columns=Ventas.columns)
        resultado_contratos = pd.concat([resultado_contratos,Compras])
        resultado_contratos = pd.concat([resultado_contratos,totales])
        totales = pd.DataFrame([['MARGEN TOTAL','-','-',Compras_kwh+compras_bolsa_kWh,ventas_COP+ventas_bolsa_COP+Compras_COP+compras_bolsa_COP]],columns=Ventas.columns)
        resultado_contratos = pd.concat([resultado_contratos,totales])
        resultado_contratos['Total [kWh/mes]'] = resultado_contratos['Total [kWh/mes]'].apply(lambda x: f'{x:,.2f}')
        resultado_contratos['Total [COP]'] = resultado_contratos['Total [COP]'].apply(lambda x: f'${x:,.2f}')
        print('Tabla de resultados realizada')
        return Ventas,resultado_contratos
    
    def imagen_liquidacion(self,año,mes,dias,Ventas,dataframe_):
        fig, ax = plt.subplots(figsize=(10, 2))
        ax.axis('tight')
        ax.axis('off')
        
        # Crear la tabla
        tabla = ax.table(cellText=dataframe_.values, colLabels=dataframe_.columns, cellLoc='center', loc='center')
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(9)

        # Establecer el formato de los títulos
        for (i, j), cell in tabla.get_celld().items():
            if i == 0 or i == len(dataframe_) or i==len(Ventas)+2 or i == len(dataframe_)-1:  # Títulos
                cell.set_text_props(fontweight='bold', color='black')
            else:
                cell.set_text_props(fontweight='normal', color='black')

        # Guardar la tabla como imagen
        plt.savefig(f'{str(año)}_{str(mes)}_{str(dias)}.png', bbox_inches='tight', dpi=500)
        plt.close()
        print(f"Se crea imagen {str(año)}_{str(mes)}_{str(dias)}_para compartir")
