import unittest

from ai.pwnder_my_orbs.pmo_test_handler_fixture import PmoTestHandlerFixture
from rs.common.handlers.common_battle_handler import CommonBattleHandler


class BattleHandlerTestCase(PmoTestHandlerFixture):
    handler = CommonBattleHandler

    def test_plays_dualcast(self):
        self.execute_handler_tests('battles/with_orbs/defect_with_orb_and_dualcast.json', ['play 2'])


if __name__ == '__main__':
    unittest.main()
