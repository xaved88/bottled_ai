from calculator.test_calculator_fixture import CalculatorTestFixture
from rs.calculator.cards import CardId, get_card
from rs.calculator.play_path import PlayPath
from rs.calculator.powers import PowerId
from rs.calculator.relics import RelicId


class CalculatorCardsTest(CalculatorTestFixture):

    def test_strike_dummy(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.STRIKE_DUMMY] = 1
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 9)

    def test_velvet_choker(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.STRIKE_R))
        state.hand.append(get_card(CardId.STRIKE_R))
        state.relics[RelicId.VELVET_CHOKER] = 4
        play = self.when_calculating_state_play(state)
        # see that only 2 of the 3 strikes are played because choker stops it
        self.see_enemy_lost_hp(play, 12)

    def test_paper_phrog(self):
        state = self.given_state(CardId.STRIKE_R)
        state.targets[0].powers[PowerId.VULNERABLE] = 1
        state.relics[RelicId.PAPER_PHROG] = 1
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 10)

    def test_nunchaku_increments_with_attack(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.NUNCHAKU] = 3
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 1)
        self.see_relic_value(play, RelicId.NUNCHAKU, 4)

    def test_nunchaku_does_not_increment_with_skill(self):
        state = self.given_state(CardId.DEFEND_R)
        state.relics[RelicId.NUNCHAKU] = 3
        play = self.when_calculating_state_play(state)
        self.see_player_spent_energy(play, 1)
        self.see_relic_value(play, RelicId.NUNCHAKU, 3)

    def test_nunchaku_gives_energy(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.NUNCHAKU] = 9
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 0)
        self.see_relic_value(play, RelicId.NUNCHAKU, 0)

    def test_nunchaku_cant_play_when_lacking_energy_but_would_receive_it(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.NUNCHAKU] = 9
        state.player.energy = 0
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_relic_value(play, RelicId.NUNCHAKU, 9)

    def test_pen_nib_increments_with_attack(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.PEN_NIB] = 3
        play = self.when_calculating_state_play(state)
        self.see_relic_value(play, RelicId.PEN_NIB, 4)

    def test_pen_nib_does_not_increment_with_skill(self):
        state = self.given_state(CardId.DEFEND_R)
        state.relics[RelicId.PEN_NIB] = 3
        play = self.when_calculating_state_play(state)
        self.see_relic_value(play, RelicId.PEN_NIB, 3)

    def test_pen_nib_effect(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        state.relics[RelicId.PEN_NIB] = 9
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 20)
        self.see_player_spent_energy(play, 1)
        self.see_relic_value(play, RelicId.PEN_NIB, 0)

    # HELPER METHODS
    def see_relic_value(self, play: PlayPath, relic_id: RelicId, value: int):
        self.assertEqual(value, play.state.relics.get(relic_id))
