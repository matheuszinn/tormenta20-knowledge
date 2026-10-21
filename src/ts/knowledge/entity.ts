import type { SearchResult, EntityType } from "./types.js";
import { toSourceReferences } from "./sources.js";
import type { BookReference } from "../models/concerns/book_referenceable.js";

/**
 * Minimum shape a TS model must expose to be turned into a `SearchResult`.
 *
 * All current TS models with `bookReferences()` (plural) satisfy this.
 * `description` is optional: some models (e.g. `classe`) expose no such getter,
 * and models with a nullable description may return `null`.
 */
export interface KnowledgeModelLike {
  readonly id: string;
  readonly name: string;
  readonly description?: string | null;
  bookReferences(): BookReference[];
}

/**
 * Maps a TS model table name to its public `EntityType`.
 *
 * One canonical mapping — keep in sync with the `EntityType` union in
 * `./types.ts`. `poderes` collapses every power subtype
 * (`poder_concedido`, `poder_tormenta`, `poder_geral`, …) to `poder`.
 */
export const TABLE_TO_ENTITY_TYPE: Readonly<Record<string, EntityType>> = Object.freeze({
  armas: "arma",
  armaduras: "armadura",
  escudos: "escudo",
  itens: "item",
  melhorias: "melhoria",
  encantamentos: "encantamento",
  materiais_especiais: "material_especial",
  pocoes: "pocao",
  acessorios_magicos: "acessorio_magico",
  magias: "magia",
  poderes: "poder",
  classes: "classe",
  origens: "origem",
  racas: "raca",
  divindades: "divindade",
  condicoes: "condicao",
  regras: "regra",
  pericias: "pericia",
  tabelas: "tabela",
});

/**
 * Tables that are not user-facing entities and must never be adapted into a
 * `SearchResult`.
 *
 * - `indice_remissivo` is metadata (the remissive index itself).
 * - `livros` is the sourcebook registry.
 */
const NON_ENTITY_TABLES: ReadonlySet<string> = new Set(["indice_remissivo", "livros"]);

/**
 * Resolves the public `EntityType` for a table name.
 *
 * @returns The matching `EntityType`, or `null` for metadata tables and
 *   unknown table names.
 */
export function entityTypeFor(tableName: string): EntityType | null {
  if (NON_ENTITY_TABLES.has(tableName)) return null;
  return TABLE_TO_ENTITY_TYPE[tableName] ?? null;
}

/**
 * Converts a TS model instance into a public `SearchResult`.
 *
 * `matchedBy` is left empty; `score` and `evidence` are unset. Etapa 2 (search)
 * populates these as the query matches the entity.
 *
 * `description` is omitted when `null`/empty (never stored as an empty string).
 * `sources` is always an array — possibly empty if the entity has no index
 * entry.
 *
 * @throws `TypeError` if the table name maps to no public `EntityType`
 *   (metadata table or unknown table).
 */
export function toSearchResult(model: KnowledgeModelLike, tableName: string): SearchResult {
  const type = entityTypeFor(tableName);
  if (type === null) {
    throw new TypeError(
      `Cannot map table "${tableName}" to an EntityType (metadata or unknown table).`
    );
  }
  const result: SearchResult = {
    id: model.id,
    type,
    name: model.name,
    sources: toSourceReferences(model.bookReferences()),
    matchedBy: [],
  };
  const description = model.description;
  if (typeof description === "string" && description.length > 0) {
    result.description = description;
  }
  return result;
}
