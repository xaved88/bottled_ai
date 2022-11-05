from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.discard_handler import DiscardHandler


class TestEventHandler(RsTestHandlerFixture):
    handler = DiscardHandler

    def test_handle_discard_with_relic(self):
        self.execute_handler_tests('/other/discard_relic.json', ['choose strike'])

    def test_handle_discard_with_relic_curse(self):
        self.execute_handler_tests('/other/discard_relic_curse.json', ['choose pain'])

    def test_handle_discard_with_relic_done(self):
        self.execute_handler_tests('/other/discard_relic_done.json', ['confirm'])

    def test_handle_discard_everything_discarded(self):
        self.execute_handler_tests('/other/discarded_everything.json', ['confirm'])