import unittest

from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.synergy_handlers.scaling_battle_handler import ScalingBattleHandler


class ScalingBattleHandlerTestCase(RsTestHandlerFixture):
    handler = ScalingBattleHandler
    ai_handlers = [ScalingBattleHandler()]

    def test_plays_inflame(self):
        self.execute_handler_tests('battles/Synergies/should_play_inflame.json', ['play 1'])

