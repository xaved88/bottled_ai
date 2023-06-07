import unittest

from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.custom_legacy_battle.sentries_handler import SentriesHandler
from rs.common.handlers.common_battle_handler import CommonBattleHandler


class SentriesHandlerTest(RsTestHandlerFixture):
    def test_attacks_edge_sentry_even_when_mid_is_lower_health(self):
        self.handler = SentriesHandler
        self.execute_handler_tests('battles/sentries/sentry_low_middle_health.json', ['play 5 0'])

    def test_yolo(self):
        self.handler = SentriesHandler
        self.execute_handler_tests('battles/sentries/sentry_yolo_state_with_three.json', ['play 5 0'])

    def test_returns_to_normal_battle_handler_after_one_is_dead(self):
        self.handler = CommonBattleHandler
        self.execute_handler_tests('battles/sentries/sentry_one_dead.json')


if __name__ == '__main__':
    unittest.main()
