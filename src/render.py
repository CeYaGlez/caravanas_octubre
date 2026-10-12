"""
Renderiza las plantillas HTML inyectando los datos reales.

Cada plantilla tiene placeholders /*DATA:xxx*/. Este módulo los
sustituye por JSON (o código JS crudo, cuando aplica).
"""
from __future__ import annotations

import json
from functools import lru_cache

import pandas as pd

from src.paths import (
    ASSETS,
    CALENDARIO_HTML,
    CALENDARIO_OCTUBRE_CSV,
    MAPA_PATHS_JS,
)


@lru_cache(maxsize=None)
def _read(path) -> str:
    return path.read_text(encoding="utf-8")


def _inyectar(html: str, placeholder: str, contenido: str) -> str:
    marca = f"/*DATA:{placeholder}*/"
    if marca not in html:
        raise ValueError(f"Falta el placeholder {marca} en la plantilla")
    return html.replace(marca, contenido)


def _eventos_js() -> str:
    """Convierte data/calendario_oct_2026.csv a un array JS literal."""
    df = pd.read_csv(CALENDARIO_OCTUBRE_CSV)
    items = []
    for _, r in df.iterrows():
        dias = list(range(int(r["dia_inicio"]), int(r["dia_fin"]) + 1))
        item = [int(r["caravana"]), r["municipio"], r["map_key"], dias]
        if int(r["destacado"]):
            item.append(1)
        items.append(item)
    return ",\n".join(json.dumps(i, ensure_ascii=False) for i in items)


def render_calendario() -> str:
    """Devuelve el HTML completo del calendario."""
    html = _read(CALENDARIO_HTML)

    # 1) Paths del mapa: se inyectan como código JS crudo
    mapa_js = _read(MAPA_PATHS_JS)
    html = _inyectar(html, "mapa_paths", mapa_js)

    # 2) Eventos: array JS construido desde el CSV
    html = _inyectar(html, "eventos", _eventos_js())

    return html


def render_comparativa() -> str:
    """Devuelve el HTML completo de la comparativa (ex-v3)."""
    from src.paths import (
        COMPARATIVA_HTML,
        GEO_V3_JSON,
        MAPA_COMPARATIVA_JS,
        MUNICIPIOS_V3_JSON,
    )

    html = _read(COMPARATIVA_HTML)

    # Los tres bloques ya vienen extraídos del HTML original:
    #   - GEO → data/geo_v3.json
    #   - M   → data/municipios_v3.json
    #   - P   → assets/mapa_comparativa.js
    # Se inyectan como JS crudo.
    html = _inyectar(html, "geo", _read(GEO_V3_JSON))
    html = _inyectar(html, "municipios", _read(MUNICIPIOS_V3_JSON))
    html = _inyectar(html, "map_paths", _read(MAPA_COMPARATIVA_JS))

    return html
