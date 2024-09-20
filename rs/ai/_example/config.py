# card id. 'strike+' is an upgraded strike
CARD_REMOVAL_PRIORITY_LIST = [
    'strike',
    'strike+',
    'defend',
    'defend+']

# [card display name]: [max amount to have in deck]
DESIRED_CARDS_FOR_DECK: dict[str, int] = {
    'perfected strike': 1337,
    'twin strike': 2,
    'wild strike': 2,
}

# card display name: max amount to have in deck
DESIRED_CARDS_FROM_POTIONS: dict[str, int] = {
    'demon form': 1,
    'apotheosis': 1,
}

HIGH_PRIORITY_UPGRADES = [
    'Apotheosis',
]

DESIRED_POTIONS = [
    'fruit juice',
    'fairy in a bottle',
    'focus potion',
    'cultist potion',
    'power potion',
    'potion of capacity',
    'heart of iron',
    'duplication potion',
    'distilled chaos',
    'blessing of the forge',
    'attack potion',
    'dexterity potion',
    'ambrosia',
    'fear potion',
    'essence of steel',
    'strength potion',
    'regen potion',
    'blood potion',
    'entropic brew',
    'liquid bronze',
    'energy potion',
    'skill potion',
    'ancient potion',
    'weak potion',
    'gambler\u0027s brew',
    'poison potion',
    'colorless potion',
    'flex potion',
    'swift potion',
    'bottled miracle',
    'essence of darkness',
    'fire potion',
    'explosive potion',
    'speed potion',
    'block potion',
    'cunning potion',
    'ghost in a jar',
    'stance potion',
    'smoke bomb',
    'elixir potion',
    'liquid memories',
    'snecko oil',
    'stance potion',
]