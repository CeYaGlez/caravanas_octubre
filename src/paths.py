"""
Rutas centralizadas del proyecto.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA      = ROOT / "data"
ASSETS    = ROOT / "assets"
TEMPLATES = ASSETS / "templates"

# ---- datos ----
EXCEL_CSV              = DATA / "TABLA_SEDE_CARAVANAS.csv"
MUNICIPIOS_CSV         = DATA / "municipios.csv"
CALENDARIO_OCTUBRE_CSV = DATA / "calendario_oct_2026.csv"
GEO_V3_JSON            = DATA / "geo_v3.json"
MUNICIPIOS_V3_JSON     = DATA / "municipios_v3.json"

# ---- assets ----
MAPA_PATHS_JS       = ASSETS / "mapa_paths.js"
MAPA_COMPARATIVA_JS = ASSETS / "mapa_comparativa.js"

# ---- plantillas ----
CALENDARIO_HTML  = TEMPLATES / "calendario.html"
COMPARATIVA_HTML = TEMPLATES / "comparativa.html"
