/**
 * @packageDocumentation
 *
 * Knowledge Engine — types and adapters for querying the Tormenta20 base.
 *
 * Etapa 1 of the SPEC: foundation only. No search logic yet (that's Etapa 2).
 *
 * @example
 * ```ts
 * import { Arma } from "tormenta20"
 * import { toSearchResult } from "tormenta20/knowledge"
 *
 * const adaga = Arma.find("adaga")!
 * const sr = toSearchResult(adaga, "armas")
 * // => { id: "adaga", type: "arma", name: "Adaga", sources: [...], matchedBy: [] }
 * ```
 */
export type {
  EntityType,
  SourceReference,
  MatchChannel,
  SearchResult,
  SearchOptions,
  SearchResponse,
  GetEntityOptions,
} from "./types.js";

export { toSourceReference, toSourceReferences } from "./sources.js";

export {
  entityTypeFor,
  toSearchResult,
  TABLE_TO_ENTITY_TYPE,
  type KnowledgeModelLike,
} from "./entity.js";
