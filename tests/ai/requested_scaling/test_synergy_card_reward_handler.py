from ai.requested_scaling.fixtures.synergy_choosing_text_fixture import SynergyCardRewardHandlerFixture
from rs.ai.requested_scaling.handlers.synergy_handlers.synergy_card_reward_handler import SynergyCardRewardHandler


class SynergyCardRewardHandlerTest(SynergyCardRewardHandlerFixture):
    handler = SynergyCardRewardHandler

    def test_early_damage_check(self):
        # choices: body slam, fire breathing and twin strike. Should pick twin strike
        self.execute_handler_tests('card_reward/synergy_card_reward_states/smarter_card_reward_testing.json',
                                   ['wait 30', 'choose twin strike', 'wait 30'])

