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

    def test_get_deck_card_list_by_id(self):
        state = load_resource_state("card_reward/card_reward_skip_because_amount_and_some_in_deck_are_upgraded.json")
        deck_list = state.get_deck_card_list_by_id()
        self.assertEqual({'bash': 1, 'defend_r': 4, 'strike_r': 3, 'twin strike': 2}, deck_list)

    def test_get_deck_card_list_upgrade_stripped_from_name(self):
        state = load_resource_state("card_reward/card_reward_skip_because_amount_and_some_in_deck_are_upgraded.json")
        deck_list = state.get_deck_card_list_by_name_with_upgrade_stripped()
        self.assertEqual({'bash': 1, 'defend': 4, 'strike': 3, 'twin strike': 2}, deck_list)

    def test_custom_state_is_initialized_if_missing(self):
        state = load_resource_state("battles/general/battle_state_pen_nib.json", memory_book=None)
        self.assertEqual(True, state.memory_general is not None)

    def test_curse_of_the_bell_stripped_by_curse_check_that_strips_it(self):
        state = load_resource_state("campfire/campfire_do_not_toke.json")
        self.assertEqual(False, state.deck.contains_curses_we_can_remove())

    def test_curse_of_the_bell_not_stripped_by_inclusive_curse_check(self):
        state = load_resource_state("campfire/campfire_do_not_toke.json")
        self.assertEqual(True, state.deck.contains_curses_of_any_kind())

    def test_get_correct_amount_of_card_in_deck(self):
        state = load_resource_state("other/some_strikes_in_deck.json")
        self.assertEqual(3, state.deck.contains_card_amount("strike"))

    def test_get_falling_event_options(self):
        state = load_resource_state("event/event_falling.json")
        self.assertEqual(['tranquility', 'strike', 'halt'], state.get_falling_event_options())

    def test_get_falling_event_2_options(self):
        state = load_resource_state("event/event_falling_2_options.json")
        self.assertEqual(['tranquility', 'crush joints'], state.get_falling_event_options())

    def test_get_act_4_keys(self):
        state = load_resource_state("other/act_4_keys.json")
        self.assertEqual(['e', 's'], state.get_act_4_keys())

    def test_get_act_4_keys_not_present(self):
        state = load_resource_state("other/chest_medium_reward.json")
        self.assertEqual(['Communication Mod out of date'], state.get_act_4_keys())

    def test_get_burning_elite_position(self):
        state = load_resource_state("path/path_includes_burning_elite.json")
        self.assertEqual('1_5', state.get_burning_elite_position())

    def test_get_burning_elite_position_not_available(self):
        state = load_resource_state("path/path_elites.json")
        self.assertEqual(0, state.get_burning_elite_position())

