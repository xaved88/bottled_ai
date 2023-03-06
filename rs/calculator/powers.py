from enum import Enum
from typing import List


class PowerId(Enum):
    FAKE = 'fake'  # for unknown powers

    ANGRY = 'angry'
    ARTIFACT = 'artifact'
    BUFFER = 'buffer'
    CURL_UP = 'curl up'
    DEXTERITY = 'dexterity'
    ENTANGLED = 'entangled'
    FLAME_BARRIER = 'flame barrier'
    FLIGHT = 'flight'
    FRAIL = 'frail'
    INTANGIBLE = 'intangibleplayer'
    METALLICIZE = 'metallicize'
    MINION = 'minion'
    MODE_SHIFT = 'mode_shift'
    NO_DRAW = 'no draw'
    PLATED_ARMOR = 'plated armor'
    RAGE = 'rage'
    SHARP_HIDE = 'sharp hide'
    SPLIT = 'split'
    STRENGTH = 'strength'
    THORNS = 'thorns'
    VIGOR = 'vigor'
    VULNERABLE = 'vulnerable'
    WEAKENED = 'weakened'
    THOUSAND_CUTS = 'thousand cuts'
    ACCURACY = 'accuracy'
    INFINITE_BLADES = 'infinite blades'
    AFTER_IMAGE = 'after image'


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
