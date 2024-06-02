from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.enums.power_id import PowerId


# NOTE: X-Cost cards do not yet work properly with dupe pot / echo form...
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

    def test_x_cost_is_played_still_at_0_energy(self):
        state = self.given_state(CardId.WHIRLWIND)
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_has_energy(play, 0)
        self.see_cards_played(play, 1)

    def test_malaise(self):
        state = self.given_state(CardId.MALAISE)
        state.player.energy = 2
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 2)
        self.see_enemy_has_power(play, PowerId.STRENGTH, -2)
        self.see_player_has_energy(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_upgraded_malaise(self):
        state = self.given_state(CardId.MALAISE, upgrade=1)
        state.player.energy = 2
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 3)
        self.see_enemy_has_power(play, PowerId.STRENGTH, -3)
        self.see_player_has_energy(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_skewer(self):
        state = self.given_state(CardId.SKEWER)
        state.player.energy = 2
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 14)
        self.see_player_has_energy(play, 0)
        self.see_player_discard_pile_count(play, 1)

    def test_upgraded_skewer(self):
        state = self.given_state(CardId.SKEWER, upgrade=1)
        state.player.energy = 2
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 20)
        self.see_player_has_energy(play, 0)
        self.see_player_discard_pile_count(play, 1)

    def test_multicast(self):
        state = self.given_state(CardId.MULTI_CAST, orbs=[(OrbId.LIGHTNING, 1)], orb_slots=3)
        state.player.energy = 2
        play = self.when_playing_the_first_card(state)
        self.see_orb_count(play, 0)
        self.see_enemy_lost_hp(play, 16)
        self.see_player_has_energy(play, 0)
        self.see_player_discard_pile_count(play, 1)

    def test_upgraded_multicast(self):
        state = self.given_state(CardId.MULTI_CAST, upgrade=1, orbs=[(OrbId.LIGHTNING, 1)], orb_slots=3)
        state.player.energy = 2
        play = self.when_playing_the_first_card(state)
        self.see_orb_count(play, 0)
        self.see_enemy_lost_hp(play, 24)
        self.see_player_has_energy(play, 0)
        self.see_player_discard_pile_count(play, 1)

    def test_upgraded_multicast_no_energy(self):
        state = self.given_state(CardId.MULTI_CAST, upgrade=1, orbs=[(OrbId.LIGHTNING, 1)], orb_slots=3)
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        self.see_orb_count(play, 0)
        self.see_enemy_lost_hp(play, 8)
        self.see_player_has_energy(play, 0)
        self.see_player_discard_pile_count(play, 1)

    def test_tempest(self):
        state = self.given_state(CardId.TEMPEST, orbs=[], orb_slots=3)
        state.player.energy = 2
        play = self.when_playing_the_first_card(state)
        self.see_orb_count(play, 2)
        self.see_player_has_energy(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_upgraded_tempest(self):
        state = self.given_state(CardId.TEMPEST, upgrade=1, orbs=[], orb_slots=3)
        state.player.energy = 2
        play = self.when_playing_the_first_card(state)
        self.see_orb_count(play, 3)
        self.see_player_has_energy(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_tempest_with_more_energy_than_orb_slots(self):
        state = self.given_state(CardId.TEMPEST, orbs=[], orb_slots=3)
        state.player.energy = 4
        play = self.when_playing_the_first_card(state)
        self.see_orb_count(play, 3)
        self.see_enemy_lost_hp(play, 8)
        self.see_player_has_energy(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_reinforced_body_2_energy(self):
        state = self.given_state(CardId.REINFORCED_BODY)
        state.player.energy = 2
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 14)
        self.see_player_has_energy(play, 0)
        self.see_player_discard_pile_count(play, 1)

    def test_reinforced_body_no_energy(self):
        state = self.given_state(CardId.REINFORCED_BODY)
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 0)
        self.see_player_has_energy(play, 0)
        self.see_player_discard_pile_count(play, 1)

    def test_upgraded_reinforced_body(self):
        state = self.given_state(CardId.REINFORCED_BODY, upgrade=1)
        state.player.energy = 2
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 18)
        self.see_player_has_energy(play, 0)
        self.see_player_discard_pile_count(play, 1)

    def test_reinforced_body_with_frail(self):
        state = self.given_state(CardId.REINFORCED_BODY, player_powers={PowerId.FRAIL: 1})
        state.player.energy = 5
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 25)
        self.see_player_has_energy(play, 0)
        self.see_player_discard_pile_count(play, 1)
