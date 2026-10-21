# frozen_string_literal: true

require_relative "../src/ruby/tormenta20"
require_relative "seeds_helpers"
require "json"

# Seed script to import JSON data into SQLite database

module Tormenta20
  # Seeds module for importing JSON data into the SQLite database.
  #
  # This module provides methods to import all Tormenta20 game data
  # from JSON files into the database.
  #
  # @example Import all data
  #   Tormenta20::Seeds.import_all
  #
  # @example Clear and reimport
  #   Tormenta20::Seeds.clear_all
  #   Tormenta20::Seeds.import_all
  module Seeds
    JSON_BASE_PATH = File.expand_path("../src/json", __dir__)

    # -------------------------------------------------------------------------
    # Table attribute lists + row transforms shared by the importers below.
    # Kept at module level (not inside `class << self`) so callers — and the
    # specs — can address them as `Tormenta20::Seeds::NAME`.
    # -------------------------------------------------------------------------
    RACAS_ATTRS = %i[
      id name description size movement vision vision_range attribute_bonuses
      skill_bonuses racial_abilities chosen_abilities_amount
      available_chosen_abilities page livro_id longevidade devotos
    ].freeze

    ENCANTAMENTOS_ATTRS = %i[id name description categoria escudo_only conta_como_dois prerequisitos efeito].freeze

    # Coerces the boolean flags to the 0/1 the DB stores and defaults the
    # optional JSON columns, mirroring bin/build_db's seed_encantamentos.
    ENCANTAMENTOS_TRANSFORM = lambda do |data|
      data.slice(*ENCANTAMENTOS_ATTRS).tap do |row|
        row[:escudo_only]     = row[:escudo_only] ? 1 : 0
        row[:conta_como_dois] = row[:conta_como_dois] ? 1 : 0
        row[:prerequisitos] ||= []
        row[:efeito]        ||= {}
      end
    end

    POCOES_ATTRS = %i[id name subtipo spell_id pm_cost categoria preco roll_min roll_max aprimoramento description].freeze

    POCOES_TRANSFORM = ->(data) { data.slice(*POCOES_ATTRS) }

    ACESSORIOS_ATTRS = %i[id name categoria preco roll_min roll_max description efeito].freeze

    # Mirrors bin/build_db's seed_acessorios: the structured effect defaults
    # to an empty hash when the JSON omits it.
    ACESSORIOS_TRANSFORM = lambda do |data|
      data.slice(*ACESSORIOS_ATTRS).tap { |row| row[:efeito] ||= {} }
    end

    REGRAS_BASE_KEYS = %i[id name description].freeze

    # Everything that is not id/name/description lands in the free-form
    # `data` JSON column (mirrors bin/build_db's seed_regras).
    REGRAS_TRANSFORM = lambda do |raw|
      data_content = raw.reject { |k, _| REGRAS_BASE_KEYS.include?(k) }
      { id: raw[:id], name: raw[:name], description: raw[:description], data: data_content }
    end

    CONDICOES_ATTRS = %i[id name description effects condition_type escalates_to].freeze

    PERICIAS_ATTRS = %i[id name atributo trained_only armor_penalty resistance_skill description uses].freeze

    PERICIA_BOOLEAN_ATTRS = %i[trained_only armor_penalty resistance_skill].freeze

    # The three flag columns are INTEGER, so coerce the JSON booleans to 0/1
    # exactly like bin/build_db's seed_pericias.
    PERICIAS_TRANSFORM = lambda do |data|
      PERICIA_BOOLEAN_ATTRS.each { |attr| data[attr] = data[attr] ? 1 : 0 }
      data
    end

    TABELAS_ATTRS = %i[id name description headers rows].freeze

    class << self
      def import_all
        check_no_needs_review!
        puts "Starting data import..."
        puts "=" * 60

        import_livros
        import_racas
        import_habilidades_de_raca
        import_origens
        import_poderes_habilidades_unicas
        import_divindades
        import_poderes_concedidos
        import_poderes_tormenta
        import_poderes_gerais
        import_classes
        import_habilidades_de_classe
        import_magias
        import_equipamentos
        import_itens_superiores
        import_itens_magicos
        import_regras
        import_condicoes
        import_pericias
        import_tabelas
        import_indice_remissivo

        puts "=" * 60
        puts "Data import completed!"
        print_summary
      end

      # =======================================================================
      # LIVROS
      # =======================================================================
      def import_livros
        puts "\nImporting livros..."

        json_dir = File.join(JSON_BASE_PATH, "livros")
        unless Dir.exist?(json_dir)
          puts "  Directory not found: #{json_dir}"
          return
        end

        files = Dir.glob(File.join(json_dir, "*.json"))
        puts "  Found #{files.size} files"

        success_count = 0
        error_count = 0

        files.each_with_index do |file, index|
          data = JSON.parse(File.read(file), symbolize_names: true)
          row = livro_row(data)
          next if row[:id].nil?

          record = Models::Livro.find_or_initialize_by(id: row[:id])
          record.nome       = row[:nome]
          record.nome_curto = row[:nome_curto]
          record.save!

          success_count += 1
          print "\r  Imported: #{index + 1}/#{files.size}" if ((index + 1) % 10).zero?
        rescue StandardError => e
          error_count += 1
          puts "\n  Error importing #{File.basename(file)}: #{e.message}"
        end

        puts "\n  Successfully imported #{success_count} livros"
        puts "  Failed to import #{error_count} livros" if error_count.positive?
      end

      # Build the attribute hash for a single livro row from raw JSON.
      def livro_row(data)
        { id: data[:id], nome: data[:nome], nome_curto: data[:nome_curto] }
      end

      # =======================================================================
      # RAÇAS
      # =======================================================================
      def import_racas
        import_json_files("racas", Models::Raca, RACAS_ATTRS)
      end

      # =======================================================================
      # PODERES - HABILIDADES DE RAÇA
      # =======================================================================
      def import_habilidades_de_raca
        base_dir = File.join(JSON_BASE_PATH, "poderes", "habilidades_de_raca")
        unless Dir.exist?(base_dir)
          puts "  Directory not found: #{base_dir}"
          return
        end

        files = Dir.glob(File.join(base_dir, "**", "*.json"))
        puts "\nImporting habilidades_de_raca..."
        puts "  Found #{files.size} files"

        success_count = 0
        error_count = 0

        files.each do |file|
          persist_poder_row(habilidade_de_raca_row(file))
          success_count += 1
        rescue StandardError => e
          error_count += 1
          puts "\n  Error importing #{File.basename(file)}: #{e.message}"
        end

        puts "\n  Successfully imported #{success_count} habilidades_de_raca"
        puts "  Failed to import #{error_count} habilidades_de_raca" if error_count.positive?
      end

      # =======================================================================
      # ORIGENS
      # =======================================================================
      def import_origens
        import_json_files(
          "origens",
          Models::Origem,
          %i[id name description items benefits unique_power]
        )
      end

      # =======================================================================
      # PODERES - HABILIDADES ÚNICAS DE ORIGEM
      # =======================================================================
      def import_poderes_habilidades_unicas
        import_json_files(
          "poderes/habilidades_unicas_de_origem",
          Models::Poder,
          %i[id name description effects prerequisites],
          extra_attrs: { type: "habilidade_unica_origem" },
          transform: lambda { |data|
            data[:origin_id] = data.delete(:origin) if data[:origin]
            data
          }
        )
      end

      # =======================================================================
      # DIVINDADES
      # =======================================================================
      def import_divindades
        import_json_files(
          "deuses",
          Models::Divindade,
          %i[id name title description beliefs_objectives holy_symbol energy
             preferred_weapon devotees granted_powers obligations_restrictions]
        )
      end

      # =======================================================================
      # PODERES CONCEDIDOS
      # =======================================================================
      def import_poderes_concedidos
        import_json_files(
          "poderes/poderes_concedidos",
          Models::Poder,
          %i[id name description effects prerequisites deities],
          extra_attrs: { type: "poder_concedido" }
        )
      end

      # =======================================================================
      # PODERES DA TORMENTA
      # =======================================================================
      def import_poderes_tormenta
        import_json_files(
          "poderes/poderes_da_tormenta",
          Models::Poder,
          %i[id name description effects prerequisites],
          extra_attrs: { type: "poder_tormenta" }
        )
      end

      # =======================================================================
      # PODERES GERAIS (combate, destino, magia)
      # =======================================================================
      def import_poderes_gerais
        puts "\nImporting poderes_gerais..."

        json_dir = File.join(JSON_BASE_PATH, "poderes/poderes_gerais")
        return puts "  Directory not found: #{json_dir}" unless Dir.exist?(json_dir)

        files = Dir.glob(File.join(json_dir, "**", "*.json"))
        puts "  Found #{files.size} files"

        success_count = 0
        error_count = 0

        files.each_with_index do |file, index|
          data = JSON.parse(File.read(file), symbolize_names: true)

          record = Models::Poder.find_or_initialize_by(id: data[:id])
          record.name        = data[:name]
          record.type        = data[:type]
          record.description = data[:description]
          record.effects     = data[:effects] || []
          record.costs       = data[:costs] || []
          record.prerequisites = data[:requirements] || []
          record.save!

          success_count += 1
          print "\r  Imported: #{index + 1}/#{files.size}" if ((index + 1) % 10).zero?
        rescue StandardError => e
          error_count += 1
          puts "\n  Error importing #{File.basename(file)}: #{e.message}"
        end

        puts "\n  Successfully imported #{success_count} poderes_gerais"
        puts "  Failed to import #{error_count} poderes_gerais" if error_count.positive?
      end

      # =======================================================================
      # CLASSES
      # =======================================================================
      def import_classes
        import_json_files(
          "classes",
          Models::Classe,
          %i[id name hit_points mana_points skills proficiencies abilities powers progression spellcasting]
        )
      end

      # =======================================================================
      # PODERES - HABILIDADES DE CLASSE
      # =======================================================================
      def import_habilidades_de_classe
        base_dir = File.join(JSON_BASE_PATH, "poderes", "habilidades_de_classe")
        unless Dir.exist?(base_dir)
          puts "  Directory not found: #{base_dir}"
          return
        end

        files = Dir.glob(File.join(base_dir, "*", "*.json"))
        puts "\nImporting habilidades_de_classe..."
        puts "  Found #{files.size} files"

        success_count = 0
        error_count = 0

        files.each do |file|
          persist_poder_row(habilidade_de_classe_row(file))
          success_count += 1
        rescue StandardError => e
          error_count += 1
          puts "\n  Error importing #{File.basename(file)}: #{e.message}"
        end

        puts "\n  Successfully imported #{success_count} habilidades_de_classe"
        puts "  Failed to import #{error_count} habilidades_de_classe" if error_count.positive?
      end

      # =======================================================================
      # MAGIAS
      # =======================================================================
      def import_magias
        puts "\nImporting magias..."

        json_dir = File.join(JSON_BASE_PATH, "magias")
        return puts "  Directory not found: #{json_dir}" unless Dir.exist?(json_dir)

        files = Dir.glob(File.join(json_dir, "**", "*.json"))
        puts "  Found #{files.size} magia files"

        success_count = 0
        error_count = 0

        files.each_with_index do |file, index|
          data = JSON.parse(File.read(file), symbolize_names: true)
          import_magia(data)
          success_count += 1
          print "\r  Imported: #{index + 1}/#{files.size}" if ((index + 1) % 10).zero?
        rescue StandardError => e
          error_count += 1
          puts "\n  Error importing #{File.basename(file)}: #{e.message}"
        end

        puts "\n  Successfully imported #{success_count} magias"
        puts "  Failed to import #{error_count} magias" if error_count.positive?
      end

      def import_magia(data)
        raw_target = data[:target]
        target = if raw_target.is_a?(Hash)
                   raw_target
                 else
                   (raw_target.is_a?(Array) ? raw_target.first || {} : {})
                 end
        effect_details = data[:effect_details].is_a?(Hash) ? data[:effect_details] : {}
        resistance = data[:resistance].is_a?(Hash) ? data[:resistance] : {}
        extra_costs = data[:extra_costs].is_a?(Hash) ? data[:extra_costs] : {}

        Models::Magia.find_or_initialize_by(id: data[:id]).tap do |magia|
          magia.name = data[:name]
          magia.type = data[:type]
          magia.circle = data[:circle]
          magia.school = data[:school]
          magia.execution = data[:execution]
          magia.execution_details = data[:execution_details]
          magia.range = data[:range]
          magia.duration = data[:duration]
          magia.duration_details = data[:duration_details]
          magia.counterspell = data[:counterspell]
          magia.description = data[:description] || ""

          magia.target_amount = target[:amount]
          magia.target_up_to = if target[:up_to].nil?
                                 nil
                               else
                                 (target[:up_to] ? 1 : 0)
                               end
          magia.target_type = target[:type]

          magia.effect = data[:effect]
          magia.effect_shape = effect_details[:shape]
          magia.effect_dimension = effect_details[:dimension]
          magia.effect_size = effect_details[:size]
          magia.effect_other_details = effect_details[:other_details]

          magia.area_effect = data[:area_effect]
          magia.area_effect_details = data[:area_effect_details]

          magia.resistance_effect = resistance[:effect]
          magia.resistance_skill = resistance[:skill]

          magia.extra_costs_material_component = extra_costs[:material_component]
          magia.extra_costs_material_cost = extra_costs[:material_component_cost]
          magia.extra_costs_pm_debuff = extra_costs[:pm_debuff]
          magia.extra_costs_pm_sacrifice = extra_costs[:pm_sacrifice]

          magia.enhancements = data[:enhancements] || []
          magia.effects = data[:effects] || []

          magia.save!
        end
      end

      # =======================================================================
      # EQUIPAMENTOS
      # =======================================================================
      def import_equipamentos
        import_armas
        import_armaduras
        import_escudos
        import_itens
      end

      PROFICIENCIA_TO_CATEGORY = {
        "simples" => "simples",
        "marcial" => "marciais",
        "exotica" => "exoticas",
        "fogo" => "fogo"
      }.freeze

      def import_armas
        import_json_files(
          "equipamentos/armas",
          Models::Arma,
          %i[id name category price damage damage_type critical range weight properties description],
          transform: lambda { |data|
            data[:category]    ||= PROFICIENCIA_TO_CATEGORY[data.delete(:proficiencia).to_s]
            data[:price]       ||= data.delete(:preco)
            data[:damage]      ||= data.delete(:dano)
            data[:damage_type] ||= data.delete(:tipo_dano)
            data[:critical]    ||= data.delete(:critico)
            data[:range]       ||= data.delete(:alcance)
            data[:weight]      ||= data.delete(:espacos)
            data[:properties]  ||= [data.delete(:habilidades), data.delete(:especial)].flatten.compact
            data
          }
        )
      end

      def import_armaduras
        import_json_files(
          "equipamentos/armaduras",
          Models::Armadura,
          %i[id name category price defense_bonus armor_penalty weight properties description],
          transform: lambda { |data|
            data[:category]      ||= data.delete(:categoria)
            data[:price]         ||= data.delete(:preco)
            data[:defense_bonus] ||= data.delete(:bonus_defesa)
            data[:armor_penalty] ||= data.delete(:penalidade_armadura)
            data[:weight]        ||= data.delete(:espacos)
            data[:properties]    ||= [data.delete(:especial)].flatten.compact
            data
          }
        )
      end

      def import_escudos
        import_json_files(
          "equipamentos/escudos",
          Models::Escudo,
          %i[id name price defense_bonus armor_penalty weight properties description],
          transform: lambda { |data|
            data[:price] ||= data.delete(:preco)
            data[:defense_bonus] ||= data.delete(:bonus_defesa)
            data[:armor_penalty] ||= data.delete(:penalidade_armadura)
            data[:weight] ||= data.delete(:espacos)
            data
          }
        )
      end

      def import_itens
        import_json_files(
          "equipamentos/itens",
          Models::Item,
          %i[id name category price weight description effects],
          transform: lambda { |data|
            data[:category] ||= data.delete(:categoria)
            data[:price]    ||= data.delete(:preco)
            data[:weight]   ||= data.delete(:espacos)
            # The item's structured effect lives under `efeito` in most files
            # (with `effects` as a fallback), and animal partner blocks
            # (parceiro, besta_de_carga, alternativo, restricoes,
            # isento_restricao_cavalgar_combate) only become queryable via the
            # DB once merged into effects. Both are handled by the shared
            # helper so bin/build_db stays in sync.
            effects = build_item_effects(data)
            data[:effects] = effects unless effects.empty?
            data
          }
        )
      end

      # =======================================================================
      # ITENS SUPERIORES
      # =======================================================================
      def import_itens_superiores
        import_materiais_especiais
        import_melhorias
        import_encantamentos
      end

      def import_materiais_especiais
        import_json_files(
          "itens_superiores/materiais_especiais",
          Models::MaterialEspecial,
          %i[id name description applicable_to price_modifier effects]
        )
      end

      def import_melhorias
        import_json_files(
          "itens_superiores/melhorias",
          Models::Melhoria,
          %i[id name description applicable_to price effects]
        )
      end

      def import_encantamentos
        import_json_files(
          "itens_superiores/encantamentos",
          Models::Encantamento,
          ENCANTAMENTOS_ATTRS,
          transform: ENCANTAMENTOS_TRANSFORM
        )
      end

      # =======================================================================
      # ITENS MÁGICOS
      # =======================================================================
      def import_itens_magicos
        import_pocoes
        import_acessorios
      end

      def import_pocoes
        import_json_files(
          "itens_magicos/pocoes",
          Models::Pocao,
          POCOES_ATTRS,
          transform: POCOES_TRANSFORM
        )
      end

      def import_acessorios
        import_json_files(
          "itens_magicos/acessorios",
          Models::AcessorioMagico,
          ACESSORIOS_ATTRS,
          transform: ACESSORIOS_TRANSFORM
        )
      end

      # =======================================================================
      # REGRAS
      # =======================================================================
      def import_regras
        import_json_files("regras", Models::Regra, %i[id name description data], transform: REGRAS_TRANSFORM)
      end

      # =======================================================================
      # CONDIÇÕES
      # =======================================================================
      def import_condicoes
        import_json_files("condicoes", Models::Condicao, CONDICOES_ATTRS)
      end

      # =======================================================================
      # PERÍCIAS
      # =======================================================================
      def import_pericias
        import_json_files("pericias", Models::Pericia, PERICIAS_ATTRS, transform: PERICIAS_TRANSFORM)
      end

      # =======================================================================
      # TABELAS
      # =======================================================================
      def import_tabelas
        import_json_files("tabelas", Models::Tabela, TABELAS_ATTRS)
      end

      # =======================================================================
      # ÍNDICE REMISSIVO
      # =======================================================================
      # Each file is named after its livro id and holds a JSON array of entries
      # (`termo`, `pagina`, optional `tabela`/`registro_id`). Mirrors
      # bin/build_db's seed_indice_remissivo.
      def import_indice_remissivo
        json_dir = File.join(JSON_BASE_PATH, "indice_remissivo")
        unless Dir.exist?(json_dir)
          puts "  Directory not found: #{json_dir}"
          return
        end

        puts "\nImporting indice_remissivo..."

        success_count = 0
        error_count = 0

        Dir.glob(File.join(json_dir, "*.json")).sort.each do |file|
          livro_id = File.basename(file, ".json")
          entries = JSON.parse(File.read(file))
          next unless entries.is_a?(Array)

          indice_remissivo_rows(livro_id, entries).each do |row|
            record = Models::IndiceRemissivo.find_or_initialize_by(
              livro_id: row[:livro_id], termo: row[:termo], pagina: row[:pagina]
            )
            record.tabela      = row[:tabela]
            record.registro_id = row[:registro_id]
            record.save!
            success_count += 1
          end
        rescue StandardError => e
          error_count += 1
          puts "\n  Error importing #{File.basename(file)}: #{e.message}"
        end

        puts "\n  Successfully imported #{success_count} entradas de índice remissivo"
        puts "  Failed to import #{error_count} entradas de índice remissivo" if error_count.positive?
      end

      # Build the persistable rows for one livro's index entries, skipping
      # malformed entries without a termo or pagina.
      def indice_remissivo_rows(livro_id, entries)
        entries.filter_map do |entry|
          next unless entry["termo"] && entry["pagina"]

          {
            livro_id: livro_id,
            termo: entry["termo"],
            pagina: entry["pagina"].to_i,
            tabela: entry["tabela"],
            registro_id: entry["registro_id"]
          }
        end
      end

      # =======================================================================
      # PODER HELPERS (habilidades de classe / raça)
      # =======================================================================
      def poder_habilidade_row(data, type:, class_id: nil)
        {
          id: data[:id],
          name: data[:name] || data[:id],
          type: type,
          class_id: class_id,
          description: data[:description],
          effects: data[:effects] || {},
          prerequisites: data[:requirements] || data[:prerequisites] || []
        }
      end

      def habilidade_de_classe_row(file)
        data = JSON.parse(File.read(file), symbolize_names: true)
        poder_habilidade_row(data, type: "poder_classe", class_id: File.basename(File.dirname(file)))
      end

      def habilidade_de_raca_row(file)
        data = JSON.parse(File.read(file), symbolize_names: true)
        poder_habilidade_row(data, type: "habilidade_de_raca")
      end

      def persist_poder_row(row)
        record = Models::Poder.find_or_initialize_by(id: row[:id])
        record.name          = row[:name]
        record.type          = row[:type]
        record.class_id      = row[:class_id]
        record.description   = row[:description]
        record.effects       = row[:effects]
        record.prerequisites = row[:prerequisites]
        record.save!
      end

      # =======================================================================
      # UTILITY METHODS
      # =======================================================================
      def clear_all
        puts "Clearing all data..."
        [
          Models::IndiceRemissivo,
          Models::Poder, Models::Origem, Models::Divindade, Models::Classe,
          Models::Magia, Models::Arma, Models::Armadura, Models::Escudo,
          Models::Item, Models::MaterialEspecial, Models::Melhoria, Models::Encantamento,
          Models::Pocao, Models::AcessorioMagico, Models::Regra, Models::Condicao,
          Models::Pericia, Models::Tabela, Models::Raca, Models::Livro
        ].each(&:delete_all)
        puts "Data cleared!"
      end

      def print_summary
        puts "\nDatabase Summary:"
        puts "-" * 40
        puts "  Racas:              #{Models::Raca.count}"
        puts "  Origens:            #{Models::Origem.count}"
        puts "  Poderes:            #{Models::Poder.count}"
        puts "    - Hab. Unicas:    #{Models::Poder.habilidades_unicas.count}"
        puts "    - Concedidos:     #{Models::Poder.poderes_concedidos.count}"
        puts "    - Tormenta:       #{Models::Poder.poderes_tormenta.count}"
        puts "    - Hab. Classe:    #{Models::Poder.poderes_classe.count}"
        puts "    - Hab. Raca:      #{Models::Poder.by_type("habilidade_de_raca").count}"
        puts "  Divindades:         #{Models::Divindade.count}"
        puts "  Classes:            #{Models::Classe.count}"
        puts "  Magias:             #{Models::Magia.count}"
        puts "  Armas:              #{Models::Arma.count}"
        puts "  Armaduras:          #{Models::Armadura.count}"
        puts "  Escudos:            #{Models::Escudo.count}"
        puts "  Itens:              #{Models::Item.count}"
        puts "  Materiais Esp.:     #{Models::MaterialEspecial.count}"
        puts "  Melhorias:          #{Models::Melhoria.count}"
        puts "  Encantamentos:      #{Models::Encantamento.count}"
        puts "  Pocoes:             #{Models::Pocao.count}"
        puts "  Acessorios Mag.:    #{Models::AcessorioMagico.count}"
        puts "  Regras:             #{Models::Regra.count}"
        puts "  Condicoes:          #{Models::Condicao.count}"
        puts "  Pericias:           #{Models::Pericia.count}"
        puts "  Tabelas:            #{Models::Tabela.count}"
        puts "  Livros:             #{Models::Livro.count}"
        puts "  Indice Remissivo:   #{Models::IndiceRemissivo.count}"
        puts "-" * 40
      end

      private

      # Refuses to seed when any JSON file still carries a `needs_review`
      # flag. Remove the flag (after fixing the data) or delete the file
      # before building. Raises RuntimeError listing every flagged location.
      def check_no_needs_review!
        flagged = []
        Dir.glob(File.join(JSON_BASE_PATH, "**", "*.json")).sort.each do |file|
          data = JSON.parse(File.read(file))
          find_needs_review(data, "$", []).each do |path|
            flagged << "#{file.sub("#{JSON_BASE_PATH}/", "")} at #{path}"
          end
        rescue StandardError => e
          flagged << "#{file.sub("#{JSON_BASE_PATH}/", "")} (unparseable: #{e.message})"
        end

        return if flagged.empty?

        raise "Refusing to seed: #{flagged.size} file(s) still need review:\n  - #{flagged.join("\n  - ")}"
      end

      def find_needs_review(value, path, out)
        case value
        when Hash
          value.each do |key, val|
            if key == "needs_review" && !val.nil? && val != false
              out << path
            else
              find_needs_review(val, "#{path}.#{key}", out)
            end
          end
        when Array
          value.each_with_index { |val, i| find_needs_review(val, "#{path}[#{i}]", out) }
        end
        out
      end

      def import_json_files(subdir, model, attrs, extra_attrs: {}, transform: nil)
        entity_name = subdir.split("/").last
        puts "\nImporting #{entity_name}..."

        json_dir = File.join(JSON_BASE_PATH, subdir)
        unless Dir.exist?(json_dir)
          puts "  Directory not found: #{json_dir}"
          return
        end

        files = Dir.glob(File.join(json_dir, "**", "*.json"))
        puts "  Found #{files.size} files"

        return if files.empty?

        success_count = 0
        error_count = 0

        files.each_with_index do |file, index|
          data = JSON.parse(File.read(file), symbolize_names: true)
          data = transform.call(data) if transform

          record = model.find_or_initialize_by(id: data[:id])
          attrs.each do |attr|
            record.send("#{attr}=", data[attr]) if data.key?(attr)
          end
          extra_attrs.each do |attr, value|
            record.send("#{attr}=", value)
          end
          record.save!

          success_count += 1
          print "\r  Imported: #{index + 1}/#{files.size}" if ((index + 1) % 10).zero?
        rescue StandardError => e
          error_count += 1
          puts "\n  Error importing #{File.basename(file)}: #{e.message}"
        end

        puts "\n  Successfully imported #{success_count} #{entity_name}"
        puts "  Failed to import #{error_count} #{entity_name}" if error_count.positive?
      end
    end
  end
end

# Run seeds if this file is executed directly
if __FILE__ == $PROGRAM_NAME
  ENV["TORMENTA20_DB_MODE"] = "create_on_build"
  Tormenta20::Database.setup
  Tormenta20::Seeds.import_all
end
