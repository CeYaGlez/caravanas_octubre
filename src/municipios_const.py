"""
Constantes de limpieza de municipios.
Tres capas: ALIAS (corrige tildes/puntos), RENOMBRES (etiquetas) y FUSIONES (suma datos).
"""

# ---------- 1. ALIAS ----------
# Grafías alternativas (tildes, puntos, nombres cortos) → nombre canónico oficial
ALIAS = {
    # Faltas de ortografía o tildes
    "Almoloya de Juarez":          "Almoloya de Juárez",
    "Almoloya del Rio":            "Almoloya del Río",
    "Chimalhuacan":                "Chimalhuacán",
    "Nicolas Romero":              "Nicolás Romero",
    "Nezahualcoyotl":              "Nezahualcóyotl",
    "Polotitlan":                  "Polotitlán",
    "Rayon":                       "Rayón",
    "San Jose del Rincon":         "San José del Rincón",
    "San Jose del Rincón":         "San José del Rincón",
    "San Martin de las Piramides": "San Martín de las Pirámides",
    "San Martín de las Piramides": "San Martín de las Pirámides",
    "sultepec":                    "Sultepec",
    "Teotihuacan":                 "Teotihuacán",
    "Tepotzotlan":                 "Tepotzotlán",
    "Texcaltitlan":                "Texcaltitlán",
    "Villa guerrero":              "Villa Guerrero",
    "Xonacatlan":                  "Xonacatlán",
    "Atizapan de Zaragoza":        "Atizapán de Zaragoza",

    # Puntos finales (errores de captura)
    "Cuautitlán Izcalli.":         "Cuautitlán Izcalli",
    "Jocotitlán.":                 "Jocotitlán",
    "Papalotla.":                  "Papalotla",
    "San Antonio la Isla.":        "San Antonio la Isla",
    "Tultepec.":                   "Tultepec",

    # Nombres cortos que en el informe salen extendidos
    "Tianguistenco":               "Santiago Tianguistenco",
}

# ---------- 2. RENOMBRES ----------
# Solo cambia la etiqueta, no se fusiona con nada.
RENOMBRES = {
    "Almoloya (sin especificar: ¿Juárez, Río o Alquisiras?)": "Almoloya (por confirmar)",
}

# ---------- 3. FUSIONES ----------
# Aquí SÍ se suman los datos. Izquierda (origen) → Derecha (destino final)
FUSIONES = {
    "Amanalco":         "Amanalco de Becerra",
    "Jajalpa Tenango":  "Tenango del Valle",
    "Huhuetoca":        "Huehuetoca",
    "Santo Tomas":      "Santo Tomás de los Plátanos",
    "Santo Tomas ":     "Santo Tomás de los Plátanos",  # Ojo: con espacio al final
}


def normalizar(nombre: str) -> str:
    """Aplica alias, renombres y fusiones en una sola pasada."""
    nombre = ALIAS.get(nombre, nombre)
    nombre = RENOMBRES.get(nombre, nombre)
    nombre = FUSIONES.get(nombre, nombre)
    return nombre
