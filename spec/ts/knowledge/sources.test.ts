import { describe, it, expect } from "vitest"
import { toSourceReference, toSourceReferences } from "../../../src/ts/knowledge/sources.js"
import type { BookReference } from "../../../src/ts/models/concerns/book_referenceable.js"

const ref: BookReference = {
  livro: "Tormenta 20 - Edição Jogo do Ano",
  pagina: 152,
  formatted: "T20 - EJA, p. 152",
  bookId: "t20_eja",
  bookAbbreviation: "T20 - EJA",
}

describe("knowledge/sources", () => {
  describe("toSourceReference", () => {
    it("maps every internal field to its public counterpart", () => {
      expect(toSourceReference(ref)).toEqual({
        bookId: "t20_eja",
        bookName: "Tormenta 20 - Edição Jogo do Ano",
        bookAbbreviation: "T20 - EJA",
        page: 152,
        formatted: "T20 - EJA, p. 152",
      })
    })

    it("does not carry the internal Portuguese field names through", () => {
      const out = toSourceReference(ref) as Record<string, unknown>
      expect(out.livro).toBeUndefined()
      expect(out.pagina).toBeUndefined()
    })
  })

  describe("toSourceReferences", () => {
    it("returns an empty array for empty input", () => {
      expect(toSourceReferences([])).toEqual([])
    })

    it("returns a same-length array, preserving order", () => {
      const second: BookReference = {
        livro: "Tormenta 20 - Ameaças de Arton",
        pagina: 401,
        formatted: "T20 - Ameaças, p. 401",
        bookId: "ameacas_de_arton",
        bookAbbreviation: "T20 - Ameaças",
      }
      const out = toSourceReferences([ref, second])
      expect(out).toHaveLength(2)
      expect(out[0].page).toBe(152)
      expect(out[1].page).toBe(401)
      expect(out[1].bookId).toBe("ameacas_de_arton")
    })
  })
})
