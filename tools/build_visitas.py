import sys
from pathlib import Path
import pandas as pd
import re

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.municipios_const import normalizar

RAW         = ROOT / "data" / "raw" / "informe_acumulado.csv"
OUT_MUNI    = ROOT / "data" / "visitas_por_municipio.csv"
OUT_DETALLE = ROOT / "data" / "caravanas_detalle.csv"

def main():
    # Leemos sin saltarnos filas fijas para que sea inmune a cambios de formato
    df = pd.read_csv(RAW, encoding="utf-8-sig", header=None)
    
    # Buscamos la fila donde empiezan los datos (la que dice "1" o "1." en la columna 1)
    start_idx = 0
    for i, val in enumerate(df[1]):
        if str(val).strip() in ("1", "1."):
            start_idx = i
            break

    # Extraemos solo las columnas que nos importan
    df = df.iloc[start_idx:, [1, 2, 3, 4]].copy()
    df.columns = ["nc", "municipio_original", "tramites", "personas"]

    # Limpiamos el número de caravana (le quitamos el punto si lo tiene)
    df["nc"] = df["nc"].astype(str).str.replace(".", "", regex=False).str.strip()
    
    # Filtramos solo las filas donde nc sea un número puro (1 a 373)
    df = df[df["nc"].str.match(r"^\d+$", na=False)].copy()

    df["municipio_original"] = df["municipio_original"].astype(str).str.strip()
    df["municipio"] = df["municipio_original"].apply(normalizar)

    df["tramites"] = pd.to_numeric(df["tramites"].astype(str).str.replace(",", "").str.strip(), errors="coerce").fillna(0).astype(int)
    df["personas"] = pd.to_numeric(df["personas"], errors="coerce").fillna(0).astype(int)

    # Detalle
    detalle = df[["nc", "municipio_original", "municipio", "tramites", "personas"]].rename(
        columns={"municipio_original": "municipio_en_excel", "municipio": "municipio_normalizado"}
    )
    detalle.to_csv(OUT_DETALLE, index=False, encoding="utf-8-sig")

    # Conteo
    municipios = (
        df.groupby("municipio")
        .agg(Visitas=("municipio", "size"), Trámites=("tramites", "sum"), Personas=("personas", "sum"))
        .reset_index()
        .rename(columns={"municipio": "Municipio"})
        .sort_values(["Visitas", "Municipio"], ascending=[False, True])
        .reset_index(drop=True)
    )
    municipios.to_csv(OUT_MUNI, index=False, encoding="utf-8-sig")

    print(f"✓ {OUT_MUNI.relative_to(ROOT)}")
    print(f"    Filas:     {len(municipios)}   (esperado 125)")
    print(f"    Visitas:   {municipios['Visitas'].sum()}")
    print(f"    Trámites:  {municipios['Trámites'].sum():,}")
    print(f"    Personas:  {municipios['Personas'].sum():,}")

if __name__ == "__main__":
    main()
