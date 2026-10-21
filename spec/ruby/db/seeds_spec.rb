# frozen_string_literal: true

require_relative "../spec_helper"
require_relative "../../../db/seeds"

RSpec.describe Tormenta20::Seeds do
  let(:json_base) { described_class::JSON_BASE_PATH }

  def parse(path)
    JSON.parse(File.read(path), symbolize_names: true)
  end

  # ===========================================================================
  # CONSTRAINT: Models::Base#readonly? makes the DB unwritable at runtime, so
  # the importers cannot be exercised end-to-end. These specs cover the pure
  # row/transform logic each importer feeds into the model instead.
  # ===========================================================================

  describe ".livro_row" do
    it "maps id / nome / nome_curto from raw JSON" do
      data = parse(File.join(json_base, "livros", "t20_eja.json"))

      expect(described_class.livro_row(data)).to eq(
        id: "t20_eja",
        nome: "Tormenta 20 - Edição Jogo do Ano",
        nome_curto: "T20 - EJA"
      )
    end

    it "produces a complete row for every livros file" do
      Dir.glob(File.join(json_base, "livros", "*.json")).each do |file|
        row = described_class.livro_row(parse(file))

        expect(row[:id]).to be_present
        expect(row[:nome]).to be_present
        expect(row[:nome_curto]).to be_present
      end
    end
  end

  describe "POCOES_TRANSFORM" do
    let(:data) { parse(File.join(json_base, "itens_magicos/pocoes", "abençoar_alimentos.json")) }

    it "keeps exactly the pocoes columns" do
      row = described_class::POCOES_TRANSFORM.call(data)

      expect(row.keys).to match_array(described_class::POCOES_ATTRS)
    end

    it "drops keys that are not columns (e.g. page)" do
      row = described_class::POCOES_TRANSFORM.call(data)

      expect(row).not_to have_key(:page)
      expect(row[:id]).to eq("abençoar_alimentos")
      expect(row[:subtipo]).to eq("oleo")
      expect(row[:pm_cost]).to eq(1)
      expect(row[:categoria]).to eq("menor")
    end
  end

  describe "ACESSORIOS_TRANSFORM" do
    it "keeps exactly the acessorios columns and the structured efeito" do
      data = parse(File.join(json_base, "itens_magicos/acessorios", "amuleto_da_robustez.json"))
      row = described_class::ACESSORIOS_TRANSFORM.call(data)

      expect(row.keys).to match_array(described_class::ACESSORIOS_ATTRS)
      expect(row).not_to have_key(:page)
      expect(row[:id]).to eq("amuleto_da_robustez")
      expect(row[:efeito]).to eq(bonus_atributo: { constituicao: 2 })
    end

    it "defaults efeito to an empty hash when the JSON omits it" do
      row = described_class::ACESSORIOS_TRANSFORM.call(id: "x", name: "X", categoria: "menor")

      expect(row[:efeito]).to eq({})
    end
  end

  describe "ENCANTAMENTOS_TRANSFORM" do
    it "coerces the boolean flags to 0/1 and defaults the JSON columns" do
      row = described_class::ENCANTAMENTOS_TRANSFORM.call(
        id: "x", name: "X", description: "desc", categoria: "arma",
        escudo_only: true, conta_como_dois: false
      )

      expect(row.keys).to match_array(described_class::ENCANTAMENTOS_ATTRS)
      expect(row[:escudo_only]).to eq(1)
      expect(row[:conta_como_dois]).to eq(0)
      expect(row[:prerequisitos]).to eq([])
      expect(row[:efeito]).to eq({})
    end

    it "preserves a real weapon enchantment" do
      data = parse(File.join(json_base, "itens_superiores/encantamentos/armas", "ameacadora.json"))
      row = described_class::ENCANTAMENTOS_TRANSFORM.call(data)

      expect(row[:id]).to eq("ameacadora")
      expect(row[:categoria]).to eq("arma")
      expect(row[:efeito]).to eq(descricao_curta: "Margem de ameaça duplica")
    end
  end

  describe "PERICIAS_TRANSFORM" do
    it "converts the three boolean flags to 1/0" do
      row = described_class::PERICIAS_TRANSFORM.call(
        id: "x", name: "X", atributo: "FOR",
        trained_only: true, armor_penalty: false, resistance_skill: true
      )

      expect(row[:trained_only]).to eq(1)
      expect(row[:armor_penalty]).to eq(0)
      expect(row[:resistance_skill]).to eq(1)
    end

    it "coerces nil flags to 0" do
      row = described_class::PERICIAS_TRANSFORM.call(id: "x", name: "X", atributo: "FOR")

      expect(row[:trained_only]).to eq(0)
      expect(row[:armor_penalty]).to eq(0)
      expect(row[:resistance_skill]).to eq(0)
    end

    it "maps the real Fortitude skill (a resistance skill)" do
      data = parse(File.join(json_base, "pericias", "fortitude.json"))
      row = described_class::PERICIAS_TRANSFORM.call(data)

      expect(row[:id]).to eq("fortitude")
      expect(row[:atributo]).to eq("CON")
      expect(row[:resistance_skill]).to eq(1)
      expect(row[:trained_only]).to eq(0)
    end
  end

  describe "REGRAS_TRANSFORM" do
    let(:data) { parse(File.join(json_base, "regras", "alcances.json")) }

    it "keeps only id/name/description at the top level" do
      row = described_class::REGRAS_TRANSFORM.call(data)

      expect(row.keys).to contain_exactly(:id, :name, :description, :data)
    end

    it "funnels the free-form keys into data" do
      row = described_class::REGRAS_TRANSFORM.call(data)

      expect(row[:data]).to include(:categorias, :regras, :page)
      expect(row[:data][:categorias].first[:id]).to eq("curto")
      expect(row[:data][:regras][:dentro_alcance]).to eq("sem penalidade")
    end

    it "does not mutate the source hash" do
      described_class::REGRAS_TRANSFORM.call(data)

      expect(data).to have_key(:categorias)
      expect(data).to have_key(:regras)
    end
  end

  describe ".habilidade_de_classe_row" do
    let(:file) do
      File.join(json_base, "poderes/habilidades_de_classe/arcanista/fluxo_de_mana.json")
    end

    it "extracts class_id from the parent directory name" do
      row = described_class.habilidade_de_classe_row(file)

      expect(row[:class_id]).to eq("arcanista")
    end

    it "tags the row as a class power" do
      row = described_class.habilidade_de_classe_row(file)

      expect(row[:type]).to eq("poder_classe")
      expect(row[:id]).to eq("fluxo_de_mana")
      expect(row[:name]).to eq("Fluxo de Mana")
    end

    it "maps requirements into prerequisites" do
      row = described_class.habilidade_de_classe_row(file)

      expect(row[:prerequisites]).to eq(
        [{ type: "character_lvl", sub_type: "hard", value: 10 }]
      )
    end

    it "derives the class_id from the directory for every class power" do
      Dir.glob(File.join(json_base, "poderes/habilidades_de_classe", "*", "*.json")).each do |path|
        expected_class = File.basename(File.dirname(path))
        row = described_class.habilidade_de_classe_row(path)

        expect(row[:class_id]).to eq(expected_class)
        expect(row[:type]).to eq("poder_classe")
      end
    end
  end

  describe ".habilidade_de_raca_row" do
    let(:file) do
      File.join(json_base, "poderes/habilidades_de_raca/silfide/asas_de_borboleta.json")
    end

    it "tags the row as a race ability" do
      row = described_class.habilidade_de_raca_row(file)

      expect(row[:type]).to eq("habilidade_de_raca")
      expect(row[:id]).to eq("asas_de_borboleta")
      expect(row[:name]).to eq("Asas de Borboleta")
    end

    it "never sets a class_id" do
      row = described_class.habilidade_de_raca_row(file)

      expect(row[:class_id]).to be_nil
    end

    it "preserves the structured effects hash" do
      row = described_class.habilidade_de_raca_row(file)

      expect(row[:effects]).to include(size: "minúsculo", hover_movement: 9)
    end

    it "tags every race ability file as habilidade_de_raca" do
      Dir.glob(File.join(json_base, "poderes/habilidades_de_raca", "**", "*.json")).each do |path|
        expect(described_class.habilidade_de_raca_row(path)[:type]).to eq("habilidade_de_raca")
      end
    end
  end

  describe ".indice_remissivo_rows" do
    let(:entries) do
      [
        { "termo" => "Abalado", "pagina" => 400, "tabela" => "condicoes", "registro_id" => "abalado" },
        { "termo" => "Abençoado", "pagina" => 82 },
        { "termo" => "Sem Pagina" },
        { "pagina" => 10 }
      ]
    end

    it "maps valid entries into rows and drops malformed ones" do
      rows = described_class.indice_remissivo_rows("t20_eja", entries)

      expect(rows.size).to eq(2)
      expect(rows.first).to eq(
        livro_id: "t20_eja", termo: "Abalado", pagina: 400,
        tabela: "condicoes", registro_id: "abalado"
      )
      expect(rows.last[:tabela]).to be_nil
      expect(rows.last[:registro_id]).to be_nil
    end

    it "coerces pagina to an integer" do
      rows = described_class.indice_remissivo_rows("t20_eja", [{ "termo" => "X", "pagina" => 42 }])

      expect(rows.first[:pagina]).to eq(42)
    end

    it "derives livro_id from the file name for every index file" do
      Dir.glob(File.join(json_base, "indice_remissivo", "*.json")).each do |file|
        livro_id = File.basename(file, ".json")
        parsed = JSON.parse(File.read(file))
        next unless parsed.is_a?(Array)

        described_class.indice_remissivo_rows(livro_id, parsed).each do |row|
          expect(row[:livro_id]).to eq(livro_id)
        end
      end
    end
  end

  describe ".import_all wiring" do
    # Every leaf importer import_all reaches directly or through the grouping
    # methods (import_equipamentos / import_itens_superiores / import_itens_magicos).
    let(:leaf_importers) do
      %i[
        import_livros import_racas import_habilidades_de_raca import_origens
        import_poderes_habilidades_unicas import_divindades import_poderes_concedidos
        import_poderes_tormenta import_poderes_gerais import_classes
        import_habilidades_de_classe import_magias
        import_armas import_armaduras import_escudos import_itens
        import_materiais_especiais import_melhorias import_encantamentos
        import_pocoes import_acessorios
        import_regras import_condicoes import_pericias import_tabelas
        import_indice_remissivo
      ]
    end

    before do
      leaf_importers.each { |m| allow(described_class).to receive(m) }
      allow(described_class).to receive(:check_no_needs_review!)
      allow(described_class).to receive(:print_summary)
    end

    it "invokes every leaf importer" do
      expect { described_class.import_all }.to output.to_stdout

      leaf_importers.each { |m| expect(described_class).to have_received(m) }
    end

    it "includes the 10 previously-missing importers" do
      expect { described_class.import_all }.to output.to_stdout

      %i[
        import_racas import_condicoes import_pericias import_tabelas import_pocoes
        import_acessorios import_encantamentos import_indice_remissivo
        import_habilidades_de_classe import_habilidades_de_raca
      ].each { |m| expect(described_class).to have_received(m) }
    end
  end

  describe ".clear_all wiring" do
    let(:models) do
      [
        Tormenta20::Models::IndiceRemissivo,
        Tormenta20::Models::Poder, Tormenta20::Models::Origem, Tormenta20::Models::Divindade,
        Tormenta20::Models::Classe, Tormenta20::Models::Magia, Tormenta20::Models::Arma,
        Tormenta20::Models::Armadura, Tormenta20::Models::Escudo, Tormenta20::Models::Item,
        Tormenta20::Models::MaterialEspecial, Tormenta20::Models::Melhoria,
        Tormenta20::Models::Encantamento, Tormenta20::Models::Pocao,
        Tormenta20::Models::AcessorioMagico, Tormenta20::Models::Regra,
        Tormenta20::Models::Condicao, Tormenta20::Models::Pericia,
        Tormenta20::Models::Tabela, Tormenta20::Models::Raca, Tormenta20::Models::Livro
      ]
    end

    it "deletes every table, including the 10 new ones" do
      models.each { |m| allow(m).to receive(:delete_all) }

      expect { described_class.clear_all }.to output.to_stdout

      models.each { |m| expect(m).to have_received(:delete_all) }
    end
  end

  describe ".print_summary" do
    let(:counter_models) do
      [
        Tormenta20::Models::Raca, Tormenta20::Models::Origem, Tormenta20::Models::Divindade,
        Tormenta20::Models::Classe, Tormenta20::Models::Magia, Tormenta20::Models::Arma,
        Tormenta20::Models::Armadura, Tormenta20::Models::Escudo, Tormenta20::Models::Item,
        Tormenta20::Models::MaterialEspecial, Tormenta20::Models::Melhoria,
        Tormenta20::Models::Encantamento, Tormenta20::Models::Pocao,
        Tormenta20::Models::AcessorioMagico, Tormenta20::Models::Regra,
        Tormenta20::Models::Condicao, Tormenta20::Models::Pericia,
        Tormenta20::Models::Tabela, Tormenta20::Models::Livro,
        Tormenta20::Models::IndiceRemissivo
      ]
    end

    before do
      counter_models.each { |m| allow(m).to receive(:count).and_return(0) }
      allow(Tormenta20::Models::Poder).to receive(:count).and_return(0)
      %i[habilidades_unicas poderes_concedidos poderes_tormenta poderes_classe by_type].each do |scope|
        allow(Tormenta20::Models::Poder).to receive(scope).and_return(double(count: 0))
      end
    end

    it "reports a count for every entity table" do
      expected = [
        /Racas: +0/, /Encantamentos: +0/, /Pocoes: +0/, /Acessorios Mag\.: +0/,
        /Condicoes: +0/, /Pericias: +0/, /Tabelas: +0/, /Livros: +0/,
        /Indice Remissivo: +0/
      ]

      expect { described_class.print_summary }.to output(Regexp.union(expected)).to_stdout
    end
  end
end
