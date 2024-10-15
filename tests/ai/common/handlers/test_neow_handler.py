from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_neow_handler import CommonNeowHandler


class TestNeowHandler(CoTestHandlerFixture):
    handler = CommonNeowHandler

    def test_handle_neow(self):
        self.execute_handler_tests('/event/event_neow.json', ['choose obtain a random common relic', 'wait 30'])
