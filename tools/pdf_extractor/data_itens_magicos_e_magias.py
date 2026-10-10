"""
Definições de Itens Mágicos, Artefatos e Novas Magias de Ameaças de Arton (Capítulo 3, p. 404-407).
"""

ITENS_MAGICOS = [
    {
        "id": "chifre_de_unicornio",
        "name": "Chifre de Unicórnio",
        "categoria": "maior",
        "preco": 60000,
        "description": "Poderoso item de cura. Se estiver empunhando, pode lançar Curar Ferimentos e Purificação (-1 PM caso já conheça). Permite lançar Segunda Chance uma única vez (perde poderes). Pode ser empunhado como espada curta formidável ou moído em 12 doses de pó de chifre.",
        "page": 404,
        "efeito": {
            "magias_concedidas": ["curar_ferimentos", "purificacao", "segunda_chance"],
            "arma": "espada_curta_formidavel"
        }
    },
    {
        "id": "fragmento_de_filacterio",
        "name": "Fragmento de Filactério",
        "categoria": "maior",
        "preco": 45000,
        "description": "Fragmento do receptáculo da alma de um lich. Concede +2 na CD para resistir a magias de necromancia e permite lançar Toque Vampírico como reação ao sofrer dano (3 vezes por dia).",
        "page": 404,
        "efeito": {
            "cd_necromancia": 2,
            "reacao_toque_vampirico": 3
        }
    },
    {
        "id": "grilhao_de_descrenca",
        "name": "Grilhão de Descrença",
        "categoria": "maior",
        "preco": 50000,
        "description": "Corrente pesada forjada por hereges puristas. Uma criatura presa pelos grilhões não pode lançar magias divinas, canalizar energia ou usar poderes concedidos de deuses.",
        "page": 404,
        "efeito": {
            "bloqueio_magia_divina": True,
            "bloqueio_poderes_concedidos": True
        }
    },
    {
        "id": "pilao_conspurcado",
        "name": "Pilão Conspurcado",
        "categoria": "medio",
        "preco": 24000,
        "description": "Pequeno pilão de madeira com símbolos místicos e fragmentos de ossos. Conta como uma costela de lich para magias de trevas e aumenta em +1d6 o dano de preparados corrosivos e venenos nele macerados.",
        "page": 405,
        "efeito": {
            "aprimoramento_alquimia_venenos": "+1d6 dano",
            "foco_trevas": True
        }
    },
    {
        "id": "pistola_demoniaca",
        "name": "Pistola Demoníaca",
        "categoria": "maior",
        "preco": 75000,
        "description": "Pistola forjada em pacto com um demônio da pólvora. Está sempre carregada e não precisa de munição. Dispara chamas sulfurosas (2d6 perfuração + 2d6 fogo). Exige teste de Vontade CD 25 diário para resistir ao impulso homicida.",
        "page": 405,
        "efeito": {
            "municao_infinita": True,
            "dano_fogo_extra": "2d6",
            "maldicao_impulso_homicida": "Vontade CD 25"
        }
    },
    {
        "id": "uyzrrak_daukthra",
        "name": "Uyzrrak da'Ukthra",
        "categoria": "maior",
        "preco": 80000,
        "description": "Cetro ancestral dos sacerdotes lefeu feito de quitina avermelhada pulsante. Suas magias causam +1d8 de dano de matéria vermelha e concedem 1 ponto de Tormenta temporário ao usuário na cena.",
        "page": 405,
        "efeito": {
            "dano_materia_vermelha": "1d8",
            "afinidade_tormenta": True
        }
    },
    # Artefatos
    {
        "id": "amuleto_do_abutre",
        "name": "Amuleto do Abutre",
        "categoria": "artefato",
        "preco": 0,
        "description": "Artefato do Arquilich Ferren Asloth. Concede +50 PM (após 1 dia de uso), +5 na CD de magias arcanas e a habilidade Conhecimento Sequestrado. Funciona como segundo filactério de Ferren; falhas em Vontade diária (CD 20+) corrompem e destroem a alma do portador.",
        "page": 405,
        "efeito": {
            "pm_extra": 50,
            "cd_magias_arcanas": 5,
            "conhecimento_sequestrado": True,
            "maldicao_filacterio": "Vontade CD 20+1 por dia"
        }
    },
    {
        "id": "rompedor_da_realidade",
        "name": "Rompedor da Realidade",
        "categoria": "artefato",
        "preco": 0,
        "description": "Machado de guerra gigante lefeu atroz pungente anticriatura (não lefeu) magnífico de matéria vermelha. Ignora redução de dano, fortificação e imunidade a críticos. Vítimas atingidas perdem 1 ponto de atributo aleatório permanentemente (Fort CD For evita). Não lefeu que empunhe fica debilitado.",
        "page": 405,
        "efeito": {
            "ignora_rd_fortificacao_critico": True,
            "dreno_atributo_permanente": "1 ponto permanente",
            "empunhadura_nao_lefeu": "debilitado"
        }
    }
]

