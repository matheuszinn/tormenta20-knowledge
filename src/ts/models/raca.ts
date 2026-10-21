import { BaseModel } from "./base.js"
import { Query } from "../query.js"
import { getBookReferenceFor, getBookReferencesFor, type BookReference } from "./concerns/book_referenceable.js"

const TABLE = "racas"

/** Size category of a race. */
export type RacaSize = "minúsculo" | "pequeno" | "médio" | "grande"

/** Vision type of a race. */
export type RacaVision = "normal" | "baixa_luminosidade" | "visao_no_escuro"

/**
 * A Raça (playable race) in Tormenta20.
 *
 * @example
 * ```ts
 * Raca.all()
 * Raca.find("humano")
 *
 * const elfo = Raca.find("elfo")!
 * elfo.attributeBonusFor("DES")   // +2
 * elfo.hasVisaoNoEscuro           // false
 * ```
 */
export class Raca extends BaseModel {
  get description(): string { return this._row.description as string }
  get size(): RacaSize { return this._row.size as RacaSize }
  /** Base movement speed in metres. */
  get movement(): number { return this._row.movement as number }
  get vision(): RacaVision { return this._row.vision as RacaVision }
  /** Effective range of darkvision/low-light vision in metres, or `null` for normal vision. */
  get visionRange(): number | null { return (this._row.vision_range as number) ?? null }
  /** Map of attribute key → bonus value (e.g. `{ DES: 2, INT: -2 }`). */
  get attributeBonuses(): Record<string, number> { return BaseModel.json(this._row.attribute_bonuses, {}) }
  /** JSON array of skill bonus descriptors. */
  get skillBonuses(): unknown[] { return BaseModel.json(this._row.skill_bonuses, []) }
  /** IDs of racial abilities all members of this race have. */
  get racialAbilities(): string[] { return BaseModel.json(this._row.racial_abilities, []) }
  /** Number of racial abilities the player may choose at character creation. */
  get chosenAbilitiesAmount(): number { return (this._row.chosen_abilities_amount as number) ?? 0 }
  /** Pool of ability IDs the player chooses from. */
  get availableChosenAbilities(): unknown[] { return BaseModel.json(this._row.available_chosen_abilities, []) }
  /** Printed-book page reference. */
  get page(): number | null { return (this._row.page as number) ?? null }
  /** Source book slug, or `null` for the basic book. */
  get livroId(): string | null { return (this._row.livro_id as string) ?? null }
  /**
   * Lifespan category from the race stat block (`"Normal"`, `"x2"`, `"x5"`,
   * `"Indefinida"`), or `null` when the book gives none.
   */
  get longevidade(): string | null { return (this._row.longevidade as string) ?? null }
  /**
   * Deity slugs this race commonly worships. `["qualquer"]` means any deity;
   * `[]` means the book lists none / unknown.
   */
  get devotos(): string[] { return BaseModel.json(this._row.devotos, []) }

  /**
   * Returns the racial attribute bonus for the given attribute key (e.g. `"FOR"`, `"DES"`).
   * Returns `0` if there is no bonus for that attribute.
   */
  attributeBonusFor(attribute: string): number {
    return this.attributeBonuses[attribute] ?? 0
  }

  get isMinusculo(): boolean { return this.size === "minúsculo" }
  get isPequeno(): boolean { return this.size === "pequeno" }
  get isGrande(): boolean { return this.size === "grande" }
  /** `true` if the race has darkvision. */
  get hasVisaoNoEscuro(): boolean { return this.vision === "visao_no_escuro" }

  /** Returns the sourcebook page reference, or `null` if not indexed. */
  bookReference(): BookReference | null { return getBookReferenceFor(this.id, TABLE) }

  /** Returns all sourcebook page references (multi-source), or an empty array if not indexed. */
  bookReferences(): BookReference[] { return getBookReferencesFor(this.id, TABLE) }

  toH() {
    return {
      id: this.id, name: this.name, description: this.description,
      size: this.size, movement: this.movement, vision: this.vision,
      vision_range: this.visionRange, attribute_bonuses: this.attributeBonuses,
      skill_bonuses: this.skillBonuses, racial_abilities: this.racialAbilities,
      chosen_abilities_amount: this.chosenAbilitiesAmount,
      available_chosen_abilities: this.availableChosenAbilities,
      page: this.page, livro_id: this.livroId,
      longevidade: this.longevidade, devotos: this.devotos,
    }
  }

  static query(): Query<Raca> { return BaseModel.makeQuery(TABLE, Raca) }
  static all(): Raca[] { return Raca.query().all() }
  static find(id: string): Raca | null { return Raca.query().find(id) }
  static first(): Raca | null { return Raca.query().first() }
  static last(): Raca | null { return Raca.query().last() }
  static count(): number { return Raca.query().count() }
}
