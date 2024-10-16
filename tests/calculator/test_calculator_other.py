from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.cards import get_card
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.executor import get_best_battle_path
from rs.calculator.interfaces.memory_items import MemoryItem, StanceType
from rs.common.comparators.common_general_comparator import CommonGeneralComparator
from test_helpers.resources import load_resource_state


class CalculatorOtherTest(CalculatorTestFixture):

    def test_minions_die_when_leader_dies(self):
        state = load_resource_state("battles/general/minions.json")
        path = get_best_battle_path(state, CommonGeneralComparator(), 100)
        for monster in path.state.monsters:
            self.assertEqual(0, monster.current_hp)
        self.assertEqual(1, len(path.plays))

    def test_draw_uncapped_by_hand_amount(self):
        state = self.given_state(CardId.BATTLE_TRANCE)
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 3)
        self.see_player_drew_cards(play, 3)
        self.see_player_discard_pile_count(play, 1)

    def test_draw_capped_by_hand_amount(self):
        state = self.given_state(CardId.BATTLE_TRANCE)
        for i in range(9):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 10)
        self.see_player_drew_cards(play, 1)
        self.see_player_discard_pile_count(play, 1)

    def test_draw_pile_reduced_by_drawing_cards(self):
        state = self.given_state(CardId.GRAND_FINALE)
        state.hand.append(get_card(CardId.SHRUG_IT_OFF))
        state.draw_pile.append(get_card(CardId.DEFEND_R))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_draw_pile_count(play, 0)
        self.see_enemy_lost_hp(play, 50)

    def test_emptying_draw_pile_clears_discard_pile_one_draw(self):
        state = self.given_state(CardId.SHRUG_IT_OFF)
        for i in range(6):
            state.discard_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_drew_cards(play, 1)
        self.see_player_hand_count(play, 1)
        self.see_player_draw_pile_count(play, 5)
        self.see_player_discard_pile_count(play, 1)

    def test_emptying_draw_pile_clears_discard_pile_multi_draw(self):
        state = self.given_state(CardId.BATTLE_TRANCE)
        state.draw_pile.append(get_card(CardId.WOUND))
        for i in range(6):
            state.discard_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_drew_cards(play, 3)
        self.see_player_hand_count(play, 3)
        self.see_player_draw_pile_count(play, 4)
        self.see_player_discard_pile_count(play, 1)

    def test_type_of_drawn_card_free_early(self):
        state = self.given_state(CardId.OFFERING)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, -2)
        self.see_player_drew_cards(play, 3)
        self.assertEqual(3, play.state.draw_free_early)
        self.assertEqual(0, play.state.draw_pay_early)
        self.assertEqual(0, play.state.draw_free)
        self.assertEqual(0, play.state.draw_pay)

    def test_type_of_drawn_card_pay_early(self):
        state = self.given_state(CardId.ACROBATICS)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 3)
        self.assertEqual(0, play.state.draw_free_early)
        self.assertEqual(3, play.state.draw_pay_early)
        self.assertEqual(0, play.state.draw_free)
        self.assertEqual(0, play.state.draw_pay)

    def test_type_of_drawn_card_free(self):
        state = self.given_state(CardId.BATTLE_TRANCE)
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 3)
        self.assertEqual(0, play.state.draw_free_early)
        self.assertEqual(0, play.state.draw_pay_early)
        self.assertEqual(3, play.state.draw_free)
        self.assertEqual(0, play.state.draw_pay)

    def test_type_of_drawn_card_pay(self):
        state = self.given_state(CardId.SHRUG_IT_OFF)
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_drew_cards(play, 1)
        self.assertEqual(0, play.state.draw_free_early)
        self.assertEqual(0, play.state.draw_pay_early)
        self.assertEqual(0, play.state.draw_free)
        self.assertEqual(1, play.state.draw_pay)

    def test_type_of_drawn_card_rushdown(self):
        state = self.given_state(CardId.ERUPTION, player_powers={PowerId.RUSHDOWN: 2})
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 3)
        self.see_player_drew_cards(play, 2)
        self.assertEqual(0, play.state.draw_free_early)
        self.assertEqual(0, play.state.draw_pay_early)
        self.assertEqual(0, play.state.draw_free)
        self.assertEqual(2, play.state.draw_pay)

    def test_type_of_drawn_card_comparator_values_restricted_by_hand(self):
        state = self.given_state(CardId.INSIGHT)
        for i in range(9):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_drew_cards(play, 1)
        self.assertEqual(1, play.state.draw_free_early)
        self.assertEqual(0, play.state.draw_pay_early)
        self.assertEqual(0, play.state.draw_free)
        self.assertEqual(0, play.state.draw_pay)

    def test_cards_that_should_exhaust_do_actually_exhaust(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand[0].exhausts = True
        play = self.when_playing_the_first_card(state)
        self.see_player_exhaust_count(play, 1)
        self.see_player_discard_pile_count(play, 0)
        self.see_player_hand_count(play, 0)

    def test_ethereal_cards_exhaust_on_turn_end(self):
        state = self.given_state(CardId.ASCENDERS_BANE)
        state.hand.append(get_card(CardId.ASCENDERS_BANE))
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_exhaust_count(play, 2)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_hand_count(play, 0)

    def test_ethereal_cards_exhaust_after_curses_applied(self):
        state = self.given_state(CardId.REGRET)
        state.hand.append(get_card(CardId.ASCENDERS_BANE))
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_lost_hp(play, 2)

    def test_hand_goes_to_discard_when_turn_ended(self):
        state = self.given_state(CardId.WOUND)
        state.hand.append(get_card(CardId.DOUBT))
        state.hand.append(get_card(CardId.DOUBT))
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_hand_count(play, 0)
        self.see_player_discard_pile_count(play, 3)

    def test_retrieve_from_discard_single(self):
        state = self.given_state(CardId.WOUND)
        for i in range(5):
            state.discard_pile.append(get_card(CardId.CLEAVE))
        play = self.when_playing_the_first_card(state)
        play.state.retrieve_from_discard(CardId.CLEAVE, just_one=True)
        self.see_player_hand_count(play, 2)
        self.see_player_discard_pile_count(play, 4)
        self.see_hand_card_is(play, CardId.WOUND, 0)
        self.see_hand_card_is(play, CardId.CLEAVE, 1)

    def test_retrieve_from_discard_multiple(self):
        state = self.given_state(CardId.WOUND)
        for i in range(5):
            state.discard_pile.append(get_card(CardId.CLEAVE))
        play = self.when_playing_the_first_card(state)
        play.state.retrieve_from_discard(CardId.CLEAVE, just_one=False)
        self.see_player_hand_count(play, 6)
        self.see_player_discard_pile_count(play, 0)
        self.see_hand_card_is(play, CardId.WOUND, 0)
        self.see_hand_card_is(play, CardId.CLEAVE, 1)

    def test_retrieve_from_discard_limited_by_hand_size(self):
        state = self.given_state(CardId.WOUND)
        for i in range(8):
            state.hand.append(get_card(CardId.WOUND))
        for i in range(5):
            state.discard_pile.append(get_card(CardId.CLEAVE))
        play = self.when_playing_the_first_card(state)
        play.state.retrieve_from_discard(CardId.CLEAVE, just_one=False)
        self.see_player_hand_count(play, 10)
        self.see_player_discard_pile_count(play, 4)
        self.see_hand_card_is(play, CardId.WOUND, 0)
        self.see_hand_card_is(play, CardId.CLEAVE, 9)

    def test_inflict_random_damage_respects_vulnerable_modifiers(self):
        state = self.given_state(CardId.SWORD_BOOMERANG, relics={RelicId.PAPER_PHROG: 1})
        state.monsters[0].powers[PowerId.VULNERABLE] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 15)
        self.see_random_damage_dealt(play, 0)

    def test_inflict_random_damage_respects_pen_nib_single_target(self):
        state = self.given_state(CardId.SWORD_BOOMERANG, relics={RelicId.PEN_NIB: 9})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 18)
        self.see_random_damage_dealt(play, 0)

    def test_inflict_random_damage_respects_pen_nib_multi_target(self):
        state = self.given_state(CardId.SWORD_BOOMERANG, relics={RelicId.PEN_NIB: 9}, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_random_damage_dealt(play, 18)

    def test_inflict_random_damage_respects_wrath_single_target(self):
        state = self.given_state(CardId.SWORD_BOOMERANG)
        state.add_memory_value(MemoryItem.STANCE, StanceType.WRATH)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 18)
        self.see_random_damage_dealt(play, 0)

    def test_inflict_random_damage_respects_wrath(self):
        state = self.given_state(CardId.SWORD_BOOMERANG, targets=2)
        state.add_memory_value(MemoryItem.STANCE, StanceType.WRATH)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_random_damage_dealt(play, 18)

    def test_monster_block_disappears_on_their_turn(self):
        state = self.given_state(CardId.WOUND)
        state.monsters[0].block = 3
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_block_is(play, 0)

    def test_monster_block_does_not_prevent_them_taking_thorns_damage_because_it_is_gone(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.THORNS: 3})
        state.monsters[0].damage = 1
        state.monsters[0].hits = 1
        state.monsters[0].block = 3
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 3)

    def test_random_damage_affected_by_damage_bonuses(self):
        state = self.given_state(CardId.SWORD_BOOMERANG, relics={RelicId.PEN_NIB: 9}, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_random_damage_dealt(play, 18)

    def test_do_not_revive_from_normal_heal_regen(self):
        state = self.given_state(CardId.SWORD_BOOMERANG, player_powers={PowerId.REGENERATION_PLAYER: 3})
        state.player.current_hp = 0
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 50)

    def test_do_not_revive_from_dying_to_thorns_if_bite(self):
        state = self.given_state(CardId.BITE)
        state.monsters[0].powers[PowerId.THORNS] = 3
        state.player.current_hp = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 50)

    def test_damage_bonuses_apply_to_damage_granted_by_pre_hooks(self):
        state = self.given_state(CardId.MIND_BLAST)
        for i in range(5):
            state.draw_pile.append(get_card(CardId.WOUND))
        state.relics[RelicId.PEN_NIB] = 9
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_player_spent_energy(play, 2)
        self.see_relic_value(play, RelicId.PEN_NIB, 0)

    def test_trigger_more_than_X_cards_played_counter(self):
        state = self.given_state(CardId.STRIKE_R)
        state.add_memory_value(MemoryItem.CARDS_THIS_TURN, 29)
        play = self.when_playing_the_first_card(state)
        self.assertEqual(1, play.state.get_memory_value(MemoryItem.PLAYED_30_PLUS_CARDS_IN_A_TURN))

    def test_do_not_trigger_again_more_than_X_cards_played_counter(self):
        state = self.given_state(CardId.STRIKE_R)
        state.add_memory_value(MemoryItem.CARDS_THIS_TURN, 35)
        play = self.when_playing_the_first_card(state)
        self.assertEqual(1, play.state.get_memory_value(MemoryItem.PLAYED_30_PLUS_CARDS_IN_A_TURN))
