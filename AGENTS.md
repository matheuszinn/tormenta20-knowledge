# AGENTS.md

Compact notes for OpenCode sessions working in this repo. Skip what's obvious from filenames.

## What this repo is

Tri-language library (Ruby, TypeScript, Python) exposing Tormenta20 TTRPG data through the **same SQLite database** (`db/tormenta20.sqlite3`). JSON files in `src/json/` are the source of truth; the DB and the language bindings are generated artifacts.

- `src/json/**` — gold-master data
- `db/schema.sql` — single schema
- `db/tormenta20.sqlite3` — **generated** (gitignored content; `npm run seed` / `rake build_db`)
- `src/ruby/tormenta20/**` — Ruby models + entrypoint (`require 'tormenta20'`)
- `src/ts/**` — TS models + entrypoint (re-exports from `src/ts/index.ts`)
- `src/python/**` — Python bindings (lightweight)
- `db/seeds.rb` and `src/ts/seeder.ts` — **two parallel seeders** writing the same DB
- `docs/{ruby,ts}/` — generated API docs; `typedoc` builds `docs/`

Three parallel model layers must stay aligned: a schema change in `db/schema.sql` needs matching changes in both seeders, both model sets, and `docs/*`.

## Workflow — per-step validation (knowledge engine work)

Work in this repo follows the **Etapas** listed in
`SPEC-tormenta20-knowledge-ai.md` (§11). Adopt a strict **validate each
step individually** discipline:

