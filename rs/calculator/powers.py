from enum import Enum
from typing import List


class PowerId(Enum):
    ARTIFACT = 'artifact'
    CURL_UP = 'curl_up'
    DEXTERITY = 'dexterity'
    ENTANGLED = 'entangled'
    FRAIL = 'frail'
    PLATED_ARMOR = 'plated armor'
    STRENGTH = 'strength'
    VIGOR = 'vigor'
    VULNERABLE = 'vulnerable'
    WEAK = 'weak'


Powers = dict[PowerId: int]

DEBUFFS: List[PowerId] = [
    PowerId.FRAIL,
    PowerId.VULNERABLE,
    PowerId.WEAK,
]
