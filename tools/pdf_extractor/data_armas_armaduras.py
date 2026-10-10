"""
Definições de Armas, Armaduras e Escudos de Ameaças de Arton (Capítulo 3).
"""

ARMAS = [
    # Armas Simples
    {
        "id": "porrete",
        "name": "Porrete",
        "type": "arma",
        "proficiencia": "simples",
        "proposito": "corpo_a_corpo",
        "empunhadura": "leve",
        "preco": 2,
        "dano": "1d6",
        "critico": "x2",
        "alcance": None,
        "tipo_dano": "impacto",
        "espacos": 1,
        "habilidades": [],
        "especial": {},
        "description": "Um pedaço de madeira pesado e tosco, comum entre bandidos, capangas e povos rústicos.",
        "page": 394,
        "subpath": "simples/porrete.json"
    },
    {
        "id": "zarabatana",
        "name": "Zarabatana",
        "type": "arma",
        "proficiencia": "simples",
        "proposito": "ataque_a_distancia",
        "empunhadura": "uma_mao",
        "preco": 5,
        "dano": "1d3",
        "critico": "x2",
        "alcance": "curto",
        "tipo_dano": "perfuracao",
        "espacos": 1,
        "habilidades": ["disparo"],
        "especial": {
            "inoculacao_veneno_bonus_cd": 2
        },
        "description": "Tubo longo através do qual pequenos dardos são soprados. Ideal para inocular venenos; a CD para resistir ao veneno dos dardos aumenta em +2.",
        "page": 394,
        "subpath": "simples/zarabatana.json"
    },
    # Armas Marciais
    {
        "id": "neko_te",
        "name": "Neko-te",
        "type": "arma",
        "proficiencia": "marcial",
        "proposito": "corpo_a_corpo",
        "empunhadura": "leve",
        "preco": 10,
        "dano": "1d4",
        "critico": "19",
        "alcance": None,
        "tipo_dano": "corte",
        "espacos": 1,
        "habilidades": ["agil"],
        "especial": {
            "esconder_bonus": 5
        },
        "description": "Luva de couro com garras metálicas afiadas nas pontas dos dedos, típica de Tamu-ra. É uma arma ágil e pode ser escondida facilmente com +5 em testes de Ladinagem.",
        "page": 394,
        "subpath": "marciais/neko_te.json"
    },
    {
        "id": "gladio",
        "name": "Gládio",
        "type": "arma",
        "proficiencia": "marcial",
        "proposito": "corpo_a_corpo",
        "empunhadura": "uma_mao",
        "preco": 12,
        "dano": "1d6",
        "critico": "19/x3",
        "alcance": None,
        "tipo_dano": "perfuracao",
        "espacos": 1,
        "habilidades": ["versatil"],
        "especial": {},
        "description": "Espada curta e reta com ponta reforçada usada pelas legiões do Império de Tauron. Causa golpes penetrantes devastadores.",
        "page": 394,
        "subpath": "marciais/gladio.json"
    },
    {
        "id": "tetsubo",
        "name": "Tetsubo",
        "type": "arma",
        "proficiencia": "marcial",
        "proposito": "corpo_a_corpo",
        "empunhadura": "duas_maos",
        "preco": 20,
        "dano": "1d10",
        "critico": "x2",
        "alcance": None,
        "tipo_dano": "impacto",
        "espacos": 2,
        "habilidades": ["versatil"],
        "especial": {
            "derrubar_empurrar_bonus": 2
        },
        "description": "Versão mais pesada e sofisticada do tacape, geralmente reforçado com anéis metálicos, rebites e cravos. Fornece +2 em testes para derrubar ou empurrar.",
        "page": 394,
        "subpath": "marciais/tetsubo.json"
    },
    # Armas de Fogo
    {
        "id": "traque",
        "name": "Traque",
        "type": "arma",
        "proficiencia": "fogo",
        "proposito": "ataque_a_distancia",
        "empunhadura": "leve",
        "preco": 75,
        "dano": "2d6",
        "critico": "19/x3",
        "alcance": "curto",
        "tipo_dano": "perfuracao",
        "espacos": 1,
        "habilidades": ["disparo"],
        "especial": {
            "defeito_resultado_impar": "emperra"
        },
        "description": "Arma de fogo rústica feita com sucata e materiais de segunda mão, suscetível a falhar. Se errar um ataque com resultado ímpar no d20, emperra até ser desarmada.",
        "page": 394,
        "subpath": "fogo/traque.json"
    },
    {
        "id": "arcabuz",
        "name": "Arcabuz",
        "type": "arma",
        "proficiencia": "fogo",
        "proposito": "ataque_a_distancia",
        "empunhadura": "duas_maos",
        "preco": 800,
        "dano": "2d10",
        "critico": "19/x3",
        "alcance": "medio",
        "tipo_dano": "perfuracao",
        "espacos": 2,
        "habilidades": ["disparo"],
        "especial": {},
        "description": "Arma longa de fogo primitiva, antecessora do mosquete, com cano pesado e boca alargada, disparando projéteis de alto impacto.",
        "page": 394,
        "subpath": "fogo/arcabuz.json"
    },
    {
        "id": "bacamarte",
        "name": "Bacamarte",
        "type": "arma",
        "proficiencia": "fogo",
        "proposito": "ataque_a_distancia",
        "empunhadura": "duas_maos",
        "preco": 450,
        "dano": "4d6",
        "critico": "19/x3",
        "alcance": "especial",
        "tipo_dano": "perfuracao",
        "espacos": 2,
        "habilidades": ["disparo"],
        "especial": {
            "cone_ou_dispersao": "atinge todos em cone curto de 4,5m"
        },
        "description": "Arma de fogo curta de cano largo que dispara estilhaços em área cônica curta, devastadora a curta distância.",
        "page": 394,
        "subpath": "fogo/bacamarte.json"
    },
    # Armas Exóticas
    {
        "id": "acoite_finntroll",
        "name": "Açoite Finntroll",
        "type": "arma",
        "proficiencia": "exotica",
        "proposito": "corpo_a_corpo",
        "empunhadura": "uma_mao",
        "preco": 30,
        "dano": "1d8",
        "critico": "x2",
        "alcance": None,
        "tipo_dano": "corte",
        "espacos": 1,
        "habilidades": ["alongada", "desarmar"],
        "especial": {},
        "description": "Chicote espinhoso e pesado forjado com técnicas cruéis dos trolls nobres de Finntroll.",
        "page": 394,
        "subpath": "exoticas/acoite_finntroll.json"
    },
    {
        "id": "espada_vespa",
        "name": "Espada Vespa",
        "type": "arma",
        "proficiencia": "exotica",
        "proposito": "corpo_a_corpo",
        "empunhadura": "uma_mao",
        "preco": 75,
        "dano": "2d4",
        "critico": "18",
        "alcance": None,
        "tipo_dano": "corte ou perfuracao",
        "espacos": 1,
        "habilidades": ["agil"],
        "especial": {},
        "description": "Lâmina sinuosa extremamente leve e rápida com dentes de serrilha invertida, criada por duelistas e assassinos.",
        "page": 394,
        "subpath": "exoticas/espada_vespa.json"
    },
    {
        "id": "pistola_punhal",
        "name": "Pistola-Punhal",
        "type": "arma",
        "proficiencia": "exotica",
        "proposito": "corpo_a_corpo",
        "empunhadura": "leve",
        "preco": 300,
        "dano": "1d4 / 2d6",
        "critico": "19 / 19/x3",
        "alcance": "curto",
        "tipo_dano": "perfuracao",
        "espacos": 1,
        "habilidades": ["dupla", "disparo"],
        "especial": {
            "arma_combinada": "punhal corpo a corpo acoplado a pistola de disparo único"
        },
        "description": "Arma híbrida engenhosa combinando a lâmina de um punhal com o cano de uma pistola.",
        "page": 394,
        "subpath": "exoticas/pistola_punhal.json"
    },
    {
        "id": "mordida_do_diabo",
        "name": "Mordida do Diabo",
        "type": "arma",
        "proficiencia": "exotica",
        "proposito": "corpo_a_corpo",
        "empunhadura": "leve",
        "preco": 30,
        "dano": "1d4",
        "critico": "x2",
        "alcance": None,
        "tipo_dano": "perfuracao",
        "espacos": 1,
        "habilidades": ["agil"],
        "especial": {
            "prender_arma": "concede bônus em testes de desarmar e quebrar armas"
        },
        "description": "Adaga com lâminas móveis acionadas por mola que se abrem ao atingir o alvo ou para prender armas inimigas.",
        "page": 394,
        "subpath": "exoticas/mordida_do_diabo.json"
    },
    {
        "id": "presa_de_serpente",
        "name": "Presa de Serpente",
        "type": "arma",
        "proficiencia": "exotica",
        "proposito": "corpo_a_corpo",
        "empunhadura": "uma_mao",
        "preco": 1000,
        "dano": "1d8",
        "critico": "17",
        "alcance": None,
        "tipo_dano": "corte",
        "espacos": 1,
        "habilidades": ["agil"],
        "especial": {},
        "description": "Lâmina curva feita da mandíbula de monstros ofídicos, afiada a níveis moleculares com margem de ameaça 17.",
        "page": 394,
        "subpath": "exoticas/presa_de_serpente.json"
    },
    {
        "id": "lanca_de_fogo",
        "name": "Lança de Fogo",
        "type": "arma",
        "proficiencia": "exotica",
        "proposito": "corpo_a_corpo",
        "empunhadura": "duas_maos",
        "preco": 1000,
        "dano": "1d8 / 2d8",
        "critico": "x3 / 19/x3",
        "alcance": "curto",
        "tipo_dano": "perfuracao e fogo",
        "espacos": 2,
        "habilidades": ["alongada"],
        "especial": {
            "disparo_acoplado": "+1d8 de fogo contra oponente adjacente; exige proficiência em armas de fogo para disparar"
        },
        "description": "Lança longa equipada com um tubo de pólvora na ponta, capaz de desferir ataques perfurantes e rajadas flamejantes.",
        "page": 394,
        "subpath": "exoticas/lanca_de_fogo.json"
    },
    {
        "id": "shuriken",
        "name": "Shuriken",
        "type": "arma",
        "proficiencia": "exotica",
        "proposito": "ataque_a_distancia",
        "empunhadura": "leve",
        "preco": 1,
        "dano": "1d4",
        "critico": "x2",
        "alcance": "curto",
        "tipo_dano": "perfuracao",
        "espacos": 0.5,
        "habilidades": ["arremesso"],
        "especial": {
            "ataque_adicional": "Uma vez por rodada ao atacar com shuriken, gaste 1 PM para um ataque adicional contra o mesmo alvo."
        },
        "description": "Projéteis de arremesso em forma de estrela. Permite desferir rajadas rápidas contra o mesmo alvo.",
        "page": 394,
        "subpath": "exoticas/shuriken.json"
    },
    {
        "id": "arpao",
        "name": "Arpão",
        "type": "arma",
        "proficiencia": "exotica",
        "proposito": "ataque_a_distancia",
        "empunhadura": "uma_mao",
        "preco": 30,
        "dano": "1d10",
        "critico": "x3",
        "alcance": "curto",
        "tipo_dano": "perfuracao",
        "espacos": 1,
        "habilidades": ["arremesso"],
        "especial": {
            "fisgar": "Se causar dano, o alvo fica fisgado e preso pela corda"
        },
        "description": "Lança de pesca pesada farpada com corda presa à empunhadura, usada para fisgar e puxar criaturas marinhas e inimigos.",
        "page": 394,
        "subpath": "exoticas/arpao.json"
    }
]

