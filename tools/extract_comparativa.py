"""
Extrae GEO, M y P del comparativa.html usando marcadores literales.
Sin regex, sin parser de brackets. Simple y confiable.

Marcadores identificados en el v3:
    const GEO =  ...  →  function norm(...)   [GEO termina donde empieza norm]
    const M=[    ...  →  const P=             [M termina donde empieza P]
    const P={    ...  →  const Y=             [P termina donde empieza Y]
"""
from pathlib import Path


ROOT      = Path(__file__).resolve().parent.parent
TEMPLATE  = ROOT / "assets" / "templates" / "comparativa.html"
BACKUP    = TEMPLATE.with_suffix(".html.bak")
GEO_JSON  = ROOT / "data" / "geo_v3.json"
M_JSON    = ROOT / "data" / "municipios_v3.json"
PATHS_JS  = ROOT / "assets" / "mapa_comparativa.js"


def bloque(text: str, desde: str, hasta: str) -> str:
    """Devuelve el texto entre 'desde' (inclusive) y 'hasta' (exclusive)."""
    i = text.index(desde)
    j = text.index(hasta, i + len(desde))
    return text[i:j]


def a_objeto_js(bloque_texto: str) -> str:
    """Del bloque 'const X=...;' saca solo el literal {…} o […], sin 'const X=' ni ';'."""
    _, _, resto = bloque_texto.partition("=")
    return resto.strip().rstrip(";").strip()


def main():
    if not TEMPLATE.exists():
        raise SystemExit(f"No encuentro {TEMPLATE}")

    content = TEMPLATE.read_text(encoding="utf-8")

    if not BACKUP.exists():
        BACKUP.write_text(content, encoding="utf-8")
        print(f"✓ Backup: {BACKUP.name}")
    else:
        print("· Backup ya existía")

    # --- Extraer ---
    geo_obj = a_objeto_js(bloque(content, "const GEO =", "function norm"))
    GEO_JSON.write_text(geo_obj, encoding="utf-8")
    print(f"✓ {GEO_JSON.relative_to(ROOT)}  ({len(geo_obj):,} bytes)")

    m_obj = a_objeto_js(bloque(content, "const M=[", "const P="))
    M_JSON.write_text(m_obj, encoding="utf-8")
    print(f"✓ {M_JSON.relative_to(ROOT)}  ({len(m_obj):,} bytes)")

    p_obj = a_objeto_js(bloque(content, "const P={", "const Y="))
    PATHS_JS.write_text(p_obj, encoding="utf-8")
    print(f"✓ {PATHS_JS.relative_to(ROOT)}  ({len(p_obj):,} bytes)")

    # --- Reemplazar por placeholders (recomputando índices en cada paso) ---
    i = content.index("const GEO =")
    j = content.index("function norm", i)
    content = content[:i] + "const GEO = /*DATA:geo*/;\n" + content[j:]

    i = content.index("const M=[")
    j = content.index("const P=", i)
    content = content[:i] + "const M = /*DATA:municipios*/;\n" + content[j:]

    i = content.index("const P={")
    j = content.index("const Y=", i)
    content = content[:i] + "const P = /*DATA:map_paths*/;\n" + content[j:]

    TEMPLATE.write_text(content, encoding="utf-8")
    print("✓ comparativa.html es ahora plantilla")


if __name__ == "__main__":
    main()
