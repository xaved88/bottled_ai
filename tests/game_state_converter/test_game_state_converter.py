import unittest

from test_helpers.resources import load_resource_state


class GameStateConverterTest(unittest.TestCase):

    def test_loading_all_potions(self):
        state = load_resource_state("other/combat_reward_full_potions.json")
        potions = state.get_held_potion_names() + state.get_reward_potion_names()
        self.assertEqual(['cultist potion', 'speed potion', 'power potion', 'ancient potion'], potions)

    def test_get_relic_counter(self):
        state = load_resource_state("campfire/campfire_girya_lift.json")
        counter = state.get_relic_counter("Girya")
        self.assertEqual(0, counter)

    def test_get_relic_counter_failure(self):
        state = load_resource_state("campfire/campfire_rest.json")
        counter = state.get_relic_counter("Girya")
        self.assertEqual(False, counter)

    def test_get_choice_list(self):
        state = load_resource_state("card_reward/card_reward_skip_upgraded_card_because_amount.json")
        choices = state.get_choice_list()
        self.assertEqual(['pommel strike', 'heel hook', 'twin strike+'], choices)

    def test_get_choice_list_upgrade_stripped_from_choice(self):
        state = load_resource_state("card_reward/card_reward_skip_upgraded_card_because_amount.json")
        choices = state.get_choice_list_upgrade_stripped_from_choice()
        self.assertEqual(['pommel strike', 'heel hook', 'twin strike'], choices)

    def test_get_deck_card_list(self):
        state = load_resource_state("card_reward/card_reward_skip_because_amount_and_some_in_deck_are_upgraded.json")
        deck_list = state.get_deck_card_list()
        self.assertEqual({'bash+': 1, 'defend': 4, 'strike': 3, 'twin strike': 1, 'twin strike+': 1}, deck_list)

    def test_get_deck_card_list_upgrade_stripped_from_name(self):
        state = load_resource_state("card_reward/card_reward_skip_because_amount_and_some_in_deck_are_upgraded.json")
        deck_list = state.get_deck_card_list_upgrade_stripped_from_name()
        self.assertEqual({'bash': 1, 'defend': 4, 'strike': 3, 'twin strike': 2}, deck_list)

    def test_custom_state_is_initialized_if_missing(self):
        state = load_resource_state("battles/general/battle_state_pen_nib.json", memory_book=None)
        self.assertEqual(True, state.memory_general is not None)

    def test_curse_of_the_bell_stripped_by_curse_check_that_strips_it(self):
        state = load_resource_state("campfire/campfire_do_not_toke.json")
        deck_list = state.deck.contains_curses_we_can_remove()
        self.assertEqual(False, deck_list)

    def test_curse_of_the_bell_not_stripped_by_inclusive_curse_check(self):
        state = load_resource_state("campfire/campfire_do_not_toke.json")
        deck_list = state.deck.contains_curses_of_any_kind()
        self.assertEqual(True, deck_list)

    def test_get_correct_amount_of_card_in_deck(self):
        state = load_resource_state("other/some_strikes_in_deck.json")
        self.assertEqual(3, state.deck.contains_card_amount("strike"))