1. **One Etapa at a time.** Do not combine adjacent Etapas in the same
   change (e.g. don't ship Etapa 1 + Etapa 2 together). Each Etapa
   becomes a reviewable unit.
2. **At the end of each Etapa**, before moving on, the human runs
   validation end-to-end:
   - **`scripts/validate-etapa1.ts`** (Etapa 1) or analogous script added
     for subsequent Etapas. The script must hit real DB rows and prove
     the new shape against the SPEC.
   - **`npx vitest run spec/ts/<etapa>/`** (TS) or
     **`bundle exec rspec spec/<etapa>/`** (Ruby) for the new specs.
   - **Baseline check** (`bundle exec rake build_db && npm test &&
     bundle exec rspec`) must remain green.
3. **Do not advance to the next Etapa until the human confirms the
   previous one.** The orchestrator surfaces a short "what to validate"
   note at the end of each lane; the user decides when to proceed.
4. **Exceptions / partial completion** belong in the audit doc
   (`docs/knowledge-query.md`) under a `## N. Estado da Etapa X` heading,
   not in the implementation files. Never mark an Etapa ✓ in the SPEC
   before the human has validated it.

Validation scripts live under `scripts/`. Naming: `validate-etapa<N>.ts`
matching the Etapa being shipped.

## JSON key convention: follow the basic book

**There is no single rule — each entity has its own house style.** Look at the existing basic book entries (`livro_id: null` or `livro_id: "t20_eja"`) in the same directory and mirror the same key names. The two seeders (`db/seeds.rb`, `src/ts/seeder.ts`) handle the translation to DB columns; the JSON itself stays in the convention its directory uses.

**The pattern per directory, as it actually exists today:**

| Directory | Convention in use | Notes |
|---|---|---|
| `racas/` | English core (`id`, `name`, `description`, `size`, `page`); Portuguese for movement/vision (`movement`, `vision`, `vision_range`, `attribute_bonuses`, `skill_bonuses`, `racial_abilities`, `chosen_abilities_amount`, `available_chosen_abilities`); Ameaças races add `longevidade` (`"Normal"`/`"x2"`/`"x5"`/`"Indefinida"`, `null` when the book gives none) and `devotos` (array of deity slugs, `["qualquer"]` when the book says "Qualquer", `null` when unknown) | `attribute_bonuses` uses Portuguese attribute names as keys (`destreza`, `forca`, `constituicao`, `inteligencia`, `sabedoria`, `carisma`) — these are values-of-keys, not English fields. `devotos: []` in the DB means unknown; `["qualquer"]` means any deity. |
| `classes/` | Mostly English (`id`, `name`, `hit_points`, `mana_points`, `skills`, `description`); `skills` uses `choose_amount` / `choose_from` instead of `choose.amount` / `choose.from`; per-skill objects use `name` + `attribute` | See `arcanista.json` for the canonical shape |
| `origens/` | English (`id`, `name`, `description`, `items`, `benefits`, `page`); `unique_power` value is a slug string (not an object); `items[]` entries have `type: "fixed"` plus a Portuguese `text` field; `benefits.skills`/`powers` are arrays of Portuguese names | |
| `deuses/` | Mixed: English (`id`, `name`, `title`, `description`, `energy`, `devotees`, `granted_powers`, `page`); Portuguese (`beliefs_objectives`, `holy_symbol`, `preferred_weapon`, `obligations_restrictions`) | `devotees` is `{ races: [...], classes: [...] }` |
| `pericias/` | English (`id`, `name`, `trained_only`, `armor_penalty`, `description`, `uses`, `page`); Portuguese (`atributo` as uppercase string like `"FOR"`, `cd`) | `uses[]` entries only have `name` (no `id`); structure is loose, see `atletismo.json` |
| `poderes/` | English (`id`, `name`, `type`, `sub_type`, `description`, `requirements`, `effects`, `page`); inside `requirements`/`effects` entries: `attr` is English, `sub_type` is English, `duration` is English, `weapons` is English | Look at `poderes_gerais/poderes_de_combate/ataque_poderoso.json` |
| `magias/` | Mixed; English core (`id`, `name`, `type`, `circle`, `school`, `execution`, `range`, `target`, `effect`, `duration`, `extra_costs`, `description`, `enhancements`, `effects`, `counterspell`); Portuguese spellbook legacy (`resistance`, `effect_details.dimension`) | `circle` is a **string** `"2"`, not an int. Some fields like `resistance.effect` have trailing `\|` artifacts from the source. Do not "fix" the typos without checking the seeder. |
| `equipamentos/armas/` | English (`id`, `name`, `type`, `description`, `page`); Portuguese (`proficiencia`, `proposito`, `empunhadura`, `preco`, `dano`, `critico`, `alcance`, `tipo_dano`, `espacos`, `habilidades`, `especial`) | `type` is always `"arma"`, `proficiencia` carries the category (`simples`/`marcial`/`exotica`/`fogo`) |
| `equipamentos/armaduras/` | English (`id`, `name`, `type`, `description`); Portuguese (`categoria`, `preco`, `bonus_defesa`, `penalidade_armadura`, `espacos`, `especial`, `vestir_remover`) | `type` is always `"armadura"`; `categoria` is `leve`/`pesada` |
| `equipamentos/escudos/` | Same as armaduras, plus `ataque` object with Portuguese keys | `type` is always `"escudo"` |
| `equipamentos/itens/**/` | English (`id`, `name`, `type`, `description`, `page`); Portuguese core (`categoria`, `preco`, `espacos`); extra Portuguese fields per item type (`cd_fabricacao`, `uso`, `conta_como_vestido`, `doses_veneno_armazenadas`, etc.) | Look at siblings in the same leaf folder before adding new fields. `animais/` files carry a `parceiro` block with `tipo[]` (array: `montaria`/`perseguidor`/`especial`/`besta_de_carga`), `porte`, `pagina_criatura`, `patamares.{iniciante,veterano,mestre}` (per-tier `movement[]`/`damage[]`/`attack[]`/`defense[]`/`skill_bonus[]`/`saving_throw[]`/`senses[]`/`maneuvers[]`/`powers[]`/`extra_actions[]`/`terreno[]`/`special[]`), plus optional `besta_de_carga`, `alternativo`, `restricoes[]`, `isento_restricao_cavalgar_combate`. Both seeders merge these into the `itens.effects` JSON column. |
| `itens_superiores/materiais_especiais/` | English (`id`, `name`, `description`, `page`); Portuguese (`type`, `aparencia`, `origem`, `precos_adicionais`, `efeitos` — plural, with per-item-type nested objects) | No `applicable_to` array |
| `itens_superiores/melhorias/**/` | English (`id`, `name`, `description`, `page`); Portuguese (`type`, `categoria`, `efeito` — singular, `prerequisitos`) | Both seeders agora leem `efeito \|\| effects` (Round 1). 35/37 melhorias usam `efeito` e populam `melhorias.effects`. Gotcha #6 resolvido. |
| `itens_superiores/encantamentos/**/` | English (`id`, `name`, `description`, `page`); Portuguese (`type`, `categoria`, `efeito` — singular) | Inside `efeito`: Portuguese keys like `dano_extra`, `tipo_dano_extra` |
| `itens_magicos/pocoes/` | Portuguese-heavy: `subtipo`, `pm_cost`, `categoria`, `preco`, `roll_min`, `roll_max`, `aprimoramento`; English: `id`, `name`, `spell_id`, `description`, `page` | |
| `itens_magicos/acessorios/` | English (`id`, `name`, `description`, `page`); Portuguese (`categoria`, `preco`, `roll_min`, `roll_max`, `efeito` — singular) | `categoria` is `menor`/`medio`/`maior`/`artefato` |
| `condicoes/` | English (`id`, `name`, `description`, `effects`, `condition_type`, `escalates_to`, `page`) | `effects` is a loose list of Portuguese effect descriptions, not structured |
| `regras/` | English core (`id`, `name`, `description`, `page`, `livro_id`) + free-form per-rule keys (e.g. `categorias`, `margens`, `multiplicadores`) | Free-form keys collapse into the `regra.data` JSON column. Treat them as English field names, but the *values* are typically Portuguese. |
| `tabelas/` | English (`id`, `name`, `description`, `headers`, `rows`, `page`, `livro_id`) | `headers`/`rows` are simple arrays |
| `livros/` | Portuguese (`id`, `nome`, `nome_curto`) | DB column names match |
| `indice_remissivo/<livro_id>.json` | Portuguese (`termo`, `pagina`, `tabela`, `registro_id`) — entry-level | DB column names match |

**Bottom line: when adding a new file, copy the structure of an existing sibling from the basic book.** When in doubt, run `grep -l "your_key" src/json/<dir>/` and copy the pattern. Do not invent a new convention for an existing directory.

## Page convention: `page` is the printed page

`page` (and `pagina_criatura`) always means the **printed folio** — the number a reader sees holding the physical book. Same for `indice_remissivo.pagina` (which is what `bookReference()` returns). Offsets, verified against the PDFs in `books/`:

- Ameaças de Arton: printed = PDF page − 2 (e.g. Rompedor da Realidade text on PDF p405 = printed p403)
- T20 Edição Jogo do Ano: printed = PDF page − 6 (e.g. Adaga text on PDF p152 = printed p146)

Legacy status, so you know what you're looking at:

- Basic-book files (`livro_id` absent): values are **PDF numbers** (verified: adaga 152, hynne 33). Convert to printed on touch.
- Ameaças files edited/created after Oct 2026: already printed. Older untouched Ameaças files are mixed — verify against the PDF before trusting.
- Never add a `page_source`/`page_type` field. If you verified a value, it's printed, full stop.

## Free-form reference: how the DB columns relate to JSON keys

The two active seeders (`bin/build_db` em Ruby, `src/ts/seeder.ts` em TS) traduzem per-table. `db/seeds.rb` é mantido em sincronia mas é código morto (não-executável em runtime). Some mappings are clean 1:1 (e.g. `pericias.atributo` → `pericias.atributo`); others have aliases (`armas.proficiencia` → `armas.category` via `ARMA_CATEGORY_MAP`). When you change a JSON key, check `seeder.ts` to see if you also broke a column.

Known translation sites (TS seeder):
- `armas`: `proficiencia`→`category`, `preco`→`price`, `dano`→`damage`, `tipo_dano`→`damage_type`, `critico`→`critical`, `alcance`→`range`, `espacos`→`weight`, `[habilidades, especial]`→`properties` (Round 1)
- `armaduras`/`escudos`: `preco`→`price`, `bonus_defesa`→`defense_bonus`, `penalidade_armadura`→`armor_penalty`, `espacos`→`weight`, `habilidades`→`properties`
- `itens`: `preco`→`price`, `espacos`→`weight`, `category`/`categoria`→`category`, `efeito`→`effects` (Round 1; antes só `effects`)
- `melhorias`: `efeito`→`effects` (Round 1; antes só `effects`)
- `poderes`: `requirements`→`prerequisites`, plus `type` is set per-directory (`PODER_DIR_TYPE_MAP`)
- `magias`: `resistance`→split into `resistance_effect`/`resistance_skill`, `target` flattened into `target_amount`/`target_up_to`/`target_type`, `effect_details.other_details`→`effect_other_details`, `effect_details.dimension`→`effect_dimension` (Round 3; antes `effect_dimention`)

**Multi-fonte**: cada entity pode aparecer em múltiplas páginas no `indice_remissivo` (mesmo `(tabela, registro_id)`). `bookReference()` (singular) retorna a primeira; `bookReferences()` (plural, Round 3) retorna `BookReference[]` ordenado por `(livro_id, pagina)`. Exemplo: `melhorias.espinhosa` aparece em `ameacas_de_arton` p401 **e** `t20_eja` p171.

## Critical gotchas

1. **Runtime DB is read-only.** `src/ruby/tormenta20/models/base.rb:41` makes every ActiveRecord model `readonly? = true`; class-level writes (`create`, `update_all`, `delete_all`, …) raise `ReadOnlyError`. The DB ships pre-populated. Re-run the seeder to apply data changes — do not try to write through ActiveRecord.

2. **JSON is the source of truth, not the models.** Editing only `src/ts/models/*` or `src/ruby/tormenta20/models/*` has zero runtime effect on consumers (they read the seeded DB). To change data: edit `src/json/**` and re-seed.

3. **Build order matters.** Both CI jobs run `bundle exec rake build_db` / `npm run seed` **before** tests, because specs exercise the seeded DB. Locally the same applies: `rake` auto-runs `build_db` via `Rakefile:24` (`Rake::Task[:spec].enhance([:build_db])`), but TS does **not** — `npm test` requires `npm run seed` to have been run first in this checkout. If a TS spec fails with "no such table", the DB wasn't rebuilt.

4. **Two seeders must agree.** `bin/build_db` (Ruby, used by CI test-ruby via `rake build_db` → `bin/test` → `bin/ci`) and `src/ts/seeder.ts` (TS, used by CI test-ts + `npm run seed` + npm publish) write the same `.sqlite3` from the same `src/json/`. **`db/seeds.rb` is dead code** (não referenciado por nenhum workflow, bin/* ou Rakefile) — é mantido em sincronia por política "JSON é fonte da verdade" e cobre as 21 tabelas, mas `Models::Base#readonly? = true` impede `save!` em runtime; sua lógica é exercitada via testes de unidade. When you add a new top-level JSON folder or a new column, update both **active** seeders — or whichever one CI actually runs locally. Field renames (e.g. `proficiencia` → `category`, `preco` → `price` in `armas`/`armaduras`) live in the seeder transforms; the JSON keeps the basic-book keys. After Round 1+2, ambos os seeders canônicos produzem DBs idênticos byte-a-byte nos dados (paridade verificada via `comm` em `indice_remissivo`).

5. **`Rakefile:24` enhancements apply to user-run `rake` but not `rspec` directly.** `bundle exec rake` builds the DB then runs specs; `bundle exec rspec spec/models/regra_spec.rb` does not — it expects a pre-built DB at `db/tormenta20.sqlite3` or it fails. Use `bin/test` or `bin/ci` wrappers that build first.

6. ~~**Melhorias `efeito` is dropped by the TS seeder.**~~ **Resolvido (Round 1)** — TS agora lê `efeito ?? effects ?? {}` via `mapMelhoria` em `src/ts/seeder.ts`. Ruby `bin/build_db` já lia `efeito || effects`. 35 arquivos que usavam `efeito` agora populam `melhorias.effects`. `materiais_especiais.applicable_to` ainda é `[]` em alguns caminhos — verificar caso a caso.

8. **Builds refuse when any JSON has `needs_review`.** All three build paths (`npm run seed`, `bin/build_db`, `db/seeds.rb`) deep-scan `src/json/**` for a `needs_review` key (any truthy value, at any depth) and abort listing every flagged file:line before touching the DB. Currently flagged: `deuses/hippion.json`, `equipamentos/itens/animais/elefante.json` (`$.besta_de_carga`), `racas/mashin.json`, `racas/soterrado.json`, `racas/trog_anao.json`. To unblock: fix the data and delete the flag — never bypass the guard.

7. ~~`npm run seed` aborts on `racas` ("no column named page")~~ — fixed by adding `page`, `livro_id`, `longevidade`, `devotos` columns and making `seedRacas` map explicitly. **Round 1**: `livro_id TEXT REFERENCES livros(id)` agora tem FK. If you change `db/schema.sql`, delete the local `db/tormenta20.sqlite3` (gitignored, generated) before re-seeding — `CREATE TABLE IF NOT EXISTS` will not add columns to an existing DB file.

## Commands

| Task | Command |
|---|---|
| Build DB (Ruby path) | `bundle exec rake build_db` (or `bin/build_db`) |
| Build DB (TS path) | `npm run seed` (also covers `npm publish` via `prepublishOnly`) |
| Ruby specs | `bundle exec rake` (= rspec + rubocop) or `bin/test` |
| Single Ruby spec | `bundle exec rspec spec/ruby/models/regra_spec.rb` *(needs DB already built)* |
| TS specs | `npm test` *(needs DB already built; `npm run seed` first)* |
| TS single file | `npx vitest run spec/ts/models/regra.test.ts` |
| TS coverage | `npm run coverage` (excludes `src/ts/seeder.ts`) |
| TS typecheck | `npx tsc --noEmit` |
| TS build → `dist/` | `npm run build` |
| Ruby lint | `bundle exec rubocop` |
| JSON lint | `find src/json -name "*.json" \| xargs bundle exec jsonlint` (install via `gem install jsonlint`) |
| Full local CI | `bin/ci` |
| Override DB path (TS) | `TORMENTA20_DB_PATH=/some/path.db npm run seed` |

## Project layout rules

- **`src/json/regras/*.json`** — rule entries. Shape: `{ id, name, description, page?, livro_id?, ...free-form }`. Free-form keys collapse into the `regra.data` JSON column (`seeder.ts:326`). Each rule has its own internal schema (e.g. `alcances.json` uses `categorias[]`, `critico.json` uses `margens[]/multiplicadores[]`). No per-rule JSON Schema. The TS/Ruby `Regra.data` getter just returns the blob.
- **`src/json/tabelas/*.json`** — generic `headers[]/rows[]` tables.
- **`src/json/indice_remissivo/<livro_id>.json`** — remissive index entries. File name **is** the `livro_id`. Each entry is `{ termo, pagina, tabela?, registro_id? }`. Without an entry, `bookReference()` returns `null` even if the entity exists.
- **`src/json/livros/*.json`** — book registry (`id`, `nome`, `nome_curto`). The DB columns are Portuguese, the JSON keys are Portuguese to match.
- `books/` — source PDFs for extraction work. Not consumed at runtime.

## Style and conventions

- Ruby: `.rubocop.yml` enforces double quotes, target 3.0, line length 200, **most complexity metrics disabled**.
- TS: strict mode, `Node16` modules, `"type": "module"`. `dist/` is built output.
- Ruby version pinned in `.ruby-version` (3.3.6). CI uses the same.
- Portuguese is the data language: descriptions, labels, rule names — even error messages.
- **Field-name convention is per-directory** — see the table above. There is no global "Portuguese or English" rule for field names; only the *values* are universally Portuguese.
- Gem relies on `libsqlite3` system lib (Debian/Ubuntu `apt install libsqlite3-0`, Alpine `apk add sqlite-libs`). macOS has it pre-installed; CI runs Ubuntu and installs nothing extra because it's pre-baked into the runner image.

## Tooling notes

- **CodeGraph** is available (`.codegraph/`). Use `codegraph_explore` for "how does X work" — most answers return in one call with source + call paths. Manual `grep`/`Read` loops repeat work the index already did.
- No `.opencode/opencode.json`, no pre-commit, no codegen pipeline beyond the seeders.
- Coverage uploaded to Codecov from both runtimes; ruby flag = `ruby`, ts flag = `typescript`. Tokens live in CI secrets.
- `vite/vitest`: coverage provider `v8`, output in `coverage/{ts,ruby}`.
- `typedoc` generates `docs/ts/**`; YARD generates `docs/ruby/**`. Deploy to GitHub Pages is `deploy-docs.yml` (path-filtered on `src/ts/**`, `typedoc.json`, `docs/**`, README).
- Publishing: `publish-gem.yml` for Ruby, `publish-npm.yml` for npm. Both run on tag releases. `npm version ${tag}` is run by CI.
