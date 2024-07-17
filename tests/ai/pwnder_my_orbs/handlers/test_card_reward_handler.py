from ai.pwnder_my_orbs.pmo_test_handler_fixture import PmoTestHandlerFixture
from rs.ai.pwnder_my_orbs.handlers.card_reward_handler import CardRewardHandler


class CardRewardHandlerTestCase(PmoTestHandlerFixture):
    handler = CardRewardHandler

    def test_pick_up_some_card(self):
        self.execute_handler_tests('/card_reward/pwnder_my_orbs_card_reward_take.json', ['choose 0', 'wait 30'])

    def test_pick_up_higher_prio_in_group(self):
        self.execute_handler_tests('/card_reward/pwnder_my_orbs_card_reward_take_higher_prio_in_group.json',
                                   ['choose 0', 'wait 30'])

    def test_pick_up_higher_prio_different_group(self):
        self.execute_handler_tests('/card_reward/pwnder_my_orbs_card_reward_take_higher_prio_different_group.json',
                                   ['choose 1', 'wait 30'])

    def test_skip_because_enough_single_card(self):
        self.execute_handler_tests('/card_reward/pwnder_my_orbs_card_reward_skip_because_enough_single_card.json',
                                   ['skip', 'proceed'])

    def test_skip_because_enough_group(self):
        self.execute_handler_tests('/card_reward/pwnder_my_orbs_card_reward_skip_because_enough_group.json',
                                   ['skip', 'proceed'])

    def test_take_from_lower_group_because_group_full(self):
        self.execute_handler_tests(
            '/card_reward/pwnder_my_orbs_card_reward_take_from_lower_group_because_group_full.json',
            ['choose 2', 'wait 30'])
