
from ai.requested_strike.requested_scaling.synergy_choosing_text_fixture import SynergyCardRewardHandlerFixture
from rs.ai.requested_scaling.handlers.synergy_handlers.synergy_card_reward_handler import SynergyCardRewardHandler


class SynergyCardRewardHandlerTest(SynergyCardRewardHandlerFixture):
    handler = SynergyCardRewardHandler

    def test_plays_inflame(self):
        self.execute_handler_tests('battles/Synergies/smarter_card_reward_testing.json', [])

