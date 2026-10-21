import Database from "better-sqlite3"
import { readdirSync, readFileSync, statSync } from "fs"
import { join, dirname, basename } from "path"
import { fileURLToPath } from "url"

const __dirname = dirname(fileURLToPath(import.meta.url))
const JSON_DIR = join(__dirname, "../../src/json")
const DB_PATH = process.env.TORMENTA20_DB_PATH ?? join(__dirname, "../../db/tormenta20.sqlite3")
const SCHEMA_PATH = join(__dirname, "../../db/schema.sql")

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf-8")) as T
}

function loadJsonFiles<T>(dir: string): T[] {
  const results: T[] = []
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry)
    if (statSync(full).isDirectory()) {
      results.push(...loadJsonFiles<T>(full))
    } else if (entry.endsWith(".json")) {
      const parsed = readJson<T>(full)
      if (parsed && typeof parsed === "object" && "id" in (parsed as object) && (parsed as Record<string, unknown>).id !== "") {
        results.push(parsed)
      }
    }
  }
  return results
}

function loadJsonDir<T>(dir: string): T[] {
  return readdirSync(dir)
    .filter((f) => f.endsWith(".json"))
    .map((f) => readJson<T>(join(dir, f)))
    .filter((p) => (p as Record<string, unknown>).id !== "")
}

function listJsonFiles(dir: string): string[] {
  const results: string[] = []
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry)
    if (statSync(full).isDirectory()) {
      results.push(...listJsonFiles(full))
    } else if (entry.endsWith(".json")) {
      results.push(full)
    }
  }
  return results.sort()
}

function findNeedsReview(value: unknown, path: string, out: string[]): void {
  if (Array.isArray(value)) {
    value.forEach((v, i) => findNeedsReview(v, `${path}[${i}]`, out))
  } else if (value && typeof value === "object") {
    for (const [k, v] of Object.entries(value)) {
      if (k === "needs_review" && v !== null && v !== false) out.push(path)
      else findNeedsReview(v, path ? `${path}.${k}` : k, out)
    }
  }
}

// Refuses to seed when any JSON file still carries a `needs_review` flag.
// Remove the flag (after fixing the data) or delete the file before building.
function assertNoNeedsReview(): void {
  const flagged: string[] = []
  for (const file of listJsonFiles(JSON_DIR)) {
    try {
      const paths: string[] = []
      findNeedsReview(readJson<unknown>(file), "$", paths)
      for (const p of paths) flagged.push(`${file.replace(`${JSON_DIR}/`, "")} at ${p}`)
    } catch (e) {
      flagged.push(`${file.replace(`${JSON_DIR}/`, "")} (unparseable: ${(e as Error).message})`)
    }
  }
  if (flagged.length > 0) {
    console.error(`Refusing to seed: ${flagged.length} file(s) still need review:`)
    for (const f of flagged) console.error(`  - ${f}`)
    throw new Error("needs_review flags present; fix the data and remove the flags before building")
  }
}

// Mirrors Ruby `bin/build_db`'s `register_indice_remissivo`. Any entity whose
// JSON carries a `page` (or `pagina`) is auto-registered in the remissive
// index, so the TS seeder produces the same `indice_remissivo` table as Ruby.
export function registerIndiceRemissivo(
  db: Database.Database,
  data: Record<string, unknown>,
  table: string,
): void {
  const page = data.page ?? data.pagina
  if (page == null) return

  const livroId = (data.livro_id ?? data.book_id ?? "t20_eja") as string
  const termo = (data.name ?? data.id) as string
  const stmt = db.prepare(
    `INSERT INTO indice_remissivo (livro_id, termo, pagina, tabela, registro_id)
     VALUES (?, ?, ?, ?, ?)
     ON CONFLICT(livro_id, termo, pagina) DO UPDATE SET
       tabela = excluded.tabela,
       registro_id = excluded.registro_id`,
  )
  stmt.run(livroId, termo, Number(page), table, (data.id as string) ?? null)
}

