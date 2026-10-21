# frozen_string_literal: true

require_relative "../spec_helper"
require_relative "../../../db/seeds_helpers"

RSpec.describe Tormenta20::Seeds do
  describe ".build_item_effects" do
    it "reads the structured effect from `efeito` when `effects` is absent" do
      data = { id: "batata_valkariana", efeito: { bonus: "+1d6", duracao: "até o fim do dia" } }

      expect(described_class.build_item_effects(data)).to eq(
        bonus: "+1d6", duracao: "até o fim do dia"
      )
    end

    it "prefers `effects` over `efeito` when both are present" do
      data = { effects: { source: "effects" }, efeito: { source: "efeito" } }

      expect(described_class.build_item_effects(data)).to eq(source: "effects")
    end

    it "merges animal partner blocks alongside the item effect" do
      data = {
        efeito: { bonus: 1 },
        parceiro: { tipo: ["montaria"] },
        besta_de_carga: true,
        alternativo: { foo: "bar" },
        restricoes: [{ cd: 20 }]
      }

      expect(described_class.build_item_effects(data)).to eq(
        bonus: 1,
        parceiro: { tipo: ["montaria"] },
        besta_de_carga: true,
        alternativo: { foo: "bar" },
        restricoes: [{ cd: 20 }]
      )
    end

    it "sets the cavalgar-combate exemption flag" do
      data = { isento_restricao_cavalgar_combate: true }

      expect(described_class.build_item_effects(data)).to eq(isento_restricao_cavalgar_combate: true)
    end

    it "ignores a nil partner block" do
      data = { parceiro: nil, besta_de_carga: nil }

      expect(described_class.build_item_effects(data)).to eq({})
    end

    it "returns an empty hash when there is no efeito, effects, or partner block" do
      data = { id: "traje_de_viajante", name: "Traje de Viajante", efeito: nil }

      expect(described_class.build_item_effects(data)).to eq({})
    end

    it "handles string-keyed JSON (the bin/build_db path)" do
      data = { "efeito" => { "bonus" => "+2" }, "parceiro" => { "tipo" => ["montaria"] } }

      expect(described_class.build_item_effects(data)).to eq(
        bonus: "+2", parceiro: { "tipo" => ["montaria"] }
      )
    end

    it "does not mutate the input hash" do
      data = { efeito: { bonus: 1 }, parceiro: { tipo: ["montaria"] } }

      described_class.build_item_effects(data)

      expect(data).to eq(efeito: { bonus: 1 }, parceiro: { tipo: ["montaria"] })
    end

    it "extracts the effect from a real item JSON file" do
      path = File.expand_path(
        "../../../src/json/equipamentos/itens/alimentacao/batata_valkariana.json",
        __dir__
      )
      data = JSON.parse(File.read(path), symbolize_names: true)

      expect(described_class.build_item_effects(data)).to include(
        bonus: "+1d6", aplicacao: "um teste a sua escolha"
      )
    end
  end
end
