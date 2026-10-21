# frozen_string_literal: true

require_relative "../spec_helper"

RSpec.describe Tormenta20::Concerns::BookReferenceable do
  let(:classe) { Tormenta20::Models::Classe.first }

  describe "included in all models" do
    it "is included in Classe" do
      expect(Tormenta20::Models::Classe.ancestors).to include(described_class)
    end

    it "is included in Raca" do
      expect(Tormenta20::Models::Raca.ancestors).to include(described_class)
    end

    it "is included in Magia" do
      expect(Tormenta20::Models::Magia.ancestors).to include(described_class)
    end
  end

  describe "when no index entry exists" do
    before do
      allow(Tormenta20::Models::IndiceRemissivo).to receive(:includes).and_return(
        double(where: double(order: []), find_by: nil)
      )
    end

    it "#book_reference returns nil" do
      expect(classe.book_reference).to be_nil
    end

    it "#book_references returns an empty array" do
      expect(classe.book_references).to eq([])
    end

    it "#page returns nil" do
      expect(classe.page).to be_nil
    end

    it "#book returns nil" do
      expect(classe.book).to be_nil
    end

    it "#full_book returns nil" do
      expect(classe.full_book).to be_nil
    end
  end

  describe "when an index entry exists" do
    let(:livro) do
      double("Livro", nome_curto: "T20 - EJA", nome: "Tormenta 20 - Edição Jogo do Ano")
    end

    let(:entry) do
      double("IndiceRemissivo", pagina: 56, livro: livro)
    end

    before do
      allow(Tormenta20::Models::IndiceRemissivo).to receive(:includes).and_return(
        double(where: double(order: [entry]), find_by: entry)
      )
    end

    it "#book_reference returns formatted string" do
      expect(classe.book_reference).to eq("T20 - EJA, p. 56")
    end

    it "#book_references returns every formatted entry" do
      expect(classe.book_references).to eq(
        [{ livro: "T20 - EJA", pagina: 56, formatted: "T20 - EJA, p. 56" }]
      )
    end

    it "#page returns the page number" do
      expect(classe.page).to eq(56)
    end

    it "#book returns the short book name" do
      expect(classe.book).to eq("T20 - EJA")
    end

    it "#full_book returns the full book name" do
      expect(classe.full_book).to eq("Tormenta 20 - Edição Jogo do Ano")
    end
  end

  describe "memoization" do
    it "only runs the book_references query once per instance" do
      relation = double(where: double(order: []), find_by: nil)
      allow(Tormenta20::Models::IndiceRemissivo).to receive(:includes).and_return(relation)

      # Force fresh instance without memoized value
      fresh = Tormenta20::Models::Classe.first

      fresh.book_references
      fresh.book_references
      fresh.book_reference

      expect(Tormenta20::Models::IndiceRemissivo).to have_received(:includes).once
    end
  end

  describe "with the real database" do
    it "#book_references lists every source of a multi-source entity, in order" do
      melhoria = Tormenta20::Models::Melhoria.find("espinhosa")

      expect(melhoria.book_references).to eq(
        [
          { livro: "T20 - Ameaças", pagina: 401, formatted: "T20 - Ameaças, p. 401" },
          { livro: "T20 - EJA", pagina: 171, formatted: "T20 - EJA, p. 171" }
        ]
      )
      expect(melhoria.book_reference).to eq("T20 - Ameaças, p. 401")
    end

    it "#book_references scopes by tabela when the same id exists in two tables" do
      magia = Tormenta20::Models::Magia.find("bola_de_fogo")
      pocao = Tormenta20::Models::Pocao.find("bola_de_fogo")

      expect(magia.book_references.map { |r| r[:pagina] }).to eq([188])
      expect(pocao.book_references.map { |r| r[:pagina] }).to eq([347])
    end
  end
end
