# Spec de implementação — Knowledge Query e integração com IA

**Projeto:** `tormenta20-knowledge`  
**Status:** proposta de implementação editável  
**Objetivo:** tornar os dados da biblioteca consultáveis por linguagem natural e por ferramentas de IA, sem acoplar o núcleo a um fornecedor/modelo de IA.

---

## 1. Objetivo e visão

Evoluir a biblioteca existente para que seja, no mesmo repositório, uma base consultável de conhecimento de Tormenta20, com interfaces para aplicações e agentes de IA.

Exemplo de pergunta:

> Quais itens dão bônus em Intimidação?

Resposta esperada: resultados encontrados nos dados da biblioteca, com descrição do efeito e referências bibliográficas precisas (livro e página). A aplicação não deve inventar nomes, valores, regras ou fontes.

### Princípios

1. **A base de dados é a fonte da verdade.** O modelo de IA interpreta e apresenta; não substitui os dados.
2. **AI-provider agnostic.** O núcleo não importa SDKs da OpenAI, Anthropic, Google ou outros provedores.
3. **Começar sem embeddings.** Primeiro explorar SQLite, campos estruturados, referências e busca textual. Adicionar busca vetorial apenas se testes demonstrarem uma lacuna real.
4. **Proveniência obrigatória.** Todo resultado deve manter sua entidade de origem e, quando disponível, livro, página e trecho de evidência.
5. **Não confundir encontrado com inferido.** Uma entidade cuja descrição menciona Intimidação não deve ser apresentada automaticamente como fornecendo um bônus numérico.
6. **Compatibilidade.** Evitar mudanças incompatíveis nas APIs Ruby, TypeScript e Python já existentes.
7. **Uma implementação, várias interfaces.** Biblioteca de consulta, CLI, MCP e eventual REST devem chamar o mesmo núcleo.

## 2. Escopo

### MVP — incluído

- **Adicionar o livro "Ameaças de Arton" à base de dados**, incluindo criaturas, monstros e NPCs com seus atributos, habilidades, estatísticas e referências bibliográficas.
- Auditar e normalizar as referências a livro/página já adicionadas ao repositório.
- API TypeScript de consulta local ao SQLite distribuído com a biblioteca.
- Busca por nome, texto, categoria/tipo e filtros simples.
- Resultados com identificador, tipo, descrição, relevância e fontes.
- Busca de regras e entidades usando o índice remissivo como pista complementar.
- Consulta focada em efeitos/modificadores com distinção entre dados estruturados e possíveis correspondências textuais.
- Servidor MCP no próprio repositório, expondo ferramentas de consulta seguras e documentadas.
- Testes automatizados e documentação de uso.

### Fora do MVP

- Treinar ou fazer fine-tuning de modelos.
- Criar um grafo de conhecimento/instalar Neo4j.
- Exigir PostgreSQL, serviço remoto ou API key para consultas locais.
- Implementar um motor completo de cálculo de personagem/combate.
- Fazer extração automática de novos PDFs como requisito para uso da biblioteca.
- Colocar um fornecedor de LLM como dependência obrigatória.
- Embeddings e vector database antes de medir a qualidade da busca lexical/estruturada.

## 3. Arquitetura proposta

```text
Aplicação / Agente de IA
        │
        ├── MCP (primeira interface de IA)
        ├── API TypeScript (uso programático local)
        └── REST HTTP (opcional, fase posterior)
                 │
                 ▼
          Query / Knowledge Engine
          ├── validação de entrada
          ├── busca estruturada
          ├── busca textual
          ├── índice remissivo
          ├── fusão/ranking de resultados
          └── resolução de fontes e páginas
                 │
                 ▼
           SQLite existente
          ├── entidades T20
          ├── descrições e efeitos
          ├── livros/referências
          └── índice remissivo
```

### Escolha tecnológica

Usar **TypeScript/Node.js** para o núcleo novo e o MCP, acompanhando o ecossistema que o repositório já usa (`type: module`, TypeScript, `better-sqlite3` e Vitest). O acesso ao SQLite deve seguir os padrões de conexão e distribuição da biblioteca já existentes.

