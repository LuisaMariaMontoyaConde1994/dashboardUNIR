import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊Laboratorio: Visualización Interactiva de la Información")
st.write("Especialización en Big Data y Visual Analytics")
st.markdown("### UNIR")

# 1. Introducción
with st.expander("📄 Introducción", expanded=True):
    st.markdown("""
    Esta aplicación demuestra el uso de diferentes bibliotecas de visualización en Python:

    * **Matplotlib**: Biblioteca base para visualización.
    * **Seaborn**: Visualizaciones estadísticas de alto nivel.
    * **Plotly**: Gráficos interactivos.
    * **Streamlit**: Framework para aplicaciones de datos.

    Bases utilizadas:
    * [`causeofdeath.csv`](https://yusef.es/dataset/causeofdeath.csv)
    * `annual-number-of-deaths-by-cause.csv` (fuente: [Our World in Data](https://ourworldindata.org))
    """)

# 2. Carga de datos
try:
    df1 = pd.read_csv('data/causeofdeath.csv', sep=';')
    df2 = pd.read_csv('data/annual-number-of-deaths-by-cause.csv')
    st.success("✅ Datos cargados exitosamente")

    # Procesar df1
    tabla = df1.pivot_table(index='Cause of death or injury',
                              columns='Measure',
                              values='Value',
                              aggfunc='first').reset_index()
    tabla.columns = ['Causa', 'Cambio_2010_2017', 'Porcentaje_2017']

    # Convertir a numérico las columnas relevantes
    tabla['Cambio_2010_2017'] = tabla['Cambio_2010_2017'].astype(str).str.replace(',', '.')
    tabla['Cambio_2010_2017'] = pd.to_numeric(tabla['Cambio_2010_2017'], errors='coerce')

    tabla['Porcentaje_2017'] = tabla['Porcentaje_2017'].astype(str).str.replace(',', '.')
    tabla['Porcentaje_2017'] = pd.to_numeric(tabla['Porcentaje_2017'], errors='coerce')

except Exception as e:
    st.error(f"❌ Error al cargar los datos: {e}")

# 3. Vista previa de los datos
with st.expander("👁️ Vista previa de las bases de datos", expanded=False):
    st.subheader("📌 Datos procesados de causeofdeath.csv")
    try:
        st.dataframe(tabla)
    except:
        st.write("❌ No se pudieron mostrar los datos procesados.")
    st.subheader("📌 Datos: annual-number-of-deaths-by-cause.csv")
    st.dataframe(df2.head())

# 4. Gráfico de barras con Plotly
st.header("🌟 Visualización Interactiva con Plotly")

if not tabla.empty:
    top10 = tabla.sort_values(by='Porcentaje_2017', ascending=False).head(10)

    fig_plotly = px.bar(
        top10,
        x='Porcentaje_2017',
        y='Causa',
        orientation='h',
        title='🔝 Top 10 causas de muerte en 2017',
        color='Porcentaje_2017',
        color_continuous_scale='Blues',
        text='Porcentaje_2017'
    )

    fig_plotly.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig_plotly.update_layout(
        xaxis_title='Porcentaje de muertes (%)',
        yaxis_title='Causa',
        title_font=dict(size=20),
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig_plotly, use_container_width=True)
else:
    st.error("❌ La tabla está vacía, no se puede graficar.")

# 5. Gráfico de dispersión con Plotly
st.header("📉 Tendencia de las causas principales de muerte (2010–2017)")

