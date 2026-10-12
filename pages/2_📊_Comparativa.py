"""
Sección: Comparativa 2024–2026.
"""
import streamlit as st
import streamlit.components.v1 as components

from src.render import render_comparativa

st.set_page_config(
    page_title="Comparativa · Caravanas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      #MainMenu, footer {visibility: hidden;}
      .block-container {padding: 0 !important; max-width: 100% !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

html = render_comparativa()
components.html(html, height=2400, scrolling=True)
