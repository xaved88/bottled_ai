from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.neow_handler import NeowHandler


class TestNeowHandler(RsTestHandlerFixture):
    handler = NeowHandler

    def test_handle_neow(self):
        self.execute_handler_tests('/other/event_neow.json', ['choose obtain a random common relic', 'wait 30'])
