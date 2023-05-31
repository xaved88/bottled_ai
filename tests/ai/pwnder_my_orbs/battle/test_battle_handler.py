import unittest

from ai.pwnder_my_orbs.pmo_test_handler_fixture import PmoTestHandlerFixture
from rs.ai.pwnder_my_orbs.handlers.battle_handler import BattleHandler


class BattleHandlerTestCase(PmoTestHandlerFixture):
    handler = BattleHandler

    def test_plays_dualcast(self):
        self.execute_handler_tests('battles/with_orbs/defect_with_orb_and_dualcast.json', ['play 2'])

    def test_keep_calculating_even_if_multi_evoke_killed_everyone(self):
        self.execute_handler_tests('battles/with_orbs/multi_evoke_kills_last_enemy.json', ['play 1'])


if __name__ == '__main__':
    unittest.main()
