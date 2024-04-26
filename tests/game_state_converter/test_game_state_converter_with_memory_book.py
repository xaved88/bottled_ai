import unittest

from rs.calculator.enums.card_id import CardId
from rs.calculator.interfaces.memory_items import MemoryItem, ResetSchedule
from rs.machine.the_bots_memory_book import TheBotsMemoryBook
from test_helpers.resources import load_resource_state


class GameStateConverterWithMemoryBookTest(unittest.TestCase):

    def test_memory_of_steam_barrier_is_reset_outside_of_battle(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_by_card[CardId.STEAM_BARRIER][ResetSchedule.BATTLE] = {"test": 4}
        new_state = load_resource_state('card_reward/card_reward_take.json', memory_book=mb)
        self.assertEqual(False, "test" in new_state.memory_by_card[CardId.STEAM_BARRIER][ResetSchedule.BATTLE])

    def test_memory_of_ritual_dagger_is_not_reset_outside_of_battle(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_by_card[CardId.RITUAL_DAGGER][ResetSchedule.GAME] = {"test": 4}
        new_state = load_resource_state('card_reward/card_reward_take.json', memory_book=mb)
        self.assertEqual(True, "test" in new_state.memory_by_card[CardId.RITUAL_DAGGER][ResetSchedule.GAME])

    def test_memory_of_glass_knife_is_reset_outside_of_battle(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_by_card[CardId.GLASS_KNIFE][ResetSchedule.BATTLE] = {"test": 4}
        new_state = load_resource_state('card_reward/card_reward_take.json', memory_book=mb)
        self.assertEqual(False, "test" in new_state.memory_by_card[CardId.GLASS_KNIFE][ResetSchedule.BATTLE])

    def test_memory_of_claws_played_is_reset_outside_of_battle(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_general[MemoryItem.CLAWS_THIS_BATTLE] = 4
        new_state = load_resource_state('card_reward/card_reward_take.json', memory_book=mb)
        self.assertEqual(0, new_state.memory_general[MemoryItem.CLAWS_THIS_BATTLE])

    def test_memory_of_attacks_this_turn_is_not_reset_while_in_the_same_turn(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_general[MemoryItem.ATTACKS_THIS_TURN] = 4
        new_state = load_resource_state('battles/general/basic_turn_1.json', memory_book=mb)
        self.assertEqual(4, new_state.memory_general[MemoryItem.ATTACKS_THIS_TURN])

    def test_memory_of_attacks_this_turn_is_reset_when_entering_a_new_turn(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_general[MemoryItem.ATTACKS_THIS_TURN] = 4
        new_state = load_resource_state('battles/general/basic_turn_2.json', memory_book=mb)
        self.assertEqual(0, new_state.memory_general[MemoryItem.ATTACKS_THIS_TURN])

    def test_memory_of_attacks_this_turn_is_reset_when_leaving_battle(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_general[MemoryItem.ATTACKS_THIS_TURN] = 4
        new_state = load_resource_state('card_reward/card_reward_take.json', memory_book=mb)
        self.assertEqual(0, new_state.memory_general[MemoryItem.ATTACKS_THIS_TURN])

    def test_memory_of_cards_this_turn_is_reset_when_entering_a_new_turn(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_general[MemoryItem.CARDS_THIS_TURN] = 4
        new_state = load_resource_state('battles/general/basic_turn_2.json', memory_book=mb)
        self.assertEqual(0, new_state.memory_general[MemoryItem.CARDS_THIS_TURN])

    def test_memory_of_frost_this_battle_is_reset_when_leaving_battle(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_general[MemoryItem.FROST_THIS_BATTLE] = 4
        new_state = load_resource_state('card_reward/card_reward_take.json', memory_book=mb)
        self.assertEqual(0, new_state.memory_general[MemoryItem.FROST_THIS_BATTLE])

    def test_memory_of_lightning_this_battle_turn_is_reset_when_leaving_battle(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_general[MemoryItem.LIGHTNING_THIS_BATTLE] = 4
        new_state = load_resource_state('card_reward/card_reward_take.json', memory_book=mb)
        self.assertEqual(0, new_state.memory_general[MemoryItem.LIGHTNING_THIS_BATTLE])
