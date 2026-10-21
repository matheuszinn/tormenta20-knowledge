# frozen_string_literal: true

require_relative "../spec_helper"

RSpec.describe "Database schema" do
  let(:connection) { Tormenta20::Models::Base.connection }

  # Returns the list of [column, referenced_table] pairs for a table's FKs.
  def foreign_keys_for(table)
    connection.foreign_keys(table).map do |fk|
      [fk.options[:column], fk.to_table]
    end
  end

  describe "foreign keys" do
    it "constrains racas.livro_id to livros.id" do
      expect(foreign_keys_for("racas")).to include(%w[livro_id livros])
    end

    it "constrains indice_remissivo.livro_id to livros.id" do
      expect(foreign_keys_for("indice_remissivo")).to include(%w[livro_id livros])
    end
  end

  describe "foreign key enforcement" do
    before do
      connection.execute("PRAGMA foreign_keys = ON")
    end

    it "rejects a raca referencing a non-existent livro" do
      expect do
        connection.execute(
          "INSERT INTO racas (id, name, livro_id) VALUES ('teste_fk', 'Teste', 'id_que_nao_existe_em_livros')"
        )
      end.to raise_error(ActiveRecord::StatementInvalid, /FOREIGN KEY constraint failed/)
    end

    after do
      connection.execute("DELETE FROM racas WHERE id = 'teste_fk'")
    end
  end
end
