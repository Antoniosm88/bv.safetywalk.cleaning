import pandas as pd
import numpy as np

#Carga el excel en un Dataframe (datos de las SW)
df= pd.read_excel('/home/antonio/Documentos/BV/SW_informe_dataCleaning/Data/BV Safety_All Safety Walks.xlsx', engine='openpyxl')
#Borra las primeras 4 filas del Df
df1=df.drop([0,1,2,3])
new_header = df1.iloc[0] #grab the first row for the header
df2 = df1[1:] #take the data less the header row
df2.columns = new_header #set the header row as the df header
df3=df2.reset_index()
#Cambiamos el nómbre de las columnas
df4 = df3.rename(columns = {'Number':'Número',
                            'Created Date':'Fecha de creación',
                            'Name of the Observer':'Nombre del observador',
                            'Name of the Observed Person(s)':'Nombre de la persona o personas observadas',
                            'Operating Group':'Grupo Operativo',
                            'Country':'País',
                            'Entity':'Entidad',
                            'Site':'Sitio',
                            'BV Site Name':'Nombre del sitio de BV',
                            'Client Name':'Nombre del cliente',
                            'Site Address':'Dirección del sitio',
                            '1. Mind On Task?': '1. ¿Mente en la tarea?', 
                            '2. Eyes on Task?': '2. ¿Ojos puestos en la tarea?',
                            '3. Using equpment properly?': "3. ¿Utiliza el equipo correctamente?",
                            '4. Performing task while not rushing?': "4. ¿Realiza la tarea sin apresurarse?",
                            '5. Wearing prescribed PPE?': '5. ¿Usa el EPI definido?',
                            '6. Following Safe Working Procedures?':'6. ¿Sigue procedimientos de trabajo seguros?',
                            '7. Authorization is obtained...':'7. Se obtiene la autorización ...',
                            '8. Check surrounding work areas...':'8. Verifica el entorno de trabajo, 2 min para mi seguridad',
                            '9. Personnel acted safely for the task observed':'9. El personal actuó con seguridad para la tarea observada.',
                            '10. Aware of the Emergency Evacuation...':'10.Conoce la Ruta de Evaluación de Emergencias y el Punto de Reunión',
                            '11. The person is aware of the need to report near hit and unsafe situation.':'11. La persona es consciente de la necesidad de reportar Cuasi Accidentes y Condiciones Inseguras?.',
                            '12. Personnel stops Working if the situation is unsafe.':'12. El personal deja de trabajar si la situación no es segura.',
                            '13. Personnel is competent and trained...':'13. El personal esta capacitado y suficientemente formado para la Tarea.',
                            '14. Adequate and worn correctly the applicable PPE':'14. Los EPIS definidos son adecuados y se usan correctamente.',
                            '15. Good conditions, well maintained and properly stored.':'15. los EPIS estan en buen estado, bien mantenidos y se almacenan correctamente.',
                            '16. Good housekeeping of the work area...':'16. Buena limpieza del área de trabajo',
                            '17. Area Free of Slip Trip and Fall Hazards':'17. Área libre de riesgos de resbalones, tropiezos y caídas',
                            '18. Walkways, aisles, emergency exits...':'18. Pasillos, salidas de emergencia y equipos de emergencia no estan obstruidos.',
                            '19. Spillage controlled':'19. Derrames controlados',
                            '20. All containers in use and in the area are labelled.':'20. Todos los contenedores en uso y en el área están etiquetados.',
                            '21. No Noise, Dust, Odor Issues':'21. Sin ruidos, polvo ni olores',
                            '22. Hazardous substances are stored properly':'22. Las sustancias peligrosas se almacenan adecuadamente',
                            '23. The work area is secured from hazards...':'23. El área de trabajo está protegida contra riesgos',
                            '24. Sufficient lighting and ventilation.':'24. Iluminación y ventilación suficientes.',
                            '25. Use intrinsically safe equipment...':'25. Uso de equipos intrínsecamente seguro.',
                            '26. Machine guarding or Lock-Out-Tag-Out...':'26. Protección de la maquina o señal de bloqueo-etiquetado disponible',
                            '27. Scaffold or ladder is safe for use.':'27. El andamio o la escalera son seguros para su uso.',
                            'Did I use my Stop Work Authority?':'¿Usé mi autorización para detener el trabajo?',
                            'Comments / Action Plan':'Comentarios / Plan de acción'},
                            
                                             inplace = False)
