from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.cards import get_card
from rs.calculator.enums.card_id import CardId
from rs.calculator.executor import get_best_battle_path
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
