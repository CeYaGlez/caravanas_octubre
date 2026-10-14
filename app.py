"""
Caravanas Itinerantes por la Justicia Social.

Punto de entrada: redirige automáticamente al panel unificado.
"""
import streamlit as st

st.set_page_config(
    page_title="Caravanas · Justicia Social",
    page_icon="🚐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Redirección al panel principal (pages/1_🚐_Caravanas.py)
st.switch_page("pages/1_🚐_Caravanas.py")
