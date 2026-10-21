# Knowledge Query — Auditoria e linha de base (Fase 0)

> Documento vivo. **Status:** linha de base verde após Etapa 0 (inspeção, correção
> do gap `livros` em `db/seeds.rb`, criação de fixtures de avaliação) **e**
> limpeza do drift conhecido (9 lanes em 3 rounds, ver §0.1 abaixo).
>
> **Escopo confirmado**: este projeto **não vai adicionar `criaturas`** (Etapa 0.5
> do SPEC está descartada — sem tabela, schema, model ou JSON para monstros/NPCs
> de Ameaças de Arton). A base atual (Livro Básico + Ameaças como livro
> registrado/índice remissivo/racas/magias/acessorios/regras adicionais) é o
> escopo fechado da API de busca.

Esta página registra o que existe hoje no repositório em termos de estrutura
de dados, modelo de referências bibliográficas, fluxo de build e lacunas
conhecidas — tudo o que as Etapas 1–7 do
[`SPEC-tormenta20-knowledge-ai.md`](../SPEC-tormenta20-knowledge-ai.md)
precisam assumir como verdade.

A intenção é **não criar uma segunda representação manual de páginas ou
fontes**: tudo o que puder ser resolvido a partir do JSON canônico e da
tabela `indice_remissivo` deve ser resolvido a partir deles. Onde houver
lacuna, ela é registrada aqui como lacuna — não como dado inventado.

## 0.1 Histórico de drift cleanup (Etapa 0+)

Dois rounds de limpeza, **antes** de construir a API de busca em cima.
Estado final:

### Round 1 (4 lanes)

| Item                                | Antes                                  | Depois                                                  | Verificado por                                  |
|-------------------------------------|----------------------------------------|---------------------------------------------------------|-------------------------------------------------|
| `armas.properties` (TS ≠ Ruby)      | TS: `a.habilidades`; Ruby: `[hab, esp]` | ambos: `[a.habilidades, a.especial].flat().filter(Boolean)` | `adaga.properties` idêntico em ambos os DBs + `spec/ts/seeder.test.ts` |
| `itens.effects` (dropa `efeito`)   | ambos seeders liam só `effects`        | ambos: `effects ?? efeito ?? {}` via helper compartilhado `Tormenta20::Seeds.build_item_effects` | `batata_valkariana.effects` populada + `spec/ruby/db/seeds_itens_spec.rb` + `spec/ts/seeder.test.ts` |
| `melhorias.effects` (TS lê só `effects`, Ruby `efeito \|\| effects`) | TS perdia 35/37 melhorias | ambos: `efeito ?? effects ?? {}` | `spec/ts/seeder.test.ts`; seeders produzem DB idêntico |
| `TS bookReference` ignora `tabela`  | WHERE só `registro_id`                 | `getBookReferenceFor(registroId, tabela)` filtra ambos   | `spec/ts/concerns/book_referenceable.test.ts` distingue `bola_de_fogo` em `magias` (p188) vs `pocoes` (p347) |
| `TS bookReference` em 10/21 modelos | só 10 modelos expunham                 | 19 modelos (todos exceto `Livro`, que é o próprio sourcebook) | `spec/ts/concerns/book_referenceable.test.ts` smoke-tests para cada |
| `racas.livro_id` sem FK             | coluna órfã                           | `livro_id TEXT REFERENCES livros(id)`                   | `.schema racas` + `spec/ruby/db/schema_spec.rb` (FK listada + insert órfão rejeitado com `PRAGMA foreign_keys = ON`) |

### Round 2 (3 lanes)

| Item                                | Antes                                  | Depois                                                  | Verificado por                                  |
|-------------------------------------|----------------------------------------|---------------------------------------------------------|-------------------------------------------------|
| `db/seeds.rb` cobria 11/21 tabelas  | faltavam 10 importers                 | cobre todas 21 (incl. `IndiceRemissivo`, `Raca`, `Condicao`, `Pericia`, `Tabela`, `Pocao`, `AcessorioMagico`, `Encantamento`, habilidades_de_classe/raca) | `spec/ruby/db/seeds_spec.rb` cobre os transforms puros + wiring de `import_all`/`clear_all`/`print_summary` |
| Cobertura de `page` em `indice_remissivo` (TS ≠ Ruby) | TS só lia `indice_remissivo/*.json` (2063 rows); Ruby auto-registrava de `data["page"]` (2085) | TS agora chama `registerIndiceRemissivo(db, data, table)` após cada insert (2085 rows, paridade) | `npm run seed` em DB limpo produz exatamente 2085; `comm <(sqlite3 db1) <(sqlite3 db2)` zero diff |
| `Encantamento.armadurasEscudos` categoria | Ruby `"armadura_escudo"` (zero rows); TS `"armadura"` (25 rows) | ambos `"armadura"` (TS estava correto; Ruby corrigido) | DB: `armadura=25, arma=28`; spec `encantamento_spec.rb`/`.test.ts` assert count > 0 |
| `Pocao.medias` categoria | TS `"media"` (zero rows); Ruby `"medio"` (15 rows) | ambos `"medio"` (Ruby estava correto; TS corrigido) | DB: `menor=18, medio=15, maior=5`; specs assertam contagens |
| `Poder` sub-type scopes em Ruby | 4 scopes só em TS (`poderesCombate/poderesDestino/poderesMagia/habilidadesDeRaca`) | adicionados a Ruby (`poderes_combate/poderes_destino/poderes_magia/habilidades_de_raca`) | specs Ruby+TS contam rows por tipo |
| `Arma.melee` empty-string handling | Ruby só `range IS NULL`; TS `range IS NULL OR range = ''` | Ruby alinhado ao TS (`range IS NULL OR range = ''`); 56 armas, 35 NULL, 0 empty, 21 ranged | specs assertam contagens iguais nos dois lados |

