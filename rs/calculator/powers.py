from enum import Enum


class PowerId(Enum):
    VULNERABLE = 'vulnerable'
    WEAK = 'vulnerable'
    STRENGTH = 'strength'


Powers = dict[PowerId: int]
