"""
Panel unificado de Caravanas por la Justicia Social.

Vista única con un mapa que cambia según el modo seleccionado:
    - Octubre 2026  (calendario interactivo)
    - Histórico 24-26  (análisis de datos)
"""
import streamlit as st
import streamlit.components.v1 as components

from src.render import render_calendario, render_comparativa

st.set_page_config(
    page_title="Caravanas · Justicia Social",
    page_icon="🚐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ocultamos el menú de Streamlit, el toolbar (Deploy) y el footer.
# Dejamos visible el botón « del sidebar.
st.markdown(
    """
    <style>
      /* Oculta Deploy, menú, "Running…" */
      [data-testid="stToolbar"] {display: none !important;}
      [data-testid="stDecoration"] {display: none !important;}
      [data-testid="stStatusWidget"] {display: none !important;}
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}

      /* Header: transparente, pequeño y SIN capturar clics */
      header[data-testid="stHeader"] {
        background: transparent;
        height: 2.5rem;
        pointer-events: none;
      }
      /* Devolvemos clic solo al botón « del sidebar */
      [data-testid="stSidebarCollapsedControl"] {
        pointer-events: auto;
        top: 8px;
        left: 8px;
      }

      /* Contenido con un poco de aire arriba para no pegarse */
      .block-container {
        padding: 1.25rem 0 0 !important;
        max-width: 100% !important;
      }

      /* Toggle centrado y con aire */
      div[role="radiogroup"] {
        justify-content: center;
        gap: 22px;
        padding: 12px 0 6px;
      }
      div[role="radiogroup"] label {
        font-size: 16px;
        font-weight: 600;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Toggle de modo ----------------
modo = st.radio(
    "Vista",
    options=["📅 Octubre 2026", "📊 Histórico 24-26"],
    index=0,
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# ---------------- Render según modo ----------------
if modo == "📅 Octubre 2026":
    html = render_calendario()
    components.html(html, height=1600, scrolling=True)
else:
    html = render_comparativa()
    components.html(html, height=2400, scrolling=True)