ARMADURAS = [
    {
        "id": "armadura_de_ossos",
        "name": "Armadura de Ossos",
        "type": "armadura",
        "categoria": "leve",
        "preco": 120,
        "bonus_defesa": 3,
        "penalidade_armadura": -2,
        "espacos": 2,
        "especial": {
            "intimidacao_bonus": 1,
            "cd_medo_bonus": 1
        },
        "description": "Produzida por nezumi e xamãs tribais com ossadas trabalhadas. Fornece +1 em Intimidação e na CD de seus efeitos de medo.",
        "page": 395,
        "subpath": "leves/armadura_de_ossos.json"
    },
    {
        "id": "veste_de_teia_de_aranha",
        "name": "Veste de Teia de Aranha",
        "type": "armadura",
        "categoria": "leve",
        "preco": 3000,
        "bonus_defesa": 4,
        "penalidade_armadura": 0,
        "espacos": 2,
        "especial": {
            "furtividade_bonus": 5,
            "sem_material_especial": True
        },
        "description": "Feita de teia de aranha gigante, maleável, silenciosa e forte como aço. Fornece +5 em Furtividade.",
        "page": 395,
        "subpath": "leves/veste_de_teia_de_aranha.json"
    },
    {
        "id": "armadura_de_quitina",
        "name": "Armadura de Quitina",
        "type": "armadura",
        "categoria": "pesada",
        "preco": 350,
        "bonus_defesa": 7,
        "penalidade_armadura": -3,
        "espacos": 5,
        "especial": {
            "nao_reduz_deslocamento": True
        },
        "description": "Feita com carapaças de insetos gigantes dos povos-trovão. Mais leve que contrapartes metálicas, não reduz o deslocamento do usuário.",
        "page": 395,
        "subpath": "pesadas/armadura_de_quitina.json"
    }
]

ESCUDOS = [
    {
        "id": "escudo_de_couro",
        "name": "Escudo de Couro",
        "type": "escudo",
        "categoria": "leve",
        "preco": 3,
        "bonus_defesa": 1,
        "penalidade_armadura": -1,
        "espacos": 1,
        "especial": {
            "bonus_defesa_ataques_distancia": 2,
            "nao_pode_atacar": True
        },
        "description": "Armação de madeira esticando couro flexível amarrado ao braço. Contra ataques à distância seu bônus na Defesa aumenta em +2.",
        "page": 395,
        "subpath": "escudo_de_couro.json"
    }
]
