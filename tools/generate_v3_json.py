import json
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_DETALLE = ROOT / "data" / "caravanas_detalle.csv"
JSON_OUT = ROOT / "data" / "municipios_v3.json" # Archivo que lee la vista histórica

def main():
    df = pd.read_csv(CSV_DETALLE, encoding="utf-8-sig")
    muns = {}
    
    for _, row in df.iterrows():
        nombre = row["municipio_normalizado"]
        if nombre not in muns:
            muns[nombre] = {"n": nombre, "v": [], "tr": {"2024": 0, "2025": 0, "2026": 0}, "pr": [], "g": nombre}
            
        # Inferir año (1-97: 2024, 98-245: 2025, 246-373: 2026)
        nc = int(row["nc"])
        anio = 2024 if nc <= 97 else (2025 if nc <= 245 else 2026)
        
        # En el CSV original no tenemos la sede, así que ponemos 'E' (explanada) por defecto
        # para que las gráficas de eficiencia no fallen.
        muns[nombre]["v"].append([anio, 1, "E", int(row["personas"])])
        muns[nombre]["tr"][str(anio)] += int(row["tramites"])
        
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(list(muns.values()), f, ensure_ascii=False, indent=2)
        
    print(f"✓ Regenerado {JSON_OUT.name} con {len(muns)} municipios.")

if __name__ == "__main__":
    main()
