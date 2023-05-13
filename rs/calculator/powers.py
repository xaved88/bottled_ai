from enum import Enum
from typing import List


# NOT IMPLEMENTED but probably should be
# 'duplicationpower'
# 'explosive'
# there are many others that aren't listed


class PowerId(Enum):
    FAKE = 'fake'  # for unknown powers

    ANGER_NOB = 'anger'                 # Non-standard naming to distinguish it from Angry
    ANGRY = 'angry'
    ACCURACY = 'accuracy'
    AFTER_IMAGE = 'after image'
    ARTIFACT = 'artifact'
    BARRICADE = 'barricade'
    BUFFER = 'buffer'
    CHOKED = 'choked'
    CONFUSED = 'confusion'              # Bot takes the new costs into account
    CONSTRICTED = 'constricted'
    CURL_UP = 'curl up'
    DEXTERITY = 'dexterity'
    DRAW_CARD = 'draw card'     # It affects a future turn though, so we mostly don't do anything with it.
    DRAW_REDUCTION = 'draw reduction'   # It affects a future turn though, so we mostly don't do anything with it.
    ENERGIZED = 'energized'           # It affects a future turn though, so we mostly don't do anything with it.
    ENTANGLED = 'entangled'
    FADING = 'fading'                   # N/A
    FLAME_BARRIER = 'flame barrier'
    FLIGHT = 'flight'
    FRAIL = 'frail'
    INFINITE_BLADES = 'infinite blades'
    INTANGIBLE_PLAYER = 'intangibleplayer'
    INTANGIBLE_ENEMY = 'intangible'
    MALLEABLE = 'malleable'
    METALLICIZE = 'metallicize'
    MINION = 'minion'
    MODE_SHIFT = 'mode shift'
    NEXT_TURN_BLOCK = 'next turn block' # It affects a future turn though, so we mostly don't do anything with it.
    NO_DRAW = 'no draw'
    PEN_NIB_POWER = 'pen nib'           # Covered by Pen Nib relic counting
    POISON = 'poison'
    PLATED_ARMOR = 'plated armor'
    RAGE = 'rage'
    SHACKLED = 'shackled'               # Enemy regains strength at end of turn, not currently relevant
    SHARP_HIDE = 'sharp hide'
    SHIFTING = 'shifting'
    SPLIT = 'split'
    STRENGTH = 'strength'
    TOOLS_OF_THE_TRADE = 'tools of the trade'
    THIEVERY = 'thievery'               # N/A
    THORNS = 'thorns'
    TIME_WARP = 'time warp'
    VIGOR = 'vigor'
    VULNERABLE = 'vulnerable'
    WEAKENED = 'weakened'
    THOUSAND_CUTS = 'thousand cuts'


Powers = dict[PowerId: int]

DEBUFFS: List[PowerId] = [
    PowerId.CHOKED,
    PowerId.CONFUSED,
    PowerId.CONSTRICTED,
    PowerId.DRAW_REDUCTION,
    PowerId.FRAIL,
    PowerId.ENTANGLED,
    PowerId.VULNERABLE,
    PowerId.WEAKENED,
    PowerId.NO_DRAW,
]

DEBUFFS_WHEN_NEGATIVE: List[PowerId] = [
    PowerId.STRENGTH,
    PowerId.DEXTERITY,
]


def get_power_count(powers: Powers, desired_powers: List[PowerId]) -> int:
    return sum(powers[p] for p in powers.keys() if p in desired_powers)
