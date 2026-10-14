"""
Constantes de limpieza de municipios, compartidas.

El Excel institucional trae nombres "fantasma" que no son municipios
reales o que están duplicados. Centralizamos aquí las reglas para que
src/data.py (panel Streamlit) y tools/build_visitas.py (CSV entregables)
cuenten exactamente lo mismo.

Reglas:
  - FUSIONES: el nombre de la izquierda se colapsa en el de la derecha.
              Sus visitas/trámites/personas se SUMAN.
  - RENOMBRES: solo cambia la etiqueta, no se fusiona con nada.
"""

# nombre en origen → nombre canónico  (los datos se SUMAN)
FUSIONES = {
    "Amanalco": "Amanalco de Becerra",
    "Jajalpa Tenango": "Tenango del Valle",
}

# nombre en origen → etiqueta más clara  (NO se fusiona con nada)
RENOMBRES = {
    "Almoloya (sin especificar: ¿Juárez, Río o Alquisiras?)": "Almoloya (por confirmar)",
}


def normalizar(nombre: str) -> str:
    """Aplica renombres y luego fusiones en una sola pasada."""
    nombre = RENOMBRES.get(nombre, nombre)
    nombre = FUSIONES.get(nombre, nombre)
    return nombre