O MCP é uma interface útil para clientes compatíveis, mas não deve ser o único contrato. Qualquer aplicativo pode consumir a API TypeScript diretamente; um REST simples pode ser adicionado depois para clientes que não suportam MCP. O núcleo não deve conhecer MCP nem HTTP.

### Dependências novas

- MCP SDK oficial para TypeScript, como dependência isolada do módulo MCP.
- Nenhuma dependência de provedor de LLM no MVP.
- Nenhum banco externo adicional no MVP.

Confirmar a versão corrente do SDK MCP e sua compatibilidade com a versão de Node já declarada no projeto antes de adicionar a dependência.

## 4. Fase 0 — auditoria e inventário (pré-requisito)

Antes de alterar o schema, inspecionar a implementação atual e registrar o resultado em `docs/knowledge-query.md`.

### Verificações

- [ ] Listar as tabelas e views presentes no SQLite gerado.
- [ ] Identificar como cada tipo de entidade associa livro e página: coluna, JSON, método derivado ou tabela de relacionamento.
- [ ] Confirmar se a referência suporta uma ou várias fontes por entidade.
- [ ] Confirmar como páginas são representadas quando a entidade aparece em mais de uma página.
- [ ] Confirmar como o índice remissivo associa `livro`, `termo`, `página` e entidade.
- [ ] Identificar quais descrições e efeitos estão em texto livre e quais já são dados estruturados.
- [ ] Verificar diferenças entre o JSON de origem, `schema.sql`, banco gerado e os modelos públicos.
- [ ] Confirmar estratégia de build/seed e se a geração do banco é determinística.
- [ ] Criar fixtures e exemplos reais para pelo menos armas, itens, poderes, magias e regras.

### Regra importante

Não criar uma segunda representação manual de páginas se o dado já existe. Criar adaptadores ou views sobre a fonte atual. Se a auditoria encontrar lacunas, documentar explicitamente quais registros não possuem fonte conhecida.

## 5. Contratos e modelos públicos

Os nomes abaixo são uma proposta inicial. Ajustar ao estilo já adotado no pacote antes de publicar a API.

### 5.1 Tipos básicos

```ts
export type EntityType =
  | 'arma'
  | 'armadura'
  | 'escudo'
  | 'item'
  | 'melhoria'
  | 'encantamento'
  | 'material_especial'
  | 'pocao'
  | 'magia'
  | 'poder'
  | 'classe'
  | 'origem'
  | 'raca'
  | 'divindade'
  | 'condicao'
  | 'regra'
  | 'criatura'          // monstros e criaturas (Ameaças de Arton)
  | 'npc';              // NPCs notáveis (Ameaças de Arton)

export interface SourceReference {
  bookId?: string;
  bookName?: string;
  bookAbbreviation?: string;
  page?: number;
  formatted?: string;
  url?: string;
}

export interface SearchResult {
  id: string;
  type: EntityType;
  name: string;
  description?: string;
  sources: SourceReference[];
  matchedBy: Array<'name' | 'description' | 'effect' | 'index' | 'structured'>;
  score?: number;
  evidence?: string[];
}
```

Os campos opcionais só devem ser incluídos se realmente existirem. Não inventar páginas, nomes de livro nem valores ausentes. `score` é sinal interno de ordenação e não deve ser descrito ao usuário como probabilidade de verdade.

### 5.2 Busca geral

```ts
export interface SearchOptions {
  query: string;
  types?: EntityType[];
  limit?: number;       // default 10; validar faixa máxima
  bookIds?: string[];
  includeIndex?: boolean;
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
  total?: number;       // quando calcular o total for viável
}

export function searchKnowledge(options: SearchOptions): SearchResponse;
```

Requisitos:

- Rejeitar consulta vazia ou maior que o limite documentado.
- Validar `limit` e limitar o máximo (sugestão inicial: 50).
- Fazer binding de parâmetros SQL; nunca interpolar query diretamente em SQL.
- Normalizar acentos e caixa para comparar termos em português, preservando o nome original no resultado.
- Não retornar todas as colunas internas do banco por padrão.

