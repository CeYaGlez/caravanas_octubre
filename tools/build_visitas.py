"""
Genera los CSVs limpios del conteo de visitas.

Entrada:
    data/raw/conteo_visitas.xlsx

Salida:
    data/visitas_por_municipio.csv   ← el entregable: cuántas veces por municipio
    data/caravanas_detalle.csv       ← las 373 caravanas crudas

Uso:
    python tools/build_visitas.py
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW  = ROOT / "data" / "raw" / "conteo_visitas.xlsx"
OUT_MUNI   = ROOT / "data" / "visitas_por_municipio.csv"
OUT_DETALLE = ROOT / "data" / "caravanas_detalle.csv"


def main():
    # ---------- 1. Conteo por municipio (el entregable) ----------
    df = pd.read_excel(RAW, sheet_name="Conteo por municipio")

    # Solo las 4 columnas que importan
    municipios = (
        df[["Municipio", "Visitas", "Trámites", "Personas"]]
        .copy()
        .sort_values(["Visitas", "Municipio"], ascending=[False, True])
        .reset_index(drop=True)
    )

    # Forzar tipos numéricos por si vienen como texto
    for col in ["Visitas", "Trámites", "Personas"]:
        municipios[col] = pd.to_numeric(municipios[col], errors="coerce").fillna(0).astype(int)

    municipios.to_csv(OUT_MUNI, index=False, encoding="utf-8-sig")

    # ---------- 2. Detalle de las 373 caravanas ----------
    detalle = pd.read_excel(RAW, sheet_name="Detalle caravanas")

    detalle = (
        detalle[["Nc.", "Municipio normalizado", "Trámites", "Personas", "Nota"]]
        .rename(columns={
            "Nc.": "nc",
            "Municipio normalizado": "municipio",
            "Trámites": "tramites",
            "Personas": "personas",
            "Nota": "nota",
        })
    )
    detalle["tramites"] = pd.to_numeric(detalle["tramites"], errors="coerce").fillna(0).astype(int)
    detalle["personas"] = pd.to_numeric(detalle["personas"], errors="coerce").fillna(0).astype(int)
    detalle["nota"] = detalle["nota"].fillna("")

    detalle.to_csv(OUT_DETALLE, index=False, encoding="utf-8-sig")

    # ---------- 3. Verificación ----------
    print(f"✓ {OUT_MUNI.relative_to(ROOT)}")
    print(f"    Municipios: {len(municipios)}")
    print(f"    Visitas:    {municipios['Visitas'].sum()}")
    print(f"    Trámites:   {municipios['Trámites'].sum():,}")
    print(f"    Personas:   {municipios['Personas'].sum():,}")
    print()
    print(f"✓ {OUT_DETALLE.relative_to(ROOT)}")
    print(f"    Caravanas:  {len(detalle)}")
    print(f"    Trámites:   {detalle['tramites'].sum():,}")
    print(f"    Personas:   {detalle['personas'].sum():,}")


if __name__ == "__main__":
    main()