Cobertura de testes:

| Suíte   | Baseline (Phase 0) | Após Round 1 | Após Round 2 | Após Round 3 | Δ total |
|---------|-------------------:|-------------:|-------------:|-------------:|--------:|
| Ruby    | 270                | 282          | 320          | 324          | +54     |
| TS      | 136                | 158          | 171          | 178          | +42     |
| **Total** | **406**          | **440**      | **491**      | **502**      | **+96** |

### Round 3 (2 lanes — últimos detritos)

| Item                                | Antes                                  | Depois                                                  | Verificado por                                  |
|-------------------------------------|----------------------------------------|---------------------------------------------------------|-------------------------------------------------|
| Typo `dimention` em todas as camadas | `magias.effect_dimention` ↔ JSON `effect_details.dimention` (51 arquivos) | renomeado atomicamente: JSON (51), JSON Schema, `db/schema.sql`, ambos os seeders, modelos Ruby+TS, AGENTS.md; coluna DB `effect_dimension` populada | `grep -ri dimention` retorna 0; `PRAGMA table_info(magias)` mostra `effect_dimension TEXT`; specs 324/178 |
| Comentário stale `db/schema.sql:316` | `-- 'arma' \| 'armadura_escudo'` (mas DB só tem `arma`/`armadura`) | `-- 'arma' \| 'armadura'` (28 encantamentos de arma, 25 de armadura) | diff visual |
| Multi-fonte explícita por entidade | `bookReference()` retorna uma única página; sem helper plural | TS: `getBookReferencesFor(registroId, tabela)` retorna `BookReference[]` ordenado por `(livro_id, pagina)`; 19 modelos ganham `bookReferences()`. Ruby: `#book_references` memoizado; `#book_reference` agora retorna `book_references.first&.dig(:formatted)` | `spec/ts/concerns/book_referenceable.test.ts` cobre `bola_de_fogo` (1 row cada tabela) e `espinhosa` (2 rows: Ameaças p401 + EJA p171); mesmo em Ruby. `docs/knowledge-query.md` §2.3, §6 e §10 #1 atualizados |

Cobertura de drift remanescente:
- ~~**Multi-fonte explícita por entidade**~~ **Resolvido (Round 3)** —
  sem tabela de junção (mantido), mas o helper plural
  `getBookReferencesFor(registroId, tabela)` em TS e `book_references`
  em Ruby expõem **explicitamente** todas as fontes (livro + página)
  de uma entidade. Sem inferência a partir de nome.
- ~~**`encode_dimention` (sic)**~~ **Resolvido (Round 3)** — renomeado
  `dimention` → `dimension` de forma atômica em todas as camadas
  (JSON, JSON Schema, `db/schema.sql`, ambos os seeders, modelos e docs)
  — ver §4 G.
- **`db/seeds.rb` segue fora do CI**: agora cobre as 21 tabelas, mas
  continua sendo código morto (nenhum workflow o invoca). Mantido por
  política "JSON é fonte da verdade".
- ~~**`db/schema.sql:316` comentário stale**~~ **Resolvido (Round 3)** —
  corrigido para `-- 'arma' | 'armadura'` (28 encantamentos de arma,
  25 de armadura).

**Restrição residual conhecida**: `db/seeds.rb` cobre as 21 tabelas mas
não é executável em runtime (`Models::Base#readonly? = true` faz
`save!` levantar `ActiveRecord::ReadOnlyRecord`). A transformação é
exercitada via testes de unidade. Mantido por convenção; ver §4 F.

---

## 1. Tabelas, views e contagens (estado pós-build)

O banco é gerado por `bin/build_db` (caminho Ruby usado por CI) e/ou
`src/ts/seeder.ts` (caminho TypeScript usado por `npm run seed`,
`prepublishOnly` e CI TS). O arquivo `db/tormenta20.sqlite3` é ignorado
pelo git — é artefato.

