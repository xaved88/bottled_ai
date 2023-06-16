from enum import Enum


class OrbId(Enum):
    LIGHTNING = "Lightning"
    FROST = "Frost"
    DARK = "Dark"
    PLASMA = "Plasma"
    INTERNAL_RANDOM_ORB = "Random"  # internal use only, used to represent getting random orbs from the Chaos card
