import unittest

from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.potion_id import PotionId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.game_state_converter import create_battle_state
from rs.calculator.interfaces.memory_items import MemoryItem
from rs.machine.orb import Orb
from test_helpers.resources import load_resource_state


class GameStateConverterTest(unittest.TestCase):

    def test_battle_state_fails_with_non_battle_game_state(self):
        state = load_resource_state("event/event_purifier.json")
        battle_state = create_battle_state(state)
        self.assertIsNone(battle_state)

    def test_simple_battle_state_loaded(self):
        state = load_resource_state("battles/general/battle_simple_state.json")
        battle_state = create_battle_state(state)
        self.assertIsNotNone(battle_state)
        self.assertEqual(4, len(battle_state.hand))
        self.assertEqual(5, len(battle_state.draw_pile))
        self.assertEqual(1, len(battle_state.discard_pile))

    def test_battle_state_with_relics_loaded(self):
        state = load_resource_state("battles/general/battle_state_pen_nib.json")
        battle_state = create_battle_state(state)
        self.assertIsNotNone(battle_state)
        self.assertEqual(3, len(battle_state.relics))
        self.assertIn(RelicId.BURNING_BLOOD, battle_state.relics)
        self.assertIn(RelicId.BLOOD_VIAL, battle_state.relics)
        self.assertIn(RelicId.PEN_NIB, battle_state.relics)

    def test_battle_state_with_powers(self):
        state = load_resource_state("battles/general/battle_state_enemy_vulnerable.json")
        battle_state = create_battle_state(state)
        self.assertIsNotNone(battle_state)
        self.assertIn(PowerId.VULNERABLE, battle_state.monsters[0].powers)

    def test_echo_form_ready_is_loaded(self):
        state = load_resource_state("battles/powers/echo_form_ready.json")
        battle_state = create_battle_state(state)
        self.assertIsNotNone(battle_state)
        self.assertIn(PowerId.INTERNAL_ECHO_FORM_READY, battle_state.player.powers)
        self.assertEqual(battle_state.player.powers[PowerId.INTERNAL_ECHO_FORM_READY], 1)

    def test_echo_form_not_ready_is_loaded(self):
        state = load_resource_state("battles/powers/echo_form_not_ready.json")
        battle_state = create_battle_state(state)
        self.assertIsNotNone(battle_state)
        self.assertNotIn(PowerId.INTERNAL_ECHO_FORM_READY, battle_state.player.powers)

    def test_echo_form_multiple_charges_ready_is_loaded(self):
        # NOTE: This is a doctored state
        # I haven't confirmed this is actually what multiple echo form charges look like in game
        state = load_resource_state("battles/powers/echo_form_double_ready.json")
        battle_state = create_battle_state(state)
        self.assertIsNotNone(battle_state)
        self.assertIn(PowerId.INTERNAL_ECHO_FORM_READY, battle_state.player.powers)
        self.assertEqual(battle_state.player.powers[PowerId.INTERNAL_ECHO_FORM_READY], 2)

    def test_battle_state_loaded_custom_state(self):
        state = load_resource_state("battles/general/battle_state_pen_nib.json")
        battle_state = create_battle_state(state)
        self.assertIsNotNone(battle_state)
        self.assertIsNotNone(state.memory_by_card[CardId.RITUAL_DAGGER])
        self.assertIsNotNone(battle_state.memory_by_card[CardId.RITUAL_DAGGER])

    def test_battle_state_loaded_attacks_this_turn(self):
        state = load_resource_state("battles/general/battle_state_pen_nib.json")
        battle_state = create_battle_state(state)
        self.assertIsNotNone(battle_state)
        self.assertEqual(0, state.memory_general[MemoryItem.ATTACKS_THIS_TURN])
        self.assertEqual(0, battle_state.memory_general[MemoryItem.ATTACKS_THIS_TURN])

    def test_battle_state_with_potions_loaded(self):
        state = load_resource_state("battles/general/battle_state_potions.json")
        battle_state = create_battle_state(state)
        self.assertIsNotNone(battle_state)
        self.assertEqual(3, len(battle_state.potions))
        self.assertIn(PotionId.FAIRY_IN_A_BOTTLE, battle_state.potions)

    def test_get_monster_name(self):
        state = load_resource_state("battles/general/attack.json")
        battle_state = create_battle_state(state)
        self.assertEqual('Cultist', battle_state.monsters[0].name)

    def test_orb_slot_count(self):
        state = load_resource_state("battles/with_orbs/basic_defect_with_orbs.json")
        count = state.get_player_orb_slots()
        self.assertEqual(3, count)

    def test_orb_slot_count_when_no_orbs(self):
        state = load_resource_state("battles/general/battle_simple_state.json")
        count = state.get_player_orb_slots()
        self.assertEqual(0, count)

    def test_get_orbs(self):
        state = load_resource_state("battles/with_orbs/basic_defect_with_orbs.json")
        orbs = state.get_player_orbs()
        self.assertEqual(1, len(orbs))
        (orbId, amount) = orbs[0]
        self.assertEqual(Orb.LIGHTNING, orbId)
        self.assertEqual(8, amount)

    def test_get_charged_dark_orb(self):
        state = load_resource_state("battles/with_orbs/multi_evoke_kills_last_enemy.json")
        orbs = state.get_player_orbs()
        self.assertEqual(1, len(orbs))
        (orbId, amount) = orbs[0]
        self.assertEqual(Orb.DARK, orbId)
        self.assertEqual(13, amount)

    def test_get_orbs_state_contains_specifically_empty_orbs(self):
        state = load_resource_state("battles/with_orbs/defect_very_without_orbs.json")
        orbs = state.get_player_orbs()
        self.assertEqual(0, len(orbs))