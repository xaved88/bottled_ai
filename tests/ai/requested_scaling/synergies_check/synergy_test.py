from ai.requested_scaling.synergies_check.synergy_test_fixture import SynergyCalculatorTestFixture
from rs.ai.requested_scaling.synergies.synergy_calculator import get_synergy
from rs.calculator.cards import CardId, get_card


class SynergyTester(SynergyCalculatorTestFixture):

    def test_base_deck_with_inflame(self):
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
                CardId.BASH]
        result = get_synergy(card, deck)
        #result should be 0 in this case since there is no real str scaling cards
        self.assertGreaterEqual(result, 0)

    def test_heavy_blade_with_inflame(self):
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
                CardId.HEAVY_BLADE]
        result = get_synergy(card, deck)
        #2 from Heavy Blade out of 11 cards, should be 0.2
        self.assertGreater(result, 0.1)
        self.assertGreater(0.3, result)

    def test_evolve_synergies(self):
        card = CardId.EVOLVE
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
                CardId.POWER_THROUGH]
        result = get_synergy(card, deck)
        self.assertGreater(result, 0)


    def test_shenanigans_zero_length_deck(self):
        card = CardId.EVOLVE
        deck = []
        result = get_synergy(card, deck)
        self.assertEqual(result, 0)


    def card_is_not_a_synergy_provider(self):
        card = CardId.STRIKE_R
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
                CardId.HEAVY_BLADE]
        result = get_synergy(card, deck)
        self.assertEqual(result, 0)
