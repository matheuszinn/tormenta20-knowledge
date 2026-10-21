import { BaseModel } from "./base.js"
import { Query } from "../query.js"
import { getBookReferenceFor, getBookReferencesFor, type BookReference } from "./concerns/book_referenceable.js"

const TABLE = "regras"

/**
 * A Regra (game rule entry) in Tormenta20.
 *
 * Rules entries contain structured reference data for T20 mechanics.
 *
 * @example
 * ```ts
 * Regra.all()
 * Regra.find("combate")
 * ```
 */
export class Regra extends BaseModel {
  get description(): string | null { return (this._row.description as string) ?? null }
  /** JSON object with structured rule data (schema varies per entry). */
  get data(): Record<string, unknown> { return BaseModel.json(this._row.data, {}) }

  /** Returns the sourcebook page reference, or `null` if not indexed. */
  bookReference(): BookReference | null { return getBookReferenceFor(this.id, TABLE) }

  /** Returns all sourcebook page references (multi-source), or an empty array if not indexed. */
  bookReferences(): BookReference[] { return getBookReferencesFor(this.id, TABLE) }

  toH() {
    return { id: this.id, name: this.name, description: this.description, data: this.data }
  }

  static query(): Query<Regra> { return BaseModel.makeQuery(TABLE, Regra) }
  static all(): Regra[] { return Regra.query().all() }
  static find(id: string): Regra | null { return Regra.query().find(id) }
  static first(): Regra | null { return Regra.query().first() }
  static last(): Regra | null { return Regra.query().last() }
  static count(): number { return Regra.query().count() }
}
