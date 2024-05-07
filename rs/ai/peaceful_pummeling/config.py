CARD_REMOVAL_PRIORITY_LIST = ['strike', 'strike+', 'defend', 'defend+']

DESIRED_CARDS_FOR_DECK: dict[str, int] = {
    'tranquility': 3,
    'crescendo': 3,
    'collect': 1,
    'brilliance': 1,
    'pressure points': 1,
    'like water': 2,
    'carve reality': 1,
    'wallop': 1,
    'windmill strike': 1,
    'battle hymn': 1,
    'reach heaven': 1,
    'deva form': 1,
    'signature move': 1,
    'talk to the hand': 1,
    'swivel': 1,
    'spirit shield': 1,
    'flying sleeves': 1,
    'sands of time': 1,
    'rushdown': 1,
    'tantrum': 2,
    'fasting': 1,
    'wave of the hand': 1,
    'perseverance': 1,
    'wheel kick': 1,
    'wreath of flame': 1,
    'crush joints': 1,
    'sash whip': 1,
    'follow-up': 1,
    'deceive reality': 1,
    'master reality': 1,
    'empty body': 1,
    'empty fist': 2,
    'empty mind': 1,
    'indignation': 1,
    'mental fortress': 2,
    'fear no evil': 2,
    'halt': 2,
    'inner peace': 2,
    'flurry of blows': 2,
    'prostrate': 2,
    'worship': 2,
    'pray': 1,
}

DESIRED_CARDS_FROM_POTIONS: dict[str, int] = {
    'apotheosis': 1,
}

HIGH_PRIORITY_UPGRADES = [
    'Apotheosis',
]