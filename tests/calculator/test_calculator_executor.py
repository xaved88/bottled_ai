import unittest

from rs.calculator.executor import get_discard_commands, get_exhaust_commands
from rs.calculator.battle_state import PLAY_DISCARD, PLAY_EXHAUST


class CalculatorExecutorTestCase(unittest.TestCase):

    def test_simple_discard_command_case(self):
        # given
        plays = [(0, PLAY_DISCARD), (0, PLAY_DISCARD), (0, PLAY_DISCARD)]
        # when
        result = get_discard_commands(plays)
        # then
        self.assertEqual(["choose 0", "choose 1", "choose 2", "confirm", "wait 30"], result)

    def test_complex_discard_command_case(self):
        # given
        plays = [(2, PLAY_DISCARD), (1, PLAY_DISCARD), (3, PLAY_DISCARD)]
        # when
        result = get_discard_commands(plays)
        # then
        self.assertEqual(["choose 2", "choose 1", "choose 5", "confirm", "wait 30"], result)

    def test_partial_discard_command_case(self):
        # given
        plays = [(2, PLAY_DISCARD), (1, -1), (3, PLAY_DISCARD)]
        # when
        result = get_discard_commands(plays)
        # then
        self.assertEqual(["choose 2", "confirm", "wait 30"], result)

    def test_simple_exhaust_command_case(self):
        # given
        plays = [(0, PLAY_EXHAUST), (0, PLAY_EXHAUST), (0, PLAY_EXHAUST)]
        # when
        result = get_exhaust_commands(plays)
        # then
        self.assertEqual(["choose 0", "choose 1", "choose 2", "confirm", "wait 30"], result)

    def test_complex_exhaust_command_case(self):
        # given
        plays = [(2, PLAY_EXHAUST), (1, PLAY_EXHAUST), (3, PLAY_EXHAUST)]
        # when
        result = get_exhaust_commands(plays)
        # then
        self.assertEqual(["choose 2", "choose 1", "choose 5", "confirm", "wait 30"], result)

    def test_partial_exhaust_command_case(self):
        # given
        plays = [(2, PLAY_EXHAUST), (1, -1), (3, PLAY_EXHAUST)]
        # when
        result = get_exhaust_commands(plays)
        # then
        self.assertEqual(["choose 2", "confirm", "wait 30"], result)