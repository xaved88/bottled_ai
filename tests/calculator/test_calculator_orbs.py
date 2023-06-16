from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.enums.power_id import PowerId


class CalculatorOrbsTest(CalculatorTestFixture):

    def test_lightning_orb_triggers_on_end_turn(self):
        state = self.given_state(CardId.WOUND, orbs=[(OrbId.LIGHTNING, 1)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 3)

    def test_lightning_orb_trigger_with_focus(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.FOCUS: 3}, orbs=[(OrbId.LIGHTNING, 1)],
                                 orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 6)

    def test_frost_orb_triggers_on_end_turn(self):
        state = self.given_state(CardId.WOUND, orbs=[(OrbId.FROST, 1)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_block(play, 2)

    def test_frost_orb_triggers_with_focus(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.FOCUS: 3}, orbs=[(OrbId.FROST, 1)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_block(play, 5)

    def test_dark_orb_triggers_on_end_turn(self):
        state = self.given_state(CardId.WOUND, orbs=[(OrbId.DARK, 6)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        orb_id, amount = play.state.orbs[0]
        self.assertEqual(OrbId.DARK, orb_id)
        self.assertEqual(12, amount)

    def test_dark_orb_triggers_with_focus(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.FOCUS: 3}, orbs=[(OrbId.DARK, 6)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        orb_id, amount = play.state.orbs[0]
        self.assertEqual(OrbId.DARK, orb_id)
        self.assertEqual(15, amount)

    def test_lightning_orb_evocation(self):
        state = self.given_state(CardId.WOUND, orbs=[(OrbId.LIGHTNING, 1)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.state.evoke_orbs()
        self.see_enemy_lost_hp(play, 8)
        self.see_orb_count(play, 0)

    def test_lightning_orb_evocation_with_focus(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.FOCUS: 3}, orbs=[(OrbId.LIGHTNING, 1)],
                                 orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.state.evoke_orbs()
        self.see_enemy_lost_hp(play, 11)
        self.see_orb_count(play, 0)

    def test_frost_orb_evocation(self):
        state = self.given_state(CardId.WOUND, orbs=[(OrbId.FROST, 1)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.state.evoke_orbs()
        self.see_player_has_block(play, 5)
        self.see_orb_count(play, 0)

    def test_frost_orb_evocation_with_focus(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.FOCUS: 3}, orbs=[(OrbId.FROST, 1)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.state.evoke_orbs()
        self.see_player_has_block(play, 8)
        self.see_orb_count(play, 0)

    def test_dark_orb_evocation(self):
        state = self.given_state(CardId.WOUND, orbs=[(OrbId.DARK, 12)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.state.evoke_orbs()
        self.see_enemy_lost_hp(play, 12)
        self.see_orb_count(play, 0)

    def test_dark_orb_evocation_with_focus(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.FOCUS: 3}, orbs=[(OrbId.DARK, 12)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.state.evoke_orbs()
        self.see_enemy_lost_hp(play, 12)
        self.see_orb_count(play, 0)

    def test_plasma_orb_evocation(self):
        state = self.given_state(CardId.WOUND, orbs=[(OrbId.PLASMA, 1)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.state.evoke_orbs()
        self.see_player_spent_energy(play, -2)
        self.see_orb_count(play, 0)

    def test_channeling_lightning_orb(self):
        state = self.given_state(CardId.WOUND, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.state.channel_orb(OrbId.LIGHTNING)

        orb_id, amount = play.state.orbs[0]
        self.assertEqual(OrbId.LIGHTNING, orb_id)

    def test_channeling_darkness_orb_gives_correct_amount(self):
        state = self.given_state(CardId.WOUND, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.state.channel_orb(OrbId.DARK)

        orb_id, amount = play.state.orbs[0]
        self.assertEqual(OrbId.DARK, orb_id)
        self.assertEqual(6, amount)

    def test_channeling_darkness_orb_with_focus(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.FOCUS: 3}, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.state.channel_orb(OrbId.DARK)

        orb_id, amount = play.state.orbs[0]
        self.assertEqual(OrbId.DARK, orb_id)
        self.assertEqual(9, amount)

    def test_channeling_an_orb_evokes_when_full(self):
        state = self.given_state(CardId.WOUND, orbs=[(OrbId.FROST, 1)], orb_slots=1)
        play = self.when_playing_the_first_card(state)
        play.state.channel_orb(OrbId.DARK)
        self.see_player_has_block(play, 5)

    def test_channeling_an_orb_does_nothing_when_no_slots(self):
        state = self.given_state(CardId.ZAP, orb_slots=0)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_orb_count(play, 0)

    def test_channeling_random_orb(self):
        state = self.given_state(CardId.WOUND, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.state.channel_orb(OrbId.INTERNAL_RANDOM_ORB)

        orb_id, amount = play.state.orbs[0]
        self.assertEqual(OrbId.INTERNAL_RANDOM_ORB, orb_id)

    def test_random_orb_evocation(self):
        state = self.given_state(CardId.WOUND, orbs=[(OrbId.INTERNAL_RANDOM_ORB, 1)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.state.evoke_orbs()
        self.see_enemy_lost_hp(play, 0)
        self.see_orb_count(play, 0)
