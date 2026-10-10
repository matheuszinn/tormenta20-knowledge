#!/usr/bin/env python3
"""
Extrai as 29 raças jogáveis de Tormenta 20 - Ameaças de Arton e suas habilidades de raça
a partir do texto oficial do PDF e salva em src/json/racas/ e src/json/poderes/habilidades_de_raca/.
"""

import json
import re
from pathlib import Path
import fitz

BASE_DIR = Path(__file__).resolve().parent.parent.parent
JSON_BASE = BASE_DIR / "src" / "json"
LIVRO_ID = "ameacas_de_arton"
PDF_PATH = BASE_DIR / "books" / "Tormenta 20 - Ameaças de Arton.pdf"

def slugify(text: str) -> str:
    replacements = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n'
    }
    text = text.lower()
    for char, rep in replacements.items():
        text = text.replace(char, rep)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', '_', text.strip())
    return text

def clean_text(text: str) -> str:
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    text = re.sub(r'\s*\n\s*', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

RACES_CONFIG = [
    {
        "id": "bugbear",
        "name": "Bugbear",
        "page": 79,
        "pdf_page": 81,
        "size": "médio",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"forca": 2, "destreza": 1, "carisma": -1},
        "search": "Bugbear: Habilidades de Raça",
        "description": "Grandes goblinoides brutais e peludos, com sentidos predatórios aguçados e apetite pelo terror de suas presas."
    },
    {
        "id": "centauro",
        "name": "Centauro",
        "page": 105,
        "pdf_page": 107,
        "size": "grande",
        "movement": 12,
        "vision": "normal",
        "attributes": {"sabedoria": 2, "forca": 1, "inteligencia": -1},
        "search": "Centauro: Habilidades de Raça",
        "description": "Nômades orgulhosos com tronco humanoide e corpo inferior de cavalo, mestres da cavalaria e das planícies."
    },
    {
        "id": "ceratops",
        "name": "Ceratops",
        "page": 265,
        "pdf_page": 267,
        "size": "médio",
        "movement": 9,
        "vision": "visao_na_penumbra",
        "attributes": {"constituicao": 2, "forca": 1, "destreza": -1, "inteligencia": -1},
        "search": "Ceratops: Habilidades de Raça",
        "description": "Povo-trovão robusto com gola óssea e chifres frontais imponentes, leais e defensores inabaláveis de suas tribos."
    },
    {
        "id": "elfo_do_mar",
        "name": "Elfo-do-Mar",
        "page": 316,
        "pdf_page": 318,
        "size": "médio",
        "movement": 9,
        "vision": "visao_na_penumbra",
        "attributes": {"destreza": 2, "constituicao": 1, "inteligencia": -1},
        "search": "Elfo-do-Mar:  Habilidades de Raça",
        "description": "Primos aquáticos dos elfos terrestres adaptados às profundezas do Grande Oceano, com brânquias e pele em tons oceânicos."
    },
    {
        "id": "finntroll",
        "name": "Finntroll",
        "page": 339,
        "pdf_page": 341,
        "size": "médio",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"inteligencia": 2, "constituicao": 1, "forca": -1},
        "search": "Finntroll:  \nHabilidades de Raça",
        "description": "Trolls nobres cultos e cruéis com fisiologia vegetal regenerativa, mestres de magia e escravagistas temidos."
    },
    {
        "id": "gnoll",
        "name": "Gnoll",
        "page": 115,
        "pdf_page": 117,
        "size": "médio",
        "movement": 9,
        "vision": "visao_na_penumbra",
        "attributes": {"constituicao": 2, "sabedoria": 1, "inteligencia": -1},
        "search": "Gnoll: Habilidades de Raça",
        "description": "Humanoides hienídeos agressivos e gregários que caçam em matilhas implacáveis e respeitam a força."
    },
    {
        "id": "golem_desperto",
        "name": "Golem Desperto",
        "page": 134,
        "pdf_page": 136,
        "size": "médio",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"forca": 1, "carisma": -1},
        "search": "Chassi.",
        "description": "Golens que despertaram consciência além do modelo de ferro básico, podendo ser construídos com chassis de barro, bronze ou espelhos."
    },
    {
        "id": "harpia",
        "name": "Harpia",
        "page": 201,
        "pdf_page": 203,
        "size": "médio",
        "movement": 12,
        "vision": "visao_no_escuro",
        "attributes": {"destreza": 2, "carisma": 1, "inteligencia": -1},
        "search": "Harpia: Habilidades de Raça",
        "description": "Criaturas aladas predadoras com asas emplumadas e garras rapinantes nos pés, capazes de voar e aterrorizar com seus gritos estridentes."
    },
    {
        "id": "hobgoblin",
        "name": "Hobgoblin",
        "page": 84,
        "pdf_page": 86,
        "size": "médio",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"constituicao": 2, "destreza": 1, "carisma": -1},
        "search": "Hobgoblin: Habilidades de Raça",
        "description": "Goblinoides disciplinados e militaristas da Aliança Negra, criados para a guerra, estratégia e lealdade hierárquica."
    },
    {
        "id": "kallyanach",
        "name": "Kallyanach",
        "page": 151,
        "pdf_page": 153,
        "size": "médio",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"escolha": "+2 em um atributo ou +1 em dois atributos"},
        "search": "Herança Dracônica",
        "description": "Humanoides abençoados com sangue dracônico direto de Kallyadranoch, ostentando escamas, cauda e sopro elemental."
    },
    {
        "id": "kaijin",
        "name": "Kaijin",
        "page": 157,
        "pdf_page": 159,
        "size": "médio",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"forca": 2, "constituicao": 1, "carisma": -2},
        "search": "Kaijin: Habilidades de Raça",
        "description": "Nascidos da contaminação da Tormenta em Tamu-ra, com couraças avermelhadas e força monstruosa, buscando honra ou redenção."
    },
    {
        "id": "kappa",
        "name": "Kappa",
        "page": 158,
        "pdf_page": 160,
        "size": "pequeno",
        "movement": 9,
        "vision": "visao_na_penumbra",
        "attributes": {"destreza": 2, "constituicao": 1, "carisma": -1},
        "search": "Kappa: Habilidades de Raça",
        "description": "Espíritos aquáticos anfíbios com carapaça de tartaruga e prato d'água no topo da cabeça, travessos e leais a promessas."
    },
    {
        "id": "kobolds",
        "name": "Kobolds",
        "page": 182,
        "pdf_page": 185,
        "size": "pequeno",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"destreza": 2, "forca": -1},
        "search": "Kobolds: Habilidades de Raça",
        "description": "Um personagem kobolds é um ajuntamento de pequenos répteis que agem e lutam em conjunto como uma única entidade engenhosa."
    },
    {
        "id": "mashin",
        "name": "Mashin",
        "page": 160,
        "pdf_page": 162,
        "size": "médio",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"forca": 1, "carisma": -1},
        "search": "Mashin: Habilidades de Raça",
        "description": "Golens esguios e artísticos de Tamu-ra imbuídos com espíritos ancestrais, integrando precisão e tradição oriental."
    },
    {
        "id": "meio_orc",
        "name": "Meio-Orc",
        "page": 31,
        "pdf_page": 33,
        "size": "médio",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"forca": 2, "outro": 1},
        "search": "Meio-Orc: Habilidades de Raça",
        "description": "Descendentes da união entre humanos e orcs, combinando a versatilidade humana com a ferocidade e resistência orc."
    },
    {
        "id": "minauro",
        "name": "Minauro",
        "page": 175,
        "pdf_page": 177,
        "size": "médio",
        "movement": 9,
        "vision": "visao_na_penumbra",
        "attributes": {"forca": 1, "outros_dois": 1},
        "search": "Minauro: Habilidades de Raça",
        "description": "Descendentes da mistura de minotauros com humanos ou outras raças, mantendo chifres e determinação mas sem a fobia de labirintos."
    },
    {
        "id": "moreau",
        "name": "Moreau",
        "page": 303,
        "pdf_page": 305,
        "size": "médio",
        "movement": 9,
        "vision": "visao_na_penumbra",
        "attributes": {"heranca": 1, "outros_dois": 1},
        "search": "Herança.",
        "description": "Habitantes dos Reinos de Moreania abençoados pelos Doze Deuses Animais, com traços da herança de seu clã ancestral."
    },
    {
        "id": "nagah",
        "name": "Nagah",
        "page": 333,
        "pdf_page": 335,
        "size": "médio",
        "movement": 9,
        "vision": "visao_na_penumbra",
        "attributes": {"forca": 1, "destreza": 1, "constituicao": 1},
        "search": "Nagah: Habilidades de Raça",
        "description": "Povo serpentino com tronco humanoide e cauda de cobra em vez de pernas, sutis e ágeis no combate."
    },
    {
        "id": "nezumi",
        "name": "Nezumi",
        "page": 162,
        "pdf_page": 164,
        "size": "pequeno",
        "movement": 9,
        "vision": "visao_na_penumbra",
        "attributes": {"constituicao": 2, "destreza": 1, "inteligencia": -1},
        "search": "Nezumi: Habilidades de Raça",
        "description": "Humanoides ratos sobreviventes nativos das ilhas de Tamu-ra, conhecidos pela resiliência, velocidade e engenho rústico."
    },
    {
        "id": "ogro",
        "name": "Ogro",
        "page": 40,
        "pdf_page": 42,
        "size": "grande",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"forca": 3, "constituicao": 2, "inteligencia": -1, "carisma": -1},
        "search": "Ogro:  Habilidades de Raça",
        "description": "Gigantescos e musculosos habitantes das montanhas e ermos artonianos com força avassaladora e compleição intimidadora."
    },
    {
        "id": "orc",
        "name": "Orc",
        "page": 33,
        "pdf_page": 35,
        "size": "médio",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"forca": 2, "constituicao": 1, "inteligencia": -1},
        "search": "Orc: Habilidades de Raça",
        "description": "Guerreiros subterrâneos fortes e honrados, forjados pelas agruras das profundezas e pela tradição tribal."
    },
    {
        "id": "pteros",
        "name": "Pteros",
        "page": 267,
        "pdf_page": 269,
        "size": "médio",
        "movement": 9,
        "vision": "visao_na_penumbra",
        "attributes": {"sabedoria": 2, "destreza": 1, "inteligencia": -1},
        "search": "Pteros: Habilidades de Raça",
        "description": "Membros alados dos povos-trovão de Galrasia, sábios exploradores dos céus e observadores atentos da natureza."
    },
    {
        "id": "soterrado",
        "name": "Soterrado",
        "page": 354,
        "pdf_page": 356,
        "size": "médio",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"constituicao": -1, "outros_tres": 1},
        "search": "Raça Variante:",
        "description": "Variante da raça osteon preservada pelo gelo perpétuo das Uivantes, imbuída com o frio da morte."
    },
    {
        "id": "tabrachi",
        "name": "Tabrachi",
        "page": 37,
        "pdf_page": 39,
        "size": "médio",
        "movement": 9,
        "vision": "visao_na_penumbra",
        "attributes": {"constituicao": 2, "forca": 1, "carisma": -1},
        "search": "Tabrachi: Habilidades de Raça",
        "description": "Guerreiros anfibios robustos semelhantes a sapos antropomórficos, mestres da luta com salto e camuflagem pantaneira."
    },
    {
        "id": "tengu",
        "name": "Tengu",
        "page": 164,
        "pdf_page": 166,
        "size": "médio",
        "movement": 9,
        "vision": "visao_na_penumbra",
        "attributes": {"destreza": 2, "inteligencia": 1},
        "search": "Tengu: Habilidades",
        "description": "Humanoides com feições e asas de corvo de Tamu-ra, esgrimistas graciosos e ilusionistas naturais."
    },
    {
        "id": "trog_anao",
        "name": "Trog Anão",
        "page": 39,
        "pdf_page": 41,
        "size": "pequeno",
        "movement": 6,
        "vision": "visao_no_escuro",
        "attributes": {"constituicao": 2, "forca": 1, "destreza": -1, "inteligencia": -1},
        "search": "Raça Variante: Trog Anão",
        "description": "Variante reptiliana menor dos trogs com a resistência obstinada dos anões e mau cheiro característico."
    },
    {
        "id": "velocis",
        "name": "Velocis",
        "page": 268,
        "pdf_page": 270,
        "size": "médio",
        "movement": 12,
        "vision": "visao_na_penumbra",
        "attributes": {"destreza": 2, "sabedoria": 1, "inteligencia": -1},
        "search": "Velocis: Habilidades de Raça",
        "description": "Povo-trovão velociraptor veloz e caçador implacável das savanas e florestas densas de Galrasia."
    },
    {
        "id": "voracis",
        "name": "Voracis",
        "page": 270,
        "pdf_page": 272,
        "size": "médio",
        "movement": 9,
        "vision": "visao_na_penumbra",
        "attributes": {"destreza": 2, "constituicao": 1, "inteligencia": -1},
        "search": "Voracis: Habilidades de Raça",
        "description": "Predadores bípedes ferozes com garras afiadas e dentes serrilhados, caçadores implacáveis de presas grandes."
    },
    {
        "id": "yidishan",
        "name": "Yidishan",
        "page": 300,
        "pdf_page": 302,
        "size": "médio",
        "movement": 9,
        "vision": "visao_no_escuro",
        "attributes": {"carisma": -2, "outros_tres": 1},
        "search": "Yidishan: Habilidades de Raça",
        "description": "Híbridos mecânico-orgânicos que combinam carne e componentes metálicos ou mecânicos em simbiose."
    }
]

