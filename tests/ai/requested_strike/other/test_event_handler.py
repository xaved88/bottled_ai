from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.event_handler import EventHandler


class TestEventHandler(RsTestHandlerFixture):
    handler = EventHandler

    def test_handle_purifier(self):
        self.execute_handler_tests('/other/event_purifier.json', ['choose 0', 'wait 30'])
