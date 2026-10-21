# frozen_string_literal: true

# Shared helpers for the two seeders (bin/build_db and db/seeds.rb).
#
# This file is intentionally dependency-free so it can be loaded by both the
# raw-SQL seeder (bin/build_db) and the ActiveRecord seeder (db/seeds.rb).
module Tormenta20
  # Import helpers shared by the JSON seeders (bin/build_db, db/seeds.rb).
  module Seeds
    # Top-level item JSON keys that represent animal partner blocks. They are
    # not columns of the `itens` table, so they must be folded into the
    # `effects` payload to become queryable in the DB.
    ITEM_EFFECT_PARTNER_KEYS = %w[parceiro besta_de_carga alternativo restricoes].freeze

    # Build the `effects` payload for a single item row.
    #
    # Item JSON files under `src/json/equipamentos/itens/**` keep their
    # structured effect under the top-level `efeito` key (85 of the current
    # files); `effects` is supported as an alternative/preferred source. The
    # animal partner blocks (`parceiro`, `besta_de_carga`, `alternativo`,
    # `restricoes`) and the `isento_restricao_cavalgar_combate` flag are merged
    # into the same payload.
    #
    # Accepts either string-keyed (bin/build_db) or symbol-keyed (db/seeds.rb)
    # hashes; the returned hash is keyed with symbols at the top level (nested
    # values keep the key type they came in with).
    #
    # @param data [Hash] raw item JSON (string- or symbol-keyed)
    # @return [Hash{Symbol => Object}] effects payload (empty hash when the item
    #   carries no effect and no partner block)
    def self.build_item_effects(data)
      source = fetch_item_key(data, "effects")
      source = fetch_item_key(data, "efeito") unless source.is_a?(Hash)
      effects = source.is_a?(Hash) ? source.transform_keys(&:to_sym) : {}

      ITEM_EFFECT_PARTNER_KEYS.each do |key|
        value = fetch_item_key(data, key)
        effects[key.to_sym] = value unless value.nil?
      end

      effects[:isento_restricao_cavalgar_combate] = true if fetch_item_key(data, "isento_restricao_cavalgar_combate")

      effects
    end

    # Fetch a top-level key from an item hash regardless of key type.
    #
    # @param data [Hash]
    # @param key [String]
    # @return [Object, nil]
    def self.fetch_item_key(data, key)
      return data[key.to_sym] if data.key?(key.to_sym)

      data[key]
    end
  end
end
