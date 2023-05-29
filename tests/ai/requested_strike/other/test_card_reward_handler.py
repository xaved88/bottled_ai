from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.common.handlers.card_reward.common_card_reward_handler import CommonCardRewardHandler


class CardRewardHandlerTestCase(RsTestHandlerFixture):
    handler = CommonCardRewardHandler

    def test_select_card(self):
        self.execute_handler_tests('/card_reward/card_reward_take.json', ['choose 2', 'wait 30'])

    def test_skip(self):
        self.execute_handler_tests('/card_reward/card_reward_skip.json', ['skip', 'proceed'])
