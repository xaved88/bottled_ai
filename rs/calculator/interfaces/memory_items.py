from enum import Enum, auto


class MemoryItem(Enum):
    ATTACKS_THIS_TURN = auto()
    CARDS_THIS_TURN = auto()
    CLAWS_THIS_BATTLE = auto()
    FROST_THIS_BATTLE = auto()
    LAST_KNOWN_TURN = auto()
    NECRONOMICON_READY = auto()
    LIGHTNING_THIS_BATTLE = auto()


class ResetSchedule(Enum):
    GAME = auto()
    BATTLE = auto()
    TURN = auto()
