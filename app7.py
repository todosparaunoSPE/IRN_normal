# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:09:57 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Datos proporcionados con la columna "Posición"
data = {
    "SIEFORE": [
        "SB FINAL", "SB INICIAL", "SB 60-64", "SB 65-69", "SB 70-74", 
        "SB 75-79", "SB 80-84", "SB 85-89", "SB 90-94"
    ],
    "dic-19_IRN": [4.73, 4.4, 4.57, 4.56, 4.64, 4.71, 4.49, 4.41, 4.4],
    "dic-19_Posición": [1, 9, 4, 4, 4, 5, 9, 9, 9],
    "dic-20_IRN": [4.83, 5.08, 5.3, 5.29, 5.27, 5.33, 5.1, 5.07, 5.09],
    "dic-20_Posición": [3, 8, 5, 5, 6, 7, 9, 9, 8],
    "dic-21_IRN": [3.67, 4.8, 4.66, 4.69, 4.73, 4.92, 4.85, 4.91, 5.13],
    "dic-21_Posición": [2, 7, 5, 6, 6, 7, 7, 8, 7],
    "dic-22_IRN": [5.55, 5.5, 5.86, 5.84, 5.72, 5.74, 5.57, 5.6, 6.01],
    "dic-22_Posición": [3, 4, 3, 2, 4, 5, 5, 5, 3],
    "dic-23_IRN": [5.62, 5.66, 5.59, 5.77, 5.62, 5.48, 5.46, 5.5, 5.97],
    "dic-23_Posición": [1, 3, 3, 1, 3, 5, 3, 3, 4],
    "nov-24_IRN": [5.97, 5.74, 5.91, 6.12, 5.94, 5.71, 5.65, 5.66, 5.95],
    "nov-24_Posición": [4, 5, 1, 3, 3, 6, 6, 6, 6]
}

# Crear un DataFrame a partir de los datos
df = pd.DataFrame(data)

# Configurar la aplicación de Streamlit
st.title("Visualización de SIEFORE y IRN por año con posiciones")

# Sección de ayuda en la barra lateral
with st.sidebar:
    st.header("Ayuda")
    st.write("""
    Esta aplicación permite visualizar el rendimiento de diferentes SIEFORES en términos de su IRN (Índice de Rendimiento Neto) durante varios años, junto con sus posiciones relativas en el ranking.

    **Funcionalidades:**
    - **Gráfico de barras con posiciones:** Muestra el IRN de cada SIEFORE en los años seleccionados con las posiciones indicadas en el gráfico de barras.
    - **Gráfico de líneas con posiciones:** Muestra la evolución del IRN por SIEFORE a través de los años seleccionados.
    - **Resumen estadístico:** Muestra un resumen de los valores seleccionados de IRN para los años elegidos y también un resumen de las posiciones por SIEFORE.

    **Cómo usar la aplicación:**
    - Selecciona los años que deseas visualizar en el gráfico de barras.
    - Observa el gráfico de barras y las posiciones en función del IRN.
    - Visualiza la evolución del IRN por cada SIEFORE en el gráfico de líneas.
    - Consulta los resúmenes estadísticos para un análisis detallado de los resultados.

    Los datos muestran los rendimientos de las SIEFORES para varios años, y las posiciones indican cómo se comparan con otras SIEFORES en cada año.

    Esta herramienta puede ser útil para analizar el rendimiento histórico de las SIEFORES y tomar decisiones informadas sobre inversiones.
    """)

# Mostrar los datos en un DataFrame
st.dataframe(df)

# Gráfico de barras con posiciones
st.subheader("Gráfico de Barras con Posiciones")
selected_years = st.multiselect("Selecciona uno o más años para el gráfico de barras:", 
                                [year for year in df.columns if "_IRN" in year])

