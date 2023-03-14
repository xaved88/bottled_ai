from rs.calculator.cards import CardId
from rs.ai.requested_scaling.synergies.synergy_calculator import getSynergy

import unittest


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