#Cargamos el excel donde están los empreados que realizan las SW
Lista_sw2= pd.read_excel('/home/antonio/Documentos/BV/SW_informe_dataCleaning/Data/LISTA SW.xlsx',engine='openpyxl',sheet_name='Hoja1')
col_one_list=list(Lista_sw2['Nombres de los que hacen SW'])
#Homogeneizamos la columna donde estan los nombres de los empleados que han subido las SW a QESIS
nombres=[]
for e in df4['Nombre del observador']:
    word_list = e.split()
    if word_list[-1].isupper()==True:
        nombres.append(word_list)
    if word_list[-1].isupper()==False:
        word_list.remove(word_list[-1])
        nombres.append(word_list)
#Esta función convierte las listas en strings
def listToString(s):  
    
    # initialize an empty string 
    str1 = " " 
    
    # return string   
    return (str1.join(s))
#La lista donde se ha homogeneizado los nombres se transforma en strings
nombres2=[]
for e in nombres:
    nombres2.append(listToString(e))  
#Agregamos la lista con los nombres limpios a la columna del Df y las pasamos a mayúsculas.

df4['Nombre del observador']=nombres2
df4['Nombre del observador']= df4['Nombre del observador'].str.upper()
nombres_PORTUGAL = df4[(df4['País'] == ' Portugal ')]
#creamos un nuevo Df con un filtro para elegir Portugal
nombres_PORTUGAL = df4[(df4['País'] == ' Portugal ')]
#Bucle for para introducir en una lista los nombres de los portugueses que tienen 2 apellidos.
#Si tienen + de 3 elementos debe de coger el 2º elemento y borrarlo.
nombre_portugal=[]
for e in nombres_PORTUGAL['Nombre del observador']:
    word_list = e.split()
    if len(word_list) >= 3:
        word_list.remove(word_list[-2])
        nombre_portugal.append(word_list)
    else:
        nombre_portugal.append(word_list)
#aplicamos la función para pasar de list a string.
nombres3=[]
for e in nombre_portugal:
    nombres3.append(listToString(e))
nombres_ESPAÑAs = df4[(df4['País'] == ' Spain ')]
nombres4=[]
for e in nombres_ESPAÑAs:
    nombres4.append(listToString(e))

#Añadimos los nombres modificados a la columna del Df que creamos con el filtro.
nombres_PORTUGAL['Nombre del observador']=nombres3

#Concatenamos el df principal con el que creamos con el filtro.
df4 = pd.concat([df4, nombres_PORTUGAL],ignore_index=True)

nombre_5=[]
for e in df4['Nombre del observador']:
    word_list = e.split()
    nombre_5.append(word_list)
for e in nombre_5:
    if len(e)==2:
        e.extend(["."])
nombres6=[]
for e in nombre_5:
    nombres6.append(listToString(e)) 

df4['Nombre del observador']=nombres6

df4.reset_index(drop=True, inplace=True)

clean_country = df4[(df4['País'] != ' Spain ')& (df4['País'] != ' Portugal ')].index
# Delete these row indexes from dataFrame
df4.drop(clean_country , inplace=True)

#Cambiarmos el nombre de la columna por Nombre completo OBSERVADOR.
df4 = df4.rename(columns={'Nombre del observador':'Nombre completo OBSERVADOR'})

