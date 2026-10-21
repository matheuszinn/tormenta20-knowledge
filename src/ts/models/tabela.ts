import { BaseModel } from "./base.js"
import { Query } from "../query.js"
import { getBookReferenceFor, getBookReferencesFor, type BookReference } from "./concerns/book_referenceable.js"

const TABLE = "tabelas"

/**
 * A Tabela (reference table) in Tormenta20.
 *
 * Tables store structured tabular data from T20 sourcebooks (e.g. random loot tables,
 * encounter tables, etc.).
 *
 * @example
 * ```ts
 * Tabela.all()
 * Tabela.find("tesouros_por_nd")
 *
 * const t = Tabela.find("tesouros_por_nd")!
 * t.headers   // ["ND", "Tibares", "Itens"]
 * t.rows      // [["1", "50", "—"], ...]
 * ```
 */
export class Tabela extends BaseModel {
  get description(): string | null { return (this._row.description as string) ?? null }
  /** Column header labels. */
  get headers(): string[] { return BaseModel.json(this._row.headers, []) }
  /** Array of row arrays, each containing string values in header order. */
  get rows(): unknown[][] { return BaseModel.json(this._row.rows, []) }

  /** Returns the sourcebook page reference, or `null` if not indexed. */
  bookReference(): BookReference | null { return getBookReferenceFor(this.id, TABLE) }

  /** Returns all sourcebook page references (multi-source), or an empty array if not indexed. */
  bookReferences(): BookReference[] { return getBookReferencesFor(this.id, TABLE) }

  toH() {
    return { id: this.id, name: this.name, description: this.description, headers: this.headers, rows: this.rows }
  }

  static query(): Query<Tabela> { return BaseModel.makeQuery(TABLE, Tabela) }
  static all(): Tabela[] { return Tabela.query().all() }
  static find(id: string): Tabela | null { return Tabela.query().find(id) }
  static first(): Tabela | null { return Tabela.query().first() }
  static last(): Tabela | null { return Tabela.query().last() }
  static count(): number { return Tabela.query().count() }
}