| # | Tabela                 | Registros¹ | Colunas relevantes para referência               |
|---|------------------------|-----------:|---------------------------------------------------|
| 1 | `racas`                | 47         | `page INTEGER`, `livro_id TEXT` (sem FK)          |
| 2 | `origens`              | 35         | sem `page`/`livro_id` (dropado pelo seeder)       |
| 3 | `poderes`              | 701        | sem `page`/`livro_id`                            |
| 4 | `divindades`           | 21         | sem `page`/`livro_id`                            |
| 5 | `classes`              | 14         | sem `page`/`livro_id`                            |
| 6 | `magias`               | 205        | sem `page`/`livro_id`                            |
| 7 | `armas`                | 56         | sem `page`/`livro_id`                            |
| 8 | `armaduras`            | 13         | sem `page`/`livro_id`                            |
| 9 | `escudos`              | 3          | sem `page`/`livro_id`                            |
| 10| `itens`                | 165        | sem `page`/`livro_id`                            |
| 11| `materiais_especiais`  | 28         | sem `page`/`livro_id`                            |
| 12| `melhorias`            | 37         | sem `page`/`livro_id`                            |
| 13| `encantamentos`        | 53         | sem `page`/`livro_id`                            |
| 14| `pocoes`               | 38         | sem `page`/`livro_id`                            |
| 15| `acessorios_magicos`   | 73         | sem `page`/`livro_id`                            |
| 16| `pericias`             | 29         | sem `page`/`livro_id`                            |
| 17| `condicoes`            | 35         | sem `page`/`livro_id`                            |
| 18| `regras`               | 27         | `data JSON` contém `page`/`livro_id` quando o JSON os traz |
| 19| `tabelas`              | 1          | n/a                                              |
| 20| `livros`               | 2          | é a fonte — `id`, `nome`, `nome_curto`           |
| 21| `indice_remissivo`     | 2 085      | `livro_id` (FK), `termo`, `pagina`, `tabela`, `registro_id` |

¹ Contagens obtidas após `bundle exec rake build_db` em ambiente limpo
(commit `6b7973c` "Adding ameaças de arton" + fix de `db/seeds.rb`).

**Views** (`db/schema.sql:580–607`):
- `magias_summary` — id, name, type, circle, school, execution, range, duration
- `poderes_por_tipo` — `type, count, GROUP_CONCAT(names)`
- `divindades_resumo` — id, name, title, energy, `json_array_length(granted_powers)`

Única chave estrangeira declarada em todo o schema:
`indice_remissivo.livro_id → livros(id)`. Demais `livro_id` (em
`racas.livro_id`) e referências lógicas (`registro_id` em
`indice_remissivo`, `spell_id` em `pocoes`, `class_id`/`origin_id` em
`poderes`) **não têm constraint**.

---

## 2. Modelo de referências bibliográficas

### 2.1 Como cada tipo de entidade carrega livro/página

O JSON fonte usa convenções por diretório (ver tabela em `AGENTS.md`).
A coluna de "page" na tabela DB existe **apenas para `racas`**.

| Entidade (dir JSON)              | Tabela DB               | `livro_id` na linha? | `page` na linha? | Onde fica, então? |
|----------------------------------|-------------------------|:---:|:---:|---|
| `racas/`                         | `racas`                 | ✓  | ✓  | primeira classe (`page INT`, `livro_id TEXT`) |
| `regras/`                        | `regras`                | —  | —  | dentro do blob `data JSON` |
| `armas/`, `armaduras/`, `escudos/` | …                    | —  | —  | via `indice_remissivo(tabela, registro_id)` |
| `equipamentos/itens/**`          | `itens`                 | —  | —  | via `indice_remissivo` |
| `itens_magicos/pocoes`           | `pocoes`                | —  | —  | via `indice_remissivo` |
| `itens_magicos/acessorios`       | `acessorios_magicos`    | —  | —  | via `indice_remissivo` |
| `itens_superiores/**`            | `materiais`/`melhorias`/`encantamentos` | — | — | via `indice_remissivo` |
| `poderes/**`                     | `poderes`               | —  | —  | via `indice_remissivo` |
| `magias/`                        | `magias`                | —  | —  | via `indice_remissivo` |
| `pericias/`                      | `pericias`              | —  | —  | via `indice_remissivo` |
| `classes/`, `origens/`, `deuses/`| `classes`/`origens`/`divindades` | — | — | via `indice_remissivo` |
| `condicoes/`                     | `condicoes`             | —  | —  | via `indice_remissivo` |
| `tabelas/`                       | `tabelas`               | —  | —  | via `indice_remissivo` (JSON não traz `page`) |
| `livros/`                        | `livros`                | (é a chave) | — | é a fonte dos livros |

### 2.2 Fontes múltiplas por entidade

**Suporte: parcial.**

- **Multi-fonte explícito por linha:** apenas `racas` (`livro_id` + `page`).
- **`regras`:** `page`/`livro_id` sobrevivem como chaves livres dentro do
  blob `regras.data` (5 arquivos os trazem; ex.: `regras_adicionais_de_ameacas.json`
  → `livro_id:"ameacas_de_arton"`, `page:376`). Não há coluna nem índice
  na build TS.
- **Tudo o mais:** uma entidade só pode estar ligada a mais de um livro
  via múltiplas linhas em `indice_remissivo` (cada uma com seu próprio
  `livro_id`). **Não há tabela de junção** e nenhuma entidade guarda um
  array de fontes.

### 2.3 Páginas múltiplas por entidade

**Representação: sim (no índice), exposição: parcial.**

Schema de `indice_remissivo` (`db/schema.sql:453–473`):

