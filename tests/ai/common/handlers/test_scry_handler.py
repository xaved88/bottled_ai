from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from config import p_delay
from rs.common.handlers.common_scry_handler import CommonScryHandler


class TestScryHandler(CoTestHandlerFixture):
    handler = CommonScryHandler

    def test_just_dismissing_scry(self):
        self.execute_handler_tests('/other/do_not_die_to_scrying.json', ['confirm'])