export function seed(): void {
  assertNoNeedsReview()
  const db = new Database(DB_PATH)
  db.pragma("journal_mode = WAL")
  db.pragma("foreign_keys = OFF")

  const schema = readFileSync(SCHEMA_PATH, "utf-8")
  db.exec(schema)

  const insert = db.transaction((table: string, rows: Record<string, unknown>[]) => {
    if (rows.length === 0) return
    const keys = Object.keys(rows[0])
    const cols = keys.join(", ")
    const vals = keys.map(() => "?").join(", ")
    const stmt = db.prepare(`INSERT OR REPLACE INTO ${table} (${cols}) VALUES (${vals})`)
    for (const row of rows) stmt.run(...keys.map((k) => {
      const v = row[k]
      return typeof v === "object" && v !== null ? JSON.stringify(v) : v
    }))
  })

  seedRacas(db, insert)
  seedOrigens(db, insert)
  seedDivindades(db, insert)
  seedClasses(db, insert)
  seedPoderes(db, insert)
  seedMagias(db, insert)
  seedEquipamentos(db, insert)
  seedItensSuperiores(db, insert)
  seedCondicoes(db, insert)
  seedPericias(db, insert)
  seedRegras(db, insert)
  seedTabelas(db, insert)
  seedLivros(db, insert)
  seedItensmagicos(db, insert)
  seedIndiceRemissivo()

  db.pragma("foreign_keys = ON")
  db.close()
  console.log("✓ Tormenta 20 database seeded successfully")
}

function seedRacas(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  const racas = loadJsonDir<Record<string, unknown>>(join(JSON_DIR, "racas"))
  insert("racas", racas.map((r) => ({
    id: r.id, name: r.name, description: r.description ?? null,
    size: r.size, movement: r.movement, vision: r.vision ?? "normal",
    vision_range: r.vision_range ?? null,
    attribute_bonuses: r.attribute_bonuses ?? {}, skill_bonuses: r.skill_bonuses ?? [],
    racial_abilities: r.racial_abilities ?? [],
    chosen_abilities_amount: r.chosen_abilities_amount ?? 0,
    available_chosen_abilities: r.available_chosen_abilities ?? [],
    page: r.page ?? null, livro_id: r.livro_id ?? null,
    longevidade: r.longevidade ?? null, devotos: r.devotos ?? [],
  })))
  racas.forEach((r) => registerIndiceRemissivo(db, r, "racas"))
}

function seedOrigens(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  const origens = loadJsonDir<Record<string, unknown>>(join(JSON_DIR, "origens"))
  insert("origens", origens.map((o) => ({
    id: o.id, name: o.name, description: o.description ?? null,
    items: o.items ?? [], benefits: o.benefits ?? {}, unique_power: o.unique_power ?? null,
  })))
  origens.forEach((o) => registerIndiceRemissivo(db, o, "origens"))
}

function seedDivindades(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  const divs = loadJsonDir<Record<string, unknown>>(join(JSON_DIR, "deuses"))
  insert("divindades", divs.map((d) => ({
    id: d.id, name: d.name, title: d.title ?? null, description: d.description ?? null,
    beliefs_objectives: d.beliefs_objectives ?? [], holy_symbol: d.holy_symbol ?? null,
    energy: d.energy ?? "qualquer", preferred_weapon: d.preferred_weapon ?? null,
    devotees: d.devotees ?? {}, granted_powers: d.granted_powers ?? [],
    obligations_restrictions: d.obligations_restrictions ?? null,
  })))
  divs.forEach((d) => registerIndiceRemissivo(db, d, "divindades"))
}

function seedClasses(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  const classes = loadJsonDir<Record<string, unknown>>(join(JSON_DIR, "classes"))
  insert("classes", classes.map((c) => ({
    id: c.id, name: c.name,
    hit_points: c.hit_points ?? {}, mana_points: c.mana_points ?? {},
    skills: c.skills ?? {}, proficiencies: c.proficiencies ?? {},
    abilities: c.abilities ?? [], powers: c.powers ?? [],
    progression: c.progression ?? [],
    spellcasting: c.spellcasting && Object.keys(c.spellcasting as object).length > 0 ? c.spellcasting : null,
  })))
  classes.forEach((c) => registerIndiceRemissivo(db, c, "classes"))
}

