from enum import Enum, auto


class MemoryItem(Enum):
    ATTACKS_THIS_TURN = auto()
    LAST_KNOWN_TURN = auto()
    CLAWS_PLAYED_THIS_BATTLE = auto()


class ResetSchedule(Enum):
    GAME = auto()
    BATTLE = auto()
    TURN = auto()