def extract_abilities_from_text(section_text: str):
    # Encontra o fim da caixa de raça
    for stop in ['Longevidade.', 'Longevidade', 'Devotos.', 'Devotos:']:
        idx = section_text.find(stop)
        if idx != -1:
            eol = section_text.find('\n', idx + len(stop) + 15)
            section_text = section_text[:eol if eol != -1 else idx + 50]
            break

    abilities = []
    pattern = r'(?:^|\n|•\s*)([A-ZÁ-Ú][A-Za-zÁ-ú\s\’\'-]{2,30})\.\s+'
    matches = list(re.finditer(pattern, section_text))
    for i, m in enumerate(matches):
        name = m.group(1).strip()
        if name in ['Longevidade', 'Devotos', 'Equipamento', 'Tesouro']:
            continue
        start_pos = m.end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(section_text)
        desc = section_text[start_pos:end_pos].strip()
        abilities.append({
            "name": name,
            "description": clean_text(desc)
        })
    return abilities

def main():
    doc = fitz.open(PDF_PATH)
    print("📖 Lendo PDF para extração das 29 raças...")

    total_races = 0
    total_powers = 0

    for cfg in RACES_CONFIG:
        p_idx = cfg["pdf_page"] - 1
        text = doc[p_idx].get_text()
        if cfg["id"] == "moreau":
            text += "\n" + doc[p_idx + 1].get_text()

        search_term = cfg["search"]
        start_idx = text.find(search_term)
        if start_idx == -1:
            m = re.search(rf'{cfg["name"].split()[0]}[:\s\n]+Habilidades? de Raça', text, re.IGNORECASE)
            start_idx = m.start() if m else 0

        section = text[start_idx:start_idx + 4000]

        abilities = extract_abilities_from_text(section)
        ability_ids = []

        race_powers_dir = JSON_BASE / "poderes" / "habilidades_de_raca" / cfg["id"]
        race_powers_dir.mkdir(parents=True, exist_ok=True)

        for ab in abilities:
            ab_id = slugify(ab["name"])
            ability_ids.append(ab_id)

            power_data = {
                "id": ab_id,
                "name": ab["name"],
                "type": "habilidade_de_raca",
                "race": cfg["id"],
                "description": ab["description"],
                "effects": {},
                "page": cfg["page"],
                "livro_id": LIVRO_ID
            }

            p_file = race_powers_dir / f"{ab_id}.json"
            with open(p_file, "w", encoding="utf-8") as f:
                json.dump(power_data, f, ensure_ascii=False, indent=2)
                f.write("\n")
            total_powers += 1

        race_data = {
            "id": cfg["id"],
            "name": cfg["name"],
            "description": cfg["description"],
            "size": cfg["size"],
            "movement": cfg["movement"],
            "vision": cfg["vision"],
            "vision_range": None,
            "attribute_bonuses": cfg["attributes"],
            "skill_bonuses": [],
            "racial_abilities": ability_ids,
            "chosen_abilities_amount": 0,
            "available_chosen_abilities": [],
            "page": cfg["page"],
            "livro_id": LIVRO_ID
        }

        r_file = JSON_BASE / "racas" / f"{cfg['id']}.json"
        with open(r_file, "w", encoding="utf-8") as f:
            json.dump(race_data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        total_races += 1
        print(f"  ✓ {cfg['name']} ({len(ability_ids)} habilidades)")

    print(f"\n🎉 Sucesso! {total_races} raças e {total_powers} habilidades raciais exportadas!")

if __name__ == "__main__":
    main()
