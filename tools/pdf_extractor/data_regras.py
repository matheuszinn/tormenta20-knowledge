# frozen_string_literal: false
"""
Definições de regras e habilidades gerais de ameaças para Ameaças de Arton.
"""

REGRAS = [
    {
        "id": "habilidades_gerais_de_ameacas",
        "name": "Habilidades Gerais de Ameaças",
        "description": "Habilidades comuns a várias ameaças e monstros de Tormenta 20, descritas no Capítulo 1 de Ameaças de Arton.",
        "page": 16,
        "livro_id": "ameacas_de_arton",
        "habilidades": [
            {
                "id": "agarrar_aprimorado",
                "nome": "Agarrar Aprimorado",
                "descricao": "Se a criatura acertar um ataque com uma arma natural (especificada na habilidade), poderá fazer a manobra agarrar com esta arma como uma ação livre. Enquanto está usando a arma natural para agarrar, a criatura não pode usá-la para desferir outros ataques. A descrição da habilidade pode limitar o tipo ou tamanho de criatura que pode ser agarrada desta forma e também descrever efeitos adicionais."
            },
            {
                "id": "ataque_furtivo",
                "nome": "Ataque Furtivo",
                "descricao": "A criatura é capaz de desferir ataques furtivos, como um ladino. Uma vez por rodada, ela causa a quantidade de dano adicional indicada com ataques corpo a corpo, ou à distância em alcance curto, contra alvos desprevenidos ou que ela esteja flanqueando."
            },
            {
                "id": "bando",
                "nome": "Bando",
                "descricao": "A criatura é formada por um grupo de indivíduos, geralmente seres do mesmo tipo. Se um ataque do bando exceder a Defesa do inimigo por 10 ou mais, causa o dobro do dano. Se um ataque do bando errar, ainda causa metade do dano. Um bando é imune a manobras de combate e efeitos que afetam apenas uma criatura e não causam dano, mas tem vulnerabilidade a dano de área. Um personagem com Trespassar que acerte a criatura pode usá-lo para fazer um ataque adicional contra ela (apenas uma vez por turno)."
            },
            {
                "id": "cura_acelerada",
                "nome": "Cura Acelerada",
                "descricao": "No início de seu turno, a criatura recupera pontos de vida iguais ao seu valor de cura acelerada. Se houver algum tipo de dano listado após uma barra (ex: cura acelerada 10/ácido), não recupera dano desse tipo. Não cura perda de PV, apenas dano."
            },
            {
                "id": "derrubar",
                "nome": "Derrubar",
                "descricao": "Se a criatura acertar um ataque com uma arma (especificada na habilidade), poderá fazer a manobra derrubar com esta arma como uma ação livre."
            },
            {
                "id": "deslocamento_especial",
                "nome": "Deslocamento Especial",
                "descricao": "Modos especiais de movimentação listados após o deslocamento básico: Escalada (pode caminhar por superfícies verticais ou teto), Escavação (move-se sob terreno granular; o terreno se fecha atrás da criatura), Natação (desloca-se na água sem testes de Atletismo, respira debaixo d'água e não sofre penalidades submersas) e Voo (pode voar e encerrar deslocamento no ar; ao perder deslocamento cai 150m por rodada; derrubada cai 1d6x1,5m)."
            },
            {
                "id": "doenca",
                "nome": "Doença",
                "descricao": "Um dos ataques da criatura transmite uma doença. Um personagem que sofra dano desse ataque deve passar num teste de Fortitude ou é contaminado."
            },
            {
                "id": "engolir",
                "nome": "Engolir",
                "descricao": "Se a ameaça começar seu turno agarrando uma criatura uma ou mais categorias de tamanho menor, poderá fazer um teste de agarrar contra ela. Se vencer, engole a criatura. Uma criatura engolida continua agarrada, fica cega, tem cobertura total contra efeitos externos (e vice-versa) e sofre o dano indicado no início de cada turno da ameaça. Pode escapar vencendo teste de agarrar/Acrobacia ou causando dano interno suficiente até o valor indicado."
            },
            {
                "id": "enxame",
                "nome": "Enxame",
                "descricao": "A criatura é um aglomerado de seres menores que agem em conjunto. Pode entrar no espaço ocupado por um personagem e, no fim de seu turno, causa o efeito indicado a qualquer personagem em seu espaço automaticamente. É imune a manobras e efeitos de alvo único que não causam dano, tem vulnerabilidade a dano de área e sofre metade do dano de ataques com armas. Estar dentro do enxame é condição ruim para lançar magias."
            },
            {
                "id": "evasao",
                "nome": "Evasão",
                "descricao": "Quando sofre um efeito que permite um teste de Reflexos para reduzir o dano à metade, a criatura não sofre dano algum se passar."
            },
            {
                "id": "evasao_aprimorada",
                "nome": "Evasão Aprimorada",
                "descricao": "Como Evasão, mas, se falhar no teste de Reflexos, sofre apenas metade do dano."
            },
            {
                "id": "familiar",
                "nome": "Familiar",
                "descricao": "A criatura pode ser invocada como um familiar conforme o poder Familiar (Tormenta20, p. 38) e Apêndice A."
            },
            {
                "id": "faro",
                "nome": "Faro",
                "descricao": "A criatura tem olfato apurado. Contra inimigos que não possa ver, não fica desprevenida e camuflagem total lhe causa apenas 20% de chance de falha em alcance curto."
            },
            {
                "id": "fortificacao",
                "nome": "Fortificação",
                "descricao": "A criatura tem chance percentual indicada de ignorar o dano adicional de acertos críticos e ataques furtivos (1d100)."
            },
            {
                "id": "imunidade",
                "nome": "Imunidade",
                "descricao": "A criatura é imune a um tipo de efeito, dano ou condição. Não sofre nenhuma consequência direta daquilo contra a qual é imune. Imunidade a críticos/ataques furtivos os transforma em acertos normais."
            },
            {
                "id": "incorporeo",
                "nome": "Incorpóreo",
                "descricao": "A criatura não tem corpo físico. Só pode ser afetada por armas e efeitos mágicos ou outras criaturas incorpóreas. Pode atravessar objetos sólidos, tem Força nula e não manipula objetos físicos."
            },
            {
                "id": "magias",
                "nome": "Magias",
                "descricao": "A criatura lança magias com nível de conjurador, CD e limite de PM especificados. Apresenta lista de magias conhecidas preparadas."
            },
            {
                "id": "maior_que_a_morte",
                "nome": "Maior que a Morte",
                "descricao": "Enquanto tiver pelo menos metade de seus PV, a criatura é imune a habilidades de 'morte instantânea' (como Assassino Fantasmagórico, Roubar a Alma, etc.)."
            },
            {
                "id": "natureza_vegetal",
                "nome": "Natureza Vegetal",
                "descricao": "A criatura é vegetal senciente. É imune a atordoamento e metamorfose. Contra magias sem teste de resistência, tem direito a teste de Fortitude (CD da magia) para evitar o efeito."
            },
            {
                "id": "parceiro",
                "nome": "Parceiro",
                "descricao": "A criatura pode ser empregada como um parceiro pelos personagens conforme regras do Apêndice A."
            },
            {
                "id": "percepcao_as_cegas",
                "nome": "Percepção às Cegas",
                "descricao": "Usa sentidos diferentes da visão (radar, sonar, etc.). Escuridão e invisibilidade não a afetam. Faz testes de Percepção usando esses sentidos em alcance curto."
            },
            {
                "id": "reducao_de_dano",
                "nome": "Redução de Dano (RD)",
                "descricao": "A criatura ignora parte do dano que sofre conforme valor numérico indicado. Pode ter exceções específicas indicadas após a barra (ex: RD 10/mágico)."
            },
            {
                "id": "resistencia_a_efeito",
                "nome": "Resistência a Efeito",
                "descricao": "A criatura recebe um bônus em testes de resistência contra efeitos do tipo especificado (ex: resistência a magia +2)."
            },
            {
                "id": "sensibilidade_a_luz",
                "nome": "Sensibilidade a Luz",
                "descricao": "A criatura é suscetível a luz. Quando exposta à luz do sol ou similar, fica ofuscada."
            },
            {
                "id": "visao_na_penumbra",
                "nome": "Visão na Penumbra",
                "descricao": "Enxerga em escuridão leve em alcance curto (exceto mágica), ignorando camuflagem leve por essa escuridão."
            },
            {
                "id": "visao_no_escuro",
                "nome": "Visão no Escuro",
                "descricao": "Enxerga em escuridão total em alcance curto (exceto mágica), ignorando camuflagem total por essa escuridão."
            },
            {
                "id": "vulnerabilidade_a_efeito",
                "nome": "Vulnerabilidade a Efeito",
                "descricao": "A criatura sofre +50% de dano ou de perda de vida de um tipo ou característica específicos."
            }
        ]
    },
    {
        "id": "regras_adicionais_de_ameacas",
        "name": "Regras Adicionais de Ameaças",
        "description": "Regras sobre combate, CDs, morte, ND S/S+ e magias em criaturas no papel de ameaças (Capítulo 2).",
        "page": 376,
        "livro_id": "ameacas_de_arton",
        "topicos": [
            {
                "titulo": "Criaturas e Ataques",
                "descricao": "Luta e Pontaria são consideradas iguais aos ataques listados. Ataque desarmado rápido causa 1d3 + bônus de dano principal (com passos ajustados pelo tamanho). Armas empunhadas perdem modificações especiais se empunhadas por personagens."
            },
            {
                "titulo": "CD de Habilidades",
                "descricao": "Diretrizes para determinar o atributo-chave da CD: Habilidades Atléticas usam Força ou Destreza; Habilidades Fisiológicas (venenos, sopros, doenças) usam Constituição; Habilidades de Controle/Mentais usam Carisma; Magias usam o atributo de conjuração (Int/Car para arcanos)."
            },
            {
                "titulo": "Ameaças e Morte",
                "descricao": "Por padrão morrem com 0 PV. Ameaças importantes, chefes e NPCs notáveis podem seguir a regra de sangramento de personagens jogadores."
            },
            {
                "titulo": "Condições de Itens",
                "descricao": "Equipamentos de ameaças muitas vezes estão danificados ou improvisados. Podem ter a melhoria Traque ou estar sob desgaste."
            },
            {
                "titulo": "Parceiros de Ameaças",
                "descricao": "Ameaças podem possuir parceiros integrados à ficha ou tratados como criaturas separadas pelo mestre com ND próprio."
            },
            {
                "titulo": "Recompensas por Vários Inimigos",
                "descricao": "Em combates com múltiplos inimigos, a XP e tesouro podem ser unificados calculando com base no ND total do encontro."
            },
            {
                "titulo": "Criaturas S e S+",
                "descricao": "Status especial de ameaças épicas acima de ND 20 que não podem ser derrotadas apenas com força bruta. Estatísticas não listadas contam como ND 20, mas seu ND efetivo para poderes de outras criaturas é superior a 20."
            },
            {
                "titulo": "Magias sem Custo e Simuladas",
                "descricao": "Algumas ameaças possuem habilidades mágicas naturais sem gasto de PM ou que simulam efeitos de magias específicas com parâmetros fixos."
            }
        ]
    },
    {
        "id": "tipos_de_criaturas",
        "name": "Tipos de Criaturas",
        "description": "Definição e traços dos 6 grandes tipos de criaturas do sistema Tormenta 20.",
        "page": 14,
        "livro_id": "ameacas_de_arton",
        "tipos": [
            {
                "tipo": "Construtos",
                "descricao": "Objetos inanimados que ganharam vida por magia ou tecnologia. Imunes a cansaço, efeitos de metabolismo, trevas e veneno; não recuperam PV por descanso nem por cura mágica convencional (exigem testes de Ofício ou magias de conserto)."
            },
            {
                "tipo": "Espíritos",
                "descricao": "Seres nativos de outros Planos conectados às forças primordiais ou aspectos dos deuses. Geralmente possuem visão no escuro."
            },
            {
                "tipo": "Humanoides",
                "descricao": "Seres com anatomia semelhante a humanos, inteligentes e membros de culturas/sociedades com raça ou subtipo definido."
            },
            {
                "tipo": "Monstros",
                "descricao": "Criaturas de anatomia aberrante, criaturas da Tormenta, quimeras ou criações selvagens dos deuses, frequentemente com habilidades mágicas ou sobrenaturais."
            },
            {
                "tipo": "Mortos-Vivos",
                "descricao": "Cadáveres animados por energia negativa. Possuem visão no escuro; imunidade a cansaço, metabolismo, trevas e veneno; sofrem dano por cura de luz e recuperam PV com energia negativa."
            },
            {
                "tipo": "Animais",
                "descricao": "Feras e criaturas naturais sem inteligência civilizada (Int nula ou -4/-5). Podem ser domesticados ou treinados como parceiros."
            }
        ]
    },
    {
        "id": "regras_de_parceiros",
        "name": "Regras de Parceiros e Besta de Carga",
        "description": "Regras para emprego de ameaças como parceiros de personagens jogadores e montarias (Apêndice A).",
        "page": 418,
        "livro_id": "ameacas_de_arton",
        "regras": {
            "parceiros_especiais": "Um parceiro especial fornece benefícios listados em sua descrição e conta como o tipo indicado para poderes que exigem aquele tipo (ex: hiena conta como perseguidor para Companheiro Animal). Se tiver mais de um tipo, é escolhido no momento da criação.",
            "natacao_e_parceiros": "Exceto quando indicado, parceiros com deslocamento de natação não permitem ao cavaleiro respirar ou falar debaixo d'água nem anulam penalidades padrão de submersão.",
            "novo_tipo_besta_de_carga": {
                "nome": "Besta de Carga",
                "descricao": "Criatura capaz de carregar peso, como um boi, burro ou mula.",
                "niveis": {
                    "iniciante": "Pode carregar 10 espaços de itens.",
                    "veterano": "Pode carregar 15 espaços de itens.",
                    "mestre": "Pode carregar 20 espaços de itens."
                }
            }
        }
    }
]
