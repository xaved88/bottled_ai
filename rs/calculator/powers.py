from typing import List

from rs.calculator.enums.power_id import PowerId
from rs.calculator.interfaces.powers import Powers

DEBUFFS: List[PowerId] = [
    PowerId.BIAS,
    PowerId.BLOCK_RETURN,
    PowerId.CHOKED,
    PowerId.CONFUSED,
    PowerId.CONSTRICTED,
    PowerId.DRAW_REDUCTION,
    PowerId.ENTANGLED,
    PowerId.FASTING,
    PowerId.FRAIL,
    PowerId.LOCK_ON,
    PowerId.MARK,
    PowerId.NO_DRAW,
    PowerId.POISON,
    PowerId.VULNERABLE,
    PowerId.WEAKENED,
    PowerId.WRAITH_FORM_POWER,
]

DEBUFFS_WHEN_NEGATIVE: List[PowerId] = [
    PowerId.STRENGTH,
    PowerId.DEXTERITY,
    PowerId.FOCUS,
]


def get_power_count(powers: Powers, desired_powers: List[PowerId]) -> int:
    return sum(powers[p] for p in powers.keys() if p in desired_powers)
