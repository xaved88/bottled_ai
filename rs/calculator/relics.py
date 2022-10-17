from enum import Enum


class RelicId(Enum):
    FAKE = 'fake'  # We make anything we don't know into this "fake" type

    CHAMPION_BELT = 'champion belt'
    FOSSILIZED_HELIX = 'fossilized helix'
    LETTER_OPENER = 'letter opener'
    NUNCHAKU = 'nunchaku'
    PAPER_PHROG = 'paper phrog'
    ODD_MUSHROOM = 'odd mushroom'
    ORICHALCUM = 'orichalcum'
    ORNAMENTAL_FAN = 'ornamental fan'
    PEN_NIB = 'pen nib'
    STRIKE_DUMMY = 'strike dummy'
    THE_BOOT = 'the boot'
    TORII = 'torii'
    TUNGSTEN_ROD = 'tungsten rod'
    VELVET_CHOKER = 'velvet choker'


Relics = dict[RelicId: int]
