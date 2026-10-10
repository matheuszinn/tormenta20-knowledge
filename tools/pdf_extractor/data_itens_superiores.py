"""
Definições de Melhorias e Materiais Especiais de Ameaças de Arton (Capítulo 3, p. 401-403).
"""

MELHORIAS = [
    {
        "id": "anatomia_monstruosa",
        "name": "Anatomia Monstruosa",
        "type": "melhoria",
        "categoria": "armaduras_escudos",
        "efeito": {
            "adaptada_a_monstros": "Adaptada à fisiologia de criaturas com anatomia não humana (centauros, nagahs, trogs, etc.), sem penalidade de uso."
        },
        "prerequisitos": None,
        "description": "A armadura ou escudo é forjada sob medida para criaturas com caudas, asas, múltiplos membros ou formatos corporais atípicos.",
        "page": 401,
        "subpath": "armaduras_escudos/anatomia_monstruosa.json"
    },
    {
        "id": "camuflada",
        "name": "Camuflada",
        "type": "melhoria",
        "categoria": "armaduras_escudos",
        "efeito": {
            "furtividade_em_terreno": 2
        },
        "prerequisitos": None,
        "description": "Tratada com padrões de camuflagem ou tinturas naturais. Fornece +2 em Furtividade no terreno escolhido durante a fabricação.",
        "page": 401,
        "subpath": "armaduras_escudos/camuflada.json"
    },
    {
        "id": "envenenada",
        "name": "Envenenada",
        "type": "melhoria",
        "categoria": "armas",
        "efeito": {
            "doses_veneno_armazenadas": 1,
            "acao_aplicacao": "livre"
        },
        "prerequisitos": None,
        "description": "Possui canaletas e reservatório interno capaz de armazenar uma dose de veneno que pode ser liberada na lâmina como ação livre.",
        "page": 401,
        "subpath": "armas/envenenada.json"
    },
    {
        "id": "espinhosa",
        "name": "Espinhosa",
        "type": "melhoria",
        "categoria": "armaduras_escudos",
        "efeito": {
            "dano_agarrar": "1d6 perfuração"
        },
        "prerequisitos": None,
        "description": "Cravejada com espinhos de metal ou ossos afiados. Causa 1d6 pontos de dano de perfuração ao usar a manobra agarrar ou a quem agarrar você.",
        "page": 401,
        "subpath": "armaduras_escudos/espinhosa.json"
    },
    {
        "id": "improvavel",
        "name": "Improvável",
        "type": "melhoria",
        "categoria": "armas",
        "efeito": {
            "disfarce_de_outro_objeto": True
        },
        "prerequisitos": None,
        "description": "Construída para aparentar ser um objeto inofensivo cotidiano (bengala, livro, ferramenta). Testes para identificá-la como arma sofrem -5.",
        "page": 401,
        "subpath": "armas/improvavel.json"
    },
    {
        "id": "macabra",
        "name": "Macabra",
        "type": "melhoria",
        "categoria": "armaduras_escudos",
        "efeito": {
            "intimidacao_bonus": 2
        },
        "prerequisitos": None,
        "description": "Decorada com crânios, garras e símbolos aterradores. Concede +2 em testes de Intimidação.",
        "page": 401,
        "subpath": "armaduras_escudos/macabra.json"
    },
    {
        "id": "sedenta",
        "name": "Sedenta",
        "type": "melhoria",
        "categoria": "armas",
        "efeito": {
            "dano_sangramento": "1d4 por rodada em crítico"
        },
        "prerequisitos": None,
        "description": "Possui serrilhas cruéis que rasgam a carne. Em caso de acerto crítico, causa 1d4 de dano de sangramento por rodada.",
        "page": 401,
        "subpath": "armas/sedenta.json"
    }
]

