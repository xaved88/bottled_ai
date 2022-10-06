from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.card_reward_handler import CardRewardHandler


class CardRewardHandlerTestCase(RsTestHandlerFixture):
    handler = CardRewardHandler

    def test_select_card(self):
        self.execute_handler_tests('/card_reward/card_reward_take.json', ['wait 30', 'choose 2', 'wait 30'])

    def test_skip(self):
        self.execute_handler_tests('/card_reward/card_reward_skip.json', ['skip', 'proceed'])
