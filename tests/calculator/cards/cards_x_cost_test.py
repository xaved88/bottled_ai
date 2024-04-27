from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.enums.card_id import CardId


class CardsXCostTest(CalculatorTestFixture):

    def test_whirlwind(self):
        state = self.given_state(CardId.WHIRLWIND, targets=2)
        state.player.energy = 2
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 10, enemy_index=0)
        self.see_enemy_lost_hp(play, 10, enemy_index=1)
        self.see_player_has_energy(play, 0)

    def test_upgraded_whirlwind(self):
        state = self.given_state(CardId.WHIRLWIND, upgrade=1)
        state.player.energy = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 24)
        self.see_player_has_energy(play, 0)

    def test_whirlwind_is_played_still_at_0_energy(self):
        state = self.given_state(CardId.WHIRLWIND)
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_has_energy(play, 0)
        self.see_cards_played(play, 1)