### 5.3 Busca de entidade por ID

```ts
export interface GetEntityOptions {
  id: string;
  type?: EntityType;
}

export function getEntity(options: GetEntityOptions): SearchResult | null;
```

Deve retornar a entidade completa de acordo com o contrato público apropriado, mais as fontes resolvidas. Uma busca por ID precisa ser determinística e não passar por ranking semântico.

### 5.4 Busca de modificadores/efeitos

```ts
export interface EffectSearchOptions {
  target?: string;        // exemplo: "Intimidação"
  operation?: 'bonus' | 'penalty' | 'any';
  entityTypes?: EntityType[];
  minValue?: number;
  maxValue?: number;
  limit?: number;
}

export interface EffectSearchResult extends SearchResult {
  effectEvidence: Array<{
    text: string;
    value?: number;
    operation?: string;
    target?: string;
    classification: 'structured' | 'text_match' | 'unclassified';
  }>;
}

export function searchEffects(options: EffectSearchOptions): EffectSearchResult[];
```

O resultado deve distinguir:

- `structured`: alvo e modificador podem ser demonstrados pelos campos de dados;
- `text_match`: a descrição menciona termos relevantes, mas o modificador não foi normalizado;
- `unclassified`: possível relação encontrada, ainda sem classificação confiável.

No MVP, a API não deve declarar que um resultado fornece `+N` se esse valor não puder ser extraído de um campo estruturado ou de evidência textual inequívoca validada. Preferir retornar a evidência para revisão a inferir uma regra.

## 6. Estratégia de busca

Implementar incrementalmente, na seguinte ordem.

### 6.1 Busca estruturada

Usar consultas SQL para IDs, tipo, categoria, atributos, requisitos e outros campos que já existem no schema. Para perguntas com filtro explícito, essa deve ser a fonte prioritária.

### 6.2 Busca textual

Criar uma camada de busca sobre nome, descrição, efeitos e campos de texto relevantes. Avaliar SQLite FTS5 após validar se o SQLite embarcado e o processo de build o suportam nos ambientes-alvo. Se não, iniciar com busca lexical normalizada e índices adequados.

Requisitos da normalização:

- caixa indiferente;
- comparação sem acentos;
- tratamento de espaços e pontuação;
- preservar a grafia original de apresentação;
- tratar aliases/sinônimos por dicionário extensível e revisado (por exemplo, nome oficial da perícia e formas usuais de escrita).

Não remover palavras importantes como `não`, `exceto`, `apenas`, `uma vez` ou `enquanto`; elas podem inverter o significado de regras.

### 6.3 Índice remissivo

Usar o índice remissivo como uma fonte de descoberta e de localização de conteúdo, não como prova de que um item concede determinado efeito. Um termo pode apontar para várias páginas e entidades.

### 6.4 Ranking

Ordenação inicial recomendada:

1. correspondência exata de ID/nome;
2. correspondência de nome normalizado;
3. correspondência estruturada nos filtros;
4. correspondência de frase/termos na descrição e efeitos;
5. correspondência no índice remissivo.

Deduplicar resultados pela chave estável da entidade. Preservar todas as fontes relevantes encontradas. Não usar vetor/LLM para ordenar consultas simples se uma regra determinística resolve o caso.

### 6.5 Embeddings (fase futura)

Só adicionar depois de montar um conjunto de consultas avaliadas e demonstrar que a busca lexical/estruturada falha em perguntas semânticas. Se adicionados, embeddings devem ser um índice derivado e reconstruível; não são a fonte canônica. O provedor de embeddings deve ser plugável e a ausência de credenciais deve continuar permitindo o uso básico da biblioteca.

## 7. MCP server

Adicionar um servidor MCP no mesmo repositório, usando as funções públicas do Knowledge Engine. Não duplicar lógica SQL nos handlers MCP.

### Ferramentas do MVP

#### `search_knowledge`

Entrada:

```json
{
  "query": "intimidação",
  "types": ["item", "poder", "magia"],
  "limit": 10,
  "includeIndex": true
}
```

Uso: busca geral por nome e texto, com filtros opcionais.

#### `get_entity`

Entrada:

```json
{
  "id": "identificador-estavel",
  "type": "item"
}
```

Uso: obter a entidade, descrição, efeitos disponíveis e fontes.

#### `search_effects`

Entrada:

```json
{
  "target": "Intimidação",
  "operation": "bonus",
  "entityTypes": ["item", "poder", "magia"],
  "limit": 20
}
```

Uso: pesquisar efeitos e modificadores. A resposta deve explicitar se cada correspondência é estruturada ou apenas textual.

#### `search_rules`

Entrada:

```json
{
  "query": "como funciona intimidar",
  "limit": 10
}
```

Uso: busca especializada em regras, descrições, índice remissivo e fontes relacionadas.

### Requisitos do MCP

- Usar transporte `stdio` inicialmente, adequado a clientes locais.
- Escrever logs em `stderr`, nunca em `stdout`, para não corromper o protocolo.
- Respostas estruturadas e concisas, contendo IDs e fontes.
- Não permitir que o cliente forneça SQL, nomes arbitrários de tabela ou caminhos de arquivos.
- Tratar entradas inválidas com erro claro e sem stack trace em conteúdo destinado ao modelo.
- Permitir configuração do caminho do SQLite somente através de opção documentada e validada; por padrão usar o banco distribuído pela biblioteca.
- Encerrar conexões/recursos corretamente.
- Testar inicialização, chamadas de ferramenta, erros de validação e execução por stdin/stdout.

O servidor MCP não deve chamar uma LLM. Ele entrega dados e ferramentas; o cliente/host escolhe o modelo. Isso mantém o servidor agnóstico de IA.

## 8. API HTTP/REST (opcional, após MVP)

Se houver necessidade de consumo remoto, acrescentar um pequeno servidor HTTP, ainda no mesmo repositório, que delega às mesmas funções.

Rotas sugeridas:

```text
GET  /health
GET  /v1/search?q=...&type=item
GET  /v1/entities/:type/:id
POST /v1/effects/search
POST /v1/rules/search
```

Não adicionar REST no primeiro incremento se o objetivo é usar a biblioteca dentro de processos locais e via MCP. Uma API REST pressupõe deployment, política de CORS, limites, autenticação e versionamento; não deve aumentar o escopo sem um consumidor concreto.

## 9. Interpretação de linguagem natural

A busca inicial deve aceitar texto livre, mas não depender de uma LLM. Para consultas conhecidas, implementar parsers pequenos e determinísticos, por exemplo:

- "itens que dão bônus em Intimidação" → `searchEffects({ target: "Intimidação", operation: "bonus", entityTypes: ["item"] })`;
- "magias de 3º círculo" → busca estruturada por tipo e círculo;
- "onde aparece X?" → entidade e índice remissivo/fontes;
- "o que é X?" → entidade por nome e, se necessário, busca textual.

Não tentar criar um parser completo de português no MVP. Quando não for possível mapear a pergunta com segurança, executar busca geral e retornar resultados com evidência; não converter silenciosamente a pergunta numa afirmação factual.

### Integração opcional com LLM

Uma camada `QueryInterpreter` pode ser introduzida futuramente:

```ts
export interface QueryPlan {
  intent: 'search' | 'get_entity' | 'search_effects' | 'search_rules';
  args: Record<string, unknown>;
}

export interface QueryInterpreter {
  interpret(question: string): Promise<QueryPlan>;
}
```

A implementação determinística é o fallback obrigatório. Um adaptador de LLM, caso seja criado, deve devolver um plano sujeito a schema validation; depois disso, somente funções de consulta permitidas podem ser chamadas. A LLM não monta SQL e não altera dados.

A geração de resposta em linguagem natural fica fora do núcleo nesta fase. Um consumidor pode enviar os resultados e as fontes para qualquer LLM que escolher.

## 10. Organização de código sugerida

