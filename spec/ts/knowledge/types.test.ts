import { describe, it, expect } from "vitest"
import type {
  EntityType,
  SourceReference,
  MatchChannel,
  SearchResult,
  SearchOptions,
  SearchResponse,
  GetEntityOptions,
} from "../../../src/ts/knowledge/types.js"

/**
 * Canary tests for the public Knowledge types. These are compile-time checks
 * (type assignability) plus a couple of shape assertions. They do not exercise
 * the database — see `entity.test.ts` for the real adapter tests.
 */
describe("knowledge/types", () => {
  it("accepts every documented EntityType value", () => {
    const all: EntityType[] = [
      "arma",
      "armadura",
      "escudo",
      "item",
      "melhoria",
      "encantamento",
      "material_especial",
      "pocao",
      "acessorio_magico",
      "magia",
      "poder",
      "classe",
      "origem",
      "raca",
      "divindade",
      "condicao",
      "regra",
      "pericia",
      "tabela",
      "criatura",
      "npc",
    ]
    expect(all).toHaveLength(21)
    expect(new Set(all).size).toBe(21)
  })

  it("accepts a fully-populated SourceReference", () => {
    const ref: SourceReference = {
      bookId: "t20_eja",
      bookName: "Tormenta 20 - Edição Jogo do Ano",
      bookAbbreviation: "T20 - EJA",
      page: 56,
      formatted: "T20 - EJA, p. 56",
      url: "https://example.invalid/t20_eja/56",
    }
    expect(ref.bookId).toBe("t20_eja")
  })

  it("accepts an empty SourceReference (all fields optional)", () => {
    const ref: SourceReference = {}
    expect(ref.page).toBeUndefined()
  })

  it("accepts a minimal SearchResult", () => {
    const result: SearchResult = {
      id: "adaga",
      type: "arma",
      name: "Adaga",
      sources: [],
      matchedBy: [],
    }
    expect(result.description).toBeUndefined()
    expect(result.score).toBeUndefined()
    expect(result.evidence).toBeUndefined()
  })

  it("accepts a fully-populated SearchResult", () => {
    const result: SearchResult = {
      id: "adaga",
      type: "arma",
      name: "Adaga",
      description: "Uma faca afiada.",
      sources: [{ bookId: "t20_eja", page: 152 }],
      matchedBy: ["name", "description"],
      score: 1.5,
      evidence: ["Adaga"],
    }
    expect(result.matchedBy).toHaveLength(2)
  })

  it("accepts every MatchChannel value", () => {
    const channels: MatchChannel[] = ["name", "description", "effect", "index", "structured"]
    expect(channels).toHaveLength(5)
  })

  it("accepts SearchOptions, SearchResponse and GetEntityOptions", () => {
    const options: SearchOptions = {
      query: "intimidação",
      types: ["item", "poder"],
      limit: 10,
      bookIds: ["t20_eja"],
      includeIndex: true,
    }
    const response: SearchResponse = { query: options.query, results: [], total: 0 }
    const get: GetEntityOptions = { id: "adaga", type: "arma" }
    expect(response.results).toEqual([])
    expect(get.id).toBe("adaga")
  })
})
