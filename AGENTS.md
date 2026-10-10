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
| `magias/` | Mixed; English core (`id`, `name`, `type`, `circle`, `school`, `execution`, `range`, `target`, `effect`, `duration`, `extra_costs`, `description`, `enhancements`, `effects`, `counterspell`); Portuguese spellbook legacy (`resistence`, `effect_details.dimention` [sic — typo for `dimension`]) | `circle` is a **string** `"2"`, not an int. Some fields like `resistence.effect` have trailing `\|` artifacts from the source. Do not "fix" the typos without checking the seeder. |
| `equipamentos/armas/` | English (`id`, `name`, `type`, `description`, `page`); Portuguese (`proficiencia`, `proposito`, `empunhadura`, `preco`, `dano`, `critico`, `alcance`, `tipo_dano`, `espacos`, `habilidades`, `especial`) | `type` is always `"arma"`, `proficiencia` carries the category (`simples`/`marcial`/`exotica`/`fogo`) |
| `equipamentos/armaduras/` | English (`id`, `name`, `type`, `description`); Portuguese (`categoria`, `preco`, `bonus_defesa`, `penalidade_armadura`, `espacos`, `especial`, `vestir_remover`) | `type` is always `"armadura"`; `categoria` is `leve`/`pesada` |
| `equipamentos/escudos/` | Same as armaduras, plus `ataque` object with Portuguese keys | `type` is always `"escudo"` |
| `equipamentos/itens/**/` | English (`id`, `name`, `type`, `description`, `page`); Portuguese core (`categoria`, `preco`, `espacos`); extra Portuguese fields per item type (`cd_fabricacao`, `uso`, `conta_como_vestido`, `doses_veneno_armazenadas`, etc.) | Look at siblings in the same leaf folder before adding new fields. `animais/` files carry a `parceiro` block with `tipo[]` (array: `montaria`/`perseguidor`/`especial`/`besta_de_carga`), `porte`, `pagina_criatura`, `patamares.{iniciante,veterano,mestre}` (per-tier `movement[]`/`damage[]`/`attack[]`/`defense[]`/`skill_bonus[]`/`saving_throw[]`/`senses[]`/`maneuvers[]`/`powers[]`/`extra_actions[]`/`terreno[]`/`special[]`), plus optional `besta_de_carga`, `alternativo`, `restricoes[]`, `isento_restricao_cavalgar_combate`. Both seeders merge these into the `itens.effects` JSON column. |
| `itens_superiores/materiais_especiais/` | English (`id`, `name`, `description`, `page`); Portuguese (`type`, `aparencia`, `origem`, `precos_adicionais`, `efeitos` — plural, with per-item-type nested objects) | No `applicable_to` array |
| `itens_superiores/melhorias/**/` | English (`id`, `name`, `description`, `page`); Portuguese (`type`, `categoria`, `efeito` — singular, `prerequisitos`) | The seeder reads `efeito` only for encantamentos, not melhorias; melhorias `efeito` data is currently NOT written to the DB (seeder bug, see gotcha #6) |
| `itens_superiores/encantamentos/**/` | English (`id`, `name`, `description`, `page`); Portuguese (`type`, `categoria`, `efeito` — singular) | Inside `efeito`: Portuguese keys like `dano_extra`, `tipo_dano_extra` |
| `itens_magicos/pocoes/` | Portuguese-heavy: `subtipo`, `pm_cost`, `categoria`, `preco`, `roll_min`, `roll_max`, `aprimoramento`; English: `id`, `name`, `spell_id`, `description`, `page` | |
| `itens_magicos/acessorios/` | English (`id`, `name`, `description`, `page`); Portuguese (`categoria`, `preco`, `roll_min`, `roll_max`, `efeito` — singular) | `categoria` is `menor`/`medio`/`maior`/`artefato` |
| `condicoes/` | English (`id`, `name`, `description`, `effects`, `condition_type`, `escalates_to`, `page`) | `effects` is a loose list of Portuguese effect descriptions, not structured |
| `regras/` | English core (`id`, `name`, `description`, `page`, `livro_id`) + free-form per-rule keys (e.g. `categorias`, `margens`, `multiplicadores`) | Free-form keys collapse into the `regra.data` JSON column. Treat them as English field names, but the *values* are typically Portuguese. |
| `tabelas/` | English (`id`, `name`, `description`, `headers`, `rows`, `page`, `livro_id`) | `headers`/`rows` are simple arrays |
| `livros/` | Portuguese (`id`, `nome`, `nome_curto`) | DB column names match |
| `indice_remissivo/<livro_id>.json` | Portuguese (`termo`, `pagina`, `tabela`, `registro_id`) — entry-level | DB column names match |

**Bottom line: when adding a new file, copy the structure of an existing sibling from the basic book.** When in doubt, run `grep -l "your_key" src/json/<dir>/` and copy the pattern. Do not invent a new convention for an existing directory.

## Free-form reference: how the DB columns relate to JSON keys

The two seeders (`src/ts/seeder.ts`, `db/seeds.rb`) translate per-table. Some are clean 1:1 (e.g. `pericias.atributo` → `pericias.atributo`); others have aliases (`armas.proficiencia` → `armas.category` via `ARMA_CATEGORY_MAP`). When you change a JSON key, check `seeder.ts` to see if you also broke a column.

Known translation sites (TS seeder):
- `armas`: `proficiencia`→`category`, `preco`→`price`, `dano`→`damage`, `tipo_dano`→`damage_type`, `critico`→`critical`, `alcance`→`range`, `espacos`→`weight`, `habilidades`→`properties`
- `armaduras`/`escudos`: `preco`→`price`, `bonus_defesa`→`defense_bonus`, `penalidade_armadura`→`armor_penalty`, `espacos`→`weight`, `habilidades`→`properties`
- `itens`: `preco`→`price`, `espacos`→`weight`, `category`/`categoria`→`category`
- `poderes`: `requirements`→`prerequisites`, plus `type` is set per-directory (`PODER_DIR_TYPE_MAP`)
- `magias`: `resistence`→split into `resistence_effect`/`resistence_skill`, `target` flattened into `target_amount`/`target_up_to`/`target_type`, `effect_details.other_details`→`effect_other_details`

## Critical gotchas

1. **Runtime DB is read-only.** `src/ruby/tormenta20/models/base.rb:41` makes every ActiveRecord model `readonly? = true`; class-level writes (`create`, `update_all`, `delete_all`, …) raise `ReadOnlyError`. The DB ships pre-populated. Re-run the seeder to apply data changes — do not try to write through ActiveRecord.

2. **JSON is the source of truth, not the models.** Editing only `src/ts/models/*` or `src/ruby/tormenta20/models/*` has zero runtime effect on consumers (they read the seeded DB). To change data: edit `src/json/**` and re-seed.

3. **Build order matters.** Both CI jobs run `bundle exec rake build_db` / `npm run seed` **before** tests, because specs exercise the seeded DB. Locally the same applies: `rake` auto-runs `build_db` via `Rakefile:24` (`Rake::Task[:spec].enhance([:build_db])`), but TS does **not** — `npm test` requires `npm run seed` to have been run first in this checkout. If a TS spec fails with "no such table", the DB wasn't rebuilt.

4. **Two seeders must agree.** `db/seeds.rb` (Ruby, used by CI test-ruby) and `src/ts/seeder.ts` (TS, used by CI test-ts + `npm run seed` + npm publish) write the same `.sqlite3` from the same `src/json/`. When you add a new top-level JSON folder or a new column, update both seeders — or whichever one CI actually runs locally. Field renames (e.g. `proficiencia` → `category`, `preco` → `price` in `armas`/`armaduras`) live in the seeder transforms; the JSON keeps the basic-book keys.

5. **`Rakefile:24` enhancements apply to user-run `rake` but not `rspec` directly.** `bundle exec rake` builds the DB then runs specs; `bundle exec rspec spec/models/regra_spec.rb` does not — it expects a pre-built DB at `db/tormenta20.sqlite3` or it fails. Use `bin/test` or `bin/ci` wrappers that build first.

6. **Melhorias `efeito` is dropped by the TS seeder.** `seedItensSuperiores` reads `applicable_to`, `price`, `effects` — *not* `efeito`. Existing melhoria files (e.g. `envenenada.json`, `sedenta.json`) use `efeito`, so that data never reaches the DB. Either rename the keys or extend the seeder before you trust any melhoria row. Same applies to `materiais_especiais.applicable_to` (hardcoded to `[]` in `seeder.ts:280`).

7. ~~`npm run seed` aborts on `racas` ("no column named page")~~ — fixed by adding `page`, `livro_id`, `longevidade`, `devotos` columns and making `seedRacas` map explicitly. If you change `db/schema.sql`, delete the local `db/tormenta20.sqlite3` (gitignored, generated) before re-seeding — `CREATE TABLE IF NOT EXISTS` will not add columns to an existing DB file.

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