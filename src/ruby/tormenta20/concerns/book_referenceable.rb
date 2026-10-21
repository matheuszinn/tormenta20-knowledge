# frozen_string_literal: true

module Tormenta20
  module Concerns
    # Mixin that gives any gem model access to its book/page reference.
    #
    # Methods are lazy-loaded: the database is queried on the first call
    # and the result is memoized for the lifetime of the instance.
    #
    # @example
    #   guerreiro = Tormenta20.classes.find("guerreiro")
    #   guerreiro.book_reference  # => "T20 - EJA, p. 56"
    #   guerreiro.page            # => 56
    #   guerreiro.book            # => "T20 - EJA"
    #   guerreiro.full_book       # => "Tormenta 20 - Edição Jogo do Ano"
    module BookReferenceable
      # Todas as referências do registro (uma por linha em `indice_remissivo`),
      # em ordem de `livro_id` e `pagina`. Array vazio se não houver entrada.
      #
      # @return [Array<Hash>] cada item: `{ livro:, pagina:, formatted: }`
      def book_references
        @book_references ||= Models::IndiceRemissivo
                             .includes(:livro)
                             .where(tabela: self.class.table_name, registro_id: id.to_s)
                             .order(:livro_id, :pagina)
                             .map { |e| { livro: e.livro.nome_curto, pagina: e.pagina, formatted: "#{e.livro.nome_curto}, p. #{e.pagina}" } }
      end

      # "T20 - EJA, p. 215" — primeira referência; nil se não houver entrada no
      # índice. Para a lista completa use {#book_references}.
      def book_reference
        book_references.first&.dig(:formatted)
      end

      # Número da página (Integer) — nil se não indexado.
      def page
        _indice_entry&.pagina
      end

      # Nome curto do livro (String) — nil se não indexado.
      def book
        _indice_entry&.livro&.nome_curto
      end

      # Nome completo do livro (String) — nil se não indexado.
      def full_book
        _indice_entry&.livro&.nome
      end

      private

      def _indice_entry
        # Memoize por instância; reset se o id mudar.
        return @_indice_entry if defined?(@_indice_entry)

        @_indice_entry = Models::IndiceRemissivo
                         .includes(:livro)
                         .find_by(tabela: self.class.table_name, registro_id: id.to_s)
      end
    end
  end
end
