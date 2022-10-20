import unittest

from rs.calculator.comparator import DefaultSbcComparator
from rs.calculator.executor import get_best_battle_path
from test_helpers.resources import load_resource_state


class CalculatorOtherTest(unittest.TestCase):

    def test_minions_die_when_leader_dies(self):
        state = load_resource_state("battles/smart_battle/smart_battle_minions.json")
        path = get_best_battle_path(state, DefaultSbcComparator())
        for monster in path.state.monsters:
            self.assertEqual(0, monster.current_hp)
        self.assertEqual(1, len(path.plays))