Ajustar a estrutura à organização existente, evitando mover módulos de domínio já publicados.

```text
src/ts/
  knowledge/
    index.ts
    types.ts
    search.ts
    entity.ts
    effects.ts
    rules.ts
    normalize.ts
    ranking.ts
    sources.ts
    db.ts                 # reutilizar o acesso já existente se possível
  mcp/
    server.ts
    tools/
      search-knowledge.ts
      get-entity.ts
      search-effects.ts
      search-rules.ts
  cli/
    query.ts              # opcional para depuração local

spec/ ou src/ts/**/*.test.ts
  knowledge-search.test.ts
  get-entity.test.ts
  effect-search.test.ts
  source-references.test.ts
  mcp-server.test.ts

docs/
  knowledge-query.md
  mcp.md
  examples/
```

A biblioteca deve exportar funções e tipos públicos de um ponto de entrada estável, por exemplo `Knowledge`, `searchKnowledge`, `getEntity` e `searchEffects`, seguindo as convenções públicas que já existem no pacote.

## 11. Plano de implementação por PRs/etapas

### Etapa 0 — audit e baseline

- Inspecionar os métodos atuais de acesso ao banco e de referências bibliográficas.
- Adicionar fixtures de consultas reais e documentar lacunas.
- Confirmar testes e builds atuais sem modificações.
- **Gap identificado:** o `seeds.rb` não importa registros da tabela `livros`, embora o schema a defina. Corrigir para que o seed popule os livros a partir de `src/json/livros/`.

**Saída:** documento de auditoria e baseline verde.

### Etapa 0.5 — adição do livro Ameaças de Arton

**Objetivo:** expandir a base de dados para além do Livro Básico, incluindo o conteúdo completo do suplemento "Ameaças de Arton" antes de construir as interfaces de consulta. Isso garante que a busca e a validação de qualidade já operem sobre um corpus multi-livro.

#### Pré-requisitos

- Etapa 0 concluída (auditoria e baseline verde).
- Acesso ao conteúdo do livro "Ameaças de Arton" para extração dos dados.

#### Tarefas

- [ ] Registrar o livro na base: criar `src/json/livros/ameacas_de_arton.json` com `id`, `nome`, `nome_curto`.
- [ ] Corrigir o seed para importar todos os livros de `src/json/livros/` na tabela `livros` (gap identificado na Etapa 0).
- [ ] Criar a tabela `criaturas` no schema SQL com os campos necessários:
  - `id`, `name`, `description`, `tipo` (monstro, NPC, animal, constructo, morto-vivo, etc.)
  - `nivel_de_desafio` (ND), `tamanho`, `tipo_criatura`
  - `atributos` (JSON: FOR, DES, CON, INT, SAB, CAR)
  - `defesa`, `pontos_de_vida`, `deslocamento`
  - `ataques` (JSON), `habilidades` (JSON), `tesouros` (JSON)
  - `resistencias` (JSON), `imunidades` (JSON), `vulnerabilidades` (JSON)
  - `descricao_combate`, `descricao_habitat`
  - `livro_id` (FK para `livros`), `pagina` (referência bibliográfica)
- [ ] Extrair **todas** as criaturas, monstros e NPCs do livro "Ameaças de Arton" em arquivos JSON individuais em `src/json/criaturas/`.
- [ ] Para cada criatura, incluir: estatísticas completas, habilidades especiais, descrição de combate, habitat e referência de página.
- [ ] Criar o seed de importação para criaturas (`import_criaturas` no `seeds.rb`).
- [ ] Criar o índice remissivo do livro "Ameaças de Arton" em `src/json/indice_remissivo/ameacas_de_arton.json`, associando termos a páginas, tabelas e registro_ids.
- [ ] Adicionar o modelo Ruby/TypeScript correspondente (`Criatura` / `Creature`).
- [ ] Atualizar os modelos públicos TypeScript para incluir os novos `EntityType`: `'criatura'` e `'npc'`.
- [ ] Validar que o build e os testes existentes continuam passando após a adição.
- [ ] Criar testes para ao menos 5 criaturas representativas (variando ND, tipo e complexidade de habilidades).

