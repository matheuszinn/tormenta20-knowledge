/**
 * Public types for the Knowledge Engine — querying the Tormenta20 base.
 *
 * These mirror SPEC §5.1 but are the authoritative surface for the TypeScript
 * package. A few entity types not present in the SPEC are included here:
 * `pericia`, `tabela` and `acessorio_magico` (each backed by its own table).
 */

/**
 * The kinds of entities the knowledge base can return.
 *
 * `criatura` and `npc` are reserved for a future extension (Etapa 0.5 of the
 * SPEC was cancelled — see `docs/knowledge-query.md`). They are accepted here
 * for forward compatibility but will not appear in results today.
 *
 * `pericia`, `tabela` and `acessorio_magico` are not enumerated in the SPEC
 * §5.1 union but are real tables in the database with public `EntityType`s.
 */
export type EntityType =
  | "arma"
  | "armadura"
  | "escudo"
  | "item"
  | "melhoria"
  | "encantamento"
  | "material_especial"
  | "pocao"
  | "acessorio_magico"
  | "magia"
  | "poder"
  | "classe"
  | "origem"
  | "raca"
  | "divindade"
  | "condicao"
  | "regra"
  | "pericia"
  | "tabela"
  | "criatura" // reserved — Etapa 0.5 cancelled
  | "npc"; // reserved — Etapa 0.5 cancelled

/**
 * A single place where an entity appears: a book and page.
 *
 * Provenance rule: a `SourceReference` must come from an existing index entry
 * (`indice_remissivo` joined to `livros`). Pages are never inferred. Every
 * optional field is only present when the source data provides it — do not
 * invent a book name, abbreviation, page or URL.
 */
export interface SourceReference {
  /** `livros.id`, e.g. `"t20_eja"` or `"ameacas_de_arton"`. */
  bookId?: string;
  /** Full book name, e.g. `"Tormenta 20 - Edição Jogo do Ano"`. */
  bookName?: string;
  /** Short book abbreviation, e.g. `"T20 - EJA"`. */
  bookAbbreviation?: string;
  /** Printed page number. */
  page?: number;
  /** Human-readable label, e.g. `"T20 - EJA, p. 56"`. */
  formatted?: string;
  /** Optional canonical link to the source, when one exists. */
  url?: string;
}

/**
 * The channel through which a query matched an entity.
 *
 * - `name` — the display name matched.
 * - `description` — the free-text description matched.
 * - `effect` — a structured effect/modifier field matched.
 * - `index` — the remissive index matched.
 * - `structured` — a structured column/filter matched.
 */
export type MatchChannel = "name" | "description" | "effect" | "index" | "structured";

/**
 * A single entity returned by a knowledge query.
 *
 * - `sources` lists **every** book+page where the entity appears; it is never
 *   inferred and may be empty when the entity has no index entry.
 * - `matchedBy` lists the channels that contributed to the match. Etapa 1
 *   (adapters) always leaves it empty; Etapa 2 (search) populates it.
 * - `score` is an internal ordering signal, **not** a probability of truth.
 *   Do not present it to users as such.
 * - `evidence` carries text snippets justifying each match. Etapa 2 populates
 *   it; it is unset by the adapters produced in Etapa 1.
 * - `description` is omitted entirely (not stored as an empty string) when the
 *   entity has no description.
 */
export interface SearchResult {
  id: string;
  type: EntityType;
  name: string;
  description?: string;
  sources: SourceReference[];
  matchedBy: MatchChannel[];
  score?: number;
  evidence?: string[];
}

/** Options for a general knowledge query. Etapa 2 consumes these. */
export interface SearchOptions {
  query: string;
  types?: EntityType[];
  limit?: number;
  bookIds?: string[];
  includeIndex?: boolean;
}

/** Response envelope for a general knowledge query. */
export interface SearchResponse {
  query: string;
  results: SearchResult[];
  total?: number;
}

/** Options for looking up a single entity by ID. */
export interface GetEntityOptions {
  id: string;
  type?: EntityType;
}
