import unittest

from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.synergy_handlers.scaling_battle_handler import ScalingBattleHandler


class ScalingBattleHandlerTestCase(RsTestHandlerFixture):
    handler = ScalingBattleHandler

    ai_handlers = [ScalingBattleHandler()]

    def test_plays_bash(self):
        self.execute_handler_tests('battles/general/battle_should_play_bash.json', ['play 2 0'])

    def test_woke_blokes_transformation(self):
        self.execute_handler_tests('battles/general/battle_woke_bloke_transforming.json', ["end"])


if __name__ == '__main__':
    unittest.main()
