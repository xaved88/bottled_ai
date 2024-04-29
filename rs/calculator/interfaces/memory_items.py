from enum import Enum, auto


class MemoryItem(Enum):
    ATTACKS_THIS_TURN = auto()
    CARDS_THIS_TURN = auto()
    CLAWS_THIS_BATTLE = auto()
    FROST_THIS_BATTLE = auto()
    LAST_KNOWN_TURN = auto()
    NECRONOMICON_READY = auto()
    LIGHTNING_THIS_BATTLE = auto()
    TYPE_LAST_PLAYED = auto()
    ORANGE_PELLETS_ATTACK = auto()
    ORANGE_PELLETS_SKILL = auto()
    ORANGE_PELLETS_POWER = auto()
    STANCE = auto()


class ResetSchedule(Enum):
    GAME = auto()
    BATTLE = auto()
    TURN = auto()


class StanceType(Enum):
    NO_STANCE = auto()
    CALM = auto()
    WRATH = auto()
    DIVINITY = auto()

