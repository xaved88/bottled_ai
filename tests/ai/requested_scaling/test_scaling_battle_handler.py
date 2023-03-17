import unittest

from ai.requested_scaling.fixtures.scaling_text_fixture import ScalingHandlerFixture
from rs.ai.requested_scaling.handlers.synergy_handlers.scaling_battle_handler import ScalingBattleHandler


class ScalingHandlerTest(ScalingHandlerFixture):
    handler = ScalingBattleHandler


    def ignore_scaling_if_snecko_and_card_is_more_expensive(self):
        self.execute_handler_tests('battles/synergy_states/handle_scaling_with_no_energy.json', [])