const PODER_DIR_TYPE_MAP: Record<string, string> = {
  habilidades_de_raca: "habilidade_de_raca",
  habilidades_unicas_de_origem: "habilidade_unica_origem",
  poderes_concedidos: "poder_concedido",
  poderes_da_tormenta: "poder_tormenta",
  poderes_de_combate: "poder_combate",
  poderes_de_destino: "poder_destino",
  poderes_de_magia: "poder_magia",
}

function seedPoderes(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  const poderesDir = join(JSON_DIR, "poderes")
  const rows: Record<string, unknown>[] = []
  const originals: Record<string, unknown>[] = []

  for (const topDir of readdirSync(poderesDir)) {
    const topPath = join(poderesDir, topDir)
    if (!statSync(topPath).isDirectory()) continue

    if (topDir === "poderes_gerais") {
      for (const subDir of readdirSync(topPath)) {
        const subPath = join(topPath, subDir)
        if (!statSync(subPath).isDirectory()) continue
        const type = PODER_DIR_TYPE_MAP[subDir] ?? "poder_geral"
        const files = loadJsonFiles<Record<string, unknown>>(subPath)
        rows.push(...files.map((p) => mapPoder(p, type, null, null)))
        originals.push(...files)
      }
      continue
    }

    if (topDir === "habilidades_de_classe") {
      for (const classDir of readdirSync(topPath)) {
        const classPath = join(topPath, classDir)
        if (!statSync(classPath).isDirectory()) continue
        const files = loadJsonDir<Record<string, unknown>>(classPath)
        rows.push(...files.map((p) => mapPoder(p, "poder_classe", null, classDir)))
        originals.push(...files)
      }
      continue
    }

    const type = PODER_DIR_TYPE_MAP[topDir] ?? "poder_geral"

    if (topDir === "habilidades_de_raca") {
      for (const subDir of readdirSync(topPath)) {
        const subPath = join(topPath, subDir)
        if (statSync(subPath).isDirectory()) {
          const files = loadJsonDir<Record<string, unknown>>(subPath)
          rows.push(...files.map((p) => mapPoder(p, type, null, null)))
          originals.push(...files)
        } else if (subDir.endsWith(".json")) {
          const p = readJson<Record<string, unknown>>(subPath)
          if ((p.id as string) !== "") {
            rows.push(mapPoder(p, type, null, null))
            originals.push(p)
          }
        }
      }
      continue
    }

    if (topDir === "habilidades_unicas_de_origem") {
      const files = loadJsonDir<Record<string, unknown>>(topPath)
      rows.push(...files.map((p) => mapPoder(p, type, (p.origin as string) ?? null, null)))
      originals.push(...files)
      continue
    }

    const files = loadJsonFiles<Record<string, unknown>>(topPath)
    rows.push(...files.map((p) => mapPoder(p, type, null, null)))
    originals.push(...files)
  }

  insert("poderes", rows)
  originals.forEach((p) => registerIndiceRemissivo(db, p, "poderes"))
}

function mapPoder(p: Record<string, unknown>, type: string, originId: string | null, classId: string | null): Record<string, unknown> {
  return {
    id: p.id, name: p.name, type,
    description: p.description ?? null,
    effects: p.effects ?? [], costs: p.costs ?? [],
    prerequisites: p.requirements ?? p.prerequisites ?? [],
    origin_id: originId, class_id: classId,
    deities: p.deities ?? [],
  }
}

function seedMagias(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  const magias = loadJsonDir<Record<string, unknown>>(join(JSON_DIR, "magias"))
  insert("magias", magias.map((m) => {
    const target = Array.isArray(m.target) ? m.target[0] : (m.target as Record<string, unknown> | null)
    return {
      id: m.id, name: m.name, type: m.type, circle: m.circle, school: m.school,
      execution: m.execution, execution_details: m.execution_details ?? null,
      range: m.range, duration: m.duration, duration_details: m.duration_details ?? null,
      counterspell: m.counterspell ?? null, description: m.description,
      target_amount: target?.amount ?? null,
      target_up_to: target?.up_to ? 1 : 0,
      target_type: target?.type ?? null,
      effect: m.effect ?? null, effect_shape: null, effect_dimension: null,
      effect_size: null, effect_other_details: m.effect_details ?? null,
      area_effect: null, area_effect_details: null,
      resistance_effect: (m.resistance as Record<string, unknown>)?.effect ?? null,
      resistance_skill: (m.resistance as Record<string, unknown>)?.skill ?? null,
      extra_costs_material_component: null, extra_costs_material_cost: null,
      extra_costs_pm_debuff: null, extra_costs_pm_sacrifice: null,
      enhancements: m.enhancements ?? [], effects: m.effects ?? [],
    }
  }))
  magias.forEach((m) => registerIndiceRemissivo(db, m, "magias"))
}

