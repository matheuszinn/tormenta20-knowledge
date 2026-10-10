"""
Pipeline principal para extração de dados do PDF do Tormenta 20.

Uso:
    python pipeline.py <pdf_path> <section> <entity_type> [--model MODEL] [--output-dir DIR]

Exemplo:
    python pipeline.py tormenta20.pdf racas racas --model mistral --output-dir ../../src/json/racas
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Optional

import requests
from tqdm import tqdm

from pdf_extractor import PDFExtractor, extract_entities, list_available_sections, ENTITY_PATTERNS
from prompts import get_prompt, PROMPTS


# Configuração do Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "mistral"


class LLMClient:
    """Cliente para comunicação com o Ollama."""

    def __init__(self, model: str = DEFAULT_MODEL, base_url: str = OLLAMA_URL):
        self.model = model
        self.base_url = base_url

    def check_connection(self) -> bool:
        """Verifica se o Ollama está rodando."""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    def list_models(self) -> list[str]:
        """Lista modelos disponíveis."""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [m["name"] for m in data.get("models", [])]
        except:
            pass
        return []

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.1) -> str:
        """
        Gera resposta do modelo.

        Args:
            system_prompt: Prompt de sistema
            user_prompt: Prompt do usuário
            temperature: Temperatura (menor = mais determinístico)

        Returns:
            Resposta do modelo
        """
        payload = {
            "model": self.model,
            "prompt": user_prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": 4096,  # Máximo de tokens na resposta
            }
        }

        try:
            response = requests.post(self.base_url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.Timeout:
            raise TimeoutError("Timeout ao gerar resposta do modelo")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Erro de conexão com Ollama: {e}")


def extract_json_from_response(response: str) -> Optional[dict]:
    """
    Extrai JSON de uma resposta do modelo.

    Tenta encontrar JSON válido mesmo se houver texto extra.
    """
    # Remove markdown code blocks se presentes
    response = re.sub(r'^```json\s*', '', response, flags=re.MULTILINE)
    response = re.sub(r'^```\s*$', '', response, flags=re.MULTILINE)
    response = response.strip()

    # Tenta parsear diretamente
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass

    # Tenta encontrar JSON no texto
    json_patterns = [
        r'\{[\s\S]*\}',  # Objeto JSON
        r'\[[\s\S]*\]',  # Array JSON
    ]

    for pattern in json_patterns:
        matches = re.findall(pattern, response)
        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue

    return None


def slugify(text: str) -> str:
    """Converte texto para slug."""
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


ENTITY_TYPE_TO_TABLE = {
    "racas": "racas",
    "classes": "classes",
    "origens": "origens",
    "divindades": "divindades",
    "pericias": "pericias",
    "magias": "magias",
    "poderes": "poderes",
    "poderes_combate": "poderes",
    "poderes_destino": "poderes",
    "poderes_magia": "poderes",
    "poderes_concedidos": "poderes",
    "poderes_tormenta": "poderes",
    "armas": "armas",
    "armaduras": "armaduras",
    "itens_gerais": "itens",
    "condicoes": "condicoes",
    "itens_superiores": "melhorias",
    "pocoes_pergaminhos": "pocoes",
    "acessorios": "acessorios_magicos",
}

ENTITY_TYPE_TO_DIR = {
    "racas": "racas",
    "classes": "classes",
    "origens": "origens",
    "divindades": "deuses",
    "pericias": "pericias",
    "magias": "magias",
    "condicoes": "condicoes",
    "armas": "equipamentos/armas",
    "armaduras": "equipamentos/armaduras",
    "itens_gerais": "equipamentos/itens",
    "poderes_combate": "poderes/poderes_gerais",
    "poderes_destino": "poderes/poderes_gerais",
    "poderes_magia": "poderes/poderes_gerais",
    "poderes_concedidos": "poderes/poderes_concedidos",
    "poderes_tormenta": "poderes/poderes_da_tormenta",
    "pocoes_pergaminhos": "itens_magicos/pocoes",
    "acessorios": "itens_magicos/acessorios",
}


def update_indice_remissivo(
    livro_id: str,
    termo: str,
    pagina: int,
    tabela: Optional[str] = None,
    registro_id: Optional[str] = None,
    index_dir: Optional[Path] = None
) -> bool:
    """
    Atualiza ou insere uma entrada no índice remissivo JSON do livro especificado.
    """
    if index_dir is None:
        index_dir = Path(__file__).parent.parent.parent / "src" / "json" / "indice_remissivo"

    index_dir.mkdir(parents=True, exist_ok=True)
    index_file = index_dir / f"{livro_id}.json"

    entries = []
    if index_file.exists():
        try:
            with open(index_file, "r", encoding="utf-8") as f:
                entries = json.load(f)
        except Exception as e:
            print(f"Aviso ao carregar {index_file}: {e}")
            entries = []

    # Procura entrada existente por (tabela, registro_id) ou (termo, pagina)
    found = False
    for entry in entries:
        if registro_id and entry.get("registro_id") == registro_id and entry.get("tabela") == tabela:
            entry["pagina"] = pagina
            entry["termo"] = termo
            found = True
            break
        elif entry.get("termo", "").strip().lower() == termo.strip().lower() and entry.get("pagina") == pagina:
            if tabela:
                entry["tabela"] = tabela
            if registro_id:
                entry["registro_id"] = registro_id
            found = True
            break

    if not found:
        new_entry = {
            "termo": termo,
            "pagina": pagina,
        }
        if tabela:
            new_entry["tabela"] = tabela
        if registro_id:
            new_entry["registro_id"] = registro_id
        entries.append(new_entry)

    entries.sort(key=lambda x: slugify(x.get("termo", "")))

    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    return True


def validate_json_structure(data: dict, entity_type: str) -> tuple[bool, list[str]]:
    """
    Valida a estrutura básica do JSON.

    Returns:
        Tupla (é_válido, lista_de_erros)
    """
    errors = []

    # Campos obrigatórios para todos os tipos
    required_fields = ["id", "name"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Campo obrigatório ausente: {field}")

    # Validações específicas por tipo
    if entity_type == "racas":
        if "attributes" not in data:
            errors.append("Campo 'attributes' ausente")
        if "abilities" not in data:
            errors.append("Campo 'abilities' ausente")

    elif entity_type == "classes":
        if "hit_points" not in data:
            errors.append("Campo 'hit_points' ausente")
        if "skills" not in data:
            errors.append("Campo 'skills' ausente")

    elif entity_type == "origens":
        if "benefits" not in data:
            errors.append("Campo 'benefits' ausente")

    elif entity_type == "divindades":
        if "channel_energy" not in data:
            errors.append("Campo 'channel_energy' ausente")
        if "granted_powers" not in data:
            errors.append("Campo 'granted_powers' ausente")

    elif entity_type == "pericias":
        if "key_attribute" not in data:
            errors.append("Campo 'key_attribute' ausente")
        if "uses" not in data:
            errors.append("Campo 'uses' ausente")

    elif entity_type == "magias":
        if "type" not in data:
            errors.append("Campo 'type' ausente")
        if "circle" not in data:
            errors.append("Campo 'circle' ausente")

    return len(errors) == 0, errors


def process_entity(
    client: LLMClient,
    entity_content: str,
    entity_type: str,
    retries: int = 2
) -> tuple[Optional[dict], list[str]]:
    """
    Processa uma entidade e retorna o JSON.

    Args:
        client: Cliente LLM
        entity_content: Conteúdo textual da entidade
        entity_type: Tipo de entidade
        retries: Número de tentativas

    Returns:
        Tupla (json_data ou None, lista_de_erros)
    """
    errors = []

    for attempt in range(retries + 1):
        try:
            system_prompt, user_prompt = get_prompt(entity_type, entity_content)
            response = client.generate(system_prompt, user_prompt)

            json_data = extract_json_from_response(response)
            if json_data is None:
                errors.append(f"Tentativa {attempt + 1}: Não foi possível extrair JSON da resposta")
                continue

            is_valid, validation_errors = validate_json_structure(json_data, entity_type)
            if not is_valid:
                errors.extend([f"Tentativa {attempt + 1}: {e}" for e in validation_errors])
                continue

            return json_data, []

        except Exception as e:
            errors.append(f"Tentativa {attempt + 1}: {str(e)}")

        if attempt < retries:
            time.sleep(1)  # Pequena pausa entre tentativas

    return None, errors


def run_pipeline(
    pdf_path: str,
    section: str,
    entity_type: str,
    model: str = DEFAULT_MODEL,
    output_dir: str = None,
    dry_run: bool = False,
    toc_start: int = 3,
    toc_end: int = 6,
    livro_id: str = "t20_eja",
    update_index: bool = True
) -> dict:
    """
    Executa o pipeline completo.

    Args:
        pdf_path: Caminho para o PDF
        section: Seção do índice ou slug
        entity_type: Tipo de entidade
        model: Modelo LLM a usar
        output_dir: Diretório de saída
        dry_run: Se True, não salva arquivos
        toc_start: Página inicial do índice
        toc_end: Página final do índice
        livro_id: ID do livro no banco de dados (padrão: "t20_eja")
        update_index: Se True, sincroniza o índice remissivo JSON

    Returns:
        Estatísticas de execução
    """
    stats = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "errors": []
    }

    # Verificar tipo de entidade
    if entity_type not in PROMPTS:
        print(f"Erro: Tipo de entidade '{entity_type}' desconhecido.")
        print(f"Tipos disponíveis: {list(PROMPTS.keys())}")
        sys.exit(1)

    # Inicializar cliente LLM
    client = LLMClient(model=model)

    if not dry_run:
        if not client.check_connection():
            print("Erro: Ollama não está rodando.")
            print("Inicie com: ollama serve")
            sys.exit(1)

        available_models = client.list_models()
        if model not in [m.split(":")[0] for m in available_models]:
            print(f"Aviso: Modelo '{model}' pode não estar instalado.")
            print(f"Modelos disponíveis: {available_models}")
            print(f"Instale com: ollama pull {model}")

    # Preparar diretório de saída
    if output_dir:
        output_path = Path(output_dir)
    else:
        sub_dir = ENTITY_TYPE_TO_DIR.get(entity_type, entity_type)
        output_path = Path(__file__).parent.parent.parent / "src" / "json" / sub_dir
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Pipeline de Extração - Tormenta 20")
    print(f"{'='*60}")
    print(f"PDF: {pdf_path}")
    print(f"Seção: {section}")
    print(f"Tipo: {entity_type}")
    print(f"Livro ID: {livro_id}")
    print(f"Modelo: {model}")
    print(f"Saída: {output_path}")
    print(f"{'='*60}\n")

    # Extrair entidades
    print("Extraindo entidades do PDF...")
    try:
        entities = extract_entities(pdf_path, section, entity_type)
    except ValueError as e:
        print(f"Erro: {e}")
        print("\nListando seções disponíveis...")
        sections = list_available_sections(pdf_path, toc_start, toc_end)
        for slug, info in sections.items():
            print(f"  {slug}: {info['title']} (págs. {info['start_page']}-{info['end_page']})")
        sys.exit(1)

    stats["total"] = len(entities)
    print(f"Encontradas {len(entities)} entidades.\n")

    if dry_run:
        print("Modo dry-run: mostrando entidades encontradas")
        for entity in entities:
            page_info = f" (pág. {entity['page']})" if entity.get("page") else ""
            print(f"  - {entity['header']}{page_info}")
        return stats

    # Processar cada entidade
    print("Processando entidades...\n")
    for entity in tqdm(entities, desc="Processando"):
        header = entity["header"]
        content = entity["content"]
        page = entity.get("page")

        json_data, errors = process_entity(client, content, entity_type)

        if json_data:
            # Garantir que o ID está correto
            if "id" not in json_data or not json_data["id"]:
                json_data["id"] = slugify(header)

            if page is not None:
                json_data["page"] = page
            if livro_id:
                json_data["livro_id"] = livro_id

            # Salvar arquivo
            filename = f"{json_data['id']}.json"
            filepath = output_path / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            # Atualizar índice remissivo
            if update_index and page is not None:
                tabela = ENTITY_TYPE_TO_TABLE.get(entity_type, entity_type)
                termo = json_data.get("name") or header
                update_indice_remissivo(
                    livro_id=livro_id,
                    termo=termo,
                    pagina=page,
                    tabela=tabela,
                    registro_id=json_data["id"]
                )

            stats["success"] += 1
            page_str = f" (pág. {page})" if page else ""
            tqdm.write(f"✓ {header}{page_str} -> {filename}")
        else:
            stats["failed"] += 1
            stats["errors"].append({
                "entity": header,
                "errors": errors
            })
            tqdm.write(f"✗ {header}: {errors[-1] if errors else 'Erro desconhecido'}")

    # Relatório final
    print(f"\n{'='*60}")
    print("Relatório Final")
    print(f"{'='*60}")
    print(f"Total processado: {stats['total']}")
    print(f"Sucesso: {stats['success']}")
    print(f"Falhas: {stats['failed']}")

    if stats["errors"]:
        print(f"\nEntidades com erro:")
        for error in stats["errors"]:
            print(f"  - {error['entity']}")
            for e in error["errors"]:
                print(f"      {e}")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline de extração de dados do Tormenta 20",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Listar seções disponíveis no PDF
  python pipeline.py tormenta20.pdf --list-sections

  # Extrair todas as raças
  python pipeline.py tormenta20.pdf racas racas

  # Extrair classes usando modelo específico
  python pipeline.py tormenta20.pdf classes classes --model llama3

  # Dry-run para ver entidades e páginas sem processar
  python pipeline.py tormenta20.pdf magias magias --dry-run

Tipos de entidade disponíveis:
  racas, classes, origens, divindades, pericias, magias, poderes
        """
    )

    parser.add_argument("pdf_path", help="Caminho para o PDF do Tormenta 20")
    parser.add_argument("section", nargs="?", help="Seção do índice para extrair")
    parser.add_argument("entity_type", nargs="?", help="Tipo de entidade")

    parser.add_argument("--model", "-m", default=DEFAULT_MODEL,
                        help=f"Modelo LLM a usar (padrão: {DEFAULT_MODEL})")
    parser.add_argument("--output-dir", "-o",
                        help="Diretório de saída para os JSONs")
    parser.add_argument("--livro-id", default="t20_eja",
                        help="ID do livro no banco de dados (padrão: t20_eja)")
    parser.add_argument("--no-update-index", action="store_true",
                        help="Não atualiza o arquivo src/json/indice_remissivo/<livro_id>.json")
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="Não processa, apenas mostra entidades encontradas")
    parser.add_argument("--list-sections", "-l", action="store_true",
                        help="Lista seções disponíveis no PDF")
    parser.add_argument("--toc-start", type=int, default=3,
                        help="Página inicial do índice (padrão: 3)")
    parser.add_argument("--toc-end", type=int, default=6,
                        help="Página final do índice (padrão: 6)")

    args = parser.parse_args()

    if args.list_sections:
        sections = list_available_sections(args.pdf_path, args.toc_start, args.toc_end)
        print("\nSeções disponíveis:")
        print("=" * 60)
        for slug, info in sections.items():
            print(f"{slug}: {info['title']} (págs. {info['start_page']}-{info['end_page']})")
        sys.exit(0)

    if not args.section or not args.entity_type:
        parser.print_help()
        print("\nErro: section e entity_type são obrigatórios")
        sys.exit(1)

    run_pipeline(
        pdf_path=args.pdf_path,
        section=args.section,
        entity_type=args.entity_type,
        model=args.model,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
        toc_start=args.toc_start,
        toc_end=args.toc_end,
        livro_id=args.livro_id,
        update_index=not args.no_update_index
    )


if __name__ == "__main__":
    main()