```sql
CREATE TABLE indice_remissivo (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  livro_id    TEXT    NOT NULL REFERENCES livros(id),
  termo       TEXT    NOT NULL,
  pagina      INTEGER NOT NULL,
  tabela      TEXT,
  registro_id TEXT,
  created_at, updated_at
);
CREATE INDEX idx_indice_termo    ON indice_remissivo(termo);
CREATE INDEX idx_indice_livro    ON indice_remissivo(livro_id);
CREATE INDEX idx_indice_registro ON indice_remissivo(tabela, registro_id);
CREATE UNIQUE INDEX idx_indice_livro_termo_pagina
  ON indice_remissivo(livro_id, termo, pagina);
```

- A chave única é `(livro_id, termo, pagina)` — o mesmo termo em páginas
  diferentes vira **linhas distintas**. O mesmo `registro_id` pode
  aparecer em várias páginas e em várias tabelas.
- Exemplos reais:
  - `Adaga` → `(t20_eja, 152, armas, adaga)`
  - `Bola de Fogo` → `(t20_eja, 188, magias)` **e** `(t20_eja, 347, pocoes)` — duas linhas, tabelas diferentes.
  - `Abençoado` → `(t20_eja, 82, NULL, NULL)` **e** `(t20_eja, 344, encantamentos)` — termo "órfão" coexistindo com a versão ligada.
- **Exposição:** o método público retorna **uma única** página.
  - Ruby `BookReferenceable#book_reference` filtra por
    `tabela=self.class.table_name, registro_id=id` e devolve só a
    primeira ocorrência (`spec/ruby/concerns/book_referenceable_spec.rb`
    trave esse comportamento).
  - TS `getBookReferenceFor(registroId, tabela)` (em
    `src/ts/models/concerns/book_referenceable.ts`) filtra por ambos
    `tabela` e `registro_id` e devolve a primeira ocorrência (via
    `getBookReferencesFor(...)[0]`) — paridade com Ruby.
    Diferenças: Ruby memoiza, TS não.
- **Multi-fonte explícita (adicionado nesta fase):** os dois lados agora
  expõem a lista completa de fontes de uma entidade, sem inferir nada.
  - TS: `getBookReferencesFor(registroId, tabela)` em
    `src/ts/models/concerns/book_referenceable.ts` (sem `LIMIT`, ordenado
    por `livro_id, pagina`); cada um dos 19 modelos com `bookReference()`
    também expõe `bookReferences(): BookReference[]` (array vazio se não
    indexado).
  - Ruby: `BookReferenceable#book_references` em
    `src/ruby/tormenta20/concerns/book_referenceable.rb` (ordena por
    `livro_id, pagina`, array vazio se não indexado). `#book_reference`
    passa a ser `book_references.first` — a assinatura singular não mudou.

### 2.4 Como o índice remissivo associa livro, termo, página e entidade

- **`livro_id` é coluna obrigatória na linha** (`NOT NULL`, FK para
  `livros(id)`). Sem FK row → índice remissivo rejeita.
- O seeder TS (`src/ts/seeder.ts:441–470`) deriva `livro_id` do **nome
  do arquivo** em `src/json/indice_remissivo/<livro_id>.json`.
- O seeder Ruby (`bin/build_db:566–580` + `:582–610`) faz o mesmo e,
  adicionalmente, faz **auto-registro**: para cada entidade importada
  cujo JSON traga `page` ou `pagina`, insere
  `(livro_id = data["livro_id"] || "t20_eja", termo = name, pagina, tabela, registro_id)`
  em `indice_remissivo`. Isso **amplia** a cobertura do índice quando
  uma entidade tem `page` no JSON mas não tem entrada manual no índice
  remissivo.

---

## 3. Texto livre vs dados estruturados

| Tabela               | Coluna(s) JSON | Forma do JSON (amostra) | Estruturado? |
|----------------------|----------------|--------------------------|---|
| `poderes`            | `effects` (array), `costs`, `prerequisites` | ex.: `ataque_poderoso.json` → `[{type:"attack_penalty", value:-2, duration:"instantanea"}, {type:"damage_improvement", value:5}]` | sim — objetos |
| `magias`             | `effects` (array), `enhancements` (array) | ex.: `bola_de_fogo.json` → `[{type:"dano", attribute:"pv", amount:"6d6", resistance_requirement:"reflexos"}]`; `enhancements:[{cost,type,description,extra_details}]` | sim — objetos |
| `itens`              | `effects` (objeto) | `elefante.json` → `{parceiro:{tipo, porte, pagina_criatura, patamar:{…}}, besta_de_carga:{…}}` (bloco de parceiro animal). Itens com `efeito` próprio (`batata_valkariana.json` → `{bonus:"+1d6", aplicacao:"...", duracao:"..."}`) agora chegam ao DB via fallback `effects ?? efeito ?? {}` (resolvido na limpeza de drift). | sim — parcial (parceiros + `efeito` opcional) |
| `materiais_especiais` | `effects` (objeto) | `adamante.json` → `{arma:{aumento_dano:"um_passo"}, armadura_leve:{reducao_dano:2}, …}` | sim — chaveado por tipo de item |
| `encantamentos`      | `efeito` (objeto) | `flamejante.json` → `{dano_extra:"1d6", tipo_dano_extra:"fogo", descricao_curta:"…"}` | sim |
| `melhorias`          | `effects` (objeto) | `envenenada.json` → `{doses_veneno_armazenadas:1, acao_aplicacao:"livre"}`. Seeder agora lê `efeito ?? effects ?? {}` (resolvido) | sim |
| `acessorios_magicos` | `efeito` (objeto) | `anel_da_protecao.json` → `{bonus_defesa:2}` | sim |
| `condicoes`          | `effects` (array) | `abalado.json` → `["-2 em testes de perícia"]` | **texto livre** |
| `regras`             | `data` (objeto) | `alcances.json` → `{categorias:[…], regras:{…}, page:149}`; `critico.json` → `{formato, valores_padrao, interpretacao, margens:[…]}`. Schema livre, regra a regra | **forma própria** |
| `tabelas`            | `headers` (array), `rows` (array) | `jogatina_resultados.json` → tabela plana | n/a |
| `racas`              | `attribute_bonuses`, `skill_bonuses`, `racial_abilities`, `available_chosen_abilities` | ex.: `hynne.json` → `attribute_bonuses:{destreza:2, …}`; `racial_abilities:["arremessador", …]` | sim — mas **`racial_abilities` é array de strings (slug de poder)**, não estruturado |