const ARMA_CATEGORY_MAP: Record<string, string> = {
  simples: "simples",
  marcial: "marciais",
  exotica: "exoticas",
  fogo: "fogo",
}

// Pure JSON→row mappers, exported so specs can assert the transform without
// running the destructive seeder against a real database.
export type RecordArmaRow = Record<string, unknown>
export type RecordItemRow = Record<string, unknown>
export type RecordMelhoriaRow = Record<string, unknown>

export function mapArma(a: Record<string, unknown>): RecordArmaRow {
  // Ruby `bin/build_db` merges `habilidades` and `especial` into `properties`
  // via `[data["habilidades"], data["especial"]].flatten.compact`.
  const properties = [a.habilidades, a.especial].flat().filter(Boolean)
  return {
    id: a.id, name: a.name,
    category: ARMA_CATEGORY_MAP[a.proficiencia as string] ?? a.proficiencia,
    price: a.preco ?? 0,
    damage: a.dano ?? null,
    damage_type: a.tipo_dano ?? null,
    critical: a.critico ?? null,
    range: a.alcance === "corpo_a_corpo" || !a.alcance ? null : a.alcance,
    weight: a.espacos ?? 0,
    properties,
    description: a.description ?? null,
  }
}

export function mapItem(i: Record<string, unknown>): RecordItemRow {
  // `efeito` is the house style for 86 of ~165 item files; `effects` is the DB
  // column name. Prefer the primary `effects` key when present, else fall back
  // to `efeito` (which otherwise gets dropped).
  const effects: Record<string, unknown> =
    (i.effects as Record<string, unknown> | undefined) ??
    (i.efeito as Record<string, unknown> | undefined) ??
    {}
  // Animal partner blocks (parceiro, besta_de_carga, alternativo, restricoes,
  // isento_restricao_cavalgar_combate) live in JSON but only become queryable
  // via the DB if we copy them into the effects JSON column here.
  if (i.parceiro !== undefined) effects.parceiro = i.parceiro
  if (i.besta_de_carga !== undefined) effects.besta_de_carga = i.besta_de_carga
  if (i.alternativo !== undefined) effects.alternativo = i.alternativo
  if (i.restricoes !== undefined) effects.restricoes = i.restricoes
  if (i.isento_restricao_cavalgar_combate === true) {
    effects.isento_restricao_cavalgar_combate = true
  }
  return {
    id: i.id, name: i.name, category: i.category ?? null,
    price: i.preco ?? i.price ?? 0,
    weight: i.espacos ?? i.weight ?? 0,
    description: i.description ?? null,
    effects,
  }
}

export function mapMelhoria(m: Record<string, unknown>): RecordMelhoriaRow {
  // Ruby `bin/build_db` reads `data["efeito"] || data["effects"] || {}`.
  return {
    id: m.id, name: m.name, description: m.description ?? null,
    applicable_to: m.applicable_to ?? [], price: m.price ?? 0,
    effects: (m.efeito ?? m.effects ?? {}) as Record<string, unknown>,
  }
}

