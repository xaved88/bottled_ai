CARD_REMOVAL_PRIORITY_LIST = ['strike', 'strike+', 'defend', 'defend+']

DESIRED_CARDS_FOR_DECK: dict[str, int] = {
    'perfected strike': 1337,
    'twin strike': 5,
    'wild strike': 2,
}

HIGH_PRIORITY_UPGRADES = [
    'Apotheosis',
    'Fission',
    'Defragment',
    'Biased Cognition',
]

DESIRED_POTIONS = [
    'fruit juice',
    'fairy in a bottle',
    'focus potion',
    'cultist potion',
    # 'power potion',  # we don't currently pick cards from potions with pwnder
    'potion of capacity',
    'duplication potion',
    'blessing of the forge',
    # 'attack potion',  # we don't currently pick cards from potions with pwnder
    'dexterity potion',
    'ambrosia',
    'fear potion',
    'essence of steel',
    'strength potion',
    'regen potion',
    'entropic brew',
    'liquid bronze',
    'energy potion',
    # 'skill potion',  # we don't currently pick cards from potions with pwnder
    'ancient potion',
    'weak potion',
    'gambler\u0027s brew',
    'poison potion',
    # 'colorless potion',   # we don't currently pick cards from potions with pwnder
    'flex potion',
    'swift potion',
    'essence of darkness',
    'fire potion',
    'explosive potion',
    'speed potion',
    'block potion',
    'cunning potion',
    'smoke bomb',
    'elixir potion',
    'distilled chaos',  # We don't want to accidentally play Biased Cog way too early
    'liquid memories',
    'snecko oil',
]