> Implicação para busca de efeitos (Etapa 4):
> - `poderes.effects`, `magias.effects`, `materiais_especiais.effects`,
>   `encantamentos.efeito`, `acessorios_magicos.efeito` e `racas` oferecem
>   estrutura utilizável. **São a prioridade** para a busca estruturada.
> - `condicoes.effects`, `regras.data` e `*.description` são texto livre.
>   Busca neles é **descoberta**, não prova.

---

## 4. Drift entre JSON, schema, DB gerado e modelos públicos

> Itens A–E foram resolvidos na limpeza de drift (ver §0.1).
> Itens F–H permanecem. Itens A–E abaixo descrevem **o que era**;
> a tabela em §0.1 mostra **o que ficou**.

A. ~~**TS `getBookReference` ignora `tabela`** (`book_referenceable.ts:27`):
   `registro_id="bola_de_fogo"` casa tanto em `magias` (p188) quanto em
   `pocoes` (p347). TS devolve `LIMIT 1` arbitrário; Ruby filtra por
   `tabela=self.class.table_name`.~~ **Resolvido**: a função foi
   renomeada para `getBookReferenceFor(registroId, tabela)` e filtra por
   ambos. Coberto por `spec/ts/concerns/book_referenceable.test.ts`.

B. ~~**TS expõe `bookReference` em apenas 10 dos 21 modelos**: arma, armadura,
   classe, divindade, escudo, item, magia, origem, poder, raca. **Faltam**:
   acessorio_magico, condicao, encantamento, livro, material_especial,
   melhoria, pericia, pocao, regra, tabela.~~ **Resolvido**: 19 modelos
   agora expõem (todos exceto `Livro`, que é o próprio sourcebook).

C. ~~**`armas.properties` diverge entre Ruby e TS**:
   - TS (`seeder.ts:284`) → `properties = data["habilidades"]` (só uma chave).
   - Ruby (`bin/build_db:336`) → `properties = [data["habilidades"], data["especial"]].flatten.compact` (merge das duas).~~ **Resolvido**:
   ambos agora produzem `[a.habilidades, a.especial].flat().filter(Boolean)`
   (TS extraído para `mapArma` puro + testado em
   `spec/ts/seeder.test.ts`).

D. ~~**Itens: `efeito` é dropado em massa**. 88 arquivos em
   `equipamentos/itens/**` usam `efeito`; **0** usam `effects`. Ambos
   seeders (`seeder.ts:320`, `bin/build_db:374`, `seeds.rb:323`) leem
   apenas `effects`.~~ **Resolvido**: ambos agora leem
   `effects ?? efeito ?? {}` (TS via `mapItem`; Ruby via
   `Tormenta20::Seeds.build_item_effects` extraído para
   `db/seeds_helpers.rb` e compartilhado entre `bin/build_db` e
   `db/seeds.rb`). Verificado: `batata_valkariana.effects` populada
   com `{"bonus":"+1d6","aplicacao":"...","duracao":"..."}`.

E. ~~**Melhorias: 35/37 arquivos usam `efeito`, 2 usam `effects`**. O seeder
   lê `efeito || effects` em `bin/build_db` e `seeds.rb`, mas só `effects`
   em `seeder.ts`.~~ **Resolvido**: TS agora lê `efeito ?? effects ?? {}`
   (via `mapMelhoria` puro); produz DB idêntico ao Ruby.

F. ~~**`db/seeds.rb` vs `bin/build_db`**~~ **Resolvido**:
   `db/seeds.rb` agora cobre as 21 tabelas (incluindo
   `IndiceRemissivo`, `Raca`, `Condicao`, `Pericia`, `Tabela`, `Pocao`,
   `AcessorioMagico`, `Encantamento`, habilidades_de_classe/raca).
   Continuam as duas ressalvas: (a) **fora do CI** — nenhum workflow
   invoca o script; o caminho real é `bundle exec rake build_db` →
   `bin/build_db`. (b) **Não executa em runtime** — `Models::Base#readonly?`
   faz `save!` levantar `ActiveRecord::ReadOnlyRecord`. A lógica pura é
   testada via `spec/ruby/db/seeds_spec.rb`; as escritas end-to-end
   permanecem não-verificadas. Política: manter em sincronia por
   "JSON é fonte da verdade", não por uso.

