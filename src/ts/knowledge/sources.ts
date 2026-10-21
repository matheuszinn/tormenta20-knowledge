import type { BookReference } from "../models/concerns/book_referenceable.js";
import type { SourceReference } from "./types.js";

/**
 * Converts the internal `BookReference` (Portuguese-named fields, internal to
 * the models) to the public `SourceReference` shape (English-named fields per
 * SPEC §5.1).
 */
export function toSourceReference(ref: BookReference): SourceReference {
  return {
    bookId: ref.bookId,
    bookName: ref.livro,
    bookAbbreviation: ref.bookAbbreviation,
    page: ref.pagina,
    formatted: ref.formatted,
  };
}

/**
 * Converts a list of internal references to public source references.
 *
 * Empty input yields empty output, preserving the "no source" case explicitly
 * (never fabricating a source).
 */
export function toSourceReferences(refs: BookReference[]): SourceReference[] {
  return refs.map(toSourceReference);
}
