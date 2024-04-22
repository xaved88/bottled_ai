import unittest

from rs.calculator.enums.card_id import CardId
from rs.machine.the_bots_memory_book import TheBotsMemoryBook
from test_helpers.resources import load_resource_state


class GameStateConverterWithMemoryBookTest(unittest.TestCase):

    def test_memory_of_steam_barrier_is_reset_outside_of_battle(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_by_card[CardId.STEAM_BARRIER] = {"test": 4}
        new_state = load_resource_state('card_reward/card_reward_take.json', memory_book=mb)
        self.assertEqual(False, "test" in new_state.memory_by_card[CardId.STEAM_BARRIER])

    def test_memory_of_claws_played_is_reset_outside_of_battle(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory["claws_played_this_battle"] = 4
        new_state = load_resource_state('card_reward/card_reward_take.json', memory_book=mb)
        self.assertEqual(0, new_state.memory["claws_played_this_battle"])

    def test_memory_of_attacks_this_turn_is_not_reset_while_in_the_same_turn(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory["attacks_this_turn"] = 4
        new_state = load_resource_state('battles/general/basic_turn_1.json', memory_book=mb)
        self.assertEqual(4, new_state.memory["attacks_this_turn"])

    def test_memory_of_attacks_this_turn_is_reset_when_entering_a_new_turn(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory["attacks_this_turn"] = 4
        new_state = load_resource_state('battles/general/basic_turn_2.json', memory_book=mb)
        self.assertEqual(0, new_state.memory["attacks_this_turn"])

    def test_memory_of_attacks_this_turn_is_reset_when_leaving_battle(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory["attacks_this_turn"] = 4
        new_state = load_resource_state('card_reward/card_reward_take.json', memory_book=mb)
        self.assertEqual(0, new_state.memory["attacks_this_turn"])
