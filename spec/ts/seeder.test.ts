import { describe, it, expect } from "vitest"
import { mapArma, mapItem, mapMelhoria } from "../../src/ts/seeder.js"

describe("seeder mappers", () => {
  describe("mapArma", () => {
    it("merges habilidades and especial string into properties", () => {
      const row = mapArma({
        id: "adaga",
        name: "Adaga",
        proficiencia: "simples",
        habilidades: ["dupla"],
        especial: "leve",
      })
      expect(row.properties).toEqual(["dupla", "leve"])
    })

    it("still includes especial when habilidades is absent", () => {
      const row = mapArma({
        id: "adaga",
        name: "Adaga",
        proficiencia: "simples",
        especial: "dupla",
      })
      expect(row.properties).toEqual(["dupla"])
    })

    it("keeps an object especial alongside array habilidades", () => {
      // Real armas JSON stores `especial` as an object, not a string.
      const row = mapArma({
        id: "adaga",
        name: "Adaga",
        proficiencia: "simples",
        habilidades: ["dupla"],
        especial: { ocultar_bonus: 5 },
      })
      expect(row.properties).toEqual(["dupla", { ocultar_bonus: 5 }])
    })
  })

  describe("mapItem", () => {
    it("falls back to efeito when effects is missing", () => {
      const row = mapItem({
        id: "gorad_quente",
        name: "Gorad Quente",
        efeito: { pm_temporarios: 2 },
      })
      expect(row.effects).toEqual({ pm_temporarios: 2 })
    })

    it("prefers effects over efeito when both are present", () => {
      const row = mapItem({
        id: "item",
        name: "Item",
        effects: { from_effects: true },
        efeito: { from_efeito: true },
      })
      expect(row.effects).toEqual({ from_effects: true })
    })

    it("merges a parceiro block into effects.parceiro", () => {
      const row = mapItem({
        id: "cavalo",
        name: "Cavalo",
        efeito: { nota: "x" },
        parceiro: { tipo: ["montaria"] },
      })
      expect(row.effects.parceiro).toEqual({ tipo: ["montaria"] })
      expect(row.effects.nota).toBe("x")
    })
  })

  describe("mapMelhoria", () => {
    it("falls back to efeito when effects is missing", () => {
      const row = mapMelhoria({
        id: "reforcada",
        name: "Reforçada",
        efeito: { bonus_defesa: 1 },
      })
      expect(row.effects).toEqual({ bonus_defesa: 1 })
    })

    it("uses effects when efeito is missing", () => {
      const row = mapMelhoria({
        id: "melhoria",
        name: "Melhoria",
        effects: { only_effects: true },
      })
      expect(row.effects).toEqual({ only_effects: true })
    })

    it("prefers efeito over effects when both are present", () => {
      const row = mapMelhoria({
        id: "melhoria",
        name: "Melhoria",
        efeito: { from_efeito: true },
        effects: { from_effects: true },
      })
      expect(row.effects).toEqual({ from_efeito: true })
    })
  })
})
