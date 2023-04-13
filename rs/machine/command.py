from enum import Enum


class Command(Enum):
    CANCEL = "cancel"
    CHOOSE = "choose"
    CONFIRM = "confirm"
    END = "end"
    LEAVE = "leave"
    PLAY = "play"
    POTION = "potion"
    PROCEED = "proceed"
    SKIP = "skip"
    WAIT = "wait"
