import unittest

from ai.requested_strike.requested_scaling.scaling_text_fixture import ScalingHandlerFixture
from rs.ai.requested_scaling.handlers.synergy_handlers.scaling_battle_handler import ScalingBattleHandler


class ScalingHandlerTest(ScalingHandlerFixture):
    handler = ScalingBattleHandler

    def test_plays_inflame(self):
        self.execute_handler_tests('battles/Synergies/not_play_limit_break.json', [])