#### Decisões de schema

- O campo `tipo` da criatura deve seguir a categorização do livro (ex: constructo, morto-vivo, animal, monstro, humanóide, etc.).
- Criaturas com variantes (ex: diferentes NDs) devem ser registros separados com IDs distintos.
- NPCs notáveis que possuem stat block completo devem ser registrados com `tipo = 'npc'`.
- Habilidades especiais de criaturas que sejam equivalentes a poderes ou magias existentes devem referenciar o `id` correspondente quando possível, sem duplicar a descrição.

#### Regras de extração

- Não inventar dados ausentes no livro. Se uma criatura não lista tesouro ou habitat, o campo deve ser nulo ou vazio.
- Preservar a grafia e nomenclatura original do livro.
- Cada JSON deve incluir `livro_id: "ameacas_de_arton"` e `pagina` com o número correto.
- A extração deve ser verificável: todo dado extraído deve ser rastreável à página de origem.

**Saída:** banco SQLite contendo todas as criaturas e NPCs do livro "Ameaças de Arton", com referências bibliográficas, índice remissivo e testes de integridade passando.

### Etapa 1 — modelo de resultado e resolução de fontes (inclui criaturas)

- Criar tipos `SearchResult` e `SourceReference` compatíveis com o modelo atual.
- Centralizar a resolução de livros/páginas num módulo único.
- Preservar múltiplas referências e ausências de referência.
- Garantir que criaturas do livro "Ameaças de Arton" são corretamente resolvidas com `bookId`, `bookName` e `page`.

**Saída:** uma função de entidade consegue retornar os dados e suas fontes consistentemente, incluindo entidades de múltiplos livros.

### Etapa 2 — API de busca programática

- Implementar normalização de texto em português.
- Implementar `searchKnowledge` com filtros por tipo e limites.
- Implementar `getEntity` por ID/tipo.
- Adicionar testes de SQL injection, entrada inválida, resultados vazios, acentos e duplicatas.

**Saída:** aplicações TypeScript conseguem consultar a biblioteca sem IA.

### Etapa 3 — busca de regras e índice remissivo

- Implementar `searchRules` sobre tabelas textuais e índice remissivo.
- Retornar páginas e termos associados, sem confundir ocorrência com confirmação semântica.
- Testar entidades com mais de uma fonte/página.

**Saída:** busca rastreável de regras e localização bibliográfica.

### Etapa 4 — busca de efeitos

- Inventariar a estrutura atual de `effects`, `benefits`, melhorias, encantamentos e descrições.
- Consultar campos estruturados antes do texto livre.
- Implementar `searchEffects` e classificação de evidência.
- Adicionar testes para bônus, penalidades, condições, requisitos e negações quando presentes nos dados.

**Saída:** o sistema diferencia bônus comprovados de possíveis correspondências.

### Etapa 5 — MCP

- Adicionar SDK MCP e entry point executável/documentado.
- Expor `search_knowledge`, `get_entity`, `search_effects` e `search_rules`.
- Testar input schema, ferramentas, saída JSON, erros e protocolo stdio.
- Documentar exemplos de configuração em um cliente MCP compatível.

**Saída:** um cliente MCP consegue consultar a biblioteca sem uma API key de LLM.

### Etapa 6 — qualidade, avaliação e release

- Criar um conjunto versionado de perguntas e resultados esperados.
- Avaliar precisão e recall qualitativamente nas consultas de referência.
- Revisar documentação, compatibilidade, tamanho da dependência e processo de publicação.
- Atualizar changelog e versão conforme as políticas do projeto.

**Saída:** release documentada e reproduzível.

### Etapa 7 — REST, embeddings e interpretação com LLM (somente mediante necessidade)

Implementar separadamente, com decisão de escopo baseada no uso real. Manter o mesmo contrato de domínio e de resultados.

## 12. Conjunto de avaliação inicial

Criar testes com dados reais do banco e anotar os resultados esperados manualmente. Sugestões:

