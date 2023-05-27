from typing import List, Callable

from rs.calculator.cards import Card
from rs.calculator.powers import Powers
from rs.calculator.relics import Relics
from rs.calculator.targets import Player, Monster

"""
These classes only exists so that we can reference BattleState and CardEffects elsewhere and avoid circular dependencies.
It should be kept to have the same var members as BattleState/CardEffects, and essentially function as an interface for it.
"""


class BattleStateInterface:
    player: Player
    hand: List[Card]
    discard_pile: List[Card]
    exhaust_pile: List[Card]
    draw_pile: List[Card]
    monsters: List[Monster]
    relics: Relics
    cards_discarded_this_turn: int
    # functions
    draw_cards: Callable[[int], None]
    add_cards_to_hand: Callable[[Card, int], None]
    discard_card: Callable[[Card], None]
    inflict_random_target_damage: Callable[[int, int, bool, float, bool, int], None]
    add_random_poison: Callable[[int, int], None]


class CardEffectsInterface:
    damage: int
    hits: int
    blockable: bool
    block: int
    applies_powers: Powers
    energy_gain: int
    draw: int
