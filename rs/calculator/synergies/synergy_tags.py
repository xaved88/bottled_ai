# For now creating a constant for every single tag
from enum import Enum

STRENGTH_TAG = 1
DEXTERITY_TAG = 1
FOCUS_TAG = 1
POWERPLAY_TAG = 1
EXHAUST_TAG = 1


class SynergyTag(Enum):
    STRENGTH = 'STRENGTH'
    DEXTERITY = 'DEXTERITY'
    FOCUS = 'FOCUS'
    POWERPLAY = 'POWERPLAY'
    EXHAUST = 'EXHAUST'
