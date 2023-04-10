from enum import Enum
from typing import List


# NOT IMPLEMENTED but probably should be
# 'constricted'
# 'duplicationpower'
# 'explosive'
# 'malleable'
# there are many others that aren't listed


class PowerId(Enum):
    FAKE = 'fake'  # for unknown powers

    ANGRY = 'angry'
    ACCURACY = 'accuracy'
    AFTER_IMAGE = 'after image'
    ARTIFACT = 'artifact'
    BARRICADE = 'barricade'
    BUFFER = 'buffer'
    CONFUSED = 'confusion'              # Calculator takes the new costs into account
    CURL_UP = 'curl up'
    DEXTERITY = 'dexterity'
    DRAW_REDUCTION = 'draw reduction'   # We'll see what we get
    ENTANGLED = 'entangled'
    FADING = 'fading'                   # N/A
    FLAME_BARRIER = 'flame barrier'
    FLIGHT = 'flight'
    FRAIL = 'frail'
    INFINITE_BLADES = 'infinite blades'
    INTANGIBLE = 'intangibleplayer'
    METALLICIZE = 'metallicize'
    MINION = 'minion'
    MODE_SHIFT = 'mode shift'
    NO_DRAW = 'no draw'
    PEN_NIB_POWER = 'pen nib'           # Covered by Pen Nib relic counting
    POISON = 'poison'
    PLATED_ARMOR = 'plated armor'
    RAGE = 'rage'
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
