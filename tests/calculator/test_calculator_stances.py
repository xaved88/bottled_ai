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

    def test_wrath_increases_ritual_dagger_damage(self):
        state = self.given_state(CardId.RITUAL_DAGGER)
        state.add_memory_by_card(CardId.RITUAL_DAGGER, "default", 3)
        state.add_memory_value(MemoryItem.STANCE, StanceType.WRATH)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 36)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)

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
        self.see_player_has_power(play, PowerId.MANTRA_INTERNAL, 2)

    def test_enter_divinity(self):
        state = self.given_state(CardId.PROSTRATE, player_powers={PowerId.MANTRA_INTERNAL: 9})
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.DIVINITY)
        self.see_player_has_energy(play, 8)
        self.see_player_has_power(play, PowerId.MANTRA_INTERNAL, 1)

    def test_divinity_triples_damage_dealt(self):
        state = self.given_state(CardId.STRIKE_R)
        state.add_memory_value(MemoryItem.STANCE, StanceType.DIVINITY)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 18)

    def test_enter_divinity_and_exit_calm(self):
        state = self.given_state(CardId.PROSTRATE, player_powers={PowerId.MANTRA_INTERNAL: 9})
        state.add_memory_value(MemoryItem.STANCE, StanceType.CALM)
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.DIVINITY)
        self.see_player_has_energy(play, 10)
        self.see_player_has_power(play, PowerId.MANTRA_INTERNAL, 1)

    def test_divinity_exits_on_turn_end(self):
        state = self.given_state(CardId.STRIKE_R)
        state.change_stance(StanceType.DIVINITY)
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_stance(play, StanceType.NO_STANCE)

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

    def test_mental_fortress_power(self):
        state = self.given_state(CardId.CRESCENDO, player_powers={PowerId.MENTAL_FORTRESS: 4})
        state.add_memory_value(MemoryItem.STANCE, StanceType.NO_STANCE)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 4)
        self.see_stance(play, StanceType.WRATH)

    def test_flurry_of_blows(self):
        state = self.given_state(CardId.CRESCENDO)
        state.discard_pile.append(get_card(CardId.FLURRY_OF_BLOWS))
        state.discard_pile.append(get_card(CardId.FLURRY_OF_BLOWS))
        state.add_memory_value(MemoryItem.STANCE, StanceType.NO_STANCE)
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.WRATH)
        self.see_player_hand_count(play, 2)
        self.see_enemy_lost_hp(play, 0)
        self.assertEqual(CardId.FLURRY_OF_BLOWS, play.state.hand[0].id)

    def test_flurry_of_blows_cannot_be_retrieved_because_it_got_moved_to_draw(self):
        state = self.given_state(CardId.CRESCENDO, player_powers={PowerId.RUSHDOWN: 1})
        state.discard_pile.append(get_card(CardId.WOUND))
        state.discard_pile.append(get_card(CardId.FLURRY_OF_BLOWS))
        state.add_memory_value(MemoryItem.STANCE, StanceType.NO_STANCE)
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.WRATH)
        self.see_player_discard_pile_count(play, 0)
        self.see_player_hand_count(play, 1)
        self.see_enemy_lost_hp(play, 0)
        self.assertEqual(CardId.CRESCENDO, play.state.exhaust_pile[0].id)
        self.see_player_hand_count(play, 1)
        self.assertEqual(CardId.CARD_FROM_DRAW, play.state.hand[0].id)
        self.assertEqual(CardId.FLURRY_OF_BLOWS, play.state.draw_pile[0].id)

    def test_tantrum(self):
        state = self.given_state(CardId.TANTRUM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 9)
        self.see_player_discard_pile_count(play, 0)
        self.see_player_draw_pile_count(play, 1)
        self.assertEqual(CardId.TANTRUM, play.state.draw_pile[0].id)
        self.assertEqual(0, play.state.draw_pile[0].upgrade)
        self.see_stance(play, StanceType.WRATH)

    def test_tantrum_upgraded(self):
        state = self.given_state(CardId.TANTRUM, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 12)
        self.see_player_discard_pile_count(play, 0)
        self.see_player_draw_pile_count(play, 1)
        self.assertEqual(CardId.TANTRUM, play.state.draw_pile[0].id)
        self.assertEqual(1, play.state.draw_pile[0].upgrade)
        self.see_stance(play, StanceType.WRATH)

    def test_rushdown_power(self):
        state = self.given_state(CardId.CRESCENDO, player_powers={PowerId.RUSHDOWN: 4})
        state.add_memory_value(MemoryItem.STANCE, StanceType.NO_STANCE)
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.WRATH)
        self.see_player_drew_cards(play, 4)

    def test_rushdown_power_constrained_by_hand_size(self):
        state = self.given_state(CardId.CRESCENDO, player_powers={PowerId.RUSHDOWN: 4})
        for i in range(9):
            state.hand.append(get_card(CardId.WOUND))
        state.add_memory_value(MemoryItem.STANCE, StanceType.NO_STANCE)
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.WRATH)
        self.see_player_drew_cards(play, 1)

    def test_inner_peace_goes_calm_if_not_calm(self):
        state = self.given_state(CardId.INNER_PEACE)
        state.add_memory_value(MemoryItem.STANCE, StanceType.NO_STANCE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 0)
        self.see_stance(play, StanceType.CALM)

    def test_inner_peace_draws_if_calm(self):
        state = self.given_state(CardId.INNER_PEACE)
        state.add_memory_value(MemoryItem.STANCE, StanceType.CALM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 3)
        self.see_stance(play, StanceType.CALM)

    def test_indignation_goes_wrath_if_not_wrath(self):
        state = self.given_state(CardId.INDIGNATION)
        state.add_memory_value(MemoryItem.STANCE, StanceType.NO_STANCE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 0)
        self.see_stance(play, StanceType.WRATH)

    def test_indignation_applies_vulnerable_if_wrath(self):
        state = self.given_state(CardId.INDIGNATION, targets=2)
        state.add_memory_value(MemoryItem.STANCE, StanceType.WRATH)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 3, 0)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 3, 0)
        self.see_stance(play, StanceType.WRATH)

    def test_indignation_applies_vulnerable_if_wrath_upgraded(self):
        state = self.given_state(CardId.INDIGNATION, upgrade=1, targets=2)
        state.add_memory_value(MemoryItem.STANCE, StanceType.WRATH)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 5, 0)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 5, 0)
        self.see_stance(play, StanceType.WRATH)

    def test_fear_no_evil_triggers(self):
        state = self.given_state(CardId.FEAR_NO_EVIL)
        state.add_memory_value(MemoryItem.STANCE, StanceType.NO_STANCE)
        state.monsters[0].hits = 1
        state.monsters[0].damage = 1
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 8)
        self.see_stance(play, StanceType.CALM)

    def test_fear_no_evil_does_not_trigger_on_no_hits(self):
        state = self.given_state(CardId.FEAR_NO_EVIL)
        state.add_memory_value(MemoryItem.STANCE, StanceType.NO_STANCE)
        state.monsters[0].hits = 0
        state.monsters[0].damage = 1
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 8)
        self.see_stance(play, StanceType.NO_STANCE)

    def test_fear_no_evil_does_not_trigger_on_not_real_damage(self):
        state = self.given_state(CardId.FEAR_NO_EVIL)
        state.add_memory_value(MemoryItem.STANCE, StanceType.NO_STANCE)
        state.monsters[0].hits = 1
        state.monsters[0].damage = -1
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 8)
        self.see_stance(play, StanceType.NO_STANCE)

    def test_halt_triggers(self):
        state = self.given_state(CardId.HALT)
        state.add_memory_value(MemoryItem.STANCE, StanceType.WRATH)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_has_block(play, 12)

    def test_halt_triggers_upgraded(self):
        state = self.given_state(CardId.HALT, upgrade=1)
        state.add_memory_value(MemoryItem.STANCE, StanceType.WRATH)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_has_block(play, 18)

    def test_halt_does_not_trigger(self):
        state = self.given_state(CardId.HALT)
        state.add_memory_value(MemoryItem.STANCE, StanceType.NO_STANCE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_has_block(play, 3)

    def test_gaining_mantra_actively_increases_mantra_counter(self):
        state = self.given_state(CardId.PRAY)
        state.player.energy = 1
        play = self.when_playing_the_whole_hand(state)
        play.state.end_turn()
        self.see_enemy_lost_hp(play, 0)
        self.assertEqual(3, play.state.get_memory_value(MemoryItem.MANTRA_THIS_BATTLE))

    def test_devotion_increases_mantra_counter(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.DEVOTION: 2})
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_whole_hand(state)
        self.assertEqual(2, play.state.get_memory_value(MemoryItem.MANTRA_THIS_BATTLE))

    def test_damaru_increases_mantra_counter(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.DAMARU: 1})
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_whole_hand(state)
        self.assertEqual(1, play.state.get_memory_value(MemoryItem.MANTRA_THIS_BATTLE))
        self.see_player_has_power(play, PowerId.MANTRA_INTERNAL, 1)

    def test_damaru_pushes_into_divinity(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.DAMARU: 1}, player_powers={PowerId.MANTRA_INTERNAL: 9})
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_whole_hand(state)
        self.assertEqual(1, play.state.get_memory_value(MemoryItem.MANTRA_THIS_BATTLE))
        self.see_stance(play, StanceType.DIVINITY)
        self.see_player_has_power(play, PowerId.MANTRA_INTERNAL, 0)

    def test_blasphemy(self):
        state = self.given_state(CardId.BLASPHEMY)
        play = self.when_playing_the_first_card(state)
        self.see_stance(play, StanceType.DIVINITY)
        self.see_player_spent_energy(play, -2)
        self.see_player_has_power(play, PowerId.BLASPHEMER, 1)

    def test_passive_mantra_can_put_us_into_divinity(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.DAMARU: 1}, player_powers={PowerId.MANTRA_INTERNAL: 9})
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 18)
        self.see_stance(play, StanceType.DIVINITY)

    def test_internal_mantra_saved_into_memory_book(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.DAMARU: 1}, player_powers={PowerId.MANTRA_INTERNAL: 5})
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.assertEqual(6, play.state.get_memory_value(MemoryItem.SAVE_INTERNAL_MANTRA))

    def test_internal_mantra_retrieved_from_memory_book(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.DAMARU: 1})
        state.add_memory_value(MemoryItem.SAVE_INTERNAL_MANTRA, 3)
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_has_power(play, PowerId.MANTRA_INTERNAL, 4)
        self.assertEqual(4, play.state.get_memory_value(MemoryItem.SAVE_INTERNAL_MANTRA))
