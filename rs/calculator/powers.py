from enum import Enum


class PowerId(Enum):
    VULNERABLE = 'vulnerable'
    WEAK = 'vulnerable'


Powers = dict[PowerId: int]