#Creamos una lista con las preguntas de las SW
list_preguntas=['1. ¿Mente en la tarea?',
       '2. ¿Ojos puestos en la tarea?', '3. ¿Utiliza el equipo correctamente?',
       '4. ¿Realiza la tarea sin apresurarse?', '5. ¿Usa el EPI definido?',
       '6. ¿Sigue procedimientos de trabajo seguros?',
       '7. Se obtiene la autorización ...',
       '8. Verifica el entorno de trabajo, 2 min para mi seguridad',
       '9. El personal actuó con seguridad para la tarea observada.',
       '10.Conoce la Ruta de Evaluación de Emergencias y el Punto de Reunión',
       '11. La persona es consciente de la necesidad de reportar Cuasi Accidentes y Condiciones Inseguras?.',
       '12. El personal deja de trabajar si la situación no es segura.',
       '13. El personal esta capacitado y suficientemente formado para la Tarea.',
       '14. Los EPIS definidos son adecuados y se usan correctamente.',
       '15. los EPIS estan en buen estado, bien mantenidos y se almacenan correctamente.',
       '16. Buena limpieza del área de trabajo',
       '17. Área libre de riesgos de resbalones, tropiezos y caídas',
       '18. Pasillos, salidas de emergencia y equipos de emergencia no estan obstruidos.',
       '19. Derrames controlados',
       '20. Todos los contenedores en uso y en el área están etiquetados.',
       '21. Sin ruidos, polvo ni olores',
       '22. Las sustancias peligrosas se almacenan adecuadamente',
       '23. El área de trabajo está protegida contra riesgos',
       '24. Iluminación y ventilación suficientes.',
       '25. Uso de equipos intrínsecamente seguro.',
       '26. Protección de la maquina o señal de bloqueo-etiquetado disponible',
       '27. El andamio o la escalera son seguros para su uso.']
#Realizamos a  todas las columnas y sustituimos los elementos vacios por N/A.
df4[list_preguntas] = df4[list_preguntas].fillna('N/A')
#Carga el excel de los datos de los empleados del archívo HC (datos de las SW)
df_empleados= pd.read_excel('/home/antonio/Documentos/BV/SW_informe_dataCleaning/Data/Resumen HC Enero 2021.xlsx',engine='openpyxl',sheet_name='HC ENERO')

#Sustituimos el los nombres sin segundo apellido por un  ".".
df_empleados['SEGUNDO APELLIDO'] = df_empleados['SEGUNDO APELLIDO'].fillna('.')

#Creamos un nuevo df con el filtro de NO ESPAÑA(Portugal) y Segundo apellido "."
clean_country_PORTUGAL = df_empleados[(df_empleados['PAIS'] != 'ESPAÑA')& (df_empleados['SEGUNDO APELLIDO'] != '.')]

#Sustituimos la columna de primer apellido por la de segundo apellido
clean_country_PORTUGAL['PRIMER APELLIDO']=clean_country_PORTUGAL['SEGUNDO APELLIDO']

# Modificamos toda la columna de segundo apellido por "."
clean_country_PORTUGAL['SEGUNDO APELLIDO']='.'

#concatenamos el df de empleados con el que hemos creado y modificado
df_empleados = pd.concat([df_empleados, clean_country_PORTUGAL],ignore_index=True)

#creamos una columna uniendo Nombre+primerapellido+segundoapellido
df_empleados['Nombre completo OBSERVADOR'] = df_empleados['NOMBRE'] + " " + df_empleados['PRIMER APELLIDO']+ " " +df_empleados['SEGUNDO APELLIDO']

#Pasamos a mayúsculas la nueva columna creada.
df_empleados['Nombre completo OBSERVADOR']=df_empleados['Nombre completo OBSERVADOR'].str.upper()

#creamos un nuevo df con los nombres que aparecen en la lista de los empleados que tienen que hacer las sw en 2021.
df_empleados=df_empleados[df_empleados['Nombre completo OBSERVADOR'].isin(col_one_list)]

#Combina los 2 archivos EXCEL por el Nombre del empleado
SW2021=pd.merge(df4, df_empleados, on='Nombre completo OBSERVADOR', how='outer')

#Crea una nueva columna con true/false si en la columna pais hay nulos o no.
SW2021['ESTADO DEL EMPLEADO'] = SW2021['PAIS'].isnull()

#reemplaza True por Baja y False por Activo.
SW2021['ESTADO DEL EMPLEADO'] =SW2021['ESTADO DEL EMPLEADO'].replace({True: 'Baja',False: 'Activo',})

#Extraemos de la fecha de la columna "fecha de creación" el mes en este caso "ene" y lo guardamos 
#en una nueva columna llamada "Mes"
SW2021['Mes']=SW2021['Fecha de creación'].str.extract(r'([a-z]+)')

