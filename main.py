import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Título de la aplicación
st.title('Lector de Archivos CSV desde GitHub')

# URLs de los archivos CSV en tu repositorio de GitHub
csv_files = {
    'DIVIPOLA_Municipios': 'https://raw.githubusercontent.com/JulianTorrest/FONDO_MUJER/main/01.%20DIVIPOLA_Municipios.csv',
    'Proyección de Población': 'https://raw.githubusercontent.com/JulianTorrest/FONDO_MUJER/main/02.%20Proyecci%C3%B3n%20de%20poblacion-Mun-2020-2035.csv',
    'Ingresos per cápita predial': 'https://raw.githubusercontent.com/JulianTorrest/FONDO_MUJER/main/03.%20Ingresos%20per%20c%C3%A1pita%20por%20impuesto%20predial.csv',
    'Total de Predios': 'https://raw.githubusercontent.com/JulianTorrest/FONDO_MUJER/main/04.%20Total%20de%20predios.csv',
    'Ingresos per cápita industria y comercio': 'https://raw.githubusercontent.com/JulianTorrest/FONDO_MUJER/main/05.%20Ingresos%20per%20c%C3%A1pita%20por%20impuesto%20a%20la%20Industria%20y%20al%20comercio.csv'
}

# Un selectbox para que el usuario elija el archivo
selected_file_name = st.selectbox('Selecciona un archivo para ver:', list(csv_files.keys()))

if selected_file_name:
    url = csv_files[selected_file_name]

    try:
        # Usamos requests para obtener el contenido del archivo
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la solicitud no fue exitosa

        # Usamos StringIO para leer el contenido del archivo de texto
        csv_data = StringIO(response.text)

        # Usamos pd.read_csv para leer el archivo CSV
        df = pd.read_csv(csv_data)

        # Rellenar los valores NaN con una cadena vacía para evitar errores de renderizado.
        df = df.fillna('')

        st.subheader(f'Datos del archivo: {selected_file_name}')

        # Muestra la tabla en la aplicación de Streamlit
        st.dataframe(df)

    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar el archivo desde GitHub: {e}")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