G. ~~**`encode_dimention` (sic)**: nome de coluna herdado com typo
   (`magias.effect_dimention` ↔ JSON `effect_details.dimention`). Não
   corrigir sem alinhar com o seeder.~~ **Resolvido**: renomeado
   `dimention` → `dimension` atomicamente nas 51 magias em
   `src/json/magias/`, em `src/schema/magia.schema.json`,
   `db/schema.sql`, `bin/build_db`, `db/seeds.rb`,
   `src/ruby/tormenta20/seeder.rb`, `src/ruby/tormenta20/models/magia.rb`,
   `src/ts/seeder.ts` e `docs/ruby/magias.md`.

H. ~~**Cobertura de índice remissivo por seeder**~~ **Resolvido**:
   TS `src/ts/seeder.ts` agora chama `registerIndiceRemissivo(db, data, table)`
   após cada insert, replicando `bin/build_db#register_indice_remissivo`.
   DB limpo via `npm run seed` produz exatamente 2085 rows em
   `indice_remissivo`, com paridade exata (via `comm`) com o caminho
   Ruby. Exemplo: `Rompedor da Realidade` →
   `(ameacas_de_arton, acessorios_magicos, p403, rompedor_da_realidade)`
   foi auto-registrado a partir do `page` do JSON.
   **Exceção documentada**: `regras` não é auto-registrado pelo TS
   porque Ruby também não (o `seed_regras` transforma o JSON e remove
   `page`); manter paridade > simetria mecânica.

---

## 5. Build, seed e determinismo

**Três caminhos de build**, com semânticas diferentes:

| Caminho                         | Chamado por                                       | Estratégia |
|---------------------------------|---------------------------------------------------|------------|
| `bundle exec rake build_db` → `bin/build_db` | `bin/test`, `bin/ci`, `Rakefile`, gem packaging | **deleta** o `.sqlite3`, recria do zero |
| `npm run seed` → `src/ts/seeder.ts` | `prepublishOnly`, CI TS, docs deploy | abre o DB existente, `INSERT OR REPLACE`, deixa sobras |
| `ruby db/seeds.rb` (legado)     | só execução direta (não chamado em CI)            | `find_or_initialize_by` (upsert) |

**Determinismo lógico (dados):** SIM — ambos seeders chaveiam por PK
e usam upserts; ordem de `Dir.glob`/`readdirSync` não afeta o conteúdo
da linha.

**Determinismo binário (byte-a-byte):** NÃO.

- `created_at`/`updated_at` usam `DATETIME DEFAULT CURRENT_TIMESTAMP` e
  trigger `AFTER UPDATE`. Nenhum seeder os seta; rebuilds diferem.
- `indice_remissivo.id` é `INTEGER PRIMARY KEY AUTOINCREMENT` e nenhum
  seeder o fornece → IDs dependem da ordem de inserção.
- `readdirSync`/`Dir.glob` **sem `.sort`** em ambos seeders
  (`seeder.ts:31–36`, `:441–470`; `bin/build_db:653`; `seeds.rb:455`).
  Mitigação: PK-upsert. Mas o ID do índice remissivo e o layout WAL
  variam.
- Sem `Math.random`/`Date.now`/`rand`/`shuffle` em nenhum seeder.

> Implicação para Etapa 6 (qualidade/avaliação): o conjunto de
> perguntas/respostas é avaliado contra **dados determinísticos** (por
> PK), nunca contra o hash do arquivo. Toda comparação de "build
> reproduzível" deve se dar por linha, não por arquivo.

---

## 6. `bookReference` hoje (Ruby e TS)

| Aspecto                            | Ruby (`book_referenceable.rb`) | TS (`book_referenceable.ts`) |
|------------------------------------|--------------------------------|------------------------------|
| Incluso em quais modelos?          | todos os 21 (via `Base`)       | 19 (todos exceto `Livro`, que é o sourcebook) |
| Função de lookup                   | `BookReferenceable#_indice_entry` (escopo AR) | `getBookReferenceFor(registroId, tabela)` |
| Filtro na consulta                 | `tabela = self.class.table_name AND registro_id = id` | `tabela = ? AND registro_id = ?` (paridade com Ruby) |
| `LIMIT`                            | `find_by` (1ª ocorrência)      | `LIMIT 1` (agora correto, mesmo filtro) |
| Eager-load                         | sim (`includes(:livro)`)       | JOIN explícito |
| Memoização                         | sim (`@_indice_entry`)         | não |
| Retorno                            | string `"T20 - EJA, p. 56"`    | objeto `{livro, pagina, formatted}` |
| Acesso granular                    | `book_reference`, `page`, `book`, `full_book` | um único `bookReference()` |
| Coberto por teste                  | `spec/ruby/concerns/book_referenceable_spec.rb` (com mocks + caso sem entrada) | `spec/ts/concerns/book_referenceable.test.ts` (filtro por `tabela`, ausência, shape, smoke de 9 modelos) |

