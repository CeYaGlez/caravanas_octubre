"""
Sección: Calendario de octubre 2026.
"""
import streamlit as st
import streamlit.components.v1 as components

from src.render import render_calendario

st.set_page_config(
    page_title="Calendario · Caravanas",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",   # ← mantiene el sidebar abierto al navegar
)

# Solo ocultamos el MENÚ de Streamlit y el footer.
# Dejamos el header para que el botón « del sidebar siempre esté visible.
st.markdown(
    """
    <style>
      #MainMenu, footer {visibility: hidden;}
      .block-container {padding: 0 !important; max-width: 100% !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

html = render_calendario()
components.html(html, height=1600, scrolling=True)
