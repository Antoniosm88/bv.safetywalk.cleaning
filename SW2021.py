import pandas as pd
import SW
import HC
import numpy as np

def SW_2021(df4,df_empleados):
    # Combina los 2 archivos EXCEL por el Nombre del empleado
    SW2021 = pd.merge(df4, df_empleados, on='Nombre completo OBSERVADOR', how='outer')
    #crea una columna nueva con los nulos y no nulos de la columna país.
    SW2021['ESTADO DEL EMPLEADO'] = SW2021['PAIS'].isnull()
    # reemplaza True por Baja y False por Activo.
    SW2021['ESTADO DEL EMPLEADO'] = SW2021['ESTADO DEL EMPLEADO'].replace({True: 'Baja', False: 'Activo', })
    # Extraemos de la fecha de la columna "fecha de creación" el mes en este caso "ene" y lo guardamos
    # en una nueva columna llamada "Mes"
    SW2021['Mes'] = SW2021['Fecha de creación'].str.extract(r'([a-z]+)')
    columna_categoria = []
    for e in SW2021['MANAGER']:
        if e == 'Manager':
            columna_categoria.append("MANAGER")

        else:
            columna_categoria.append("COORDINADOR")
    SW2021['MANAGER/COORDINADOR'] = columna_categoria
    operacional = ['CER', 'GTS', 'NS', 'BVN',
                   'IoperacionalSO 17021/65', 'NC', 'VOC', 'HSE', 'IAA', 'C&O', 'TRAINING',
                   'IND', 'VOC MARRUECOS', 'ICA', 'STF', 'OIL & PETROL', 'ISV',
                   'METAL & MINERAL', 'AGRICOLA', 'CTC', 'ISO17020', 'ENV', 'TQR', 'HSI', 'ISO17025',
                   'HSE Endesa', 'VDT']

    sales = ['SALES', 'SALES&MARKETING']

    soporte = ['INFORMATION TECHNOLOGY', 'FINANCE', 'MANAGEMENT', 'HUMAN RESOURCES', 'OFFICE',
               'LEGAL' 'INFORMATION SYSTEM', 'PURCHASING & G.S.',
               'CREDIT COLLECTION', 'GIS']
    columna_familia = []
    for e in SW2021['NIVEL3']:
        if e in operacional:
            columna_familia.append("OPERACIONAL")
        elif e in sales:
            columna_familia.append("SALES")
        elif e in soporte:
            columna_familia.append("SOPORTE")
        elif e not in operacional or sales or soporte:
            columna_familia.append("NIVEL 3 No definido")
    SW2021['FAMILIA'] = columna_familia
    # creamos un nuevo Df con las columnas de la union entre DF_empleados y el archívo de las SW.
    SW_MES = SW2021[
        ['Nombre completo OBSERVADOR', 'ESTADO DEL EMPLEADO', 'MANAGER/COORDINADOR', 'FAMILIA', 'PAIS', 'EMPRESA',
         'RAZON SOCIAL', 'CIF', 'CODIGO FLEX EMPRESA',
         'CODIGO GPCN', 'PRIMER APELLIDO', 'SEGUNDO APELLIDO', 'NOMBRE',
         'FECHA NACIMIENTO', 'Nº FLEX', 'CODIGO SF', 'MAIL TRABAJADOR',
         'FECHA ANTIGUEDAD', 'NIF', 'SEXO', 'MODALIDAD DEL CONTRATO', 'NIVEL1',
         'NIVEL2', 'NIVEL3', 'PC', 'OFICINA FISICA', 'CODIGO FLEX OFICINA',
         'CATEGORIA / PUESTO', 'CONVENIO', 'NIVEL SALARIAL', 'FTE',
         'GRUPO COSTE', 'MANAGER', 'Nº S.S.', 'GRUPO COTIZACION',
         'CENTRO DE COTIZACION', 'RESPONSABLE PC',
         'APROBADOR PORTAL DEL EMPLEADO', 'MAIL APROBADOR',
         'SEGUNDO APROBADOR COMPRAS', 'index', 'Número', 'Fecha de creación', 'Mes',
         'Nombre de la persona o personas observadas', 'Grupo Operativo', 'País',
         'Entidad', 'Sitio', 'Nombre del sitio de BV', 'Nombre del cliente',
         'Dirección del sitio', '1. ¿Mente en la tarea?',
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
    SW_MES = SW_MES.assign(eneP='', Acum_Ene='', febP='', Acum_Feb='', marP='', Acum_Mar='', abrP='', Acum_Abr='',
                           mayP='', Acum_May='',
                           junP='', Acum_Jun='', julP='', Acum_Jul='', agoP='', Acum_Ago='', sepP='', Acum_Sep='',
                           octP='', Acum_Oct='',
                           novP='', Acum_Nov='', dicP='', Acum_Dic='')
    del Lista_sw2['CRUCE']
    dict_names = Lista_sw2.to_dict()

    def fun_to_apply(name):
        area_dict = dict(zip(df_nombres['Nombres de los que hacen SW'], df_nombres['objetivo año']))
        if name in area_dict:
            return area_dict[name]
        else:
            return 0

    SW_MES['Objetivo 2021'] = SW_MES['Nombre completo OBSERVADOR'].apply(lambda x: fun_to_apply(x))
    meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
    SW_MES['marP'] = np.where((SW_MES['Objetivo 2021'] == 4), 1, 0)
    SW_MES['junP'] = np.where((SW_MES['Objetivo 2021'] == 4), 1, 0)
    SW_MES['sepP'] = np.where((SW_MES['Objetivo 2021'] == 4), 1, 0)
    SW_MES['dicP'] = np.where((SW_MES['Objetivo 2021'] == 4), 1, 0)
    SW_MES['dicP'] = np.where((SW_MES['Objetivo 2021'] == 4), 1, 0)
    SW_MES['febP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
    SW_MES['marP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
    SW_MES['abrP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
    SW_MES['junP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
    SW_MES['julP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
    SW_MES['agoP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
    SW_MES['sepP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
    SW_MES['octP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
    SW_MES['novP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
    SW_MES['dicP'] = np.where((SW_MES['Objetivo 2021'] == 12), 1, 0)
    SW_MES['Acum_SW'] = 0
    SW_MES['Mes'] = SW_MES['Mes'].fillna(0)
    lista_fecha = []
    for e in SW_MES['Mes']:
        lista_fecha.append(e)
    SW_MES['Mes'] = lista_fecha
    list_fechas = list(SW_MES['Mes'])
    acum_ene = []
    for e in list_fechas:
        contador = 0
        if e == 'ene':
            acum_ene.append(contador + 1)
        else:
            acum_ene.append(0)
    SW_MES['Acum_Ene'] = acum_ene
    acum_ene.append(0)
    acum_feb = []
    for e in list_fechas:
        contador = 0
        if e == 'feb':
            acum_feb.append(contador + 1)
        else:
            acum_feb.append(0)
    SW_MES['Acum_Feb'] = acum_feb
    acum_mar = []
    for e in list_fechas:
        contador = 0
        if e == 'mar':
            acum_mar.append(contador + 1)
        else:
            acum_mar.append(0)
    SW_MES['Acum_Mar'] = acum_mar
    acum_abr = []
    for e in list_fechas:
        contador = 0
        if e == 'abr':
            acum_abr.append(contador + 1)
        else:
            acum_abr.append(0)
    SW_MES['Acum_Abr'] = acum_abr
    acum_may = []
    for e in list_fechas:
        contador = 0
        if e == 'may':
            acum_may.append(contador + 1)
        else:
            acum_may.append(0)
    SW_MES['Acum_May'] = acum_may
    acum_jun = []
    for e in list_fechas:
        contador = 0
        if e == 'jun':
            acum_jun.append(contador + 1)
        else:
            acum_jun.append(0)
    SW_MES['Acum_Jun'] = acum_jun
    acum_jul = []
    for e in list_fechas:
        contador = 0
        if e == 'may':
            acum_jul.append(contador + 1)
        else:
            acum_jul.append(0)
    SW_MES['Acum_Jul'] = acum_jul
    acum_ago = []
    for e in list_fechas:
        contador = 0
        if e == 'ago':
            acum_ago.append(contador + 1)
        else:
            acum_ago.append(0)
    SW_MES['Acum_Ago'] = acum_ago
    acum_Sep = []
    for e in list_fechas:
        contador = 0
        if e == 'sep':
            acum_Sep.append(contador + 1)
        else:
            acum_Sep.append(0)
    SW_MES['Acum_Sep'] = acum_Sep
    acum_oct = []
    for e in list_fechas:
        contador = 0
        if e == 'oct':
            acum_oct.append(contador + 1)
        else:
            acum_oct.append(0)
    SW_MES['Acum_Oct'] = acum_oct
    acum_nov = []
    for e in list_fechas:
        contador = 0
        if e == 'nov':
            acum_nov.append(contador + 1)
        else:
            acum_nov.append(0)
    SW_MES['Acum_Nov'] = acum_nov
    acum_dic = []
    for e in list_fechas:
        contador = 0
        if e == 'dic':
            acum_dic.append(contador + 1)
        else:
            acum_dic.append(0)
    SW_MES['Acum_Dic'] = acum_dic
    SW_MES['Acum_SW'] = SW_MES['Acum_Ene'] + SW_MES['Acum_Feb'] + SW_MES['Acum_Mar'] + SW_MES['Acum_Abr'] + SW_MES[
        'Acum_May'] + SW_MES['Acum_Jun'] + SW_MES['Acum_Jul'] + SW_MES['Acum_Ago'] + SW_MES['Acum_Sep'] + SW_MES[
                            'Acum_Oct'] + SW_MES['Acum_Nov'] + SW_MES['Acum_Dic']
    for i in range(len(col_one_list)):
        col_one_list[i] = col_one_list[i].upper()
    SW_MES['Nombre completo OBSERVADOR'] = SW_MES['Nombre completo OBSERVADOR'].str.replace('.', '')
    SW_MES['Nombre completo OBSERVADOR'].str.strip().str.lstrip()
    SW_MES_lista = SW_MES[SW_MES['Nombre completo OBSERVADOR'].isin(col_one_list)]
    return SW_MES_lista.to_excel('../Data/SW_MES_lista.xlsx')