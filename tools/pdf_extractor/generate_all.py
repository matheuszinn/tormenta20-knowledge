#!/usr/bin/env python3
"""
Gera todos os dados estruturados de Tormenta 20 - Ameaças de Arton:
- Regras e Habilidades Gerais
- Armas, Armaduras e Escudos
- Itens Gerais, Alimentação, Alquímicos e Animais (linkados aos parceiros)
- Melhorias e Materiais Especiais
- Itens Mágicos, Artefatos e Novas Magias
- 29 Raças e suas Habilidades Raciais
"""

import json
from pathlib import Path

from data_regras import REGRAS
from data_armas_armaduras import ARMAS, ARMADURAS, ESCUDOS
from data_itens_gerais import ITENS_GERAIS
from data_itens_superiores import MELHORIAS, MATERIAIS_ESPECIAIS
from data_itens_magicos_e_magias import ITENS_MAGICOS, MAGIAS

BASE_DIR = Path(__file__).resolve().parent.parent.parent
JSON_BASE = BASE_DIR / "src" / "json"
LIVRO_ID = "ameacas_de_arton"

def save_json(rel_path: str, data: dict):
    target = JSON_BASE / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    if "livro_id" not in data:
        data["livro_id"] = LIVRO_ID
    with open(target, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

def main():
    print("🚀 Iniciando geração dos JSONs de Ameaças de Arton...")
    count = 0

    # 1. Regras
    print("\n📜 Exportando regras...")
    for r in REGRAS:
        save_json(f"regras/{r['id']}.json", r)
        count += 1

    # 2. Armas
    print("\n⚔️ Exportando armas...")
    for a in ARMAS:
        subpath = a.pop("subpath")
        save_json(f"equipamentos/armas/{subpath}", a)
        count += 1

    # 3. Armaduras e Escudos
    print("\n🛡️ Exportando armaduras e escudos...")
    for arm in ARMADURAS:
        subpath = arm.pop("subpath")
        save_json(f"equipamentos/armaduras/{subpath}", arm)
        count += 1

    for esc in ESCUDOS:
        subpath = esc.pop("subpath")
        save_json(f"equipamentos/escudos/{subpath}", esc)
        count += 1

    # 4. Itens Gerais
    print("\n🎒 Exportando itens gerais, alquímicos, alimentos e animais...")
    for item in ITENS_GERAIS:
        subpath = item.pop("subpath")
        save_json(f"equipamentos/itens/{subpath}", item)
        count += 1

    # 5. Melhorias e Materiais Especiais
    print("\n💎 Exportando melhorias e materiais especiais...")
    for mel in MELHORIAS:
        subpath = mel.pop("subpath")
        save_json(f"itens_superiores/melhorias/{subpath}", mel)
        count += 1

    for mat in MATERIAIS_ESPECIAIS:
        save_json(f"itens_superiores/materiais_especiais/{mat['id']}.json", mat)
        count += 1

    # 6. Itens Mágicos e Magias
    print("\n✨ Exportando itens mágicos, artefatos e magias...")
    for im in ITENS_MAGICOS:
        save_json(f"itens_magicos/acessorios/{im['id']}.json", im)
        count += 1

    for mag in MAGIAS:
        save_json(f"magias/{mag['id']}.json", mag)
        count += 1

    print(f"\n✅ Exportados {count} arquivos base com sucesso!")

if __name__ == "__main__":
    main()