#Creamos una lista con si en la columna Manager o coodinador.
columna_categoria=[]
for e in SW2021['MANAGER']:
    if e == 'Manager':
        columna_categoria.append("MANAGER")
        
    else:
        columna_categoria.append("COORDINADOR")
    
#Creamos nueva columna con la lista columna_categoria.          
SW2021['MANAGER/COORDINADOR']=columna_categoria

#Creamos 3 listas con las familias de cada categoría.

operacional=['CER', 'GTS', 'NS', 'BVN',
       'IoperacionalSO 17021/65', 'NC', 'VOC', 'HSE', 'IAA', 'C&O', 'TRAINING',
       'IND', 'VOC MARRUECOS', 'ICA', 'STF', 'OIL & PETROL', 'ISV',
       'METAL & MINERAL', 'AGRICOLA', 'CTC', 'ISO17020', 'ENV', 'TQR', 'HSI', 'ISO17025', 
          'HSE Endesa','VDT' ]


sales=['SALES','SALES&MARKETING']

soporte=['INFORMATION TECHNOLOGY','FINANCE','MANAGEMENT','HUMAN RESOURCES','OFFICE','LEGAL' 'INFORMATION SYSTEM','PURCHASING & G.S.',
         'CREDIT COLLECTION','GIS']

columna_familia=[]
for e in SW2021['NIVEL3']:
    if e in operacional:
        columna_familia.append("OPERACIONAL")
    elif e in sales:
        columna_familia.append("SALES")
    elif e in soporte:
        columna_familia.append("SOPORTE")
    elif e not in operacional or sales or soporte:
        columna_familia.append("NIVEL 3 No definido")

SW2021['FAMILIA']=columna_familia

#creamos un nuevo Df con las columnas de la union entre DF_empleados y el archívo de las SW.
SW_MES=SW2021[['Nombre completo OBSERVADOR','ESTADO DEL EMPLEADO','MANAGER/COORDINADOR', 'FAMILIA','PAIS', 'EMPRESA', 'RAZON SOCIAL', 'CIF', 'CODIGO FLEX EMPRESA',
       'CODIGO GPCN', 'PRIMER APELLIDO', 'SEGUNDO APELLIDO', 'NOMBRE',
       'FECHA NACIMIENTO', 'Nº FLEX', 'CODIGO SF', 'MAIL TRABAJADOR',
       'FECHA ANTIGUEDAD', 'NIF', 'SEXO', 'MODALIDAD DEL CONTRATO', 'NIVEL1',
       'NIVEL2', 'NIVEL3', 'PC', 'OFICINA FISICA', 'CODIGO FLEX OFICINA',
       'CATEGORIA / PUESTO', 'CONVENIO', 'NIVEL SALARIAL', 'FTE',
       'GRUPO COSTE', 'MANAGER', 'Nº S.S.', 'GRUPO COTIZACION',
       'CENTRO DE COTIZACION', 'RESPONSABLE PC',
       'APROBADOR PORTAL DEL EMPLEADO', 'MAIL APROBADOR',
       'SEGUNDO APROBADOR COMPRAS', 'index', 'Número', 'Fecha de creación','Mes', 'Nombre de la persona o personas observadas', 'Grupo Operativo', 'País',
       'Entidad', 'Sitio', 'Nombre del sitio de BV', 'Nombre del cliente',
       'Dirección del sitio','1. ¿Mente en la tarea?',
       '2. ¿Ojos puestos en la tarea?', '3. ¿Utiliza el equipo correctamente?',
       '4. ¿Realiza la tarea sin apresurarse?', '5. ¿Usa el EPI definido?',
       '6. ¿Sigue procedimientos de trabajo seguros?',
       '7. Se obtiene la autorización ...',
       '8. Verifica el entorno de trabajo, 2 min para mi seguridad',
       '9. El personal actuó con seguridad para la tarea observada.',
       '10.Conoce la Ruta de Evaluación de Emergencias y el Punto de Reunión',
       '11. La persona es consciente de la necesidad de reportar Cuasi Accidentes y Condiciones Inseguras?.',
       '12. El personal deja de trabajar si la situación no es segura.',
       '13. El personal esta capacitado y suficientemente formado para la Tarea.',
       '14. Los EPIS definidos son adecuados y se usan correctamente.',
       '15. los EPIS estan en buen estado, bien mantenidos y se almacenan correctamente.',
       '16. Buena limpieza del área de trabajo',
       '17. Área libre de riesgos de resbalones, tropiezos y caídas',
       '18. Pasillos, salidas de emergencia y equipos de emergencia no estan obstruidos.',
       '19. Derrames controlados',
       '20. Todos los contenedores en uso y en el área están etiquetados.',
       '21. Sin ruidos, polvo ni olores',
       '22. Las sustancias peligrosas se almacenan adecuadamente',
       '23. El área de trabajo está protegida contra riesgos',
       '24. Iluminación y ventilación suficientes.',
       '25. Uso de equipos intrínsecamente seguro.',
       '26. Protección de la maquina o señal de bloqueo-etiquetado disponible',
       '27. El andamio o la escalera son seguros para su uso.',
       '¿Usé mi autorización para detener el trabajo?',
       'Comentarios / Plan de acción']]

