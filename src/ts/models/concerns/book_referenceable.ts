import { database } from "../../database.js"

/**
 * A resolved book reference — the page where a record appears in a T20 sourcebook.
 */
export interface BookReference {
  /** Full book name (e.g. `"Tormenta 20 - Edição Jogo do Ano"`). */
  livro: string
  /** Page number. */
  pagina: number
  /** Human-readable label, e.g. `"T20 - EJA, p. 56"`. */
  formatted: string
  /** `livros.id`, e.g. `"t20_eja"` or `"ameacas_de_arton"`. */
  bookId: string
  /** Short book abbreviation, e.g. `"T20 - EJA"` or `"T20 - Ameaças"`. */
  bookAbbreviation: string
}

/**
 * Looks up **every** book and page for a given record via the `indice_remissivo`
 * table.
 *
 * An entity can be indexed on multiple pages (and across multiple books). The
 * lookup is scoped by **both** `tabela` and `registro_id`, because the same
 * `registro_id` can appear in multiple tables (e.g. `"bola_de_fogo"` is both a
 * magia and a poção, indexed at different pages). Filtering by `tabela` prevents
 * returning wrong pages for such collisions.
 *
 * @param registroId - The record's string ID (e.g. `"espada_longa"`)
 * @param tabela - The table the record belongs to (e.g. `"armas"`)
 * @returns All `BookReference`s (ordered by `livro_id`, then `pagina`); an empty
 *   array if the record has no index entry
 *
 * @example
 * ```ts
 * const refs = getBookReferencesFor("espinhosa", "melhorias")
 * // => [{ livro: "...Ameaças...", pagina: 401, ... }, { livro: "...EJA...", pagina: 171, ... }]
 * ```
 */
export function getBookReferencesFor(registroId: string, tabela: string): BookReference[] {
  const rows = database.db
    .prepare(
      `SELECT ir.pagina, l.id AS book_id, l.nome, l.nome_curto
       FROM indice_remissivo ir
       JOIN livros l ON l.id = ir.livro_id
       WHERE ir.tabela = ? AND ir.registro_id = ?
       ORDER BY ir.livro_id, ir.pagina`
    )
    .all(tabela, registroId) as Array<{
      pagina: number
      book_id: string
      nome: string
      nome_curto: string
    }>

  return rows.map((row) => ({
    livro: row.nome,
    pagina: row.pagina,
    formatted: `${row.nome_curto}, p. ${row.pagina}`,
    bookId: row.book_id,
    bookAbbreviation: row.nome_curto,
  }))
}

/**
 * Looks up the first book and page for a given record via the
 * `indice_remissivo` table.
 *
 * Returns **the first match**; for the complete list use
 * {@link getBookReferencesFor}. The lookup is scoped by **both** `tabela` and
 * `registro_id`, because the same `registro_id` can appear in multiple tables
 * (e.g. `"bola_de_fogo"` is both a magia and a poção, indexed at different
 * pages). Filtering by `tabela` prevents returning the wrong page for such
 * collisions.
 *
 * The bare `getBookReference` name was removed (not kept as a shim) since every
 * caller now carries a `tabela` and calling without one is always a bug.
 *
 * @param registroId - The record's string ID (e.g. `"espada_longa"`)
 * @param tabela - The table the record belongs to (e.g. `"armas"`)
 * @returns The first `BookReference`, or `null` if the record has no index entry
 *
 * @example
 * ```ts
 * const ref = getBookReferenceFor("espada_longa", "armas")
 * // => { livro: "...", pagina: 126, formatted: "T20 - EJA, p. 126", bookId: "t20_eja", bookAbbreviation: "T20 - EJA" }
 * ```
 */
export function getBookReferenceFor(registroId: string, tabela: string): BookReference | null {
  return getBookReferencesFor(registroId, tabela)[0] ?? null
}
