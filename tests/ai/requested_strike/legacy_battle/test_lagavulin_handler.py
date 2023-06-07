from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.custom_legacy_battle.lagavulin_handler import LagavulinHandler


class LagavulinHandlerTestCase(RsTestHandlerFixture):
    handler = LagavulinHandler

    def test_plays_bash(self):
        self.execute_handler_tests('battles/lagavulin/lagavulin_bash_turn_one.json', ['play 3 0'])
