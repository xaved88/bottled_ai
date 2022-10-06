from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.purge_handler import PurgeHandler


class TestPurgeHandler(RsTestHandlerFixture):
    handler = PurgeHandler

    def test_regular_purge(self):
        self.execute_handler_tests('/other/purge_regular.json', ['choose 5', 'wait 30'])

    def test_empty_cage(self):
        self.execute_handler_tests('/other/purge_empty_cage.json', ['choose 5', 'wait 30', 'choose 6', 'wait 30'])
