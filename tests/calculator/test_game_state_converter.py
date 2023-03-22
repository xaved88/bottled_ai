import unittest

from rs.calculator.game_state_converter import create_hand_state
from rs.calculator.powers import PowerId
from rs.calculator.relics import RelicId
from test_helpers.resources import load_resource_state


class GameStateConverterTest(unittest.TestCase):

    def test_hand_state_fails_with_non_battle_game_state(self):
        state = load_resource_state("other/event_purifier.json")
        hand_state = create_hand_state(state)
        self.assertIsNone(hand_state)

    def test_simple_hand_state_loaded(self):
        state = load_resource_state("battles/general/battle_simple_state.json")
        hand_state = create_hand_state(state)
        self.assertIsNotNone(hand_state)
        self.assertEqual(4, len(hand_state.hand))
        self.assertEqual(5, len(hand_state.draw_pile))
        self.assertEqual(1, len(hand_state.discard_pile))

    def test_hand_state_with_relics_loaded(self):
        state = load_resource_state("battles/general/battle_state_pen_nib.json")
        hand_state = create_hand_state(state)
        self.assertIsNotNone(hand_state)
        self.assertEqual(3, len(hand_state.relics))
        self.assertIn(RelicId.BURNING_BLOOD, hand_state.relics)
        self.assertIn(RelicId.BLOOD_VIAL, hand_state.relics)
        self.assertIn(RelicId.PEN_NIB, hand_state.relics)

    def test_hand_state_with_powers(self):
        state = load_resource_state("battles/general/battle_state_enemy_vulnerable.json")
        hand_state = create_hand_state(state)
        self.assertIsNotNone(hand_state)
        self.assertIn(PowerId.VULNERABLE, hand_state.monsters[0].powers)