function seedEquipamentos(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  const eqDir = join(JSON_DIR, "equipamentos")

  const armas = loadJsonFiles<Record<string, unknown>>(join(eqDir, "armas"))
  insert("armas", armas.map(mapArma))
  armas.forEach((a) => registerIndiceRemissivo(db, a, "armas"))

  const armaduras = loadJsonFiles<Record<string, unknown>>(join(eqDir, "armaduras"))
  insert("armaduras", armaduras.map((a) => ({
    id: a.id, name: a.name, category: a.categoria ?? a.category,
    price: a.preco ?? a.price ?? 0,
    defense_bonus: a.bonus_defesa ?? a.defense_bonus ?? 0,
    armor_penalty: a.penalidade ?? a.armor_penalty ?? 0,
    weight: a.espacos ?? a.weight ?? 0,
    properties: a.habilidades ?? a.properties ?? [],
    description: a.description ?? null,
  })))
  armaduras.forEach((a) => registerIndiceRemissivo(db, a, "armaduras"))

  const escudos = loadJsonFiles<Record<string, unknown>>(join(eqDir, "escudos"))
  insert("escudos", escudos.map((e) => ({
    id: e.id, name: e.name,
    price: e.preco ?? e.price ?? 0,
    defense_bonus: e.bonus_defesa ?? e.defense_bonus ?? 0,
    armor_penalty: e.penalidade ?? e.armor_penalty ?? 0,
    weight: e.espacos ?? e.weight ?? 0,
    properties: e.habilidades ?? e.properties ?? [],
    description: e.description ?? null,
  })))
  escudos.forEach((e) => registerIndiceRemissivo(db, e, "escudos"))

  const itens = loadJsonFiles<Record<string, unknown>>(join(eqDir, "itens"))
  insert("itens", itens.map(mapItem))
  itens.forEach((i) => registerIndiceRemissivo(db, i, "itens"))
}

function seedItensSuperiores(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  const dir = join(JSON_DIR, "itens_superiores")

  const materiais = loadJsonDir<Record<string, unknown>>(join(dir, "materiais_especiais"))
  insert("materiais_especiais", materiais.map((m) => ({
    id: m.id, name: m.name, description: m.description ?? null,
    applicable_to: m.applicable_to ?? [], price_modifier: m.precos_adicionais ?? m.price_modifier ?? {},
    effects: m.efeitos ?? m.effects ?? {},
  })))
  materiais.forEach((m) => registerIndiceRemissivo(db, m, "materiais_especiais"))

  const melhorias = loadJsonFiles<Record<string, unknown>>(join(dir, "melhorias"))
  insert("melhorias", melhorias.map(mapMelhoria))
  melhorias.forEach((m) => registerIndiceRemissivo(db, m, "melhorias"))

  const encantamentos = loadJsonFiles<Record<string, unknown>>(join(dir, "encantamentos"))
  insert("encantamentos", encantamentos.map((e) => ({
    id: e.id, name: e.name, description: e.description ?? null,
    categoria: e.categoria ?? "arma",
    escudo_only: e.escudo_only ? 1 : 0,
    conta_como_dois: e.conta_como_dois ? 1 : 0,
    prerequisitos: e.prerequisitos ?? [],
    efeito: e.efeito ?? {},
  })))
  encantamentos.forEach((e) => registerIndiceRemissivo(db, e, "encantamentos"))
}

function seedCondicoes(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  const condicoes = loadJsonDir<Record<string, unknown>>(join(JSON_DIR, "condicoes"))
  insert("condicoes", condicoes.map((c) => ({
    id: c.id, name: c.name, description: c.description ?? null,
    effects: c.effects ?? [], condition_type: c.condition_type ?? c.tipo ?? null,
    escalates_to: c.escalates_to ?? null,
  })))
  condicoes.forEach((c) => registerIndiceRemissivo(db, c, "condicoes"))
}

function seedPericias(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  const pericias = loadJsonDir<Record<string, unknown>>(join(JSON_DIR, "pericias"))
  insert("pericias", pericias.map((p) => ({
    id: p.id, name: p.name, atributo: p.atributo,
    trained_only: p.trained_only ? 1 : 0,
    armor_penalty: p.armor_penalty ? 1 : 0,
    resistance_skill: p.resistance_skill ? 1 : 0,
    description: p.description ?? null, uses: p.uses ?? [],
  })))
  pericias.forEach((p) => registerIndiceRemissivo(db, p, "pericias"))
}