#Asignamos nuevas columnas a SW_MES.
SW_MES=SW_MES.assign(eneP='',Acum_Ene='',febP='',Acum_Feb='',marP='',Acum_Mar='',abrP='',Acum_Abr='',mayP='',Acum_May='',
       junP='',Acum_Jun='',julP='',Acum_Jul='',agoP='',Acum_Ago='',sepP='',Acum_Sep='',octP='',Acum_Oct='',
        novP='',Acum_Nov='',dicP='',Acum_Dic='')

del Lista_sw2['CRUCE']

df_nombres= pd.read_excel('/home/antonio/Documentos/BV/SW_informe_dataCleaning/Data/LISTA SW.xlsx', engine='openpyxl')

def fun_to_apply(name):
    area_dict = dict(zip(df_nombres['Nombres de los que hacen SW'], df_nombres['objetivo año']))
    if name in area_dict:
            return area_dict[name]
    else:
            return 0
SW_MES['Objetivo 2021']  = SW_MES['Nombre completo OBSERVADOR'].apply(lambda x: fun_to_apply(x))

SW_MES['eneP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
SW_MES['febP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
SW_MES['marP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
SW_MES['abrP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
SW_MES['mayP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
SW_MES['junP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
SW_MES['julP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
SW_MES['agoP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
SW_MES['sepP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
SW_MES['octP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
SW_MES['novP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
SW_MES['marP'] = np.where((SW_MES['Objetivo 2021'] == 4), 1, 0)
SW_MES['junP'] = np.where((SW_MES['Objetivo 2021'] == 4), 1, 0)
SW_MES['sepP'] = np.where((SW_MES['Objetivo 2021'] == 4), 1, 0)
SW_MES['dicP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
SW_MES['dicP'] = np.where((SW_MES['dicP'] == 0), 1, SW_MES['dicP'])
SW_MES['Acum_SW']=0
SW_MES['Mes'] = SW_MES['Mes'].fillna(0)
lista_fecha=[]
for e in SW_MES['Mes']:
    lista_fecha.append(e)
SW_MES['Mes']=lista_fecha
list_fechas=list(SW_MES['Mes'])
acum_ene=[]
for e in list_fechas:
    contador=0
    if e == 'ene':
        acum_ene.append(contador+1)
    else:
        acum_ene.append(0)
SW_MES['Acum_Ene']=acum_ene

acum_feb=[]
for e in list_fechas:
    contador=0
    if e == 'feb':
        acum_feb.append(contador+1)
    else:
        acum_feb.append(0)
SW_MES['Acum_Feb']=acum_feb

acum_mar=[]
for e in list_fechas:
    contador=0
    if e == 'mar':
        acum_mar.append(contador+1)
    else:
        acum_mar.append(0)
SW_MES['Acum_Mar']=acum_mar

acum_abr=[]
for e in list_fechas:
    contador=0
    if e == 'abr':
        acum_abr.append(contador+1)
    else:
        acum_abr.append(0)
SW_MES['Acum_Abr']=acum_abr

acum_may=[]
for e in list_fechas:
    contador=0
    if e == 'may':
        acum_may.append(contador+1)
    else:
        acum_may.append(0)
SW_MES['Acum_May']=acum_may

acum_jun=[]
for e in list_fechas:
    contador=0
    if e == 'jun':
        acum_jun.append(contador+1)
    else:
        acum_jun.append(0)
SW_MES['Acum_Jun']=acum_jun

acum_jul=[]
for e in list_fechas:
    contador=0
    if e == 'may':
        acum_jul.append(contador+1)
    else:
        acum_jul.append(0)
SW_MES['Acum_Jul']=acum_jul

acum_ago=[]
for e in list_fechas:
    contador=0
    if e == 'ago':
        acum_ago.append(contador+1)
    else:
        acum_ago.append(0)
SW_MES['Acum_Ago']=acum_ago

acum_Sep=[]
for e in list_fechas:
    contador=0
    if e == 'sep':
        acum_Sep.append(contador+1)
    else:
        acum_Sep.append(0)
SW_MES['Acum_Sep']=acum_Sep

acum_oct=[]
for e in list_fechas:
    contador=0
    if e == 'oct':
        acum_oct.append(contador+1)
    else:
        acum_oct.append(0)
SW_MES['Acum_Oct']=acum_oct

acum_nov=[]
for e in list_fechas:
    contador=0
    if e == 'nov':
        acum_nov.append(contador+1)
    else:
        acum_nov.append(0)
SW_MES['Acum_Nov']=acum_nov

acum_dic=[]
for e in list_fechas:
    contador=0
    if e == 'dic':
        acum_dic.append(contador+1)
    else:
        acum_dic.append(0)
SW_MES['Acum_Dic']=acum_dic

SW_MES['Acum_SW']=SW_MES[ 'Acum_Ene']+SW_MES[ 'Acum_Feb']+SW_MES[ 'Acum_Mar']+SW_MES['Acum_Abr']+SW_MES[ 'Acum_May']+SW_MES[ 'Acum_Jun']+SW_MES[ 'Acum_Jul']+SW_MES[ 'Acum_Ago']+SW_MES[ 'Acum_Sep']+SW_MES[ 'Acum_Oct']+SW_MES[ 'Acum_Nov']+SW_MES[ 'Acum_Dic']

SW_MES = SW_MES.loc[:,~SW_MES.columns.duplicated()]

for i in range(len(col_one_list)):
    col_one_list[i] = col_one_list[i].upper() 

SW_MES_lista=SW_MES[SW_MES['Nombre completo OBSERVADOR'].isin(col_one_list)]
SW_MES_lista['Nombre completo OBSERVADOR'].str.strip().str.lstrip()

SW_MES_lista['Nombre completo OBSERVADOR'] = SW_MES_lista['Nombre completo OBSERVADOR'].str.replace('.', '')

SW_MES_lista.to_excel('/home/antonio/Documentos/BV/SW_informe_dataCleaning/Data/SW_MES_lista.xlsx')

df8= pd.read_excel('/home/antonio/Documentos/BV/SW_informe_dataCleaning/Data/SW_MES_lista.xlsx', engine='openpyxl')

listaaanombre=[]
listaaobjetivo=[]
count=0
for e in df8['Nombre completo OBSERVADOR']:
    if count==171:
        break
    if e not in listaaanombre:
        listaaobjetivo.append(df8['Objetivo 2021'][count])
        count=count + 1
        listaaanombre.append(e)
    elif e in listaaanombre:
        count=count + 1
        listaaobjetivo.append(0)
        listaaanombre.append(0)
df8['Objetivos 2021_unicos']=listaaobjetivo

del df8['Unnamed: 0']

df8[['1. ¿Mente en la tarea?',
       '2. ¿Ojos puestos en la tarea?', '3. ¿Utiliza el equipo correctamente?',
       '4. ¿Realiza la tarea sin apresurarse?', '5. ¿Usa el EPI definido?',
       '6. ¿Sigue procedimientos de trabajo seguros?',
       '7. Se obtiene la autorización ...',
       '8. Verifica el entorno de trabajo, 2 min para mi seguridad',
       '9. El personal actuó con seguridad para la tarea observada.',
       '10.Conoce la Ruta de Evaluación de Emergencias y el Punto de Reunión',
       '11. La persona es consciente de la necesidad de reportar Cuasi Accidentes y Condiciones Inseguras?.',
       '12. El personal deja de trabajar si la situación no es segura.',
       '13. El personal esta capacitado y suficientemente formado para la Tarea.',
       '14. Los EPIS definidos son adecuados y se usan correctamente.',
       '15. los EPIS estan en buen estado, bien mantenidos y se almacenan correctamente.',
       '16. Buena limpieza del área de trabajo',
       '17. Área libre de riesgos de resbalones, tropiezos y caídas',
       '18. Pasillos, salidas de emergencia y equipos de emergencia no estan obstruidos.',
       '19. Derrames controlados',
       '20. Todos los contenedores en uso y en el área están etiquetados.',
       '21. Sin ruidos, polvo ni olores',
       '22. Las sustancias peligrosas se almacenan adecuadamente',
       '23. El área de trabajo está protegida contra riesgos',
       '24. Iluminación y ventilación suficientes.',
       '25. Uso de equipos intrínsecamente seguro.',
       '26. Protección de la maquina o señal de bloqueo-etiquetado disponible',
       '27. El andamio o la escalera son seguros para su uso.',
       '¿Usé mi autorización para detener el trabajo?',
       'Comentarios / Plan de acción']] = df8[['1. ¿Mente en la tarea?',
       '2. ¿Ojos puestos en la tarea?', '3. ¿Utiliza el equipo correctamente?',
       '4. ¿Realiza la tarea sin apresurarse?', '5. ¿Usa el EPI definido?',
       '6. ¿Sigue procedimientos de trabajo seguros?',
       '7. Se obtiene la autorización ...',
       '8. Verifica el entorno de trabajo, 2 min para mi seguridad',
       '9. El personal actuó con seguridad para la tarea observada.',
       '10.Conoce la Ruta de Evaluación de Emergencias y el Punto de Reunión',
       '11. La persona es consciente de la necesidad de reportar Cuasi Accidentes y Condiciones Inseguras?.',
       '12. El personal deja de trabajar si la situación no es segura.',
       '13. El personal esta capacitado y suficientemente formado para la Tarea.',
       '14. Los EPIS definidos son adecuados y se usan correctamente.',
       '15. los EPIS estan en buen estado, bien mantenidos y se almacenan correctamente.',
       '16. Buena limpieza del área de trabajo',
       '17. Área libre de riesgos de resbalones, tropiezos y caídas',
       '18. Pasillos, salidas de emergencia y equipos de emergencia no estan obstruidos.',
       '19. Derrames controlados',
       '20. Todos los contenedores en uso y en el área están etiquetados.',
       '21. Sin ruidos, polvo ni olores',
       '22. Las sustancias peligrosas se almacenan adecuadamente',
       '23. El área de trabajo está protegida contra riesgos',
       '24. Iluminación y ventilación suficientes.',
       '25. Uso de equipos intrínsecamente seguro.',
       '26. Protección de la maquina o señal de bloqueo-etiquetado disponible',
       '27. El andamio o la escalera son seguros para su uso.',
       '¿Usé mi autorización para detener el trabajo?',
       'Comentarios / Plan de acción']].fillna('N/A')

df_SPM= pd.read_excel('/home/antonio/Documentos/BV/SW_informe_dataCleaning/Data/TECNICO SPM.xlsx', engine='openpyxl')

def fun_to_apply(name):
    area_dict = dict(zip(df_SPM['NIVEL2'], df_SPM['NOMBRE TECNICO SPM']))
    if name in area_dict:
            return area_dict[name]
    else:
            return 'SIN ASIGNAR'

df8['NOMBRE TECNICO SPM']  = df8['NIVEL2'].apply(lambda x: fun_to_apply(x))       

df8.to_excel('/home/antonio/Documentos/BV/SW_informe_dataCleaning/Data/SW_MES_PWB.xlsx')

print('too bien')