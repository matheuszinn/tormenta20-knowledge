#!/usr/bin/env python3
"""
Scan the PDF and fill in page numbers for existing JSON entities.
Uses the PDF's Table of Contents (TOC/bookmarks) as primary source,
falling back to text search for entities not in the TOC.

Usage:
    .venv/bin/python tools/pdf_extractor/scan_pages.py "books/T20 - Livro Básico - Jogo do Ano.pdf"
    .venv/bin/python tools/pdf_extractor/scan_pages.py "books/T20 - Livro Básico - Jogo do Ano.pdf" --dry-run
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import fitz  # PyMuPDF


# Mapping of JSON directories to their DB table names
DIR_TO_TABLE = {
    "racas": "racas",
    "classes": "classes",
    "origens": "origens",
    "deuses": "divindades",
    "pericias": "pericias",
    "magias": "magias",
    "condicoes": "condicoes",
    "equipamentos/armas": "armas",
    "equipamentos/armaduras": "armaduras",
    "equipamentos/escudos": "escudos",
    "equipamentos/itens": "itens",
    "poderes/poderes_gerais": "poderes",
    "poderes/poderes_concedidos": "poderes",
    "poderes/poderes_da_tormenta": "poderes",
    "poderes/habilidades_de_raca": "poderes",
    "poderes/habilidades_unicas_de_origem": "poderes",
    "poderes/habilidades_de_classe": "poderes",
    "itens_superiores/materiais_especiais": "materiais_especiais",
    "itens_superiores/melhorias": "melhorias",
    "itens_superiores/encantamentos": "encantamentos",
    "itens_magicos/pocoes": "pocoes",
    "itens_magicos/acessorios": "acessorios_magicos",
    "regras": "regras",
    "tabelas": "tabelas",
}

# Page ranges for known sections (helps disambiguate common names)
SECTION_PAGE_RANGES = {
    "t20_eja": {
        "racas":       (24, 37),
        "classes":     (38, 90),
        "origens":     (91, 101),
        "divindades":  (102, 111),
        "pericias":    (120, 129),
        "poderes":     (133, 143),
        "armas":       (152, 157),
        "armaduras":   (160, 160),
        "escudos":     (160, 160),
        "itens":       (161, 169),
        "magias":      (184, 217),
        "condicoes":   (400, 401),
        "materiais_especiais": (172, 173),
        "melhorias":   (170, 173),
        "encantamentos": (341, 351),
        "pocoes":      (347, 351),
        "acessorios_magicos": (348, 355),
        "regras":      (144, 245),
        "tabelas":     (120, 405),
    },
    "ameacas_de_arton": {
        "racas":       (31, 356),
        "poderes":     (16, 356),
        "armas":       (394, 396),
        "armaduras":   (395, 397),
        "escudos":     (395, 397),
        "itens":       (396, 401),
        "melhorias":   (401, 402),
        "materiais_especiais": (401, 404),
        "acessorios_magicos": (404, 405),
        "magias":      (405, 407),
        "regras":      (14, 420),
    }
}


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
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', '_', text.strip())
    return text


def normalize(text: str) -> str:
    """Normalize a string for comparison: lowercase, strip, collapse whitespace."""
    text = text.lower().strip()
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text


def load_all_entities(json_base: Path, livro_id: Optional[str] = None) -> List[dict]:
    """Load all JSON entities from src/json/, optionally filtered by livro_id."""
    entities = []

    for rel_dir, table in DIR_TO_TABLE.items():
        dir_path = json_base / rel_dir
        if not dir_path.exists():
            continue

        for json_file in sorted(dir_path.rglob("*.json")):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if isinstance(data, list):
                    continue

                name = data.get("name")
                entity_id = data.get("id")
                if not name or not entity_id:
                    continue

                item_livro = data.get("livro_id") or data.get("book_id") or "t20_eja"
                if livro_id and item_livro != livro_id:
                    continue

                entities.append({
                    "id": entity_id,
                    "name": name,
                    "table": table,
                    "file": json_file,
                    "data": data,
                    "has_page": "page" in data or "pagina" in data,
                })
            except Exception:
                continue

    return entities


def build_toc_lookup(pdf_path: str) -> Dict[str, int]:
    """Build a lookup from TOC bookmark titles to page numbers."""
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    doc.close()

    lookup = {}
    for level, title, page in toc:
        key = normalize(title)
        lookup[key] = page

    return lookup


def build_page_texts(pdf_path: str) -> Dict[int, str]:
    """Extract text from every page."""
    doc = fitz.open(pdf_path)
    pages = {}
    for i, page in enumerate(doc):
        pages[i + 1] = page.get_text()
    doc.close()
    return pages


def find_entity_page(
    entity_name: str,
    table: str,
    toc_lookup: Dict[str, int],
    page_texts: Dict[int, str],
    description: Optional[str] = None,
    livro_id: str = "t20_eja",
) -> Optional[int]:
    """
    Find the page for an entity using:
    1. TOC bookmark match (most reliable)
    2. Text search within the expected section page range (standalone or substring)
    3. Description text match (useful for items with custom font titles)
    """
    name_norm = normalize(entity_name)

    # 1. Try exact TOC match
    if name_norm in toc_lookup:
        return toc_lookup[name_norm]

    # Try common TOC variations
    for suffix in [
        f" ({table})",  # e.g. "acólito (origem)"
        f" (perícia)",
        f" (classe)",
    ]:
        if name_norm + suffix in toc_lookup:
            return toc_lookup[name_norm + suffix]

    # 2. Fall back to text search within section range
    book_ranges = SECTION_PAGE_RANGES.get(livro_id, SECTION_PAGE_RANGES["t20_eja"])
    page_range = book_ranges.get(table)
    if page_range:
        start_p, end_p = page_range
        
        # First pass: Description text match (most reliable, skips tables)
        if description:
            desc_norm = normalize(description[:50]) # Use up to 50 chars
            if len(desc_norm) > 10:
                for page_num in range(start_p, min(end_p + 1, max(page_texts.keys()) + 1)):
                    if page_num not in page_texts:
                        continue
                    if desc_norm in normalize(page_texts[page_num]):
                        return page_num
        
        # Second pass: Prefer standalone lines (likely a heading)
        pattern = re.compile(r'(?im)^\s*' + re.escape(entity_name) + r'\s*$')
        for page_num in range(start_p, min(end_p + 1, max(page_texts.keys()) + 1)):
            if page_num not in page_texts:
                continue
            if pattern.search(page_texts[page_num]):
                return page_num
                        
        # Third pass: Broader substring match
        for page_num in range(start_p, min(end_p + 1, max(page_texts.keys()) + 1)):
            if page_num not in page_texts:
                continue
            page_text = page_texts[page_num].lower()
            if name_norm in page_text:
                return page_num
                    
    # 4. Broader text search for entities without a known range
    if not page_range:
        for page_num in sorted(page_texts.keys()):
            if name_norm in page_texts[page_num].lower():
                return page_num

    return None


def update_indice_remissivo(
    index_file: Path,
    livro_id: str,
    entries_to_add: List[dict],
) -> Tuple[int, int]:
    """Update the indice_remissivo JSON file. Returns (added, enriched)."""
    existing = []
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            existing = json.load(f)

    existing_by_reg = {}
    existing_by_termo_page = {}
    for entry in existing:
        reg_key = (entry.get("tabela"), entry.get("registro_id"))
        if reg_key[1]:
            existing_by_reg[reg_key] = entry
        tp_key = (entry.get("termo", "").lower().strip(), entry.get("pagina"))
        existing_by_termo_page[tp_key] = entry

    added = 0
    enriched = 0
    for new_entry in entries_to_add:
        reg_key = (new_entry.get("tabela"), new_entry.get("registro_id"))
        tp_key = (new_entry["termo"].lower().strip(), new_entry["pagina"])

        if reg_key[1] and reg_key in existing_by_reg:
            entry = existing_by_reg[reg_key]
            entry["pagina"] = new_entry["pagina"]
            entry["termo"] = new_entry["termo"]
            enriched += 1
        elif tp_key in existing_by_termo_page:
            entry = existing_by_termo_page[tp_key]
            if new_entry.get("tabela") and not entry.get("tabela"):
                entry["tabela"] = new_entry["tabela"]
                enriched += 1
            if new_entry.get("registro_id") and not entry.get("registro_id"):
                entry["registro_id"] = new_entry["registro_id"]
                enriched += 1
        else:
            existing.append(new_entry)
            added += 1

    existing.sort(key=lambda x: slugify(x.get("termo", "")))

    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    return added, enriched


def main():
    parser = argparse.ArgumentParser(description="Scan PDF and fill page numbers in existing JSONs")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--livro-id", default="t20_eja", help="Book ID (default: t20_eja)")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Don't write files, just show matches")
    args = parser.parse_args()

    json_base = Path(__file__).parent.parent.parent / "src" / "json"
    pdf_path = args.pdf_path

    print(f"📖 Loading PDF: {pdf_path}")

    print("   Building TOC lookup...")
    toc_lookup = build_toc_lookup(pdf_path)
    print(f"   {len(toc_lookup)} TOC entries")

    print("   Extracting page texts...")
    page_texts = build_page_texts(pdf_path)
    print(f"   {len(page_texts)} pages indexed\n")

    print("📂 Loading JSON entities...")
    entities = load_all_entities(json_base, args.livro_id)
    print(f"   {len(entities)} entities found for book '{args.livro_id}'\n")

    index_entries = []
    for entity in entities:
        p = entity["data"].get("page") or entity["data"].get("pagina")
        if p:
            index_entries.append({
                "termo": entity["name"],
                "pagina": int(p),
                "tabela": entity["table"],
                "registro_id": entity["id"],
            })

    already_has_page = len([e for e in entities if e["has_page"]])
    needs_page = [e for e in entities if not e["has_page"]]
    print(f"   {already_has_page} already have page numbers")
    print(f"   {len(needs_page)} need page numbers\n")

    print("🔍 Scanning PDF for entity names...")
    found = 0
    not_found = 0

    for entity in needs_page:
        desc = entity["data"].get("description") or entity["data"].get("descricao")
        page = find_entity_page(entity["name"], entity["table"], toc_lookup, page_texts, description=desc, livro_id=args.livro_id)
        if page:
            found += 1
            entity["found_page"] = page

            index_entries.append({
                "termo": entity["name"],
                "pagina": page,
                "tabela": entity["table"],
                "registro_id": entity["id"],
            })

            if not args.dry_run:
                data = entity["data"]
                data["page"] = page
                with open(entity["file"], "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    f.write("\n")

            print(f"  ✓ {entity['name']} ({entity['table']}) → p. {page}")
        else:
            not_found += 1

    print(f"\n{'='*60}")
    print(f"📊 Results:")
    print(f"   Found: {found}")
    print(f"   Not found: {not_found}")

    if not args.dry_run and index_entries:
        index_file = json_base / "indice_remissivo" / f"{args.livro_id}.json"
        new_added, enriched = update_indice_remissivo(index_file, args.livro_id, index_entries)
        print(f"\n📇 Updated {index_file.name}: {new_added} new, {enriched} enriched")

    if not_found > 0:
        print(f"\n⚠ Entities not found in PDF ({not_found}):")
        for entity in needs_page:
            if "found_page" not in entity:
                print(f"    - {entity['name']} ({entity['table']}, {entity['file'].name})")


if __name__ == "__main__":
    main()
