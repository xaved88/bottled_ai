from rs.calculator.cards import CardId
from rs.calculator.synergies.synergy_calculator import getSynergy

import unittest

from rs.helper.seed import get_seed_string, make_seed_string_number


class SynergyTester(unittest.TestCase):
    def test_inflame_synergy(self):
        card = CardId.INFLAME
        deck = [CardId.STRIKE_R,
                CardId.STRIKE_R,
                CardId.STRIKE_R,
                CardId.STRIKE_R,
                CardId.STRIKE_R,
                CardId.DEFEND_R,
                CardId.DEFEND_R,
                CardId.DEFEND_R,
                CardId.DEFEND_R,
                CardId.BASH,
                CardId.HEAVY_BLADE,
                CardId.INFLAME]
        result = getSynergy(card, deck)
        print(result)




