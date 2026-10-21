import { describe, it, expect } from "vitest"
import { Poder } from "../../../src/ts/models/poder.js"

const VALID_TYPES = [
  "habilidade_unica_origem", "poder_concedido", "poder_tormenta",
  "poder_classe", "habilidade_de_raca", "poder_geral",
  "poder_combate", "poder_destino", "poder_magia",
] as const

describe("Poder", () => {
  describe("data integrity", () => {
    it("has poderes loaded from the database", () => {
      expect(Poder.count()).toBeGreaterThan(0)
    })

    it("every poder has required fields", () => {
      for (const p of Poder.all()) {
        expect(p.id).toBeTruthy()
        expect(p.name).toBeTruthy()
        expect(VALID_TYPES).toContain(p.type)
      }
    })

    it("effects and prerequisites are defined", () => {
      for (const p of Poder.all()) {
        expect(p.effects).toBeDefined()
        expect(p.prerequisites).toBeDefined()
      }
    })
  })

  describe("scopes", () => {
    it("habilidadesUnicas returns only habilidade_unica_origem", () => {
      const result = Poder.habilidadesUnicas().all()
      expect(result.length).toBeGreaterThan(0)
      result.forEach((p) => expect(p.type).toBe("habilidade_unica_origem"))
    })

    it("poderesCombate returns only poder_combate", () => {
      const result = Poder.poderesCombate().all()
      expect(result.length).toBeGreaterThan(0)
      result.forEach((p) => expect(p.type).toBe("poder_combate"))
    })

    it("poderesDestino returns only poder_destino", () => {
      const result = Poder.poderesDestino().all()
      expect(result.length).toBeGreaterThan(0)
      result.forEach((p) => expect(p.type).toBe("poder_destino"))
    })

    it("poderesMagia returns only poder_magia", () => {
      const result = Poder.poderesMagia().all()
      expect(result.length).toBeGreaterThan(0)
      result.forEach((p) => expect(p.type).toBe("poder_magia"))
    })

    it("habilidadesDeRaca returns only habilidade_de_raca", () => {
      const result = Poder.habilidadesDeRaca().all()
      expect(result.length).toBeGreaterThan(0)
      result.forEach((p) => expect(p.type).toBe("habilidade_de_raca"))
    })

    it("poderesClasse returns only poder_classe", () => {
      const result = Poder.poderesClasse().all()
      expect(result.length).toBeGreaterThan(0)
      result.forEach((p) => expect(p.type).toBe("poder_classe"))
    })

    it("byClass filters by class_id", () => {
      const result = Poder.byClass("guerreiro").all()
      expect(result.length).toBeGreaterThan(0)
      result.forEach((p) => expect(p.classId).toBe("guerreiro"))
    })

    it("byType filters correctly", () => {
      for (const type of VALID_TYPES) {
        const result = Poder.byType(type).all()
        result.forEach((p) => expect(p.type).toBe(type))
      }
    })
  })

  describe("toH", () => {
    it("returns a plain object with required keys", () => {
      const p = Poder.first()!
      const h = p.toH()
      expect(h).toMatchObject({ id: p.id, name: p.name, type: p.type })
      expect(h.effects).toBeDefined()
      expect(Array.isArray(h.prerequisites)).toBe(true)
    })
  })
})