if not tabla.empty:
    fig_scatter = px.scatter(
        top10,
        x='Porcentaje_2017',
        y='Cambio_2010_2017',
        color='Causa',
        size='Porcentaje_2017',
        text='Causa',
        title='📈 ¿Están aumentando o disminuyendo las principales causas?',
        labels={
            'Porcentaje_2017': 'Porcentaje de muertes (2017)',
            'Cambio_2010_2017': 'Cambio porcentual 2010–2017'
        },
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig_scatter.add_hline(y=0, line_dash="dash", line_color="gray")

    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(
        title_font=dict(size=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        plot_bgcolor='white',
        height=600
    )

    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.error("❌ No se puede mostrar el gráfico de dispersión porque la tabla está vacía.")
# ---------------------------------------------------
# 🟣 Gráfico 3: Muertes globales por causa (2017)
# ---------------------------------------------------

st.header("🌍 Muertes globales por causa (2017)")

# Filtrar año 2017
muertes_2017 = df2[df2['Year'] == 2017]

# Columnas de interés
columnas_interes = [
    'Entity',
    'Deaths - Malaria - Sex: Both - Age: All Ages (Number)',
    'Deaths - Diarrheal diseases - Sex: Both - Age: All Ages (Number)',
    'Deaths - Tuberculosis - Sex: Both - Age: All Ages (Number)',
    'Deaths - HIV/AIDS - Sex: Both - Age: All Ages (Number)'
]

# Seleccionar y sumar globalmente (sin Entity)
muertes_seleccionadas = muertes_2017[columnas_interes]
totales = muertes_seleccionadas.drop('Entity', axis=1).sum().sort_values(ascending=False).reset_index()
totales.columns = ['Causa', 'Muertes']

# Limpiar nombres
totales['Causa'] = totales['Causa'].str.replace('Deaths - ', '', regex=False).str.replace(' - Sex: Both - Age: All Ages (Number)', '', regex=False)

# Gráfico interactivo con Plotly
fig_muertes = px.bar(
    totales,
    x='Causa',
    y='Muertes',
    text='Muertes',
    title='🌍 Muertes globales por causa (2017)',
    labels={'Muertes': 'Número de muertes', 'Causa': 'Causa'},
    color='Muertes',
    color_continuous_scale='oranges'
)

fig_muertes.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_muertes.update_layout(
    xaxis=dict(tickangle=45),
    title_font=dict(size=20),
    plot_bgcolor='white',
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig_muertes, use_container_width=True)
# ---------------------------------------------------
# 🔴 Gráfico 4: Cambios porcentuales más relevantes
# ---------------------------------------------------

st.header("📈 Causas con mayores aumentos y disminuciones (2010–2017)")

# Eliminar valores vacíos
tabla_limpia = tabla.dropna(subset=['Cambio_2010_2017'])

# Ordenar por cambio
tabla_ordenada = tabla_limpia.sort_values(by='Cambio_2010_2017')

# Seleccionar 10 que más disminuyeron y 10 que más aumentaron
cambios_top = pd.concat([tabla_ordenada.head(10), tabla_ordenada.tail(10)])

# Crear columna de color: azul para disminución, rojo para aumento
cambios_top['Color'] = cambios_top['Cambio_2010_2017'].apply(lambda x: 'Disminuyó' if x < 0 else 'Aumentó')

# Gráfico con Plotly
fig_cambios = px.bar(
    cambios_top,
    x='Cambio_2010_2017',
    y='Causa',
    orientation='h',
    color='Color',
    color_discrete_map={'Disminuyó': '#1f77b4', 'Aumentó': '#d62728'},
    title='📉 Causas con Cambios Porcentuales Más Relevantes (2010–2017)',
    labels={'Cambio_2010_2017': 'Cambio porcentual', 'Causa': 'Causa'}
)

# Línea vertical en x=0
fig_cambios.add_vline(x=0, line_dash="dash", line_color="gray")

fig_cambios.update_layout(
    title_font=dict(size=20),
    plot_bgcolor='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    height=700
)

st.plotly_chart(fig_cambios, use_container_width=True)

# ---------------------------------------------------
# 🌍 Mapa interactivo con selectbox
# ---------------------------------------------------

st.header("🗺️ Mapa mundial de muertes por causa (2017)")

# Lista de columnas disponibles (puedes agregar más)
causas_disponibles = {
    'Malaria': 'Deaths - Malaria - Sex: Both - Age: All Ages (Number)',
    'VIH/SIDA': 'Deaths - HIV/AIDS - Sex: Both - Age: All Ages (Number)',
    'Tuberculosis': 'Deaths - Tuberculosis - Sex: Both - Age: All Ages (Number)',
    'Diarrea': 'Deaths - Diarrheal diseases - Sex: Both - Age: All Ages (Number)',
    'Enfermedad cardíaca isquémica': 'Deaths - Ischemic heart disease - Sex: Both - Age: All Ages (Number)',
    'Derrame cerebral (Stroke)': 'Deaths - Stroke - Sex: Both - Age: All Ages (Number)'
}

# Selección de causa
causa_nombre = st.selectbox("Selecciona una causa", list(causas_disponibles.keys()))
columna_causa = causas_disponibles[causa_nombre]

# Filtrar año 2017
muertes_2017 = df2[df2['Year'] == 2017]

# Crear mapa
fig_mapa = px.choropleth(
    muertes_2017,
    locations='Entity',
    locationmode='country names',
    color=columna_causa,
    hover_name='Entity',
    title=f"🌍 Muertes por {causa_nombre} en el Mundo (2017)",
    color_continuous_scale='OrRd',
    labels={columna_causa: 'Número de muertes'}
)

fig_mapa.update_layout(
    title_font=dict(size=20),
    geo=dict(showframe=False, showcoastlines=False),
    plot_bgcolor='white'
)

st.plotly_chart(fig_mapa, use_container_width=True)
# Selección de causa
columna_causa = 'Deaths - HIV/AIDS - Sex: Both - Age: All Ages (Number)'

# Filtrar por causa y sumar globalmente por año
muertes_anuales = df2.groupby('Year')[columna_causa].sum().reset_index()

# Gráfico de línea
fig_linea = px.line(muertes_anuales,
                    x='Year',
                    y=columna_causa,
                    title='Evolución anual de muertes por VIH/SIDA (1990–2017)',
                    labels={columna_causa: 'Número de muertes'},
                    markers=True)
st.plotly_chart(fig_linea)
# Filtrar 2017
muertes_2017 = df2[df2['Year'] == 2017]
columna = 'Deaths - Tuberculosis - Sex: Both - Age: All Ages (Number)'

# Top 10 países
top10_paises = muertes_2017[['Entity', columna]].sort_values(by=columna, ascending=False).head(10)

fig_barras = px.bar(top10_paises,
                    x=columna,
                    y='Entity',
                    orientation='h',
                    title='Top 10 países con más muertes por Tuberculosis (2017)',
                    labels={columna: 'Número de muertes', 'Entity': 'País'})
st.plotly_chart(fig_barras)
# Causas seleccionadas
causas = [
    'Deaths - HIV/AIDS - Sex: Both - Age: All Ages (Number)',
    'Deaths - Malaria - Sex: Both - Age: All Ages (Number)',
    'Deaths - Tuberculosis - Sex: Both - Age: All Ages (Number)'
]

# Sumatoria por año
df_area = df2.groupby('Year')[causas].sum().reset_index()

# Gráfico apilado
fig_area = px.area(df_area,
                   x='Year',
                   y=causas,
                   title='Evolución de muertes por distintas causas (1990–2017)',
                   labels={'value': 'Muertes', 'variable': 'Causa'})
st.plotly_chart(fig_area)
fig.write_html("dashboard.html")





