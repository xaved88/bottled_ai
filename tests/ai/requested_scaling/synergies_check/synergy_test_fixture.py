import unittest

from rs.calculator.cards import CardId, get_card
from rs.calculator.hand_state import HandState
from rs.calculator.relics import Relics
from rs.calculator.targets import Player, Monster


class SynergyCalculatorTestFixture(unittest.TestCase):
    def given_state(self, card_id: CardId, upgrade: int = 0, targets: int = 1, player_powers=None,
                    relics: Relics = None) -> HandState:
        return HandState(
            player=Player(50, 100, 0, {} if player_powers is None else player_powers, 5, relics),
            hand=[get_card(card_id, None, upgrade)],
            monsters=[Monster(100, 100, 0, {}) for i in range(targets)],
            relics=relics,
        )