if selected_years:
    # Crear el gráfico de barras, incluyendo las posiciones en el color
    bar_fig = px.bar(
        df.melt(id_vars=["SIEFORE"], value_vars=selected_years, var_name="Año", value_name="IRN"),
        x="SIEFORE", y="IRN", color="Año", text="IRN",
        title=f"IRN de cada SIEFORE en los años seleccionados con posiciones",
        labels={"SIEFORE": "SIEFORE", "IRN": "IRN"},
        barmode="group",
        height=500
    )
    bar_fig.update_traces(textposition="outside")
    st.plotly_chart(bar_fig)

    # Agregar las posiciones al gráfico
    position_data = []
    for index, row in df.iterrows():
        for year in selected_years:
            position_data.append({
                "SIEFORE": row["SIEFORE"],
                "Año": year.split("_")[0],
                "Posición": row[year.replace("IRN", "Posición")],
                "IRN": row[year]
            })
    position_df = pd.DataFrame(position_data)

    # Mostrar un gráfico adicional para mostrar las posiciones
    position_fig = px.scatter(
        position_df, x="Año", y="Posición", color="SIEFORE",
        title="Posiciones de las SIEFORE por Año",
        labels={"Posición": "Posición", "Año": "Año", "SIEFORE": "SIEFORE"},
        height=500
    )
    st.plotly_chart(position_fig)

# Gráfico de líneas con posiciones
st.subheader("Gráfico de Líneas con Posiciones")
# Modificar para incluir solo los años de dic-19_IRN a nov-24_IRN
line_fig = px.line(
    df.melt(id_vars=["SIEFORE"], value_vars=["dic-19_IRN", "dic-20_IRN", "dic-21_IRN", "dic-22_IRN", "dic-23_IRN", "nov-24_IRN"], 
            var_name="Año", value_name="IRN"),
    x="Año", y="IRN", color="SIEFORE",
    title="Evolución del IRN por SIEFORE",  # Título modificado
    markers=True,
    labels={"Año": "Año", "IRN": "IRN"},
    height=600
)
st.plotly_chart(line_fig)

# Análisis de los resultados seleccionados con posiciones
st.subheader("Análisis de los Resultados Seleccionados con Posiciones")

if selected_years:
    # Filtrar los datos para las fechas seleccionadas
    df_selected = df[["SIEFORE"] + selected_years]

    # Mostrar resumen de los valores seleccionados
    summary = df_selected.describe()
    st.write("Resumen estadístico de los valores seleccionados:")
    st.dataframe(summary)

    # Mostrar también las posiciones
    position_summary = df[["SIEFORE"] + [year.replace("IRN", "Posición") for year in selected_years]]
    st.write("Resumen de posiciones por SIEFORE:")
    st.dataframe(position_summary)

    # Cálculo de la variación en las posiciones
    df_position_variation = df[["SIEFORE"] + [year.replace("IRN", "Posición") for year in selected_years]]
    df_position_variation["Variación en Posición"] = df_position_variation.apply(
        lambda row: row[selected_years[-1].replace("IRN", "Posición")] - row[selected_years[0].replace("IRN", "Posición")],
        axis=1
    )

    # Agregar sugerencias sobre por qué puede bajar de posición
    def generar_sugerencia(row):
        if row["Variación en Posición"] > 0:
            return "Posiblemente debido a un rendimiento inferior en los últimos años comparado con otras SIEFORES."
        elif row["Variación en Posición"] < 0:
            return "Posiblemente debido a un rendimiento superior en los últimos años comparado con otras SIEFORES."
        else:
            return "No ha habido un cambio significativo en el rendimiento."

    df_position_variation["Sugerencia"] = df_position_variation.apply(generar_sugerencia, axis=1)

    # Mostrar el DataFrame con las sugerencias al final
    st.write("Resumen de variación de posiciones y sugerencias:")
    st.dataframe(df_position_variation[["SIEFORE"] + [year.replace("IRN", "Posición") for year in selected_years] + ["Variación en Posición", "Sugerencia"]])