import { BaseModel } from "./base.js"
import { Query } from "../query.js"
import { getBookReferenceFor, getBookReferencesFor, type BookReference } from "./concerns/book_referenceable.js"

const TABLE = "melhorias"

/**
 * A Melhoria (item upgrade/improvement) in Tormenta20.
 *
 * Melhorias are purchased enhancements applied to existing equipment.
 *
 * @example
 * ```ts
 * Melhoria.all()
 * Melhoria.find("resistente")
 * ```
 */
export class Melhoria extends BaseModel {
  get description(): string | null { return (this._row.description as string) ?? null }
  /** JSON array of equipment types this melhoria can be applied to. */
  get applicableTo(): unknown[] { return BaseModel.json(this._row.applicable_to, []) }
  /** Price in tibares. */
  get price(): number { return (this._row.price as number) ?? 0 }
  /** JSON object with mechanical effects. */
  get effects(): Record<string, unknown> { return BaseModel.json(this._row.effects, {}) }

  /** Returns the sourcebook page reference, or `null` if not indexed. */
  bookReference(): BookReference | null { return getBookReferenceFor(this.id, TABLE) }

  /** Returns all sourcebook page references (multi-source), or an empty array if not indexed. */
  bookReferences(): BookReference[] { return getBookReferencesFor(this.id, TABLE) }

  toH() {
    return {
      id: this.id, name: this.name, description: this.description,
      applicable_to: this.applicableTo, price: this.price, effects: this.effects,
    }
  }

  static query(): Query<Melhoria> { return BaseModel.makeQuery(TABLE, Melhoria) }
  static all(): Melhoria[] { return Melhoria.query().all() }
  static find(id: string): Melhoria | null { return Melhoria.query().find(id) }
  static first(): Melhoria | null { return Melhoria.query().first() }
  static last(): Melhoria | null { return Melhoria.query().last() }
  static count(): number { return Melhoria.query().count() }
}
