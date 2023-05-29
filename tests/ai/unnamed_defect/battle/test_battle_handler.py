import unittest

from ai.unnamed_defect.ud_test_handler_fixture import UdTestHandlerFixture
from rs.common.handlers.common_battle_handler import CommonBattleHandler


class BattleHandlerTestCase(UdTestHandlerFixture):
    handler = CommonBattleHandler

    def test_plays_dualcast(self):
        self.execute_handler_tests('battles/with_orbs/defect_with_orb_and_dualcast.json', ['play 2'])


if __name__ == '__main__':
    unittest.main()