1. "Quais itens dão bônus em Intimidação?"
2. "Quais poderes melhoram Intimidação?"
3. "Quais magias mencionam a perícia Intimidação?"
4. "Onde a regra de Intimidação é explicada?"
5. "Quais efeitos fornecem bônus de +2 ou mais?"
6. "Encontre a entidade pelo nome exato X."
7. "Onde X aparece nos livros?"
8. "Quais requisitos o poder X possui?"
9. "Quais entidades mencionam um termo sinônimo ou acentuado?"
10. "Busque uma expressão que não exista e retorne lista vazia."
11. "Quais criaturas de ND 5 ou superior existem no livro Ameaças de Arton?"
12. "Quais monstros são mortos-vivos?"
13. "Encontre criaturas que tenham resistência a fogo."
14. "Onde o monstro X aparece no livro Ameaças de Arton?"

Para cada caso, verificar:

- se os resultados corretos aparecem;
- se entidades não relacionadas são excluídas;
- se o texto de evidência sustenta a afirmação;
- se livro/página correspondem aos dados;
- se ausência de resultado não vira resposta inventada.

## 13. Critérios de aceite do MVP

- [ ] A API de busca pode ser usada sem credenciais de IA ou serviços externos.
- [ ] O mesmo núcleo é utilizado pela biblioteca e pelo MCP.
- [ ] IDs de entidade são estáveis e resultados não dependem apenas do nome exibido.
- [ ] As referências disponíveis são retornadas sem serem reconstruídas por suposição.
- [ ] A busca aceita acentos e caixa diferentes.
- [ ] Os filtros por tipo e os limites funcionam e são validados.
- [ ] Resultados de efeitos distinguem dado estruturado de correspondência textual.
- [ ] Consultas são parametrizadas e não aceitam SQL arbitrário.
- [ ] O MCP funciona por stdio e não escreve logs em stdout.
- [ ] Testes existentes continuam passando; novos módulos têm testes automatizados.
- [ ] Documentação inclui setup, configuração de cliente MCP, exemplos e limitações conhecidas.
- [ ] O livro "Ameaças de Arton" está integrado: criaturas consultáveis, fontes rastreáveis, índice remissivo presente.
- [ ] Buscas retornam entidades de múltiplos livros com as fontes corretas.

## 14. Riscos e decisões a evitar

- **Não migrar todo o banco para PostgreSQL no MVP.** SQLite já é parte do pacote e facilita uso local/offline.
- **Não criar embeddings por padrão.** Primeiro medir busca lexical e estruturada.
- **Não declarar bônus com base apenas em similaridade semântica.** Similaridade é descoberta, não prova.
- **Não acoplar o pacote a um LLM.** Nem SDK de provedor nem API key deve ser exigido para a consulta básica.
- **Não duplicar fontes/páginas.** Centralizar resolução e manter o dado original como autoridade.
- **Não assumir que todas as entidades têm páginas.** Fonte ausente deve ser representada como ausente e coberta por teste.
- **Não implementar regras derivadas silenciosamente.** Diferença entre texto original, extração estruturada e inferência deve permanecer explícita.
- **Não inventar stat blocks de criaturas.** Cada campo deve vir diretamente do livro. Campos ausentes devem ser nulos, não preenchidos por suposição.

## 15. Decisões em aberto para ajustar localmente

- O MCP deve ser publicado como comando executável no pacote ou como subpath export separado?
- O REST faz parte do primeiro release ou fica para uma versão posterior?
- A busca deve retornar entidades inteiras ou um resumo seguro por padrão, com opção para detalhes?
- A normalização de sinônimos será um dicionário manual versionado ou terá também aliases vindos dos dados?
- Quais categorias de efeitos serão suportadas de modo estruturado na primeira versão?
- Qual é a política de versão da API pública e como serão sinalizadas alterações incompatíveis?

**Recomendação padrão:** implementar primeiro as Etapas 0–5; manter REST, embeddings e LLM interpretativa para depois. Isso entrega uma base útil e integrável sem transformar o projeto numa aplicação dependente de fornecedor de IA.
