import pandas as pd

#Carga el excel en un Dataframe (datos de las SW)
df= pd.read_excel('../Data/BV Safety_All Safety Walks.xlsx', engine='openpyxl')
def cleaning_SW(df):
    # Borra las primeras 4 filas del Df
    df1 = df.drop([0, 1, 2, 3])
    new_header = df1.iloc[0]  # grab the first row for the header
    df2 = df1[1:]  # take the data less the header row
    df2.columns = new_header  # set the header row as the df header
    df3 = df2.reset_index()
    # Cambiamos el nómbre de las columnas
    df4 = df3.rename(columns={'Number': 'Número',
                              'Created Date': 'Fecha de creación',
                              'Name of the Observer': 'Nombre del observador',
                              'Name of the Observed Person(s)': 'Nombre de la persona o personas observadas',
                              'Operating Group': 'Grupo Operativo',
                              'Country': 'País',
                              'Entity': 'Entidad',
                              'Site': 'Sitio',
                              'BV Site Name': 'Nombre del sitio de BV',
                              'Client Name': 'Nombre del cliente',
                              'Site Address': 'Dirección del sitio',
                              '1. Mind On Task?': '1. ¿Mente en la tarea?',
                              '2. Eyes on Task?': '2. ¿Ojos puestos en la tarea?',
                              '3. Using equpment properly?': "3. ¿Utiliza el equipo correctamente?",
                              '4. Performing task while not rushing?': "4. ¿Realiza la tarea sin apresurarse?",
                              '5. Wearing prescribed PPE?': '5. ¿Usa el EPI definido?',
                              '6. Following Safe Working Procedures?': '6. ¿Sigue procedimientos de trabajo seguros?',
                              '7. Authorization is obtained...': '7. Se obtiene la autorización ...',
                              '8. Check surrounding work areas...': '8. Verifica el entorno de trabajo, 2 min para mi seguridad',
                              '9. Personnel acted safely for the task observed': '9. El personal actuó con seguridad para la tarea observada.',
                              '10. Aware of the Emergency Evacuation...': '10.Conoce la Ruta de Evaluación de Emergencias y el Punto de Reunión',
                              '11. The person is aware of the need to report near hit and unsafe situation.': '11. La persona es consciente de la necesidad de reportar Cuasi Accidentes y Condiciones Inseguras?.',
                              '12. Personnel stops Working if the situation is unsafe.': '12. El personal deja de trabajar si la situación no es segura.',
                              '13. Personnel is competent and trained...': '13. El personal esta capacitado y suficientemente formado para la Tarea.',
                              '14. Adequate and worn correctly the applicable PPE': '14. Los EPIS definidos son adecuados y se usan correctamente.',
                              '15. Good conditions, well maintained and properly stored.': '15. los EPIS estan en buen estado, bien mantenidos y se almacenan correctamente.',
                              '16. Good housekeeping of the work area...': '16. Buena limpieza del área de trabajo',
                              '17. Area Free of Slip Trip and Fall Hazards': '17. Área libre de riesgos de resbalones, tropiezos y caídas',
                              '18. Walkways, aisles, emergency exits...': '18. Pasillos, salidas de emergencia y equipos de emergencia no estan obstruidos.',
                              '19. Spillage controlled': '19. Derrames controlados',
                              '20. All containers in use and in the area are labelled.': '20. Todos los contenedores en uso y en el área están etiquetados.',
                              '21. No Noise, Dust, Odor Issues': '21. Sin ruidos, polvo ni olores',
                              '22. Hazardous substances are stored properly': '22. Las sustancias peligrosas se almacenan adecuadamente',
                              '23. The work area is secured from hazards...': '23. El área de trabajo está protegida contra riesgos',
                              '24. Sufficient lighting and ventilation.': '24. Iluminación y ventilación suficientes.',
                              '25. Use intrinsically safe equipment...': '25. Uso de equipos intrínsecamente seguro.',
                              '26. Machine guarding or Lock-Out-Tag-Out...': '26. Protección de la maquina o señal de bloqueo-etiquetado disponible',
                              '27. Scaffold or ladder is safe for use.': '27. El andamio o la escalera son seguros para su uso.',
                              'Did I use my Stop Work Authority?': '¿Usé mi autorización para detener el trabajo?',
                              'Comments / Action Plan': 'Comentarios / Plan de acción'},

                     inplace=False)
    # Cargamos el excel donde están los empreados que realizan las SW
    Lista_sw2 = pd.read_excel('../Data/LISTA SW.xlsx', engine='openpyxl', sheet_name='Hoja1')
    col_one_list = list(Lista_sw2['Nombres de los que hacen SW'])
    # Homogeneizamos la columna donde estan los nombres de los empleados que han subido las SW a QESIS
    nombres = []
    for e in df4['Nombre del observador']:
        word_list = e.split()
        if word_list[-1].isupper() == True:
            nombres.append(word_list)
        if word_list[-1].isupper() == False:
            word_list.remove(word_list[-1])
            nombres.append(word_list)

    # Esta función convierte las listas en strings
    def listToString(s):

        # initialize an empty string
        str1 = " "

        # return string
        return (str1.join(s))

    # La lista donde se ha homogeneizado los nombres se transforma en strings
    nombres2 = []
    for e in nombres:
        nombres2.append(listToString(e))
        # Agregamos la lista con los nombres limpios a la columna del Df y las pasamos a mayúsculas.

    df4['Nombre del observador'] = nombres2
    df4['Nombre del observador'] = df4['Nombre del observador'].str.upper()
    # creamos un nuevo Df con un filtro para elegir Portugal
    nombres_PORTUGAL = df4[(df4['País'] == ' Portugal ')]
    # Bucle for para introducir en una lista los nombres de los portugueses que tienen 2 apellidos.
    # Si tienen + de 3 elementos debe de coger el 2º elemento y borrarlo.
    nombre_portugal = []
    for e in nombres_PORTUGAL['Nombre del observador']:
        word_list = e.split()
        if len(word_list) >= 3:
            word_list.remove(word_list[-2])
            nombre_portugal.append(word_list)
        else:
            nombre_portugal.append(word_list)
    # aplicamos la función para pasar de list a string.
    nombres3 = []
    for e in nombre_portugal:
        nombres3.append(listToString(e))
    nombres_ESPAÑAs = df4[(df4['País'] == ' Spain ')]
    nombres4 = []
    for e in nombres_ESPAÑAs:
        nombres4.append(listToString(e))
    # Añadimos los nombres modificados a la columna del Df que creamos con el filtro.
    nombres_PORTUGAL['Nombre del observador'] = nombres3
    # Concatenamos el df principal con el que creamos con el filtro.
    df4 = pd.concat([df4, nombres_PORTUGAL], ignore_index=True)
    nombre_5 = []
    for e in df4['Nombre del observador']:
        word_list = e.split()
        nombre_5.append(word_list)
    for e in nombre_5:
        if len(e) == 2:
            e.extend(["."])
    nombres6 = []
    for e in nombre_5:
        nombres6.append(listToString(e))
    df4['Nombre del observador'] = nombres6
    df4.reset_index(drop=True, inplace=True)
    lista_pais = pd.unique(df4['País']).tolist()
    clean_country = df4[(df4['País'] != ' Spain ') & (df4['País'] != ' Portugal ')].index
    # Delete these row indexes from dataFrame
    df4.drop(clean_country, inplace=True)
    lista_grupo = pd.unique(df4['Grupo Operativo']).tolist()
    df4 = df4.rename(columns={'Nombre del observador': 'Nombre completo OBSERVADOR'})
    # Creamos una lista con las preguntas de las SW
    list_preguntas = ['1. ¿Mente en la tarea?',
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
    # Realizamos a  todas las columnas y sustituimos los elementos vacios por N/A.
    df4[list_preguntas] = df4[list_preguntas].fillna('N/A')
    return df4