#!/usr/bin/env python3
"""
Extrator de dados do livro Tormenta 20 - Ameaças de Arton.
Gera os arquivos JSON em src/json/ com base no texto oficial do PDF.
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
JSON_BASE = BASE_DIR / "src" / "json"
LIVRO_ID = "ameacas_de_arton"

def save(rel_path: str, data: dict):
    out = JSON_BASE / rel_path
    out.parent.mkdir(parents=True, exist_ok=True)
    data["livro_id"] = LIVRO_ID
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"  ✓ {rel_path}")

print("Iniciando extração do suplemento Ameaças de Arton...")
