from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Caravanas Itinerantes · Octubre 2026",
    page_icon="🗺️",
    layout="wide",
)

# Quita el menú/encabezado de Streamlit y los márgenes para que se vea como página oficial
st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden;}
      .block-container {padding: 0 !important; max-width: 100% !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

html = Path(__file__).with_name("caravanas-octubre.html").read_text(encoding="utf-8")
components.html(html, height=1500, scrolling=True)
