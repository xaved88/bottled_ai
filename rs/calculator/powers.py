from enum import Enum
from typing import List


class PowerId(Enum):
    FAKE = 'fake'  # for unknown powers

    ANGRY = 'angry'
    ACCURACY = 'accuracy'
    AFTER_IMAGE = 'after image'
    ARTIFACT = 'artifact'
    BARRICADE = 'barricade'
    BUFFER = 'buffer'
    CURL_UP = 'curl up'
    DARK_EMBRACE = 'dark embrace'
    DEXTERITY = 'dexterity'
    ENTANGLED = 'entangled'
    EVOLVE = 'evolve'
    FEEL_NO_PAIN = 'feel no pain'
    FIRE_BREATHING = 'fire breathing'
    FLAME_BARRIER = 'flame barrier'
    FLIGHT = 'flight'
    FRAIL = 'frail'
    INFINITE_BLADES = 'infinite blades'
    INTANGIBLE = 'intangibleplayer'
    METALLICIZE = 'metallicize'
    MINION = 'minion'
    MODE_SHIFT = 'mode_shift'
    NO_DRAW = 'no draw'
    POISON = 'poison'
    PLATED_ARMOR = 'plated armor'
    RAGE = 'rage'
    SHARP_HIDE = 'sharp hide'
    SPLIT = 'split'
    STRENGTH = 'strength'
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
