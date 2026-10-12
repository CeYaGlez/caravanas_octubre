"""
Cálculos de la comparativa. Nada de presentación aquí.

Todas las funciones toman objetos de src.data (Municipio, Visita) y
devuelven números o dicts puros. El HTML decide cómo mostrarlos.
"""
from __future__ import annotations

from statistics import median

from src.data import Municipio, Visita

ANIOS = (2024, 2025, 2026)


# ---------------------------------------------------------------- helpers

def filtrar(visitas: list[Visita], anio: int | None = None,
            sede: str | None = None) -> list[Visita]:
    """Filtra visitas por año y/o sede ('E' o 'F')."""
    return [
        v for v in visitas
        if (anio is None or v.anio == anio)
        and (sede is None or v.sede == sede)
    ]


def promedio_personas(visitas: list[Visita]) -> float:
    """Promedio de personas por visita (ignora visitas sin dato)."""
    vals = [v.personas for v in visitas if v.personas is not None]
    return sum(vals) / len(vals) if vals else 0.0


def mediana_personas(visitas: list[Visita]) -> float:
    vals = [v.personas for v in visitas if v.personas is not None]
    return median(vals) if vals else 0.0


def total_personas(visitas: list[Visita]) -> int:
    return sum(v.personas or 0 for v in visitas)


def cobertura_por_mil(personas: int, poblacion: int | None) -> float:
    """Personas atendidas por cada 1,000 habitantes."""
    return personas / poblacion * 1000 if poblacion else 0.0


# ---------------------------------------------------------------- agregados

def resumen_por_anio(municipios: list[Municipio],
                     anios: tuple[int, ...] = ANIOS) -> list[dict]:
    """Promedio de personas por visita, separando explanada y fuera."""
    out = []
    for anio in anios:
        e = [v for m in municipios
             for v in m.visitas if v.anio == anio and v.sede == "E"]
        f = [v for m in municipios
             for v in m.visitas if v.anio == anio and v.sede == "F"]
        out.append({
            "anio": anio,
            "personas_por_visita_explanada": promedio_personas(e),
            "personas_por_visita_fuera":     promedio_personas(f),
            "visitas_explanada": len(e),
            "visitas_fuera":     len(f),
        })
    return out


def cambios_de_sede(municipios: list[Municipio]) -> list[dict]:
    """
    Detecta cuando un municipio cambió entre E y F entre años consecutivos.
    Devuelve un dict por cada cambio detectado.
    """
    out = []
    for m in municipios:
        por_anio: dict[int, list[Visita]] = {}
        for v in m.visitas:
            if v.sede in ("E", "F"):
                por_anio.setdefault(v.anio, []).append(v)

        anios_ord = sorted(por_anio)
        for a, b in zip(anios_ord, anios_ord[1:]):
            s1 = por_anio[a][0].sede
            s2 = por_anio[b][0].sede
            if s1 == s2:
                continue

            p1 = promedio_personas(por_anio[a])
            p2 = promedio_personas(por_anio[b])
            out.append({
                "municipio": m.nombre,
                "de": s1,
                "a": s2,
                "anio_de": a,
                "anio_a": b,
                "personas_antes": p1,
                "personas_despues": p2,
                "delta_pct": (p2 - p1) / p1 * 100 if p1 else None,
            })
    return out


# ---------------------------------------------------------------- serialización

def a_diccionario_template(m: Municipio) -> dict:
    """
    Convierte un Municipio al shape que espera la plantilla comparativa.html:

        {
          "n":  nombre corto (etiqueta),
          "g":  nombre geográfico (para lookup en el mapa SVG),
          "v":  [[anio, numero, sede, personas], ...],
          "pr": [años con sede asignada sin visita registrada],
          "tr": {"2024": int, "2025": int, "2026": int}
        }
    """
    return {
        "n":  m.nombre,
        "g":  m.nombre,
        "v":  [[v.anio, v.numero, v.sede, v.personas] for v in m.visitas],
        "pr": [],  # por ahora no lo inferimos desde el CSV
        "tr": {str(a): t for a, t in m.tramites.items()},
    }