MAGIAS = [
    {
        "id": "acoite_flamejante",
        "name": "Açoite Flamejante",
        "type": "arcana",
        "circle": "1",
        "school": "conv",
        "execution": "padrão",
        "range": "pessoal",
        "duration": "sustentada",
        "resistence": {
            "effect": "Reflexos reduz parcial",
            "skill": "reflexos"
        },
        "description": "Um açoite de fogo surge em sua mão. Como ação padrão causa 2d6 pontos de dano de fogo em alcance curto e deixa o alvo em chamas e enredado enquanto durarem as chamas (Reflexos reduz à metade e evita chamas).",
        "enhancements": [
            {"cost": 2, "type": "muda", "description": "muda a execução para movimento."},
            {"cost": 2, "type": "muda", "description": "muda o dano para 4d6. Requer 2º círculo."},
            {"cost": 5, "type": "muda", "description": "muda o dano para 6d6. Requer 3º círculo."}
        ],
        "effects": [{"type": "dano", "amount": "2d6", "damage_type": "fogo"}],
        "page": 406
    },
    {
        "id": "dardo_gelido",
        "name": "Dardo Gélido",
        "type": "arcana",
        "circle": "1",
        "school": "evoc",
        "execution": "padrão",
        "range": "curto",
        "target": {"amount": 1, "type": "criatura"},
        "duration": "instantânea",
        "resistence": {
            "effect": "Fortitude parcial",
            "skill": "fortitude"
        },
        "description": "Você dispara um dardo de gelo que causa 2d6 pontos de dano de frio e deixa o alvo lento por 1 rodada (Fortitude reduz dano à metade e evita a condição).",
        "enhancements": [
            {"cost": 1, "type": "aumenta", "description": "aumenta o dano em +1d6."},
            {"cost": 1, "type": "aumenta", "description": "aumenta o número de alvos em +1 (limitado pelo círculo máximo)."}
        ],
        "effects": [{"type": "dano", "amount": "2d6", "damage_type": "frio"}],
        "page": 406
    },
    {
        "id": "invocar_fagulha_elemental",
        "name": "Invocar Fagulha Elemental",
        "type": "arcana",
        "circle": "2",
        "school": "conv",
        "execution": "completa",
        "range": "curto",
        "duration": "sustentada",
        "description": "Transforma porção inerte de elemento em elemental Pequeno (ar, água, fogo ou terra) que funciona como familiar comum ou elemental, auxiliando apenas você sem contar no limite de parceiros.",
        "enhancements": [
            {"cost": 1, "type": "especial", "description": "além do normal, fornece redução 10 contra o dano correspondente."},
            {"cost": 2, "type": "especial", "description": "recebe a habilidade de dois familiares, um comum e um elemental."}
        ],
        "page": 406
    },
    {
        "id": "jato_corrosivo",
        "name": "Jato Corrosivo",
        "type": "arcana",
        "circle": "1",
        "school": "evoc",
        "execution": "padrão",
        "range": "pessoal",
        "area": "linha de 9m",
        "duration": "instantânea",
        "resistence": {
            "effect": "Reflexos reduz à metade",
            "skill": "reflexos"
        },
        "description": "Dispara jato que causa 2d6 pontos de dano de ácido a criaturas na área (+1 por dado contra construtos e objetos soltos).",
        "enhancements": [
            {"cost": 1, "type": "aumenta", "description": "aumenta o dano em +1d6."},
            {"cost": 1, "type": "muda", "description": "muda resistência para Reflexos parcial (se falhar, fica vulnerável)."}
        ],
        "effects": [{"type": "dano", "amount": "2d6", "damage_type": "acido"}],
        "page": 406
    },
    {
        "id": "katana_celestial",
        "name": "Katana Celestial",
        "type": "divina",
        "circle": "5",
        "school": "evoc",
        "execution": "padrão",
        "range": "pessoal",
        "area": "linha de 60m ou duas linhas de 30m em V",
        "duration": "instantânea",
        "resistence": {
            "effect": "Reflexos parcial",
            "skill": "reflexos"
        },
        "description": "Golpe sagrado dos céus. Causa 12d8 pontos de dano de luz (12d12 em mortos-vivos) e deixa os alvos cegos e surdos até o fim da cena (Reflexos reduz à metade e evita as condições).",
        "enhancements": [
            {"cost": 3, "type": "aumenta", "description": "aumenta o dano em +2d8 (+2d12 contra mortos-vivos)."},
            {"cost": 6, "type": "muda", "description": "muda a área para linha de 120m ou quatro linhas de 30m em X."}
        ],
        "effects": [{"type": "dano", "amount": "12d8", "damage_type": "luz"}],
        "page": 406
    },
    {
        "id": "momento_de_tormenta",
        "name": "Momento de Tormenta",
        "type": "universal",
        "circle": "2",
        "school": "conv",
        "execution": "completa",
        "range": "pessoal",
        "area": "cubo de 30m",
        "duration": "sustentada",
        "description": "Nuvem rubra surge acima do conjurador. Como ação de movimento a cada turno manifesta chuva ácida (6d4 ácido), neblina venenosa (2d12 perda PV), raios escarlates (6d8 eletricidade em até 6 alvos) ou pesadelos reais (4d6 psíquico e perde 1d4 PM).",
        "enhancements": [
            {"cost": 3, "type": "aumenta", "description": "aumenta o dano em +1 dado do mesmo tipo."},
            {"cost": 5, "type": "especial", "description": "criaturas na área ficam alquebradas enquanto permanecerem nela."},
            {"cost": 5, "type": "especial", "description": "(Apenas Aharadak) muda área para círculo de 1km de raio."}
        ],
        "page": 406
    },
    {
        "id": "transformacao_em_dragao",
        "name": "Transformação em Dragão",
        "type": "arcana",
        "circle": "4",
        "school": "trans",
        "execution": "completa",
        "range": "pessoal",
        "target": {"type": "voce"},
        "duration": "sustentada",
        "description": "Invoca o poder de um dragão. Recebe +2 em Força, Constituição, Inteligência e Carisma, +5 na Defesa, redução 30 contra o elemento do sopro e pode exalar cone de 9m causando 8d6+8 de dano como ação padrão.",
        "enhancements": [
            {"cost": 3, "type": "aumenta", "description": "aumenta o bônus nos atributos para +4, a Defesa para +10 e o dano do sopro para 12d6+12. Requer 5º círculo."}
        ],
        "effects": [
            {"type": "modificador_atributo", "amount": 2},
            {"type": "defesa", "amount": 5}
        ],
        "page": 407
    }
]