function seedRegras(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  if (!existsDir(join(JSON_DIR, "regras"))) return
  const regras = loadJsonDir<Record<string, unknown>>(join(JSON_DIR, "regras"))
  insert("regras", regras.map((r) => {
    const { id, name, description, ...rest } = r
    return { id, name, description: description ?? null, data: rest }
  }))
  // Ruby's `seed_regras` transform moves everything except id/name/description
  // into `data`, so `register_indice_remissivo` never sees a top-level `page`
  // and skips regras. We mirror that observed behaviour (no registration).
}

function seedTabelas(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  if (!existsDir(join(JSON_DIR, "tabelas"))) return
  const tabelas = loadJsonDir<Record<string, unknown>>(join(JSON_DIR, "tabelas"))
  insert("tabelas", tabelas.map((t) => ({
    id: t.id, name: t.name, description: t.description ?? null,
    headers: t.headers ?? [],
    rows: t.rows ?? [],
  })))
  tabelas.forEach((t) => registerIndiceRemissivo(db, t, "tabelas"))
}

function seedLivros(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  if (!existsDir(join(JSON_DIR, "livros"))) return
  const livros = loadJsonDir<Record<string, unknown>>(join(JSON_DIR, "livros"))
  insert("livros", livros.map((l) => ({
    id: l.id, nome: l.nome, nome_curto: l.nome_curto,
  })))
  livros.forEach((l) => registerIndiceRemissivo(db, l, "livros"))
}

function seedItensmagicos(db: Database.Database, insert: ReturnType<typeof Database.prototype.transaction>): void {
  const base = join(JSON_DIR, "itens_magicos")

  if (existsDir(join(base, "pocoes"))) {
    const pocoes = loadJsonDir<Record<string, unknown>>(join(base, "pocoes"))
    insert("pocoes", pocoes.map((p) => ({
      id: p.id, name: p.name, subtipo: p.subtipo, spell_id: p.spell_id,
      pm_cost: p.pm_cost, categoria: p.categoria, preco: p.preco ?? null,
      roll_min: p.roll_min ?? null, roll_max: p.roll_max ?? null,
      aprimoramento: p.aprimoramento ?? null, description: p.description ?? null,
    })))
    pocoes.forEach((p) => registerIndiceRemissivo(db, p, "pocoes"))
  }

  if (existsDir(join(base, "acessorios"))) {
    const acessorios = loadJsonDir<Record<string, unknown>>(join(base, "acessorios"))
    insert("acessorios_magicos", acessorios.map((a) => ({
      id: a.id, name: a.name, categoria: a.categoria, preco: a.preco ?? null,
      roll_min: a.roll_min ?? null, roll_max: a.roll_max ?? null,
      description: a.description ?? null, efeito: a.efeito ?? {},
    })))
    acessorios.forEach((a) => registerIndiceRemissivo(db, a, "acessorios_magicos"))
  }
}

function seedIndiceRemissivo(): void {
  if (!existsDir(join(JSON_DIR, "indice_remissivo"))) return
  const rows: Record<string, unknown>[] = []

  for (const file of readdirSync(join(JSON_DIR, "indice_remissivo"))) {
    if (!file.endsWith(".json")) continue
    const livroId = file.replace(".json", "")
    const entries = JSON.parse(readFileSync(join(JSON_DIR, "indice_remissivo", file), "utf-8")) as Record<string, unknown>[]
    if (!Array.isArray(entries)) continue
    for (const e of entries) {
      if (!e.termo || !e.pagina) continue
      rows.push({
        livro_id: livroId,
        termo: e.termo,
        pagina: Number(e.pagina),
        tabela: e.tabela ?? null,
        registro_id: e.registro_id ?? null,
      })
    }
  }

  if (rows.length === 0) return
  const db2 = new Database(DB_PATH)
  const stmt = db2.prepare("INSERT OR REPLACE INTO indice_remissivo (livro_id, termo, pagina, tabela, registro_id) VALUES (?, ?, ?, ?, ?)")
  const run = db2.transaction(() => {
    for (const r of rows) stmt.run(r.livro_id, r.termo, r.pagina, r.tabela, r.registro_id)
  })
  run()
  db2.close()
}

function existsDir(path: string): boolean {
  try { return statSync(path).isDirectory() } catch { return false }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  seed()
}
