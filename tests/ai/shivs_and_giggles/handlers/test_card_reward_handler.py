from ai.shivs_and_giggles.sg_test_handler_fixture import SgTestHandlerFixture
from rs.ai.shivs_and_giggles.handlers.card_reward_handler import CardRewardHandler


class CardRewardHandlerTestCase(SgTestHandlerFixture):
    handler = CardRewardHandler

    def test_snecko_skip(self):
        self.execute_handler_tests('/card_reward/shivs_and_giggles_card_reward_snecko_eye_skip.json', ['skip', 'proceed'])

    def test_snecko_eye_take_other(self):
        self.execute_handler_tests('/card_reward/shivs_and_giggles_card_reward_snecko_eye_take_other.json', ['choose 1', 'wait 30'])