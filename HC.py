import pandas as pd
import SW
df_empleados= pd.read_excel('../Data/Resumen HC Enero 2021.xlsx',engine='openpyxl',sheet_name='HC ENERO')
def cleaning_HC(df_empleados):
    # Sustituimos el los nombres sin segundo apellido por un  ".".
    df_empleados['SEGUNDO APELLIDO'] = df_empleados['SEGUNDO APELLIDO'].fillna('.')
    # Creamos un nuevo df con el filtro de NO ESPAÑA(Portugal) y Segundo apellido "."
    clean_country_PORTUGAL = df_empleados[
        (df_empleados['PAIS'] != 'ESPAÑA') & (df_empleados['SEGUNDO APELLIDO'] != '.')]
    #Sustituimos la columna de primer apellido por la de segundo apellido
    clean_country_PORTUGAL['PRIMER APELLIDO']=clean_country_PORTUGAL['SEGUNDO APELLIDO']
    # Modificamos toda la columna de segundo apellido por "."
    clean_country_PORTUGAL['SEGUNDO APELLIDO'] = '.'
    # concatenamos el df de empleados con el que hemos creado y modificado
    df_empleados = pd.concat([df_empleados, clean_country_PORTUGAL], ignore_index=True)
    # creamos una columna uniendo Nombre+primerapellido+segundoapellido
    df_empleados['Nombre completo OBSERVADOR'] = df_empleados['NOMBRE'] + " " + df_empleados['PRIMER APELLIDO'] + " " + \
                                                 df_empleados['SEGUNDO APELLIDO']
    # Pasamos a mayúsculas la nueva columna creada.
    df_empleados['Nombre completo OBSERVADOR'] = df_empleados['Nombre completo OBSERVADOR'].str.upper()
    # creamos un nuevo df con los nombres que aparecen en la lista de los empleados que tienen que hacer las sw en 2021.
    df_empleados = df_empleados[df_empleados['Nombre completo OBSERVADOR'].isin(col_one_list)]
    return df_empleados
