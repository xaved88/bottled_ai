from typing import List

from rs.calculator.cards import Card
from rs.calculator.relics import Relics
from rs.calculator.targets import Player, Monster

"""
This class only exists so that we can reference HandState elsewhere and avoid circular dependencies.
It should be kept to have the same var members as HandState, and essentially function as an interface for it.
"""


class HandStateInterface:
    player: Player
    hand: List[Card]
    discard_pile: List[Card]
    exhaust_pile: List[Card]
    draw_pile: List[Card]
    monsters: List[Monster]
    relics: Relics