Ausência de referência é tratada: ambos retornam `nil` (Ruby) / `null`
(TS) sem lançar.

> **Há helper para a lista completa de fontes** em ambos os lados:
> `getBookReferencesFor`/`bookReferences()` no TS e
> `BookReferenceable#book_references` no Ruby — ver §2.3. Os helpers
> singulares (`bookReference`/`book_reference`) continuam retornando
> apenas a primeira ocorrência. O plural é o pré-requisito da Etapa 4
> (`searchEffects`) para distinguir "mencionado em uma fonte" de
> "apoiado por múltiplas fontes".

---

## 7. Gap conhecido — `db/seeds.rb` não importava `livros`

**Sintoma:** o schema define `livros(id, nome, nome_curto)`, `src/json/livros/`
tem 2 arquivos (`t20_eja.json`, `ameacas_de_arton.json`) e ambos os
seeders canônicos (`bin/build_db`, `src/ts/seeder.ts`) já os importam.
Mas o seeder legado ActiveRecord (`db/seeds.rb`) não tinha nenhum
`import_livros`, omitia `Models::Livro` do `clear_all` e da
`print_summary`. Consequência: `db/seeds.rb` deixava a tabela `livros`
vazia se invocado diretamente — e qualquer `book_reference` ou join
`indice_remissivo → livros` feito por modelos AR a partir dele falhava
em silêncio (a tabela existia, o registro não).

**Correção aplicada nesta Fase 0** (`db/seeds.rb`):
- novo `import_livros` no início de `import_all` (lê
  `src/json/livros/*.json`, faz `find_or_initialize_by(id:)` e grava
  `nome`/`nome_curto`);
- `Models::Livro` adicionado a `clear_all`;
- `Livros: N` exibido em `print_summary`.

**Verificação:** `bundle exec ruby db/seeds.rb` agora importa 2 livros,
correspondendo aos 2 arquivos em `src/json/livros/`. O caminho canônico
`bin/build_db` permanece inalterado (já estava correto) e a linha de
base verde se mantém.

> Nota: `db/seeds.rb` continua sendo legado (não é invocado por nenhum
> workflow CI). Mantê-lo alinhado com `bin/build_db` é, ainda assim,
> parte do contrato "JSON é fonte da verdade, dois seeders devem
> concordar" declarado em `AGENTS.md`.

---

## 8. Linha de base (commit `6b7973c` + Fase 0)

| Verificação              | Resultado                                                                                  |
|--------------------------|--------------------------------------------------------------------------------------------|
| Ruby specs               | `bundle exec rspec` → **320 examples, 0 failures** (`spec/ruby/`; +50 vs baseline 270)   |
| Ruby lint (tocados)      | `bundle exec rubocop db/seeds.rb db/seeds_helpers.rb bin/build_db spec/ruby/db/` → **no offenses** |
| TS specs                 | `npm test` → **171 tests passed, 26 files** (`spec/ts/`; +35 vs baseline 136)             |
| TS typecheck             | `npx tsc --noEmit` → **clean**                                                             |
| Build Ruby               | `bundle exec rake build_db` → **OK**, `livros: 2`, `indice_remissivo: 2085`               |
| Build TS                 | `npm run seed` em DB limpo → **OK**, `indice_remissivo: 2085` (paridade exata com Ruby)  |
| FK enforcement           | `PRAGMA foreign_keys = ON; INSERT INTO racas VALUES (..., 'livro_inexistente')` → **FOREIGN KEY constraint failed (19)** |
| `bola_de_fogo` lookup    | `tabela=magias → p188`, `tabela=pocoes → p347` (distintos, filtro de `tabela` ativo)      |
| DB file                  | `db/tormenta20.sqlite3` — **gitignored** (gerado); regerado a cada `rake build_db`        |

---

## 9. Avaliação — fixtures de perguntas reais

Conjunto inicial de perguntas, ancoradas em dados reais do banco. Serão
usadas como fixtures de teste nas Etapas 2, 3, 4 e 6. Cada item lista
o **resultado esperado** (o que esperamos que apareça) e o **resultado
proibido** (o que esperamos que **não** apareça). Atualizar após cada
etapa conforme a busca revelar limites.

> Não preencher a coluna "resultado esperado" significa "ainda a
> definir" — registrar explicitamente essa indefinição é parte da
> auditoria.