MATERIAIS_ESPECIAIS = [
    {
        "id": "casca_de_carapaca",
        "name": "Casca de Carapaça",
        "type": "material_especial",
        "description": "Placas rígidas extraídas de carapaças de insetos colossais e crustáceos das profundezas.",
        "precos_adicionais": {
            "arma": 1000,
            "armadura_leve": 500,
            "armadura_pesada": 1500,
            "escudo": 500
        },
        "efeitos": {
            "arma": {"dano_contra_construcoes": "+1d8"},
            "armadura": {"resistencia_impacto": 2},
            "escudo": {"resistencia_impacto": 2}
        },
        "page": 401
    },
    {
        "id": "concha_do_dragao_marinho",
        "name": "Concha do Dragão-Marinho",
        "type": "material_especial",
        "description": "Concha iridescente lendária encontrada apenas em fossas abissais oceânicas.",
        "precos_adicionais": {
            "armadura": 3000,
            "escudo": 2000,
            "esoterico": 3000
        },
        "efeitos": {
            "armadura": {"resistencia_frio": 5, "resistencia_eletricidade": 5},
            "esoterico": {"magias_agua_frio_cd": 1}
        },
        "page": 401
    },
    {
        "id": "coral_de_namalkah",
        "name": "Coral de Namalkah",
        "type": "material_especial",
        "description": "Coral sagrado petrificado das bacias marinhas abençoadas pelo Oceano.",
        "precos_adicionais": {
            "arma": 1500,
            "esoterico": 2000
        },
        "efeitos": {
            "arma": {"dano_perfuracao_adicional": 2},
            "esoterico": {"recuperacao_pm_curas": 1}
        },
        "page": 401
    },
    {
        "id": "couro_de_lendas",
        "name": "Couro de Lendas",
        "type": "material_especial",
        "description": "Couro espesso de bestas míticas como hidras, tarrasques e dragões.",
        "precos_adicionais": {
            "armadura_leve": 2000,
            "escudo": 1000
        },
        "efeitos": {
            "armadura_leve": {"reducao_dano": 2},
            "escudo": {"reducao_dano": 1}
        },
        "page": 402
    },
    {
        "id": "escamas_de_wyrm",
        "name": "Escamas de Wyrm",
        "type": "material_especial",
        "description": "Escamas sobrepostas impenetráveis de dragões anciões.",
        "precos_adicionais": {
            "armadura_pesada": 5000,
            "escudo": 2500
        },
        "efeitos": {
            "armadura_pesada": {"reducao_dano_elemental": 10},
            "escudo": {"reducao_dano_elemental": 5}
        },
        "page": 402
    },
    {
        "id": "fio_de_seda_monstro",
        "name": "Fio de Seda-Monstro",
        "type": "material_especial",
        "description": "Fio fiado por aranhas gigantes e lagartas abissais, mais resistente que aço temperado.",
        "precos_adicionais": {
            "armadura_leve": 1500,
            "vestuario": 1000
        },
        "efeitos": {
            "armadura_leve": {"penalidade_armadura": 0, "defesa": 1}
        },
        "page": 402
    },
    {
        "id": "madeira_de_tronco_de_ferro",
        "name": "Madeira de Tronco-de-Ferro",
        "type": "material_especial",
        "description": "Madeira milenar de árvores fossilizadas das florestas de Galrasia tão densa quanto ferro fundido.",
        "precos_adicionais": {
            "arma": 800,
            "escudo": 500
        },
        "efeitos": {
            "arma": {"dano_impacto": 1},
            "escudo": {"rd_fogo": 5}
        },
        "page": 402
    },
    {
        "id": "marfim_de_mamute",
        "name": "Marfim de Mamute",
        "type": "material_especial",
        "description": "Presas maciças de mamutes e bestas das Uivantes, fáceis de esculpir e incrivelmente duras.",
        "precos_adicionais": {
            "arma": 1200,
            "esoterico": 1500
        },
        "efeitos": {
            "arma": {"critico_multiplicador": "+1 em investida"},
            "esoterico": {"magias_frio_dano": 2}
        },
        "page": 402
    },
    {
        "id": "metal_meteorico",
        "name": "Metal Meteórico",
        "type": "material_especial",
        "description": "Fragmentos estelares colhidos de bólidos caídos dos céus artonianos.",
        "precos_adicionais": {
            "arma": 4000,
            "armadura_pesada": 4000
        },
        "efeitos": {
            "arma": {"dano_espiritos_monstros": "1d8 essência"},
            "armadura_pesada": {"rd_magica": 5}
        },
        "page": 402
    },
    {
        "id": "obsidiana_de_doherimm",
        "name": "Obsidiana de Doherimm",
        "type": "material_especial",
        "description": "Vidro vulcânico das profundezas subterrâneas dos anões com lâminas de fio molecular.",
        "precos_adicionais": {
            "arma": 2500
        },
        "efeitos": {
            "arma": {"margem_ameaca": 1, "dano_sangramento": 1}
        },
        "page": 402
    },
    {
        "id": "osso_de_megalokk",
        "name": "Osso de Megalokk",
        "type": "material_especial",
        "description": "Ossos fossilizados imbuídos com a fúria primal do Deus dos Monstros.",
        "precos_adicionais": {
            "arma": 1800,
            "armadura": 1200
        },
        "efeitos": {
            "arma": {"dano_adicional_furia": 2},
            "armadura": {"intimidacao": 2}
        },
        "page": 402
    },
    {
        "id": "pederneira_vulcanica",
        "name": "Pederneira Vulcânica",
        "type": "material_especial",
        "description": "Rocha mineral ígnea de vulcões ativos que faisca calor constante.",
        "precos_adicionais": {
            "arma": 1000,
            "arma_de_fogo": 1500
        },
        "efeitos": {
            "arma": {"dano_fogo": "1d4"},
            "arma_de_fogo": {"recarregar_acao": "reduz um passo"}
        },
        "page": 402
    },
    {
        "id": "prata_draconica",
        "name": "Prata Dracônica",
        "type": "material_especial",
        "description": "Liga metálica ancestral purificada sob o fogo de dragões de prata.",
        "precos_adicionais": {
            "arma": 2000,
            "esoterico": 2000
        },
        "efeitos": {
            "arma": {"dano_mortos_vivos_licantropos": "1d6 luz"},
            "esoterico": {"magias_luz_dano": 2}
        },
        "page": 402
    },
    {
        "id": "quitina_razza",
        "name": "Quitina Razza",
        "type": "material_especial",
        "description": "Quitina ultrarresistente do temível razza'kham, troféu supremo de caçadores de monstros.",
        "precos_adicionais": {
            "arma": 3000,
            "armadura_leve": 1500,
            "armadura_pesada": 4500,
            "escudo": 1500,
            "esoterico": 3000
        },
        "efeitos": {
            "arma": {"dado_extra_no_maximo": True},
            "armadura_leve": {"percepcao": 2, "defesa": 1},
            "armadura_pesada": {"percepcao": 5, "defesa": 2},
            "escudo": {"percepcao": 2, "defesa": 1},
            "esoterico": {"dado_extra_dano_magia_no_maximo": True}
        },
        "page": 401
    }
]
