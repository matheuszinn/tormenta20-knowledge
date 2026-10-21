# frozen_string_literal: true

require "tmpdir"

require_relative "../spec_helper"
require_relative "../../../db/seeds"

RSpec.describe Tormenta20::Seeds do
  let(:json_base) { described_class::JSON_BASE_PATH }

  # Replaces the real constant so Models::Livro.find_or_initialize_by can be
  # stubbed without ever touching the read-only database.
  let(:livro_class) { class_double("Tormenta20::Models::Livro").as_stubbed_const }
  let(:record) { double("livro") }

  def parse(path)
    JSON.parse(File.read(path), symbolize_names: true)
  end

  before do
    # Models::Base#readonly? blocks every write at runtime; neutralize it for
    # the importer, and let find_or_initialize_by hand back our record double.
    allow_any_instance_of(Tormenta20::Models::Base).to receive(:readonly?).and_return(false)
    allow(livro_class).to receive(:find_or_initialize_by).and_return(record)
    allow(record).to receive(:nome=)
    allow(record).to receive(:nome_curto=)
    allow(record).to receive(:save!)
  end

  describe ".import_livros" do
    it "imports a single livro file and persists it" do
      data = parse(File.join(json_base, "livros", "t20_eja.json"))
      expect(data).to eq(
        id: "t20_eja",
        nome: "Tormenta 20 - Edição Jogo do Ano",
        nome_curto: "T20 - EJA"
      )

      livro_file = File.join(json_base, "livros", "t20_eja.json")
      allow(Dir).to receive(:glob).with(File.join(json_base, "livros", "*.json")).and_return([livro_file])

      expect { described_class.import_livros }.to output(/Successfully imported 1 livros/).to_stdout

      expect(livro_class).to have_received(:find_or_initialize_by).with(id: "t20_eja").once
      expect(record).to have_received(:nome=).with("Tormenta 20 - Edição Jogo do Ano")
      expect(record).to have_received(:nome_curto=).with("T20 - EJA")
      expect(record).to have_received(:save!).once
    end

    it "iterates over every file in a directory of two livros" do
      Dir.mktmpdir do |dir|
        x = File.join(dir, "x.json")
        y = File.join(dir, "y.json")
        File.write(x, JSON.generate(id: "x", nome: "X", nome_curto: "X"))
        File.write(y, JSON.generate(id: "y", nome: "Y", nome_curto: "Y"))

        allow(Dir).to receive(:glob).with(File.join(json_base, "livros", "*.json")).and_return([x, y])

        expect { described_class.import_livros }.to output(/Successfully imported 2 livros/).to_stdout

        expect(livro_class).to have_received(:find_or_initialize_by).with(id: "x").ordered
        expect(livro_class).to have_received(:find_or_initialize_by).with(id: "y").ordered
        expect(record).to have_received(:save!).twice
        expect(record).to have_received(:nome=).with("X")
        expect(record).to have_received(:nome=).with("Y")
      end
    end

    it "upserts on every run (idempotent find_or_initialize_by + save!)" do
      livro_file = File.join(json_base, "livros", "t20_eja.json")
      allow(Dir).to receive(:glob).with(File.join(json_base, "livros", "*.json")).and_return([livro_file])

      expect { described_class.import_livros }.to output.to_stdout
      expect { described_class.import_livros }.to output.to_stdout

      expect(livro_class).to have_received(:find_or_initialize_by).with(id: "t20_eja").twice
      expect(record).to have_received(:save!).twice
    end

    it "returns early when the livros directory is missing" do
      allow(Dir).to receive(:exist?).and_call_original
      allow(Dir).to receive(:exist?).with(File.join(json_base, "livros")).and_return(false)

      expect { described_class.import_livros }.to output(/Directory not found/).to_stdout

      expect(livro_class).not_to have_received(:find_or_initialize_by)
      expect(record).not_to have_received(:save!)
    end
  end
end