| #  | Pergunta (PT-BR)                                          | Esperado aparece                                                                 | Proibido aparecer                         | Status |
|----|-----------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------|--------|
| 1  | Quais itens dão bônus em Intimidação?                     | itens cuja `description` ou `effects` mencione Intimidação **e** bônus numérico  | itens só com menção incidental             | a definir |
| 2  | Quais poderes melhoram Intimidação?                       | poderes em `poderes_conciledidos`/`poderes_gerais` com `effects` referindo Intimidação | magia `Bola de Fogo`                     | a definir |
| 3  | Quais magias mencionam Intimidação?                       | magias com `description`/`effects` mencionando Intimidação                       | regras genéricas                          | a definir |
| 4  | Onde a regra de Intimidação é explicada?                   | `regras`/`pericias` que descrevam a perícia + entradas em `indice_remissivo`     | —                                         | a definir |
| 5  | Quais efeitos dão +2 ou mais?                              | entradas com `effects[].value ≥ 2` em `poderes`/`magias`/`encantamentos`        | efeitos sem `value` numérico              | a definir |
| 6  | Buscar entidade "Adaga" pelo nome exato                   | `armas(id="adaga")`                                                              | outros itens/armas                        | determinístico (id) |
| 7  | Onde aparece "Allihanna"?                                 | `divindades(id="allihanna")` + entradas em `indice_remissivo(tabela="divindades")` | —                                       | determinístico (id) |
| 8  | Quais requisitos o poder X tem?                            | `poderes(id=X).prerequisites` (JSON)                                              | —                                         | determinístico (id) |
| 9  | Buscar com acentos diferentes ("Intimidacao")              | mesmas entidades da #1                                                          | —                                         | a definir (normalização) |
| 10 | Buscar "xyzzy123" (não existe)                             | `results: []`                                                            | nada                                      | determinístico |
| 11 | Criaturas de ND ≥ 5 no livro Ameaças de Arton              | — | — | **fora de escopo** (Etapa 0.5 descartada) |
| 12 | Quais monstros são mortos-vivos?                          | — | — | **fora de escopo** (Etapa 0.5 descartada) |
| 13 | Criaturas com resistência a fogo                           | — | — | **fora de escopo** (Etapa 0.5 descartada) |
| 14 | Onde o monstro X aparece em Ameaças de Arton?              | — | — | **fora de escopo** (Etapa 0.5 descartada) |

### Amostras reais atualmente verificáveis (sem precisar de `criaturas`)

Para ganhar confiança antes de automatizar, abaixo estão 3 amostras
executadas contra o DB atual (válidas já na linha de base).

```text
# 6 — busca por nome exato "Adaga"
sqlite> SELECT id, name, category FROM armas WHERE id = 'adaga';
adaga|Adaga|simples

# 7 — onde aparece "Allihanna"
sqlite> SELECT ir.pagina, l.nome_curto, ir.tabela
        FROM indice_remissivo ir JOIN livros l ON ir.livro_id = l.id
        WHERE ir.registro_id = 'allihanna';
103|T20 - EJA|divindades

# 10 — "xyzzy123" não existe
sqlite> SELECT * FROM armas WHERE id = 'xyzzy123';
(empty)
```

---

## 10. Riscos e decisões registradas nesta fase

> Após Round 1 (4 itens resolvidos), Round 2 (3 itens resolvidos) e
> Round 3 (multi-fonte explícita), todos os itens desta fase estão
> resolvidos.

1. ~~**Resolução multi-fonte.**~~ **Resolvido (Round 3)** — sem tabela
   de junção, multi-fonte existe como múltiplas linhas em
   `indice_remissivo` e agora é exposto explicitamente por
   `getBookReferencesFor` + `bookReferences()` (TS) e
   `BookReferenceable#book_references` (Ruby), ordenados por
   `livro_id, pagina`; array vazio quando não indexado. Ver §2.3.
2. ~~**Drift TS vs Ruby nas mesmas entradas.**~~ **Resolvido
   (Round 1)** — `armas.properties`, `itens.effects` e
   `melhorias.effects` agora idênticos nos dois seeders.
3. ~~**`db/seeds.rb` legado.**~~ **Resolvido (Round 2)** — agora
   cobre as 21 tabelas. Continua fora do CI por design, e a
   transformação só é exercitada via testes de unidade
   (`Models::Base#readonly?` bloqueia runtime).
4. ~~**Cobertura de `page`.**~~ **Resolvido (Round 2)** —
   `npm run seed` em DB limpo produz 2085 rows em `indice_remissivo`,
   paridade exata com Ruby.
5. ~~**Sem FK em `racas.livro_id`.**~~ **Resolvido (Round 1)** —
   FK adicionada; enforcement verificado por `spec/ruby/db/schema_spec.rb`.
6. ~~**TS `bookReference` ignora `tabela`.**~~ **Resolvido (Round 1)** —
   `getBookReferenceFor(registroId, tabela)` filtra por ambos; 19
   modelos expõem o método.

---

## 11. O que esta fase **não** faz (escopo das Etapas 1+)

- Não cria o módulo `src/ts/knowledge/` — é a Etapa 2.
- Não cria tipos `SearchResult`/`SourceReference` — é a Etapa 1.
- Não cria normalização de texto (sem acentos, caixa, sinônimos) — Etapa 2.
- **Não cria `criaturas` (Ameaças de Arton) — Etapa 0.5 descartada.** Sem
  tabela, schema, model ou JSON para monstros/NPCs. As perguntas 11–14 da
  §9 ficam fora do escopo da API de busca.
- Não cria o servidor MCP — Etapa 5.
- Não cria camada de LLM interpretativa — Etapa 7 (mediante uso real).

---

*Próxima revisão: ao fim da Etapa 1 (modelo `SearchResult`/`SourceReference`).
O helper de múltiplas fontes já está documentado em §2.3
(`getBookReferencesFor`/`bookReferences()` no TS e
`BookReferenceable#book_references` no Ruby), expondo o que existe em
`indice_remissivo` sem inferir.*