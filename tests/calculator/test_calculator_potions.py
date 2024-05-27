from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.potion_id import PotionId
from rs.calculator.enums.relic_id import RelicId


class CalculatorPotionsTest(CalculatorTestFixture):

    def test_fairy_in_a_bottle_heals_when_hitting_0(self):
        state = self.given_state(CardId.WOUND, potions=[PotionId.FAIRY_IN_A_BOTTLE])
        state.monsters[0].hits = 2
        state.monsters[0].damage = 10
        state.player.current_hp = 5
        state.player.max_hp = 166.667
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_potion_count(play, 0)
        self.see_player_lost_hp(play, 10)
