from ai.peaceful_pummeling.pp_test_handler_fixture import PpTestHandlerFixture
from rs.ai.peaceful_pummeling.handlers.card_reward_handler import CardRewardHandler


class TestEventHandler(PpTestHandlerFixture):
    handler = CardRewardHandler

    def test_library_card_selection(self):
        self.execute_handler_tests('/card_reward/peaceful_pummeling_event_library_select_card.json',
                                   ['choose 16', 'wait 30'])

    def test_library_nothing_desirable(self):
        self.execute_handler_tests('/card_reward/peaceful_pummeling_event_library_nothing_desirable.json',
                                   ['choose 0', 'wait 30'])
