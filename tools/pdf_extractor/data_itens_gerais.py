"""
Definições de Itens Gerais de Ameaças de Arton (Tabela 3-3 e descrições):
- Equipamento de Aventura
- Vestuário
- Esotéricos
- Alimentação
- Alquímicos: Preparados, Catalisadores e Venenos
- Animais (todos linkados a parceiros/montarias da Tabela A-2)
"""

ITENS_GERAIS = [
    # Equipamento de Aventura
    {
        "id": "caixa_de_voz",
        "name": "Caixa de Voz",
        "type": "item",
        "categoria": "equipamento_de_aventura",
        "preco": 50,
        "espacos": 1,
        "description": "Complexo mecanismo da Supremacia com 1d4 cargas. Permite aumentar o alcance de uma habilidade de bardo ou nobre em um passo ao gastar uma carga.",
        "page": 396,
        "subpath": "aventura/caixa_de_voz.json"
    },
    {
        "id": "corda_de_teia",
        "name": "Corda de Teia",
        "type": "item",
        "categoria": "equipamento_de_aventura",
        "preco": 100,
        "espacos": 1,
        "description": "Feita de teia de aranha gigante (10m). Funciona como corda normal, mas arrebentá-la exige 5 pontos de dano de corte ou teste de Força (CD 28).",
        "page": 396,
        "subpath": "aventura/corda_de_teia.json"
    },
    {
        "id": "dente_de_wisphago",
        "name": "Dente de Wisphago",
        "type": "item",
        "categoria": "equipamento_de_aventura",
        "preco": 100,
        "espacos": 1,
        "description": "Vestido como amuleto. Em teste de resistência contra magia arcana, pode ser gasto para rolar novamente com +2 de bônus (se desfaz após o uso).",
        "page": 396,
        "subpath": "aventura/dente_de_wisphago.json"
    },
    {
        "id": "gema_de_forca",
        "name": "Gema de Força",
        "type": "item",
        "categoria": "equipamento_de_aventura",
        "preco": 200,
        "espacos": 1,
        "description": "Engenho da Supremacia com 1d4 cargas. Permite produzir domo como o efeito básico de Campo de Força ou reduzir em -2 PM o custo dessa magia.",
        "page": 396,
        "subpath": "aventura/gema_de_forca.json"
    },

    # Vestuário
    {
        "id": "garra_feroz",
        "name": "Garra Feroz",
        "type": "item",
        "categoria": "vestuario",
        "preco": 60,
        "espacos": 1,
        "description": "Pinças de insetos gigantes presas com tiras de couro. Funciona como manopla e seus benefícios se aplicam a armas naturais ou garras de Forma Selvagem.",
        "page": 396,
        "subpath": "vestuario/garra_feroz.json"
    },
    {
        "id": "manto_do_mantor",
        "name": "Manto do Mantor",
        "type": "item",
        "categoria": "vestuario",
        "preco": 450,
        "espacos": 1,
        "description": "Manto feito com couro de mantor. Na escuridão completa, fornece camuflagem total mesmo contra criaturas que vejam no escuro.",
        "page": 396,
        "subpath": "vestuario/manto_do_mantor.json"
    },
    {
        "id": "manto_pesado",
        "name": "Manto Pesado",
        "type": "item",
        "categoria": "vestuario",
        "preco": 10,
        "espacos": 1,
        "description": "Veste pesada com capuz que protege contra sol e claridade em excesso. Concede imunidade à condição ofuscado e desconsidera luz solar.",
        "page": 396,
        "subpath": "vestuario/manto_pesado.json"
    },
    {
        "id": "sombreiro",
        "name": "Sombreiro",
        "type": "item",
        "categoria": "vestuario",
        "preco": 10,
        "espacos": 1,
        "description": "Chapéu com abas muito largas comum perto de Smokestone. Fornece resistência a efeitos de sentidos +2.",
        "page": 396,
        "subpath": "vestuario/sombreiro.json"
    },
    {
        "id": "traje_selako",
        "name": "Traje Selako",
        "type": "item",
        "categoria": "vestuario",
        "preco": 90,
        "espacos": 1,
        "description": "Feito de couro de selako. Fornece +2 em testes de Atletismo para nadar e +3m no deslocamento de natação.",
        "page": 396,
        "subpath": "vestuario/traje_selako.json"
    },

    # Esotéricos
    {
        "id": "ankh_solar",
        "name": "Ankh Solar",
        "type": "item",
        "categoria": "esoterico",
        "preco": 450,
        "espacos": 1,
        "description": "Pode ser usado como arma leve simples (1d6, 19, corte). Suas magias com teste de resistência ganham o aprimoramento (+2 PM: alvos que falham não podem recuperar PV por 1 rodada).",
        "page": 396,
        "subpath": "esotericos/ankh_solar.json"
    },
    {
        "id": "tomo_de_guerra",
        "name": "Tomo de Guerra",
        "type": "item",
        "categoria": "esoterico",
        "preco": 300,
        "espacos": 1,
        "description": "Quando lança uma magia de evocação, você recebe +1 PM para gastar em aprimoramentos.",
        "page": 396,
        "subpath": "esotericos/tomo_de_guerra.json"
    },
    {
        "id": "tomo_do_rancor",
        "name": "Tomo do Rancor",
        "type": "item",
        "categoria": "esoterico",
        "preco": 750,
        "espacos": 1,
        "description": "Suas magias de dano recebem aprimoramento (+2 PM: causa +2d8+2 pontos de dano de corte, impacto ou perfuração a sua escolha).",
        "page": 396,
        "subpath": "esotericos/tomo_do_rancor.json"
    },

    # Alimentação
    {
        "id": "algravia",
        "name": "Algravia",
        "type": "item",
        "categoria": "alimentacao",
        "preco": 3,
        "espacos": 0,
        "description": "Bebida fermentada típica de povos bárbaros e nômades, restaurando energia rápida.",
        "page": 398,
        "subpath": "alimentacao/algravia.json"
    },
    {
        "id": "banquete_de_canceronte",
        "name": "Banquete de Canceronte",
        "type": "item",
        "categoria": "alimentacao",
        "preco": 36,
        "espacos": 0,
        "description": "Prato feito com carnes exóticas de caranguejos gigantes e carapaças marinhas, fortalecendo a vitalidade do grupo.",
        "page": 398,
        "subpath": "alimentacao/banquete_de_canceronte.json"
    },
    {
        "id": "coc_au_triz",
        "name": "Coc-au-Triz",
        "type": "item",
        "categoria": "alimentacao",
        "preco": 54,
        "espacos": 0,
        "description": "Guisado gourmet feito com aves monstruosas e temperos raros de Ahlen.",
        "page": 398,
        "subpath": "alimentacao/coc_au_triz.json"
    },
    {
        "id": "cozido_de_serpe",
        "name": "Cozido de Serpe",
        "type": "item",
        "categoria": "alimentacao",
        "preco": 12,
        "espacos": 0,
        "description": "Cozido encorpado preparado a partir de carne de serpe das montanhas.",
        "page": 398,
        "subpath": "alimentacao/cozido_de_serpe.json"
    },
    {
        "id": "gorlogg_ensopado",
        "name": "Gorlogg Ensopado",
        "type": "item",
        "categoria": "alimentacao",
        "preco": 6,
        "espacos": 0,
        "description": "Ensopado altamente nutritivo criado em Yuvalin. Em sua próxima noite de sono, aumenta a recuperação de PV e PM em +1 por nível.",
        "page": 398,
        "subpath": "alimentacao/gorlogg_ensopado.json"
    },
    {
        "id": "omelete_monstruosa",
        "name": "Omelete Monstruosa",
        "type": "item",
        "categoria": "alimentacao",
        "preco": 3,
        "espacos": 0,
        "description": "Feita com ovos de pragas monstruosas ou feras dracônicas. Fornece +2 em dano e -2 em perícias baseadas em Sabedoria até o fim do dia.",
        "page": 398,
        "subpath": "alimentacao/omelete_monstruosa.json"
    },
    {
        "id": "sashimi_de_kraken",
        "name": "Sashimi de Kraken",
        "type": "item",
        "categoria": "alimentacao",
        "preco": 60,
        "espacos": 0,
        "description": "Iguaria de Tamu-ra servida crua. Concede +2 em Diplomacia (cumulativo) e 5 PM temporários.",
        "page": 398,
        "subpath": "alimentacao/sashimi_de_kraken.json"
    },

    # Alquímicos - Preparados
    {
        "id": "balsamo_de_drogadora",
        "name": "Bálsamo de Drogadora",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "preparado",
        "preco": 60,
        "espacos": 0.5,
        "description": "Pasta gosmenta dos povos-trovão. Aplicá-la é uma ação completa e cura 4d6+4 PV.",
        "page": 396,
        "subpath": "alquimicos/preparados/balsamo_de_drogadora.json"
    },
    {
        "id": "bomba_de_fumaca",
        "name": "Bomba de Fumaça",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "preparado",
        "preco": 15,
        "espacos": 0.5,
        "description": "Emite nuvem de fumaça espessa de 6m de raio que obscurece a visão até o fim da cena (camuflagem leve até 1,5m e total a partir de 3m).",
        "page": 396,
        "subpath": "alquimicos/preparados/bomba_de_fumaca.json"
    },
    {
        "id": "elixir_quimerico",
        "name": "Elixir Quimérico",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "preparado",
        "preco": 120,
        "espacos": 0.5,
        "description": "Beber concede arma natural de mordida (1d6, x2, perfuração) até o fim da cena e permite ataque extra de mordida por 1 PM na ação agredir.",
        "page": 396,
        "subpath": "alquimicos/preparados/elixir_quimerico.json"
    },
    {
        "id": "eter_elemental",
        "name": "Éter Elemental",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "preparado",
        "preco": 60,
        "espacos": 0.5,
        "description": "Extraído de elementais. Beber concede resistência 10 contra o elemento do preparado até o fim da cena.",
        "page": 396,
        "subpath": "alquimicos/preparados/eter_elemental.json"
    },
    {
        "id": "isca_putrefata",
        "name": "Isca Putrefata",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "preparado",
        "preco": 60,
        "espacos": 0.5,
        "description": "Frasco de restos mortais diluídos arremessável em alcance médio. Atrai mortos-vivos e predadores que priorizam o alvo atingido.",
        "page": 397,
        "subpath": "alquimicos/preparados/isca_putrefata.json"
    },
    {
        "id": "lagrima_petrea",
        "name": "Lágrima Pétrea",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "preparado",
        "preco": 30,
        "espacos": 0.5,
        "description": "Substância mineral que ao ser ingerida endurece a pele, fornecendo +2 na Defesa por 1 hora.",
        "page": 398,
        "subpath": "alquimicos/preparados/lagrima_petrea.json"
    },
    {
        "id": "oleo_de_baleia",
        "name": "Óleo de Baleia",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "preparado",
        "preco": 30,
        "espacos": 0.5,
        "description": "Óleo isolante térmico que protege contra frio intenso e concede resistência a frio 5 por 1 hora.",
        "page": 398,
        "subpath": "alquimicos/preparados/oleo_de_baleia.json"
    },
    {
        "id": "oleo_de_besouro",
        "name": "Óleo de Besouro",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "preparado",
        "preco": 50,
        "espacos": 0.5,
        "description": "Substância luminescente que reage ao calor, iluminando áreas escuras sem gerar fumaça por 4 horas.",
        "page": 398,
        "subpath": "alquimicos/preparados/oleo_de_besouro.json"
    },
    {
        "id": "po_azul",
        "name": "Pó Azul",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "preparado",
        "preco": 150,
        "espacos": 0.5,
        "description": "Composto estimulante de mana que permite recuperar 1d4 PM quando consumido.",
        "page": 398,
        "subpath": "alquimicos/preparados/po_azul.json"
    },

    # Alquímicos - Catalisadores
    {
        "id": "corrosivo_mineral",
        "name": "Corrosivo Mineral",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "catalisador",
        "preco": 150,
        "espacos": 0.5,
        "description": "Catalisador para magias ácidas. Adiciona +2d6 pontos de dano de ácido à magia lançada.",
        "page": 398,
        "subpath": "alquimicos/catalisadores/corrosivo_mineral.json"
    },
    {
        "id": "gelo_extremo",
        "name": "Gelo Extremo",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "catalisador",
        "preco": 150,
        "espacos": 0.5,
        "description": "Fragmento de gelo eterno das Uivantes. Adiciona +2d6 pontos de dano de frio a magias.",
        "page": 398,
        "subpath": "alquimicos/catalisadores/gelo_extremo.json"
    },
    {
        "id": "pedaco_de_lingua",
        "name": "Pedaço de Língua",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "catalisador",
        "preco": 30,
        "espacos": 0.5,
        "description": "Língua de criatura falante usada como catalisador de magias de ilusão e encantamento, aumentando sua CD em +1.",
        "page": 398,
        "subpath": "alquimicos/catalisadores/pedaco_de_lingua.json"
    },
    {
        "id": "raio_cristalizado",
        "name": "Raio Cristalizado",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "catalisador",
        "preco": 150,
        "espacos": 0.5,
        "description": "Fulgurita criada por raio elemental. Adiciona +2d6 pontos de dano de eletricidade a magias.",
        "page": 398,
        "subpath": "alquimicos/catalisadores/raio_cristalizado.json"
    },

    # Alquímicos - Venenos
    {
        "id": "esporos_de_cogumelo",
        "name": "Esporos de Cogumelo",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "veneno",
        "preco": 75,
        "espacos": 0.5,
        "description": "Veneno inalável (Fortitude CD 18). Causa alucinações e a condição confuso por 1d4 rodadas.",
        "page": 398,
        "subpath": "alquimicos/venenos/esporos_de_cogumelo.json"
    },
    {
        "id": "peconha_ancia",
        "name": "Peçonha Anciã",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "veneno",
        "preco": 1800,
        "espacos": 0.5,
        "description": "Extraída de vermes e monstros milenares (Fortitude CD 25). Causa 4d12 pontos de dano de veneno e a condição paralisado por 1 rodada.",
        "page": 398,
        "subpath": "alquimicos/venenos/peconha_ancia.json"
    },
    {
        "id": "peconha_irritante",
        "name": "Peçonha Irritante",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "veneno",
        "preco": 10,
        "espacos": 0.5,
        "description": "Veneno de contato leve (Fortitude CD 12). Causa coceira e distração severa, impondo a condição vulnerável por 1 rodada.",
        "page": 398,
        "subpath": "alquimicos/venenos/peconha_irritante.json"
    },
    {
        "id": "veneno_batraquio",
        "name": "Veneno Batráquio",
        "type": "item",
        "categoria": "alquimico",
        "subcategoria": "veneno",
        "preco": 30,
        "espacos": 0.5,
        "description": "Secretado por sapos atrozes (Fortitude CD 16). Causa 2d6 pontos de dano de veneno e a condição lento por 1 rodada.",
        "page": 398,
        "subpath": "alquimicos/venenos/veneno_batraquio.json"
    },

    # Animais (linkados à Tabela A-2 de Parceiros)
    {
        "id": "bulette",
        "name": "Bulette",
        "type": "item",
        "categoria": "animal",
        "preco": 500,
        "espacos": 0,
        "parceiro": {
            "tipo": "montaria",
            "porte": "grande",
            "nivel": "iniciante",
            "beneficio": "Concede bônus de Defesa +2 e deslocamento de escavação enquanto montado.",
            "pagina_criatura": 102
        },
        "description": "O tubarão-da-terra domesticado como montaria Grande pesada capaz de escavar o solo.",
        "page": 398,
        "subpath": "animais/bulette.json"
    },
    {
        "id": "capivara",
        "name": "Capivara",
        "type": "item",
        "categoria": "animal",
        "preco": 60,
        "espacos": 0,
        "parceiro": {
            "tipo": "montaria",
            "porte": "medio",
            "nivel": "iniciante",
            "beneficio": "Montaria Média dócil que fornece deslocamento de natação e serenidade contra efeitos de medo (+2 em testes de Vontade contra medo).",
            "pagina_criatura": 211
        },
        "description": "Grande roedor semiaquático pacífico e resistente. Pode ser usado como parceiro montaria Médio com excelente capacidade de natação.",
        "page": 398,
        "subpath": "animais/capivara.json"
    },
    {
        "id": "corcel_do_deserto",
        "name": "Corcel do Deserto",
        "type": "item",
        "categoria": "animal",
        "preco": 150,
        "espacos": 0,
        "parceiro": {
            "tipo": "montaria",
            "porte": "grande",
            "nivel": "iniciante",
            "beneficio": "Ignora terreno difícil de areia e fornece resistência a calor extremo.",
            "pagina_criatura": 214
        },
        "description": "Cavalo adaptado ao calor causticante do Deserto da Perdição. Parceiro montaria Grande veloz em climas áridos.",
        "page": 398,
        "subpath": "animais/corcel_do_deserto.json"
    },
    {
        "id": "dromedario",
        "name": "Dromedário",
        "type": "item",
        "categoria": "animal",
        "preco": 75,
        "espacos": 0,
        "parceiro": {
            "tipo": "montaria",
            "porte": "grande",
            "nivel": "iniciante",
            "beneficio": "Conta como montaria e besta de carga (carrega 10 espaços adicionais sem penalidade).",
            "pagina_criatura": 215
        },
        "description": "Animal de tração e montaria resistente que aguenta dias sem água no deserto.",
        "page": 398,
        "subpath": "animais/dromedario.json"
    },
    {
        "id": "elefante",
        "name": "Elefante",
        "type": "item",
        "categoria": "animal",
        "preco": 1500,
        "espacos": 0,
        "parceiro": {
            "tipo": "montaria",
            "porte": "enorme",
            "nivel": "iniciante",
            "beneficio": "Montaria Enorme com atropelamento devastador e capacidade massiva de carga.",
            "pagina_criatura": 216
        },
        "description": "Paquiderme gigantesco treinado para guerra e transporte pesado.",
        "page": 398,
        "subpath": "animais/elefante.json"
    },
    {
        "id": "hiena",
        "name": "Hiena",
        "type": "item",
        "categoria": "animal",
        "preco": 220,
        "espacos": 0,
        "parceiro": {
            "tipo": "especial_perseguidor_ou_montaria",
            "porte": "medio",
            "nivel": "iniciante",
            "beneficio": "Pode atuar como parceiro perseguidor ou montaria Média para personagens Pequenos.",
            "pagina_criatura": 119
        },
        "description": "Predador das savanas com mordida trituradora e risada inquietante.",
        "page": 398,
        "subpath": "animais/hiena.json"
    },
    {
        "id": "leao",
        "name": "Leão",
        "type": "item",
        "categoria": "animal",
        "preco": 800,
        "espacos": 0,
        "parceiro": {
            "tipo": "montaria",
            "porte": "grande",
            "nivel": "iniciante",
            "beneficio": "Montaria Grande feroz com bônus em testes de ataque em investida (+2).",
            "pagina_criatura": 217
        },
        "description": "Grande felino de juba majestosa treinado como montaria de combate.",
        "page": 398,
        "subpath": "animais/leao.json"
    },
    {
        "id": "rinoceronte",
        "name": "Rinoceronte",
        "type": "item",
        "categoria": "animal",
        "preco": 600,
        "espacos": 0,
        "parceiro": {
            "tipo": "montaria",
            "porte": "grande",
            "nivel": "iniciante",
            "beneficio": "Montaria Grande com armadura natural pesada (+3 Defesa do cavaleiro) e marrada poderosa.",
            "pagina_criatura": 219
        },
        "description": "Besta encouraçada das savanas com chifre frontal intimidador.",
        "page": 398,
        "subpath": "animais/rinoceronte.json"
    },
    {
        "id": "urso_pardo",
        "name": "Urso Pardo",
        "type": "item",
        "categoria": "animal",
        "preco": 300,
        "espacos": 0,
        "parceiro": {
            "tipo": "montaria",
            "porte": "grande",
            "nivel": "iniciante",
            "beneficio": "Montaria Grande resistente que concede bônus de manobra de agarrar e defesa natural.",
            "pagina_criatura": 223
        },
        "description": "Predador corpulento das florestas e colinas do norte, treinado para montaria pesada.",
        "page": 398,
        "subpath": "animais/urso_pardo.json"
    }
]
