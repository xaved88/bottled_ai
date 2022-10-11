from enum import Enum
from typing import List


class PowerId(Enum):
    FAKE = 'fake'  # for unknown powers

    ARTIFACT = 'artifact'
    CURL_UP = 'curl up'
    DEXTERITY = 'dexterity'
    ENTANGLED = 'entangled'
    FLAME_BARRIER = 'flame barrier'  # no handling for flame barrier yet. implement with thorns
    FRAIL = 'frail'
    PLATED_ARMOR = 'plated armor'
    STRENGTH = 'strength'
    VIGOR = 'vigor'
    VULNERABLE = 'vulnerable'
    WEAKENED = 'weakened'


Powers = dict[PowerId: int]

DEBUFFS: List[PowerId] = [
    PowerId.FRAIL,
    PowerId.ENTANGLED,
    PowerId.VULNERABLE,
    PowerId.WEAKENED,
]
