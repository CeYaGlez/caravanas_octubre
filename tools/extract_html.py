"""
Script de UNA SOLA VEZ: extrae datos del HTML original y convierte
calendario.html en una plantilla con placeholders.

Uso:
    python tools/extract_html.py

Hace 3 cosas:
    1. Extrae P y BG (mapa SVG) → assets/mapa_paths.js
    2. Extrae E (eventos octubre) → data/calendario_oct_2026.csv
    3. Reescribe calendario.html con placeholders /*DATA:xxx*/
"""
import ast
import re
from pathlib import Path


ROOT      = Path(__file__).resolve().parent.parent
HTML      = ROOT / "assets" / "templates" / "calendario.html"
BACKUP    = ROOT / "assets" / "templates" / "calendario.html.bak"
MAPA_JS   = ROOT / "assets" / "mapa_paths.js"
EVENTOS   = ROOT / "data" / "calendario_oct_2026.csv"


def main():
    if not HTML.exists():
        raise SystemExit(f"No encuentro {HTML}")

    content = HTML.read_text(encoding="utf-8")

    # Respaldo la primera vez
    if not BACKUP.exists():
        BACKUP.write_text(content, encoding="utf-8")
        print(f"✓ Backup guardado en {BACKUP.name}")
    else:
        print(f"· Backup ya existía, no lo sobrescribo")

    # ---------- 1. Extraer P y BG ----------
    m_p = re.search(r'const P=(\{.*?\});\s*const BG=', content, re.DOTALL)
    m_bg = re.search(r'const BG=(\{.*?\});\s*const R=', content, re.DOTALL)
    if not m_p or not m_bg:
        raise SystemExit("No pude encontrar P o BG en el HTML")

    mapa_js_content = (
        "// Generado automáticamente por tools/extract_html.py\n"
        f"const P={m_p.group(1)};\n"
        f"const BG={m_bg.group(1)};\n"
    )
    MAPA_JS.write_text(mapa_js_content, encoding="utf-8")
    print(f"✓ {MAPA_JS.relative_to(ROOT)} creado ({len(mapa_js_content):,} bytes)")

    # ---------- 2. Extraer E ----------
    m_e = re.search(r'const E=\[(.*?)\]\.map\(', content, re.DOTALL)
    if not m_e:
        raise SystemExit("No pude encontrar E en el HTML")

    e_raw = "[" + m_e.group(1) + "]"
    # R(1,3) → [1, 2, 3]
    e_raw = re.sub(
        r"R\((\d+),(\d+)\)",
        lambda mm: str(list(range(int(mm.group(1)), int(mm.group(2)) + 1))),
        e_raw,
    )
    eventos = ast.literal_eval(e_raw)

    lineas = ["caravana,municipio,map_key,dia_inicio,dia_fin,destacado"]
    for ev in eventos:
        caravana, municipio, map_key, dias = ev[0], ev[1], ev[2], ev[3]
        destacado = ev[4] if len(ev) > 4 else 0
        lineas.append(
            f"{caravana},{municipio},{map_key},{dias[0]},{dias[-1]},{destacado}"
        )
    EVENTOS.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"✓ {EVENTOS.relative_to(ROOT)} creado ({len(eventos)} eventos)")

    # ---------- 3. Reescribir el HTML con placeholders ----------
    new_content = re.sub(
        r'const P=\{.*?\};\s*const BG=\{.*?\};\s*const R=',
        "/*DATA:mapa_paths*/\nconst R=",
        content,
        count=1,
        flags=re.DOTALL,
    )
    new_content = re.sub(
        r'const E=\[.*?\]\.map\(',
        "const E=[\n/*DATA:eventos*/\n].map(",
        new_content,
        count=1,
        flags=re.DOTALL,
    )

    if new_content == content:
        raise SystemExit("⚠ No se modificó nada. Revisa los regex.")

    HTML.write_text(new_content, encoding="utf-8")
    print(f"✓ calendario.html convertido en plantilla")


if __name__ == "__main__":
    main()
