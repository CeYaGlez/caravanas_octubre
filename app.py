"""
Caravanas Itinerantes por la Justicia Social.

Portada del proyecto.
"""
import streamlit as st

st.set_page_config(
    page_title="Caravanas por la Justicia Social",
    page_icon="🚐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Solo ocultamos el menú de Streamlit y el footer (dejamos el header
# para que el botón del sidebar siempre esté visible).
st.markdown(
    """
    <style>
      #MainMenu, footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🚐 Caravanas Itinerantes por la Justicia Social")
st.markdown("Bienvenido al tablero del programa. Usa los accesos directos o el menú lateral.")

st.subheader("Secciones")

st.page_link(
    "pages/1_📅_Calendario.py",
    label="Calendario",
    icon="📅",
    help="Programación de octubre 2026",
)
st.caption(
    "Mapa interactivo, filtros por caravana / municipio / fecha y descarga en PDF."
)

st.page_link(
    "pages/2_📊_Comparativa.py",
    label="Comparativa",
    icon="📊",
    help="Histórico 2024–2026: visitas, personas, trámites y cambios de sede",
)
st.caption(
    "Histórico 2024–2026: visitas, personas atendidas, trámites y cambios de sede."
)

st.divider()
st.caption(
    "**Fuente de datos**: `data/TABLA_SEDE_CARAVANAS.csv` "
    "(exportado del Excel institucional)."
)
