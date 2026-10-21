import { describe, it, expect, beforeEach, afterEach } from "vitest"
import Database from "better-sqlite3"
import { readFileSync, rmSync, mkdtempSync } from "fs"
import { join, dirname } from "path"
import { tmpdir } from "os"
import { fileURLToPath } from "url"
import { registerIndiceRemissivo } from "../../src/ts/seeder.js"

const __dirname = dirname(fileURLToPath(import.meta.url))
const SCHEMA_PATH = join(__dirname, "../../db/schema.sql")

function readAll(db: Database.Database): Record<string, unknown>[] {
  return db
    .prepare(
      "SELECT livro_id, termo, pagina, tabela, registro_id FROM indice_remissivo ORDER BY id",
    )
    .all() as Record<string, unknown>[]
}

// Builds a throwaway SQLite file from the real schema so the helper is
// exercised against the same unique index the production seeder writes to.
describe("registerIndiceRemissivo", () => {
  let dir: string
  let db: Database.Database

  beforeEach(() => {
    dir = mkdtempSync(join(tmpdir(), "t20-seeder-"))
    db = new Database(join(dir, "test.sqlite3"))
    db.pragma("foreign_keys = OFF")
    db.exec(readFileSync(SCHEMA_PATH, "utf-8"))
  })

  afterEach(() => {
    db.close()
    rmSync(dir, { recursive: true, force: true })
  })

  it("creates a row when page is present", () => {
    registerIndiceRemissivo(db, { id: "x", name: "X", page: 42, livro_id: "t20_eja" }, "armas")

    const rows = readAll(db)
    expect(rows).toHaveLength(1)
    expect(rows[0]).toMatchObject({
      livro_id: "t20_eja",
      termo: "X",
      pagina: 42,
      tabela: "armas",
      registro_id: "x",
    })
  })

  it("upserts tabela/registro_id on the (livro_id, termo, pagina) conflict", () => {
    registerIndiceRemissivo(db, { id: "x", name: "X", page: 42 }, "armas")
    registerIndiceRemissivo(db, { id: "y", name: "X", page: 42 }, "poderes")

    const rows = readAll(db)
    expect(rows).toHaveLength(1)
    expect(rows[0].tabela).toBe("poderes")
    expect(rows[0].registro_id).toBe("y")
  })

  it("is a no-op without page/pagina", () => {
    registerIndiceRemissivo(db, { id: "x", name: "X" }, "armas")
    expect(readAll(db)).toHaveLength(0)
  })

  it("defaults livro_id to t20_eja when missing", () => {
    registerIndiceRemissivo(db, { id: "x", name: "X", page: 10 }, "armas")
    expect(readAll(db)[0].livro_id).toBe("t20_eja")
  })

  it("falls back to id when name is missing", () => {
    registerIndiceRemissivo(db, { id: "x", page: 10 }, "armas")
    expect(readAll(db)[0].termo).toBe("x")
  })

  it("reads pagina as an alias for page", () => {
    registerIndiceRemissivo(db, { id: "x", name: "X", pagina: "7" }, "armas")
    expect(readAll(db)[0].pagina).toBe(7)
  })
})
