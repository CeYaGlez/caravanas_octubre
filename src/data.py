from __future__ import annotations
from dataclasses import dataclass, field
from functools import lru_cache
import pandas as pd
from src.paths import ASSETS
from src.municipios_const import normalizar

@dataclass(frozen=True)
class Visita:
    anio: int
    numero: int
    sede: str
    personas: int | None

@dataclass
class Municipio:
    nombre: str
    visitas: list[Visita] = field(default_factory=list)
    tramites: dict[int, int] = field(default_factory=dict)

@lru_cache(maxsize=1)
def load_municipios() -> dict[str, Municipio]:
    # Leemos el detalle de las 373 visitas (el CSV que genera build_visitas.py)
    csv_path = ASSETS.parent / "data" / "caravanas_detalle.csv"
    
    if not csv_path.exists():
        return {}
        
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    out: dict[str, Municipio] = {}
    
    # Como no hay fecha real, inferimos el año por rangos (aprox)
    # 1-97 (2024), 98-245 (2025), 246-373 (2026)
    def inferir_anio(nc):
        if nc <= 97: return 2024
        if nc <= 245: return 2025
        return 2026

    for _, row in df.iterrows():
        nombre = row["municipio_normalizado"]
        if nombre not in out:
            out[nombre] = Municipio(nombre=nombre)
            
        m = out[nombre]
        anio = inferir_anio(row["nc"])
        m.visitas.append(Visita(anio=anio, numero=1, sede="E", personas=row["personas"]))
        
        # Acumular trámites por año
        m.tramites[anio] = m.tramites.get(anio, 0) + row["tramites"]
        
    return out
