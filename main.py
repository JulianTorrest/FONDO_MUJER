import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Título de la aplicación
st.title('Lector de Archivos Excel desde GitHub')

# URLs de los archivos de Excel en tu repositorio de GitHub
excel_files = {
    'DIVIPOLA_Municipios': 'https://raw.githubusercontent.com/JulianTorrest/FONDO_MUJER/main/01.%20DIVIPOLA_Municipios.xlsx',
    'Proyección de Población': 'https://raw.githubusercontent.com/JulianTorrest/FONDO_MUJER/main/02.%20Proyecci%C3%B3n%20de%20poblacion-Mun-2020-2035.xlsx',
    'Ingresos per cápita predial': 'https://raw.githubusercontent.com/JulianTorrest/FONDO_MUJER/main/03.%20Ingresos%20per%20c%C3%A1pita%20por%20impuesto%20predial.xlsx',
    'Total de Predios': 'https://raw.githubusercontent.com/JulianTorrest/FONDO_MUJER/main/04.%20Total%20de%20predios.xlsx',
    'Ingresos per cápita industria y comercio': 'https://raw.githubusercontent.com/JulianTorrest/FONDO_MUJER/main/05.%20Ingresos%20per%20c%C3%A1pita%20por%20impuesto%20a%20la%20Industria%20y%20al%20comercio.xlsx'
}

# Un selectbox para que el usuario elija el archivo
selected_file_name = st.selectbox('Selecciona un archivo para ver:', list(excel_files.keys()))

if selected_file_name:
    url = excel_files[selected_file_name]

    try:
        # Usamos requests para obtener el contenido del archivo
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la solicitud no fue exitosa

        # Usar BytesIO para evitar la advertencia de `FutureWarning`
        excel_data = BytesIO(response.content)

        # Leemos el contenido como un archivo en memoria
        df = pd.read_excel(excel_data, engine='openpyxl')

        # --- Solución a los errores de tipo de dato de PyArrow ---
        # 1. Rellenar los valores NaN en columnas de texto
        string_cols = df.select_dtypes(include='object').columns
        df[string_cols] = df[string_cols].fillna('')

        # 2. Convertir todas las columnas de texto a tipo string
        # Esto asegura que no haya tipos de datos mixtos (int y string) en la misma columna.
        df[string_cols] = df[string_cols].astype(str)

        # 3. Solución para el problema de 'Expected bytes' en columnas 'Unnamed'
        # Convertir a string cualquier columna con el nombre 'Unnamed:'
        for col in df.columns:
            if 'Unnamed:' in str(col):
                df[col] = df[col].astype(str)
        
        st.subheader(f'Datos del archivo: {selected_file_name}')
        
        # Muestra la tabla en la aplicación de Streamlit
        st.dataframe(df)

    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar el archivo desde GitHub: {e}")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
