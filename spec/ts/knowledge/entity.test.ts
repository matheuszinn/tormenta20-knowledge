import { describe, it, expect } from "vitest"
import {
  entityTypeFor,
  toSearchResult,
  TABLE_TO_ENTITY_TYPE,
  type KnowledgeModelLike,
} from "../../../src/ts/knowledge/entity.js"
import { Arma } from "../../../src/ts/models/arma.js"
import { AcessorioMagico } from "../../../src/ts/models/acessorio_magico.js"
import { Divindade } from "../../../src/ts/models/divindade.js"
import { Magia } from "../../../src/ts/models/magia.js"
import { Melhoria } from "../../../src/ts/models/melhoria.js"
import { Pocao } from "../../../src/ts/models/pocao.js"
import type { BookReference } from "../../../src/ts/models/concerns/book_referenceable.js"

describe("knowledge/entity", () => {
  describe("entityTypeFor", () => {
    it("maps every entity table in TABLE_TO_ENTITY_TYPE", () => {
      const entries = Object.entries(TABLE_TO_ENTITY_TYPE)
      expect(entries).toHaveLength(19)
      for (const [table, type] of entries) {
        expect(entityTypeFor(table)).toBe(type)
      }
    })

    it("maps the canonical entity tables explicitly", () => {
      expect(entityTypeFor("armas")).toBe("arma")
      expect(entityTypeFor("armaduras")).toBe("armadura")
      expect(entityTypeFor("escudos")).toBe("escudo")
      expect(entityTypeFor("itens")).toBe("item")
      expect(entityTypeFor("melhorias")).toBe("melhoria")
      expect(entityTypeFor("encantamentos")).toBe("encantamento")
      expect(entityTypeFor("materiais_especiais")).toBe("material_especial")
      expect(entityTypeFor("pocoes")).toBe("pocao")
      expect(entityTypeFor("acessorios_magicos")).toBe("acessorio_magico")
      expect(entityTypeFor("magias")).toBe("magia")
      expect(entityTypeFor("poderes")).toBe("poder")
      expect(entityTypeFor("classes")).toBe("classe")
      expect(entityTypeFor("origens")).toBe("origem")
      expect(entityTypeFor("racas")).toBe("raca")
      expect(entityTypeFor("divindades")).toBe("divindade")
      expect(entityTypeFor("condicoes")).toBe("condicao")
      expect(entityTypeFor("regras")).toBe("regra")
      expect(entityTypeFor("pericias")).toBe("pericia")
      expect(entityTypeFor("tabelas")).toBe("tabela")
    })

    it("refuses metadata and unknown tables", () => {
      expect(entityTypeFor("indice_remissivo")).toBeNull()
      expect(entityTypeFor("livros")).toBeNull()
      expect(entityTypeFor("unknown_table")).toBeNull()
    })
  })

  describe("toSearchResult — real entities", () => {
    it("maps an Arma with non-empty sources", () => {
      const adaga = Arma.find("adaga")!
      const result = toSearchResult(adaga, "armas")

      expect(result.id).toBe("adaga")
      expect(result.type).toBe("arma")
      expect(result.name).toBe("Adaga")
      expect(result.matchedBy).toEqual([])
      expect(result.score).toBeUndefined()
      expect(result.evidence).toBeUndefined()

      expect(result.sources.length).toBeGreaterThan(0)
      const ref = result.sources[0]
      expect(ref.bookId).toBe("t20_eja")
      expect(ref.bookName).toBe("Tormenta 20 - Edição Jogo do Ano")
      expect(ref.bookAbbreviation).toBe("T20 - EJA")
      expect(ref.page).toBe(152)
      expect(ref.formatted).toMatch(/^T20.*p\. \d+$/)
      expect(ref.livro).toBeUndefined()
      expect(ref.pagina).toBeUndefined()
    })

    it("maps a Divindade (Allihanna, p. 103)", () => {
      const allihanna = Divindade.find("allihanna")!
      const result = toSearchResult(allihanna, "divindades")

      expect(result.type).toBe("divindade")
      expect(result.sources.map((s) => s.page)).toContain(103)
    })

    it("preserves multiple sources for a multi-source Melhoria (Espinhosa)", () => {
      const espinhosa = Melhoria.find("espinhosa")!
      const result = toSearchResult(espinhosa, "melhorias")

      expect(result.type).toBe("melhoria")
      expect(result.sources).toHaveLength(2)
      expect(result.sources.map((s) => s.page)).toEqual([401, 171])
      expect(result.sources.map((s) => s.bookId)).toEqual([
        "ameacas_de_arton",
        "t20_eja",
      ])
    })

    it("maps a Magia with a single indexed source (Bola de Fogo, p. 188)", () => {
      const bolaDeFogo = Magia.find("bola_de_fogo")!
      const result = toSearchResult(bolaDeFogo, "magias")

      expect(result.type).toBe("magia")
      expect(result.sources).toHaveLength(1)
      expect(result.sources[0].page).toBe(188)
    })

    it("scopes Pocao sources by tabela (Bola de Fogo, p. 347)", () => {
      const pocao = Pocao.find("bola_de_fogo")!
      const result = toSearchResult(pocao, "pocoes")

      expect(result.type).toBe("pocao")
      expect(result.sources).toHaveLength(1)
      expect(result.sources[0].page).toBe(347)
    })

    it("maps an AcessorioMagico", () => {
      const acessorio = AcessorioMagico.find("amuleto_da_robustez")!
      const result = toSearchResult(acessorio, "acessorios_magicos")

      expect(result.type).toBe("acessorio_magico")
      expect(result.id).toBe("amuleto_da_robustez")
    })
  })

  describe("toSearchResult — description handling", () => {
    const emptySources: BookReference[] = []

    it("includes a non-empty description", () => {
      const model: KnowledgeModelLike = {
        id: "x",
        name: "X",
        description: "Uma descrição.",
        bookReferences: () => emptySources,
      }
      const result = toSearchResult(model, "armas")
      expect(result.description).toBe("Uma descrição.")
    })

    it("omits the description key when description is null", () => {
      const model: KnowledgeModelLike = {
        id: "x",
        name: "X",
        description: null,
        bookReferences: () => emptySources,
      }
      const result = toSearchResult(model, "armas")
      expect(result.description).toBeUndefined()
      expect("description" in result).toBe(false)
    })

    it("omits the description key when description is empty", () => {
      const model: KnowledgeModelLike = {
        id: "x",
        name: "X",
        description: "",
        bookReferences: () => emptySources,
      }
      const result = toSearchResult(model, "armas")
      expect(result.description).toBeUndefined()
      expect("description" in result).toBe(false)
    })

    it("omits the description key when the model exposes no description", () => {
      const model: KnowledgeModelLike = {
        id: "x",
        name: "X",
        bookReferences: () => emptySources,
      }
      const result = toSearchResult(model, "armas")
      expect(result.description).toBeUndefined()
    })

    it("yields an empty sources array when the model has no references", () => {
      const model: KnowledgeModelLike = {
        id: "x",
        name: "X",
        bookReferences: () => [],
      }
      const result = toSearchResult(model, "armas")
      expect(result.sources).toEqual([])
    })
  })

  describe("toSearchResult — refusals", () => {
    it("throws TypeError for a metadata table", () => {
      const model: KnowledgeModelLike = {
        id: "x",
        name: "X",
        bookReferences: () => [],
      }
      expect(() => toSearchResult(model, "indice_remissivo")).toThrow(TypeError)
      expect(() => toSearchResult(model, "livros")).toThrow(TypeError)
    })

    it("throws TypeError for an unknown table", () => {
      const model: KnowledgeModelLike = {
        id: "x",
        name: "X",
        bookReferences: () => [],
      }
      expect(() => toSearchResult(model, "unknown_table")).toThrow(TypeError)
    })
  })
})
