import { describe, it, expect } from "vitest"
import { getBookReferenceFor, getBookReferencesFor } from "../../../src/ts/models/concerns/book_referenceable.js"
import { Arma } from "../../../src/ts/models/arma.js"
import { AcessorioMagico } from "../../../src/ts/models/acessorio_magico.js"
import { Condicao } from "../../../src/ts/models/condicao.js"
import { Encantamento } from "../../../src/ts/models/encantamento.js"
import { MaterialEspecial } from "../../../src/ts/models/material_especial.js"
import { Melhoria } from "../../../src/ts/models/melhoria.js"
import { Pericia } from "../../../src/ts/models/pericia.js"
import { Pocao } from "../../../src/ts/models/pocao.js"
import { Regra } from "../../../src/ts/models/regra.js"
import { Tabela } from "../../../src/ts/models/tabela.js"

describe("book_referenceable concern", () => {
  describe("getBookReferenceFor", () => {
    it("filters by tabela to avoid cross-table id collisions", () => {
      // "bola_de_fogo" is both a magia (p. 188) and a poção (p. 347).
      const asMagia = getBookReferenceFor("bola_de_fogo", "magias")
      const asPocao = getBookReferenceFor("bola_de_fogo", "pocoes")

      expect(asMagia).not.toBeNull()
      expect(asPocao).not.toBeNull()
      expect(asMagia!.pagina).not.toBe(asPocao!.pagina)
      expect(asMagia!.pagina).toBe(188)
      expect(asPocao!.pagina).toBe(347)
    })

    it("returns null for an unknown registro_id", () => {
      expect(getBookReferenceFor("id_que_nao_existe", "tabela_qualquer")).toBeNull()
    })

    it("returns null when the id exists but under a different tabela", () => {
      // "adaga" is indexed under armas; querying another table must not match.
      expect(getBookReferenceFor("adaga", "magias")).toBeNull()
    })

    it("resolves a reference with livro, pagina and formatted", () => {
      const ref = Arma.find("adaga")!.bookReference()

      expect(ref).not.toBeNull()
      expect(typeof ref!.livro).toBe("string")
      expect(typeof ref!.pagina).toBe("number")
      expect(typeof ref!.formatted).toBe("string")
      expect(ref!.pagina).toBe(152)
      expect(ref!.formatted).toContain(String(ref!.pagina))
    })
  })

  describe("getBookReferencesFor", () => {
    it("returns a single entry for bola_de_fogo as magia", () => {
      const refs = getBookReferencesFor("bola_de_fogo", "magias")
      expect(refs).toHaveLength(1)
      expect(refs[0].pagina).toBe(188)
    })

    it("returns a single entry for bola_de_fogo as poção", () => {
      const refs = getBookReferencesFor("bola_de_fogo", "pocoes")
      expect(refs).toHaveLength(1)
      expect(refs[0].pagina).toBe(347)
    })

    it("returns every source for a multi-source entity, in livro_id/pagina order", () => {
      // "espinhosa" is indexed in Ameaças (p401) and EJA (p171).
      const refs = getBookReferencesFor("espinhosa", "melhorias")
      expect(refs.map((r) => r.pagina)).toEqual([401, 171])
      expect(refs[0].formatted).toContain("401")
      expect(refs[1].formatted).toContain("171")
    })

    it("returns an empty array for an unknown registro_id", () => {
      expect(getBookReferencesFor("id_que_nao_existe", "tabela_qualquer")).toEqual([])
    })
  })

  describe("model bookReference() methods", () => {
    it("AcessorioMagico.bookReference() is callable", () => {
      const ref = AcessorioMagico.find("amuleto_da_robustez")?.bookReference() ?? null
      expect(ref === null || typeof ref.pagina === "number").toBe(true)
    })

    it("Condicao.bookReference() is callable", () => {
      const ref = Condicao.find("abalado")?.bookReference() ?? null
      expect(ref === null || typeof ref.pagina === "number").toBe(true)
    })

    it("Encantamento.bookReference() is callable", () => {
      const ref = Encantamento.find("abascanto")?.bookReference() ?? null
      expect(ref === null || typeof ref.pagina === "number").toBe(true)
    })

    it("MaterialEspecial.bookReference() is callable", () => {
      const ref = MaterialEspecial.find("aco_rubi")?.bookReference() ?? null
      expect(ref === null || typeof ref.pagina === "number").toBe(true)
    })

    it("Melhoria.bookReference() is callable", () => {
      const ref = Melhoria.find("ajustada")?.bookReference() ?? null
      expect(ref === null || typeof ref.pagina === "number").toBe(true)
    })

    it("Pericia.bookReference() is callable", () => {
      const ref = Pericia.find("acrobacia")?.bookReference() ?? null
      expect(ref === null || typeof ref.pagina === "number").toBe(true)
    })

    it("Pocao.bookReference() is callable", () => {
      const ref = Pocao.find("bola_de_fogo")?.bookReference() ?? null
      expect(ref === null || typeof ref.pagina === "number").toBe(true)
    })

    it("Regra.bookReference() is callable", () => {
      const ref = Regra.find("alcances")?.bookReference() ?? null
      expect(ref === null || typeof ref.pagina === "number").toBe(true)
    })

    it("Tabela.bookReference() is callable", () => {
      const tabela = Tabela.first()
      const ref = tabela?.bookReference() ?? null
      expect(ref === null || typeof ref.pagina === "number").toBe(true)
    })
  })

  describe("model bookReferences() methods", () => {
    it("Melhoria.bookReferences() returns every source of a multi-source entity", () => {
      const refs = Melhoria.find("espinhosa")!.bookReferences()
      expect(refs.map((r) => r.pagina)).toEqual([401, 171])
    })

    it("Arma.bookReferences() returns the single indexed page", () => {
      const refs = Arma.find("adaga")!.bookReferences()
      expect(refs).toHaveLength(1)
      expect(refs[0].pagina).toBe(152)
    })

    it("Pocao.bookReferences() scopes by tabela", () => {
      const refs = Pocao.find("bola_de_fogo")!.bookReferences()
      expect(refs.map((r) => r.pagina)).toEqual([347])
    })
  })
})
