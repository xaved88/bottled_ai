import unittest

from test_helpers.resources import load_resource_state


class GameStateConverterTest(unittest.TestCase):

    def test_loading_all_potions(self):
        state = load_resource_state("other/combat_reward_full_potions.json")
        potions = state.get_all_available_potions_by_name()
        self.assertEqual(potions, ['cultist potion', 'speed potion', 'power potion', 'ancient potion'])

    def test_get_relic_counter(self):
        state = load_resource_state("campfire/campfire_girya_lift.json")
        counter = state.get_relic_counter("Girya")
        self.assertEqual(counter, 0)

    def test_get_relic_counter_failure(self):
        state = load_resource_state("campfire/campfire_rest.json")
        counter = state.get_relic_counter("Girya")
        self.assertEqual(counter, False)
