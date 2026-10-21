#!/usr/bin/env -S npx tsx
/**
 * Validation script for Etapa 1 (src/ts/knowledge/).
 *
 * Usage:
 *   tsx scripts/validate-etapa1.ts                # runs the default demo set
 *   tsx scripts/validate-etapa1.ts get <id> <table>   # arbitrary lookup
 *
 * The demo set exercises:
 *   - Singular source (adaga, allihanna)
 *   - Multi-source across books (espinhosa, amuleto_da_robustez)
 *   - Tabela collision: same id in magias vs pocoes (bola_de_fogo)
 *   - Type guard refusal (indice_remissivo, livros)
 *   - Description handling (null, empty, missing)
 */

import {
  Knowledge,
  Arma,
  Armadura,
  Divindade,
  Encantamento,
  Escudo,
  Item,
  Magia,
  Melhoria,
  Pericia,
  Pocao,
  Raca,
  Regra,
  Tabela,
  AcessorioMagico,
  database,
} from "../src/ts/index.js"

// ── Helpers ─────────────────────────────────────────────────────────────────────

interface ModelCtor {
  find(id: string): unknown
  readonly TABLE: string
}

const TABLE_TO_CTOR: Record<string, ModelCtor> = {
  armas: Arma as unknown as ModelCtor,
  armaduras: Armadura as unknown as ModelCtor,
  escudos: Escudo as unknown as ModelCtor,
  itens: Item as unknown as ModelCtor,
  melhorias: Melhoria as unknown as ModelCtor,
  encantamentos: Encantamento as unknown as ModelCtor,
  magias: Magia as unknown as ModelCtor,
  racas: Raca as unknown as ModelCtor,
  divindades: Divindade as unknown as ModelCtor,
  pericias: Pericia as unknown as ModelCtor,
  pocoes: Pocao as unknown as ModelCtor,
  regras: Regra as unknown as ModelCtor,
  tabelas: Tabela as unknown as ModelCtor,
  acessorios_magicos: AcessorioMagico as unknown as ModelCtor,
}

function header(title: string): void {
  console.log("\n" + "─".repeat(72))
  console.log(`  ${title}`)
  console.log("─".repeat(72))
}

function show(label: string, value: unknown): void {
  console.log(`\n${label}`)
  console.log(JSON.stringify(value, null, 2))
}

function lookupAndShow(id: string, table: string): void {
  const ctor = TABLE_TO_CTOR[table]
  if (!ctor) {
    console.log(`\n✗ ${table} is not a known entity table (try: ${Object.keys(TABLE_TO_CTOR).join(", ")})`)
    return
  }
  const instance = ctor.find(id)
  if (!instance) {
    console.log(`\n✗ ${table}#${id} not found`)
    return
  }
  try {
    const sr = Knowledge.toSearchResult(
      instance as unknown as Knowledge.KnowledgeModelLike,
      table,
    )
    show(`${table}#${id} →`, sr)
  } catch (err) {
    console.log(`\n✗ ${table}#${id} raised: ${(err as Error).message}`)
  }
}

function typeGuard(label: string, table: string): void {
  const result = Knowledge.entityTypeFor(table)
  console.log(`  ${label.padEnd(40)} → ${result === null ? "null (rejected)" : JSON.stringify(result)}`)
}

// ── Demo ───────────────────────────────────────────────────────────────────────

function runDemo(): void {
  console.log("\n" + "═".repeat(72))
  console.log("  Knowledge Engine — Etapa 1 validation")
  console.log("═".repeat(72))
  console.log(`  DB: ${database.mode}`)
  console.log(`  tables indexed in indice_remissivo: see sqlite3 db/tormenta20.sqlite3`)

  // 1. Singular source
  header("1. Singular source (one book, one page)")
  lookupAndShow("adaga", "armas")
  lookupAndShow("allihanna", "divindades")

  // 2. Multi-source across books
  header("2. Multi-source across books")
  lookupAndShow("espinhosa", "melhorias")
  lookupAndShow("amuleto_da_robustez", "acessorios_magicos")

  // 3. Tabela collision (same id in different tables)
  header("3. Tabela collision — same id, different tables")
  lookupAndShow("bola_de_fogo", "magias")
  lookupAndShow("bola_de_fogo", "pocoes")

  // 4. Type guard refusals
  header("4. Type guard — entityTypeFor() refusals")
  typeGuard("armas", "armas")
  typeGuard("acessorios_magicos", "acessorios_magicos")
  typeGuard("indice_remissivo (metadata)", "indice_remissivo")
  typeGuard("livros (sourcebook)", "livros")
  typeGuard("unknown_table", "unknown_table")

  // 5. toSearchResult refusal
  header("5. toSearchResult refusal")
  try {
    Knowledge.toSearchResult(
      { id: "x", name: "X", bookReferences: () => [] },
      "indice_remissivo",
    )
    console.log("  ✗ Expected TypeError, got nothing")
  } catch (err) {
    console.log(`  ✓ Raised as expected: ${(err as Error).message}`)
  }

  // 6. Description handling
  header("6. Description handling")
  const pocaoBolaFogo = Pocao.find("bola_de_fogo") as unknown as
    | Knowledge.KnowledgeModelLike
    | null
  if (pocaoBolaFogo) {
    const sr = Knowledge.toSearchResult(pocaoBolaFogo, "pocoes")
    console.log(`  pocao#bola_de_fogo.description present?  ${"description" in sr ? "yes" : "no"}`)
    if ("description" in sr) {
      console.log(`    → "${(sr.description ?? "").slice(0, 60)}..."`)
    }
  }

  console.log("\n" + "═".repeat(72))
  console.log("  Done. Compare the JSON shape against SPEC §5.1 (SourceReference,")
  console.log("  SearchResult) and §11 (Etapa 1 deliverables).")
  console.log("═".repeat(72) + "\n")
}

// ── CLI ────────────────────────────────────────────────────────────────────────

function main(): void {
  const args = process.argv.slice(2)
  if (args[0] === "get" && args[1] && args[2]) {
    lookupAndShow(args[1], args[2])
  } else if (args[0] === "type" && args[1]) {
    console.log(JSON.stringify(Knowledge.entityTypeFor(args[1]), null, 2))
  } else if (args.length === 0) {
    runDemo()
  } else {
    console.error("Usage:")
    console.error("  tsx scripts/validate-etapa1.ts                          # demo set")
    console.error("  tsx scripts/validate-etapa1.ts get <id> <table>        # arbitrary lookup")
    console.error("  tsx scripts/validate-etapa1.ts type <table>")
    process.exit(1)
  }
}

main()