from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.cards import get_card
from rs.calculator.enums.card_id import CardId


class CalculatorOtherTest(CalculatorTestFixture):

    def test_ritual_dagger_level_up_is_in_hash_state(self):
        state = self.given_state(CardId.RITUAL_DAGGER)
        state.hand.append(get_card(CardId.STRIKE_R))
        state.monsters[0].current_hp = 20  # enough that it needs both cards to kill
        paths = self.when_getting_all_paths(state)
        # We expect 5 paths: [], [S], [RD], [S,RD], [RD,S]
        # Normally the order of attacks wouldn't matter, but ritual dagger gains value on the kill, so we expect
        # this to be another path to consider in the hash state, because of the memory by card.
        self.assertEqual(5, len(paths))
