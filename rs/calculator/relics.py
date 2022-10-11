from enum import Enum


class RelicId(Enum):
    FAKE = 'fake'  # We make anything we don't know into this "fake" type
    NUNCHAKU = 'nunchaku'
    PAPER_PHROG = 'paper phrog'
    PEN_NIB = 'pen nib'
    STRIKE_DUMMY = 'strike dummy'
    VELVET_CHOKER = 'velvet choker'


Relics = dict[RelicId: int]
