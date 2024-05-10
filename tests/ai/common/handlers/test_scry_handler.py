from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_scry_handler import CommonScryHandler


class TestScryHandler(CoTestHandlerFixture):
    handler = CommonScryHandler

    def test_just_dismissing_scry(self):
        self.execute_handler_tests('/scry/do_not_break_when_scrying.json', ['wait 30', 'confirm'])

    def test_choose_card_to_pass_over(self):
        self.execute_handler_tests('/scry/simple_scry.json',
                                   ['wait 15', 'choose 0', 'wait 15', 'choose 2', 'wait 30', 'confirm'])
