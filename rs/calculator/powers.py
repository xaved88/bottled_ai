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
    NO_DRAW = 'no draw'
    PLATED_ARMOR = 'plated armor'
    RAGE = 'rage'
    SHARP_HIDE = 'sharp hide'
    STRENGTH = 'strength'
    THORNS = 'thorns'
    VIGOR = 'vigor'
    VULNERABLE = 'vulnerable'
    WEAKENED = 'weakened'


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
