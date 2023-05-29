import unittest

from rs.calculator.comparator import DefaultSbcComparator
from rs.calculator.executor import get_best_battle_path
from test_helpers.resources import load_resource_state
from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.cards import get_card
from rs.calculator.enums.card_id import CardId


class CalculatorOtherTest(CalculatorTestFixture):

    def test_minions_die_when_leader_dies(self):
        state = load_resource_state("battles/smart_battle/smart_battle_minions.json")
        path = get_best_battle_path(state, DefaultSbcComparator(), 100)
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
