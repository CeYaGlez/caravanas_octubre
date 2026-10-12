"""
Carga y normalización de los datos de caravanas.

Esta es la ÚNICA fuente de datos del proyecto. Todos los módulos
(calendario, comparativa, métricas) leen de aquí.

Fuente: data/TABLA_SEDE_CARAVANAS.csv (exportado del Excel institucional).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

import pandas as pd

from src.paths import EXCEL_CSV, MUNICIPIOS_CSV


# ---------------------------------------------------------------- modelos

@dataclass(frozen=True)
class Visita:
    """Una visita a un municipio en un año."""
    anio: int
    numero: int          # 1 = primera del año, 2 = segunda
    sede: str            # "E" explanada | "F" fuera | "?" sin dato
    personas: int | None


@dataclass
class Municipio:
    """Un municipio con todas sus visitas y trámites."""
    nombre: str
    cve: int | None = None
    poblacion: int | None = None
    region: str | None = None
    visitas: list[Visita] = field(default_factory=list)
    tramites: dict[int, int] = field(default_factory=dict)


# ---------------------------------------------------------------- helpers

# Palabras clave que definen "explanada". Todo lo demás es "fuera".
_SEDE_EXPLANADA = (
    "explanada",
    "jardín central",
    "jardin central",
    "kiosco",
)


def _classify_sede(texto: str | None) -> str | None:
    """Clasifica la sede: 'E' si es explanada, 'F' si es otra, None si vacía."""
    if not texto or not str(texto).strip():
        return None
    t = str(texto).lower()
    return "E" if any(k in t for k in _SEDE_EXPLANADA) else "F"


def _to_int(valor) -> int | None:
    """Convierte '1,133' o '650' o '' a int o None."""
    if valor is None:
        return None
    s = str(valor).replace(",", "").strip()
    if not s or s in ("-", "#", "nan", "NaN"):
        return None
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return None


def _clean_nombre(texto: str) -> str:
    """Quita puntos finales y espacios sobrantes del nombre."""
    return str(texto).strip().rstrip(".").strip()


# ---------------------------------------------------------------- carga

@lru_cache(maxsize=1)
def load_municipios() -> dict[str, Municipio]:
    """
    Lee el CSV del Excel y devuelve {nombre: Municipio}.
    Luego cruza con municipios.csv para agregar cve, población y región.
    """
    df = pd.read_csv(
        EXCEL_CSV,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8-sig",
    )
    df.columns = [c.strip() for c in df.columns]

    out: dict[str, Municipio] = {}

    for _, row in df.iterrows():
        nombre = _clean_nombre(row.get("Municipio", ""))
        if not nombre or nombre == "#":
            continue

        m = out.setdefault(nombre, Municipio(nombre=nombre))

        for anio in (2024, 2025, 2026):
            sede_raw = row.get(f"Sede {anio}", "")
            p1 = _to_int(row.get(f"Personas {anio} (primera)", ""))
            p2 = _to_int(row.get(f"Personas {anio} (segunda)", ""))
            tr = _to_int(row.get(f"Trámites {anio}", ""))

            if tr is not None:
                m.tramites[anio] = tr

            sede = _classify_sede(sede_raw)

            # Solo agregamos visita si hay indicio real de ella
            hay_visita = p1 is not None or p2 is not None or sede is not None
            if not hay_visita:
                continue

            m.visitas.append(
                Visita(anio=anio, numero=1, sede=sede or "?", personas=p1)
            )
            if p2 is not None:
                m.visitas.append(
                    Visita(anio=anio, numero=2, sede=sede or "?", personas=p2)
                )

    # Cruce con el catálogo municipios.csv
    try:
        meta = pd.read_csv(MUNICIPIOS_CSV, encoding="utf-8-sig")
        idx = {
            _clean_nombre(r["nombre"]).lower(): r
            for _, r in meta.iterrows()
        }
        for nombre, m in out.items():
            r = idx.get(nombre.lower())
            if r is not None:
                m.cve = _to_int(r.get("cve"))
                m.poblacion = _to_int(r.get("poblacion"))
                m.region = r.get("region")
    except FileNotFoundError:
        pass  # el catálogo es opcional; sin él solo perdemos pob/región

    return out
