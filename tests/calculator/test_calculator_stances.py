from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.cards import get_card
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.interfaces.memory_items import StanceType, MemoryItem


class CalculatorStancesTest(CalculatorTestFixture):

    def test_start_battle_in_no_stance_if_teardrop_locket(self):
        state = self.given_state(CardId.STRIKE_R)
        state.add_memory_value(MemoryItem.CARDS_THIS_TURN, 0)
        state.add_memory_value(MemoryItem.LAST_KNOWN_TURN, 1)
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.NO_STANCE)

    def test_start_battle_in_calm_if_teardrop_locket(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.TEARDROP_LOCKET: 1})
        state.add_memory_value(MemoryItem.CARDS_THIS_TURN, 0)
        state.add_memory_value(MemoryItem.LAST_KNOWN_TURN, 1)
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.CALM)

    def test_crescendo(self):
        state = self.given_state(CardId.CRESCENDO)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)
        self.see_stance(play, StanceType.WRATH)

    def test_crescendo_retains(self):
        state = self.given_state(CardId.CRESCENDO)
        state.hand.append(get_card(CardId.WOUND))
        state.player.energy = 0
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_hand_count(play, 1)
        self.assertEqual(CardId.CRESCENDO, play.state.hand[0].id)

    def test_tranquility(self):
        state = self.given_state(CardId.TRANQUILITY, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_exhaust_count(play, 1)
        self.see_stance(play, StanceType.CALM)

    def test_exit_calm_gives_energy(self):
        state = self.given_state(CardId.CRESCENDO, upgrade=1)
        state.add_memory_value(MemoryItem.STANCE, StanceType.CALM)
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.WRATH)
        self.see_player_has_energy(play, 7)

    def test_exit_calm_gives_more_energy_with_violet_lotus(self):
        state = self.given_state(CardId.CRESCENDO, upgrade=1, relics={RelicId.VIOLET_LOTUS: 1})
        state.add_memory_value(MemoryItem.STANCE, StanceType.CALM)
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.WRATH)
        self.see_player_has_energy(play, 8)

    def test_like_water_blocks_when_in_calm(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.LIKE_WATER: 3})
        state.add_memory_value(MemoryItem.STANCE, StanceType.CALM)
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_stance(play, StanceType.CALM)
        self.see_player_has_block(play, 3)

    def test_like_water_does_not_block_outside_calm(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.LIKE_WATER: 2})
        state.add_memory_value(MemoryItem.STANCE, StanceType.WRATH)
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_stance(play, StanceType.WRATH)
        self.see_player_has_block(play, 0)

    def test_wrath_doubles_damage_dealt(self):
        state = self.given_state(CardId.STRIKE_R)
        state.add_memory_value(MemoryItem.STANCE, StanceType.WRATH)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)

    def test_wrath_doubles_damage_taken(self):
        state = self.given_state(CardId.WOUND)
        state.add_memory_value(MemoryItem.STANCE, StanceType.WRATH)
        state.monsters[0].damage = 10
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 20)

    def test_vigilance(self):
        state = self.given_state(CardId.VIGILANCE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_has_block(play, 8)
        self.see_player_discard_pile_count(play, 1)
        self.see_stance(play, StanceType.CALM)

    def test_eruption(self):
        state = self.given_state(CardId.ERUPTION)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_lost_hp(play, 9)
        self.see_player_discard_pile_count(play, 1)
        self.see_stance(play, StanceType.WRATH)

    def test_prostrate(self):
        state = self.given_state(CardId.PROSTRATE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_has_block(play, 4)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_has_power(play, PowerId.MANTRA, 2)

    def test_enter_divinity(self):
        state = self.given_state(CardId.PROSTRATE, player_powers={PowerId.MANTRA: 9})
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.DIVINITY)
        self.see_player_has_energy(play, 8)
        self.see_player_has_power(play, PowerId.MANTRA, 1)

    def test_divinity_triples_damage_dealt(self):
        state = self.given_state(CardId.STRIKE_R)
        state.add_memory_value(MemoryItem.STANCE, StanceType.DIVINITY)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 18)

    def test_enter_divinity_and_exit_calm(self):
        state = self.given_state(CardId.PROSTRATE, player_powers={PowerId.MANTRA: 9})
        state.add_memory_value(MemoryItem.STANCE, StanceType.CALM)
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.DIVINITY)
        self.see_player_has_energy(play, 10)
        self.see_player_has_power(play, PowerId.MANTRA, 1)

    def test_empty_body(self):
        state = self.given_state(CardId.EMPTY_BODY)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 7)
        self.see_player_discard_pile_count(play, 1)
        self.see_stance(play, StanceType.NO_STANCE)

    def test_empty_fist(self):
        state = self.given_state(CardId.EMPTY_FIST)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 9)
        self.see_player_discard_pile_count(play, 1)
        self.see_stance(play, StanceType.NO_STANCE)

    def test_empty_mind(self):
        state = self.given_state(CardId.EMPTY_MIND)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 2)
        self.see_player_discard_pile_count(play, 1)
        self.see_stance(play, StanceType.NO_STANCE)
