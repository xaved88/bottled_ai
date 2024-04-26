from enum import Enum, auto


class MemoryItem(Enum):
    ATTACKS_THIS_TURN = auto()
    LAST_KNOWN_TURN = auto()
    CLAWS_THIS_BATTLE = auto()
    CARDS_THIS_TURN = auto()


class ResetSchedule(Enum):
    GAME = auto()
    BATTLE = auto()
    TURN = auto()
