from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_chest_handler import CommonChestHandler


class ChestHandlerTestCase(CoTestHandlerFixture):
    handler = CommonChestHandler

    def test_normal_chest_open(self):
        self.execute_handler_tests('/other/chest_medium_reward.json', ['choose 0', 'wait 30'])

    def test_open_chest_with_cursed_key_if_no_curse(self):
        self.execute_handler_tests('/other/chest_with_cursed_key_and_no_curses.json', ['choose 0', 'wait 30'])

    def test_open_chest_with_cursed_key_if_omamori(self):
        self.execute_handler_tests('/other/chest_with_cursed_key_and_omamori.json', ['choose 0', 'wait 30'])

    def test_skip_chest_with_cursed_key_and_too_many_curses(self):
        self.execute_handler_tests('/other/chest_with_cursed_key_and_curses.json', ['proceed'])
